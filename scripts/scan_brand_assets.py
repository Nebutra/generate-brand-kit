#!/usr/bin/env python3
"""Inventory likely brand assets and brand-term references in a repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "out",
    ".next",
    ".turbo",
    ".cache",
    ".build",
    "target",
    "DerivedData",
    "__pycache__",
    ".venv",
    "venv",
    "coverage",
}

ASSET_SUFFIXES = {
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".ico",
    ".icns",
    ".pdf",
}

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".json",
    ".md",
    ".mjs",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".toml",
    ".yaml",
    ".yml",
    ".xml",
    ".plist",
    ".rs",
    ".swift",
    ".kt",
    ".java",
    ".py",
}

BRAND_HINT_RE = re.compile(
    r"(brand|logo|icon|favicon|splash|hero|social|og-|opengraph|appicon|app-icon)",
    re.IGNORECASE,
)


def png_dimensions(path: Path) -> dict[str, int] | None:
    try:
      with path.open("rb") as handle:
          header = handle.read(24)
    except OSError:
        return None
    if len(header) >= 24 and header.startswith(b"\x89PNG\r\n\x1a\n"):
        width, height = struct.unpack(">II", header[16:24])
        return {"width": width, "height": height}
    return None


def svg_viewbox(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:4000]
    except OSError:
        return None
    match = re.search(r'viewBox=["\']([^"\']+)["\']', text)
    return match.group(1) if match else None


def iter_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        current_path = Path(current)
        for name in files:
            if name in {".DS_Store", ".gitkeep"}:
                continue
            yield current_path / name


def collect_assets(root: Path) -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    for path in iter_files(root):
        suffix = path.suffix.lower()
        relative = path.relative_to(root).as_posix()
        if suffix not in ASSET_SUFFIXES and not BRAND_HINT_RE.search(relative):
            continue
        item: dict[str, Any] = {
            "path": relative,
            "suffix": suffix,
            "bytes": path.stat().st_size,
            "brand_hint": bool(BRAND_HINT_RE.search(relative)),
        }
        if suffix == ".png":
            item["png"] = png_dimensions(path)
        if suffix == ".svg":
            item["svg_viewbox"] = svg_viewbox(path)
        assets.append(item)
    return sorted(assets, key=lambda item: (not item["brand_hint"], item["path"]))


def collect_text_hits(root: Path, terms: list[str]) -> list[dict[str, Any]]:
    if not terms:
        return []
    patterns = [(term, re.compile(re.escape(term), re.IGNORECASE)) for term in terms if term]
    hits: list[dict[str, Any]] = []
    for path in iter_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        found = {term: len(pattern.findall(text)) for term, pattern in patterns}
        found = {term: count for term, count in found.items() if count}
        if found:
            hits.append({"path": path.relative_to(root).as_posix(), "matches": found})
    return sorted(hits, key=lambda item: item["path"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Repository root to scan")
    parser.add_argument(
        "--brand-term",
        action="append",
        default=[],
        help="Brand or legacy term to search for; can be repeated",
    )
    parser.add_argument("--max-assets", type=int, default=300, help="Maximum asset rows to print")
    parser.add_argument("--max-text-hits", type=int, default=300, help="Maximum text hit rows to print")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    root = Path(args.repo).expanduser().resolve()
    assets = collect_assets(root)
    text_hits = collect_text_hits(root, args.brand_term)
    result = {
        "repo": str(root),
        "asset_count": len(assets),
        "text_hit_count": len(text_hits),
        "asset_files": assets[: args.max_assets],
        "text_hits": text_hits[: args.max_text_hits],
        "truncated": {
            "asset_files": len(assets) > args.max_assets,
            "text_hits": len(text_hits) > args.max_text_hits,
        },
    }
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
