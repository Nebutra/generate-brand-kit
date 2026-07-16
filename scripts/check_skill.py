#!/usr/bin/env python3
"""Run deterministic repository checks for generate-brand-vi."""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(*args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, "-B", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != expect:
        raise AssertionError(
            f"command returned {result.returncode}, expected {expect}: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def item_ids(catalog: dict) -> set[str]:
    return {
        f"{module}-{index:02d}"
        for module, definition in catalog["modules"].items()
        for index, _ in enumerate(definition["items"], start=1)
    }


def check_frontmatter(path: Path, expected_name: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    frontmatter = text.split("---\n", 2)[1]
    assert f"name: {expected_name}\n" in frontmatter
    assert "description:" in frontmatter


def main() -> int:
    check_frontmatter(ROOT / "SKILL.md", "generate-brand-vi")
    check_frontmatter(
        ROOT / "subskills/extend-wordmark-font/SKILL.md", "extend-wordmark-font"
    )

    catalog = json.loads(
        (ROOT / "references/vi-deliverables.json").read_text(encoding="utf-8")
    )
    routing = json.loads(
        (ROOT / "references/production-routing.json").read_text(encoding="utf-8")
    )
    known_items = item_ids(catalog)
    assert set(catalog["modules"]) == set(routing["routes"])
    assert set(routing["item_overrides"]) <= known_items
    for profile in catalog["profiles"].values():
        assert set(profile) <= set(catalog["modules"])

    run("scripts/validate_brand_asset_manifest.py", "--self-test")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        run(
            "scripts/create_brand_vi_scaffold.py",
            "--repo",
            str(root),
            "--brand",
            "SmokeBrand",
            "--profile",
            "ai-saas",
            "--require-item",
            "a1-01",
            "--require-item",
            "b2-05",
            "--require-item",
            "c1-04",
            "--external-handoff-item",
            "c14-05",
        )
        brand = root / "resources/brand"
        plan = json.loads(
            (brand / "brand-vi-production-plan.json").read_text(encoding="utf-8")
        )
        by_id = {item["id"]: item for item in plan["items"]}
        assert by_id["a1-01"]["creates_gate"] == "mark-approved"
        assert by_id["a1-02"]["creates_gate"] is None
        assert by_id["a1-02"]["requirement"] == "optional"
        assert by_id["b2-05"]["producer"] == "platform-icon"
        assert by_id["c1-04"]["producer"] == "design-token"
        assert by_id["c14-05"]["requirement"] == "external-handoff"

        scope_path = brand / "brand-vi-scope.json"
        scope = json.loads(scope_path.read_text(encoding="utf-8"))
        scope["items"]["b2-05"] = "optional"
        scope_path.write_text(json.dumps(scope), encoding="utf-8")
        run(
            "scripts/compile_brand_vi_scope.py",
            "--repo",
            str(root),
            "--force",
        )
        plan = json.loads(
            (brand / "brand-vi-production-plan.json").read_text(encoding="utf-8")
        )
        by_id = {item["id"]: item for item in plan["items"]}
        assert by_id["b2-05"]["requirement"] == "optional"

        manifest = brand / "brand-asset-manifest.json"
        run(
            "scripts/validate_brand_asset_manifest.py",
            str(manifest),
            "--root",
            str(brand),
            "--plan",
            str(brand / "brand-vi-production-plan.json"),
        )
        incomplete = run(
            "scripts/validate_brand_asset_manifest.py",
            str(manifest),
            "--root",
            str(brand),
            "--plan",
            str(brand / "brand-vi-production-plan.json"),
            "--production-complete",
            expect=1,
        )
        assert "not terminal" in incomplete.stdout

        empty = root / "empty.json"
        empty.write_text(
            json.dumps({"schemaVersion": 1, "brand": "Empty", "assets": []}),
            encoding="utf-8",
        )
        empty_result = run(
            "scripts/validate_brand_asset_manifest.py",
            str(empty),
            expect=1,
        )
        assert "at least one" in empty_result.stdout

        report = json.loads(
            (brand / "brand-vi-exploration-dag.report.json").read_text(encoding="utf-8")
        )
        assert report["taskCount"] == 6
        assert report["draft"] is True
        assert len({item["promptHash"] for item in report["tasks"]}) == 6
        assert [item["assetClass"] for item in report["tasks"]].count(
            "symbol-exploration"
        ) == 3
        assert [item["assetClass"] for item in report["tasks"]].count(
            "wordmark-exploration"
        ) == 3
        draft_execution = run(
            "scripts/run_brand_image_dag.py",
            "--repo",
            str(root),
            "--execute",
            expect=1,
        )
        assert "draft placeholders" in draft_execution.stderr

        state_root = root / "state"
        state_root.mkdir()
        old_parent = state_root / "parent-old.txt"
        new_parent = state_root / "parent-new.txt"
        child_output = state_root / "child.txt"
        old_parent.write_text("old", encoding="utf-8")
        new_parent.write_text("new", encoding="utf-8")
        child_output.write_text("child", encoding="utf-8")
        state_manifest = state_root / "brand-asset-manifest.json"
        state_manifest.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "brand": "State",
                    "assets": [
                        {
                            "id": "parent",
                            "name": "Parent",
                            "role": "deliverable",
                            "assetClass": "master",
                            "status": "complete",
                            "dependencies": [],
                            "output": {
                                "path": old_parent.name,
                                "bytes": old_parent.stat().st_size,
                                "sha256": hashlib.sha256(
                                    old_parent.read_bytes()
                                ).hexdigest(),
                            },
                            "validation": {"reviewed": True, "checks": ["human"]},
                        },
                        {
                            "id": "child",
                            "name": "Child",
                            "role": "derivative",
                            "assetClass": "application",
                            "status": "complete",
                            "dependencies": ["parent"],
                            "output": {
                                "path": child_output.name,
                                "bytes": child_output.stat().st_size,
                                "sha256": hashlib.sha256(
                                    child_output.read_bytes()
                                ).hexdigest(),
                            },
                            "validation": {"reviewed": True, "checks": ["human"]},
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        update = run(
            "scripts/update_brand_asset_state.py",
            str(state_manifest),
            "--asset",
            "parent",
            "--status",
            "complete",
            "--output",
            str(new_parent),
            "--root",
            str(state_root),
            "--reviewed",
        )
        assert "invalidated descendants: child" in update.stdout
        state = json.loads(state_manifest.read_text(encoding="utf-8"))
        state_by_id = {item["id"]: item for item in state["assets"]}
        assert state_by_id["child"]["status"] == "invalidated"
        assert "output" not in state_by_id["child"]

        glyph_config = {
            "brand": "Smoke",
            "wordmark": "approved/wordmark.png",
            "sharedGlyphDna": ["one observable terminal rule"],
            "motherGlyphs": {"A": "mother/A.png"},
            "dependencies": {},
            "acceptedControls": {},
        }
        config_path = root / "glyph-config.json"
        config_path.write_text(json.dumps(glyph_config), encoding="utf-8")
        run(
            "subskills/extend-wordmark-font/scripts/compile_glyph_dag.py",
            "--config",
            str(config_path),
            "--stage",
            "uppercase",
            "--output",
            str(root / "uppercase.yaml"),
        )
        upper_report = json.loads(
            (root / "uppercase.report.json").read_text(encoding="utf-8")
        )
        assert upper_report["taskCount"] == 25
        lower_failure = run(
            "subskills/extend-wordmark-font/scripts/compile_glyph_dag.py",
            "--config",
            str(config_path),
            "--stage",
            "lowercase-remaining",
            "--output",
            str(root / "lowercase.yaml"),
            expect=1,
        )
        assert "acceptedControls missing" in lower_failure.stderr

    print(
        "skill checks passed: scope, routing, gates, manifest, DAG, and glyph compiler"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
