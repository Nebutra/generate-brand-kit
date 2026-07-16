# Generation DAG Patterns

## Contents

Backend and compiler; recommended DAG; dependency consistency; canonical plus
family anchor; acceptance and selective reruns; negative constraints; cleanup.

## Built-in Backend

Compile and run brand DAGs through the bundled tools:

```bash
python3 scripts/compile_brand_image_dag.py \
  --spec /path/to/project/resources/brand/brand-image-spec.json \
  --stage exploration \
  --output /path/to/project/resources/brand/brand-vi-exploration-dag.yaml
python3 scripts/run_brand_image_dag.py --repo /path/to/project
python3 scripts/run_brand_image_dag.py --repo /path/to/project --execute
```

The first command is a free dry-run. The second makes billed calls after approval.
The adapter discovers a sibling or globally installed `generate-image`, defaults to
`mox`, and lets that backend resolve the global `MOX_API_KEY`. Override discovery
with `GENERATE_IMAGE_SKILL=/path/to/generate-image`; never pass the key on the
command line.

## Recommended DAG

1. **Strategy and operation specification**
   - Record evidence, 2-4 business relationships, formal operations, invariants,
     and negative constraints in `brand-image-spec.json`; this is structured
     input, not an image-generation task.

2. **Parallel isolated symbol directions**
   - Compile at least three structurally different black-and-white nodes.
   - Each image contains exactly one symbol. No wordmark, board, material, scene,
     color, application, or mockup.

3. **Parallel isolated wordmark directions**
   - Compile at least three typographically different black-and-white nodes when
     a custom wordmark is in scope.
   - Each image contains exactly one exact-spelling wordmark and no symbol.

4. **Collision and neighborhood proof**
   - Test unprompted readings, category similarity and 16-48 px behavior.
   - Reject familiar-object sinks before downstream generation.

5. **Human selection gate**
   - Approve one family or return to the operation branches.
   - No Hero, social, app icon or materialized mark may start before this gate.

6. **Post-approval production compilation**
   - Recompile from approved symbol and/or wordmark files. Clean each master
     separately, then create lockups without redrawing either source.

7. **Optional family anchors and dependent branches**
   - Use a material/reference anchor only after geometry approval and only when
     several children need the same composition or rendering language.
   - Skins, app icons, backgrounds, social cards, motion, print, and mockups
     depend on approved masters, never an exploration candidate.

8. **Proof sheets**
   - Small-size legibility, light/dark backgrounds, icon family contact sheet.

9. **Backgrounds and scenes**
   - Hero, social, onboarding, documentation.
   - Use the same approved mark/material references; do not let backgrounds invent new logos.

## Dependency Consistency Rules

- Put reference-locking assets before dependent tasks.
- Use image edit/reference inputs for shape consistency when available.
- If using prompt-only generation, explicitly constrain silhouette, composition, forbidden forms, material, lighting, and output intent.
- Promote approved masters to `approved/`; never make downstream tasks depend on exploratory folders.
- Do not use a purely serial mark pipeline before approval; one weak semantic
  decision will contaminate every descendant while appearing visually consistent.

## Canonical + Family Anchor Pattern

Use two references when a group must preserve both identity and a shared visual
language:

- **Canonical identity:** controls approved silhouette, counterform, proportion,
  posture, and other non-negotiable geometry.
- **Family anchor:** controls only the group's composition, material, lighting,
  texture density, or rendering language. It is a dependency artifact, not a
  deliverable.

State these roles in every child prompt. Do not assume reference order explains
intent to the image model. A typical child uses the canonical file plus an
upstream anchor output:

```yaml
tasks:
  - id: material-anchor
    name: 00-material-anchor
    refs: [approved/symbol-master.png]
    prompt: Establish neutral material, light, thickness, and camera. Preserve the symbol.
  - id: embroidered-skin
    name: 01-embroidered-skin
    refs: [approved/symbol-master.png, "@material-anchor"]
    prompt: >-
      Reference 1 controls exact identity geometry. Reference 2 controls only
      camera, light, scale, and thickness. Change one mechanism: embroidery.
```

Use one reference when only identity must remain fixed. Do not manufacture an
anchor merely to satisfy a numeric parent-count rule.

## Node Acceptance and Selective Reruns

Keep execution state outside the image engine in the production plan or asset
manifest:

1. Record API success as `generated`.
2. Review the node and record `accepted` or `rejected` with evidence.
3. Freeze accepted files and their input/prompt versions.
4. Rebuild only rejected nodes and descendants of visually changed parents.
5. Leave unrelated accepted branches byte-for-byte unchanged.

Metadata-only manifest edits do not invalidate visual descendants. A changed
canonical image, family anchor, prompt mechanism, crop, or target ratio does.
Cap automated retries; after repeated visual failure, mark the node `blocked`
or return it to a human decision gate instead of looping.

The generation DAG may contain anchors, calibration boards, and proof inputs.
Count only manifest assets whose role is `deliverable` or `derivative` when
reporting scope.

## Negative Constraints

Write negative constraints as visual risks, not just “ugly”:

- no old brand mark;
- no body-part/anatomical silhouette;
- no misleading letterform;
- no mascot if the product is not mascot-led;
- no fake generated text;
- no watermark;
- no decorative tile if the target platform supplies the mask/background.

## Cleanup

After approval, delete or move rejected generations outside the product repo. A future agent will treat files in `resources/brand/generated/` as usable unless the directory structure says otherwise.
