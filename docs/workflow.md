# The 7-Step Ticket-First Workflow

> **Profile:** core — applies to every project. See [profiles.md](profiles.md).

Every software change — feature, bug fix, refactor, documentation update, or data change — follows this sequence. No step may be skipped.

---

## The Steps

> *Board status* lines describe the column the ticket sits in **if you use a board**. Without one they are simply the ticket's state.

### Step 1: Capture as a Ticket

**What:** Create the ticket before any other work begins. The ticket is a GitHub Issue — always for bugs, and the default for everything else — or, for a decision, a six-line ADR stub (see [adrs.md](adrs.md#the-six-line-stub--decide-before-you-build)). Both count as "the ticket".

**Who:** PO (decides what to build) or BA (drafts the ticket)

**Requirements:**
- Clear, descriptive title
- Relevant labels (type + area + priority)
- Acceptance criteria (even if rough)
- Milestone assignment (if you use milestones)

**Example:**
```bash
gh issue create \
  --title "Add user avatar upload" \
  --label "feature,area:frontend" \
  --milestone "User Profiles" \
  --body "Users should be able to upload a profile avatar..."
```

> **If you use a board: add the ticket to it**
>
> `gh issue create` does **NOT** automatically add issues to your GitHub Projects board. You must run this immediately after creating the issue:
> ```bash
> gh project item-add [PROJECT_NUMBER] --owner [OWNER] --url [ISSUE_URL]
> ```
> An issue that is not on the board is invisible to the board. No board? `gh issue list --state open` is your board — skip this step.

**Board status:** Backlog (set automatically when added to board)

---

### Step 2: Review Documentation

**What:** Read the documentation that describes the area being changed.

**Who:** BA or Dev

**Read these:**
- Project spec (e.g., `docs/functional-spec.md`) — sections related to the change
- `CLAUDE.md` — file structure, patterns, conventions
- `README.md` — if the change affects public-facing descriptions
- `docs/adr/` — prior architectural decisions affecting this area (start with `docs/adr/README.md` for the index)

**Goal:** Understand what exists today, what will be impacted, and whether the docs match reality.

**Board status:** Still Backlog (refinement in progress)

---

### Step 3: Flag Discrepancies

**What:** If documentation and code disagree, stop and call it out.

**Who:** BA or Dev

**Rules:**
- Do **not** silently fix documentation to match code
- Do **not** silently fix code to match documentation
- Flag the mismatch in the issue comments for the human to decide
- The human (PO) decides which is correct: the code or the docs

**Example comment:**
```
The spec says the search bar filters by venue name only,
but the code also searches by neighborhood and host name.
Which is correct? Should I update the spec or the code?
```

**Board status:** Still Backlog (refinement in progress)

---

### Step 4: Refine the Ticket

**What:** Update the issue with full context from the documentation review.

**Who:** BA

**Add to the issue:**
- Which doc sections will need updating
- Which files will be touched
- Any open questions or decisions needed
- The decision, as a six-line ADR stub, if the change is above a tuning tweak (see the gate below)
- Revised acceptance criteria (now more specific)

**Example update:**
```
## Documentation Impact
- `docs/functional-spec.md` Section 7 (Venue Detail) — add avatar field
- `CLAUDE.md` Data Formats — add avatar to venue schema
- `README.md` — no change needed

## Files Affected
- `js/data.js` — schema change
- `js/components/VenueCard.js` — render avatar
- `css/components.css` — avatar styles
```

**Board status:** Ready (move manually when acceptance criteria are final)

> **Gate — decide before you build.** If the change is above a tuning tweak — it touches more than one file, or it changes behaviour — a six-line ADR stub (Context + Decision) exists before Step 5 begins. Either it *is* the ticket (Step 1) or it was written here. If you can't write the Decision paragraph, the ticket isn't ready: it stays in Backlog. See [adrs.md](adrs.md#the-six-line-stub--decide-before-you-build).

---

### Step 5: Implement the Change

**What:** Write the code. This is the only step where code is written.

**Who:** Dev (AI or human)

**Rules:**
- Reference the ticket in every commit: `#XX: description` (or `ADR-NNN: description` when the ticket is an ADR stub)
- Follow existing code patterns and conventions
- Read files before editing them
- Keep changes focused on the ticket scope

**Example commit:**
```
#42: Add avatar upload component
```

**Board status:** In Progress (move manually when coding begins)

---

### Step 6: Update All Documentation

**What:** Update every document that is affected by the change.

**Who:** Documenter (typically the same Dev who wrote the code)

**Must update:**
- Project spec — if any feature, behavior, or data format changed
- CLAUDE.md — if file structure, patterns, or architecture changed
- README.md — if public-facing features or setup instructions changed
- **`docs/adr/`** — if this change makes an architectural choice that's expensive to reverse, where reasonable contributors would consider alternatives, or that future contributors will second-guess. Complete the ADR: add Consequences to the stub, set Status to Accepted, and update `docs/adr/README.md`. Full format in [`examples/adr-template.md`](../examples/adr-template.md). See [`docs/adrs.md`](adrs.md) for the threshold rule.

**Key rule:** A change without a documentation update is **incomplete**. Documentation updates are part of the definition of done, not a follow-up task.

**Board status:** Still In Progress

---

### Step 7: Verify Consistency

**What:** Confirm that documentation and code agree. Call out any remaining gaps.

**Who:** QA (always human)

**Checklist:**
- [ ] Code matches the acceptance criteria in the ticket
- [ ] Spec accurately describes the new behavior
- [ ] CLAUDE.md reflects any structural changes
- [ ] No undocumented side effects

**Board status:** Verify (move manually when code + docs are complete)

After the human verifies, the issue is closed (and the board card moves to **Done** automatically, if you use one).

---

## Compressing Steps for Small Changes

Not every change needs the full ceremony. Here's when you can compress:

### Data-only changes (adding a record, fixing a typo)
- Steps 2-4 can compress into a quick scan
- Step 6 may be skipping the spec update if the data format didn't change
- Still need a ticket (Step 1) and human verification (Step 7)

### Bug fixes with obvious cause
- Step 2 becomes "confirm the spec describes the expected behavior"
- Steps 3-4 can compress into a single issue comment
- Step 6 only needed if the fix changes documented behavior

### Documentation-only changes
- Step 5 becomes "edit the docs" instead of "write code"
- Step 6 is the main deliverable
- Step 7 is still human review

### When NOT to compress
- New features (always full workflow)
- Changes that affect multiple files or systems
- Changes where you're unsure about the existing behavior
- Anything that modifies user-facing behavior

---

## Role Responsibilities by Step

| Step | PO | BA | Dev | Documenter | QA |
|------|----|----|-----|------------|-----|
| 1. Capture | Decides priority | Drafts ticket | — | — | — |
| 2. Review docs | — | Reads spec | Reads code | — | — |
| 3. Flag gaps | Decides resolution | Identifies gaps | Identifies gaps | — | — |
| 4. Refine | Approves scope | Updates ticket | Estimates effort | Plans doc updates | — |
| 5. Implement | — | — | Writes code | — | — |
| 6. Document | — | — | — | Updates all docs | — |
| 7. Verify | Accepts delivery | — | — | — | Tests + reviews |

---

## How Steps Map to Board Columns

*If you use a board.* Without one, the columns are the states a ticket passes through.

| Board Column | Workflow Steps | What Happens |
|-------------|---------------|--------------|
| **Backlog** | Steps 1-3 | Ticket created, docs reviewed, discrepancies flagged |
| **Ready** | Step 4 complete | AC finalized, scope agreed — pick queue for devs |
| **In Progress** | Steps 5-6 | Code written, docs updated |
| **Verify** | Step 7 | Human tests and reviews |
| **Done** | — | Accepted, issue closed |

---

## Key Rules (Summary)

1. **No code without a ticket** — an Issue (always, for bugs) or an ADR stub (for decisions)
2. **If you use a board, no ticket without a board entry** — `gh project item-add` after every `gh issue create`
3. **Decide before you build** — above a tuning tweak, a six-line ADR stub exists before code
4. **Read before writing** — understand the existing state before changing it
5. **Flag, don't fix** — discrepancies between code and docs need human decisions
6. **Docs are not optional** — incomplete documentation = incomplete work
7. **Verify is human-only** — the person (or AI) who wrote it cannot verify it
8. **Compress, don't skip** — small changes can move faster, but every step still happens
