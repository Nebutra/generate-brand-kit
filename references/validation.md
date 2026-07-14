# Validation and Cleanup

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
- Compare at least three structurally different color families before approving
  a mark. Cosmetic variations do not count as separate families. Validate each
  with a separate monochrome reduction rather than forcing the primary concept
  to be black and white.
- Place candidates in a category thumbnail neighborhood at 24-32 px and test
  both similarity and disappearance into generic geometry.
- Verify that the selected formal operation extends coherently into wordmark,
  layout and motion. Reject one-off symbolic tricks.
- Require a complete responsive logo suite by default: standalone symbol,
  standalone wordmark, primary symbol+wordmark lockup, horizontal and vertical
  arrangements, monochrome/reverse variants, and a simplified small-size mark.
  Any omitted member needs an explicit not-applicable rationale.

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
