# CI/CD

Continuous Integration and Continuous Deployment for a sole developer. This covers when to add automation, what to automate, GitHub Actions basics, and starter workflows.

---

## Why CI/CD for a Solo Dev

CI/CD isn't about team coordination — it's about catching mistakes before they reach production.

Without CI/CD, the sole-dev failure mode is:
1. Push code that works locally
2. Forget a dependency, env var, or build step
3. Production breaks
4. Scramble to rollback while figuring out what went wrong

CI/CD turns "I hope this works" into "I know this works" before it ships.

---

## When to Add It

CI/CD has a setup cost. Don't pay it on day one. Add automation when the pain justifies it:

| Signal | What to add |
|--------|------------|
| You've forgotten to run tests before pushing more than twice | **CI: run tests on PR** |
| A lint or formatting issue slipped into production | **CI: lint on PR** |
| You've broken a build by forgetting a dependency | **CI: build check on PR** |
| Deploying involves more than one manual step | **CD: auto-deploy on merge** |
| You want preview URLs for PRs | **CD: preview deploys** |
| You've shipped a security vulnerability in a dependency | **CI: dependency audit** |

Start with **one job that runs on pull requests** — typically lint + test. Add more as you learn what breaks.

---

## Pipeline Stages

A CI/CD pipeline is a sequence of automated checks and actions. Here's the typical progression, from least to most mature:

### Stage 1: Check (CI — start here)

Runs on every pull request. Blocks merge if it fails.

```
PR opened → Install deps → Lint → Build → Test → Report
```

**Goal:** "This code is safe to merge."

### Stage 2: Deploy (CD — add when ready)

Runs when code lands on `main`. Pushes to production.

```
Merge to main → Install deps → Build → Deploy → Smoke test
```

**Goal:** "Merged code is live."

### Stage 3: Gate (CD — for versioned releases)

Runs when a tag is pushed. Publishes a release.

```
Tag pushed → Install deps → Build → Test → Publish/Deploy → GitHub Release
```

**Goal:** "This version is shipped."

> Most sole-dev projects only need Stage 1 + Stage 2. Stage 3 is for libraries, CLIs, and apps with explicit versioning.

---

## GitHub Actions Basics

GitHub Actions is the CI/CD system built into GitHub. Workflows are YAML files in `.github/workflows/`.

### Key concepts

| Concept | What it is |
|---------|-----------|
| **Workflow** | A YAML file that defines what to automate (`.github/workflows/ci.yml`) |
| **Trigger** | What starts the workflow (`push`, `pull_request`, tag creation, manual) |
| **Job** | A group of steps that run on the same machine |
| **Step** | A single command or action within a job |
| **Action** | A reusable step published by GitHub or the community (`actions/checkout`, `actions/setup-node`) |
| **Secret** | An encrypted variable available to workflows (`${{ secrets.API_KEY }}`) |

### How it runs

```
Trigger fires → GitHub spins up a fresh VM → Runs your steps → Reports pass/fail
```

Every run starts clean — no leftover state from previous runs. This is a feature: if it passes in CI, it'll pass anywhere.

---

## Starter Workflows

Copy one of these into `.github/workflows/ci.yml` and customize. Each is a minimal starting point, not a production-hardened pipeline.

### Node.js (JavaScript/TypeScript)

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - run: npm ci

      - run: npm run lint
        # Remove this step if you don't have a lint script yet

      - run: npm run build
        # Remove this step if there's no build step

      - run: npm test
        # Remove this step if you don't have tests yet
```

### Python

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - run: pip install -r requirements.txt

      - run: python -m pytest
```

### Static site (HTML/CSS/JS, no build step)

```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check for broken links
        uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress './**/*.html'
          fail: true
```

> **Strip what you don't need.** A workflow with just `checkout` + `npm test` is better than a complex pipeline you copied from a blog post and don't understand.

---

## Common Additions

Add these to your starter workflow as needs arise:

### Dependency caching

Already included in the starters above via `cache: npm` / `cache: pip`. This skips re-downloading packages on every run, cutting minutes off your pipeline.

### Auto-deploy on merge to main

Add a second job that runs only on `main` pushes:

```yaml
  deploy:
    needs: check
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Platform-specific deploy step goes here
```

Most hosting platforms (Vercel, Netlify, Railway) handle deploy automatically when you connect your repo — you may not need this job at all.

### Dependency audit

Check for known vulnerabilities in your dependencies:

```yaml
      - name: Audit dependencies
        run: npm audit --audit-level=high
```

### Tag-triggered release

Publish when you push a version tag:

```yaml
on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
      - run: npm test
      - uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

---

## Branch Protection

Once you have CI, use it as a gate. In your repo settings:

**Settings → Branches → Branch protection rules → Add rule for `main`:**

- [x] Require status checks to pass before merging
- [x] Require branches to be up to date before merging
- Select your CI job name (e.g., "check")

This prevents merging a PR that fails CI. For a sole developer, this is the single most valuable branch protection rule — it stops you from merging broken code in a moment of impatience.

### Other branch protection options (add as needed)

| Rule | Worth it for solo dev? |
|------|----------------------|
| Require status checks | **Yes** — this is the whole point |
| Require PR reviews | No — you're the only reviewer |
| Require signed commits | Optional — good security hygiene, some setup cost |
| Require linear history | Optional — keeps git log clean, minor convenience |
| Restrict force pushes | Yes — protects against accidental `git push --force` to main |

---

## Secrets in CI

For workflows that deploy or access external services, you need secrets.

### Setting secrets

```bash
# Repository secret (available to all workflows in this repo)
gh secret set API_KEY

# Environment secret (scoped to a specific environment)
gh secret set API_KEY --env production
```

### Using secrets in workflows

```yaml
    steps:
      - name: Deploy
        run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

### Rules

1. **Never print secrets in logs.** GitHub masks them automatically, but avoid `echo $API_KEY` anyway.
2. **Never hardcode secrets in workflow files.** That's what `gh secret set` is for.
3. **Secrets aren't available in PRs from forks.** This is a security feature — fork PRs can't steal your secrets.
4. **Rotate secrets on the same schedule as production secrets.** CI secrets are production-adjacent — treat them accordingly.

---

## When NOT to Automate

Not everything belongs in CI:

| Task | CI? | Why not? |
|------|-----|----------|
| Running the full test suite | Yes | This is CI's primary job |
| Linting / formatting | Yes | Catches style issues before merge |
| Building the project | Yes | Catches dependency and compilation errors |
| Database migrations | **No** | Too risky to automate without review — run manually with the deploy |
| Manual QA verification | **No** | The Verify column exists because humans catch what automation misses |
| Performance testing | Maybe | Only if you have benchmarks; otherwise it's noise |
| Security scans | Yes (lightweight) | `npm audit` is cheap; full SAST tools have high false-positive rates |

---

## Debugging Failed Workflows

When CI fails:

1. **Read the error message.** Click the failed job → expand the failed step → read the output. Most CI failures have clear error messages.
2. **Reproduce locally.** Run the same command that failed (`npm test`, `npm run lint`) on your machine. If it passes locally but fails in CI, the difference is your environment.
3. **Check environment differences.** CI runs on a clean Ubuntu VM. Common gotchas:
   - Case-sensitive filesystem (Linux) vs case-insensitive (macOS/Windows)
   - Missing environment variables
   - Different Node/Python version than local
4. **Check the trigger.** Is the workflow running on the right event? `pull_request` vs `push` matters.

---

## How This Fits the Workflow

CI/CD automates the guardrails that the workflow relies on:

| Workflow concept | CI/CD automation |
|-----------------|-----------------|
| **Step 5 (Implement)** | CI runs on the PR — lint, build, test |
| **Step 7 (Verify)** | CI passes before the human verifier sees it — no wasted QA time on broken builds |
| **Definition of Done** | "Tests pass" becomes verifiable, not just a checkbox |
| **Deploy** | CD handles the [deployment](deployment.md) after merge |
| **Release** | Tag-triggered CD handles the [release](release-management.md) publish |
| **Hotfix** | Same pipeline, same checks — hotfixes don't skip CI |

```
PR opened → CI checks (auto) → Human verification (manual) → Merge → CD deploys (auto)
```

---

## Recommended First Steps

1. **Copy a starter workflow** from above into `.github/workflows/ci.yml`
2. **Strip it down** to only the steps your project actually has (if you don't have tests, remove the test step — don't leave it as a failing placeholder)
3. **Push it and open a PR** — verify that CI runs and reports status
4. **Enable branch protection** — require the status check to pass before merge
5. **Add steps** as you add linting, testing, and deploy automation to your project

Don't try to build the perfect pipeline upfront. A CI that runs `npm test` on PRs is infinitely better than a planned-but-never-built pipeline that does everything.
