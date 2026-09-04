# Definition of Done

> **Profile:** core — applies to every project. See [profiles.md](profiles.md).

> No board? "Card moved to Verify" means: comment **Ready to verify** on the ticket and hand it to the human. The column is optional; the hand-off isn't.

A change is not complete until every applicable item on its checklist is satisfied. These checklists are the exit criteria for moving an issue from **In Progress** to **Verify**.

---

## By Issue Type

### Feature

A new feature or enhancement to existing functionality.

- [ ] **Code complete** — Feature works as described in acceptance criteria
- [ ] **Follows existing patterns** — Code matches project conventions and style
- [ ] **No regressions — verified, not assumed** — Name what you ran (`npm test`, a smoke script, a manual pass through X) and what you observed; record it on the ticket. "Should be fine" is not verification.
- [ ] **Spec updated** — Project specification reflects the new behavior
- [ ] **CLAUDE.md updated** — File structure, patterns, or architecture changes documented
- [ ] **README.md updated** — If the feature is user-facing or changes setup
- [ ] **ADR written if applicable** — A decision above a tuning tweak had its stub before code; if this change makes an architectural decision per the [threshold rule](adrs.md#threshold-rule--when-to-write-one), a completed ADR exists in `docs/adr/`. (Or: explicitly noted on the ticket that no ADR is needed and why.)
- [ ] **Commit references ticket** — All commits include `#XX` (or `ADR-NNN`)
- [ ] **Ready for human verification** — Card moved to Verify column

### Bug Fix

Something was broken and now it's fixed.

- [ ] **Bug fixed** — The reported behavior no longer occurs
- [ ] **Root cause understood** — You know why it happened, not just how to suppress it
- [ ] **No regressions — verified, not assumed** — The fix doesn't break anything else, and you can say what you ran to know that.
- [ ] **Spec updated** — If the fix changes documented behavior
- [ ] **Commit references ticket** — All commits include `#XX` (or `ADR-NNN`)
- [ ] **Ready for human verification** — Card moved to Verify column

### Documentation

A change to documentation files only (no code changes).

- [ ] **Content accurate** — Documentation matches current code behavior
- [ ] **Consistent across docs** — Spec, CLAUDE.md, and README.md agree with each other
- [ ] **No broken links** — All references and cross-links work
- [ ] **Formatting correct** — Markdown renders properly
- [ ] **Commit references ticket** — All commits include `#XX` (or `ADR-NNN`)
- [ ] **Ready for human review** — Card moved to Verify column

### Task

Refactors, dependency updates, tooling, or infrastructure changes.

- [ ] **Change implemented** — The refactor, update, or config change is in place
- [ ] **No regressions — verified, not assumed** — Name the command or check that proves it.
- [ ] **No behavior changes** — Unless explicitly intended (in which case, treat as a feature)
- [ ] **Documentation updated** — If the change affects project structure or setup
- [ ] **ADR written if applicable** — If this refactor implements an architectural decision per the [threshold rule](adrs.md#threshold-rule--when-to-write-one), a new ADR exists in `docs/adr/`.
- [ ] **Commit references ticket** — All commits include `#XX` (or `ADR-NNN`)
- [ ] **Ready for human verification** — Card moved to Verify column

### Spike

Research, investigation, or proof-of-concept to answer a question.

- [ ] **Question answered** — Or explicitly marked unanswerable with current information
- [ ] **Findings documented** — In issue comments or a linked document
- [ ] **Recommendation provided** — With tradeoffs clearly stated
- [ ] **Follow-up tickets created** — If the spike produced actionable next steps
- [ ] **Ready for human review** — Card moved to Verify column

---

## Universal Rules

These apply to every issue type:

1. **Documentation is not optional.** If a change affects behavior, the spec must be updated in the same change. A change without updated documentation is incomplete.

2. **Human verification is required.** The person or AI that wrote the code cannot mark it as Done. The Verify column exists for the human to confirm the work.

3. **Ticket references are required.** Every commit must include the issue number (`#XX: description`). This creates traceability from code back to the decision that authorized it.

4. **"It works on my machine" is not done.** Verify across the target environments (mobile/desktop, different browsers, etc.) as applicable.

5. **The gate must pass.** Core: the project's local test command ([testing.md — The local gate](testing.md#the-local-gate-core)) is green before a release tag, and before Verify whenever the change touches something the suite covers. Core+ops: CI is green before Verify ([ci-cd.md](ci-cd.md)). A failing gate means the issue is not ready for human verification — fix it first, don't waste QA time.

---

## How to Use These Checklists

### In issue templates
The issue templates (`.github/ISSUE_TEMPLATE/`) include a "Definition of Done" field pre-populated with the relevant checklist. Customize it per-issue as needed.

### If you use pull requests
The PR template (`.github/PULL_REQUEST_TEMPLATE.md`) includes documentation and testing checklists. Review these before requesting verification.

### As a reviewer
When you're wearing the QA hat and verifying work in the Verify column, walk through the applicable checklist. If any item isn't satisfied, send it back to In Progress with a comment explaining what's missing.
