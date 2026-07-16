#!/usr/bin/env python3
"""Validate Alpha font binaries, glyph sources, and rendered specimens."""

from __future__ import annotations

import argparse
import string
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.ttLib import TTFont


CHARACTERS = string.ascii_uppercase + string.ascii_lowercase


def validate_font(path: Path) -> list[str]:
    errors = []
    try:
        font = TTFont(path)
        cmap = font.getBestCmap() or {}
    except Exception as error:
        return [f"{path}: cannot open font: {error}"]
    missing = [
        character for character in f" {CHARACTERS}" if ord(character) not in cmap
    ]
    if missing:
        errors.append(f"{path}: missing cmap characters {''.join(missing)!r}")
    return errors


def validate_sources(root: Path, extension: str, parse_svg: bool = False) -> list[str]:
    errors = []
    for character in CHARACTERS:
        case = "uppercase" if character.isupper() else "lowercase"
        path = root / case / f"{character}.{extension}"
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing {path}")
            continue
        if parse_svg:
            try:
                svg = ET.parse(path).getroot()
                if not svg.tag.endswith("svg") or not svg.get("viewBox"):
                    errors.append(f"{path}: invalid SVG root or viewBox")
            except ET.ParseError as error:
                errors.append(f"{path}: invalid XML: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ttf", type=Path, required=True)
    parser.add_argument("--woff2", type=Path, required=True)
    parser.add_argument("--glyph-svg-root", type=Path, required=True)
    parser.add_argument("--glyph-png-root", type=Path, required=True)
    parser.add_argument("--specimen-root", type=Path, required=True)
    args = parser.parse_args()

    errors = []
    errors.extend(validate_font(args.ttf))
    errors.extend(validate_font(args.woff2))
    errors.extend(validate_sources(args.glyph_svg_root, "svg", parse_svg=True))
    errors.extend(validate_sources(args.glyph_png_root, "png"))
    for name in ("uppercase.png", "lowercase.png", "source-word.png"):
        path = args.specimen_root / name
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing rendered specimen {path}")
    if errors:
        print(f"alpha font invalid: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "alpha font valid: 52 glyph PNGs, 52 SVGs, TTF/WOFF2 cmap, and 3 rendered specimens"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
