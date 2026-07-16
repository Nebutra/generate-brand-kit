# Wordmark-to-Font Workflow Contract

## Contents

1. Evidence model
2. Structural dependency map
3. Prompt contract
4. Review matrix
5. Failure modes
6. Completion contract

## Evidence Model

Classify every rule before generation:

| Level | Meaning | Example |
|---|---|---|
| Direct | Visible in the approved wordmark | `A` counter, `R` leg, `C` terminal |
| Repeated | Visible in two or more source glyphs | shared wedge ending, stem weight |
| Inferred | Needed to construct an unseen glyph | `B` lower bowl, `Q` tail |
| Proposed | New system with no source evidence | lowercase x-height, descender depth |

Direct and repeated evidence may be locked. Inferred and proposed rules must pass a control-stage review before becoming dependencies.

## Structural Dependency Map

Map missing uppercase letters to the source shapes that actually help construct them. Adjust this map to the available wordmark; do not blindly require these exact sources.

| Construction family | Typical targets | Useful source evidence |
|---|---|---|
| Round/open | C, G, O, Q, S | open curve, bowl, aperture, terminal |
| Bowl/stem | B, D, P, R | vertical stem, bowl, counter, leg |
| Vertical/horizontal | E, F, H, I, J, L, T, U | stem, crossbar, foot, curved base |
| Diagonal | A, K, M, N, V, W, X, Y, Z | diagonal contrast, apex, junction, wedge |

Default lowercase controls:

| Control | Locks |
|---|---|
| `o` | x-height, round overshoot, bowl/counter weight |
| `n` | stem, shoulder, join, lowercase terminal |
| `e` | aperture and cross-stroke behavior |
| `s` | spine tension and terminal balance |
| `a` | bowl-to-stem relationship and lowercase voice |
| `g` | descender, link, ear, complex counter rhythm |

Examples of downstream dependencies:

- `b d p q` depend on `o` plus `n` or `g`.
- `h m r u` depend on `n`.
- `c` depends on `o/e`; `z` on `s/e`.
- `j y` depend on accepted descender behavior from `g`.
- `v w x` use the accepted lowercase weight plus diagonal evidence from uppercase sources.

## Prompt Contract

Use one compiler, not hand-written sibling prompts. A task prompt should have this order:

```text
TASK
Create exactly one <case> Latin glyph: <character>.

REFERENCE AUTHORITY
Reference 1 is the approved full wordmark and controls global DNA.
References 2..N are isolated <source glyphs or accepted controls> and control
only <specific construction evidence>. Derive the target from these references;
do not import an unrelated typeface.

SHARED GLYPH DNA
<stable observable proportion, stroke, terminal, curve, counter and diagonal rules>

TARGET CONSTRUCTION
Use the conventional readable skeleton of <character>. Resolve <character-specific
features> with the supplied evidence. Identity comes before novelty.

OUTPUT CONTRACT
One black glyph on pure white. Fixed invisible cap/x-height/baseline/descender
metrics. Optical centering and ample side bearings. Hard flat edges.

NEGATIVE CONSTRAINTS
No word, second glyph, board, caption, punctuation, symbol, texture, mockup,
shadow, bevel, extrusion, color, gradient, ornament, calligraphy, italic drift,
or external-typeface imitation. Render exactly <character>.
```

Do not encode unsupported measurements as facts. Metric percentages may be proposed as composition controls, but must be normalized after vectorization.

Store mother-glyph paths, target dependencies, accepted controls, constructions,
and shared DNA in one config derived from
`references/glyph-dag-config.example.json`. Compile sibling tasks with
`scripts/compile_glyph_dag.py`; its report freezes prompt hashes and reference
lists for selective reruns.

## Review Matrix

| Gate | Pass criteria | Failure action |
|---|---|---|
| Mother extraction | one glyph, intact counters, zero neighbor fragments | fix contour extraction; do not prompt around contamination |
| Uppercase candidate | exact character, source DNA, consistent weight/terminal | rerun the node with relevant mother refs |
| Lowercase controls | coherent x-height, weight, shoulder, bowl, aperture, descender | stop all remaining lowercase nodes |
| Full raster set | 26+26 exact characters, no effects, family contact sheets pass | reject individual node and descendants |
| SVG outlines | counters open, no debris, acceptable point count, XML valid | retune contour threshold/epsilon |
| Font binary | 53 mapped characters including space, metrics normalized | fix builder before specimen review |
| Compiled specimen | source word remains recognizable; alphabets share rhythm | mark Alpha blocked or refine outlines/metrics |

## Failure Modes

### External-font contamination

Symptom: missing glyphs suddenly resemble a familiar font rather than the approved wordmark.

Cause: an unrelated font was used as a base, named in prompts, or treated as a structural reference.

Fix: remove it from all references and prompts; rebuild from isolated source glyphs. External fonts may be used only as explicitly approved comparison or metric references, never silently as form donors.

### Adjacent-letter fragments

Symptom: mother-glyph cards contain small black slivers near an edge.

Cause: rectangular cropping with padding.

Fix: render only the selected contour and its child contours onto a clean canvas.

### Generic but internally consistent alphabet

Symptom: the set looks like a plausible typeface but loses the source wordmark's unusual features.

Cause: prompt adjectives dominate; local reference roles are vague.

Fix: name the source-specific construction evidence for each family and compare generated glyphs beside the original mother glyphs.

### Lowercase drift

Symptom: lowercase letters vary in x-height, serif logic, or historical voice.

Cause: all lowercase letters were generated in parallel from uppercase-only evidence.

Fix: approve control letters first and make the remaining lowercase nodes depend on them.

### Case-collision data loss

Symptom: only 26 files remain after assembling 52 glyphs.

Cause: `A.ext` and `a.ext` collided on a case-insensitive filesystem.

Fix: store uppercase and lowercase in separate directories and assert file counts before compilation.

### Successful API, unusable font

Symptom: every image request succeeded, but the font has filled counters, missing characters, or inconsistent baselines.

Cause: generation status was mistaken for acceptance; binary validation was skipped.

Fix: preserve separate generated, accepted-raster, accepted-vector, and compiled states. Render specimens from the actual compiled binary.

## Completion Contract

For an A-Z/a-z Alpha, report complete only when all are true:

- approved source wordmark is preserved;
- 26 uppercase and 26 lowercase accepted raster glyphs exist;
- 26 uppercase and 26 lowercase SVG glyphs exist;
- TTF and WOFF2 open successfully;
- A-Z, a-z, and space map correctly;
- uppercase, lowercase, and source-word specimens were rendered from the TTF;
- prompt count and billed cost are recorded;
- compiler report hashes match every executed DAG;
- remaining type-design work is stated explicitly.
