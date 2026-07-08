#!/usr/bin/env python3
"""Create a neutral brand-kit scaffold for a repository."""

from __future__ import annotations

import argparse
from pathlib import Path


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; pass --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def inventory_template(brand: str, philosophy: str) -> str:
    return f"""# {brand} Brand Kit Inventory

## Brand Philosophy

{philosophy or "TBD"}

## Source Structure

- `approved/`: stable masters that downstream assets may reference.
- `generated/`: current generation outputs that are not yet approved.
- `processed/`: exported production assets derived from approved masters.

## Product Asset Slots

| Slot | Target Path | Format | Required Size | Source | Status |
| --- | --- | --- | --- | --- | --- |
| Primary logo | TBD | SVG/PNG | TBD | `approved/` | planned |
| App icon | TBD | PNG/ICNS/ICO | platform-specific | `approved/` | planned |
| Favicon | TBD | PNG/ICO | TBD | `processed/` | planned |
| Mobile icon | TBD | PNG | platform-specific | `processed/` | planned |
| Hero/social background | TBD | PNG/JPG | TBD | `generated/` | planned |

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

## Visual System

- Shape grammar: TBD
- Materials: TBD
- Palette: TBD
- Typography: follow the product's existing type system unless a brand surface requires otherwise.
- Imagery: TBD

## Negative Constraints

- No old brand mark.
- No ambiguous anatomical/suggestive silhouette.
- No generated text in raster backgrounds unless post-composed intentionally.
- No rejected exploration assets in product paths.
"""


def dag_template(brand: str) -> str:
    return f"""# {brand} brand generation DAG

tasks:
  - id: foundation-material-board
    name: 01-foundation-material-board
    ratio: "16:9"
    prompt: >-
      Create a {brand} material and palette reference board, not a logo.
      Show the brand materials, colors, lighting, and cultural mood. No text,
      no logo, no watermark.

  - id: core-mark-seed
    name: 02-core-mark-seed
    ratio: "1:1"
    refs: ["@foundation-material-board"]
    prompt: >-
      Design the primary {brand} mark using the referenced material board.
      Create one clear silhouette and one clear product signal. Centered,
      vector-friendly, readable at small size, no old brand mark, no watermark.

  - id: production-icon
    name: 03-production-icon
    ratio: "1:1"
    refs: ["@core-mark-seed"]
    prompt: >-
      Convert the approved {brand} mark into a production app icon. Preserve
      the mark relationship, adapt only material/depth/platform output needs.

  - id: legibility-proof
    name: 04-legibility-proof
    ratio: "1:1"
    refs: ["@production-icon"]
    prompt: >-
      Create a small-size legibility proof sheet on light and dark backgrounds.
      No labels, no fake text, no watermark.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--brand", required=True, help="Brand/product name")
    parser.add_argument(
        "--output",
        default="resources/brand",
        help="Brand kit output directory relative to repo",
    )
    parser.add_argument("--philosophy", default="", help="One-line brand philosophy")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    args = parser.parse_args()

    root = Path(args.repo).expanduser().resolve()
    out = root / args.output
    (out / "approved").mkdir(parents=True, exist_ok=True)
    (out / "generated").mkdir(parents=True, exist_ok=True)
    (out / "processed").mkdir(parents=True, exist_ok=True)
    for directory in ("approved", "generated", "processed"):
        keep = out / directory / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    write(out / "brand-kit-inventory.md", inventory_template(args.brand, args.philosophy), args.force)
    write(out / "visual-identity.md", vi_template(args.brand, args.philosophy), args.force)
    write(out / "brand-generation-dag.yaml", dag_template(args.brand), args.force)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
