# Changelog

> Downstream projects link to sdlc-baseline `main` for canonical process docs (see [`docs/consumption.md`](docs/consumption.md)). This file is the **human-facing signal** for changes that may affect those projects.
>
> Format loosely follows [Keep a Changelog](https://keepachangelog.com/). Conventions:
> - Sections: **Added** / **Changed** / **Deprecated** / **Removed** / **Fixed** / **Process**.
> - Entries are written from the perspective of a downstream project deciding whether to take action.

---

## [Unreleased]

### Added
- `docs/release-management.md` — versioning, release checklists, changelogs, hotfixes, and milestone lifecycle. Closes the gap between "code verified" and "users have it."
- `docs/deployment.md` — deploy patterns, environment model, config/secrets management, rollback protocol, platform guidance. Covers the "how code gets to production" leg of the SDLC.
- `docs/ci-cd.md` — CI/CD for a sole developer. Pipeline stages, GitHub Actions basics, starter workflows (Node.js, Python, static site), branch protection, secrets in CI, debugging failures. Provides the automation layer connecting the ticket-first workflow to deployment.
- `docs/backlog-hygiene.md` — review cadence (weekly/monthly/quarterly), grooming tactics, backlog size guidance, planning without sprints. Prevents the "200 open issues, no idea what to work on" failure mode.
- `docs/incident-response.md` — the 6-step sequence (detect → assess → restore → communicate → investigate → prevent), rollback-vs-fix-forward decision guide, postmortem template, sole-dev monitoring recommendations.
- `docs/kickoff-checklist.md` — step-by-step day-1 setup guide for new projects and existing-project adoption. Connects all docs into a phased sequence: repo structure → project management → deployment → CI/CD.
- `docs/consumption.md` — vendored vs referenced vs project-only model for downstream projects.
- `CHANGELOG.md` — this file.
- `scripts/sync-github-templates.sh` — helper that downstream projects can run to pull the latest GitHub-tooling-bound files (issue templates, PR template, label setup script).

### Changed
- `CLAUDE-TEMPLATE.md` slimmed from ~262 to ~80 lines. Universal process content is now linked from canonical docs rather than embedded inline. Projects copying this template now get a thin, project-specific shape by default.
- `examples/CLAUDE-example.md` updated to demonstrate the slim shape.
- `README.md` artifact table annotated by category (vendored / referenced / template).

### Process
- Established that sdlc-baseline is a **library, not a starter kit**. See [`docs/consumption.md`](docs/consumption.md). Downstream projects should reference canonical docs rather than vendor copies.

---

## [v0.4.0] — 2026-04-30

### Added
- ADR (Architecture Decision Record) protocol — `docs/adrs.md`, `examples/adr-template.md`, `examples/adr-example.md` (#2).
- Workflow Step 2 now references `docs/adr/` for prior architectural decisions.
- Workflow Step 6 now requires writing an ADR for decisions that meet the threshold rule.
- Definition of Done — Feature and Task checklists include an ADR item.

### Changed
- `CLAUDE-TEMPLATE.md` "Architecture Decisions" placeholder replaced with a pointer to `docs/adr/` and the protocol doc.
- `examples/CLAUDE-example.md` "Architecture Decisions" bullet list replaced with the pointer pattern.
- `README.md` artifact table includes `docs/adrs.md`, `examples/adr-template.md`, and `examples/adr-example.md`.

---

## [v0.3.0]

### Changed
- Renamed `chore` issue type to `task` for clarity.
- Added `spike` issue type for research / investigation tickets.
- Collapsed Backlog + Refining columns into a single Backlog column with refinement happening inline.

---

## [v0.2.0]

### Added
- Resolution labels (`resolution:wontfix`, `resolution:duplicate`, `resolution:cannot-reproduce`, `resolution:by-design`, `resolution:stale`, `resolution:superseded`) for closing issues without completing the work.
- Resolution label documentation in `CLAUDE-TEMPLATE.md`, `examples/CLAUDE-example.md`, and `README.md`.

---

## [v0.1.0]

### Added
- Initial process release: 7-step ticket-first workflow, role definitions, board column model, label taxonomy, issue templates, PR template, label setup script.

---

## How to update this file

Every PR to `main` that changes consumer-visible behavior (docs in `docs/`, templates in `examples/`, files in `.github/`, scripts that downstream projects run) should add an entry to **[Unreleased]**. When a release is cut, the [Unreleased] section becomes the new versioned section and a fresh [Unreleased] is added at the top.

For now, "release" is informal — entries accumulate under [Unreleased] until enough has changed to warrant a version bump and an announcement to downstream projects (currently just karaokedirectory).
