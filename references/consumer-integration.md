# Consumer Integration Contract

Use this contract when moving approved Brand VI work into a product repository.
Treat the design workspace as provenance, not as a directory to copy wholesale.

## Package Boundary

Keep four classes explicit:

```text
brand/
├── canonical/      # approved symbol, wordmark, lockups, palette and tokens
├── derivatives/    # platform icons, compact PNGs, host-color SVGs, font exports
├── evidence/       # contact sheets, rendered proofs, acceptance records
├── brand-asset-manifest.json
├── LICENSES.md
└── AGENTS.md
```

- Copy only approved, consumed assets into the product repository.
- Keep raw generations, rejected candidates, prompt experiments, temporary
  traces, and high-resolution review boards in the external design workspace.
- Record the source workspace, approved source file, derivative method, SHA-256,
  byte size, dimensions, owner, license, and consumer paths in the manifest.
- Do not optimize or rename a canonical master in place. Emit a derivative with
  its own manifest entry and dependency.

## Consumer Rules

- Make one canonical asset path authoritative. Generate aliases from it or
  verify them byte-for-byte; never maintain independent lookalikes.
- For host-controlled monochrome icons such as editor activity bars, derive a
  simplified SVG using `currentColor`; do not recolor the canonical mark.
- Generate lightweight PNG derivatives at the smallest dimensions that meet the
  target surface. Preserve aspect ratio and approved composition; do not center
  crop an incompatible master into a slot.
- Keep brand display fonts separate from product body and UI roles. An Alpha
  A-Z/a-z font without punctuation, numerals, diacritics, kerning, hinting, and
  localization coverage may be used only on approved brand-display surfaces.
- Preserve third-party font/image licenses beside consumed files and identify
  whether redistribution, web embedding, modification, and generated
  derivatives are allowed.

## Agent Instructions

Place an `AGENTS.md` in the brand package or nearest owned directory. State:

- which files are canonical and which are generated;
- which scripts regenerate derivatives;
- allowed symbol, wordmark, lockup, color, and font roles;
- prohibited recoloring, cropping, stretching, redrawing, or unrelated font use;
- required tests after an asset changes;
- legacy names and paths that must not return.

Do not duplicate full VI theory in `AGENTS.md`; link the canonical guidelines and
keep the file operational.

## Repo-Side Check

Provide one stable command such as `make brand-check` or `pnpm brand:check`.
Make it fail on:

- manifest checksum, byte-size, path, or dependency mismatch;
- missing canonical or generated assets;
- stale generated derivatives;
- invalid SVG/XML, missing viewBox, or forbidden hard-coded host color;
- invalid font headers or missing required character mappings;
- stale old-brand names, paths, docs, or product config references;
- source assets that changed without regenerated platform outputs.

Run product build/type tests and visual checks in addition to `brand-check`.
Asset validation cannot prove that a dock icon, first-run screen, email, or
localized layout works in context.
