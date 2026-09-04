# Bug Severity and Priority Matrix

> **Profile:** core — applies to every project. See [profiles.md](profiles.md).

> This is the one severity scale in sdlc-baseline. [incident-response.md](incident-response.md) triages in the moment with plainer words and maps back onto these four levels.

A practical framework for classifying bugs and deciding how urgently to fix them.

---

## Severity Levels

Severity describes **how bad the bug is**. It's an objective assessment of impact.

| Level | Label | Description | Examples |
|-------|-------|-------------|----------|
| **Critical** | `Critical` | System is down, data loss, or security vulnerability | App won't load, database corruption, XSS vulnerability, payments broken · Game: crashes on launch, save file corrupted, progression permanently blocked |
| **High** | `High` | Major feature is broken, no workaround | Search returns no results, login fails, form can't submit · Game: a level can't be completed, controls stop responding, a bought upgrade doesn't apply |
| **Medium** | `Medium` | Feature works but with significant issues | Filter resets on page change, slow load times, layout broken on mobile · Game: frame-rate drops on one stage, audio out of sync, score shown wrong but stored right |
| **Low** | `Low` | Cosmetic or minor inconvenience | Typo in UI, slight misalignment, tooltip shows wrong text · Game: sprite one pixel off, menu typo, wrong sound on a rare event |

---

## Priority Mapping

Priority describes **how soon to fix it**. It combines severity with business context.

| Severity | Default Priority | Rationale |
|----------|-----------------|-----------|
| **Critical** | `priority:high` | Fix immediately — drop what you're doing |
| **High** | `priority:high` | Fix before starting new features |
| **Medium** | *(no label)* | Fix in normal workflow order |
| **Low** | `priority:low` | Fix when convenient, or batch with related work |

> **Why not 4 priority levels?** For a solo dev or small team, the decision is really just "fix now" vs. "fix later" vs. "fix whenever." Two labels plus "no label = normal" covers this cleanly.

---

## Decision Guide

### When to override the default mapping

Severity and priority usually align, but not always:

| Scenario | Severity | Priority | Why |
|----------|----------|----------|-----|
| Typo on the landing page | Low | `priority:high` | First impression matters |
| Broken feature nobody uses | High | `priority:low` | No users affected |
| Security flaw in staging | Critical | *(normal)* | Not in production yet |
| Cosmetic bug right before launch | Low | `priority:high` | Timing matters |
| Exploit that makes the game more fun | Medium | `priority:low` or `resolution:by-design` | It's a feature until you decide it isn't — decide, then record it |

The PO decides priority. Severity is a fact; priority is a judgment call.

---

## Response Times

Guidelines, not SLAs. Adjust for your project's context.

| Priority | Response | Meaning |
|----------|----------|---------|
| `priority:high` | Same session | Stop current work, fix this first |
| *(normal)* | Next available slot | Pick it up when the current task is done |
| `priority:low` | When convenient | Batch with related work or tackle during downtime |

---

## Using Severity in Bug Reports

The bug issue template (`.github/ISSUE_TEMPLATE/bug.yml`) includes a Severity dropdown whose four option strings are `<Level> — <Description>` copied **verbatim** from the table above. Change one, change both in the same commit; downstream projects receive the template via `scripts/sync-github-templates.sh`. When filing a bug:

1. **Select the severity** based on the descriptions above
2. **The dev or PO adds a priority label** if it differs from the default mapping
3. **No priority label** means normal priority (fix in backlog order)

---

## Triage Checklist

When a new bug comes in:

1. **Is it really a bug?** Or is it working as designed? Check the spec.
2. **What's the severity?** Use the table above. Be honest — not everything is Critical.
3. **Does priority match severity?** If not, add a priority label and note why.
4. **Is there a workaround?** Document it in the issue for users in the meantime.
5. **Does it block other work?** If yes, set it as a blocker on the board.
