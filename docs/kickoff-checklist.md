# Project Kickoff Checklist

A step-by-step guide for setting up a new project (or adopting this SDLC in an existing one). Work through it top to bottom — each step builds on the previous one.

---

## Quick Launch

Open a Claude Code session in your new (or existing) project directory and paste this prompt, filling in the bracketed values:

```
Set up this project using the sdlc-baseline process.

sdlc-baseline location: C:\code\sdlc-baseline
(or: https://github.com/Johnesco/sdlc-baseline)

Project name: [your project name]
Purpose: [one sentence — what does it do?]
Stack: [language, framework, key dependencies]
Repo: [GitHub URL, or "create one"]

Follow the kickoff checklist in sdlc-baseline/docs/kickoff-checklist.md.
Copy the vendored files, create CLAUDE.md from the template, set up
labels and the project board, and fill in project identity together
with me. Skip deployment and CI/CD for now — I'll add those later.
```

Claude will walk through the phases below, copying files, running setup commands, and prompting you for the project-specific details it can't infer (milestones, architecture decisions, board IDs).

After this first session, every future session reads CLAUDE.md and knows the process automatically.

> **Adopting in an existing project?** Replace the last paragraph with:
> ```
> This is an existing project with code already in place. Follow the
> "Existing Project" section of the kickoff checklist. Don't retrofit
> old issues — just set up the process for new work going forward.
> ```

---

## New Project

### Phase 1: Repository and structure (30 minutes)

- [ ] **Create the GitHub repo** (or confirm it exists)
  ```bash
  gh repo create my-project --public --clone
  ```

- [ ] **Copy the CLAUDE.md skeleton**
  ```bash
  cp sdlc-baseline/CLAUDE-TEMPLATE.md my-project/CLAUDE.md
  ```
  Fill in: Project Identity, Architecture, File Structure Overview, Key Technical Patterns. Leave the rest as placeholders until you need them.

- [ ] **Copy the vendored GitHub files**
  ```bash
  cp -r sdlc-baseline/.github my-project/
  cp sdlc-baseline/scripts/setup-labels.sh my-project/scripts/
  cp sdlc-baseline/scripts/sync-github-templates.sh my-project/scripts/
  ```

- [ ] **Create a CHANGELOG.md**
  ```markdown
  # Changelog

  ## [Unreleased]
  ```
  That's enough to start. Entries accumulate here as you close issues. See [release-management.md](release-management.md#changelog).

- [ ] **Create .gitignore** — include `.env`, `.env.local`, IDE files, OS files, build output.

- [ ] **Create .env.example** (if the project will have any configuration)
  ```bash
  # .env.example — committed, no real values
  # DATABASE_URL=postgresql://localhost:5432/myapp_dev
  ```
  See [deployment.md — Configuration and Secrets](deployment.md#configuration-and-secrets).

- [ ] **Initial commit**
  ```bash
  git add -A && git commit -m "Initial project setup"
  git push -u origin main
  ```

### Phase 2: GitHub project management (15 minutes)

- [ ] **Create labels** — run the label setup script against your repo:
  ```bash
  bash scripts/setup-labels.sh
  ```
  Optionally delete GitHub's default labels first. See [labels.md](labels.md).

- [ ] **Create the Projects board** — follow [board-setup.md](board-setup.md):
  - 5 columns: Backlog → Ready → In Progress → Verify → Done
  - Enable automations (item added → Backlog, item closed → Done, item reopened → In Progress, PR merged → Done)

- [ ] **Record your Project IDs in CLAUDE.md** — board ID, status field ID, and status option IDs. Your AI assistant needs these to move cards programmatically. See [board-setup.md — Find Your Project IDs](board-setup.md#step-5-find-your-project-ids-advanced).

- [ ] **Create your first milestone** — name it after the first logical batch of work (e.g., "MVP", "v0.1", or a feature theme).

### Phase 3: Deployment (when you're ready to go live)

These steps can wait until you have something to deploy. Don't set up infrastructure for code that doesn't exist yet.

- [ ] **Pick a hosting platform** — see [deployment.md — Platform Guidance](deployment.md#platform-guidance)
- [ ] **Connect your repo for auto-deploy** (if the platform supports it)
- [ ] **Move secrets to the platform's environment config** — never commit them
- [ ] **Know how to rollback** — find the "redeploy previous" button before you need it
- [ ] **Write a 3-step smoke test** for your critical path

### Phase 4: CI/CD (when tests or builds exist)

Don't add CI on day one unless you already have a test suite. Add it when the pain of forgetting to run checks justifies the 10 minutes of setup.

- [ ] **Copy a starter workflow** from [ci-cd.md](ci-cd.md#starter-workflows) into `.github/workflows/ci.yml`
- [ ] **Strip it down** to only the steps your project actually has
- [ ] **Push and verify** — open a test PR, confirm CI runs
- [ ] **Enable branch protection** — require the CI status check to pass before merge

---

## Existing Project

Adopting this SDLC in a project that already has code and possibly some issues.

### Phase 1: Add the process layer (30 minutes)

- [ ] **Create CLAUDE.md** from the template — fill in the project-specific sections with what you already know. This is the most valuable single step.

- [ ] **Copy .github/ templates** — issue templates and PR template. These start working immediately for new issues.

- [ ] **Create labels** — run `setup-labels.sh`. If you have existing labels you want to keep, review the script first to avoid duplicates.

- [ ] **Create CHANGELOG.md** — start with `[Unreleased]`. You don't need to backfill history.

### Phase 2: Set up the board (15 minutes)

- [ ] **Create the Projects board** following [board-setup.md](board-setup.md)

- [ ] **Add existing open issues to the board**
  ```bash
  # List open issues
  gh issue list --state open

  # Add each to the board
  gh project item-add [PROJECT_NUMBER] --owner [OWNER] --url [ISSUE_URL]
  ```

- [ ] **Triage existing issues** — for each issue on the board:
  - Add a type label (`feature`, `bug`, `task`, `docs`, `spike`)
  - Add area labels if obvious
  - Move refined issues to Ready; leave vague ones in Backlog

- [ ] **Record Project IDs in CLAUDE.md**

### Phase 3: Adopt the workflow going forward

- [ ] **Use the 7-step workflow for new work** — don't try to retrofit old issues
- [ ] **Set up deployment and CI/CD** when you're ready — see Phases 3-4 under New Project above

> **Don't boil the ocean.** The biggest risk with adopting a process mid-project is trying to fix everything at once. Get the board set up, start following the workflow for new tickets, and improve incrementally.

---

## Verification

After setup, verify everything is wired up:

- [ ] Create a test issue using one of the templates — does the template render correctly?
- [ ] Add it to the board — does it land in Backlog?
- [ ] Close it — does it move to Done?
- [ ] Open a test PR — does the PR template appear? Does CI run (if configured)?
- [ ] Delete the test issue and PR

---

## What to Skip (For Now)

These are part of the full SDLC but should be added on-demand, not on day one:

| Artifact | When to add |
|----------|------------|
| ADRs (`docs/adr/`) | When you make your first architectural decision that meets the [threshold rule](adrs.md#threshold-rule--when-to-write-one) |
| Functional spec (`docs/functional-spec.md`) | When the project has enough features that you need a single source of truth for behavior |
| Staging environment | When you have paying users or risky deploys |
| Uptime monitoring | When the site is live and users depend on it |
| Backlog grooming cadence | When you have 10+ open issues |
| Incident response prep | When you have users who would notice an outage |

The goal is a working process on day one, not a perfect process. Add layers as the project grows.

---

## Quick Reference: What Goes Where

After kickoff, your project should have these files from sdlc-baseline:

```
my-project/
├── CLAUDE.md                              # From CLAUDE-TEMPLATE.md (customized)
├── CHANGELOG.md                           # Created during kickoff
├── .env.example                           # Created during kickoff (if applicable)
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── config.yml                     # Vendored from sdlc-baseline
│   │   ├── feature.yml                    # Vendored
│   │   ├── bug.yml                        # Vendored
│   │   ├── task.yml                       # Vendored
│   │   ├── spike.yml                      # Vendored
│   │   └── doc.yml                        # Vendored
│   ├── PULL_REQUEST_TEMPLATE.md           # Vendored
│   └── workflows/
│       └── ci.yml                         # Created during Phase 4 (when ready)
├── scripts/
│   ├── setup-labels.sh                    # Vendored (run once, keep for reference)
│   └── sync-github-templates.sh           # Vendored (run when sdlc-baseline updates)
└── docs/
    ├── adr/                               # Created when first ADR is needed
    └── functional-spec.md                 # Created when feature complexity warrants it
```

Everything else — workflow, roles, DoD, commit conventions, severity matrix, release management, deployment, CI/CD, backlog hygiene, incident response, ADR protocol — lives canonically in sdlc-baseline and is linked from your CLAUDE.md. See [consumption.md](consumption.md).
