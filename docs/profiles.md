# Profiles

> **Profile:** core — this document defines the profiles.

sdlc-baseline is one standard in two sizes. A **profile** is the set of docs a project is held to. Every doc carries a one-line badge naming its profile; a project declares its profile once, in `CLAUDE.md`, and reads only the docs that apply.

---

## The two profiles

| Profile | Who it's for | What it contains |
|---------|--------------|------------------|
| **`core`** | Anything that ships as an artifact or runs entirely on the user's machine: a browser game on itch.io, a desktop app, a CLI, a library, a static site with no backend | The ticket-first workflow, roles, Definition of Done, ADRs, commit conventions, releases and versioning, testing, backlog hygiene, security basics |
| **`core+ops`** | Anything that runs as a service you operate: a hosted site with a database and users, an API, a bot that has to stay up | Everything in core, plus deployment, CI/CD, and incident response |

The split is about what you **operate**, not how many people you are. A solo developer running a hosted site with users needs `core+ops`. A team shipping a desktop app needs `core`.

**Undeclared = core.** A `CLAUDE.md` with no profile line is a core project. This is a relaxation, so existing projects keep working; a project that wants the ops docs to stay binding adds the line.

---

## Manifest

### Core — every project

| Doc | Purpose |
|-----|---------|
| [start-here.html](start-here.html) | Orientation — why the process pays for one person, the loop, the first week. Read front to back; carries no badge because it is the map, not the territory |
| [workflow.md](workflow.md) | The 7-step ticket-first workflow, with the decide-before-you-build gate |
| [roles.md](roles.md) | PO / BA / Dev / Documenter / QA and the hat-switch protocol |
| [definition-of-done.md](definition-of-done.md) | Exit criteria by issue type — verification-first |
| [severity-matrix.md](severity-matrix.md) | Bug severity and priority |
| [commit-conventions.md](commit-conventions.md) | Commit, PR, and branch naming |
| [release-management.md](release-management.md) | Versioning, build numbers, changelogs, releases, hotfixes, milestones |
| [testing.md](testing.md) | Testing strategy and the local gate |
| [backlog-hygiene.md](backlog-hygiene.md) | Review cadence, grooming, planning without sprints |
| [adrs.md](adrs.md) | ADR protocol, threshold rule, the six-line stub |
| [security-basics.md](security-basics.md) | Secrets, dependencies, XSS; server-only sections headed `(ops)` |
| [labels.md](labels.md) | Label taxonomy |
| [board-setup.md](board-setup.md) | GitHub Projects board — *if you use one* |
| [kickoff-checklist.md](kickoff-checklist.md) | Day-1 setup; Phases 3–4 are ops |
| [consumption.md](consumption.md) | How downstream projects consume sdlc-baseline |
| [profiles.md](profiles.md) | This doc |

### Ops — add for projects that run a service

| Doc | Purpose |
|-----|---------|
| [deployment.md](deployment.md) | Deploy patterns, environments, config/secrets, rollback |
| [ci-cd.md](ci-cd.md) | Pipelines, GitHub Actions, branch protection — the ops gate |
| [incident-response.md](incident-response.md) | Production incidents: detect, restore, investigate, prevent |

---

## What core relaxes — and what it keeps

| Concern | core | core+ops |
|---------|------|----------|
| The ticket | A GitHub Issue (default; always for bugs) **or** an ADR stub for a decision | Same |
| Board | Optional — `gh issue list --state open` is the board. If you use one, [board-setup.md](board-setup.md) applies unchanged | Recommended |
| Milestones | Optional | Recommended |
| Pull requests | Optional — commit to `main` with `#XX:` references | Recommended; required under branch protection |
| Gate | **Required:** one local test command must pass before a release tag — [testing.md](testing.md#the-local-gate-core) | CI must pass — [ci-cd.md](ci-cd.md) |
| Decide before you build | **Required:** a six-line ADR stub before code for anything above a tuning tweak — [adrs.md](adrs.md#the-six-line-stub--decide-before-you-build) | Same |
| ADRs by the [threshold rule](adrs.md#threshold-rule--when-to-write-one) | Required | Required |
| Definition of Done | Applies — verification-first | Applies |
| Verify | Human-owned, always | Same |
| Deployment, incidents | Not applicable — your "production" is the artifact you uploaded | [deployment.md](deployment.md), [incident-response.md](incident-response.md) |

Core is not "lite". It drops the layers a project without a running service cannot exercise, and adds the one thing ops projects never needed a doc for: deciding before building. Everything else is the same discipline.

---

## Declaring a profile

In `CLAUDE.md`, directly under `## Working in this project`:

```markdown
**SDLC profile:** core
```

or `**SDLC profile:** core+ops`. `CLAUDE-TEMPLATE.md` ships with the line in place and the ops link block marked for deletion in core projects.

---

## Upgrading core → core+ops

The moment a core project grows a service — a backend, a database, anything with uptime — it is core+ops:

1. Change the profile line in `CLAUDE.md`.
2. Restore the ops link block (deployment, CI/CD, incident response) from `CLAUDE-TEMPLATE.md`.
3. Run [kickoff-checklist.md](kickoff-checklist.md) Phases 3–4.
4. CI becomes the gate; the local test command keeps running inside it.

Downgrading is the reverse, and rare: a service you switched off is usually a project you archived.

---

## Section-level markers

One doc genuinely splits: [security-basics.md](security-basics.md) is core, with its server-only sections (authentication, CSRF, IDOR, injection, HTTPS headers, production monitoring) headed `(ops)`. Core projects skip those sections. No other doc uses section markers — a doc is core or it is ops.
