# Production Drift And Evidence

Use this reference whenever the user asks for a full VI production run, names authoritative design-system files, or challenges the completeness of the output.

## 1. Canonical Source Gate

Before producing assets:

1. Record the exact canonical files or directory named by the user.
2. Read those exact files, even when root mirrors appear identical.
3. Create a manifest mapping each canonical file to every generated or mirrored copy.
4. Compare bytes or normalized structured data before production.
5. Regenerate mirrors from the canonical source through one command.
6. Repeat the drift check after production.

The canonical source must be explicit. Files being identical at one moment does not make their ownership interchangeable.

## 2. Tangible Material Gate

Classify every selected deliverable by evidence type:

- `guideline`: written rule, construction logic, usage and misuse.
- `editable-source`: PPTX, Figma variables, vector master, HTML template, motion source, or equivalent.
- `export`: PNG, SVG, ICO, PDF, platform icon, campaign artwork, or equivalent.
- `external-handoff`: evidence-dependent legal, compliance, fabrication, licensing, audio, or specialist work.

Completion requires the evidence type promised by the item's production contract. A guideline does not complete an editable-source or export requirement.

## 3. Coverage Gate

Before billed generation, report:

- selected items;
- required items;
- image-bearing items;
- editable templates;
- deterministic exports;
- external handoffs;
- expected image calls and estimated cost.

For full production, build the image DAG across all selected image-bearing branches. Four hero-style images are an exploration sample, not a VI delivery.

## 4. Promotion Gate

Use separate states and paths:

`planned -> generated -> reviewed -> accepted/promoted`

Rejected work moves to a quarantine path and cannot be referenced by production files. Provider success is not design acceptance.

## 5. Single Evidence Source

Maintain one machine-readable evidence manifest. Generate these views from it:

- production plan statuses;
- DAG status;
- item-level evidence records;
- acceptance report;
- required completion counts.

Each selected item must finish as exactly one of:

- `complete`
- `blocked`
- `not-applicable`
- `external-handoff`

Never leave `planned` in a final production handoff. A blocked record must name the missing input or capability and the precise resume action.

## 6. Completion Language

Report completion as a ratio, for example `111/128 required items complete`, followed by blocked classes. Do not describe the whole scope as complete when vector masters, Figma variables, QR payloads, compliance evidence, or specialist assets remain blocked.

## Carina Incident Lessons

- Reading root mirrors instead of the user-named `extended/` sources hid the ownership problem even though the files were initially identical.
- A hand-written DAG status overstated completion while the item plan still contained planned work.
- General Markdown documents were incorrectly treated as substitutes for templates and exports.
- A six-image application batch covered only hero/social/documentation surfaces and did not represent the selected AI SaaS VI scope.
- The corrected process used explicit canonical-source sync, a 20-image application DAG, visual promotion/quarantine, item-level evidence files, and generated terminal statuses.
