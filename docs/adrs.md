# Architecture Decision Records (ADRs)

> **Profile:** core — applies to every project. See [profiles.md](profiles.md).

A short, immutable doc that captures *why* you made an architectural choice — written at the moment of the decision, not in hindsight. The format was popularized by [Michael Nygard in 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

Code shows *what*; commit messages show *what changed*; ADRs show *why*. Without them, every architectural question becomes an archaeology dig through Slack and PRs.

---

## Threshold rule — when to write one

Write an ADR when **any two** of the following are true:

- The decision is expensive or risky to reverse
- Reasonable contributors would consider alternatives
- Future contributors will second-guess it without context

**Don't ADR:** naming conventions, formatter choice, library picks under 30 minutes of switching cost, anything reversible in a single change.

If you're unsure, err on the side of writing one — they're cheap. A 60-second ADR that exists beats a perfect ADR you didn't write.

---

## The six-line stub — decide before you build

Anything above a tuning tweak — it touches more than one file, or it changes behaviour — gets an ADR stub **before code**: a title, status and date, a Context paragraph, a Decision paragraph. Six lines ([`examples/adr-stub.md`](../examples/adr-stub.md)):

```markdown
# ADR-012: Practice run replaces ghost race
**Status:** Proposed · **Date:** 2026-06-25 · **Issue(s):** #88
## Context
The ghost replays the road faithfully but not the traffic, so racing it isn't fair — and players notice.
## Decision
Shelve the hologram behind a flag and ship a solo timed run on the same scaffolding.
```

**If you can't write the Decision paragraph, it isn't ready.** That is the test — not the file. The stub is the cheapest way to discover you are about to build something you haven't decided.

- The stub is `Proposed`. When the work lands (Step 6), add **Consequences**, set **Accepted**, and add it to the index. The one-line header is equivalent to the template's bullet list — keep whichever you have.
- Not every stub meets the [threshold rule](#threshold-rule--when-to-write-one). Those can stay as stubs or be folded into the ticket; the value was in writing it.
- In **core** projects the stub is a valid ticket: Step 1 of the [workflow](workflow.md) accepts an Issue (always, for bugs) or an ADR stub (for decisions). Commits reference it as `ADR-012: description`.
- Tuning tweaks — a constant, a colour, copy — need no stub. Bug fixes need no stub unless the fix implies a rule (see "What doesn't need an ADR").

---

## Format

Roughly the [Nygard template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). One page max — if it's longer, it's probably two ADRs.

```markdown
# ADR-NNN: <short noun-phrase title>

- **Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
- **Date:** YYYY-MM-DD
- **Issue(s):** #NN (optional)
- **Supersedes:** ADR-XXX (optional)

## Context
What's the situation? What constraints exist? What forced the decision?

## Decision
The choice, stated plainly.

## Consequences
What becomes easier. What becomes harder. What you've accepted.
```

A copy-paste skeleton lives at [`examples/adr-template.md`](../examples/adr-template.md). A worked example lives at [`examples/adr-example.md`](../examples/adr-example.md). The six-line stub lives at [`examples/adr-stub.md`](../examples/adr-stub.md).

---

## Rules

1. **Numbered sequentially** with leading zeros: `001`, `002`, `003`. Never renumbered, even after deprecation.
2. **Immutable once Accepted.** Don't edit them to reflect new information. The only allowed substantive edit is updating Status to `Superseded by ADR-NNN` when a later ADR replaces it.
3. **Written at decision time**, not after. Backfilling is fine but lower-fidelity — you'll forget the dead-ends.
4. **One decision per ADR.** Don't bundle.
5. **Stored in the repo** at `docs/adr/` — they version with the code.
6. **Tiny by design.** No diagrams unless essential. No exhaustive analysis. The point is *capture*, not persuasion.

You never delete an ADR. The history is the value.

---

## Statuses

| Status | Meaning |
|---|---|
| **Proposed** | Drafted, not yet agreed |
| **Accepted** | Current truth |
| **Deprecated** | No longer relevant, but not replaced (e.g. the constraint went away) |
| **Superseded by ADR-XXX** | Replaced; old ADR stays in repo, points forward |

---

## Where ADRs live

- **Protocol, template, examples** — in this repo (`sdlc-baseline`).
- **Actual ADRs** — in each downstream project's `docs/adr/` directory. sdlc-baseline doesn't make architectural decisions; it provides the format.

### Standard layout in a downstream project

```
project/
├── docs/
│   ├── adr/
│   │   ├── README.md                    # Index — table: # | Title | Status
│   │   ├── 001-<short-slug>.md
│   │   ├── 002-<short-slug>.md
│   │   └── …
│   ├── functional-spec.md
│   └── …
```

### Index format (`docs/adr/README.md`)

```markdown
# Architecture Decision Records

Format: see [sdlc-baseline `docs/adrs.md`](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md).

## Index

| # | Title | Status |
|---|---|---|
| [001](001-supabase-schema-jsonb.md) | Supabase schema — JSONB venues over normalized | Accepted |
| [002](002-...) | … | Accepted |
```

---

## Workflow integration

ADRs are woven into the 7-step ticket-first workflow:

- **Step 1 (Capture)** — in core, an ADR stub can *be* the ticket for a decision.
- **Step 2 (Review Documentation)** — check `docs/adr/` for prior decisions on the affected area before scoping work.
- **Step 4 → 5 (the gate)** — the stub exists before any code is written.
- **Step 6 (Update Documentation)** — complete the ADR (Consequences, Status → Accepted) in the same change.
- **Definition of Done** — for architecture-touching changes, an ADR (or an explicit "no ADR needed" justification) is part of the checklist.

See [`docs/workflow.md`](workflow.md) and [`docs/definition-of-done.md`](definition-of-done.md).

---

## What doesn't need an ADR

To keep the directory signal-rich, avoid ADRs for:

- **Naming conventions** — put these in `CLAUDE.md` or a style guide.
- **Code formatting / linting** — use a formatter; record the choice in `package.json` or equivalent.
- **Trivial library swaps** — date-fns vs dayjs is a 30-minute switch.
- **Project-specific configuration** — environment variables, feature flags, etc.
- **Bug-fix decisions** — if the fix is obvious, no ADR; if it implies a deeper architectural rule, write the ADR for the rule, not the fix.

If a decision is later second-guessed and you find yourself re-explaining it more than once, that's a signal it should have been an ADR. Write one then.

---

## Why this works

- **Onboarding:** new contributors read `docs/adr/` and get the architectural narrative in 10 minutes.
- **Debate prevention:** "should we normalize the schema?" → "see ADR-001" → 60-second resolution.
- **Self-protection:** future-you doesn't have to argue with past-you about decisions past-you doesn't remember making.
- **Drift detection:** when reality stops matching the ADR, you've identified architectural drift before it becomes a rewrite.

---

## Practical tips

- Keep `docs/adr/README.md` as a curated index. A directory listing isn't enough — humans want a table with statuses.
- Number with leading zeros (`001`, not `1`) so they sort correctly in file managers and indexes.
- Link generously — ADRs reference issues, commits, other ADRs.
- When superseding, update the old ADR's Status line **only** to point forward. Then update the index. That's the only allowed edit.
- For solo projects, no need to formally agree on Proposed → Accepted; a single-author commit is sufficient. Multi-contributor projects can use PR review as the agreement step.
- Copy-paste from `examples/adr-template.md` — don't try to remember the structure.
