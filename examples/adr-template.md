<!-- Full ADR skeleton. The six-line stub written BEFORE code is examples/adr-stub.md — start there, expand to this when the work lands. -->

# ADR-NNN: <short noun-phrase title>

- **Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
- **Date:** YYYY-MM-DD
- **Issue(s):** #NN (optional)
- **Supersedes:** ADR-XXX (optional)

## Context

What's the situation? What constraints exist? What forced the decision?

Keep it tight — one or two paragraphs. Cite issues, prior ADRs, or external links if they explain the constraint better than prose.

## Decision

The choice, stated plainly. One paragraph or a labeled summary block. The reader should know *what was decided* before they finish this section.

## Consequences

**Positive**
- <what becomes easier or possible>

**Negative / accepted tradeoffs**
- <what's harder, slower, or sacrificed — be honest>

**Future revisit triggers**
- <what would invalidate this decision and require a new ADR>

## Options considered (optional)

Only include if the alternatives matter for future readers. Otherwise, skip — the Decision section is enough.

### Option A — <name> (rejected)
One paragraph: what it was, why it was tempting, why it was rejected.

### Option B — <name> (accepted)
One paragraph: what it is, why it won.

## Rejected sub-decisions (optional)

For decisions inside the main decision (e.g. "we picked Postgres; we also picked uuid PKs and rejected serial ints").

- **<sub-decision>**: <one-line rationale>
- **<sub-decision>**: <one-line rationale>

## Implementation notes (optional)

Concrete pointers — file paths, migration numbers, feature flags, commit SHAs. Not for explaining the *why* (that's Context); for telling future readers *where the decision lives in the codebase*.
