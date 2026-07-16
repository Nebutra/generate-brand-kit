#!/usr/bin/env python3
"""Compile an edited item-level Brand VI scope without resetting design work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from create_brand_vi_scaffold import (
    REQUIREMENTS,
    asset_manifest,
    inventory_template,
    load_catalog,
    load_routing,
    production_plan,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--brand-root", default="resources/brand")
    parser.add_argument("--scope-file")
    parser.add_argument(
        "--force", action="store_true", help="Replace draft compiled files"
    )
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    brand_root = repo / args.brand_root
    scope_path = (
        Path(args.scope_file).expanduser().resolve()
        if args.scope_file
        else brand_root / "brand-vi-scope.json"
    )
    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    catalog = load_catalog()
    routing = load_routing()
    brand = scope.get("brand")
    profile = scope.get("startingProfile", "none")
    philosophy = scope.get("philosophy", "")
    selected_modules = scope.get("selectedModules")
    requirements = scope.get("items")
    if not isinstance(brand, str) or not brand:
        raise SystemExit("scope.brand is required")
    if not isinstance(selected_modules, list) or not set(selected_modules) <= set(
        catalog["modules"]
    ):
        raise SystemExit("scope.selectedModules contains invalid modules")
    if not isinstance(requirements, dict):
        raise SystemExit("scope.items must be an object")
    expected_items = {
        f"{module}-{index:02d}"
        for module in selected_modules
        for index, _ in enumerate(catalog["modules"][module]["items"], start=1)
    }
    if set(requirements) != expected_items:
        missing = sorted(expected_items - set(requirements))
        extra = sorted(set(requirements) - expected_items)
        raise SystemExit(f"scope item mismatch; missing={missing}, extra={extra}")
    invalid = {
        item_id: requirement
        for item_id, requirement in requirements.items()
        if requirement not in REQUIREMENTS
    }
    if invalid:
        raise SystemExit(f"scope has invalid requirements: {invalid}")

    manifest_path = brand_root / "brand-asset-manifest.json"
    if manifest_path.is_file():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        active = [
            asset.get("id")
            for asset in existing.get("assets", [])
            if asset.get("status") not in {"planned"}
        ]
        if active:
            raise SystemExit(
                "refusing to reset an active manifest; reconcile scope manually for assets: "
                + ", ".join(str(item) for item in active)
            )

    outputs = {
        brand_root / "brand-vi-inventory.md": inventory_template(
            brand,
            philosophy,
            profile,
            selected_modules,
            catalog,
            requirements,
        ),
    }
    plan_text = production_plan(
        brand,
        profile,
        selected_modules,
        catalog,
        routing,
        requirements,
    )
    outputs[brand_root / "brand-vi-production-plan.json"] = plan_text
    outputs[manifest_path] = asset_manifest(brand, plan_text)
    for path, content in outputs.items():
        if path.exists() and not args.force:
            raise SystemExit(
                f"{path} exists; inspect changes and pass --force for draft recompilation"
            )
        path.write_text(content, encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
