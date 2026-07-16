#!/usr/bin/env python3
"""Record Brand VI asset state and invalidate descendants of changed masters."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import mimetypes
import struct
from pathlib import Path
from typing import Any


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int] | None:
    header = path.read_bytes()[:24]
    if len(header) >= 24 and header.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", header[16:24])
    return None


def output_record(path: Path, root: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    try:
        relative = resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"output must be inside root: {resolved}") from error
    if not resolved.is_file() or resolved.stat().st_size == 0:
        raise ValueError(f"output is missing or empty: {resolved}")
    output: dict[str, Any] = {
        "path": str(relative),
        "mediaType": mimetypes.guess_type(resolved.name)[0]
        or "application/octet-stream",
        "bytes": resolved.stat().st_size,
        "sha256": sha256_file(resolved),
    }
    if dimensions := png_dimensions(resolved):
        width, height = dimensions
        divisor = math.gcd(width, height)
        output.update(
            {
                "width": width,
                "height": height,
                "aspectRatio": f"{width // divisor}:{height // divisor}",
            }
        )
    return output


def descendants(assets: list[dict[str, Any]], parent_id: str) -> set[str]:
    result = set()
    frontier = {parent_id}
    while frontier:
        next_frontier = {
            asset["id"]
            for asset in assets
            if asset.get("id") not in result
            and any(
                dependency in frontier for dependency in asset.get("dependencies", [])
            )
        }
        result.update(next_frontier)
        frontier = next_frontier
    return result


def update_plan(
    path: Path,
    plan_item: str | None,
    status: str,
    reason: str | None,
    resume_action: str | None,
) -> None:
    if not plan_item or not path.is_file():
        return
    plan = json.loads(path.read_text(encoding="utf-8"))
    item = next(
        (
            candidate
            for candidate in plan.get("items", [])
            if candidate.get("id") == plan_item
        ),
        None,
    )
    if item is None:
        raise ValueError(f"plan item not found: {plan_item}")
    if status in {"complete", "blocked", "not-applicable", "external-handoff"}:
        item["status"] = status
    if status == "blocked":
        if not reason or not resume_action:
            raise ValueError("blocked status requires --reason and --resume-action")
        item["blocker"] = reason
        item["resume_action"] = resume_action
    path.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--asset", required=True)
    parser.add_argument("--status", choices=sorted(STATUSES), required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--reviewed", action="store_true")
    parser.add_argument("--check", action="append", default=[])
    parser.add_argument("--reason")
    parser.add_argument("--resume-action")
    parser.add_argument("--plan", type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    root = args.root.expanduser().resolve() if args.root else manifest_path.parent
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assets = manifest.get("assets", [])
    asset = next(
        (candidate for candidate in assets if candidate.get("id") == args.asset),
        None,
    )
    if asset is None:
        raise SystemExit(f"asset not found: {args.asset}")
    if args.status in OUTPUT_STATUSES and args.output is None:
        raise SystemExit(f"status {args.status} requires --output")
    if (
        args.status in {"accepted", "complete", "external-handoff"}
        and not args.reviewed
    ):
        raise SystemExit(f"status {args.status} requires --reviewed")
    if args.status == "blocked" and (not args.reason or not args.resume_action):
        raise SystemExit("blocked status requires --reason and --resume-action")

    old_sha = (asset.get("output") or {}).get("sha256")
    old_status = asset.get("status")
    asset["status"] = args.status
    if args.output is not None:
        asset["output"] = output_record(args.output, root)
    if args.reviewed:
        asset["validation"] = {
            "reviewed": True,
            "checks": args.check or ["human-review"],
        }
    if args.reason:
        asset["statusReason"] = args.reason
    if args.status == "blocked":
        asset["blocker"] = args.reason

    new_sha = (asset.get("output") or {}).get("sha256")
    invalidated = []
    if (
        old_status in {"accepted", "complete"}
        and old_sha
        and new_sha
        and old_sha != new_sha
    ):
        for child_id in sorted(descendants(assets, args.asset)):
            child = next(item for item in assets if item.get("id") == child_id)
            child["status"] = "invalidated"
            child["statusReason"] = f"dependency {args.asset} changed checksum"
            child.pop("output", None)
            child.pop("validation", None)
            invalidated.append(child_id)

    plan_path = (
        args.plan.expanduser().resolve()
        if args.plan
        else manifest_path.with_name("brand-vi-production-plan.json")
    )
    update_plan(
        plan_path,
        asset.get("planItem"),
        args.status,
        args.reason,
        args.resume_action,
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{args.asset}: {args.status}")
    if invalidated:
        print("invalidated descendants: " + ", ".join(invalidated))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
