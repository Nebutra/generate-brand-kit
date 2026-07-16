# Validation and Cleanup

## Contents

File, repository, visual, family, asset-class, selected-kit, AI SaaS, and commit
hygiene checks.

## File Checks

- Use `file` to confirm raster dimensions and alpha/RGB mode.
- Parse JSON/YAML configs after edits.
- Check SVGs for expected viewBox, paths, and forbidden old colors/names.
- Confirm build outputs changed when source icons changed.

## Repo Checks

Run targeted scans for:

- old brand names;
- old asset filenames;
- rejected generation directories;
- stale docs references;
- old remotes/upstreams when a full migration is requested;
- generated outputs ignored by git but still consumed locally.

Do not delete code-level compatibility uses of `legacy` or third-party import names without reading context. A Ghostty import feature, for example, is not visual legacy.

## Visual Checks

- Inspect app/dock icon in real context.
- Check small-size legibility.
- Check light and dark backgrounds.
- Confirm platform masking: if the OS supplies rounded corners, do not bake a large square field unless the platform requires it.
- Confirm no suggestive/anatomical readings after scaling.
- Run an unprompted five-second noun test with multiple viewers before sharing
  the rationale. Record the first reading; do not negotiate with a collision.
- Compare at least three structurally different black-and-white families before
  approving a mark. Cosmetic variations do not count as separate families.
- Place candidates in a category thumbnail neighborhood at 24-32 px and test
  both similarity and disappearance into generic geometry.
- Verify that the selected formal operation extends coherently into wordmark,
  layout and motion. Reject one-off symbolic tricks.

## Generated-Family Checks

- Treat provider success as `generated`, not `accepted`; inspect every formal
  master before promotion.
- Verify identity invariants across the family: silhouette, counterform,
  proportion, orientation, and minimum-size reading.
- Verify shared family invariants: camera, scale, safe area, background,
  lighting, material depth, or texture density as applicable.
- Verify sibling differentiation. Each accepted sibling needs one visually
  evident mechanism, not a cosmetic color, gloss, or noise change.
- Compare siblings together only after the underlying symbol or wordmark has
  been approved. Keep symbol, wordmark, lockup, application, and mockup reviews
  separate so one weak generator task cannot corrupt every asset class.
- Use automated similarity metrics only as review signals. Do not hard-code a
  universal CLIP/DINO threshold as an aesthetic approval rule.

## Asset-Class Structure Checks

- Define native ratio and dimensions per asset class before generation.
- Require homogeneous dimensions where a class promises interchangeable
  masters; verify actual PNG headers rather than filenames.
- Regenerate a master created for the wrong composition or ratio. Do not crop,
  stretch, or pad it merely to satisfy a file-size check.
- Cap retries and record a named blocker when the producer repeatedly misses a
  structural constraint.
- Validate the final manifest with:

```bash
python3 scripts/validate_brand_asset_manifest.py \
  /path/to/project/brand-asset-manifest.json \
  --root /path/to/project \
  --plan /path/to/project/brand-vi-production-plan.json \
  --production-complete
```

Do not use `--allow-empty` outside a pre-scope draft. Structural validity does
not mean production completion; completion requires item reconciliation,
terminal required work, accepted evidence, byte size, and SHA-256 checks.

Use `scripts/update_brand_asset_state.py` rather than editing accepted state by
hand. After a canonical checksum changes, confirm every declared descendant is
`invalidated`, its stale manifest output is cleared, and its old product file is
quarantined before selective regeneration.

## Selected-Kit Checks

- Confirm logo guidelines include clear space, minimum size, background behavior, co-branding where relevant, and misuse examples.
- Verify type hierarchy, fallback fonts, licensing status, multilingual samples, and accessible color pairs.
- Render editable marketing, stationery, and presentation templates before delivery; do not accept source-file existence as visual QA.
- For print and packaging, distinguish screen mockups from print-ready artwork. Record color mode, bleed, safe area, dieline source, supplier proof status, and unresolved regulatory copy.
- For environment work, record site dimensions and accessibility constraints; label concepts that lack surveys or engineering as non-construction artwork.
- For motion, test reduced-motion behavior, duration/easing consistency, codecs, alpha requirements, and static fallbacks.
- For sonic assets, record authorship/model, license, duration, loudness/format target, and approval status.
- Maintain a rights register for fonts, stock imagery, generated media, music, models, and third-party marks. Legal clearance remains an external approval.
- Confirm every selected A1-B13 catalog item appears as its own inventory row with source, owner, output level, status and acceptance check.
- Test QR assets using multiple devices, sizes and screen/print conditions; preserve the required quiet zone and fallback destination.
- Check flags for aspect ratio, attachment zones, reverse-side behavior, wind/readability conditions and fabrication notes.
- Check uniforms, vehicles, retail fixtures and industrial signage against authoritative templates or measurements; otherwise label them concept-only.
- For mascot/IP systems, verify turnaround consistency, silhouette recognition, monochrome behavior, pose/expression consistency, 3D handoff assumptions and static motion fallbacks.

## AI SaaS Checks

Use `ai-saas-acceptance.md` for group-specific evidence and end-to-end flow
tests; the checks below are the minimum cross-system battery.

- Confirm AI-generated, AI-assisted and AI-executed states have distinct labels and are not communicated by sparkle decoration alone.
- Exercise idle, understanding, planning, streaming, tool use, approval, cancel, retry, partial-success, refusal, timeout and recovery states.
- Verify sources, freshness, confidence and limitations remain attached when content is copied, exported, shared or regenerated.
- Check that progress and “thinking” visuals do not imply access to hidden reasoning, certainty or measurable completion when none exists.
- Verify users can inspect context boundaries, model/provider identity, data retention/training behavior, third-party data flow and administrator policy.
- Test prompt, conversation, citations, code, tables, attachments and live updates with keyboard and screen-reader workflows; include reduced-motion behavior.
- Verify API keys, logs, traces, usage, credits, billing, deprecation and incident states use consistent language and never expose secrets.
- Require evidence and owner fields for security, privacy, compliance, SLA, certification, Responsible AI and model-card claims.
- Verify provenance metadata/watermarks survive supported transformations; clearly label missing, invalid and conflicting provenance.
- Test first-party, third-party, verified, community and customer-created agents/plugins as distinct ecosystem states.

## Commit Hygiene

- Keep rejected assets out of commits.
- Commit approved masters and generated production outputs that the product consumes.
- Mention skipped checks and environment blockers explicitly.
- Push to the correct new-brand remote, not old upstreams.
