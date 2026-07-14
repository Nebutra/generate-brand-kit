# Generation DAG Patterns

## Built-in Backend

Run brand DAGs through the bundled adapter:

```bash
python3 scripts/run_brand_image_dag.py --repo /path/to/project
python3 scripts/run_brand_image_dag.py --repo /path/to/project --execute
```

The first command is a free dry-run. The second makes billed calls after approval.
The adapter discovers a sibling or globally installed `generate-image`, defaults to
`mox`, and lets that backend resolve the global `MOX_API_KEY`. Override discovery
with `GENERATE_IMAGE_SKILL=/path/to/generate-image`; never pass the key on the
command line.

## Recommended DAG

1. **Foundation material board**
   - Palette, material, lighting, texture, cultural mood.
   - No logo or text.

2. **Strategy tension sheet**
   - State 2-4 business relationships without drawing product nouns.
   - Map each relationship to candidate formal operations.

3. **Cultural/art foundation gate**
   - Complete `logo-cultural-art-foundations.md`'s concept dossier.
   - Cite the name, product, historical, artistic, scientific, typographic or craft source.
   - Define measurable construction invariants before prompts or billed calls.

4. **Parallel symbol families**
   - Generate at least three independent graphic-symbol families in the intended brand palette.
   - Each family uses one invariant operation and contains no wordmark or generated text.
   - Each task outputs one isolated symbol only, never a board or contact sheet.

5. **Parallel wordmark families**
   - Explore typography separately from the symbol branch.
   - Generate or typeset one CARINA/name wordmark per output with no graphic symbol.
   - Judge readability, name recognition, spacing, terminals and licensing independently.

6. **Separate proof gates**
   - Test unprompted readings, category similarity and 16-48 px behavior.
   - Score symbols without the name and wordmarks without a supporting icon.
   - Reject familiar-object sinks before downstream generation.
   - Include a separate monochrome reduction; do not replace the primary color
     candidate with the reduction.

7. **Human selection gates**
   - Approve one symbol and one wordmark independently or return to their branches.
   - No Hero, social, app icon or materialized mark may start before this gate.

8. **Deterministic lockup composition**
   - Clean/vectorize each approved master independently.
   - Compose, do not regenerate, the symbol and wordmark.
   - Tune scale, baseline, clear space and optical gap without changing either design.
   - Resolve into standalone symbol, standalone wordmark, primary combination lockup, horizontal/vertical arrangements,
     monochrome/reverse variants, and a simplified micro mark.

9. **App icon variants**
   - Classic, soft/lifestyle, technical/high-contrast, monochrome glyph.
   - Preserve the approved mark; vary only material and environment.

10. **Proof sheets**
   - Small-size legibility, light/dark backgrounds, icon family contact sheet.

11. **Backgrounds and scenes**
   - Hero, social, onboarding, documentation.
   - Use the same approved mark/material references; do not let backgrounds invent new logos.

## Serial Consistency Rules

- Put reference-locking assets before dependent tasks.
- Use image edit/reference inputs for shape consistency when available.
- If using prompt-only generation, explicitly constrain silhouette, composition, forbidden forms, material, lighting, and output intent.
- Promote approved masters to `approved/`; never make downstream tasks depend on exploratory folders.
- Do not use a purely serial mark pipeline before approval; one weak semantic
  decision will contaminate every descendant while appearing visually consistent.

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
