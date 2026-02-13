# Notekeeper — Claude Project Memory

> This is a **worked example** of a filled-in `CLAUDE-TEMPLATE.md` for a hypothetical note-taking app. It demonstrates how to adapt the template to a real project.
>
> **Source template:** [`CLAUDE-TEMPLATE.md`](../CLAUDE-TEMPLATE.md)

<!-- ============================================================
     PROJECT-SPECIFIC SECTIONS
     ============================================================ -->

## Project Identity

**Name:** Notekeeper
**Purpose:** A minimal note-taking web app with markdown support and local-first storage
**Target Users:** Developers who want a distraction-free writing tool that works offline
**Live Site:** https://example.com/notekeeper

## File Structure Overview

```
notekeeper/
├── CLAUDE.md              # THIS FILE
├── README.md              # Public documentation
├── index.html             # Main SPA
│
├── css/
│   ├── base.css           # Variables, reset, typography
│   ├── layout.css         # Page structure
│   └── components.css     # Editor, sidebar, modals
│
├── js/
│   ├── app.js             # Entry point
│   ├── editor.js          # Markdown editor component
│   ├── sidebar.js         # Note list sidebar
│   ├── storage.js         # IndexedDB wrapper
│   └── utils/
│       ├── markdown.js    # Markdown-to-HTML rendering
│       └── date.js        # Date formatting
│
├── docs/
│   └── functional-spec.md # Feature specification
│
└── tests/
    └── storage.test.js    # Storage layer tests
```

## Key Technical Patterns

### Storage Layer
```javascript
// All data operations go through storage.js
import { saveNote, getNote, listNotes, deleteNote } from './storage.js';

// Notes are stored in IndexedDB for offline support
const note = await getNote('note-id');
```

### Event-Driven UI
```javascript
// Components communicate via custom events on document
document.dispatchEvent(new CustomEvent('note:selected', { detail: { id } }));
document.addEventListener('note:selected', (e) => loadNote(e.detail.id));
```

### Markdown Rendering
- Uses `marked.js` library (CDN-loaded, no build step)
- Rendering is sandboxed — HTML in markdown is escaped
- Live preview updates on debounced input (300ms)

## Data Formats

### Note Object
```javascript
{
  id: "uuid-v4-string",        // Auto-generated on creation
  title: "Note Title",          // First line of content, or "Untitled"
  content: "# Markdown\n...",   // Raw markdown string
  createdAt: "2026-01-15T...",  // ISO 8601
  updatedAt: "2026-02-10T...", // ISO 8601
  tags: ["work", "draft"],     // User-defined tags
  pinned: false                // Pinned notes sort first
}
```

## Current Feature Status

### Implemented
- [x] Create, edit, and delete notes
- [x] Markdown editor with live preview
- [x] IndexedDB local storage (offline-capable)
- [x] Note list sidebar with search
- [x] Tag filtering
- [x] Pinned notes
- [x] Keyboard shortcuts (Ctrl+N, Ctrl+S, Ctrl+P)

### In Progress
- [ ] Export to `.md` file (#23)
- [ ] Dark mode toggle (#24)

### Planned
- [ ] Multi-device sync via CouchDB
- [ ] Collaborative editing

<!-- ============================================================
     SDLC WORKFLOW
     This section is universal. It works across any project that
     uses GitHub Issues + Projects for tracking.

     Source: https://github.com/Johnesco/sdlc-baseline
     ============================================================ -->

## Instructions for Claude

### Ticket-First, Documentation-Aware Workflow (MANDATORY)

Every software change — feature, bug fix, refactor, or data update — follows this sequence. No step may be skipped.

The **Functional Specification** (`docs/functional-spec.md`) is the authoritative record of all application features, behavior, and data formats. It is the single source of truth for what this application does.

**Before ANY change**, follow these steps in order:

1. **Capture as a ticket** — Create a GitHub Issue describing the change before any other work begins. Include a clear title, relevant labels, acceptance criteria, and an associated **milestone**. Every issue must belong to an existing milestone by the time it ships; if no existing milestone fits, create a new one. No code is written without a ticket.

   > **IMPORTANT — Add to Project Board:** After creating the issue, you **must** also add it to the GitHub Projects board. The `gh issue create` command does **NOT** auto-add issues to the project board. Run this immediately after creating the issue:
   > ```
   > gh project item-add 2 --owner notekeeper-dev --url [ISSUE_URL]
   > ```
   > An issue that is not on the board is considered incomplete.

2. **Review documentation for affected areas** — Read the sections of the Functional Specification (and other docs like CLAUDE.md, README.md) that describe the area being changed. Identify what exists, what will be impacted, and note any discrepancies.

3. **Flag discrepancies** — If existing code already differs from what the documentation says, stop and flag the mismatch for validation before proceeding. Do not silently "fix" documentation to match code or vice versa without explicit confirmation.

4. **Refine the ticket** — Based on the documentation review, update the GitHub Issue with additional context, affected doc sections, and a plan for documentation updates. The ticket should reflect the full scope of work including doc changes.

5. **Implement the change** — Write the code. Reference the ticket number (`#XX`) in commits.

6. **Update all documentation** — Update the Functional Specification, CLAUDE.md, README.md, and any other affected docs so they accurately reflect the new state. This is not optional — a change is not complete until its documentation is current.

7. **Verify consistency** — After updating, confirm that the documentation and code are in agreement. Any remaining gaps must be called out explicitly.

**Key rules:**
- No code without a ticket — every change starts as a GitHub Issue
- A change without a corresponding documentation update is considered **incomplete**
- Documentation updates are part of the definition of done, not a follow-up task
- When in doubt about whether docs need updating, they do
- The Functional Specification is the primary document; CLAUDE.md and README.md are secondary but must stay consistent

### When Making Changes
1. **Ticket first** — Follow the workflow above before all else
2. **Read before editing** — Always read files before modifying them
3. **Follow existing patterns** — Match the event-driven, module-based style in the codebase
4. **Keep it simple** — No build step, no framework, no over-engineering

### Maintaining Documentation

**UPDATE the Functional Specification** (`docs/functional-spec.md`) when you:
- Add, modify, or remove any feature
- Fix a bug that changes observable behavior
- Change the note data format
- Alter UI behavior or keyboard shortcuts

**UPDATE CLAUDE.md** when you:
- Add new files or change the structure
- Modify the storage layer or event system
- Add new keyboard shortcuts
- Make significant design decisions

**UPDATE README.md** when changes affect:
- Feature descriptions
- Setup or usage instructions
- Keyboard shortcut reference

## Development Workflow

### GitHub Issues & Projects

All work is tracked in **GitHub Issues** with a **GitHub Projects** kanban board.

- **Issues** = All work items (features, bugs, docs, chores)
- **Labels** = Type (`feature`, `bug`, `docs`, `chore`) + Area (`area:frontend`, `area:data`) + Priority (`priority:high`, `priority:low`)
- **Milestones** = Core Editor, Storage & Sync, Polish & UX
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
     ============================================================ -->

## Project History

### Recent Changes
- **2026-02**: Added tag filtering to sidebar (#22)
- **2026-02**: Added pinned notes feature (#20)
- **2026-01**: Migrated from localStorage to IndexedDB (#15)
- **2026-01**: Added keyboard shortcuts (#12)
- **2025-12**: Initial release with basic editor

### Architecture Decisions
1. **Vanilla JS** — No framework, educational and lightweight
2. **IndexedDB over localStorage** — Handles larger notes, supports future sync
3. **marked.js via CDN** — Proven library, no build step needed
4. **Custom events over pub/sub** — Uses the platform, no dependencies
5. **Ticket-first workflow** — Adopted from [sdlc-baseline](https://github.com/Johnesco/sdlc-baseline)

## Security Considerations
- Markdown HTML is escaped before rendering (XSS prevention)
- No server-side storage — all data stays on the user's device
- No external API calls in current version
- Content Security Policy headers recommended for deployment

---

*Last updated: February 2026*
*Maintained by: Project contributors and Claude Code sessions*
