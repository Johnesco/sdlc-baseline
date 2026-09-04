#!/usr/bin/env python3
"""Structural gate for sdlc-baseline.

This is the project's local gate (docs/testing.md). It is deliberately
DETERMINISTIC: standard library only, no network, no LLM, no clock or
randomness. The same working tree always produces the same result, so a
failure is a real regression and never a bad day.

    python scripts/check-docs.py        # run the gate
    python scripts/check-docs.py -v     # list what each check verified

Exit 0 = green, 1 = failures, 2 = run from the wrong directory.

What it protects, and why each one is here:

  links / anchors  A standard nobody can navigate is a standard nobody
                   follows. Markdown AND html are checked.
  orphans          docs/flow-visualization.html sat unreferenced for
                   months before anyone noticed. Never again.
  badges           The profile mechanism only works if every doc declares
                   one, in the same place, every time.
  profile-set      Exactly three docs are ops. Any drift here silently
                   changes what downstream projects are held to.
  contract         Downstream repos link to blob/main/<path>#<anchor>.
                   GitHub does not redirect moved blobs, so renaming any
                   of these breaks other people's repos with no error.
                   THIS IS THE CHECK THAT MATTERS MOST.
  severity         severity-matrix.md and bug.yml duplicate four strings
                   by necessity (GitHub reads the yml from a fixed path).
                   Duplication without a check is drift with a delay.
  template         CLAUDE-TEMPLATE.md is how every new project gets the
                   profile mechanism. If its markers go, the mechanism
                   stops propagating and nothing else notices.
  hygiene          Machine-specific paths, frozen dates and pinned model
                   names have all shipped from this repo before.
"""

import os
import re
import sys
import glob

# --------------------------------------------------------------------------
# The published contract. Downstream repos (singalong, karaokedirectory,
# ifhub) and CLAUDE-TEMPLATE.md link to these by absolute GitHub URL.
# Removing or renaming one breaks those repos SILENTLY - GitHub serves a
# 404 and nothing in this repo would otherwise notice.
#
# Adding to this list is cheap. Removing from it is a breaking change to
# the standard and belongs in CHANGELOG.md.
# --------------------------------------------------------------------------
CONTRACT_FILES = [
    "docs/workflow.md", "docs/roles.md", "docs/definition-of-done.md",
    "docs/severity-matrix.md", "docs/commit-conventions.md",
    "docs/release-management.md", "docs/testing.md", "docs/backlog-hygiene.md",
    "docs/adrs.md", "docs/security-basics.md", "docs/profiles.md",
    "docs/board-setup.md", "docs/labels.md", "docs/consumption.md",
    "docs/kickoff-checklist.md", "docs/start-here.html",
    "docs/deployment.md", "docs/ci-cd.md", "docs/incident-response.md",
    "examples/adr-template.md", "examples/adr-example.md",
    "examples/adr-stub.md", "examples/CLAUDE-example.md",
    "examples/functional-spec-template.md",
    ".github/PULL_REQUEST_TEMPLATE.md", "scripts/setup-labels.sh",
    "scripts/sync-github-templates.sh", "CHANGELOG.md",
]

CONTRACT_ANCHORS = [
    # inbound from other docs in this repo
    "docs/adrs.md#threshold-rule--when-to-write-one",
    "docs/release-management.md#changelog",
    "docs/release-management.md#hotfixes",
    "docs/release-management.md#release-checklist",
    "docs/deployment.md#rollback",
    "docs/deployment.md#configuration-and-secrets",
    "docs/deployment.md#platform-guidance",
    "docs/ci-cd.md#common-additions",
    "docs/ci-cd.md#starter-workflows",
    "docs/board-setup.md#step-5-find-your-project-ids-advanced",
    "docs/kickoff-checklist.md#quick-launch",
    # added in v0.5.0
    "docs/adrs.md#the-six-line-stub--decide-before-you-build",
    "docs/testing.md#the-local-gate-core",
    "docs/release-management.md#single-source-of-truth",
]

OPS_DOCS = ["docs/ci-cd.md", "docs/deployment.md", "docs/incident-response.md"]

FORBIDDEN = [
    (r"[A-Za-z]:\\(?:code|Users)", "machine-specific absolute path"),
    (r"created:<20\d\d-\d\d-\d\d", "frozen date in an example query"),
    (r"Claude (?:Opus|Sonnet|Haiku) [\d.]+", "pinned model name"),
    (r"\]\(\.\./docs/", "fragile ../docs/ link (use a sibling path)"),
    (r"flow-visualization", "reference to a deleted file"),
]

BADGE_RE = re.compile(r"^> \*\*Profile:\*\* (core|ops)\b")

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def read(path):
    return open(path, "rb").read().decode("utf-8").replace("\r\n", "\n")


def strip_fences(text):
    """Blank out fenced code blocks: examples inside them are not real content."""
    out, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
            out.append("")
            continue
        out.append("" if fence else line)
    return "\n".join(out)


def gh_slug(heading):
    """GitHub's heading-anchor algorithm."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return re.sub(r"\s", "-", s)


def anchors_of(path):
    """Anchor ids a file offers: md headings, or id="" attributes in html."""
    if path.endswith(".html"):
        return set(re.findall(r'\bid="([^"]+)"', read(path)))
    return {gh_slug(m.group(1))
            for m in re.finditer(r"^#{1,6}\s+(.*)$", strip_fences(read(path)), re.M)}


def links_of(path):
    """Outbound relative links: markdown ](target) or html href="target"."""
    if path.endswith(".html"):
        raw = re.findall(r'\bhref="([^"]+)"', read(path))
    else:
        raw = re.findall(r"\]\(([^)\s]+)\)", strip_fences(read(path)))
    return [t for t in raw if not re.match(r"^(https?:|mailto:|data:)", t)]


def norm(p):
    return p.replace(os.sep, "/")


PAGES = None  # populated in main()

# --------------------------------------------------------------------------
# checks - each returns (list_of_failures, count_of_things_verified, unit)
# --------------------------------------------------------------------------

CHECKS = []


def check(name, blurb):
    def deco(fn):
        CHECKS.append((name, blurb, fn))
        return fn
    return deco


@check("links", "relative links resolve to a real file")
def _links():
    fails, n = [], 0
    for f in PAGES:
        d = os.path.dirname(f) or "."
        for target in links_of(f):
            filepart = target.partition("#")[0]
            if not filepart:
                continue
            n += 1
            if not os.path.exists(os.path.normpath(os.path.join(d, filepart))):
                fails.append("%s -> %s" % (norm(f), target))
    return fails, n, "links"


@check("anchors", "#fragments point at a heading that exists")
def _anchors():
    fails, n = [], 0
    for f in PAGES:
        d = os.path.dirname(f) or "."
        for target in links_of(f):
            filepart, _, anchor = target.partition("#")
            if not anchor:
                continue
            path = f if not filepart else os.path.normpath(os.path.join(d, filepart))
            if not (os.path.isfile(path) and path.endswith((".md", ".html"))):
                continue
            n += 1
            if anchor not in anchors_of(path):
                fails.append("%s -> %s" % (norm(f), target))
    return fails, n, "anchors"


@check("orphans", "every docs/ file is linked from somewhere")
def _orphans():
    fails = []
    docs = sorted(glob.glob("docs/*.md") + glob.glob("docs/*.html"))
    for f in docs:
        base = os.path.basename(f)
        others = "\n".join(read(g) for g in PAGES if norm(g) != norm(f))
        if base not in others:
            fails.append("docs/%s is referenced by nothing" % base)
    return fails, len(docs), "docs"


@check("badges", "each docs/*.md carries one profile badge on line 3")
def _badges():
    fails = []
    docs = sorted(glob.glob("docs/*.md"))
    for f in docs:
        lines = read(f).split("\n")
        hits = [l for l in lines if l.startswith("> **Profile:**")]
        if len(hits) != 1:
            fails.append("%s has %d profile badges (want 1)" % (norm(f), len(hits)))
            continue
        if len(lines) < 3 or not BADGE_RE.match(lines[2]):
            fails.append("%s: badge is not on line 3" % norm(f))
    return fails, len(docs), "docs"


@check("profile-set", "exactly the expected docs are tagged ops")
def _profile_set():
    found = sorted(norm(f) for f in glob.glob("docs/*.md")
                   if (lambda l: len(l) > 2 and BADGE_RE.match(l[2])
                       and BADGE_RE.match(l[2]).group(1) == "ops")(read(f).split("\n")))
    if found != sorted(OPS_DOCS):
        return ["ops set is %s, expected %s" % (found, sorted(OPS_DOCS))], 0, "docs"
    return [], len(found), "ops docs"


@check("contract", "paths and anchors downstream repos link to still exist")
def _contract():
    fails = []
    for p in CONTRACT_FILES:
        if not os.path.exists(p):
            fails.append("MISSING FILE %s - breaks downstream links" % p)
    for a in CONTRACT_ANCHORS:
        path, _, anchor = a.partition("#")
        if not os.path.exists(path):
            fails.append("MISSING FILE %s (for anchor #%s)" % (path, anchor))
        elif anchor not in anchors_of(path):
            fails.append("MISSING ANCHOR %s - heading was renamed" % a)
    return fails, len(CONTRACT_FILES) + len(CONTRACT_ANCHORS), "contract items"


@check("severity", "bug.yml severity strings match severity-matrix.md")
def _severity():
    matrix, yml = {}, {}
    for line in read("docs/severity-matrix.md").split("\n"):
        m = re.match(r"^\| \*\*(Critical|High|Medium|Low)\*\* \| `\1` \| ([^|]+?) \|", line)
        if m:
            matrix[m.group(1)] = m.group(2).strip()
    for line in read(".github/ISSUE_TEMPLATE/bug.yml").split("\n"):
        m = re.match(r"^\s+- (Critical|High|Medium|Low) — (.+)$", line)
        if m:
            yml[m.group(1)] = m.group(2).strip()
    fails = []
    for lvl in ("Critical", "High", "Medium", "Low"):
        if lvl not in matrix:
            fails.append("%s missing from severity-matrix.md table" % lvl)
        elif lvl not in yml:
            fails.append("%s missing from bug.yml dropdown" % lvl)
        elif matrix[lvl] != yml[lvl]:
            fails.append("%s drifted:\n      matrix: %s\n      bug.yml: %s"
                         % (lvl, matrix[lvl], yml[lvl]))
    return fails, 4, "severity levels"


@check("template", "CLAUDE-TEMPLATE.md still carries the profile mechanism")
def _template():
    t = read("CLAUDE-TEMPLATE.md")
    required = [
        ("**SDLC profile:**", "the profile declaration line"),
        ("<!-- OPS BLOCK", "the ops-block open marker"),
        ("<!-- END OPS BLOCK -->", "the ops-block close marker"),
        ("docs/profiles.md", "a link to profiles.md"),
        ("docs/testing.md", "a link to testing.md"),
    ]
    fails = ["CLAUDE-TEMPLATE.md lost %s (%r)" % (why, needle)
             for needle, why in required if needle not in t]
    return fails, len(required), "template markers"


@check("hygiene", "no machine paths, frozen dates or pinned model names")
def _hygiene():
    fails = []
    n = 0
    for f in PAGES + ["scripts/setup-labels.sh", "scripts/sync-github-templates.sh"]:
        if norm(f) in ("CHANGELOG.md", "scripts/check-docs.py"):
            continue  # the changelog records history; this file names the patterns
        for i, line in enumerate(read(f).split("\n"), 1):
            n += 1
            for pattern, why in FORBIDDEN:
                if re.search(pattern, line):
                    fails.append("%s:%d %s\n      %s" % (norm(f), i, why, line.strip()[:90]))
    return fails, n, "lines"


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------

def main():
    global PAGES
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    if not os.path.isdir("docs") or not os.path.exists("CLAUDE-TEMPLATE.md"):
        sys.stderr.write("check-docs.py must run inside the sdlc-baseline repo\n")
        return 2

    PAGES = sorted(set(
        glob.glob("*.md") + glob.glob("docs/*.md") + glob.glob("docs/*.html")
        + glob.glob("examples/*.md") + glob.glob(".github/*.md")))

    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    print("sdlc-baseline · structural gate")
    print("%d files, deterministic, no network\n" % len(PAGES))

    failed = 0
    for name, blurb, fn in CHECKS:
        fails, count, unit = fn()
        if fails:
            failed += 1
            print("  FAIL  %-13s %s" % (name, blurb))
            for f in fails:
                print("        - %s" % f)
        else:
            detail = "%d %s" % (count, unit) if count else blurb
            print("  ok    %-13s %s" % (name, detail if not verbose else "%s (%s)" % (detail, blurb)))

    print("\n%d checks, %d failing" % (len(CHECKS), failed))
    if failed:
        print("\nThe gate is red. Nothing gets tagged until it is green — docs/testing.md.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
