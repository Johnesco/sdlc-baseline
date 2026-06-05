# Testing Strategy

How to think about testing for a sole developer. This document helps you decide *what* to test and *when* to add automation. For *how* to wire tests into a CI pipeline, see [`ci-cd.md`](ci-cd.md).

---

## The Baseline

This SDLC does not prescribe a testing framework. The **Verify** column in the workflow is human-owned manual verification — that's the minimum viable testing strategy and it works for small projects.

As a project grows, supplement manual verification with automated tests. This document helps you plan that transition.

Even without automated tests, this process gives you:

- **Manual test steps** in the Test Plan field of feature issues
- **Human verification** in the Verify column (QA role)
- **Definition of Done** checklists that include regression checking
- **CI enforcement** when you're ready — see [`ci-cd.md`](ci-cd.md)

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

| Trigger | What Runs | Purpose |
|---------|-----------|---------|
| Before commit (pre-commit hook) | Linting, formatting | Catch style issues early |
| Before push (pre-push hook) | Unit tests | Catch broken logic before sharing |
| On PR (CI) | All tests | Gate merges on passing tests |
| On merge to main (CI) | All tests + deploy | Final safety net |

**Decision:** Start with "run tests manually" and add automation when the pain of forgetting justifies the setup cost. See [`ci-cd.md`](ci-cd.md) for how to wire tests into a GitHub Actions pipeline.

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
- [ ] CI passes (if configured)
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
6. **Add CI** when you have ~10 tests and want to stop running them manually — see [`ci-cd.md`](ci-cd.md)

The goal is to build the habit, not to achieve coverage.

---

## This Doc + CI/CD

Testing strategy and CI/CD are complementary:

| This doc (`testing.md`) | CI/CD doc (`ci-cd.md`) |
|------------------------|----------------------|
| *What* to test | *How* to automate the checks |
| *Which* framework to pick | *Where* the framework runs (GitHub Actions) |
| *When* to add tests (project maturity) | *When* to add CI (pain threshold) |
| Coverage decisions | Branch protection and gating |

Read this doc first to decide your testing approach. Then read [`ci-cd.md`](ci-cd.md) to automate it.
