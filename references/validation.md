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

## Commit Hygiene

- Keep rejected assets out of commits.
- Commit approved masters and generated production outputs that the product consumes.
- Mention skipped checks and environment blockers explicitly.
- Push to the correct new-brand remote, not old upstreams.
