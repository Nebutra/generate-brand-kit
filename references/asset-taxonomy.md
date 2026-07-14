# Brand/VI Deliverable Taxonomy

Use this as a scoping matrix, not a mandate to produce every row. Mark each item `required`, `optional`, `not applicable`, or `external handoff`.

## Selection Model

- Use `vi-deliverables.json` as the canonical item-level A1-B13 catalog.
- Start from a scene profile only to reduce setup work, then compose the actual module set.
- A profile is not a package tier and does not imply that unselected modules are lower value.
- Keep strategy, verbal identity, rights, governance, source ownership, and validation as cross-system requirements.

## Strategy and Verbal Identity

- positioning, audience, category, value proposition, differentiators, brand architecture
- mission, vision, values, personality, brand idea, story, messaging pillars
- name variants, pronunciation, descriptor, tagline, tone of voice, vocabulary and writing examples
- evidence labels for supplied facts, repo evidence, hypotheses, and research findings

## Core Visual Identity

- primary, secondary, symbol, wordmark, lockup, monochrome, reverse, small-size, and co-brand variants
- default responsive suite: standalone symbol, standalone wordmark, primary symbol+wordmark combination, horizontal/vertical lockups, monochrome/reverse treatments, and simplified micro mark
- clear space, minimum size, construction/proportion rationale, background rules, misuse examples
- master SVG/PDF plus approved raster masters
- color palette with HEX/RGB/CMYK/Pantone targets and verified accessible foreground/background pairs
- typography hierarchy, fallback stack, licensing status, type scale, line height, weight, and multilingual behavior
- grid, spacing, alignment, composition, shape grammar, illustration, photography, texture, iconography, and data-visualization direction
- produce separate short-name/full-name Chinese, English, and bilingual construction sheets when A2 is selected
- produce explicit vertical/horizontal lockup sheets, color-misuse sheets, auxiliary-graphic crop/scale/density rules, and coordinate/grid construction where A1-A5 require them

## Digital Product and Runtime

- app logo SVG, favicon, social share image, splash, onboarding, empty/error/loading states
- macOS `.icns`, Windows `.ico`, Linux PNG sizes, Electron/Tauri/native build icons
- iOS icon sources and Android adaptive foreground/background/monochrome layers
- light/dark/high-contrast variants, design tokens, Figma/code mapping when in scope
- store icon, screenshots, feature graphics, README/docs hero, release image, email and notification templates
- QR rules: payload ownership, error-correction level, quiet zone, minimum reproduced size, contrast, logo-overlay limit, fallback URL, and scan tests across print/screen conditions

## AI SaaS Product and Trust Identity

Use C1-C14 for AI SaaS. Do not reduce these modules to decorative AI icons.

- **Product identity:** define product/marketing brand relationships, semantic tokens, component states, themes, data visualization, white-label/co-brand rules, and Figma-to-code mappings.
- **AI disclosure:** distinguish AI-generated, AI-assisted and AI-executed behavior; define persistent AI labels, model/provider attribution and capability-limit language.
- **Runtime states:** define understanding, planning, generating, streaming, tool use, approval, partial success, failure, cancellation and recovery without presenting fictional certainty or progress.
- **Conversation:** specify prompts, roles, system/tool messages, attachments, code, citations, regeneration, branching, history and context boundaries.
- **Evidence and uncertainty:** specify sources, freshness, confidence, verified/inferred/unknown/conflicting states, explanations, audit trails and limitations.
- **Safety and privacy:** cover refusals, policy blocks, model/tool outages, data retention, training use, tenant boundaries, third-party data flows, consent and deletion.
- **Developer experience:** cover developer portal, API/SDK docs, API keys, playgrounds, traces, token/cost display, integrations, changelogs, deprecations and migrations.
- **SaaS lifecycle:** cover authentication, onboarding, workspaces, roles, pricing, usage, credits, billing, trials, upgrades, support, status and incident communication.
- **Enterprise trust:** cover security/privacy/compliance pages, Trust Center, certifications, DPA, subprocessors, residency, SLA, Responsible AI and model cards.
- **Content provenance:** define generated-media origin, Content Credentials, model/version/edit history, metadata/watermark preservation and invalid/conflicting provenance states.
- **Accessibility:** meet WCAG 2.2 across streaming announcements, keyboard/focus behavior, non-color status cues, reduced motion, semantic code/tables/charts and user control of updates.
- **Ecosystem architecture:** govern first/third-party models, agents, plugins, connectors, templates, skills, verification states, customer-created agents and marketplace review.
- **Motion and sonic:** map motion/sound to AI states, include reduced-motion/static fallbacks, and avoid deceptive thinking or progress animations.

Treat privacy, compliance, Responsible AI, model-card and provenance claims as evidence-backed content. Legal or certification approval remains external.

## Marketing and Editorial

- website hero and campaign key visual
- social avatar, cover, post, story, short-video cover, ad, banner, and OpenGraph templates
- presentation master, report cover, chart/table styles, case-study and press-kit templates
- poster, brochure, flyer, event backdrop, signage artwork, and merchandise placement guides

## Corporate and Stationery

- business card, letterhead, envelope, email signature, document cover, invoice/quotation shell
- employee badge, lanyard, folder, form, certificate, uniform and vehicle application concepts
- use the B1 catalog rather than substituting one generic stationery mockup for payroll, attendance, leave, receipt, delivery, filing, desk, access, label, cup, pen, and award applications

## Flags and Public-Relations Items

- company flag, hanging flag, promotional flag and table flag with aspect ratio, pole/sleeve zone, single/double-sided behavior, bleed, material and viewing-distance rules
- greeting card, red envelope, invitation, calendar cover, branded umbrella and other selected B5 applications

## Packaging and Physical Product

- packaging architecture, label hierarchy, structural concept, artwork zones, regulatory-copy placeholders
- dieline artwork only when an authoritative supplier dieline and print specification are supplied
- material, finish, spot-color, barcode, bleed, safe-area, preflight, proof and sample-review requirements
- treat structural engineering, regulatory approval, and press proofing as external handoffs unless qualified inputs and tooling exist

## Environment and Wayfinding

- facade/reception sign, room/floor identification, directional and regulatory sign families
- office, retail, exhibition, event, wall graphic and vehicle application concepts
- location schedule, scale rules, material/finish and accessibility requirements
- treat site survey, structural calculations, fabrication and construction drawings as external handoffs
- for industrial B11 systems, add safety-color precedence, hazard/regulatory separation, viewing distance, durability, coding/label logic and 5S/7S information hierarchy

## Mascot and Character IP

- character concept and rationale, color master, monochrome master, silhouette and small-size tests
- front/side/back turnaround, proportion sheet, expression/pose library and basic dynamic poses
- application rules, exclusion zones, co-brand behavior, merchandise/print adaptations and misuse examples
- 3D appearance target, material/lighting rules and model handoff specification
- animation model sheet, key poses, motion principles, loop/static fallbacks and export requirements
- do not claim production-ready 3D topology, rigging, animation or character rights without the appropriate source workflow and review

## Motion and Sonic

- logo motion concept, motion principles, easing/duration tokens, UI micro-interaction rules
- video opener/closer, transitions, lower thirds, captions, livestream and podcast templates
- sonic logo brief, voice persona, UI sound taxonomy and audio-format requirements
- deliver original audio only with an appropriate generation/composition workflow and rights review

## Governance, Rights, and Delivery

- visual identity manual, quick-reference sheet, deliverable matrix, consumption map, generation DAG, prompt/rationale log
- approved/generated/processed separation, naming/version rules, changelog and ownership
- font/image/model/music/license register, trademark-search record, territory and expiry fields
- supplier handoff briefs, editable sources, export matrix, acceptance criteria and known limitations
- trademark availability and legal clearance require qualified legal review

## Verification Targets

- dimensions, alpha/color mode, SVG structure, small-size legibility, masking and light/dark behavior
- WCAG 2.2 contrast, typography fallback, multilingual stress cases and reduced-motion behavior
- CMYK/spot-color intent, bleed/safe areas and supplier proof status for print
- source references in code, docs, build scripts and templates; no stale old-brand filenames or rejected paths
- every deliverable has an owner, source, target, status and acceptance check
