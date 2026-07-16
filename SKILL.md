---
name: generate-brand-vi
description: Create or migrate a modular brand/VI kit and production asset pipeline for a repo, app, system, product, organization, or campaign. Use when Codex is asked to design a visual identity, define brand strategy and verbal identity, replace an existing brand, generate logo/icon/app-icon/hero/social/print/packaging/environment/motion-ready assets, build image-generation DAGs and prompts, translate brand philosophy into product-consumable files, audit old brand assets, or clean up legacy/rejected visual material.
---

# Generate Brand VI

## Core Idea

Create brand systems that behave like water: take the shape of the project, product surface, culture, and philosophy before hardening into assets. Do not start with a logo prompt. Start with the target structure, existing repo conventions, product consumption paths, and the brand's meaning.

## Workflow

1. **Read the existing system first.**
   - Inspect repo style docs, asset folders, app configs, icon build scripts, locale/product names, README/social images, and current brand terms.
   - If the repo is unfamiliar, run `scripts/scan_brand_assets.py <repo> --brand-term <old> --brand-term <new>` for an inventory seed.

2. **Select modules and define the target material list before generating.**
   - Select composable VI modules from `references/vi-deliverables.json`. Use a scene profile only to seed optional candidates, then decide each item from actual consumption. Never model completeness as a linear `core/digital/full` ladder.
   - Mark every selected item `required`, `optional`, `not-applicable`, or `external-handoff`; inventory deliverables item by item rather than collapsing them into broad categories.
   - Create an inventory of every slot the product consumes: SVG, PNG, ICNS, ICO, app config icons, favicons, splash images, README/hero/social backgrounds, mobile adaptive icons, in-app logos, docs images, and generated source masters.
   - Consider A1-A6 foundations and adaptive identity, B1-B13 physical/application modules, and C1-C14 AI SaaS product/trust modules. AI SaaS modules cover product identity, AI disclosure, runtime states, prompts, evidence, safety, privacy, developer experience, lifecycle, enterprise trust, provenance, accessibility, ecosystem architecture, motion, and sonic behavior.
   - Use `references/asset-taxonomy.md` for common slots and sizes.
   - When C1-C14 items are selected, use `references/ai-saas-acceptance.md` to turn static scope rows into state, flow, accessibility, trust, token-parity, and product-consumption evidence.
   - Identify build commands and generated outputs. Do not replace only the visible logo while leaving compiled assets stale.
   - When the user asks to produce or deliver a VI, record item decisions in `brand-vi-scope.json`, then run `scripts/compile_brand_vi_scope.py` to compile `brand-vi-production-plan.json` using `references/production-routing.json`. Every item needs a requirement, producer, output, dependency gate, status, and acceptance check. Use item overrides for heterogeneous surfaces; never apply one module route blindly to every child.
   - When an approved mark must support many campaigns, product states, materials, or cultural contexts, select a configurable Logo Skin module from `references/logo-skin-system.md`. Keep symbol skins, wordmark variants, lockups, applications, and mockups as separate asset classes.

3. **Distill strategy and philosophy into VI rules.**
   - Establish the evidence level: supplied facts, repo evidence, stakeholder hypothesis, or research-backed finding. Do not invent market research or claim legal clearance.
   - Abstract the brand IP from the product's business scenario — what the product does or means for its buyers. Never promote an incidental metaphor (from internal docs, the agent's own process language, or this skill's documentation) into the client brand's IP.
   - Name, language variants, tone, design philosophy, cultural references, material metaphors, shape grammar, palette, typography, imagery, motion if relevant, and negative constraints.
   - Position against the current aesthetic landscape with `references/trends-2026.md`; ground craft decisions in `references/design-theory.md`; pull stage-appropriate visual references via `references/inspiration-sources.md`.
   - Apply `references/research-evidence.md`: prefer primary sources, label hypotheses and aesthetic references, date time-sensitive claims, and never repeat unsupported quantitative precision.
   - Treat user aesthetic direction as product strategy, not decoration.
   - Write or update a `visual-identity.md` / `brand-vi-inventory.md` style document before mass generation.
   - Use `references/workflow.md` for the decision gates.

4. **Derive mark form through operations, not pictograms.**
   - Translate the business scenario into 2-4 tensions or relationships such as controlled/autonomous, local/distributed, continuous/reversible, open/bounded, or individual/system.
   - Translate each relationship into formal operations: join, split, interrupt, offset, repeat, phase, fold, overlap, crop, counterform, shared axis, or controlled gap. Treat trend reports as an operation vocabulary, never as a style menu.
   - Decide whether the identity should begin with a wordmark, monogram, symbol, or responsive family. Do not assume a standalone icon is required.
   - Explore at least three structurally different families in black and white before selecting a direction. Run semantic-collision checks before adding color or material.
   - Read the mark-form derivation and collision rules in `references/design-theory.md`.

5. **Design the generation DAG deliberately.**
   - Branch before convergence: strategy tensions -> operation studies -> three or more form families -> collision review -> one approved direction -> production-clean mark -> variants -> product outputs -> proof sheets.
   - Put shared references early in the DAG when object/shape consistency matters. Do not rely on prompt adjectives alone.
   - For a coherent variant family, let each formal child reference the approved canonical identity for shape and a non-deliverable family anchor for shared composition, material, or rendering language. Use this dual-reference pattern only when both kinds of consistency are required.
   - Compile related prompts from one stable contract: invariant lock, explicit reference roles, one variation mechanism, scene constraints, and targeted negative constraints. Convert style labels into observable layout, color, process, surface, and boundary rules.
   - Write `brand-image-spec.json`, then run `scripts/compile_brand_image_dag.py --stage exploration`. Generate one isolated symbol or one isolated wordmark per node; do not mix unsettled marks, alphabets, applications, or mockups on a board.
   - Add project-specific pad images only through `explorationReferences` entries with explicit `path`, `role`, and prohibited contribution. References may teach composition, craft, or typography; they must not silently donate another brand's identity.
   - Stop at human approval. Recompile with `--stage production --approved-symbol ... --approved-wordmark ...` only after canonical masters are selected. Never place downstream production tasks behind an unapproved candidate.
   - If the user rejects hard shape guides, make prompts explicit enough to constrain form, composition, material, and banned readings.
   - Use `references/generation-dag.md` and `references/prompt-patterns.md`.

6. **Generate, judge, and promote assets.**
   - Use the bundled adapter `scripts/run_brand_image_dag.py` for raster DAGs. It automatically discovers the sibling `generate-image` skill, defaults to its `mox` provider, and reads `MOX_API_KEY` through that backend. Do not ask the user to restate the path or credential setup.
   - Run the adapter without `--execute` first to show the prompt count and estimated billed cost. Use `--execute` only after the user approves the real generation.
   - Set `GENERATE_IMAGE_SKILL` only when auto-discovery cannot locate the backend. Do not copy credentials or vendor a second generate-image implementation into this skill.
   - Promote only approved masters into an `approved/` or equivalent stable directory.
   - Treat API success as `generated`, never as `accepted`. Review identity fidelity, family consistency, sibling differentiation, composition, and asset-class dimensions before promotion.
   - Freeze accepted nodes. Rerun failed nodes or invalidated descendants instead of rebuilding unrelated successful branches; if an accepted parent changes visually, invalidate every descendant that consumes it.
   - Use `scripts/update_brand_asset_state.py` to record generated/accepted/complete states and file hashes. When a canonical checksum changes, let it invalidate declared descendants before any rerun.
   - Record formal outputs and non-deliverable dependencies in a brand asset manifest. Validate it with `scripts/validate_brand_asset_manifest.py` before reporting production completion.
   - Keep rejected explorations out of the product path; remove or quarantine them so future agents cannot accidentally consume them.
   - A rejected mark blocks only tasks declaring `mark-approved`. Continue strategy, verbal identity, typography, color, tokens, AI product patterns, accessibility, trust and governance work that does not depend on the mark.

7. **Convert into production-ready assets and handoffs.**
   - Produce a clean SVG master through deliberate vector editing or a verified deterministic tracing workflow when raster output is not enough. Record the method and inspect counters, point count, viewBox, small-size behavior, and source fidelity.
   - When the user asks to expand approved logo lettering into A-Z/a-z, a brand display font, or installable TTF/WOFF2, read `subskills/extend-wordmark-font/SKILL.md` completely and follow its mother-glyph, control-glyph, DAG, vectorization, compilation, and binary-validation gates. Do not introduce an unrelated base font unless the user explicitly approves it as a form source.
   - Export all required bitmap sizes and platform formats. Use existing repo icon scripts when present.
   - For desktop icons, verify alpha/transparent intent; for mobile icons, respect platform-specific opaque/adaptive requirements.
   - Produce editable templates and specifications where supported. For trademark clearance, font licensing, print proofs, packaging dielines, environmental engineering, original music, and construction files, create a precise external-handoff brief unless qualified tooling and source data are available.

8. **Integrate and verify.**
   - Replace source assets, generated assets, app config references, in-app components, documentation, and localized product names.
   - Run relevant asset scripts, type checks, tests, JSON validation, image/file checks, and legacy scans.
   - Visually inspect critical assets in context, especially dock/app icons and first-run/empty states.
   - Validate each asset class at its native target ratio and dimensions. Regenerate an incompatible master rather than normalizing it with a crop that changes the approved composition.
   - Read `references/consumer-integration.md`. Keep the design workspace outside the product repo; import only approved canonical assets, required derivatives, evidence, licenses, manifest, and operational `AGENTS.md` guidance.
   - Run manifest validation with its production plan and `--production-complete` before claiming delivery. Add a repo-side `brand-check` for checksums, stale derivatives, legacy references, SVG/font structure, and consumer paths.

9. **Commit only after hygiene.**
   - Scan for legacy names, rejected paths, stale generated outputs, and old remote/upstream references when a full brand migration is requested.
   - If committing, stage only intended files and summarize verification honestly.

## Useful Resources

- `scripts/scan_brand_assets.py`: inventory likely brand files and text hits in a repo.
- `scripts/create_brand_vi_scaffold.py`: create a neutral brand-VI scaffold in a target repo.
- `scripts/compile_brand_vi_scope.py`: recompile an edited item-level scope without overwriting identity strategy or image work.
- `scripts/run_brand_image_dag.py`: zero-config adapter for the installed `generate-image` backend; dry-run by default.
- `scripts/compile_brand_image_dag.py`: compile exploration or post-approval production DAGs from one stable prompt contract and emit prompt/reference hashes.
- `scripts/validate_brand_asset_manifest.py`: dependency, status, file, PNG-dimension, aspect-ratio, and acceptance validator for production manifests.
- `scripts/update_brand_asset_state.py`: calculate output metadata, record review state, sync terminal plan state, and invalidate descendants after canonical changes.
- `references/workflow.md`: detailed process, decision gates, and “water-shape” interpretation.
- `references/asset-taxonomy.md`: product-consumable asset checklist.
- `references/ai-saas-acceptance.md`: testable C1-C14 product-flow, state, accessibility, trust, lifecycle, ecosystem, motion, and sound acceptance profiles.
- `references/vi-deliverables.json`: machine-readable A1-B13 deliverable catalog and composable scene profiles.
- `references/production-routing.json`: producer, output, phase, and gate routing for every A/B/C module.
- `references/production-contract.md`: definition of done and resumable gate semantics for full production requests.
- `references/brand-asset-manifest.schema.json`: machine-readable asset/dependency/QA manifest contract.
- `references/generation-dag.md`: DAG design and consistency patterns.
- `references/prompt-patterns.md`: prompt architecture for professional visual generation.
- `references/logo-skin-system.md`: configurable mark-variant families, dependency roles, and asset-class boundaries.
- `references/validation.md`: QA, integration, and legacy cleanup checks.
- `references/consumer-integration.md`: canonical/derivative/evidence packaging, product consumption, fonts, licenses, Agent rules, and repo-side checks.
- `references/trends-2026.md`: current aesthetic trends — rising, falling, and trend-tracking sources.
- `references/design-theory.md`: durable identity theory — strategy frameworks, distinctive-asset science, craft criteria, verification battery, verbal identity.
- `references/research-evidence.md`: evidence levels, source hierarchy, freshness, conflict, and quantitative-claim discipline.
- `references/inspiration-sources.md`: reference galleries mapped to pipeline stages, GitHub brand-as-code ecosystem (DESIGN.md schema, icon slot canon, DTCG tokens), and AI-era anti-slop practice.
- `subskills/extend-wordmark-font/SKILL.md`: derive an A-Z/a-z display alphabet from approved wordmark glyphs, then produce PNG/SVG glyphs and TTF/WOFF2 packages.

## Guardrails

- Do not derive the brand IP from the skill's own process metaphors or other incidental language; the mark must abstract the product's business scenario and pass the one-sentence buyer test (`references/design-theory.md`).
- Do not accept AI-slop defaults: purple-blue gradient orbs, glassmorphism, sparkle icons, fake 3D depth, default-grotesk typography. Ban them in prompts and reject them in review.
- Do not ship brand color pairings that fail WCAG 2.2 AA contrast; emit palettes as verified foreground/background pairs.
- Do not let rejected exploration files remain in the product-consumable asset tree.
- Do not preserve old brand remotes, names, docs, or assets when the user asks for a complete migration.
- Do not confuse compatibility code named `legacy` with visual legacy assets; inspect context before deleting.
- Do not introduce a landing-page aesthetic into operational software unless the product surface actually calls for it.
- Do not present strategy hypotheses as research, trademark searches as legal opinions, screen color as a print proof, concept packaging as a production dieline, or environment mockups as construction drawings.
- Do not use one-off image outputs as final vectors when the repo needs SVG or platform icon formats.
- Do not encode a product noun, feature, or metaphor as a literal pictogram merely because it is easy to prompt. Formal relationships must survive without the explanatory story.
- Do not allow a single generated core-mark candidate to become the parent of downstream assets before a human collision review approves it.
- Do not report exploration images as a delivered Brand VI. A production request ends only with item-level `complete`, `blocked`, `not-applicable`, or `external-handoff` status.
- Do not count family anchors, reference boards, rejected candidates, or QA evidence as deliverables.
- Do not make a style name carry the prompt; require observable visual rules that distinguish sibling directions.
- Do not use a material board, logo board, or multi-asset composition as the parent of unsettled symbol or wordmark geometry.
