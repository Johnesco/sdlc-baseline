# Release Management

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

Use explicit versions (tags + GitHub Releases) when **any** of these are true:

- Users can be on different versions (libraries, CLIs, mobile apps)
- You need to point someone at "what changed since you last updated"
- You want a rollback target ("go back to v1.3.2")
- Your deployment pipeline consumes a tag

If none apply — e.g., a web app deployed on every merge — **you don't need version numbers**. Git SHAs and deploy timestamps are enough. Skip to the [Release Checklist](#release-checklist).

### Versioning scheme

Use [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`) for libraries and CLIs. Use [Calendar Versioning](https://calver.org/) (`YYYY.MM.DD` or `YYYY.MM.PATCH`) for apps where "compatibility" isn't meaningful.

For a sole developer, the practical distinction:

| Change type | Semver | Calver |
|-------------|--------|--------|
| Breaking change | Bump MAJOR | Just ship it (date changes) |
| New feature | Bump MINOR | Just ship it |
| Bug fix | Bump PATCH | Just ship it |

Semver forces you to think about compatibility. Calver forces you to ship. Pick based on whether your users need to reason about upgrade safety.

### Tagging

```bash
# Create an annotated tag
git tag -a v1.2.0 -m "v1.2.0: Add search filtering, fix mobile layout"

# Push the tag
git push origin v1.2.0
```

Tag from `main` after all issues for the release are in **Done**. Never tag from a feature branch.

---

## Release Checklist

Run this before declaring a release. For continuous-deploy projects, this is your "pre-merge sanity check" on the last PR in a batch of related work.

### Pre-release

- [ ] **All target issues are Done** — every issue tagged for this milestone is closed and verified
- [ ] **No open blockers** — check `priority:high` issues; none should be unresolved
- [ ] **Tests pass** — automated suite (if any) is green; manual verification complete
- [ ] **Documentation is current** — spec, CLAUDE.md, and README reflect the shipped state
- [ ] **CHANGELOG updated** — new entry describes what changed (see [Changelog](#changelog) below)
- [ ] **No orphaned branches** — feature branches for shipped work are deleted

### Release

- [ ] **Tag created** (if versioned) — annotated tag on `main`
- [ ] **GitHub Release created** (if versioned) — with changelog body
- [ ] **Deployed** — to production environment (however that works for your project)
- [ ] **Milestone closed** — in GitHub, close the milestone for this release

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
