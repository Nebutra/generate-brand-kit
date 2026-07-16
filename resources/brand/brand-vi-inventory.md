# generate-brand-vi Brand VI Inventory

## Brand Philosophy

Parts in, brand out: a brand kit is a kit — standardized parts that
assemble into one identity consistent across every surface. See
`visual-identity.md` for the full VI. (v2, 2026-07: replaced the retired
water/crystal identity, whose IP came from a process metaphor rather than
the business scenario.)

## Source Structure

- `approved/`: stable masters that downstream assets may reference.
- `generated/`: current generation outputs that are not yet approved.
- `processed/`: exported production assets derived from approved masters.

## Product Asset Slots

This repo is a skill, so its only product surfaces are the README and the
GitHub repo page. No app icons, favicons, or mobile slots apply.

| Slot | Target Path | Format | Required Size | Source | Status |
| --- | --- | --- | --- | --- | --- |
| Primary logo mark | `resources/brand/processed/logo.svg` | SVG | scalable, legible at 32 px | verified vector derivative of `approved/core-mark.png` | done |
| README hero banner | `resources/brand/processed/hero.png` | PNG | 1774×887 (2:1) | approved mark → production DAG | done |
| Social preview / OG card | `resources/brand/processed/social-preview.png` | PNG | 1280×640 (2:1) | approved mark + hero language | done |
| Raster mark master | `resources/brand/approved/core-mark.png` | PNG | 1254×1254 | human-approved canonical | done |

## Consumption Map

- `README.md` header → `processed/logo.svg`
- `README.md` hero → `processed/hero.png`
- GitHub repo Settings → Social preview → upload `processed/social-preview.png` (manual, GitHub has no file-based slot)
- `brand-asset-manifest.json` → dependency, checksum, dimensions, validation and usage source of truth

## Migration Notes

- Rejected generation candidates are deleted after approval; `generated/`
  holds only the current in-flight batch (empty at rest).
- If the mark changes, re-derive `logo.svg`, `hero.png`, and
  `social-preview.png` from the new approved master and update this table.
