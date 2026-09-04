# Release Management

> **Profile:** core — applies to every project. See [profiles.md](profiles.md).

How to go from "code is verified" to "users have it." This covers versioning, release checklists, changelogs, and hotfixes for a sole developer.

---

## Release Models

Not every project releases the same way. Pick the model that matches your deployment:

| Model | When to use | Example |
|-------|-------------|---------|
| **Continuous** | Every merge to `main` goes live automatically | Static sites, Netlify/Vercel apps, SaaS with CI/CD |
| **Batched** | You accumulate verified work, then ship a version | Mobile apps, CLIs, libraries, anything with "users on old versions" |
| **Manual** | You decide when to push a button | Side projects, early-stage apps, anything without CI/CD |

Most sole-dev projects start as **Manual** and graduate to **Continuous** as CI/CD matures. **Batched** is for projects where users control when they update.

> The rest of this doc applies to all three models. The differences are in *when* you run the checklist, not *what's on it*.

---

## Versioning

### When to version

Version when users can be on different copies of your software — anything downloaded, installed, or uploaded as an artifact: games, desktop apps, CLIs, libraries, store builds. The version is the shared vocabulary between you, your users, and your bug reports ("which build are you on?").

One carve-out: a **continuously deployed service** (core+ops) may skip version numbers. Every merge to `main` is live, so the commit SHA and deploy timestamp identify a release. If that's you, skip to the [Release Checklist](#release-checklist).

### The version: `MAJOR.MINOR.PATCH`

Keep the familiar shape. Define the bumps by **what the consumer experiences** — API compatibility is the right lens only when the consumer is a program.

| Bump | Libraries and CLIs ([semver](https://semver.org/)) | Apps and games |
|------|-----------------------------------------------------|----------------|
| **MAJOR** | Breaking API or CLI change | The user would call it a different product, **or** saved data / file formats no longer load |
| **MINOR** | New capability, backward compatible | New user-visible content or capability; saved data still works |
| **PATCH** | Bug fix, no new behavior | Fixes and tuning; nothing new to discover |

**1.0 is a declaration, not a threshold you drift across.** 1.0 means "the version you'd hand a stranger with no caveats." Before that it is 0.x, however many features it has. Bumping to 1.0 is a decision — record it in the changelog like any other.

[Calendar versioning](https://calver.org/) (`YYYY.MM.PATCH`) remains valid for apps where compatibility is never a question and "how recent is this?" is all a version needs to say.

### The build number

Projects that ship artifacts — zips, installers, store builds — also keep a **build number**: a monotonic integer that identifies one artifact and never resets. The version says what changed; the build says which file. Show them together: `1.2.0 (build 36)`.

- Every artifact that goes out the door gets the next number — hotfixes and re-cuts included.
- A version spans many builds (`0.9.0 (build 31)` … `0.9.0 (build 34)`); a build never spans versions.
- Put it on the title screen, about box, or `--version` output, so a bug-report screenshot identifies the exact artifact.
- Continuously deployed services don't need one — the commit SHA is their build number.

### Single source of truth

Exactly **one** machine-readable place holds the version (and the build number, if used):

| Project | Version | Build number |
|---------|---------|--------------|
| npm / Node | `package.json` → `version` | `package.json` → `config.build`, or a `BUILD` file |
| Rust | `Cargo.toml` → `version` | a `BUILD` file |
| Anything else | a `VERSION` file at the repo root | a `BUILD` file |

Everything else is **derived** from it by the release script: the constant the app displays, the git tag, the changelog header, the artifact filename. A no-build-step project stamps the constant into the source at release time (read the source of truth, write the constant, commit both in the release commit). Nothing is hand-edited in two places.

> **The anti-pattern: two sources, one stale.** A `version` in `package.json` *and* a `VERSION = '1.1.0'` in the code, both edited by hand, will disagree within a month — and the one users see will be the wrong one. If a human has to remember to update a second place, the second place is already wrong.

### Tagging

```bash
# Version tag — annotated, from main
git tag -a v1.2.0 -m "v1.2.0: Add search filtering, fix mobile layout"
git push origin v1.2.0

# Artifact projects: also tag the build, so a reported build number maps straight to a commit
git tag -a build-36 -m "build 36 (v1.2.0)"
git push origin build-36
```

Tag from `main` after all issues for the release are in **Done**. Never tag from a feature branch. Let the release script create tags from the source of truth — a hand-typed tag is the second source you just promised not to have.

---

## Release Checklist

Run this before declaring a release. For continuous-deploy projects, this is your "pre-merge sanity check" on the last PR in a batch of related work.

### Pre-release

- [ ] **All target issues are Done** — every issue tagged for this milestone is closed and verified (or, without milestones, every issue you meant to ship)
- [ ] **No open blockers** — check `priority:high` issues; none should be unresolved
- [ ] **The gate passes** — local test command (core) or CI (core+ops) is green; manual verification complete
- [ ] **Documentation is current** — spec, CLAUDE.md, and README reflect the shipped state
- [ ] **CHANGELOG updated** — new entry describes what changed (see [Changelog](#changelog) below)
- [ ] **No orphaned branches** — feature branches for shipped work are deleted

### Release

- [ ] **Tag created** (if versioned) — annotated tag on `main`
- [ ] **GitHub Release created** (if versioned) — with changelog body
- [ ] **Deployed** — to production environment (however that works for your project)
- [ ] **Milestone closed** (if you use milestones) — in GitHub, close the milestone for this release

### Post-release

- [ ] **Smoke test production** — verify the critical path works in the live environment
- [ ] **Announce if needed** — update users, stakeholders, or yourself (a note in the issue tracker is fine)

---

## Changelog

Every project should have a `CHANGELOG.md`. It answers the question users and future-you will ask: "what changed?"

### Format

Follow [Keep a Changelog](https://keepachangelog.com/) loosely:

```markdown
# Changelog

## [Unreleased]

### Added
- Search now filters by neighborhood (#45)

### Fixed
- Mobile layout overflow on venue detail page (#42)

## [1.1.0] - 2026-06-01

### Added
- Dark mode toggle (#38)

### Changed
- Venue cards now lazy-load images (#36)
```

### Sections

Use whichever apply: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.

### Rules

1. **Write entries as you close issues**, not all at once before release. The `[Unreleased]` section accumulates throughout development.
2. **Reference issue numbers.** `(#42)` links the entry to the decision that authorized it.
3. **Write for users, not developers.** "Search now filters by neighborhood" beats "Refactored SearchService to accept filter params."
4. **When you release**, move `[Unreleased]` entries into a new versioned section and add a fresh `[Unreleased]` header.

For continuous-deploy projects without version numbers, date-stamp sections instead:

```markdown
## 2026-06-04

### Added
- Search filtering by neighborhood (#45)
```

---

## GitHub Releases

For versioned projects, GitHub Releases give you a landing page per version with download links and release notes.

```bash
# Create a release from an existing tag
gh release create v1.2.0 \
  --title "v1.2.0" \
  --notes-file CHANGELOG.md \
  --latest

# Or write notes inline
gh release create v1.2.0 \
  --title "v1.2.0: Search and mobile fixes" \
  --notes "See CHANGELOG.md for details."
```

> **Tip:** `--notes-file` reads the whole file. For a cleaner release page, extract just the relevant version section into a temp file, or write the notes inline with `--notes`.

### When to use GitHub Releases

| Project type | Use GitHub Releases? |
|-------------|---------------------|
| Library / CLI (published) | Yes — users find releases here |
| Web app (continuous deploy) | Optional — git log and CHANGELOG.md are usually enough |
| Mobile app | Yes — link to app store submission |
| Side project | Optional — CHANGELOG.md alone is fine |

---

## Hotfixes

When something breaks in production and can't wait for the normal workflow:

### Process

1. **Create a `bug` issue** — even for hotfixes, ticket-first. Label it `priority:high`.
2. **Branch from `main`** — `fix/critical-search-crash`
3. **Fix, test, PR** — compress the workflow (Steps 2-4 become a quick triage comment on the issue)
4. **Merge and deploy** — don't wait for a batched release
5. **Update the changelog** — add the fix to `[Unreleased]` (or the current date section)
6. **Tag a patch version** (if versioned) — `v1.2.1`
7. **Postmortem** (optional but recommended) — a single comment on the issue: what broke, why, what prevents recurrence

### What makes a hotfix

A hotfix is justified when:
- Production is broken for users (Critical or High severity)
- A security vulnerability is exposed
- Data integrity is at risk

Everything else goes through the normal workflow. "It's annoying" is not a hotfix.

---

## Milestones

Milestones group issues into a release or a logical batch of work.

### When to create milestones

- **Versioned projects:** one milestone per planned release (`v1.2.0`, `v2.0.0`)
- **Continuous deploy:** one milestone per logical initiative ("Search & Filtering", "Mobile Optimization")
- **Don't create milestones speculatively.** A milestone with 0 issues is noise.

### Milestone lifecycle

```
Create → Assign issues → Work through them → All issues Done → Close milestone
```

```bash
# Create
gh api repos/{owner}/{repo}/milestones -f title="v1.2.0" -f description="Search and mobile fixes"

# Close when all issues are done
gh api repos/{owner}/{repo}/milestones/{number} -X PATCH -f state="closed"
```

### Scope management

Milestones resist scope creep because they're visible:

- **Adding an issue to a milestone** is a conscious decision (PO hat)
- **Removing an issue** is also visible — bump it to the next milestone, don't just unassign it
- **Milestone progress** shows in the GitHub UI — X of Y issues closed

If a milestone keeps growing, split it. Two focused milestones ship faster than one sprawling one.

---

## How This Fits the Workflow

Release management extends the 7-step workflow with what happens *after* Step 7 (Verify):

```
Steps 1-7 (per issue) → Issues accumulate in Done → Release checklist → Tag/deploy → Milestone closed
```

| Existing concept | Release connection |
|-----------------|-------------------|
| **Done column** | Issues accumulate here until a release |
| **Milestones** | Group issues into releases |
| **CHANGELOG.md** | Entries written as issues close, formalized at release time |
| **Commit conventions** | `#XX:` references connect release notes to decisions |
| **Hotfix** | Compressed workflow for urgent production fixes |

---

## Recommended First Steps

If you're adding release discipline to a project for the first time:

1. **Create a `CHANGELOG.md`** with an `[Unreleased]` section
2. **Start writing entries** as you close issues
3. **Add milestones** to group related work
4. That's it. Add tagging and GitHub Releases when the project warrants it.

The goal is traceability — being able to answer "what changed and why" at any point in time — not ceremony.
