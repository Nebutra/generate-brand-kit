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
   - When the user names canonical source files or a canonical variant directory, read those exact files directly. Do not silently substitute root mirrors, compact variants, generated copies, or apparently identical siblings.
   - If canonical and mirror sources coexist, create a source manifest and run a byte-level drift check before production. Regenerate mirrors from the canonical source; never edit both sides independently.
   - If the repo is unfamiliar, run `scripts/scan_brand_assets.py <repo> --brand-term <old> --brand-term <new>` for an inventory seed.

2. **Select modules and define the target material list before generating.**
   - Select composable VI modules from `references/vi-deliverables.json`. Use a scene profile only as a starting suggestion, then add or remove modules based on actual consumption. Never model completeness as a linear `core/digital/full` ladder.
   - Mark every selected item `required`, `optional`, `not applicable`, or `external handoff`; inventory deliverables item by item rather than collapsing them into broad categories.
   - Create an inventory of every slot the product consumes: SVG, PNG, ICNS, ICO, app config icons, favicons, splash images, README/hero/social backgrounds, mobile adaptive icons, in-app logos, docs images, and generated source masters.
   - Consider A1-A5 foundations, B1-B13 physical/application modules, and C1-C14 AI SaaS product/trust modules. AI SaaS modules cover product identity, AI disclosure, runtime states, prompts, evidence, safety, privacy, developer experience, lifecycle, enterprise trust, provenance, accessibility, ecosystem architecture, motion, and sonic behavior.
   - Use `references/asset-taxonomy.md` for common slots and sizes.
   - Identify build commands and generated outputs. Do not replace only the visible logo while leaving compiled assets stale.
   - When the user asks to produce or deliver a VI, compile the selected items into `brand-vi-production-plan.json` using `references/production-routing.json`. Every item needs a producer, output, dependency gate, status, and acceptance check.
   - Before generation, calculate and show the selected-item count, required-item count, planned tangible outputs, and expected billed image count. A small exploratory image batch is not a full-scope production plan.

3. **Distill strategy and philosophy into VI rules.**
   - Establish the evidence level: supplied facts, repo evidence, stakeholder hypothesis, or research-backed finding. Do not invent market research or claim legal clearance.
   - Abstract the brand IP from the product's business scenario — what the product does or means for its buyers. Never promote an incidental metaphor (from internal docs, the agent's own process language, or this skill's documentation) into the client brand's IP.
   - Name, language variants, tone, design philosophy, cultural references, material metaphors, shape grammar, palette, typography, imagery, motion if relevant, and negative constraints.
   - Position against the current aesthetic landscape with `references/trends-2026.md`; ground craft decisions in `references/design-theory.md`; pull stage-appropriate visual references via `references/inspiration-sources.md`.
   - Treat user aesthetic direction as product strategy, not decoration.
   - Write or update a `visual-identity.md` / `brand-vi-inventory.md` style document before mass generation.
   - Use `references/workflow.md` for the decision gates.

4. **Derive mark form through operations, not pictograms.**
   - Translate the business scenario into 2-4 tensions or relationships such as controlled/autonomous, local/distributed, continuous/reversible, open/bounded, or individual/system.
   - Translate each relationship into formal operations: join, split, interrupt, offset, repeat, phase, fold, overlap, crop, counterform, shared axis, or controlled gap. Treat trend reports as an operation vocabulary, never as a style menu.
   - Explore the graphic symbol and typographic wordmark on separate DAG branches. Never ask one image-generation call to invent both. Approve each independently, then create lockups by deterministic composition without redesigning either master. Unless explicitly not applicable, a production VI ships a responsive logo suite: standalone symbol, standalone wordmark, primary symbol+wordmark lockup, horizontal/vertical lockups, monochrome/reverse variants, and a small-size simplification.
   - Explore at least three structurally different families in the intended brand palette. Color may carry hierarchy, overlap, modular distinction, and emotional tone; do not force monochrome as the client-facing concept. Separately verify that each candidate survives a monochrome reduction.
   - Read `references/logo-design-principles.md` before mark exploration. Use external visual references only when their provenance and reuse purpose are clear; references may inform craft, never substitute for product evidence or become a style menu.
   - Read `references/logo-cultural-art-foundations.md` and complete its concept dossier before any graphic-symbol generation. Require a verified typology or source, a named artistic/scientific/craft principle, and a reproducible construction canon; otherwise stop before the billed generation gate.
   - Compile the approved dossier through `references/logo-prompt-compiler.md`. Keep essays and product nouns out of the model prompt, but preserve the **construction payload**: topology, primitive relationship, governing ratio/rhythm, signature counterform, and terminal rule. A short prompt without those invariants is under-specified and will regress to category clichés.
   - Before billed generation, create a family matrix. Every family must differ in primary source, topology, dominant silhouette, and construction invariant; changing only `fold` to `phase` or `interrupt` does not create a new family. Reject a batch when more than two families share the same compact-mass-plus-gap grammar.
   - Read the mark-form derivation and collision rules in `references/design-theory.md`.

5. **Design the generation DAG deliberately.**
   - Branch before convergence: strategy tensions -> construction prototypes -> independent symbol families and wordmark families -> separate collision/readability reviews -> approved symbol + approved wordmark -> deterministic lockup composition -> variants -> product outputs -> proof sheets.
   - Treat image generation as a variation/rendering stage, not the source of the core idea. Each symbol task must inherit a reviewed construction prototype expressed as text invariants or a provenance-clear shape guide.
   - Put shared references early in the DAG when object/shape consistency matters. Do not rely on prompt adjectives alone.
   - If the user rejects hard shape guides, make prompts explicit enough to constrain form, composition, material, and banned readings.
   - Use `references/generation-dag.md` and `references/prompt-patterns.md`.
   - For a production request, the DAG must span every selected image-bearing branch. Do not stop after logo, hero, social, or four representative boards when the scope also selects presentation, campaign, runtime-state, trust, or other application materials.
   - Keep exploration, approved masters, generated candidates, accepted production assets, and rejected/quarantined assets in separate paths. A successful API response is only `generated`; promotion requires visual review.

6. **Generate, judge, and promote assets.**
   - Use the bundled adapter `scripts/run_brand_image_dag.py` for raster DAGs. It automatically discovers the sibling `generate-image` skill, defaults to its `mox` provider, and reads `MOX_API_KEY` through that backend. Do not ask the user to restate the path or credential setup.
   - Run the adapter without `--execute` first to show the prompt count and estimated billed cost. Use `--execute` only after the user approves the real generation.
   - Set `GENERATE_IMAGE_SKILL` only when auto-discovery cannot locate the backend. Do not copy credentials or vendor a second generate-image implementation into this skill.
   - Promote only approved masters into an `approved/` or equivalent stable directory.
   - Keep rejected explorations out of the product path; remove or quarantine them so future agents cannot accidentally consume them.
   - A rejected mark blocks only tasks declaring `mark-approved`. Continue strategy, verbal identity, typography, color, tokens, AI product patterns, accessibility, trust and governance work that does not depend on the mark.

7. **Convert into production-ready assets and handoffs.**
   - Hand-vectorize or edit SVG for production marks when raster output is not enough.
   - Export all required bitmap sizes and platform formats. Use existing repo icon scripts when present.
   - For desktop icons, verify alpha/transparent intent; for mobile icons, respect platform-specific opaque/adaptive requirements.
   - Produce editable templates and specifications where supported. For trademark clearance, font licensing, print proofs, packaging dielines, environmental engineering, original music, and construction files, create a precise external-handoff brief unless qualified tooling and source data are available.
   - Distinguish four evidence classes: guideline/specification, editable template/source, exported asset, and external handoff. A Markdown specification cannot by itself complete an item whose contract requires an editable template, platform export, vector master, motion file, or audio asset.

8. **Integrate and verify.**
   - Replace source assets, generated assets, app config references, in-app components, documentation, and localized product names.
   - Run relevant asset scripts, type checks, tests, JSON validation, image/file checks, and legacy scans.
   - Visually inspect critical assets in context, especially dock/app icons and first-run/empty states.
   - Reconcile the production plan, DAG status, item evidence, and acceptance report from one machine-readable evidence manifest. Never hand-maintain conflicting completion claims in several files.
   - Materialize one evidence record per selected item with terminal status, concrete paths, acceptance rule, and blocker/resume action. A production run may end only when no selected item remains `planned`.
   - Re-run canonical-source drift checks after production and fail the handoff if mirrors have diverged.

9. **Commit only after hygiene.**
   - Scan for legacy names, rejected paths, stale generated outputs, and old remote/upstream references when a full brand migration is requested.
   - If committing, stage only intended files and summarize verification honestly.

## Useful Resources

- `scripts/scan_brand_assets.py`: inventory likely brand files and text hits in a repo.
- `scripts/create_brand_vi_scaffold.py`: create a neutral brand-VI scaffold in a target repo.
- `scripts/run_brand_image_dag.py`: zero-config adapter for the installed `generate-image` backend; dry-run by default.
- `references/workflow.md`: detailed process, decision gates, and “water-shape” interpretation.
- `references/asset-taxonomy.md`: product-consumable asset checklist.
- `references/vi-deliverables.json`: machine-readable A1-B13 deliverable catalog and composable scene profiles.
- `references/production-routing.json`: producer, output, phase, and gate routing for every A/B/C module.
- `references/production-contract.md`: definition of done and resumable gate semantics for full production requests.
- `references/generation-dag.md`: DAG design and consistency patterns.
- `references/prompt-patterns.md`: prompt architecture for professional visual generation.
- `references/validation.md`: QA, integration, and legacy cleanup checks.
- `references/trends-2026.md`: current aesthetic trends — rising, falling, and trend-tracking sources.
- `references/design-theory.md`: durable identity theory — strategy frameworks, distinctive-asset science, craft criteria, verification battery, verbal identity.
- `references/inspiration-sources.md`: reference galleries mapped to pipeline stages, GitHub brand-as-code ecosystem (DESIGN.md schema, icon slot canon, DTCG tokens), and AI-era anti-slop practice.
- `references/logo-design-principles.md`: research-backed logo principles, current trend signals, collision risks, construction rules, and review gates.
- `references/logo-cultural-art-foundations.md`: evidence labeling, OpenAI/Anthropic/Perplexity benchmark analysis, cultural and art-theory foundations, concept dossier, and construction canon.
- `references/logo-prompt-compiler.md`: separates evidence, design reasoning, and model-facing art direction; includes concise prompt templates and failure modes.
- `references/production-drift-and-evidence.md`: canonical-source selection, tangible-material coverage, evidence reconciliation, and truthful completion reporting.

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
- Do not claim a full-scope delivery from a representative sample. Report required-complete/required-total counts and name every blocked item class.
- Do not mark an image task complete merely because the provider returned a file. Generated assets must pass visual review and be promoted into an accepted path; rejected assets must be quarantined.
- Do not let the production plan, DAG status, and acceptance report become separate sources of truth. Generate all three from the same evidence manifest.
- Do not send a trend archive to an image model. Use at most two provenance-clear, operation-relevant craft references per candidate and generate one logo per output.
- Do not deliver only a symbol or only a wordmark as the default logo system. Missing responsive-suite members require an explicit `not-applicable` rationale tied to real brand surfaces.
- Do not generate a graphic symbol and typographic wordmark in the same exploration image. Combination generation is prohibited before both masters are separately approved; compose lockups from the approved assets instead.
- Do not generate a graphic symbol from an ungrounded abstract prompt. Missing provenance, named theory, or measurable construction invariants blocks generation; never invent the historical meaning after seeing an output.
- Do not paste product mechanisms, cultural essays, exact construction recipes, or long negative lists into image prompts. Translate them into a concise visual thesis first; otherwise the model will produce diagrams instead of identity.
- Do not strip the construction payload while shortening a prompt. Exact object diagrams are prohibited, but topology, ratios, repeat logic, counterform behavior, and terminal rules are required.
- Do not call cosmetic changes separate concept directions. A six-direction batch must contain six distinguishable construction families or be reduced before any billed call.
