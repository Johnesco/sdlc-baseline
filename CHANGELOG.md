# Changelog

> Downstream projects link to sdlc-baseline `main` for canonical process docs (see [`docs/consumption.md`](docs/consumption.md)). This file is the **human-facing signal** for changes that may affect those projects.
>
> Format loosely follows [Keep a Changelog](https://keepachangelog.com/). Conventions:
> - Sections: **Added** / **Changed** / **Deprecated** / **Removed** / **Fixed** / **Process**.
> - Entries are written from the perspective of a downstream project deciding whether to take action.

---

## [Unreleased]

_(nothing yet)_

---

## [v0.5.0] — 2026-09-03

> **Downstream in one line:** add `**SDLC profile:** core` (or `core+ops`) under "Working in this project" in your CLAUDE.md. Undeclared = core. Nothing moved; every existing link and anchor still resolves.

### Added
- **`docs/start-here.html`** — an orientation page for anyone who has not worked inside a formal SDLC before: why process pays for a solo developer (with the real numbers from a project that lost 8 features to building before deciding), the seven-step loop drawn with the gate in it, the three non-negotiables, the hat-switch model, a staged first week, a which-doc-when index, explicit permission to skip the board/PRs/milestones/CI, and what makes this standard different from a textbook one. Restates nothing — links out for every detail, per `consumption.md`.
- **Profiles.** Every doc in `docs/` carries a one-line badge: `core` (every project) or `ops` (only projects that run a service). `docs/profiles.md` is the manifest — what each profile contains, what core relaxes (board, PRs, milestones, CI) and what it keeps (ticket-first, DoD, ADRs, human Verify). Ops docs: `deployment.md`, `ci-cd.md`, `incident-response.md`. `security-basics.md` is core with server-only sections headed `(ops)`.
- **Decide before you build.** Anything above a tuning tweak gets a six-line ADR stub (Context + Decision) before code — `docs/adrs.md`, `docs/workflow.md` (gate between Steps 4 and 5), `examples/adr-stub.md`. The one new obligation in this release; it applies to both profiles.
- **ADR stub as ticket (core).** Workflow Step 1 accepts an Issue (always for bugs) or an ADR stub (for decisions); commits may reference `ADR-NNN:`.
- **The local gate.** `docs/testing.md` — core projects name one test command that must pass before a release tag; CI is the ops gate. Definition of Done rule 5 now reads "the gate must pass".
- **Build numbers and a single source of truth.** `docs/release-management.md` versioning rewritten: MAJOR/MINOR/PATCH defined by what the consumer experiences (separate columns for libraries vs apps/games); a monotonic build number for artifact projects (`1.2.0 (build 36)`, tag `build-N`); exactly one machine-readable place holds the version; 1.0 is a declaration.
- `CLAUDE-TEMPLATE.md` — profile declaration, `testing.md` and `profiles.md` links (testing was missing), ops link block marked for deletion in core projects, a third non-negotiable, a Releases placeholder.
- *(Docs added since v0.4.0 — retained entries follow.)*
- `docs/release-management.md` — versioning, release checklists, changelogs, hotfixes, and milestone lifecycle. Closes the gap between "code verified" and "users have it."
- `docs/deployment.md` — deploy patterns, environment model, config/secrets management, rollback protocol, platform guidance. Covers the "how code gets to production" leg of the SDLC.
- `docs/ci-cd.md` — CI/CD for a sole developer. Pipeline stages, GitHub Actions basics, starter workflows (Node.js, Python, static site), branch protection, secrets in CI, debugging failures. Provides the automation layer connecting the ticket-first workflow to deployment.
- `docs/backlog-hygiene.md` — review cadence (weekly/monthly/quarterly), grooming tactics, backlog size guidance, planning without sprints. Prevents the "200 open issues, no idea what to work on" failure mode.
- `docs/incident-response.md` — the 6-step sequence (detect → assess → restore → communicate → investigate → prevent), rollback-vs-fix-forward decision guide, postmortem template, sole-dev monitoring recommendations.
- `docs/kickoff-checklist.md` — step-by-step day-1 setup guide for new projects and existing-project adoption. Connects all docs into a phased sequence: repo structure → project management → deployment → CI/CD.
- `docs/security-basics.md` — secrets management, dependency auditing, common vulnerability prevention (XSS, injection, CSRF, IDOR), HTTPS/headers, auth guidance, security checklist for new projects.
- `docs/consumption.md` — vendored vs referenced vs project-only model for downstream projects.
- `CHANGELOG.md` — this file.
- `scripts/sync-github-templates.sh` — helper that downstream projects can run to pull the latest GitHub-tooling-bound files (issue templates, PR template, label setup script).

### Changed
- **Verification-first DoD.** "No regressions" rows require naming what was run and what was observed. "In the same PR" → "in the same change"; "In pull requests" → "If you use pull requests".
- **Board, milestones and PRs are optional in core** — `workflow.md`, `board-setup.md`, `kickoff-checklist.md`, `commit-conventions.md`, `roles.md`, `README.md`. The `gh project item-add` rule applies unchanged *if* you use a board.
- **`.github/ISSUE_TEMPLATE/bug.yml` (vendored — re-sync):** the four Severity option strings now match `docs/severity-matrix.md` verbatim. `severity-matrix.md` gains game-shaped examples; `incident-response.md` maps its triage words onto the matrix.
- `README.md` — artifact table split into Core / Ops / Vendored; board steps conditional; `scripts/sync-github-templates.sh` typed Vendored (was Template in README, Vendored in kickoff); "Tested in Production" credits the second source project.
- `docs/consumption.md` — reference table and CLAUDE.md sketch include `testing.md` and `profiles.md`; profiles noted as the evolution of the model.
- `examples/CLAUDE-example.md` — now a core-profile example, trimmed; illustrative ADR links are plain text.
- `docs/kickoff-checklist.md` — Quick Launch asks for the profile; Phase 1 names the test command, version source of truth and ADR index; Phases 3–4 labelled (ops).

### Fixed
- Broken links: `CLAUDE-TEMPLATE.md` `docs/adr/` and `examples/CLAUDE-example.md` ADR links pointed at files that don't exist in this repo; `definition-of-done.md` used `../docs/adrs.md#…` instead of `adrs.md#…`.
- Hardcoded values: a Windows path in `kickoff-checklist.md`, a date in `backlog-hygiene.md`, a model name in `commit-conventions.md`'s co-author trailer.
- This changelog claimed `CLAUDE-TEMPLATE.md` was ~80 lines (it was 117).

### Removed
- `docs/flow-visualization.html` — unlinked duplicate of the README workflow diagram.

### Changed (since v0.4.0)
- `CLAUDE-TEMPLATE.md` slimmed from ~262 to ~120 lines. Universal process content is now linked from canonical docs rather than embedded inline. Projects copying this template now get a thin, project-specific shape by default.
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

Every change to `main` that changes consumer-visible behavior (docs in `docs/`, templates in `examples/`, files in `.github/`, scripts that downstream projects run) should add an entry to **[Unreleased]**. When a release is cut, the [Unreleased] section becomes the new versioned section and a fresh [Unreleased] is added at the top.

For now, "release" is informal — entries accumulate under [Unreleased] until enough has changed to warrant a version bump and an announcement to downstream projects (karaokedirectory, singalong, ifhub).
