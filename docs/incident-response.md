# Incident Response

What to do when something breaks in production. This is the sole-developer version — no war rooms, no on-call rotations, just a clear sequence for restoring service and preventing recurrence.

---

## The Sequence

When production is broken, follow this order:

```
Detect → Assess → Restore → Communicate → Investigate → Prevent
```

**The most important rule:** Restore first, investigate second. Your users don't care *why* it's broken — they care that it works.

---

## Step 1: Detect

Something tipped you off. Common detection sources for a sole dev:

| Source | Example |
|--------|---------|
| **You noticed** | Smoke test after deploy failed, or you were using the app |
| **A user reported it** | Email, DM, support form, social media |
| **Error tracking** | Sentry, LogRocket, or platform error logs spiking |
| **Uptime monitor** | Pingdom, UptimeRobot, or platform health checks |
| **CI/CD failure** | Deploy succeeded but post-deploy health check failed |

> If you have no detection today, add an uptime monitor. Free tiers exist on most platforms. Knowing about an outage before your users tell you is worth the 5 minutes of setup.

---

## Step 2: Assess

Before acting, spend 60 seconds understanding the scope:

- **What's broken?** The whole app? One feature? One page?
- **Who's affected?** All users? A subset? Just you?
- **When did it start?** After a deploy? A config change? Seemingly random?
- **Is data at risk?** If there's any chance of data loss or corruption, that escalates everything.

### Severity (in the moment)

| Severity | Description | Response |
|----------|-------------|----------|
| **Total outage** | App won't load, all users affected | Drop everything, restore immediately |
| **Partial outage** | Core feature broken, app loads but key function doesn't work | Restore within the hour |
| **Degraded** | App works but slowly, or a non-critical feature is broken | Fix at next opportunity, note it |
| **Cosmetic** | Visual glitch, wrong text, non-functional issue | Not an incident — file a bug ticket |

---

## Step 3: Restore

Get the app back to a working state. Speed matters more than elegance.

### Decision: rollback or fix forward?

| Situation | Action |
|-----------|--------|
| Broke after a deploy and the previous version worked | **Rollback** |
| Root cause is obvious AND the fix is a one-line change | **Fix forward** |
| Root cause is unclear | **Rollback** |
| Database state changed and rolling back code won't help | **Fix forward** (carefully) |
| You're unsure | **Rollback** |

See [deployment.md — Rollback](deployment.md#rollback) for platform-specific rollback mechanics.

### If you can't rollback

Some situations resist rollback (database migrations, third-party API changes, corrupted state):

1. **Mitigate** — can you disable the broken feature without taking down the whole app? (Feature flag, config change, static fallback page)
2. **Fix forward** — apply the minimal fix to restore function, then deal with the root cause properly
3. **Communicate** — if restoration will take time, let affected users know (see Step 4)

---

## Step 4: Communicate

Even as a sole dev, communication matters:

### If you have users

- **Status page** (if you have one) — update it. Even a simple GitHub Gist or pinned tweet works.
- **Direct reply** to whoever reported it — "Thanks, I'm aware and working on it."
- **After resolution** — brief update: "Fixed. [Brief explanation]. Sorry for the disruption."

### If it's just you

Still worth a note. A one-line comment on the related issue:

```
Production was down for ~15 minutes. Caused by [X]. Rolled back, then fixed forward in #YY.
```

Future-you will want this context.

---

## Step 5: Investigate

Now that service is restored, figure out what actually happened. This doesn't need to be formal — it needs to be honest.

Answer these questions (in an issue comment or a dedicated postmortem note):

1. **What broke?** Specific symptoms.
2. **What caused it?** Root cause, not just the trigger. "Bad deploy" is a trigger. "Missing environment variable in production config" is a root cause.
3. **When did it start and end?** Timeline with approximate timestamps.
4. **How was it detected?** Did you find it, or did someone tell you?
5. **How was it resolved?** Rollback, fix forward, config change, etc.

### The "five whys" (simplified)

Keep asking "why" until you hit a systemic cause:

- **Why was the site down?** The API returned 500 errors.
- **Why 500 errors?** The database connection string was wrong.
- **Why was it wrong?** The env var wasn't set in the new deploy environment.
- **Why wasn't it set?** No checklist for environment setup when migrating platforms.
- **Root cause:** Missing deployment checklist for environment variables.

Stop when you reach something you can prevent with a process or automation change.

---

## Step 6: Prevent

The investigation should produce one or more concrete actions. File them as tickets.

### Common preventions

| Root cause pattern | Prevention |
|-------------------|-----------|
| Missed environment variable | Add to `.env.example`, add to deploy checklist |
| Untested code path | Add a test for it, add to CI |
| Config change without verification | Add a post-deploy smoke test |
| Dependency broke something | Pin the dependency version, add to `npm audit` |
| "I forgot to..." | Automate it or add it to a checklist |
| Database migration broke rollback | Adopt backward-compatible migration pattern |

Not every incident needs a sweeping process change. Sometimes the prevention is just "be more careful with X" — and that's fine, as long as you're honest about whether that will actually work.

---

## Postmortem Template

For incidents significant enough to warrant documentation (total outages, data loss, anything that affected users for more than a few minutes), write a brief postmortem. This can live as a comment on the related issue or as a standalone document.

```markdown
## Incident: [Brief title]

**Date:** YYYY-MM-DD
**Duration:** [how long users were affected]
**Severity:** [Total outage / Partial outage / Degraded]

### What happened
[2-3 sentences describing the user-visible impact]

### Timeline
- HH:MM — [event]
- HH:MM — [event]
- HH:MM — [resolved]

### Root cause
[What actually caused the problem — be specific]

### Resolution
[How it was fixed — rollback, fix forward, config change]

### Prevention
- [ ] [Action item — filed as #XX]
- [ ] [Action item — filed as #YY]

### Lessons learned
[What went well, what went poorly, what was lucky]
```

> **Blameless, not careless.** A postmortem isn't about blame — you're the only dev, there's no one to blame but yourself. It's about understanding the system well enough to prevent recurrence. "I made a mistake" is fine. "I made a mistake and here's the guardrail that will catch it next time" is the goal.

---

## Sole-Dev Realities

### You won't have on-call

You'll find out about incidents when you check your phone, open your laptop, or hear from a user. That's OK. Mitigate this with:

- **Uptime monitoring** with email/SMS alerts (UptimeRobot, Betterstack, Freshping — all have free tiers)
- **Error tracking** that notifies on spike (Sentry free tier covers most solo projects)
- **Platform alerts** — most hosting platforms can email you on deploy failure or health check failure

### Not every outage needs a postmortem

| Situation | Postmortem? |
|-----------|------------|
| Total outage affecting users | Yes |
| Data loss or corruption | Yes |
| Partial outage lasting >30 min | Yes |
| Brief outage you caught and rolled back in <5 min | No — a comment on the issue is enough |
| Cosmetic bug | No — it's just a bug, not an incident |

### The goal is learning, not process

Enterprise incident response exists because dozens of people need to coordinate under pressure. You don't have that problem. Your version is: fix it, understand it, prevent it. If writing a formal postmortem would take longer than the incident lasted, skip the template and write a paragraph in the issue.

---

## How This Fits the Workflow

Incident response is the exception path — when normal workflow is too slow:

| Normal workflow | Incident response |
|----------------|------------------|
| Steps 1-4 (capture, review, flag, refine) | Compressed into one triage comment |
| Step 5 (implement) | Rollback or minimal fix |
| Step 6 (document) | Postmortem (after resolution) |
| Step 7 (verify) | Smoke test in production |
| Ticket-first | Still ticket-first — file the bug issue before or immediately after restoring |

After the incident is resolved, any follow-up work (root cause fix, new tests, process changes) goes through the normal workflow with proper tickets.

---

## Recommended First Steps

1. **Set up uptime monitoring** — 5 minutes, free tier, email alert when your site goes down
2. **Know how to rollback** — before you need it, find the button or command for your platform (see [deployment.md](deployment.md#rollback))
3. **Bookmark this page** — when production is on fire is not the time to remember the sequence
