#!/usr/bin/env python3
"""Compile stable Brand VI exploration or production prompts into a DAG."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


PROMPT_VERSION = "brand-vi-prompt-v1"
DEFAULT_NEGATIVES = [
    "no logo board or contact sheet",
    "no secondary candidate",
    "no caption or generated explanatory text",
    "no watermark",
    "no mockup unless the task explicitly requests one",
    "no decorative glow, glass, bevel, extrusion, or unrelated texture",
    "no literal category pictogram or familiar trademark imitation",
]


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not result:
        raise ValueError(f"cannot derive an id from {value!r}")
    return result


def lines(values: list[str]) -> str:
    return (
        "; ".join(value.strip() for value in values if value.strip()) or "none supplied"
    )


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def prompt_contract(
    *,
    task: str,
    strategy: str,
    invariants: list[str],
    reference_roles: list[str],
    mechanism: str,
    scene: str,
    negatives: list[str],
) -> str:
    sections = [
        f"TASK\n{task}",
        f"STRATEGY\n{strategy}",
        f"INVARIANT LOCK\n{lines(invariants)}",
        f"REFERENCE AUTHORITY\n{lines(reference_roles)}",
        f"ONE VARIATION MECHANISM\n{mechanism}",
        f"OUTPUT AND SCENE\n{scene}",
        f"NEGATIVE CONSTRAINTS\n{lines([*negatives, *DEFAULT_NEGATIVES])}",
    ]
    return "\n\n".join(sections)


def task_record(
    task_id: str,
    ratio: str,
    prompt: str,
    refs: list[str] | None = None,
    asset_class: str | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "id": task_id,
        "name": task_id,
        "ratio": ratio,
        "prompt": prompt,
    }
    if refs:
        record["refs"] = refs
    if asset_class:
        record["assetClass"] = asset_class
    return record


def exploration_references(
    spec: dict[str, Any],
    direction: dict[str, Any],
    asset_kind: str,
) -> tuple[list[str], list[str]]:
    entries = [
        *spec.get("explorationReferences", {}).get(asset_kind, []),
        *direction.get("references", []),
    ]
    paths = []
    roles = []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ValueError(
                f"{asset_kind} exploration references require path/role objects"
            )
        role = entry.get("role")
        if not isinstance(role, str) or not role.strip():
            raise ValueError(f"{asset_kind} reference {entry['path']} requires a role")
        paths.append(entry["path"])
        prohibited = entry.get("prohibited", "must not be copied as client identity")
        roles.append(f"Reference {index} controls only {role}; it {prohibited}.")
    if not roles:
        roles.append(
            "No visual reference controls form at exploration stage; use only the approved strategy and operation."
        )
    return paths, roles


def validate_spec(spec: dict[str, Any], allow_placeholders: bool = False) -> None:
    if spec.get("schemaVersion") != 1:
        raise ValueError("brand image spec schemaVersion must equal 1")
    if not isinstance(spec.get("brand"), str) or not spec["brand"].strip():
        raise ValueError("brand image spec requires a brand")
    if not allow_placeholders and "TBD" in json.dumps(spec, ensure_ascii=False):
        raise ValueError(
            "brand image spec still contains TBD; resolve it or pass --allow-placeholders for a draft"
        )
    for key in ("symbolDirections", "wordmarkDirections"):
        directions = spec.get(key, [])
        if directions and len(directions) < 3:
            raise ValueError(
                f"{key} must contain at least three structurally distinct directions"
            )
        ids = [slug(str(direction.get("id", ""))) for direction in directions]
        if len(ids) != len(set(ids)):
            raise ValueError(f"{key} contains duplicate ids")


def compile_exploration(spec: dict[str, Any]) -> list[dict[str, Any]]:
    brand = spec["brand"]
    philosophy = spec.get("philosophy", "")
    invariants = spec.get("invariants", [])
    negatives = spec.get("negativeConstraints", [])
    tasks = []
    for direction in spec.get("symbolDirections", []):
        direction_id = slug(direction["id"])
        refs, reference_roles = exploration_references(spec, direction, "symbol")
        prompt = prompt_contract(
            task=f"Create exactly one isolated black-and-white symbol candidate for {brand}.",
            strategy=f"Brand philosophy: {philosophy}. Business tension: {direction['tension']}.",
            invariants=invariants,
            reference_roles=reference_roles,
            mechanism=f"Use only {direction['operation']}. Distinctive rule: {direction['distinctiveRule']}.",
            scene="One centered flat black symbol on pure white, square 1:1. No wordmark, letters, board, scene, or mockup.",
            negatives=negatives,
        )
        tasks.append(
            task_record(
                f"symbol-{direction_id}",
                "1:1",
                prompt,
                refs,
                "symbol-exploration",
            )
        )
    for direction in spec.get("wordmarkDirections", []):
        direction_id = slug(direction["id"])
        refs, reference_roles = exploration_references(spec, direction, "wordmark")
        prompt = prompt_contract(
            task=f"Create exactly one isolated custom wordmark spelling {brand} with exact readable letters.",
            strategy=f"Brand philosophy: {philosophy}. Typographic tension: {direction['tension']}.",
            invariants=invariants,
            reference_roles=[
                *reference_roles,
                "No external typeface is a form donor unless the spec explicitly approves it.",
            ],
            mechanism=f"Use only {direction['operation']}. Distinctive rule: {direction['distinctiveRule']}.",
            scene="One flat black wordmark on pure white, wide 3:1. No symbol, alphabet, board, scene, or mockup.",
            negatives=negatives,
        )
        tasks.append(
            task_record(
                f"wordmark-{direction_id}",
                "3:1",
                prompt,
                refs,
                "wordmark-exploration",
            )
        )
    return tasks


def compile_production(
    spec: dict[str, Any],
    approved_symbol: str | None,
    approved_wordmark: str | None,
) -> list[dict[str, Any]]:
    if not approved_symbol and not approved_wordmark:
        raise ValueError(
            "production stage requires --approved-symbol and/or --approved-wordmark"
        )
    brand = spec["brand"]
    invariants = spec.get("invariants", [])
    negatives = spec.get("negativeConstraints", [])
    tasks: list[dict[str, Any]] = []
    canonical_refs: list[str] = []

    if approved_symbol:
        prompt = prompt_contract(
            task=f"Create the production-clean raster master for the approved {brand} symbol.",
            strategy="Preserve the approved identity; this is cleanup, not redesign.",
            invariants=[
                *invariants,
                "preserve exact silhouette, counterforms, proportion, posture, and orientation",
            ],
            reference_roles=[
                "Reference 1 is the approved canonical symbol and controls all geometry."
            ],
            mechanism="Remove generation debris and normalize only edge clarity.",
            scene="One centered flat symbol on transparent or pure white 1:1 as specified; no wordmark or surrounding layout.",
            negatives=negatives,
        )
        tasks.append(
            task_record(
                "symbol-production-master",
                "1:1",
                prompt,
                [approved_symbol],
                "symbol-master",
            )
        )
        canonical_refs.append("@symbol-production-master")

    if approved_wordmark:
        prompt = prompt_contract(
            task=f"Create the production-clean raster master for the approved {brand} wordmark.",
            strategy="Preserve the approved lettering; this is cleanup, not a new type direction.",
            invariants=[
                *invariants,
                "preserve exact letter anatomy, spacing rhythm, terminals, and baseline",
            ],
            reference_roles=[
                "Reference 1 is the approved canonical wordmark and controls all lettering geometry."
            ],
            mechanism="Remove generation debris and normalize only edge clarity.",
            scene="One flat wordmark on transparent or pure white 3:1 as specified; no symbol or surrounding layout.",
            negatives=negatives,
        )
        tasks.append(
            task_record(
                "wordmark-production-master",
                "3:1",
                prompt,
                [approved_wordmark],
                "wordmark-master",
            )
        )
        canonical_refs.append("@wordmark-production-master")

    if approved_symbol and approved_wordmark:
        for orientation, ratio, composition in (
            (
                "horizontal",
                "3:1",
                "symbol left, wordmark right, optically balanced clear space",
            ),
            (
                "vertical",
                "1:1",
                "symbol above, wordmark below, optically balanced clear space",
            ),
        ):
            prompt = prompt_contract(
                task=f"Compose one {orientation} {brand} lockup from the approved masters.",
                strategy="Combine approved assets without redrawing either one.",
                invariants=[
                    *invariants,
                    "preserve both masters byte-faithfully in visible geometry",
                ],
                reference_roles=[
                    "Reference 1 controls symbol geometry; reference 2 controls wordmark geometry."
                ],
                mechanism=f"Use only this composition: {composition}.",
                scene=f"One flat {orientation} lockup on a plain field at {ratio}; no alternative layout or mockup.",
                negatives=negatives,
            )
            tasks.append(
                task_record(
                    f"lockup-{orientation}",
                    ratio,
                    prompt,
                    canonical_refs,
                    "lockup-master",
                )
            )

    for family in spec.get("skinFamilies", []):
        family_id = slug(family["id"])
        canonical = (
            "@symbol-production-master"
            if approved_symbol
            else "@wordmark-production-master"
        )
        ratio = family.get("ratio", "1:1" if approved_symbol else "3:1")
        anchor_prompt = prompt_contract(
            task=f"Establish a non-deliverable {family['name']} rendering anchor for {brand}.",
            strategy=family["usage"],
            invariants=[*invariants, "preserve the canonical identity"],
            reference_roles=[
                "Reference 1 controls identity geometry; the anchor may control only composition and rendering language."
            ],
            mechanism=family["anchorMechanism"],
            scene=family["scene"],
            negatives=negatives,
        )
        anchor_id = f"skin-anchor-{family_id}"
        tasks.append(
            task_record(anchor_id, ratio, anchor_prompt, [canonical], "family-anchor")
        )
        for child in family.get("children", []):
            child_id = slug(child["id"])
            child_prompt = prompt_contract(
                task=f"Create one {brand} {family['name']} skin master: {child['name']}.",
                strategy=child.get("usage", family["usage"]),
                invariants=[
                    *invariants,
                    "preserve the canonical silhouette, counterforms, proportion, and orientation",
                ],
                reference_roles=[
                    "Reference 1 controls exact identity geometry.",
                    "Reference 2 controls only family composition, light, depth, and rendering language.",
                ],
                mechanism=child["mechanism"],
                scene=family["scene"],
                negatives=negatives,
            )
            tasks.append(
                task_record(
                    f"skin-{family_id}-{child_id}",
                    ratio,
                    child_prompt,
                    [canonical, f"@{anchor_id}"],
                    "symbol-skin-master"
                    if approved_symbol
                    else "wordmark-variant-master",
                )
            )

    available_refs = {
        "symbol": "@symbol-production-master" if approved_symbol else None,
        "wordmark": "@wordmark-production-master" if approved_wordmark else None,
        "horizontal-lockup": "@lockup-horizontal"
        if approved_symbol and approved_wordmark
        else None,
        "vertical-lockup": "@lockup-vertical"
        if approved_symbol and approved_wordmark
        else None,
    }
    for application in spec.get("productionApplications", []):
        application_id = slug(application["id"])
        requested_refs = application.get(
            "references", ["symbol" if approved_symbol else "wordmark"]
        )
        refs = []
        reference_roles = []
        for index, reference_name in enumerate(requested_refs, start=1):
            reference = available_refs.get(reference_name)
            if not reference:
                raise ValueError(
                    f"application {application_id} requests unavailable reference {reference_name!r}"
                )
            refs.append(reference)
            reference_roles.append(
                f"Reference {index} is the approved {reference_name} and controls exact visible identity geometry."
            )
        application_prompt = prompt_contract(
            task=f"Create one production application for {brand}: {application['name']}.",
            strategy=application["usage"],
            invariants=[
                *invariants,
                "preserve every referenced identity master without redrawing",
            ],
            reference_roles=reference_roles,
            mechanism=application["mechanism"],
            scene=application["scene"],
            negatives=negatives,
        )
        tasks.append(
            task_record(
                f"application-{application_id}",
                application["ratio"],
                application_prompt,
                refs,
                application.get("assetClass", "brand-application"),
            )
        )
    return tasks


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def dump_yaml(tasks: list[dict[str, Any]]) -> str:
    output = [
        "# Compiled by compile_brand_image_dag.py. Do not hand-edit sibling prompts.",
        "tasks:",
    ]
    for task in tasks:
        output.extend(
            [
                f"  - id: {yaml_quote(task['id'])}",
                f"    name: {yaml_quote(task['name'])}",
                f"    ratio: {yaml_quote(task['ratio'])}",
            ]
        )
        if task.get("refs"):
            output.append("    refs:")
            output.extend(f"      - {yaml_quote(ref)}" for ref in task["refs"])
        output.append(
            "    prompt: |-\n"
            + "\n".join(
                f"      {line}" if line else "" for line in task["prompt"].splitlines()
            )
        )
    return "\n".join(output) + "\n"


def compilation_report(
    stage: str,
    tasks: list[dict[str, Any]],
    dag_text: str | None = None,
) -> dict[str, Any]:
    report = {
        "schemaVersion": 1,
        "stage": stage,
        "promptVersion": PROMPT_VERSION,
        "draft": any("TBD" in task["prompt"] for task in tasks),
        "taskCount": len(tasks),
        "tasks": [
            {
                "id": task["id"],
                "assetClass": task.get("assetClass"),
                "ratio": task["ratio"],
                "refs": task.get("refs", []),
                "promptHash": prompt_hash(task["prompt"]),
            }
            for task in tasks
        ],
    }
    if dag_text is not None:
        report["dagSha256"] = hashlib.sha256(dag_text.encode("utf-8")).hexdigest()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--stage", choices=("exploration", "production"), required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--approved-symbol")
    parser.add_argument("--approved-wordmark")
    parser.add_argument("--allow-placeholders", action="store_true")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    validate_spec(spec, args.allow_placeholders)
    tasks = (
        compile_exploration(spec)
        if args.stage == "exploration"
        else compile_production(spec, args.approved_symbol, args.approved_wordmark)
    )
    if not tasks:
        raise SystemExit(f"{args.stage} compilation produced no tasks")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    dag_text = dump_yaml(tasks)
    args.output.write_text(dag_text, encoding="utf-8")
    report_path = args.report or args.output.with_suffix(".report.json")
    report_path.write_text(
        json.dumps(
            compilation_report(args.stage, tasks, dag_text),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
