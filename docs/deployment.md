# Deployment

> **Profile:** ops — applies only to core+ops projects. See [profiles.md](profiles.md).

How to get code from your repository to a running environment. This covers deployment patterns, environment management, configuration, rollback, and smoke testing for a sole developer.

---

## Deployment Patterns

Pick the pattern that matches your project and comfort level:

| Pattern | How it works | Best for | Trade-off |
|---------|-------------|----------|-----------|
| **Push-to-deploy** | Merge to `main` triggers automatic deploy | Static sites, Vercel/Netlify/Cloudflare Pages, Heroku | Fast but no gate between merge and production |
| **Tag-triggered** | Creating a git tag triggers the deploy pipeline | Libraries, CLIs, mobile apps, anything with versions | Deliberate releases, but adds a manual step |
| **Manual** | You run a command or click a button to deploy | Early-stage projects, complex infrastructure | Full control, but easy to forget or deploy stale code |
| **PR preview** | Each PR gets a temporary preview environment | Frontend apps with visual changes | Great for verification, adds infrastructure cost |

Most sole-dev web projects should aim for **push-to-deploy** — it removes the "I forgot to deploy" failure mode. Graduate to **tag-triggered** when you need release gates.

> **Rule of thumb:** If deploying feels risky, you don't deploy often enough. If deploying feels boring, you've automated it well.

---

## Environments

### Do you need staging?

Probably not, at first.

| Setup | When it makes sense |
|-------|-------------------|
| **Production only** | Solo dev, small project, no paying users, push-to-deploy with good verification |
| **Production + Preview (per-PR)** | Frontend apps where you want to see changes before merge — many platforms offer this free |
| **Production + Staging** | Paying users, data migrations, third-party integrations you can't test locally, complex deploy steps |
| **Production + Staging + Dev** | Team projects, microservices, shared databases — usually overkill for solo dev |

Start with production only. Add a staging environment when you have a specific reason, not because "real projects have staging."

### Environment parity

Whatever environments you have, keep them as similar as possible:

- Same runtime versions (Node 20 in dev and prod, not Node 20 dev / Node 18 prod)
- Same environment variable names (different values are fine — `DATABASE_URL` should exist everywhere)
- Same build process (don't manually build for prod if CI builds for staging)

Differences between environments are a source of "works on my machine" bugs that survive all the way to production.

---

## Configuration and Secrets

### The rule

**Code is in the repo. Configuration is in the environment. Secrets are in the platform.**

| Category | Examples | Where it lives |
|----------|----------|---------------|
| **Code** | Application logic, templates, static assets | Git repository |
| **Configuration** | API base URLs, feature flags, log levels | Environment variables (`.env` locally, platform config in production) |
| **Secrets** | API keys, database credentials, auth tokens | Platform's secret store (Vercel env vars, GitHub Secrets, AWS SSM, etc.) |

### Local development

Use a `.env` file (or `.env.local`) for local configuration. **Never commit it.**

```bash
# .gitignore — this should already be here
.env
.env.local
.env*.local
```

Provide a `.env.example` file (committed) that documents every variable without real values:

```bash
# .env.example — committed, no real values
DATABASE_URL=postgresql://localhost:5432/myapp_dev
API_KEY=your-api-key-here
STRIPE_SECRET_KEY=sk_test_...
```

### Production secrets

Every hosting platform has a way to set environment variables securely:

```bash
# Vercel
vercel env add SECRET_NAME

# Heroku
heroku config:set SECRET_NAME=value

# GitHub Actions (for CI/CD — see ci-cd.md)
gh secret set SECRET_NAME
```

### Secret rotation checklist

When you need to rotate a secret (key compromised, employee leaves, periodic rotation):

- [ ] Generate new secret in the provider's dashboard
- [ ] Update the secret in your platform's environment configuration
- [ ] Verify the app works with the new secret
- [ ] Revoke the old secret
- [ ] Update `.env.example` if the variable name changed

---

## Deploy Checklist

A minimal list for every deploy. Expand it per-project as you learn what breaks.

### Before deploying

- [ ] `main` is green — tests pass (if CI exists), no known broken state
- [ ] Changes are verified — the work went through the Verify column
- [ ] Environment variables are set — any new config the deploy needs is already in the platform
- [ ] Database migrations run (if applicable) — before the new code tries to use new schema

### After deploying

- [ ] **Smoke test** — verify the critical path works in production (see below)
- [ ] Check error reporting — no new errors spiking in your monitoring (if any)
- [ ] Spot-check the change — the specific feature or fix you deployed actually works live

### Smoke test

A smoke test is not a full test suite. It's a 60-second check of the critical path:

1. Can the app load?
2. Can a user do the most important thing? (search, log in, submit a form, etc.)
3. Does the specific change you just deployed work?

If any of these fail, rollback immediately — investigate after.

---

## Rollback

When a deploy breaks production, the priority is **restore service first, investigate second**.

### Strategies by platform

| Platform type | Rollback method |
|--------------|----------------|
| **Vercel / Netlify / Cloudflare Pages** | Redeploy a previous deployment from the dashboard (instant) |
| **Heroku** | `heroku rollback` (reverts to previous release) |
| **Docker / container** | Redeploy the previous image tag |
| **VPS / manual deploy** | `git checkout <previous-tag>` and restart the service |
| **Tag-triggered CI** | Retag or redeploy the previous tag |

### Rollback protocol

1. **Detect** — something is broken (user report, smoke test failure, error spike)
2. **Decide** — is this "rollback now" or "hotfix forward"? If in doubt, rollback.
3. **Rollback** — use the platform's mechanism to restore the previous good state
4. **Verify** — smoke test that the rollback worked
5. **Investigate** — now figure out what went wrong, in a non-emergency context
6. **Fix forward** — create a `priority:high` bug ticket, fix properly, redeploy

> **When to fix forward instead of rolling back:** Only when the fix is trivial AND you're confident it won't make things worse. A one-line typo fix is fix-forward. Anything involving data or logic is rollback-first.

### Database rollbacks

Database changes are the hardest to roll back. Protect yourself:

- **Make schema changes backward-compatible** — add columns, don't rename or remove them in the same deploy as the code change
- **Deploy in two phases** when removing a column: (1) deploy code that stops using the column, (2) later, remove the column
- **Backup before migrations** — even a simple `pg_dump` is better than nothing

---

## Platform Guidance

This baseline is platform-agnostic, but here's how common sole-dev platforms map to the concepts above:

| Platform | Deploy trigger | Environments | Rollback | Secrets |
|----------|---------------|-------------|----------|---------|
| **Vercel** | Push to `main` (auto) | Production + PR previews (free) | Dashboard → Deployments → Redeploy | Project Settings → Environment Variables |
| **Netlify** | Push to `main` (auto) | Production + deploy previews (free) | Deploys → Published deploy → select older | Site settings → Environment variables |
| **GitHub Pages** | Push to `main` or `gh-pages` (auto) | Production only | Push a revert commit | GitHub Secrets (for Actions build step) |
| **Heroku** | `git push heroku main` or auto-deploy | Production + Review Apps (paid) | `heroku rollback` | `heroku config:set` |
| **Railway / Render / Fly.io** | Push to `main` (auto) | Production + preview (varies) | Dashboard redeploy | Platform dashboard |
| **VPS (manual)** | SSH + pull + restart | Whatever you set up | `git checkout` + restart | `.env` file on server (protect with permissions) |

> **Don't optimize your deployment pipeline on day one.** Start with whatever your platform gives you by default. Add complexity (staging environments, blue-green deploys, canary releases) only when you have evidence that the simple approach is failing.

---

## How This Fits the Workflow

Deployment is what happens after the [release checklist](release-management.md) is satisfied:

```
Steps 1-7 (per issue) → Done → Release checklist → Deploy → Smoke test → Confirm
```

| Existing concept | Deployment connection |
|-----------------|---------------------|
| **Verify column** | Work is verified before it's eligible for deployment |
| **Release checklist** | Gate between "code is ready" and "code is deployed" |
| **Hotfix process** | Compressed workflow that deploys immediately after merge |
| **CHANGELOG.md** | Records what was deployed and when |
| **`.env.example`** | Documents the configuration surface — new devs (or future-you) know what to set up |

---

## Recommended First Steps

If you have no deployment process today:

1. **Pick a platform** that supports push-to-deploy from GitHub (Vercel, Netlify, and GitHub Pages are free for most projects)
2. **Connect your repo** — set up auto-deploy from `main`
3. **Move secrets to the platform** — get them out of your code and `.env` files
4. **Commit a `.env.example`** — document every environment variable
5. **Write a 3-step smoke test** — load the app, do the main thing, check the change
6. **Know how to rollback** — find the "redeploy previous" button before you need it

That's a complete deployment setup for a sole developer. Add staging, preview environments, and database migration tooling as complexity demands it.
