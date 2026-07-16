#!/usr/bin/env python3
"""Validate a Brand VI asset manifest without third-party dependencies."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import struct
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROLES = {"deliverable", "derivative", "dependency", "exploration", "evidence"}
STATUSES = {
    "planned",
    "generated",
    "accepted",
    "complete",
    "rejected",
    "blocked",
    "invalidated",
    "not-applicable",
    "external-handoff",
}
OUTPUT_STATUSES = {"generated", "accepted", "complete", "external-handoff"}
APPROVED_STATUSES = {"accepted", "complete", "external-handoff"}
COUNTED_ROLES = {"deliverable", "derivative"}
TERMINAL_PLAN_STATUSES = {"complete", "blocked", "not-applicable", "external-handoff"}


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        header = path.read_bytes()[:24]
    except OSError:
        return None
    if len(header) >= 24 and header.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", header[16:24])
    return None


def parse_ratio(value: str) -> float | None:
    try:
        width, height = value.split(":", 1)
        width_value = float(width)
        height_value = float(height)
    except (AttributeError, TypeError, ValueError):
        return None
    if width_value <= 0 or height_value <= 0:
        return None
    return width_value / height_value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_svg(path: Path) -> list[str]:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as error:
        return [f"invalid SVG XML: {error}"]
    errors = []
    if not root.tag.endswith("svg"):
        errors.append("SVG root element is not <svg>")
    if not root.get("viewBox"):
        errors.append("SVG requires viewBox")
    graphic_names = {
        "path",
        "rect",
        "circle",
        "ellipse",
        "polygon",
        "polyline",
        "line",
        "text",
        "use",
    }
    if not any(
        element.tag.rsplit("}", 1)[-1] in graphic_names for element in root.iter()
    ):
        errors.append("SVG contains no graphic elements")
    return errors


def validate_font_header(path: Path) -> list[str]:
    try:
        header = path.read_bytes()[:4]
    except OSError as error:
        return [f"cannot read font: {error}"]
    expected = {
        ".ttf": {b"\x00\x01\x00\x00", b"true"},
        ".otf": {b"OTTO"},
        ".woff2": {b"wOF2"},
    }
    if header not in expected.get(path.suffix.lower(), set()):
        return [f"invalid {path.suffix.lower()} header"]
    return []


def validate_manifest(
    data: Any,
    root: Path,
    plan: dict[str, Any] | None = None,
    production_complete: bool = False,
    allow_empty: bool = False,
) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    summary = {"assets": 0, "counted": 0, "dependencies": 0, "accepted": 0}
    if not isinstance(data, dict):
        return ["manifest must be a JSON object"], summary
    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion must equal 1")
    if not isinstance(data.get("brand"), str) or not data["brand"].strip():
        errors.append("brand must be a non-empty string")
    assets = data.get("assets")
    if not isinstance(assets, list):
        return errors + ["assets must be an array"], summary
    if not assets and not allow_empty:
        errors.append("assets must contain at least one planned or produced asset")

    summary["assets"] = len(assets)
    by_id: dict[str, dict[str, Any]] = {}
    output_paths: set[str] = set()
    assets_by_plan_item: dict[str, list[dict[str, Any]]] = {}

    for index, asset in enumerate(assets):
        prefix = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{prefix} must be an object")
            continue
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not asset_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
            continue
        prefix = f"asset {asset_id!r}"
        if asset_id in by_id:
            errors.append(f"duplicate asset id: {asset_id}")
        else:
            by_id[asset_id] = asset

        if not isinstance(asset.get("name"), str) or not asset["name"].strip():
            errors.append(f"{prefix}: name must be a non-empty string")
        role = asset.get("role")
        status = asset.get("status")
        if role not in ROLES:
            errors.append(f"{prefix}: invalid role {role!r}")
        if status not in STATUSES:
            errors.append(f"{prefix}: invalid status {status!r}")
        if status == "blocked" and not (
            isinstance(asset.get("blocker"), str) and asset["blocker"].strip()
        ):
            errors.append(f"{prefix}: blocked status requires blocker")
        if (
            not isinstance(asset.get("assetClass"), str)
            or not asset["assetClass"].strip()
        ):
            errors.append(f"{prefix}: assetClass must be a non-empty string")
        plan_item = asset.get("planItem")
        if plan_item is not None:
            if not isinstance(plan_item, str) or not plan_item.strip():
                errors.append(f"{prefix}: planItem must be a non-empty string")
            else:
                assets_by_plan_item.setdefault(plan_item, []).append(asset)
        dependencies = asset.get("dependencies")
        if not isinstance(dependencies, list) or not all(
            isinstance(item, str) for item in dependencies
        ):
            errors.append(f"{prefix}: dependencies must be an array of asset ids")
            dependencies = []
        elif len(dependencies) != len(set(dependencies)):
            errors.append(f"{prefix}: dependencies must be unique")
        if asset_id in dependencies:
            errors.append(f"{prefix}: asset cannot depend on itself")

        if role in COUNTED_ROLES:
            summary["counted"] += 1
        if role == "dependency":
            summary["dependencies"] += 1
        if status in APPROVED_STATUSES:
            summary["accepted"] += 1

        output = asset.get("output")
        if status in OUTPUT_STATUSES and not isinstance(output, dict):
            errors.append(f"{prefix}: status {status!r} requires output")
            continue
        if not isinstance(output, dict):
            continue
        relative_path = output.get("path")
        if not isinstance(relative_path, str) or not relative_path.strip():
            errors.append(f"{prefix}: output.path must be a non-empty string")
            continue
        if Path(relative_path).is_absolute():
            errors.append(f"{prefix}: output.path must be relative: {relative_path}")
            continue
        if relative_path in output_paths:
            errors.append(f"duplicate output path: {relative_path}")
        output_paths.add(relative_path)
        resolved = (root / relative_path).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{prefix}: output.path escapes root: {relative_path}")
            continue
        if status in OUTPUT_STATUSES:
            if not resolved.is_file():
                errors.append(f"{prefix}: output file not found: {relative_path}")
                continue
            if resolved.stat().st_size == 0:
                errors.append(f"{prefix}: output file is empty: {relative_path}")
                continue

            actual_bytes = resolved.stat().st_size
            if output.get("bytes") is not None and output["bytes"] != actual_bytes:
                errors.append(
                    f"{prefix}: bytes {output['bytes']} does not match file size {actual_bytes}"
                )
            expected_sha = output.get("sha256")
            if status in APPROVED_STATUSES and expected_sha is None:
                errors.append(f"{prefix}: status {status!r} requires output.sha256")
            if expected_sha is not None:
                if not isinstance(expected_sha, str) or not re_full_sha256(
                    expected_sha
                ):
                    errors.append(
                        f"{prefix}: output.sha256 must be 64 lowercase hex characters"
                    )
                elif expected_sha != sha256_file(resolved):
                    errors.append(f"{prefix}: output.sha256 does not match file")
            if status in APPROVED_STATUSES and output.get("bytes") is None:
                errors.append(f"{prefix}: status {status!r} requires output.bytes")

        dimensions = (
            png_dimensions(resolved) if resolved.suffix.lower() == ".png" else None
        )
        if dimensions:
            actual_width, actual_height = dimensions
            if output.get("width") is not None and output["width"] != actual_width:
                errors.append(
                    f"{prefix}: width {output['width']} does not match PNG header {actual_width}"
                )
            if output.get("height") is not None and output["height"] != actual_height:
                errors.append(
                    f"{prefix}: height {output['height']} does not match PNG header {actual_height}"
                )
            if ratio_text := output.get("aspectRatio"):
                expected_ratio = parse_ratio(ratio_text)
                if expected_ratio is None:
                    errors.append(f"{prefix}: invalid aspectRatio {ratio_text!r}")
                elif abs((actual_width / actual_height) - expected_ratio) > 0.005:
                    errors.append(
                        f"{prefix}: aspectRatio {ratio_text} does not match {actual_width}x{actual_height}"
                    )

        if resolved.suffix.lower() == ".svg" and resolved.is_file():
            errors.extend(f"{prefix}: {error}" for error in validate_svg(resolved))
        if resolved.suffix.lower() in {".ttf", ".otf", ".woff2"} and resolved.is_file():
            errors.extend(
                f"{prefix}: {error}" for error in validate_font_header(resolved)
            )

        if role in COUNTED_ROLES and status in APPROVED_STATUSES:
            validation = asset.get("validation")
            if (
                not isinstance(validation, dict)
                or validation.get("reviewed") is not True
            ):
                errors.append(
                    f"{prefix}: accepted counted asset requires validation.reviewed=true"
                )

    for asset_id, asset in by_id.items():
        for dependency in asset.get("dependencies", []):
            if dependency not in by_id:
                errors.append(f"asset {asset_id!r}: unknown dependency {dependency!r}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(asset_id: str, trail: list[str]) -> None:
        if asset_id in visiting:
            errors.append(f"dependency cycle: {' -> '.join(trail + [asset_id])}")
            return
        if asset_id in visited or asset_id not in by_id:
            return
        visiting.add(asset_id)
        for dependency in by_id[asset_id].get("dependencies", []):
            visit(dependency, trail + [asset_id])
        visiting.remove(asset_id)
        visited.add(asset_id)

    for asset_id in by_id:
        visit(asset_id, [])

    if plan is not None:
        plan_items = plan.get("items") if isinstance(plan, dict) else None
        if not isinstance(plan_items, list):
            errors.append("production plan must contain an items array")
        else:
            known_plan_items = {
                item.get("id"): item
                for item in plan_items
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            }
            for plan_item in assets_by_plan_item:
                if plan_item not in known_plan_items:
                    errors.append(
                        f"manifest references unknown plan item {plan_item!r}"
                    )
            for item_id, item in known_plan_items.items():
                requirement = item.get("requirement")
                if (
                    requirement in {"required", "external-handoff"}
                    and item_id not in assets_by_plan_item
                ):
                    errors.append(f"plan item {item_id!r} has no manifest asset")
                if not production_complete or requirement == "optional":
                    continue
                status = item.get("status")
                if status not in TERMINAL_PLAN_STATUSES:
                    errors.append(f"plan item {item_id!r} is not terminal: {status!r}")
                if requirement == "required" and status == "complete":
                    item_assets = assets_by_plan_item.get(item_id, [])
                    if not any(
                        asset.get("status") == "complete" for asset in item_assets
                    ):
                        errors.append(
                            f"complete plan item {item_id!r} has no complete manifest asset"
                        )
                if requirement == "external-handoff" and status == "external-handoff":
                    item_assets = assets_by_plan_item.get(item_id, [])
                    if not any(
                        asset.get("status") == "external-handoff"
                        for asset in item_assets
                    ):
                        errors.append(
                            f"external-handoff plan item {item_id!r} has no external-handoff manifest asset"
                        )
                if status == "blocked":
                    if not (
                        isinstance(item.get("blocker"), str) and item["blocker"].strip()
                    ):
                        errors.append(f"blocked plan item {item_id!r} requires blocker")
                    if not (
                        isinstance(item.get("resume_action"), str)
                        and item["resume_action"].strip()
                    ):
                        errors.append(
                            f"blocked plan item {item_id!r} requires resume_action"
                        )
                    item_assets = assets_by_plan_item.get(item_id, [])
                    if not any(
                        asset.get("status") == "blocked" for asset in item_assets
                    ):
                        errors.append(
                            f"blocked plan item {item_id!r} has no blocked manifest asset"
                        )
            if production_complete:
                unfinished = [
                    asset.get("id")
                    for asset in assets
                    if asset.get("role") in COUNTED_ROLES
                    and asset.get("status")
                    not in {"complete", "blocked", "not-applicable", "external-handoff"}
                ]
                if unfinished:
                    errors.append(
                        f"counted assets are not terminal: {', '.join(str(item) for item in unfinished)}"
                    )

    return errors, summary


def re_full_sha256(value: str) -> bool:
    return len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def self_test() -> int:
    one_pixel_png = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl2nWQAAAAASUVORK5CYII="
    )
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "anchor.png").write_bytes(one_pixel_png)
        (root / "skin.png").write_bytes(one_pixel_png)
        valid = {
            "schemaVersion": 1,
            "brand": "Self Test",
            "assets": [
                {
                    "id": "anchor",
                    "name": "Family anchor",
                    "role": "dependency",
                    "assetClass": "family-anchor",
                    "status": "accepted",
                    "dependencies": [],
                    "output": {
                        "path": "anchor.png",
                        "width": 1,
                        "height": 1,
                        "aspectRatio": "1:1",
                        "bytes": len(one_pixel_png),
                        "sha256": hashlib.sha256(one_pixel_png).hexdigest(),
                    },
                },
                {
                    "id": "skin",
                    "name": "Skin master",
                    "role": "deliverable",
                    "assetClass": "symbol-skin-master",
                    "status": "accepted",
                    "dependencies": ["anchor"],
                    "output": {
                        "path": "skin.png",
                        "width": 1,
                        "height": 1,
                        "aspectRatio": "1:1",
                        "bytes": len(one_pixel_png),
                        "sha256": hashlib.sha256(one_pixel_png).hexdigest(),
                    },
                    "validation": {"reviewed": True, "checks": ["identity-fidelity"]},
                },
            ],
        }
        errors, _ = validate_manifest(valid, root)
        if errors:
            print("self-test valid fixture failed:")
            print("\n".join(errors))
            return 1
        invalid = json.loads(json.dumps(valid))
        invalid["assets"][1]["dependencies"] = ["missing"]
        invalid["assets"][1]["output"]["width"] = 2
        invalid["assets"][1]["validation"]["reviewed"] = False
        invalid["assets"].append(
            {
                "id": "blocked",
                "name": "Blocked item",
                "role": "deliverable",
                "assetClass": "test",
                "status": "blocked",
                "dependencies": [],
            }
        )
        errors, _ = validate_manifest(invalid, root)
        if len(errors) < 4:
            print(f"self-test invalid fixture produced too few errors: {errors}")
            return 1
    print("self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", help="Path to brand-asset-manifest.json")
    parser.add_argument("--root", help="Root used to resolve asset output paths")
    parser.add_argument(
        "--json", action="store_true", help="Print machine-readable result"
    )
    parser.add_argument("--plan", help="Production plan used for item reconciliation")
    parser.add_argument(
        "--production-complete",
        action="store_true",
        help="Require terminal plan items and complete counted assets",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow an empty draft manifest; never use for completion",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in valid and invalid fixtures",
    )
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.manifest:
        parser.error("manifest is required unless --self-test is used")

    manifest_path = Path(args.manifest).expanduser().resolve()
    root = Path(args.root).expanduser().resolve() if args.root else manifest_path.parent
    plan_path = (
        Path(args.plan).expanduser().resolve()
        if args.plan
        else manifest_path.with_name("brand-vi-production-plan.json")
    )
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"failed to read manifest: {error}") from error

    plan = None
    if plan_path.is_file():
        try:
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise SystemExit(f"failed to read production plan: {error}") from error
    elif args.plan or args.production_complete:
        raise SystemExit(f"production plan not found: {plan_path}")

    errors, summary = validate_manifest(
        data,
        root,
        plan=plan,
        production_complete=args.production_complete,
        allow_empty=args.allow_empty,
    )
    result = {
        "ok": not errors,
        "manifest": str(manifest_path),
        "root": str(root),
        **summary,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    elif errors:
        print(f"manifest invalid: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
    else:
        print(
            "manifest valid: "
            f"{summary['assets']} assets, {summary['counted']} counted, "
            f"{summary['dependencies']} dependencies, {summary['accepted']} accepted"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
