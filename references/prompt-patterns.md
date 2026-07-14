# Prompt Patterns

## Foundation Board Prompt

Use for mood, palette, and material before logo work:

```text
Create a <brand> material and palette reference board, not a logo.
Arrange <materials/metaphors> in a clean <layout style>.
Palette: <named colors>. Lighting: <direction/quality>.
Design feeling: <era/product/culture>. No text, no logo, no watermark.
```

## Graphic Symbol Study Prompt

Do not write this prompt until the cultural/art concept dossier is complete and
compiled through `logo-prompt-compiler.md`.

```text
Design one original standalone brand symbol for <category>, centered on a plain
<background>. It should feel <three perceptual qualities>. Create a <holistic
silhouette> defined by <one signature visual event>. Use <curve/angle/mass/
counterform behavior>. Palette: <colors and structural roles>. Make it authored,
optically balanced, memorable at small size, and suitable for a long-lived
international identity. One symbol only, no text or board. Avoid <three collisions>.
```

Run this prompt separately for at least three operations. Do not ask one
generation to produce a random logo grid; each family needs a stated invariant.

When external reference images are justified, select them through the provenance
and operation rules in `logo-design-principles.md` and append an explicit
non-copying clause.
Send one candidate per generation; never ask for a board or variants.

## Wordmark Study Prompt

```text
Create exactly one typographic wordmark reading <BRAND>, with no graphic symbol.
Typography strategy: <humanist/geometric/grotesque/serif/etc>.
Distinctive invariant: <terminal/counter/width/stress/rhythm rule>.
Keep every letter immediately readable and spell <BRAND> exactly once.
Plain background. No icon, monogram, board, variants, mockup or extra text.
```

Treat generated wordmarks as direction studies. Recompose the approved direction
with real licensed fonts and vector typography before production.

## Approved Direction Prompt

```text
Refine the approved <brand> form family governed by <operation>.
Preserve these invariants: <geometry/spacing/relationship>.
Remove incidental object readings identified in review: <collisions>.
Refine only the approved <symbol/wordmark> master at 16, 24, 32 and 48 px,
plus a separate monochrome reduction for validation. Do not introduce the other
logo component in this call.
```

## Lockup Composition Rule

Do not use image generation. Place the approved symbol and approved wordmark as
unchanged assets; tune only scale ratio, optical gap, baseline, alignment and
clear space. Export horizontal and vertical arrangements from the same masters.

## Production Icon Prompt

```text
Convert the approved <brand> mark into a production app icon asset.
Preserve the exact mark relationship: <shape + signal>.
Target: <desktop/mobile/web>. Output intent: <transparent/opaque/adaptive>.
Use <material/lighting/depth>. Readable at 48 px.
Do not add <extra stones/background/tile/text/old brand>.
```

## Background Prompt

```text
Create a <brand> <hero/social/onboarding> background using the approved mark and material references.
Composition: <where product screenshot/text will sit>.
Mood: <culture/product tone>. Keep low visual noise behind UI.
No generated text, no extra logos, no watermark.
```

## Standing Negative Constraints (append to every generation prompt)

Ban the AI-slop signature explicitly; models default to it:

```text
No purple-blue gradients, no floating gradient orbs, no glassmorphism,
no sparkle/star AI icons, no fake 3D depth or bevels, no watermark,
no generated text.
```

## Prompt Hygiene

- Name colors and materials; do not rely on vague “modern” alone.
- State product context: developer tool, consumer app, operational SaaS, game, venue, etc.
- State what must stay fixed and what may vary.
- Use “not a logo” for foundation boards to prevent premature marks.
- Use “approved mark” for downstream outputs to prevent drift.
- Never include a concrete object metaphor unless the brand is intentionally
  pictorial and collision review has approved that object.
- Prefer verbs and spatial relationships over nouns: interrupt, align, retain,
  reverse, attenuate, branch, rejoin, offset, phase and contain.
