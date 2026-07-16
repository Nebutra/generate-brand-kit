#!/usr/bin/env python3
"""Create a production-oriented brand-VI scaffold for a repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from compile_brand_image_dag import compilation_report, compile_exploration, dump_yaml


CATALOG_PATH = (
    Path(__file__).resolve().parent.parent / "references" / "vi-deliverables.json"
)
ROUTING_PATH = (
    Path(__file__).resolve().parent.parent / "references" / "production-routing.json"
)
HANDOFF_MODULES = {"b3", "b6", "b7", "b9", "b10", "b11", "b12"}
REQUIREMENTS = {"required", "optional", "not-applicable", "external-handoff"}


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; pass --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_routing() -> dict:
    return json.loads(ROUTING_PATH.read_text(encoding="utf-8"))


def item_ids(catalog: dict) -> list[str]:
    return [
        f"{module}-{index:02d}"
        for module, definition in catalog["modules"].items()
        for index, _ in enumerate(definition["items"], start=1)
    ]


def item_module(item_id: str) -> str:
    return item_id.rsplit("-", 1)[0]


def load_scope(path: str | None, known_items: set[str]) -> dict[str, str]:
    if not path:
        return {}
    scope_path = Path(path).expanduser().resolve()
    data = json.loads(scope_path.read_text(encoding="utf-8"))
    decisions = data.get("items") if isinstance(data, dict) else None
    if not isinstance(decisions, dict):
        raise ValueError("scope file must contain an object named 'items'")
    unknown = sorted(set(decisions) - known_items)
    invalid = sorted(
        f"{item_id}={requirement}"
        for item_id, requirement in decisions.items()
        if requirement not in REQUIREMENTS
    )
    if unknown or invalid:
        details = []
        if unknown:
            details.append(f"unknown item ids: {', '.join(unknown)}")
        if invalid:
            details.append(f"invalid requirements: {', '.join(invalid)}")
        raise ValueError("; ".join(details))
    return decisions


def resolve_route(item_id: str, module: str, routing: dict) -> dict:
    route = dict(routing["routes"][module])
    route.update(routing.get("item_overrides", {}).get(item_id, {}))
    return route


def acceptance_for(producer: str, output_kind: str) -> str:
    checks = {
        "identity-design": "Approved vector master, monochrome proof, 16/32 px tests, collision review and human approval exist",
        "identity-guidelines": "Rule is derived from the approved master and rendered in at least one correct and one misuse proof",
        "platform-icon": "Source geometry, required platform exports, alpha/mask behavior and in-context icon proofs pass",
        "qr-system": "Vector source, destination ownership, quiet zone and multi-device screen/print scans pass",
        "design-token": "DTCG source, generated code and product runtime values are byte/semantic-parity checked",
        "token-bridge": "Figma variables and code tokens have stable identifiers and an automated drift report",
        "component-library": "All interaction states, keyboard/screen-reader behavior and visual regression proofs pass",
        "theme-system": "Light, dark and high-contrast themes pass contrast, focus and non-color-state checks",
        "data-visualization": "Color, labels, keyboard/reader alternatives and representative dense/empty/error datasets pass",
        "state-system": "State matrix covers entry, progress, cancel, retry, recovery and partial-success paths",
        "credential-ux": "Secrets are redacted after creation; copy, revoke, error and audit flows are tested",
        "trust-evidence": "Every public claim has an owner, source, review date and approved evidence state",
        "email-template": "Editable source and rendered desktop/mobile/dark-mode proofs pass",
        "sonic-handoff": "Audio semantics, rights, format, loudness, mute behavior and a visual/static fallback are documented",
    }
    return checks.get(
        producer,
        f"Editable source, required exports and a rendered acceptance proof exist for {output_kind}",
    )


def production_plan(
    brand: str,
    profile: str,
    selected_modules: list[str],
    catalog: dict,
    routing: dict,
    requirements: dict[str, str],
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
            "requirement": "required",
            "acceptance": "Evidence levels are explicit and strategy-approved gate is recorded",
        }
    ]
    for module in selected_modules:
        for index, deliverable in enumerate(
            catalog["modules"][module]["items"], start=1
        ):
            item_id = f"{module}-{index:02d}"
            requirement = requirements[item_id]
            route = resolve_route(item_id, module, routing)
            gates = [gate for gate in route["gate"].split("+") if gate]
            items.append(
                {
                    "id": item_id,
                    "module": module,
                    "system": catalog["modules"][module]["name"],
                    "deliverable": deliverable,
                    "phase": route["phase"],
                    "producer": route["producer"],
                    "output_kind": route["output"],
                    "output": f"deliverables/{module}/{item_id}/",
                    "blocked_by": gates,
                    "creates_gate": route.get("creates_gate"),
                    "requirement": requirement,
                    "status": "not-applicable"
                    if requirement == "not-applicable"
                    else ("optional" if requirement == "optional" else "planned"),
                    "acceptance": acceptance_for(route["producer"], route["output"]),
                }
            )
    plan = {
        "schema_version": 1,
        "brand": brand,
        "starting_profile": profile,
        "selected_modules": selected_modules,
        "mode": "production",
        "definition_of_done": [
            "complete",
            "blocked",
            "not-applicable",
            "external-handoff",
        ],
        "gates": {
            "strategy-approved": {
                "status": "pending",
                "blocks_only_declared_items": True,
            },
            "mark-approved": {"status": "pending", "blocks_only_declared_items": True},
            "production-inputs": {
                "status": "pending",
                "blocks_only_declared_items": True,
            },
            "evidence-available": {
                "status": "pending",
                "blocks_only_declared_items": True,
            },
        },
        "items": items,
    }
    return json.dumps(plan, ensure_ascii=False, indent=2) + "\n"


def scope_document(
    brand: str,
    philosophy: str,
    profile: str,
    selected_modules: list[str],
    requirements: dict[str, str],
) -> str:
    data = {
        "schemaVersion": 1,
        "brand": brand,
        "philosophy": philosophy,
        "startingProfile": profile,
        "selectedModules": selected_modules,
        "items": requirements,
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def image_spec(brand: str, philosophy: str) -> dict:
    return {
        "schemaVersion": 1,
        "brand": brand,
        "philosophy": philosophy or "TBD: approved brand philosophy",
        "invariants": [
            "TBD: observable proportion or formal rule shared across the identity",
            "identity must remain readable at small size without explanatory copy",
        ],
        "negativeConstraints": [
            "no unrelated category symbol",
            "no accidental anatomical or suggestive silhouette",
        ],
        "explorationReferences": {"symbol": [], "wordmark": []},
        "symbolDirections": [
            {
                "id": "controlled-gap",
                "tension": "TBD: controlled versus autonomous",
                "operation": "one controlled gap",
                "distinctiveRule": "one silhouette and one intentional interruption",
            },
            {
                "id": "shared-axis",
                "tension": "TBD: individual versus system",
                "operation": "one shared axis",
                "distinctiveRule": "independent forms align without merging into a pictogram",
            },
            {
                "id": "phase-shift",
                "tension": "TBD: proposal versus approval",
                "operation": "one phase offset",
                "distinctiveRule": "a repeatable offset creates recognition without an arrow or sparkle",
            },
        ],
        "wordmarkDirections": [
            {
                "id": "controlled-terminal",
                "tension": "TBD: precise versus expressive",
                "operation": "one custom terminal rule",
                "distinctiveRule": "the same terminal behavior appears on multiple relevant letters",
            },
            {
                "id": "counterform",
                "tension": "TBD: open versus bounded",
                "operation": "one counterform rule",
                "distinctiveRule": "negative space remains readable without turning into a literal icon",
            },
            {
                "id": "rhythmic-offset",
                "tension": "TBD: stable versus adaptive",
                "operation": "one rhythmic offset",
                "distinctiveRule": "spacing and alignment carry the operation without harming spelling",
            },
        ],
        "skinFamilies": [],
        "productionApplications": [],
    }


def asset_manifest(brand: str, plan_text: str) -> str:
    plan = json.loads(plan_text)
    assets = []
    for item in plan["items"]:
        if item["requirement"] not in {"required", "external-handoff"}:
            continue
        assets.append(
            {
                "id": item["id"],
                "name": item["deliverable"],
                "planItem": item["id"],
                "role": "deliverable",
                "assetClass": item["producer"],
                "status": "planned",
                "dependencies": [],
                "usage": [],
            }
        )
    manifest = {
        "schemaVersion": 1,
        "brand": brand,
        "dag": "brand-vi-exploration-dag.yaml",
        "assets": assets,
    }
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def inventory_template(
    brand: str,
    philosophy: str,
    profile: str,
    selected_modules: list[str],
    catalog: dict,
    requirements: dict[str, str],
) -> str:
    module_summary = ", ".join(module.upper() for module in selected_modules) or "none"
    rows = []
    for module in selected_modules:
        definition = catalog["modules"][module]
        for index, item in enumerate(definition["items"], start=1):
            item_id = f"{module}-{index:02d}"
            requirement = requirements[item_id]
            delivery = (
                "artwork/spec + specialist handoff where required"
                if module in HANDOFF_MODULES
                else "editable source + exports"
            )
            rows.append(
                f"| {item_id} | {definition['name']} | {item} | {requirement} | {delivery} | {'not-applicable' if requirement == 'not-applicable' else ('optional' if requirement == 'optional' else 'planned')} | Defined in production plan |"
            )
    deliverable_rows = (
        "\n".join(rows)
        or "| - | - | No modules selected | not applicable | - | - | - |"
    )
    return f"""# {brand} Brand VI Inventory

## Brand Philosophy

{philosophy or "TBD"}

## Selection

- Starting profile: `{profile}`
- Selected modules: {module_summary}
- Requirement vocabulary: required / optional / not-applicable / external-handoff
- The profile is a starting point only; the selected module list is authoritative.
- Profile-seeded items default to optional. Only explicit scope decisions become required production work.

## Source Structure

- `approved/`: stable masters that downstream assets may reference.
- `generated/`: current generation outputs that are not yet approved.
- `processed/`: exported production assets derived from approved masters.

## Deliverable Matrix

| Item ID | System | Deliverable | Requirement | Output Level | Status | Acceptance Check |
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


def main() -> int:
    catalog = load_catalog()
    routing = load_routing()
    profiles = sorted(catalog["profiles"])
    modules = sorted(catalog["modules"])
    known_item_ids = item_ids(catalog)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--brand", required=True, help="Brand/product name")
    parser.add_argument(
        "--output",
        default="resources/brand",
        help="Brand kit output directory relative to repo",
    )
    parser.add_argument(
        "--scope-file", help="JSON file with an 'items' requirement map"
    )
    parser.add_argument(
        "--all-items-required",
        action="store_true",
        help="Explicitly require every item in selected modules",
    )
    for option, requirement in (
        ("require-item", "required"),
        ("optional-item", "optional"),
        ("not-applicable-item", "not-applicable"),
        ("external-handoff-item", "external-handoff"),
    ):
        parser.add_argument(
            f"--{option}",
            action="append",
            choices=known_item_ids,
            default=[],
            help=f"Set an item to {requirement}; repeatable",
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
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing scaffold files"
    )
    args = parser.parse_args()

    decisions = load_scope(args.scope_file, set(known_item_ids))
    cli_decisions = {}
    for attribute, requirement in (
        ("require_item", "required"),
        ("optional_item", "optional"),
        ("not_applicable_item", "not-applicable"),
        ("external_handoff_item", "external-handoff"),
    ):
        cli_decisions.update(
            {item_id: requirement for item_id in getattr(args, attribute)}
        )
    decisions.update(cli_decisions)

    selected = (
        set() if args.profile == "none" else set(catalog["profiles"][args.profile])
    )
    selected.update(args.include_module)
    selected.update(item_module(item_id) for item_id in decisions)
    selected.difference_update(args.exclude_module)
    selected_modules = [module for module in catalog["modules"] if module in selected]
    requirements = {}
    for module in selected_modules:
        for index, _ in enumerate(catalog["modules"][module]["items"], start=1):
            item_id = f"{module}-{index:02d}"
            requirements[item_id] = (
                "required" if args.all_items_required else "optional"
            )
    requirements.update(
        {
            item_id: value
            for item_id, value in decisions.items()
            if item_module(item_id) in selected
        }
    )

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
        inventory_template(
            args.brand,
            args.philosophy,
            args.profile,
            selected_modules,
            catalog,
            requirements,
        ),
        args.force,
    )
    write(
        out / "brand-vi-scope.json",
        scope_document(
            args.brand,
            args.philosophy,
            args.profile,
            selected_modules,
            requirements,
        ),
        args.force,
    )
    write(
        out / "visual-identity.md", vi_template(args.brand, args.philosophy), args.force
    )
    plan_text = production_plan(
        args.brand, args.profile, selected_modules, catalog, routing, requirements
    )
    write(out / "brand-vi-production-plan.json", plan_text, args.force)
    spec = image_spec(args.brand, args.philosophy)
    spec_text = json.dumps(spec, ensure_ascii=False, indent=2) + "\n"
    write(out / "brand-image-spec.json", spec_text, args.force)
    exploration_tasks = compile_exploration(spec)
    exploration_dag = dump_yaml(exploration_tasks)
    write(out / "brand-vi-exploration-dag.yaml", exploration_dag, args.force)
    write(
        out / "brand-vi-exploration-dag.report.json",
        json.dumps(
            compilation_report("exploration", exploration_tasks, exploration_dag),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        args.force,
    )
    write(
        out / "brand-asset-manifest.json",
        asset_manifest(args.brand, plan_text),
        args.force,
    )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
