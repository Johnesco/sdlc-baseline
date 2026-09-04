# Testing Strategy

> **Profile:** core — applies to every project. See [profiles.md](profiles.md).

How to think about testing for a sole developer. This document helps you decide *what* to test and *when* to add automation. For *how* to wire tests into a CI pipeline (core+ops), see [`ci-cd.md`](ci-cd.md). Core projects need only the local gate below.

---

## The Baseline

This SDLC does not prescribe a testing framework. The **Verify** column in the workflow is human-owned manual verification — that's the minimum viable testing strategy and it works for small projects.

As a project grows, supplement manual verification with automated tests. This document helps you plan that transition.

Even without automated tests, this process gives you:

- **Manual test steps** in the Test Plan field of feature issues
- **Human verification** in the Verify column (QA role)
- **Definition of Done** checklists that include regression checking
- **A gate** — the local test command (core), or CI (core+ops — see [`ci-cd.md`](ci-cd.md)). It must be deterministic: no model, no network, a real exit code

---

## The local gate (core)

Core projects have no CI to stop a bad release. The gate is **one command, run locally**:

1. **Name it.** `npm test` (or `make test`, `cargo test`, `pytest`) runs everything that counts. One entry point — nobody should have to remember which scripts matter.
2. **It must pass before a release tag.** No green gate, no tag, no artifact. Let the release script run it and refuse to cut a build when it fails.
3. **Run it on request, not on every commit.** Before a release, after touching anything the suite covers, or when the human asks. The point is that it is impossible to *ship* without it — not that it runs constantly.
4. **Say what you ran.** The Definition of Done asks how "no regressions" was verified. "Ran `npm test`, 17 suites green" is an answer; "should be fine" is not.

That's the whole gate. When the project grows a service, CI runs the same command — see [`ci-cd.md`](ci-cd.md).

### The gate must be deterministic

A gate that needs judgment is not a gate. Whatever the command runs, it has to
give the same answer on the same input, every time, with nothing in the loop
that can have an opinion:

- **No model.** An AI assistant is a superb reviewer and a worthless gate. It
  cannot be a check on its own work — that is the same rule as *Claude
  cannot QA its own work*, applied one level up. "I read it and it looked fine"
  is not a passing test, whoever said it.
- **No network.** A check that fails when the wifi drops trains you to ignore
  failures, and an ignored gate is no gate.
- **No clock, no randomness, no machine-specific paths.** A test that behaves
  differently on Tuesday or on someone else's laptop is worse than no test,
  because it produces failures you learn to wave through.
- **A real exit code.** 0 or non-zero. Anything that only prints is advice.

The payoff is that red always means something changed. You never have to wonder
whether the gate is having a bad day, so you never develop the habit of
re-running it until it passes.

### When the project isn't code

Prose, schemas and configuration have contracts too, and they rot in silence
because nothing compiles them. Ask what would break someone else if it changed
without anyone noticing, then assert exactly that.

This repository is the worked example. `python scripts/check-docs.py` is its
whole gate, and it asserts things a careful reader misses:

| Check | The failure it prevents |
|-------|-------------------------|
| Links and anchors resolve | A standard nobody can navigate |
| No orphaned files | A doc that sat unreferenced for months |
| Profile badge on line 3 of every doc | The profile mechanism silently not applying |
| The published URL contract still exists | Renaming a heading 404s links in *other people's repos*, with no error anywhere |
| Two copies of the severity strings agree | Duplication GitHub forces, drifting apart |
| No machine paths, frozen dates, pinned model names | Things that have shipped from here before |

None of that needs a test framework. It needs one script, in whatever language
is already on the machine, that exits non-zero when an invariant breaks.

**The rule of thumb:** every time you write down a rule, ask whether a script
could check it. If it can and you don't, the rule has already started drifting —
you just won't find out for a few months.

---

## Decisions to Make Per Project

### 1. What to test

| Layer | Examples | Worth Testing? |
|-------|----------|---------------|
| **Unit** | Pure functions, utilities, data transforms | Almost always yes |
| **Integration** | Components working together, API + database | Yes for backend, depends for frontend |
| **End-to-end** | Full user flows in a browser | High value but high maintenance |
| **Visual/Snapshot** | UI doesn't change unexpectedly | Good for component libraries |

**Decision:** Which layers give you the most confidence for the least maintenance?

### 2. What framework to use

| Project Type | Common Choices |
|-------------|----------------|
| Vanilla JS (browser) | Vitest, Jest (with jsdom), Playwright (E2E) |
| Node.js backend | Vitest, Jest, Mocha, built-in `node:test` |
| React/Vue/Svelte | Vitest + Testing Library, Playwright |
| Python | pytest |
| Go | Built-in `testing` package |
| CLI tools | Bats (bash), the tool's native test runner |

**Decision:** Pick one. Don't overthink it. The best framework is the one you'll actually use.

### 3. When to run tests

| Trigger | What runs | Profile |
|---------|-----------|---------|
| On request — before a release tag, after touching covered code, when asked | The local gate | core (required) |
| Before commit / push (git hooks) | Lint, formatting, unit tests | either (optional) |
| On PR (CI) | All tests | core+ops |
| On merge to main (CI) | All tests + deploy | core+ops |

**Decision:** Core projects stop at the first row and let the release script enforce it. Add CI when the project runs a service — see [`ci-cd.md`](ci-cd.md).

### 4. What coverage target

| Level | Meaning |
|-------|---------|
| 0% | No automated tests (current state for many projects) |
| ~50% | Core logic covered, UI mostly manual |
| ~80% | Good coverage, diminishing returns beyond this |
| 100% | Almost never worth the effort |

**Decision:** Don't set a coverage target until you have at least 20 tests. Coverage targets without tests are aspirational fiction.

---

## Adding Testing to This Workflow

When you're ready to add testing, here's how it fits into the existing process:

### Definition of Done (updated)

Add to the feature and bug DoD checklists:

```
- [ ] Tests added or updated for changed behavior
- [ ] All existing tests still pass
```

### Issue templates (updated)

The feature template already has a **Test Plan** field. Use it to describe what tests you'll write, not just manual verification steps.

### PR template (updated)

The testing checklist in the PR template can be expanded:

```
- [ ] New tests written for this change
- [ ] All tests pass locally
- [ ] The gate passes (local test command; CI for core+ops)
```

### Commit conventions

No change needed — test code follows the same `#XX: description` convention.

---

## Recommended First Steps

If you're adding tests to a project for the first time:

1. **Pick one framework** and install it
2. **Write one test** for your most important utility function
3. **Add a `test` script** to your `package.json` / `Makefile` / equivalent
4. **Run it** — if it passes, you have a test suite
5. **Add tests to new code** going forward (don't try to retroactively test everything)
6. **Wire the gate** — core: make the `test` script the one command and have the release script run it; core+ops: add CI — see [`ci-cd.md`](ci-cd.md)

The goal is to build the habit, not to achieve coverage.

---

## This Doc + the Gate

Testing strategy is core; automating it in CI is ops:

| This doc (`testing.md`) | CI/CD doc (`ci-cd.md`) |
|------------------------|----------------------|
| *What* to test | *How* to automate the checks |
| *Which* framework to pick | *Where* the framework runs (GitHub Actions) |
| *When* to add tests (project maturity) | *When* to add CI (pain threshold) |
| Coverage decisions | Branch protection and gating |

Read this doc first. Core projects then wire the local gate (above). Core+ops projects read [`ci-cd.md`](ci-cd.md) to automate it.
