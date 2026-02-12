# [Your Project Name] - Claude Project Memory

> This file serves as persistent context for Claude Code sessions. It is automatically read at the start of every conversation. Keep this document updated as the project evolves.

<!-- ============================================================
     PROJECT-SPECIFIC SECTIONS
     Fill these in for your project. They provide context that
     Claude needs to understand your codebase.
     ============================================================ -->

## Project Identity

**Name:** [Your project name]
**Purpose:** [One-sentence description of what this project does]
**Target Users:** [Who uses this]
**Live Site:** [Deployment URL, if applicable]

## File Structure Overview

```
your-project/
├── CLAUDE.md              # THIS FILE
├── README.md              # Public documentation
├── [your structure here]
```

> Update this section as the project grows. Claude uses it to navigate the codebase.

## Key Technical Patterns

> Document the patterns Claude should follow when writing code. Examples:
> - State management approach
> - Component lifecycle
> - Naming conventions
> - Error handling patterns

## Data Formats

> If your project has a data model (API responses, config files, database schema), document the canonical format here so Claude produces consistent output.

## Current Feature Status

### Implemented
- [ ] [List completed features]

### In Progress
- [ ] [List active work]

### Planned
- [ ] [List upcoming work]

<!-- ============================================================
     SDLC WORKFLOW
     This section is universal. It works across any project that
     uses GitHub Issues + Projects for tracking.

     Source: https://github.com/Johnesco/sdlc-baseline
     ============================================================ -->

## Instructions for Claude

### Ticket-First, Documentation-Aware Workflow (MANDATORY)

Every software change — feature, bug fix, refactor, or data update — follows this sequence. No step may be skipped.

The **project specification** ([your spec file, e.g., `docs/functional-spec.md`]) is the authoritative record of all application features, behavior, and data formats. It is the single source of truth for what this application does.

> If your project does not yet have a spec, treat CLAUDE.md as the primary record until one exists.

**Before ANY change**, follow these steps in order:

1. **Capture as a ticket** — Create a GitHub Issue describing the change before any other work begins. Include a clear title, relevant labels, acceptance criteria, and an associated **milestone**. Every issue must belong to an existing milestone by the time it ships; if no existing milestone fits, create a new one. No code is written without a ticket.

   > **IMPORTANT — Add to Project Board:** After creating the issue, you **must** also add it to the GitHub Projects board. The `gh issue create` command does **NOT** auto-add issues to the project board. Run this immediately after creating the issue:
   > ```
   > gh project item-add [PROJECT_NUMBER] --owner [OWNER] --url [ISSUE_URL]
   > ```
   > An issue that is not on the board is considered incomplete. This is a known gotcha — do not skip this step.

2. **Review documentation for affected areas** — Read the sections of the spec (and other docs like CLAUDE.md, README.md) that describe the area being changed. Identify what exists, what will be impacted, and note any discrepancies.

3. **Flag discrepancies** — If existing code already differs from what the documentation says, stop and flag the mismatch for validation before proceeding. Do not silently "fix" documentation to match code or vice versa without explicit confirmation.

4. **Refine the ticket** — Based on the documentation review, update the GitHub Issue with additional context, affected doc sections, and a plan for documentation updates. The ticket should reflect the full scope of work including doc changes.

5. **Implement the change** — Write the code. Reference the ticket number (`#XX`) in commits.

6. **Update all documentation** — Update the spec, CLAUDE.md, README.md, and any other affected docs so they accurately reflect the new state. This is not optional — a change is not complete until its documentation is current.

7. **Verify consistency** — After updating, confirm that the documentation and code are in agreement. Any remaining gaps must be called out explicitly.

**Key rules:**
- No code without a ticket — every change starts as a GitHub Issue
- A change without a corresponding documentation update is considered **incomplete**
- Documentation updates are part of the definition of done, not a follow-up task
- When in doubt about whether docs need updating, they do
- The spec is the primary document; CLAUDE.md and README.md are secondary but must stay consistent

### When Making Changes
1. **Ticket first** — Follow the workflow above before all else
2. **Read before editing** — Always read files before modifying them
3. **Follow existing patterns** — Match the coding style already in use
4. **Keep it simple** — Avoid over-engineering

### Maintaining Documentation

**UPDATE the project spec** when you:
- Add, modify, or remove any feature
- Fix a bug that changes observable behavior
- Change data formats or API contracts
- Alter UI behavior, states, or interactions

**UPDATE CLAUDE.md** when you:
- Add new features or pages
- Change the file structure
- Modify architectural patterns
- Make significant design decisions

**UPDATE README.md** when changes affect:
- Public-facing feature descriptions
- Setup or usage instructions
- Project overview

## Development Workflow

### GitHub Issues & Projects

All work is tracked in **GitHub Issues** with a **GitHub Projects** kanban board.

- **Issues** = All work items (features, bugs, docs, chores)
- **Labels** = Type (`feature`, `bug`, `docs`, `chore`) + Area (`area:frontend`, `area:backend`, etc.) + Priority (`priority:high`, `priority:low`)
- **Milestones** = Major feature areas. Every issue must have a milestone by the time it ships. If no existing milestone fits, create a new one.
- **Projects board** = Visual kanban for tracking status

### Board Columns

| Column | What's Here |
|--------|-------------|
| **Backlog** | Captured but not yet scoped |
| **Refining** | Defining scope and requirements |
| **Ready** | Acceptance criteria finalized, ready to build |
| **In Progress** | Actively being coded |
| **Verify** | Code complete, awaiting human testing |
| **Done** | Verified and accepted |

### Board Automations (GitHub Projects Workflows)

These transitions are handled automatically by GitHub Projects:

| Trigger | Sets Status To |
|---------|---------------|
| Item added to project | **Backlog** |
| Item reopened | **In Progress** |
| Item closed | **Done** |
| Pull request merged | **Done** |

These transitions are **manual** and must be set during the workflow:

| Transition | When to Move |
|------------|-------------|
| Backlog → Refining | When scoping/discussing the issue |
| Refining → Ready | When acceptance criteria are finalized |
| Ready → In Progress | When coding begins |
| In Progress → Verify | When code is complete, awaiting testing |

### Commit Convention

```
#XX: description
```

Where `XX` is the GitHub Issue number. Use `Fixes #XX` in PR body for auto-close.

### Idea to Ship Cycle

| Phase | What Happens |
|-------|--------------|
| **Capture** | `gh issue create` + add to project board |
| **Refine** | Discussion in issue comments, spec it out |
| **Build** | PR with `Fixes #XX`, branch + implementation |
| **Verify** | PR includes spec updates, human reviews |
| **Ship** | Merge PR → issue auto-closes → board updates |

<!-- ============================================================
     END SDLC WORKFLOW
     Everything below this line is project-specific.
     ============================================================ -->

## Project History

### Recent Changes
- [Log significant changes here as they happen]

### Architecture Decisions
- [Document key technical decisions and their rationale]

## Security Considerations

- [Document project-specific security rules here]
- Always validate user input at system boundaries
- Never store secrets in code

---

*Last updated: [Date]*
*Maintained by: Project contributors and Claude Code sessions*
