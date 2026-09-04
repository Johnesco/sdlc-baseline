# [Your Project Name] - Claude Project Memory

> This file serves as persistent context for Claude Code sessions. It is automatically read at the start of every conversation. Keep this document **thin and project-specific** — link to canonical sdlc-baseline docs rather than restating them. See [sdlc-baseline consumption model](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/consumption.md).

<!-- ============================================================
     PROJECT-SPECIFIC SECTIONS
     Fill these in for your project. They provide context Claude
     needs to understand your codebase.
     ============================================================ -->

## Project Identity

**Name:** [Your project name]
**Purpose:** [One-sentence description of what this project does]
**Target Users:** [Who uses this]
**Live Site:** [Deployment URL, if applicable]

## Architecture

[Project-specific stack, patterns, layout decisions. Examples: language/framework, build/no-build, deployment target, key dependencies.]

## File Structure Overview

```
your-project/
├── CLAUDE.md              # THIS FILE
├── README.md              # Public documentation
├── [your structure here]
```

> Update this section as the project grows. Claude uses it to navigate the codebase.

## Key Technical Patterns

[Document the patterns Claude should follow when writing code. Examples: state management approach, component lifecycle, naming conventions, error handling patterns.]

## Data Formats

[If your project has a data model (API responses, config files, database schema), document the canonical format here so Claude produces consistent output.]

## Testing

[How tests are organized and run. Name the local gate: the one command that must pass before a release tag, e.g. `npm test`.]

## Releases

**Version source of truth:** [`package.json` `version` / `VERSION` file]
**Build numbers:** [yes — `BUILD` file, shown as `x.y.z (build N)` / no]
**Release command:** [`npm run release` — runs the gate, bumps, tags, packages]

<!-- ============================================================
     WORKING IN THIS PROJECT
     Universal process content lives canonically in sdlc-baseline.
     Link out — do NOT paste copies here. Drift kills.
     ============================================================ -->

## Working in this project

**SDLC profile:** core
<!-- or: core+ops — for projects that run a service (hosted site, API, database with users).
     Undeclared = core. See https://github.com/Johnesco/sdlc-baseline/blob/main/docs/profiles.md -->

This project uses the [sdlc-baseline](https://github.com/Johnesco/sdlc-baseline) universal workflow. Claude must follow these canonical docs:

- [Workflow (7 steps)](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/workflow.md) — ticket-first, decide before you build, documentation-aware
- [Roles & hat-switch protocol](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/roles.md) — PO / BA / Dev / Documenter / QA
- [Definition of Done](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/definition-of-done.md) — exit criteria by issue type, verification-first
- [Severity & priority matrix](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/severity-matrix.md)
- [Commit, PR, and branch conventions](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/commit-conventions.md)
- [Release management](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/release-management.md) — versioning, build numbers, changelogs, hotfixes, milestones
- [Testing](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/testing.md) — testing strategy and the local gate
- [Backlog hygiene](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/backlog-hygiene.md) — review cadence, grooming, planning without sprints
- [ADR protocol](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md) — the six-line stub, threshold rule, format
- [Security basics](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/security-basics.md) — secrets, dependencies, XSS; `(ops)` sections only for core+ops
- [Profiles](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/profiles.md) — what this profile requires and relaxes
- [Board setup](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/board-setup.md) and [labels](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/labels.md) — one-time setup; the board is optional in core

<!-- OPS BLOCK — delete this block if the profile is core. Keep it for core+ops. -->
- [Deployment](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/deployment.md) — deploy patterns, environments, config/secrets, rollback
- [CI/CD](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/ci-cd.md) — GitHub Actions, starter workflows, branch protection — the ops gate
- [Incident response](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/incident-response.md) — production incidents: restore, investigate, prevent
<!-- END OPS BLOCK -->

**Three non-negotiables:**

1. **No code without a ticket.** An Issue — or, for a decision, an ADR stub. Add it to the board if you use one (the `gh project item-add` command does NOT auto-fire on issue creation).
2. **Decide before you build.** Anything above a tuning tweak — more than one file, or a behaviour change — gets a six-line ADR stub (Context + Decision) before code. If you can't write the paragraph, it isn't ready.
3. **Claude cannot QA its own work.** The Verify column is always human-owned.

When sdlc-baseline updates, glance at its [CHANGELOG](https://github.com/Johnesco/sdlc-baseline/blob/main/CHANGELOG.md) before adopting changes here.

### Project-specific deviations

[None — fill this in if this project intentionally diverges from canonical sdlc-baseline guidance. Be explicit; drift hides here otherwise.]

### Project IDs (delete if no board)

> GitHub Projects field IDs and option IDs for this project. Used by Claude when scripting `gh` commands.

- **Project board:** `PVT_…`
- **Status field:** `PVTSSF_…`
- **Status options:** Backlog=`…`, Ready=`…`, In Progress=`…`, Verify=`…`, Done=`…`

### Milestones (optional)

[Project-specific milestone table.]

| Milestone | Description |
|-----------|-------------|
| [Name] | [Scope] |

### Architecture Decisions

ADRs live in `docs/adr/` in this project (index: `docs/adr/README.md`). Format, stub and threshold rule: [sdlc-baseline `docs/adrs.md`](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md).

<!-- ============================================================
     PROJECT HISTORY & SECURITY
     ============================================================ -->

## Project History

### Recent Changes
- [Log significant changes here as they happen]

## Security Considerations

- [Document project-specific security rules here]
- Always validate user input at system boundaries
- Never store secrets in code

---

> **Maintenance note:** This template is intentionally short. Resist the urge to paste sdlc-baseline content into the consuming project. If you find yourself wanting to, add a link instead. See [`docs/consumption.md`](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/consumption.md).
