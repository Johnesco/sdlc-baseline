# sdlc-baseline — Claude Project Memory

> Persistent context for Claude Code sessions in this repo. Keep it thin: this project *is* the canonical process documentation, so process rules live in `docs/`, not here.

## Project Identity

**Name:** sdlc-baseline
**Purpose:** A lightweight, GitHub-native development lifecycle for solo devs and AI-assisted teams, consumed by reference rather than copied.
**Target Users:** The author's own projects — currently singalong (`core`), karaokedirectory (`core+ops`), ifhub, Pavement Pursuit.
**Live Site:** N/A — a documentation repository.

## Architecture

Markdown documents plus a small number of files GitHub's tooling reads from fixed paths. There is no build step and no runtime. The only executable code is in `scripts/`.

## File Structure Overview

```
sdlc-baseline/
├── CLAUDE.md                  # THIS FILE
├── README.md                  # Index, artifact table, adoption paths
├── CHANGELOG.md               # The signal downstream projects read
├── CLAUDE-TEMPLATE.md         # Copied into new projects as their CLAUDE.md
├── docs/                      # The standard. Each file badged core or ops
│   ├── start-here.html        # Orientation — the one doc read front to back
│   └── profiles.md            # The core / core+ops mechanism
├── examples/                  # Templates: ADR stub, ADR, functional spec, CLAUDE.md
├── scripts/
│   ├── check-docs.py          # THE GATE — see Testing below
│   ├── setup-labels.sh        # Vendored downstream
│   └── sync-github-templates.sh
└── .github/                   # Issue + PR templates, vendored downstream
```

## Key Technical Patterns

- **Link, never paste.** Downstream projects reference canonical docs by absolute GitHub URL. A copy is a fork nobody remembers making. See `docs/consumption.md`.
- **Tag in place; never move a file.** Downstream repos link to `blob/main/<path>#<anchor>` and GitHub does not redirect moved blobs. Renaming a file or a linked heading breaks other people's repos with no error anywhere. The `contract` check in the gate exists for exactly this.
- **The profile badge is line 3** of every `docs/*.md`, after the H1 and a blank line.
- **Duplication that GitHub forces is checked, not trusted.** The four severity strings exist in both `docs/severity-matrix.md` and `.github/ISSUE_TEMPLATE/bug.yml` because the GitHub UI reads the yml from a fixed path. The gate asserts they match.

## Testing

**The gate:**

```bash
python scripts/check-docs.py        # -v to show what each check verified
```

Nine deterministic checks: link and anchor integrity across markdown *and* html, orphaned docs, profile badges, the ops-doc set, the published downstream URL contract, severity-string sync, `CLAUDE-TEMPLATE.md` integrity, and forbidden hygiene patterns.

Standard library only — no network, no dependencies, no clock, no model in the loop. It must be green before any release tag. Extend it whenever a new invariant appears; a rule nothing checks is a rule that has already drifted.

## Releases

**Version source of truth:** the `## [x.y.z]` heading in `CHANGELOG.md` (no package manifest exists).
**Build numbers:** no — this ships as a git ref, not an artifact.
**Release command:** none. Run the gate, move `[Unreleased]` into a version section, commit, push `main`.

<!-- ============================================================
     WORKING IN THIS PROJECT
     ============================================================ -->

## Working in this project

**SDLC profile:** core
<!-- sdlc-baseline is documentation. Nothing is deployed and nothing can be down,
     so deployment, CI/CD and incident response do not apply. See docs/profiles.md. -->

This repo is the canonical source of the process, so read the docs in `docs/` directly rather than any copy. Start with [`docs/profiles.md`](docs/profiles.md) and [`docs/workflow.md`](docs/workflow.md).

**Three non-negotiables:**

1. **No code without a ticket.** A GitHub Issue — or, for a decision, a six-line ADR stub.
2. **Decide before you build.** Anything above a tuning tweak gets a stub (Context + Decision) before the change. If you can't write the paragraph, it isn't ready.
3. **Claude cannot QA its own work.** Verify is human-owned — and the gate is not Claude either. See [`docs/testing.md`](docs/testing.md#the-gate-must-be-deterministic).

### Project-specific deviations

- **No board, no milestones, no CI.** Permitted by the `core` profile; the gate is local.
- **The repo documents its own process**, so `CLAUDE.md` deliberately does not restate the workflow the way a consuming project's would. It links inward instead of outward.

### Architecture Decisions

This repo has no `docs/adr/` yet. Its structural decisions are recorded in `CHANGELOG.md` and in `docs/consumption.md`. Add `docs/adr/` at the first decision that meets the [threshold rule](docs/adrs.md#threshold-rule--when-to-write-one).
