# Worked Example: ADR-001 (from a real project)

> This is a worked example showing what an ADR looks like in practice. It's adapted from the [Austin Karaoke Directory](https://github.com/Johnesco/karaokedirectory) — the project where this protocol was first battle-tested. The original lives at [`docs/adr/001-supabase-schema-jsonb.md`](https://github.com/Johnesco/karaokedirectory/blob/main/docs/adr/001-supabase-schema-jsonb.md).
>
> Use this as a reference for tone, depth, and section structure. The copy-paste skeleton is in [`adr-template.md`](adr-template.md).

---

# ADR-001: Supabase schema — JSONB venues over normalized relational

- **Status:** Accepted
- **Date:** 2026-04-28
- **Landed in:** [`fe548ef`](https://github.com/Johnesco/karaokedirectory/commit/fe548ef) — "Refresh venue data + land Supabase JSONB scaffolding (dormant)"
- **Issue:** [#47](https://github.com/Johnesco/karaokedirectory/issues/47) (JSONB redesign), [#44](https://github.com/Johnesco/karaokedirectory/issues/44) (parent Supabase spike)
- **Supersedes:** Migration `001_initial_schema.sql` (normalized, dropped in `004_jsonb_redesign.sql`)

## Context

The project is moving to a Supabase backend in parallel with the static `js/data.js` source (production stays on JSON; Supabase engages behind a feature flag). Two schema shapes were viable.

Constraints at decision time:

- ~70 venues, single region
- Read-mostly v1 — no auth, no public writes, no moderation queue yet
- Vanilla JS client, no build step, no ORM
- The frontend always fetches the **entire** venue bundle in one shot and filters client-side
- Want minimal seed/migration friction so we can iterate

## Decision

Adopt a **JSONB-heavy 2-table model**:

```
tags     (id, label, color, text_color)
venues   (id, name, active, data JSONB)
```

The `data` column holds the full venue object — `dedicated`, `address`, `coordinates`, `host`, `socials`, `schedule[]`, `activePeriod`, `tags[]` — mirroring the existing `js/data.js` shape. Top-level columns exist only for the access patterns that need indexing/RLS: `id` (PK), `name` (sort key), `active` (RLS filter).

RLS: anon SELECT on `active = true` venues + all tags. No write policies in v1.

## Consequences

**Positive**
- `transformVenue` shrunk from ~80 lines to ~6.
- Single-table SELECT on the only real read path.
- `seed.sql` regenerates trivially from `data.js`.
- Schema additions for new fields require zero migration work.
- RLS policy surface is small — easy to reason about.

**Negative / accepted tradeoffs**
- Hudson Tavern duplication carries forward — a venue with two KJs is still two rows. Acceptable at current scale.
- No FK enforcement on hosts, companies, or tag references inside `data.tags[]`. Integrity relies on the audit script and editorial workflow.
- JSONB queries are awkward if we ever need server-side filtering by nested fields.
- No multi-region first-class support — when expansion comes, region info has to be added.

**Future revisit triggers**
- Public submissions land → moderation queue needs FK integrity → consider promoting nested fields out of JSONB.
- National expansion → add `region` column at minimum.
- Server-side filtering on a nested field at scale → promote that field to a regular column or add a GIN index.

## Options considered

### Option A — Normalized (rejected)

7-9 tables: `tags`, `hosts`, `venues`, `venue_tags`, `schedules`, `profiles`, `submissions`. UUID PKs, FK constraints, separate `schedules` for recurrence, junction table for tags. Solves duplication cleanly (one bar = one venue row, multiple shows).

### Option B — JSONB-heavy (accepted)

Two tables, `data` as JSONB. Identity-map transform on the client. Single-table fetch on read. Schema tweaks don't require migrations.

## Rationale

- **The query path is one query.** The client fetches all active venues at startup; everything else is in-memory filtering. Relational benefits buy nothing here.
- **Seed is the dominant friction.** Until auth/writes land, the cost we feel weekly is "regen the seed when `data.js` changes."
- **Schema evolution is cheap.** Adding a new social platform is a `data.js` edit + reseed — no migration.
- **Referential integrity isn't free, but it isn't earning its keep yet.** With ~70 rows and a single curator, integrity is enforced editorially.
- **Postgres has GIN indexes** if we ever need them. Not free, but available without re-architecture.

## Rejected sub-decisions

- **Per-platform social columns** (e.g. `instagram_url`): brittle; every new platform is a migration.
- **PostGIS from day one:** unused; `numeric` lat/lng inside `data.coordinates` is sufficient.
- **Separate `show_events` table for one-offs:** doubles the calendar query path.
- **UUID PKs with `slug` column:** slugs are already unique and human-meaningful; an extra UUID is overhead with no current benefit.

## Implementation notes

- **Migrations:** `001` (normalized) → `002` (RLS) → `003` (indexes) → `004_jsonb_redesign.sql` (drops 001's tables, creates this schema).
- **Dormant by default:** `js/config.js` exports `useSupabase: false`. Site continues to read `js/data.js` at runtime.
- **3-tier fallback chain** in `js/app.js`: Supabase → static `js/data.js` → empty state.

---

## What this example demonstrates

- **Status block** with date, issue links, and supersession info — gives the reader a 10-second orientation.
- **Context** is short and constraint-driven — *not* a history lesson.
- **Decision** is plain and includes a code block when it makes the choice clearer.
- **Consequences** are honest about negatives — the value of an ADR is its tradeoffs section, not its sales pitch.
- **Future revisit triggers** are explicit — they tell the next ADR author *when* this one becomes stale.
- **Options considered** is short. Two paragraphs is enough to capture an alternative.
- **Rejected sub-decisions** prevents re-litigation of related micro-choices.
- **Implementation notes** are pointers, not explanations — they help future readers *find* the decision in the codebase.
