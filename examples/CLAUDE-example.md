# Notekeeper — Claude Project Memory

> This is a **worked example** of a filled-in `CLAUDE-TEMPLATE.md` for a hypothetical note-taking app. It demonstrates how to adapt the template to a real project. It declares the **core** profile — Notekeeper has no server, so deployment, CI/CD and incident response don't apply. It keeps a board, to show core + board is a valid combination.
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

See `docs/functional-spec.md` § Status. Kept out of CLAUDE.md — it changes weekly and goes stale here.

<!-- ============================================================
     WORKING IN THIS PROJECT
     Universal process content lives canonically in sdlc-baseline.
     We link out — never paste copies here. See the consumption model:
     https://github.com/Johnesco/sdlc-baseline/blob/main/docs/consumption.md
     ============================================================ -->

## Working in this project

**SDLC profile:** core

This project uses the [sdlc-baseline](https://github.com/Johnesco/sdlc-baseline) universal workflow. Claude must follow these canonical docs:

- [Workflow (7 steps)](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/workflow.md) — ticket-first, decide before you build, documentation-aware
- [Roles & hat-switch protocol](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/roles.md) — PO / BA / Dev / Documenter / QA
- [Definition of Done](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/definition-of-done.md) — exit criteria by issue type, verification-first
- [Severity & priority matrix](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/severity-matrix.md)
- [Commit, PR, and branch conventions](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/commit-conventions.md)
- [Release management](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/release-management.md) — versioning, build numbers, changelogs, hotfixes, milestones
- [Testing](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/testing.md) — testing strategy and the local gate
- [Backlog hygiene](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/backlog-hygiene.md) — review cadence, grooming, planning without sprints
- [ADR protocol](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md) — the six-line stub, threshold rule
- [Profiles](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/profiles.md) — what this profile requires and relaxes

**The Functional Specification** (`docs/functional-spec.md`) is this project's authoritative behavior record. CLAUDE.md and README.md are secondary but must stay consistent.

**Three non-negotiables:**

1. **No code without a ticket.** An Issue — or, for a decision, an ADR stub. This project uses a board, so add it immediately:
   ```
   gh project item-add 2 --owner notekeeper-dev --url [ISSUE_URL]
   ```
2. **Decide before you build.** Anything above a tuning tweak — more than one file, or a behaviour change — gets a six-line ADR stub (Context + Decision) before code.
3. **Claude cannot QA its own work.** The Verify column is always human-owned.

When sdlc-baseline updates, glance at its [CHANGELOG](https://github.com/Johnesco/sdlc-baseline/blob/main/CHANGELOG.md) before adopting changes here.

### Project-specific deviations

This project intentionally diverges from canonical sdlc-baseline guidance in these places (none currently):

- _(none)_

### Project IDs (this project uses a board)

- **Project board:** `PVT_examplePLACEHOLDER`
- **Status field:** `PVTSSF_examplePLACEHOLDER`
- **Status options:** Backlog=`exampleA`, Ready=`exampleB`, In Progress=`exampleC`, Verify=`exampleD`, Done=`exampleE`

### Milestones

| Milestone | Description |
|-----------|-------------|
| Core Editor | Markdown editing, preview, syntax highlighting |
| Storage & Sync | IndexedDB layer, future CouchDB sync |
| Polish & UX | Keyboard shortcuts, dark mode, exports |

## Project History

### Recent Changes
- **2026-02**: Added tag filtering to sidebar (#22)
- **2026-02**: Added pinned notes feature (#20)
- **2026-01**: Migrated from localStorage to IndexedDB (#15)
- **2026-01**: Added keyboard shortcuts (#12)
- **2025-12**: Initial release with basic editor

### Architecture Decisions

Recorded as ADRs in `docs/adr/` (index: `docs/adr/README.md`). Format, stub and threshold rule: [sdlc-baseline `docs/adrs.md`](https://github.com/Johnesco/sdlc-baseline/blob/main/docs/adrs.md).

For example:
- ADR-001 — Vanilla JS, no framework
- ADR-002 — IndexedDB over localStorage
- ADR-003 — marked.js via CDN, no build step

(Pre-ADR decisions previously listed inline can be backfilled as ADRs if they meet the threshold rule.)

## Security Considerations
- Markdown HTML is escaped before rendering (XSS prevention)
- No server-side storage — all data stays on the user's device
- No external API calls in current version
- Content Security Policy headers recommended for deployment

---

*Last updated: February 2026*
*Maintained by: Project contributors and Claude Code sessions*
