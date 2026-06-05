# Security Basics

Practical security habits for a sole developer. This isn't a comprehensive security program — it's the minimum set of practices that prevent the most common vulnerabilities.

---

## The Principles

1. **Don't trust input.** Anything from users, URLs, APIs, or files could be malicious.
2. **Don't ship secrets.** Keys, tokens, and credentials belong in environment variables, not in code.
3. **Keep dependencies current.** Most vulnerabilities come from outdated packages, not your code.
4. **Use HTTPS everywhere.** No exceptions.
5. **Default to least privilege.** Give users, services, and API keys only the access they need.

---

## Secrets Management

The most common sole-dev security failure: accidentally committing a secret to Git.

### Rules

- **Never commit secrets.** API keys, database credentials, tokens, private keys — none of these belong in your repository, even a private one.
- **Use `.env` files locally, environment variables in production.** See [deployment.md — Configuration and Secrets](deployment.md#configuration-and-secrets).
- **Commit a `.env.example`** with variable names but no real values.
- **Add `.env` to `.gitignore` before your first commit.** Retroactively removing a committed secret doesn't erase it from Git history.

### If you accidentally commit a secret

1. **Revoke the secret immediately.** Generate a new key/token in the provider's dashboard. Don't just remove it from code — it's already in Git history.
2. **Remove from history** (if the repo is public):
   ```bash
   # Use git-filter-repo (preferred) or BFG Repo-Cleaner
   git filter-repo --invert-paths --path .env
   git push --force
   ```
3. **Rotate the secret** in all environments (local, CI, production).
4. **Audit for damage** — check the provider's logs for unauthorized usage between the commit and revocation.

> **Prevention beats cleanup.** Consider a pre-commit hook that scans for common secret patterns. Tools like [gitleaks](https://github.com/gitleaks/gitleaks) or [detect-secrets](https://github.com/Yelp/detect-secrets) automate this.

---

## Dependency Security

Your dependencies are your attack surface. A vulnerability in a package you use is a vulnerability in your app.

### Regular auditing

```bash
# Node.js
npm audit
npm audit --audit-level=high    # Only flag high/critical

# Python
pip-audit                        # Install: pip install pip-audit

# GitHub (all languages)
gh api repos/{owner}/{repo}/vulnerability-alerts
```

Add `npm audit` (or equivalent) to your CI pipeline — see [ci-cd.md](ci-cd.md#common-additions).

### Update strategy

| Approach | When to use |
|----------|------------|
| **Patch updates immediately** | Security advisories, `npm audit` findings |
| **Minor updates periodically** | Monthly or per-milestone batch |
| **Major updates deliberately** | Read the changelog, test thoroughly, file a ticket |

### Evaluating new dependencies

Before adding a package, check:

- **Maintenance** — when was the last commit? Are issues being addressed?
- **Popularity** — downloads and stars aren't proof of quality, but very low numbers are a signal
- **Size** — is this a 2KB utility or a 50MB framework? Smaller = less attack surface
- **Alternatives** — can you write the 10 lines yourself instead of adding a dependency?

---

## Common Vulnerabilities and Prevention

### Cross-Site Scripting (XSS)

**What:** Attacker injects malicious script into your page through user input.

**Prevention:**
- Escape all user-generated content before rendering it as HTML
- Use your framework's built-in escaping (React's JSX, Vue's `{{ }}`, etc.)
- Set `Content-Security-Policy` headers to restrict script sources
- Never use `innerHTML` with unsanitized input

```javascript
// Bad — XSS vulnerable
element.innerHTML = userInput;

// Good — escaped
element.textContent = userInput;
```

### SQL / NoSQL Injection

**What:** Attacker manipulates database queries through user input.

**Prevention:**
- Use parameterized queries or an ORM — never concatenate user input into queries
- Validate and sanitize input on the server, even if the client already validated it

```javascript
// Bad — injection vulnerable
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// Good — parameterized
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### Cross-Site Request Forgery (CSRF)

**What:** Attacker tricks a logged-in user's browser into making unwanted requests to your app.

**Prevention:**
- Use CSRF tokens for state-changing requests (most frameworks include this)
- Set `SameSite=Strict` or `SameSite=Lax` on cookies
- Require re-authentication for sensitive operations

### Insecure Direct Object References (IDOR)

**What:** User accesses another user's data by guessing or changing an ID in the URL.

**Prevention:**
- Always check authorization — "does this user have access to this resource?"
- Don't rely on obscurity (random IDs help, but aren't a substitute for access checks)
- Use UUIDs instead of sequential IDs to make guessing harder

---

## HTTPS and Transport Security

### Rules

- **Use HTTPS for everything.** Most hosting platforms (Vercel, Netlify, GitHub Pages) provide it automatically.
- **Redirect HTTP to HTTPS.** Don't serve content on both.
- **Set security headers.** At minimum:

```
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

Most hosting platforms let you configure these in a config file (`vercel.json`, `netlify.toml`, `_headers`). For custom servers, set them in your response middleware.

### API keys in the browser

If your frontend calls a third-party API directly:
- **Use restricted API keys** — limit by domain, IP, or scope
- **Never expose server-side keys to the browser** — use a backend proxy if the API requires a secret key
- **Rate-limit your proxy** to prevent abuse

---

## Authentication (When You Need It)

If your app has user accounts:

### Do

- Use a proven auth provider (Auth0, Supabase Auth, Firebase Auth, Clerk) rather than rolling your own
- Hash passwords with bcrypt, scrypt, or argon2 — never store plaintext or use MD5/SHA for passwords
- Enforce minimum password length (12+ characters is modern best practice)
- Support multi-factor authentication for sensitive apps

### Don't

- Don't store sessions in localStorage (vulnerable to XSS) — use httpOnly cookies
- Don't send passwords in URL parameters
- Don't implement "remember me" with a plaintext token
- Don't roll your own crypto

> **For most sole-dev projects:** use a third-party auth provider. The setup cost is lower than building auth correctly, and the security is better than what you'll build yourself.

---

## Security in the Development Workflow

### Issue handling

When you discover a security issue:

- **File it as a `bug` with `priority:high`** — security bugs are always high priority
- **Don't describe the exploit in a public issue** if the repo is public — use a private description or note "security fix" in the public issue and detail it after the fix ships
- **Follow the hotfix process** in [release-management.md](release-management.md#hotfixes) — fix and deploy quickly

### Code review habits

When reviewing your own code (or having AI review it), check for:

- [ ] User input escaped/sanitized before display or storage
- [ ] Database queries use parameterized inputs
- [ ] No secrets hardcoded in source files
- [ ] New dependencies reviewed for maintenance and size
- [ ] API endpoints check authorization, not just authentication
- [ ] Error messages don't leak internal details (stack traces, DB schema, file paths)

### Production monitoring

See [incident-response.md](incident-response.md) for monitoring setup. Security-specific additions:

- **Enable GitHub's Dependabot alerts** — free, automatic, catches known dependency vulnerabilities
- **Review access logs periodically** — look for unusual patterns (brute-force attempts, unexpected API usage)
- **Set up alerts for auth failures** — if your app has login, alert on spikes in failed attempts

---

## Security Checklist for New Projects

Run through this when setting up a new project (or audit an existing one):

- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` exists with variable names (no real values)
- [ ] No secrets in the codebase (`git log --all -p | grep -i "api_key\|secret\|password\|token"`)
- [ ] HTTPS configured (most platforms do this automatically)
- [ ] Security headers set (CSP, HSTS, X-Content-Type-Options)
- [ ] User input is escaped/sanitized everywhere it's rendered
- [ ] Database queries use parameterization
- [ ] Dependencies are current (`npm audit` or equivalent)
- [ ] Dependabot alerts enabled in GitHub repo settings
- [ ] Auth uses a third-party provider (if applicable)

---

## How This Fits the Workflow

Security isn't a separate phase — it's baked into every step:

| Workflow concept | Security connection |
|-----------------|-------------------|
| **Step 2 (Review docs)** | Check for security implications in the affected area |
| **Step 5 (Implement)** | Follow the prevention patterns above |
| **Step 7 (Verify)** | Include the security review habits checklist |
| **Definition of Done** | "No regressions" includes security regressions |
| **CI/CD** | `npm audit` in the pipeline catches dependency vulnerabilities |
| **Incident response** | Security incidents follow the same restore → investigate → prevent sequence |
| **Deployment** | Secrets in environment variables, not code |

---

## Recommended First Steps

1. **Check your `.gitignore`** — is `.env` in there?
2. **Run `npm audit`** (or equivalent) — fix anything critical
3. **Enable Dependabot** — GitHub repo → Settings → Code security and analysis → Enable
4. **Scan for committed secrets** — `git log --all -p | grep -iE "(api_key|secret|password|token).*="` — if you find any, revoke and rotate them
5. **Set security headers** — copy the headers above into your platform's config file
