#!/usr/bin/env python3
"""Run a brand image DAG through an installed generate-image skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def candidate_backends() -> list[Path]:
    here = Path(__file__).resolve().parent.parent
    candidates = []
    if configured := os.environ.get("GENERATE_IMAGE_SKILL"):
        candidates.append(Path(configured).expanduser())
    candidates.extend(
        [
            here.parent / "generate-image",
            Path.home() / ".codex/skills/generate-image",
            Path.home() / ".agents/skills/generate-image",
            Path.home() / ".claude/skills/generate-image",
        ]
    )
    return candidates


def resolve_backend() -> Path:
    for candidate in candidate_backends():
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "src/generate_image"
        ).is_dir():
            return candidate.resolve()
    searched = "\n  - ".join(str(path) for path in candidate_backends())
    raise SystemExit(
        "generate-image backend not found. Set GENERATE_IMAGE_SKILL or install it at one of:\n"
        f"  - {searched}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo", default=".", help="Repository containing the brand kit"
    )
    parser.add_argument(
        "--dag-file",
        default="resources/brand/brand-vi-exploration-dag.yaml",
        help="DAG path relative to --repo, or an absolute path",
    )
    parser.add_argument(
        "--output-dir",
        default="resources/brand/generated",
        help="Output directory relative to --repo, or an absolute path",
    )
    parser.add_argument(
        "--report-file",
        help="Compilation report path; defaults beside the DAG",
    )
    parser.add_argument("--provider", default="mox", help="generate-image provider")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--on-failure", choices=("skip", "fail-fast"), default="skip")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Make real billed API calls; without this flag only a dry-run is performed",
    )
    parser.add_argument(
        "--json", action="store_true", help="Request machine-readable output"
    )
    args = parser.parse_args()

    if shutil.which("uv") is None:
        raise SystemExit("uv is required to run the generate-image backend")

    repo = Path(args.repo).expanduser().resolve()
    dag = Path(args.dag_file).expanduser()
    dag = dag if dag.is_absolute() else repo / dag
    output = Path(args.output_dir).expanduser()
    output = output if output.is_absolute() else repo / output
    if not dag.is_file():
        raise SystemExit(f"DAG file not found: {dag}")
    report = (
        Path(args.report_file).expanduser()
        if args.report_file
        else dag.with_suffix(".report.json")
    )
    report = report if report.is_absolute() else repo / report
    if args.execute:
        if not report.is_file():
            raise SystemExit(f"compiled DAG report required for execution: {report}")
        report_data = json.loads(report.read_text(encoding="utf-8"))
        actual_hash = hashlib.sha256(dag.read_bytes()).hexdigest()
        if report_data.get("dagSha256") != actual_hash:
            raise SystemExit(
                "DAG differs from its compilation report; recompile before execution"
            )
        if report_data.get("draft") is True:
            raise SystemExit(
                "compiled DAG still contains draft placeholders; resolve the spec and recompile"
            )
    output.mkdir(parents=True, exist_ok=True)

    backend = resolve_backend()
    command = [
        "uv",
        "run",
        "--project",
        str(backend),
        "--no-sync",
        "generate-image",
        "--dag-file",
        str(dag),
        "--output-dir",
        str(output),
        "--provider",
        args.provider,
        "--concurrency",
        str(args.concurrency),
        "--on-failure",
        args.on_failure,
    ]
    if not args.execute:
        command.append("--dry-run")
    if args.json:
        command.append("--json")

    print(f"generate-image backend: {backend}", file=sys.stderr)
    print(f"mode: {'execute' if args.execute else 'dry-run'}", file=sys.stderr)
    return subprocess.run(command, cwd=backend, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
