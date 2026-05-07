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

[How tests are organized and run; debug modes; verification conventions.]

<!-- ============================================================
     WORKING IN THIS PROJECT
     Universal process content lives canonically in sdlc-baseline.
     Link out — do NOT paste copies here. Drift kills.
     ============================================================ -->

## Working in this project

This project uses the [sdlc-baseline](https://github.com/Johnesco/sdlc-baseline) universal workflow. Claude must follow these canonical docs:

- [Workflow (7 steps)](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/workflow.md) — ticket-first, documentation-aware
- [Roles & hat-switch protocol](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/roles.md) — PO / BA / Dev / Documenter / QA
- [Definition of Done](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/definition-of-done.md) — exit criteria by issue type
- [Severity & priority matrix](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/severity-matrix.md)
- [Commit, PR, and branch conventions](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/commit-conventions.md)
- [ADR protocol](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md) — when and how to record architectural decisions
- [Board setup](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/board-setup.md) and [labels](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/labels.md) — one-time setup

**Two non-negotiables:**

1. **No code without a ticket.** Every change starts as a GitHub Issue. Add it to the project board immediately after creating it (the `gh project item-add` command does NOT auto-fire on issue creation).
2. **Claude cannot QA its own work.** The Verify column is always human-owned.

When sdlc-baseline updates, glance at its [CHANGELOG](https://github.com/Johnesco/sdlc-baseline/blob/main/CHANGELOG.md) before adopting changes here.

### Project-specific deviations

[None — fill this in if this project intentionally diverges from canonical sdlc-baseline guidance. Be explicit; drift hides here otherwise.]

### Project IDs

> GitHub Projects field IDs and option IDs for this project. Used by Claude when scripting `gh` commands.

- **Project board:** `PVT_…`
- **Status field:** `PVTSSF_…`
- **Status options:** Backlog=`…`, Ready=`…`, In Progress=`…`, Verify=`…`, Done=`…`

### Milestones

[Project-specific milestone table.]

| Milestone | Description |
|-----------|-------------|
| [Name] | [Scope] |

### Architecture Decisions

ADRs live in [`docs/adr/`](docs/adr/). See the [index](docs/adr/README.md) for the running list. Format and threshold rule documented in [sdlc-baseline `docs/adrs.md`](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md).

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
