#!/usr/bin/env python3

import argparse
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont


ASCENDERS = set("bdfhiklt")
DESCENDERS = set("gpqy")
ASCENDING_DESCENDERS = {"j"}


def parse_svg(svg_path: Path) -> str:
    root = ET.parse(svg_path).getroot()
    path = root.find("{http://www.w3.org/2000/svg}path")
    if path is None or "d" not in path.attrib:
        raise ValueError(f"No SVG path in {svg_path}")
    return path.attrib["d"]


def vertical_span(
    character: str, cap_height: int, x_height: int, descender: int
) -> tuple[int, int]:
    if character.isupper():
        return 0, cap_height
    if character in ASCENDING_DESCENDERS:
        return descender, cap_height
    if character in ASCENDERS:
        return 0, cap_height
    if character in DESCENDERS:
        return descender, x_height
    return 0, x_height


def build_glyph(
    character: str,
    svg_path: Path,
    cap_height: int,
    x_height: int,
    descender: int,
    side_bearing: int,
):
    path_data = parse_svg(svg_path)
    bounds_pen = BoundsPen(None)
    parse_path(path_data, bounds_pen)
    if bounds_pen.bounds is None:
        raise ValueError(f"Empty glyph path in {svg_path}")
    x_min, y_min, x_max, y_max = bounds_pen.bounds
    source_width = x_max - x_min
    source_height = y_max - y_min
    target_bottom, target_top = vertical_span(
        character, cap_height, x_height, descender
    )
    scale = (target_top - target_bottom) / source_height

    # SVG coordinates run downward; TrueType coordinates run upward.
    transform = (
        scale,
        0,
        0,
        -scale,
        side_bearing - x_min * scale,
        target_top + y_min * scale,
    )
    pen = TTGlyphPen(None)
    parse_path(path_data, TransformPen(pen, transform))
    advance_width = round(source_width * scale + side_bearing * 2)
    return pen.glyph(), (advance_width, side_bearing)


def empty_glyph():
    return TTGlyphPen(None).glyph()


def safe_name(value: str) -> str:
    result = re.sub(r"[^A-Za-z0-9]+", "", value)
    if not result:
        raise ValueError("family/style name must contain letters or digits")
    return result


def css_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def build(args: argparse.Namespace) -> None:
    characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    glyph_order = [".notdef", "space"] + characters
    glyphs = {".notdef": empty_glyph(), "space": empty_glyph()}
    metrics = {".notdef": (600, 0), "space": (args.space_width, 0)}
    cmap = {32: "space"}

    for character in characters:
        case_directory = "uppercase" if character.isupper() else "lowercase"
        svg_path = args.glyph_root / case_directory / f"{character}.svg"
        if not svg_path.exists():
            raise FileNotFoundError(svg_path)
        glyph, metric = build_glyph(
            character,
            svg_path,
            args.cap_height,
            args.x_height,
            args.descender,
            args.side_bearing,
        )
        glyphs[character] = glyph
        metrics[character] = metric
        cmap[ord(character)] = character

    postscript_name = f"{safe_name(args.family_name)}-{safe_name(args.style_name)}"
    file_stem = postscript_name
    full_name = f"{args.family_name} {args.style_name}"
    builder = FontBuilder(args.upm, isTTF=True)
    builder.setupGlyphOrder(glyph_order)
    builder.setupCharacterMap(cmap)
    builder.setupGlyf(glyphs)
    builder.setupHorizontalMetrics(metrics)
    builder.setupHorizontalHeader(
        ascent=args.ascent,
        descent=args.descent,
        lineGap=args.line_gap,
    )
    builder.setupNameTable(
        {
            "familyName": args.family_name,
            "styleName": args.style_name,
            "uniqueFontIdentifier": f"{postscript_name}-{args.version}",
            "fullName": full_name,
            "psName": postscript_name,
            "version": f"Version {args.version}",
            "manufacturer": args.manufacturer,
            "designer": args.designer,
            "description": "Experimental display alphabet derived from an approved wordmark and accepted glyph references.",
        }
    )
    builder.setupOS2(
        sTypoAscender=args.ascent,
        sTypoDescender=args.descent,
        sTypoLineGap=args.line_gap,
        usWinAscent=max(args.ascent, args.cap_height),
        usWinDescent=abs(min(args.descent, args.descender)),
        sxHeight=args.x_height,
        sCapHeight=args.cap_height,
        usWeightClass=args.weight_class,
        usWidthClass=args.width_class,
        fsSelection=0x40,
    )
    builder.setupPost(keepGlyphNames=True)
    builder.setupMaxp()

    args.output_root.mkdir(parents=True, exist_ok=True)
    ttf_path = args.output_root / f"{file_stem}.ttf"
    builder.save(ttf_path)

    woff2_path = args.output_root / f"{file_stem}.woff2"
    web_font = TTFont(ttf_path)
    web_font.flavor = "woff2"
    web_font.save(woff2_path)

    slug = css_slug(args.family_name)
    css_path = args.output_root / f"{slug}.css"
    css_path.write_text(
        f'''@font-face {{
  font-family: "{args.family_name}";
  src: url("./{woff2_path.name}") format("woff2"),
       url("./{ttf_path.name}") format("truetype");
  font-style: normal;
  font-weight: {args.weight_class};
  font-display: swap;
}}
''',
        encoding="utf-8",
    )

    specimen_path = args.output_root / "specimen.html"
    specimen_path.write_text(
        f'''<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>{full_name} specimen</title>
<link rel="stylesheet" href="./{css_path.name}">
<style>
body {{ margin: 0; background: #f7f7f5; color: #171719; font-family: system-ui, sans-serif; }}
main {{ max-width: 1200px; margin: 0 auto; padding: 72px; }}
h1 {{ margin: 0 0 56px; font: 112px/0.95 "{args.family_name}"; }}
p {{ margin: 0 0 32px; font: 64px/1.2 "{args.family_name}"; overflow-wrap: anywhere; }}
small {{ display: block; margin-top: 64px; color: #666; }}
</style>
<main>
<h1>{args.family_name}</h1>
<p>ABCDEFGHIJKLMNOPQRSTUVWXYZ</p>
<p>abcdefghijklmnopqrstuvwxyz</p>
<small>Alpha set: A-Z, a-z, and space. Kerning, hinting, punctuation, numerals, diacritics, and manual outline refinement require a separate production pass.</small>
</main>
</html>
''',
        encoding="utf-8",
    )

    svg_output = args.output_root / "glyphs-svg"
    if svg_output.exists():
        shutil.rmtree(svg_output)
    shutil.copytree(args.glyph_root, svg_output)

    png_output = args.output_root / "glyphs-png"
    if png_output.exists():
        shutil.rmtree(png_output)
    shutil.copytree(args.glyph_png_root, png_output)

    for path in [ttf_path, woff2_path, css_path, specimen_path]:
        print(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glyph-root", type=Path, required=True)
    parser.add_argument("--glyph-png-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--family-name", required=True)
    parser.add_argument("--style-name", default="Regular")
    parser.add_argument("--manufacturer", default="Independent")
    parser.add_argument("--designer", default="Wordmark extension workflow")
    parser.add_argument("--version", default="1.000")
    parser.add_argument("--upm", type=int, default=1000)
    parser.add_argument("--cap-height", type=int, default=700)
    parser.add_argument("--x-height", type=int, default=480)
    parser.add_argument("--descender", type=int, default=-220)
    parser.add_argument("--ascent", type=int, default=800)
    parser.add_argument("--descent", type=int, default=-250)
    parser.add_argument("--line-gap", type=int, default=100)
    parser.add_argument("--side-bearing", type=int, default=60)
    parser.add_argument("--space-width", type=int, default=300)
    parser.add_argument("--weight-class", type=int, default=400)
    parser.add_argument("--width-class", type=int, default=5)
    args = parser.parse_args()
    build(args)


if __name__ == "__main__":
    main()
