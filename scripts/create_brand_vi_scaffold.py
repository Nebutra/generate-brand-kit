#!/usr/bin/env python3
"""Create a production-oriented brand-VI scaffold for a repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CATALOG_PATH = Path(__file__).resolve().parent.parent / "references" / "vi-deliverables.json"
ROUTING_PATH = Path(__file__).resolve().parent.parent / "references" / "production-routing.json"
HANDOFF_MODULES = {"b3", "b6", "b7", "b9", "b10", "b11", "b12"}


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; pass --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_routing() -> dict:
    return json.loads(ROUTING_PATH.read_text(encoding="utf-8"))["routes"]


def production_plan(
    brand: str,
    profile: str,
    selected_modules: list[str],
    catalog: dict,
    routing: dict,
) -> str:
    items = [
        {
            "id": "strategy-001",
            "module": "cross-system",
            "deliverable": "Brand strategy, evidence labels, architecture, naming and verbal identity",
            "phase": "strategy",
            "producer": "strategy-document",
            "output": "visual-identity.md",
            "blocked_by": [],
            "status": "ready",
            "acceptance": "Evidence levels are explicit and strategy-approved gate is recorded",
        }
    ]
    for module in selected_modules:
        route = routing[module]
        gates = [gate for gate in route["gate"].split("+") if gate]
        for index, deliverable in enumerate(catalog["modules"][module]["items"], start=1):
            items.append(
                {
                    "id": f"{module}-{index:02d}",
                    "module": module,
                    "system": catalog["modules"][module]["name"],
                    "deliverable": deliverable,
                    "phase": route["phase"],
                    "producer": route["producer"],
                    "output_kind": route["output"],
                    "output": f"deliverables/{module}/{module}-{index:02d}",
                    "blocked_by": gates,
                    "creates_gate": route.get("creates_gate"),
                    "status": "planned",
                    "acceptance": "TBD before production",
                }
            )
    plan = {
        "schema_version": 1,
        "brand": brand,
        "starting_profile": profile,
        "selected_modules": selected_modules,
        "mode": "production",
        "definition_of_done": ["complete", "blocked", "not-applicable", "external-handoff"],
        "gates": {
            "strategy-approved": {"status": "pending", "blocks_only_declared_items": True},
            "mark-approved": {"status": "pending", "blocks_only_declared_items": True},
            "production-inputs": {"status": "pending", "blocks_only_declared_items": True},
            "evidence-available": {"status": "pending", "blocks_only_declared_items": True},
        },
        "items": items,
    }
    return json.dumps(plan, ensure_ascii=False, indent=2) + "\n"


def inventory_template(
    brand: str,
    philosophy: str,
    profile: str,
    selected_modules: list[str],
    catalog: dict,
) -> str:
    module_summary = ", ".join(module.upper() for module in selected_modules) or "none"
    rows = []
    for module in selected_modules:
        definition = catalog["modules"][module]
        delivery = "artwork/spec + specialist handoff where required" if module in HANDOFF_MODULES else "editable source + exports"
        for item in definition["items"]:
            rows.append(
                f"| {module.upper()} | {definition['name']} | {item} | required | {delivery} | planned | TBD |"
            )
    deliverable_rows = "\n".join(rows) or "| - | - | No modules selected | not applicable | - | - | - |"
    return f"""# {brand} Brand VI Inventory

## Brand Philosophy

{philosophy or "TBD"}

## Selection

- Starting profile: `{profile}`
- Selected modules: {module_summary}
- Status vocabulary: required / optional / not applicable / external handoff
- The profile is a starting point only; the selected module list is authoritative.

## Source Structure

- `approved/`: stable masters that downstream assets may reference.
- `generated/`: current generation outputs that are not yet approved.
- `processed/`: exported production assets derived from approved masters.

## Deliverable Matrix

| Module | System | Deliverable | Requirement | Output Level | Status | Acceptance Check |
| --- | --- | --- | --- | --- | --- | --- |
{deliverable_rows}

## Cross-System Requirements

- Brand strategy, verbal identity, rights register, naming/version rules, and ownership apply to every selection.
- Modules involving physical production require authoritative dimensions, substrate/process data, and supplier proof status.
- Concepts without those inputs must be labeled `external handoff`, not production-ready.

## Migration Notes

- Replace old brand names, old asset paths, generated outputs, and docs references.
- Delete rejected exploration files once approval is complete.
"""


def vi_template(brand: str, philosophy: str) -> str:
    return f"""# {brand} Visual Identity

## Core Idea

{philosophy or "TBD"}

## Name and Voice

- English name: {brand}
- Localized names: TBD
- Tone: TBD

## Strategy and Evidence

- Audience/category: TBD
- Positioning/value proposition: TBD
- Evidence labels: distinguish supplied facts, repo evidence, hypotheses, and research.

## Visual System

- Shape grammar: TBD
- Materials: TBD
- Palette: TBD
- Typography: follow the product's existing type system unless a brand surface requires otherwise.
- Imagery: TBD

## Usage Rules

- Clear space and minimum size: TBD
- Background and co-branding behavior: TBD
- Typography hierarchy and fallback: TBD
- Layout/grid and accessibility: TBD

## Rights and Specialist Handoffs

- Font/image/model/music licenses: TBD
- Trademark/legal review: external approval unless documented otherwise.
- Print, packaging, environment, motion, and sonic handoffs: TBD/not applicable.

## Negative Constraints

- No old brand mark.
- No ambiguous anatomical/suggestive silhouette.
- No generated text in raster backgrounds unless post-composed intentionally.
- No rejected exploration assets in product paths.
"""


def dag_template(brand: str) -> str:
    return f"""# {brand} independent symbol and wordmark exploration DAG

tasks:
  - id: symbol-family-1
    name: 01-symbol-family-1
    ratio: "1:1"
    prompt: >-
      Create exactly one isolated graphic symbol for {brand} in its intended
      brand palette. Start from one explicit business tension and one formal
      operation. No wordmark, letters, brand name, board, variants or mockup.

  - id: symbol-family-2
    name: 02-symbol-family-2
    ratio: "1:1"
    prompt: >-
      Create exactly one second structurally distinct graphic symbol for
      {brand}, governed by a different formal operation. No wordmark, letters,
      brand name, board, variants or mockup.

  - id: symbol-family-3
    name: 03-symbol-family-3
    ratio: "1:1"
    prompt: >-
      Create exactly one third structurally distinct graphic symbol for
      {brand}, governed by another formal operation. No wordmark, letters,
      brand name, board, variants or mockup.

  - id: wordmark-family-1
    name: 04-wordmark-family-1
    ratio: "3:2"
    prompt: >-
      Create exactly one typographic wordmark reading {brand}. Use one declared
      typography strategy and one restrained distinctive terminal or counter
      rule. No graphic symbol, icon, monogram, board, variants or extra text.

  - id: wordmark-family-2
    name: 05-wordmark-family-2
    ratio: "3:2"
    prompt: >-
      Create exactly one second structurally distinct typographic wordmark
      reading {brand}. Keep every letter immediately readable. No graphic
      symbol, icon, monogram, board, variants or extra text.

  # Compose approved symbol + approved wordmark deterministically after both
  # human gates. Do not add a combined image-generation task here.
"""


def main() -> int:
    catalog = load_catalog()
    routing = load_routing()
    profiles = sorted(catalog["profiles"])
    modules = sorted(catalog["modules"])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--brand", required=True, help="Brand/product name")
    parser.add_argument(
        "--output",
        default="resources/brand",
        help="Brand kit output directory relative to repo",
    )
    parser.add_argument("--philosophy", default="", help="One-line brand philosophy")
    parser.add_argument(
        "--profile",
        choices=["none", *profiles],
        default="digital-product",
        help="Starting module profile; customize it with include/exclude options",
    )
    parser.add_argument(
        "--include-module",
        action="append",
        choices=modules,
        default=[],
        help="Add a VI module such as b3 or b13; repeatable",
    )
    parser.add_argument(
        "--exclude-module",
        action="append",
        choices=modules,
        default=[],
        help="Remove a VI module from the starting profile; repeatable",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    args = parser.parse_args()

    selected = set() if args.profile == "none" else set(catalog["profiles"][args.profile])
    selected.update(args.include_module)
    selected.difference_update(args.exclude_module)
    selected_modules = [module for module in catalog["modules"] if module in selected]

    root = Path(args.repo).expanduser().resolve()
    out = root / args.output
    (out / "approved").mkdir(parents=True, exist_ok=True)
    (out / "generated").mkdir(parents=True, exist_ok=True)
    (out / "processed").mkdir(parents=True, exist_ok=True)
    for directory in ("approved", "generated", "processed"):
        keep = out / directory / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    write(
        out / "brand-vi-inventory.md",
        inventory_template(args.brand, args.philosophy, args.profile, selected_modules, catalog),
        args.force,
    )
    write(out / "visual-identity.md", vi_template(args.brand, args.philosophy), args.force)
    write(
        out / "brand-vi-production-plan.json",
        production_plan(args.brand, args.profile, selected_modules, catalog, routing),
        args.force,
    )
    write(out / "mark-exploration-dag.yaml", dag_template(args.brand), args.force)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
