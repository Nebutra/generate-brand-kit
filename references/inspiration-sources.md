# Inspiration Sources and Ecosystem Map

Reference galleries, communities, and repos — mapped to the pipeline stage
where each is actually useful. Do not treat them as interchangeable
"inspiration"; each answers a different question. URLs verified 2026-07.

## Contents

Pipeline-stage sources; GitHub ecosystem; brand-as-code standards; AI-era
practice.

## By pipeline stage

### Moodboard / foundation-board stage
- **Cosmos** — https://www.cosmos.so/ — AI-tagged, palette/similar-image
  search; current designer favorite for visual research.
- **Are.na** — https://www.are.na/ — algorithm-free channels mixing images,
  links, text; best when the board must carry strategy linkage.
- **Savee** — https://savee.it/ — strongest pure-visual browsing grid.

### Mark-reference stage (sketching / crowding check)
- **LogoLounge** — https://www.logolounge.com/ — 450k+ searchable logos +
  annual trend reports; check how crowded a concept already is.
- **LogoArchive** — https://www.logo-archive.org/ — 5,000+ mid-century
  modernist marks; the timeless-geometry counterweight.
- **Logobook** — https://logobook.com/ — classic logos searchable by shape,
  object, designer, style; fast formal-language reference.
- **Logosystem** — https://logosystem.co/ — 1,200+ curated contemporary and
  animated logos, filterable by color/style/shape.

### Critique / concept-validation stage
- **Brand New** — https://www.underconsideration.com/brandnew/ — daily
  reviewed identity launches; before/after rebrand study.
- **BP&O** — https://bpando.org/ — strategic analysis behind systems.
- **Identity Designed** — https://identitydesigned.com/ — full-system case
  studies with editorial depth.
- **The Brand Identity** — https://thebrandidentity.com/ — studio process
  interviews.
- **Rebrand Gallery** — https://rebrandgallery.com/ — before/after rebrands;
  useful when the brief is a migration.

### Guideline-structure stage (what the deliverable should contain)
- **Branding Style Guides** — https://brandingstyleguides.com/ — archive of
  real brand-manual PDFs; the reference for sections, rules, misuse pages.
- **Frontify guideline examples** — https://www.frontify.com/en/guide/brand-guidelines-examples
- **Behance brand-guidelines search** — https://www.behance.net/search/projects/brand%20guidelines

### Type-selection validation
- **Fonts In Use** — https://fontsinuse.com/ — ~34k entries, 8,956 in
  Branding/Identity, indexed by typeface and industry; answers "how does
  this typeface behave in a real identity in this sector."

### In-context proof stage
- **Mobbin** — https://mobbin.com/ — 400k+ real app/web screenshots; verify
  how identities survive onboarding, nav, empty states.
- **Brandfetch** — https://brandfetch.com/ — auto brand pages (logo SVGs,
  colors, fonts) for competitor landscape audits;
  **WorldVectorLogo** — https://worldvectorlogo.com — free SVG downloads.

## GitHub ecosystem (agent-consumable conventions)

The key 2025–26 shift: from "links for humans" to **files for agents**.

- **VoltAgent/awesome-design-md** — 73 real-brand DESIGN.md token files
  (Stripe, Nike, Claude…) with a nine-section schema: Visual Theme, Color
  Palette & Roles, Typography Rules, Component Stylings, Layout Principles,
  Depth & Elevation, **Design Guardrails**, Responsive Behavior, **Agent
  Prompt Guide**. Emit a DESIGN.md following this schema when the target
  repo hosts a UI. https://github.com/VoltAgent/awesome-design-md
- **anthropics/skills brand-guidelines** — canonical minimal branding
  skill: exact hex tokens, font fallback chains, deterministic application
  rules in one file. https://github.com/anthropics/skills/tree/main/skills/brand-guidelines
- **mcpware/logoloom** — closest OSS analog to this skill: one command →
  31-file kit (full/icon/wordmark × light/dark/mono, favicon, OG image,
  BRAND.md); toolchain opentype.js + SVGO + sharp + vtracer. Borrow the
  variant matrix. https://github.com/mcpware/logoloom
- **glincker/thesvg** — 6,400+ brand SVGs with color/mono/light/dark/
  wordmark variant naming; model for asset distribution.
  https://github.com/glincker/thesvg
- **badges/shields** — badge standard; SVG-first, PNG fallback for
  Slack/email; `?style=for-the-badge` for boxy style.
  https://github.com/badges/shields
- **GitHub Brand Toolkit** — https://brand.github.com/ — how a platform
  ships brand assets and usage rules.
- **Open-source brand-repo patterns:** Mozilla splits marketing brand
  (mozilla/protocol + protocol-assets) from product design system
  (FirefoxUX/acorn-icons); GitLab governs brand guidelines as handbook
  markdown changed via merge request; Uber ships base.uber.com +
  uber/baseweb; IBM Carbon is fully open.
- **Discovery surfaces:** https://github.com/topics/brand-kit,
  /topics/logo-generator, /topics/brand-assets;
  awesome lists: VoltAgent/awesome-agent-skills,
  ComposioHQ/awesome-claude-skills, gztchan/awesome-design.

## Brand-as-code standards

- **DTCG Design Tokens spec v2025.10** (first stable, 2025-10-28):
  multi-file, theming/multi-brand, Oklch/Display-P3 color, aliases.
  https://www.designtokens.org/tr/2025.10/format/
- **Style Dictionary 4** — canonical transformer; DTCG and legacy formats
  cannot be mixed in one instance. https://styledictionary.com/info/dtcg/
- **Icon slot canon** (Evil Martians, holds through 2026): favicon.ico
  32×32, icon.svg (dark-mode media query), apple-touch-icon.png 180×180
  opaque, icon-192.png, icon-mask.png 512×512 with 409px-circle safe zone
  (validate at maskable.app), icon-512.png. OG images 1200×630.
  https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs
- **Asset naming grammar:** `CLIENT_PROJECT_YYYY-MM_vNN.ext`; no spaces;
  ban "final/latest" suffixes; one approved master, derivatives generated.

## AI-era practice (what separates good from slop)

- **AI output is a brief, not a final.** Studios use image models for
  exploration/moodboarding; humans rebuild marks as vectors. Documented
  human transformation is also a legal necessity: purely AI-generated
  content is uncopyrightable (US Copyright Office 2025), though a
  distinctive AI-assisted mark can be trademarked — document the design
  evolution. https://news.bloomberglaw.com/us-law-week/ai-generated-logos-require-careful-steps-to-protect-ip-rights
- **Slop tells to ban in prompts and reject in review:** purple-blue
  gradients, floating gradient orbs, glassmorphism, sparkle icons,
  fake 3D depth, Inter/Poppins-default typography, three-feature-card
  layout thinking. Catalog: https://vibecodekit.dev/ai-slop-design
- **Anti-slop rules that work:** lock decisions in a written VI before
  generating; ≤3 hues (60/30/10); intentional type pairing; texture and
  human imperfection as differentiators (the one thing averaging-based
  generation cannot produce).
- **True-vector generation** exists only in Recraft (V4 Vector, native
  SVG, needs anchor-point cleanup) and Adobe Firefly/Illustrator
  text-to-vector; **Ideogram** is strongest for lettering/logotypes
  (~2× lower text error rates). Everything else is raster → hand
  vectorization stays in the pipeline.
