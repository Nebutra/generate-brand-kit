#!/usr/bin/env python3
"""Compile per-glyph image tasks from an approved wordmark dependency map."""

from __future__ import annotations

import argparse
import hashlib
import json
import string
from pathlib import Path
from typing import Any


CONTROLS = "anoesg"
NEGATIVES = (
    "No word, second glyph, alphabet board, caption, punctuation, logo symbol, "
    "material, texture, shadow, mockup, gradient, ornament, calligraphy, italic "
    "drift, or external-typeface imitation."
)


def prompt_for(
    character: str,
    shared_dna: list[str],
    reference_roles: list[str],
    construction: str,
) -> str:
    case = "uppercase" if character.isupper() else "lowercase"
    return f"""TASK
Create exactly one {case} Latin glyph: {character}.

REFERENCE AUTHORITY
{" ".join(reference_roles)}

SHARED GLYPH DNA
{"; ".join(shared_dna)}

TARGET CONSTRUCTION
Use the conventional readable skeleton of {character}. {construction}

OUTPUT CONTRACT
One black glyph on pure white. Fixed invisible cap/x-height, baseline and descender metrics. Optical centering, ample side bearings, hard flat edges.

NEGATIVE CONSTRAINTS
{NEGATIVES} Render exactly {character}."""


def task(character: str, refs: list[str], prompt: str) -> dict[str, Any]:
    case = "uppercase" if character.isupper() else "lowercase"
    return {
        "id": f"glyph-{case}-{character}",
        "name": f"glyph-{case}-{character}",
        "ratio": "1:1",
        "refs": refs,
        "prompt": prompt,
    }


def dump_yaml(tasks: list[dict[str, Any]]) -> str:
    output = [
        "# Compiled glyph DAG. Keep uppercase and lowercase outputs in separate directories.",
        "tasks:",
    ]
    for item in tasks:
        output.extend(
            [
                f"  - id: {json.dumps(item['id'])}",
                f"    name: {json.dumps(item['name'])}",
                f"    ratio: {json.dumps(item['ratio'])}",
                "    refs:",
                *(
                    f"      - {json.dumps(ref, ensure_ascii=False)}"
                    for ref in item["refs"]
                ),
                "    prompt: |-",
                *(
                    f"      {line}" if line else ""
                    for line in item["prompt"].splitlines()
                ),
            ]
        )
    return "\n".join(output) + "\n"


def compile_tasks(config: dict[str, Any], stage: str) -> list[dict[str, Any]]:
    wordmark = config.get("wordmark")
    mother = config.get("motherGlyphs", {})
    dependencies = config.get("dependencies", {})
    controls = config.get("acceptedControls", {})
    shared_dna = config.get("sharedGlyphDna", [])
    constructions = config.get("constructions", {})
    if not isinstance(wordmark, str) or not wordmark:
        raise ValueError("config.wordmark is required")
    if not isinstance(mother, dict) or not mother:
        raise ValueError("config.motherGlyphs is required")
    if not isinstance(shared_dna, list) or not shared_dna:
        raise ValueError("config.sharedGlyphDna is required")

    if stage == "uppercase":
        characters = [
            character for character in string.ascii_uppercase if character not in mother
        ]
    elif stage == "lowercase-controls":
        characters = list(CONTROLS)
    else:
        missing_controls = sorted(set(CONTROLS) - set(controls))
        if missing_controls:
            raise ValueError(f"acceptedControls missing: {', '.join(missing_controls)}")
        characters = [
            character
            for character in string.ascii_lowercase
            if character not in CONTROLS
        ]

    tasks = []
    for character in characters:
        source_letters = dependencies.get(character, [])
        refs = [wordmark]
        roles = ["Reference 1 is the approved full wordmark and controls global DNA."]
        for source in source_letters:
            source_path = mother.get(source) or controls.get(source)
            if not source_path:
                raise ValueError(
                    f"glyph {character} depends on missing source {source}"
                )
            refs.append(source_path)
            roles.append(
                f"Reference {len(refs)} is accepted glyph {source} and controls only relevant local construction."
            )
        if character.islower() and stage == "lowercase-remaining":
            for control in CONTROLS:
                if controls[control] not in refs:
                    refs.append(controls[control])
                    roles.append(
                        f"Reference {len(refs)} is accepted lowercase control {control} and governs lowercase rhythm."
                    )
        prompt = prompt_for(
            character,
            shared_dna,
            roles,
            constructions.get(
                character,
                "Resolve unseen anatomy from the declared source evidence; do not import another typeface.",
            ),
        )
        tasks.append(task(character, refs, prompt))
    return tasks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--stage",
        choices=("uppercase", "lowercase-controls", "lowercase-remaining"),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    tasks = compile_tasks(config, args.stage)
    dag = dump_yaml(tasks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dag, encoding="utf-8")
    report = {
        "schemaVersion": 1,
        "stage": args.stage,
        "taskCount": len(tasks),
        "dagSha256": hashlib.sha256(dag.encode("utf-8")).hexdigest(),
        "tasks": [
            {
                "id": item["id"],
                "refs": item["refs"],
                "promptHash": hashlib.sha256(
                    item["prompt"].encode("utf-8")
                ).hexdigest(),
            }
            for item in tasks
        ],
    }
    report_path = args.report or args.output.with_suffix(".report.json")
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
