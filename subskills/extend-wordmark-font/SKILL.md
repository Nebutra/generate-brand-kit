---
name: extend-wordmark-font
description: Extend an approved custom wordmark or logo lettering into a coherent A-Z/a-z display alphabet and package it as PNG/SVG glyphs plus TTF/WOFF2. Use when Codex is asked to derive missing letters from a wordmark, build a brand font set, generate referenced glyphs through an image DAG, extract mother glyphs from logo typography, vectorize generated characters, or compile an installable alpha font. Do not use merely to choose an unrelated UI/body font.
---

# Extend Wordmark Font

Treat the approved wordmark as the only visual source of truth. Extract its actual glyphs, infer a bounded construction grammar, expand through reference-dependent stages, then normalize and compile. Never substitute a convenient existing font unless the user explicitly makes that font an approved source.

Read [references/workflow-contract.md](references/workflow-contract.md) before designing the DAG or prompt compiler.

## Required Gates

1. Confirm one approved wordmark image or vector master.
2. Separate direct evidence from inferred rules. Existing glyph shapes are evidence; missing glyph construction and all lowercase behavior are inference.
3. Confirm the requested character set and intended role. Default an A-Z/a-z request to an experimental display font, not body copy.
4. Keep generation candidates outside the consumer font directory until visual review passes.

If the wordmark is not approved, stop at extraction or exploration. Do not build a full alphabet from a moving target.

## Workflow

### 1. Extract Mother Glyphs

- Detect every visible wordmark glyph independently.
- Render the selected contour and its child counterforms onto a clean card. Do not crop a padded rectangle from the source; padding can import adjacent-letter fragments.
- Preserve repeated glyph instances until they are compared. Choose one canonical instance only after checking whether repetition is identical or optically adjusted.
- On macOS, run:

```bash
swift scripts/extract_wordmark_glyphs.swift \
  approved-wordmark.png work/references \
  --labels C,A-left,R,I,N,A-right
```

### 2. Write the Glyph Grammar

Record only visible properties: cap proportion, width classes, stem weight, contrast, terminal and serif construction, counter shape, curve tension, diagonal behavior, overshoot, spacing rhythm, and distinctive irregularities. State lowercase metrics as proposed rules rather than observed facts when the source is uppercase-only.

Do not let a vision model's confident measurements override the image. Use multimodal analysis as a second opinion, then verify every claimed feature visually.

### 3. Build a Dependency DAG

Do not generate 52 independent letters from one generic prompt.

1. Freeze approved source letters as mother glyphs; do not regenerate them.
2. Generate missing uppercase letters by structural family, each referencing the full wordmark and the most relevant isolated mother glyphs.
3. Generate a lowercase control set first. Default controls: `a n o e s g`; they cover bowl, shoulder, aperture, spine, single-storey construction, and descender/link behavior.
4. Review the controls as a family. If they fail, revise only the control stage.
5. Generate remaining lowercase letters from the approved wordmark plus accepted lowercase controls.

Declare every reference role in the prompt. The full wordmark controls global DNA; isolated source glyphs control local construction; accepted lowercase controls govern x-height and lowercase rhythm.

Copy `references/glyph-dag-config.example.json`, replace every path and dependency with evidence from the approved wordmark, then compile the stages instead of hand-writing sibling prompts:

```bash
python3 scripts/compile_glyph_dag.py --config glyph-dag-config.json \
  --stage uppercase --output dags/uppercase.yaml
python3 scripts/compile_glyph_dag.py --config glyph-dag-config.json \
  --stage lowercase-controls --output dags/lowercase-controls.yaml
# Add only reviewed control paths to acceptedControls before continuing.
python3 scripts/compile_glyph_dag.py --config glyph-dag-config.json \
  --stage lowercase-remaining --output dags/lowercase-remaining.yaml
```

### 4. Compile One Prompt Contract

Keep these clauses byte-stable across sibling tasks and vary only the target character, structural sources, and character-specific construction:

1. exact target character and case;
2. reference authority and prohibited contributions;
3. shared glyph DNA;
4. conventional target skeleton;
5. invisible composition metrics;
6. one black glyph on pure white;
7. negative constraints.

Require one glyph per image. Ban words, alphabet boards, secondary characters, captions, punctuation, logo symbols, materials, texture, shadow, mockups, gradients, ornament, and external-typeface imitation.

Dry-run the DAG and report task count, references, provider/model, ratio, and estimated cost before billed execution. Treat API success as `generated`, never `accepted`.

### 5. Review Before Expansion

Create uppercase and lowercase contact sheets. Check:

- exact character identity;
- one glyph only;
- source-DNA fidelity;
- family weight and contrast;
- terminal, serif, counter, and aperture consistency;
- cap/x-height, baseline, ascender, and descender behavior;
- width-class and side-bearing rhythm;
- no neighboring fragments or image effects.

Reject or rerun invalid nodes and their descendants only. Do not rebuild accepted independent branches.

### 6. Vectorize and Normalize

Use clean accepted glyph cards as inputs. On macOS:

```bash
swift scripts/vectorize_glyph.swift \
  --input accepted/A.png \
  --output glyphs-svg/uppercase/A.svg \
  --title "Brand glyph A"
```

Preserve child contours and verify counters after vectorization. Normalize font metrics during compilation; do not assume independently centered image cards share a baseline.

Keep uppercase and lowercase files in separate directories. Default macOS volumes are commonly case-insensitive, so `A.png` and `a.png` may overwrite each other in a flat folder.

### 7. Compile and Validate

Compile only accepted SVG glyphs:

```bash
uv run --with fonttools --with brotli python scripts/build_alpha_font.py \
  --glyph-root glyphs-svg \
  --glyph-png-root glyphs-png \
  --output-root fonts \
  --family-name "Brand Display Alpha"
```

Validate both packaging and visual behavior:

- open TTF and WOFF2 with FontTools;
- assert A-Z, a-z, and space mappings;
- shape representative strings with HarfBuzz;
- render uppercase, lowercase, and original-word specimens from the compiled TTF;
- XML-validate all SVG glyphs;
- compare the compiled source word against the approved wordmark;
- record limitations explicitly.

Render evidence from the compiled binary, then run the joint validator:

```bash
swift scripts/render_font_specimens.swift \
  fonts/BrandDisplayAlpha-Regular.ttf "Brand Display Alpha" "BRAND" fonts/specimens
uv run --with fonttools --with brotli python scripts/validate_alpha_font.py \
  --ttf fonts/BrandDisplayAlpha-Regular.ttf \
  --woff2 fonts/BrandDisplayAlpha-Regular.woff2 \
  --glyph-svg-root fonts/glyphs-svg \
  --glyph-png-root fonts/glyphs-png \
  --specimen-root fonts/specimens
```

An Alpha font may ship with normalized metrics and side bearings while still requiring manual Bézier refinement, kerning pairs, hinting, punctuation, numerals, diacritics, and OpenType features.

## Deliverable Layout

```text
fonts/
├── BrandDisplayAlpha-Regular.ttf
├── BrandDisplayAlpha-Regular.woff2
├── brand-display-alpha.css
├── specimen.html
├── specimens/
│   ├── uppercase.png
│   ├── lowercase.png
│   └── source-word.png
├── glyphs-png/
│   ├── uppercase/A.png ... Z.png
│   └── lowercase/a.png ... z.png
└── glyphs-svg/
    ├── uppercase/A.svg ... Z.svg
    └── lowercase/a.svg ... z.svg
```

Keep DAG files, raw generations, rejected candidates, and extraction experiments in a separate development tree.

Treat the Alpha as a brand display font. Do not map it to product body or general UI text until punctuation, numerals, diacritics, localization coverage, spacing, kerning, hinting, and fallback behavior pass a separate type-production review.

## Guardrails

- Do not introduce an external font merely to fill missing glyphs.
- Do not claim an uppercase-only wordmark proves lowercase anatomy.
- Do not use a padded raster crop as a mother-glyph reference.
- Do not generate a board containing several unsettled letters when per-glyph consistency matters.
- Do not continue to downstream lowercase expansion when control glyphs drift.
- Do not confuse a compiled font with a finished professional type family.
- Do not flatten uppercase and lowercase source files into one directory on a case-insensitive filesystem.
- Do not ship without rendered specimens from the compiled binary.
