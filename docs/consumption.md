# How to Consume sdlc-baseline

> **Treat sdlc-baseline as a library, not a starter kit.** A starter kit is copied once and forgotten. A library is referenced and updated. The first model produces drift; the second produces signal.

This doc tells downstream projects what to **vendor** (copy locally), what to **reference** (link to canonical), and what is **project-only** (never upstream).

---

## TL;DR

| Layer | Pattern | Why |
|---|---|---|
| GitHub-tooling-bound | **Vendored** (must be local at fixed paths) | GitHub's UI reads files from specific paths in the consuming repo |
| AI/dev-tool-bound | **Vendored, but thin** | Claude Code reads project-local `CLAUDE.md` |
| Universal process documentation | **Referenced** (link to sdlc-baseline `main`) | Single source of truth; drift dies |
| Templates / examples | **Referenced + copy-on-use** | Contributors fetch from upstream when needed |
| Project-specific | **Always local, never upstream** | sdlc-baseline doesn't know about your project |

---

## The forcing function: what GitHub itself reads

Some artifacts have to be in the consuming project's repo because GitHub tooling reads them from fixed paths:

- `.github/ISSUE_TEMPLATE/*.yml` — the new-issue UI
- `.github/PULL_REQUEST_TEMPLATE.md` — the new-PR UI
- `scripts/setup-labels.sh` (or equivalent) — runs against the consuming repo's labels
- `CLAUDE.md` — Claude Code reads the project-local file

You cannot reference these. They have to be copies. **This is the only category where vendoring is mandatory.** Everything else is a choice — and the choice should default to referencing.

---

## What to vendor

| Artifact | Source | Destination | Why |
|---|---|---|---|
| `.github/ISSUE_TEMPLATE/*.yml` | sdlc-baseline `.github/ISSUE_TEMPLATE/` | project `.github/ISSUE_TEMPLATE/` | GitHub UI |
| `.github/PULL_REQUEST_TEMPLATE.md` | sdlc-baseline `.github/PULL_REQUEST_TEMPLATE.md` | project `.github/PULL_REQUEST_TEMPLATE.md` | GitHub UI |
| `scripts/setup-labels.sh` | sdlc-baseline `scripts/setup-labels.sh` | project `scripts/setup-labels.sh` | Runs against consuming repo |
| `CLAUDE.md` skeleton | sdlc-baseline `CLAUDE-TEMPLATE.md` | project `CLAUDE.md` | Claude Code reads it; copy once and customize |

The `scripts/sync-github-templates.sh` helper (also in this repo) automates the first three. Run it after sdlc-baseline updates, review the diff, commit the result.

---

## What to reference (link, never copy)

These docs live canonically in sdlc-baseline. Downstream projects link to them from their `CLAUDE.md`. **Never paste their contents into a downstream repo.**

| Artifact | Canonical URL |
|---|---|
| 7-step workflow | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/workflow.md |
| Roles | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/roles.md |
| Definition of Done | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/definition-of-done.md |
| Severity matrix | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/severity-matrix.md |
| Commit / branch conventions | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/commit-conventions.md |
| Board setup | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/board-setup.md |
| Labels | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/labels.md |
| Release management | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/release-management.md |
| Deployment | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/deployment.md |
| CI/CD | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/ci-cd.md |
| Backlog hygiene | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/backlog-hygiene.md |
| Incident response | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/incident-response.md |
| ADR protocol | https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md |
| ADR template | https://github.com/Johnesco/sdlc-baseline/blob/main/examples/adr-template.md |
| ADR worked example | https://github.com/Johnesco/sdlc-baseline/blob/main/examples/adr-example.md |

If you find yourself wanting to paste any of these into a downstream `CLAUDE.md` or `docs/` folder, **stop and link instead**.

---

## What stays project-only (never upstream)

These belong in each consuming project. sdlc-baseline cannot have opinions about them.

- `docs/functional-spec.md` — the project's authoritative behavior record
- `docs/adr/*.md` — the project's actual architecture decisions
- `docs/architecture.md` — project-specific diagrams
- Project identity, mission, target users, live URL
- File structure overview (varies per project)
- Project-specific data formats / schemas
- Project-specific milestones
- Project-specific GitHub Project IDs and field IDs
- "Project-specific deviations" — anywhere your project intentionally diverges from sdlc-baseline canonical guidance

---

## What your CLAUDE.md should look like

A consuming project's `CLAUDE.md` is **thin and project-specific**. It contains identity, structure, conventions, milestones, and a "Working in this project" section that **links to** sdlc-baseline canonical docs rather than restating them.

A sketch:

```markdown
# <Project Name> — Claude Project Memory

## Project Identity
**Name:** <…>
**Purpose:** <…>
**Target Users:** <…>
**Live Site:** <URL>

## Architecture
<project-specific stack, patterns, layout>

## File Structure Overview
<project-specific tree>

## <Project-specific data formats / schemas>

## Working in this project

This project uses the [sdlc-baseline](https://github.com/Johnesco/sdlc-baseline)
universal workflow. Read the canonical docs:

- [Workflow (7 steps)](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/workflow.md)
- [Roles & hat-switch protocol](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/roles.md)
- [Definition of Done](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/definition-of-done.md)
- [Severity matrix](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/severity-matrix.md)
- [Commit / branch conventions](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/commit-conventions.md)
- [Release management](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/release-management.md)
- [Deployment](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/deployment.md)
- [CI/CD](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/ci-cd.md)
- [Backlog hygiene](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/backlog-hygiene.md)
- [Incident response](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/incident-response.md)
- [ADR protocol](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md)

### Project-specific deviations

<None — fill in any place this project intentionally differs from canonical.>

### Project IDs

- GitHub Project board: PVT_…
- Status field: PVTSSF_…
- Status options: Backlog=…, Ready=…, In Progress=…, Verify=…, Done=…

### Milestones

<project-specific milestone table>

### Architecture Decisions

ADRs live in `docs/adr/`. See the [index](docs/adr/README.md). Format and threshold rule documented in [sdlc-baseline `docs/adrs.md`](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md).

## Security Considerations
<project-specific>

## Related Documentation
<project-specific>
```

That's the whole shape. **No copy of the 7-step workflow. No re-stated role table. No board automations table. Links only.**

---

## Why drift happens (and how this prevents it)

Vendoring an entire process spec into every consuming repo guarantees drift because:

1. The process changes upstream and downstream copies don't update.
2. Downstream projects accidentally edit the vendored copy thinking it's "their" file.
3. New downstream projects fork from a stale state of an existing downstream project, propagating the drift further.

We have direct evidence: an "Architecture Decisions" placeholder existed in `CLAUDE-TEMPLATE.md`, was vendored into karaokedirectory, then quietly disappeared at some point and was only noticed when ADR work started.

The reference model prevents drift by ensuring there is exactly one place the canonical content exists, and that place is read-only from downstream projects' perspective.

---

## Versioning strategy

For solo + AI-assisted scale, **always-latest with `CHANGELOG.md`** is the right amount of process:

- sdlc-baseline `main` is always the canonical version.
- Every meaningful change to sdlc-baseline gets a `CHANGELOG.md` entry.
- Downstream projects glance at the CHANGELOG when they next touch CLAUDE.md.
- No tags, no submodules, no version pinning until a second human contributor joins.

When to escalate:

- **Tag releases (`v1.0`, `v1.1`)** when downstream projects need stability across breaking process changes (e.g. a workflow step renumber).
- **Date-stamp the project's commitment** in CLAUDE.md ("aligned with sdlc-baseline `main` as of YYYY-MM-DD") if you want a weak audit trail without tags.
- **Submodules / subtrees** — explicitly rejected at this scale. Not enough artifacts to justify the complexity.

---

## Migration path for existing projects

Projects that vendored the full template before this guidance existed should slim their `CLAUDE.md` next time they touch it:

1. Identify the universal-process block (look for `<!-- SDLC WORKFLOW -->` markers or large duplicated tables).
2. Diff against `CLAUDE-TEMPLATE.md` to find any project-specific customizations buried inside.
3. Capture customizations under "Project-specific deviations" — or upstream them to sdlc-baseline if they're actually universal improvements.
4. Replace the rest with the link block from the sketch above.
5. Migrate any project-board IDs from user-scoped memory into the project's `CLAUDE.md`.

Karaokedirectory is the seminal example — see issue [#57](https://github.com/Johnesco/karaokedirectory/issues/57).

---

## What this is not

- **Not enforcement.** Nothing here is policed by CI. The discipline is human + AI.
- **Not exhaustive.** New artifacts may need to be categorized; default to *reference* unless GitHub's tooling forces vendoring.
- **Not stable forever.** When sdlc-baseline grows beyond ~20 docs, this consumption model itself may need to evolve. Until then, links are enough.
