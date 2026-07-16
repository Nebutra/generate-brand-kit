# AI SaaS Acceptance Profiles

Use these profiles to turn C1-C14 scope rows into testable product work. Adapt
thresholds to the product; never mark a UI artifact complete from a static board
alone.

## Common Evidence

For each selected flow, retain the editable source, implemented or interactive
prototype, state matrix, representative data fixtures, keyboard/screen-reader
notes, light/dark/high-contrast captures, owner, and acceptance record.

Test at least: empty, normal, dense, long/localized, loading/streaming, partial,
error, offline/tool unavailable, permission denied, canceled, and recovered.

## C1 Product System

- Prove token source-to-code parity and document generated versus hand-owned files.
- Exercise component variants, focus, hover, active, disabled, invalid, loading,
  high contrast, zoom/reflow, reduced motion, and localization.
- Validate charts with redundant labels/patterns and nonvisual alternatives.
- Keep marketing display typography separate from operational UI typography.

## C2-C3 AI Identity and Runtime

- Distinguish AI-assisted suggestion, generated content, and autonomous action by
  language and interaction, not sparkle decoration or color alone.
- Test understand/plan/generate/tool/wait/approval/cancel/retry/partial/fail/
  timeout/recover paths as transitions, not isolated screenshots.
- Do not display fake percentage progress or hidden-reasoning theater.

## C4-C6 Conversation, Evidence, Safety

- Test prompt composition, attachments, code, tables, citations, editing,
  branching, regeneration, context boundaries, and export/copy retention.
- Preserve source, freshness, uncertainty, limitation, and conflict states through
  sharing and regeneration.
- Give refusal and safety states a clear reason class, permitted next action, and
  human/support route where appropriate; do not dead-end recoverable failures.

## C7 Privacy and Consent

- Verify tenant/workspace boundaries, retention, training use, third-party data
  flow, consent, withdrawal, deletion, and export language against owned policy.
- Test sensitive-data warnings before irreversible transmission and avoid making
  unsupported privacy promises.

## C8-C9 Developer and Lifecycle

- Reveal API secrets once, redact afterward, and test copy, revoke, rotate,
  expired, permission, rate-limit, and audit-log behavior.
- Test onboarding, invite, SSO, role changes, billing, quota, upgrade, cancel,
  notification, support, maintenance, and incident journeys end to end.

## C10-C11 Trust and Provenance

- Require an evidence owner, source, review date, and claim state for every
  security, privacy, compliance, SLA, certification, Responsible AI, and model
  claim.
- Test provenance present, missing, invalid, stripped, edited, conflicting, and
  unsupported-export states. Preserve provenance through supported transforms.

## C12 Accessibility

- Run automated checks plus keyboard-only and screen-reader workflows; automation
  alone is insufficient.
- Verify streaming announcements, focus stability, pause/control of updates,
  non-color status, reduced motion, zoom/reflow, code/table semantics, and
  localized cognitive clarity.

## C13-C14 Ecosystem, Motion, and Sound

- Distinguish first-party, third-party, verified, community, and customer-created
  agents/connectors. Test install, permission, update, revoke, suspend, and
  removal states.
- Define truthful motion semantics, static fallbacks, interruption behavior,
  duration/easing tokens, and reduced-motion paths.
- For sound, record authorship, rights, format, loudness target, mute behavior,
  urgency semantics, and a visual equivalent.
