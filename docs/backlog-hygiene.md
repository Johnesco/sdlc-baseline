# Backlog Hygiene

How to keep your issue backlog useful instead of letting it become a graveyard of good intentions. This covers review cadence, grooming tactics, and planning habits for a sole developer.

---

## The Problem

Solo devs accumulate issues faster than they close them. After a few months, the backlog looks like:

- 40 open issues, 15 of which are stale
- Duplicates nobody noticed
- Features that sounded good at 2 AM but no longer matter
- Bugs that were quietly fixed by other work
- No clear sense of "what should I work on next"

A backlog in this state is worse than no backlog — it's a source of guilt and noise, not signal.

---

## Review Cadence

### Weekly: pick your next work (5 minutes)

At the start of each working session (or week, or sprint — whatever your rhythm is):

1. **Check the Ready column.** Is there something refined and ready to build? Start there.
2. **Check priority:high issues.** Anything urgent that jumped the queue?
3. **Pick 1-3 issues** to focus on. Don't plan more than you can finish before the next review.

This is wearing the **PO hat** — deciding what gets built and in what order.

### Monthly: groom the backlog (15-30 minutes)

Once a month, scan the full backlog:

- [ ] **Close stale issues.** If an issue has been open for 2+ months with no activity and no urgency, close it with `resolution:stale`. You can always reopen it.
- [ ] **Merge duplicates.** Search for issues that describe the same problem. Close the duplicate with `resolution:duplicate` and link to the surviving issue.
- [ ] **Re-evaluate priorities.** Has anything become more or less urgent since it was filed? Add or remove `priority:high` / `priority:low`.
- [ ] **Check milestones.** Are issues assigned to the right milestones? Are any milestones stale?
- [ ] **Refine the top of the backlog.** Pick 2-3 issues in Backlog that are close to Ready and flesh out their acceptance criteria.

### Quarterly: step back (30 minutes)

Every few months, zoom out:

- **Are you building the right things?** Look at the last quarter's Done column. Does the work reflect your actual priorities?
- **Is the process working?** Are tickets getting stuck in certain columns? Is the workflow too heavy for some issue types?
- **Are milestones realistic?** Adjust scope or timelines based on actual velocity.
- **Is there tech debt piling up?** If you keep deferring `task` issues, that's a signal.

This is a lightweight retrospective. For a sole dev, it doesn't need a template — just honest reflection.

---

## Grooming Tactics

### The two-month rule

If an issue has been open for two months with no activity, it's probably not important. Close it with `resolution:stale` and a comment:

```
Closing as stale — no activity in 2+ months and not blocking anything.
Reopen if this becomes relevant again.
```

This isn't giving up. It's acknowledging reality. A closed issue is still searchable. If it matters, it'll come back.

### The "would I file this today?" test

When reviewing old issues, ask: "If this didn't exist, would I create it right now?" If the answer is no, close it. The backlog should reflect what you'd choose to work on today, not what seemed like a good idea months ago.

### Batch related issues

If you have 5 small issues that all touch the same area, consider:
- Can they be combined into one larger issue?
- Should they be grouped under a milestone?
- Would it be faster to do them all in one session?

Batching reduces context-switching and makes the backlog shorter.

### Use labels to scan faster

```bash
# All open issues with no milestone — potential orphans
gh issue list --no-milestone

# All open issues older than 60 days
gh issue list --search "created:<2026-04-04"

# All issues in Backlog that have acceptance criteria (ready to promote)
gh issue list --label "feature" --search "acceptance criteria"

# High-priority issues — should be empty or actively being worked
gh issue list --label "priority:high"
```

---

## Backlog Size

### How many open issues is healthy?

| Backlog size | Signal |
|-------------|--------|
| 0-10 | Tight and focused. Might be underusing the backlog as a capture tool. |
| 10-25 | Healthy for a sole dev. Enough to choose from, not overwhelming. |
| 25-50 | Getting heavy. Monthly grooming is essential. |
| 50+ | Backlog is a dumping ground. Block 30 minutes for an aggressive grooming session. |

There's no magic number. The test is: can you scan the backlog in under 2 minutes and know what to work on next? If not, it's too big.

### When the backlog is too big

If you're over 50 open issues:

1. **Sort by creation date.** Start from the oldest.
2. **Apply the "would I file this today?" test.** Close aggressively.
3. **Look for themes.** If 10 issues are all about search, that's a milestone, not 10 separate priorities.
4. **Set a target.** "I'll get this under 25 by end of week." Closing issues counts as productive work.

---

## Planning Without Sprints

Formal sprints (2-week timeboxes with commitment) are designed for teams. Solo devs don't need the ceremony, but they do need the discipline of choosing what to work on and sticking with it.

### A simple planning rhythm

1. **Pick a milestone** (or a theme, or just "the next 3 issues")
2. **Work through them** in priority order
3. **Don't add to the current batch** unless it's `priority:high`
4. **When the batch is done**, pick the next one

This gives you focus without the overhead of sprint planning, standups, and velocity tracking.

### Saying no

The hardest part of backlog management is saying no. Every issue in the backlog is a commitment to evaluate it later. Too many commitments and you stop evaluating any of them.

Ways to say no:
- **Close with `resolution:wontfix`** — "This isn't worth doing." That's a valid decision.
- **Close with `resolution:stale`** — "This might be worth doing, but not enough to prioritize."
- **Don't file the issue in the first place** — not every idea needs to be captured. If it's important, it'll come back.

---

## How This Fits the Workflow

Backlog hygiene is the maintenance layer around the [7-step workflow](workflow.md):

| Workflow concept | Hygiene connection |
|-----------------|-------------------|
| **Step 1 (Capture)** | Filing issues is easy. Hygiene ensures the backlog stays manageable after. |
| **Backlog column** | The grooming target. Issues should flow through, not accumulate. |
| **Ready column** | Monthly grooming promotes refined issues to Ready. |
| **Milestones** | Quarterly review checks milestone scope and progress. |
| **PO role** | Backlog grooming is PO work — deciding what matters and what doesn't. |

---

## Recommended First Steps

1. **Schedule a monthly reminder** — "Groom the backlog." 15 minutes on your calendar.
2. **Run the stale-issue scan now** — `gh issue list --search "created:<2026-04-04"` — and close what's no longer relevant.
3. **Count your open issues.** If it's over 25, block 30 minutes this week to get it under control.
