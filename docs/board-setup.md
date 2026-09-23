# GitHub Projects Board Setup

> **Profile:** core — applies to every project. See [profiles.md](profiles.md).

> **Optional in core.** For one person, `gh issue list --state open` is the board. If you do use a board, everything below applies unchanged — including Step 4.

Step-by-step guide to creating the 5-column kanban board that drives this workflow.

---

## Prerequisites

- A GitHub repository (public or private)
- The [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Repository owner or admin permissions

---

## Step 1: Create the Project

1. Go to your GitHub profile or organization
2. Click **Projects** tab → **New project**
3. Select **Board** layout
4. Name it (e.g., your project name)
5. Click **Create project**

Or via CLI. The second command links the board to your repo so it shows up under the repo's **Projects** tab:

```bash
gh project create --owner [YOUR_USERNAME] --title "[Project Name]"
gh project link [PROJECT_NUMBER] --owner [YOUR_USERNAME] --repo [REPO_NAME]
```

> Note the project number that's returned — you'll need it for `gh project item-add`. A project created from the CLI starts as a table; [Step 2's CLI path](#or-via-cli) switches it to a board.

---

## Step 2: Configure Columns

The default board has 3 columns (Todo, In Progress, Done). You need 5:

### Rename existing columns
1. Click the **Todo** column header → Rename to **Backlog**
2. Keep **In Progress** as-is
3. Keep **Done** as-is

### Add new columns
Add these columns between the existing ones (click **+** to add):

4. **Ready** — place after Backlog
5. **Verify** — place after In Progress

### Final column order

```
Backlog → Ready → In Progress → Verify → Done
```

### Or via CLI

`gh` has no command for editing a field's options, but the GraphQL API does. The list you send replaces the field's options. If you pass the existing IDs for Todo, In Progress and Done, those options are renamed in place; any option you leave out is deleted. GitHub's default automations point at options by ID, so keeping the IDs keeps them working: *Item added to project* lands new items in Backlog.

```bash
OWNER=[YOUR_USERNAME]; NUMBER=[PROJECT_NUMBER]
status_field() { gh project field-list "$NUMBER" --owner "$OWNER" --format json --jq ".fields[] | select(.name==\"Status\") | $1"; }
FIELD=$(status_field .id)
TODO=$(status_field '.options[] | select(.name=="Todo") | .id')
DOING=$(status_field '.options[] | select(.name=="In Progress") | .id')
DONE=$(status_field '.options[] | select(.name=="Done") | .id')

if [ -n "$TODO" ] && [ -n "$DOING" ] && [ -n "$DONE" ]; then
  gh api graphql -f field="$FIELD" -f todo="$TODO" -f doing="$DOING" -f done="$DONE" -f query='
    mutation($field: ID!, $todo: String!, $doing: String!, $done: String!) {
      updateProjectV2Field(input: {fieldId: $field, singleSelectOptions: [
        {id: $todo,  name: "Backlog",     color: GRAY,   description: "Captured; refinement happens here"},
        {            name: "Ready",       color: BLUE,   description: "Ready to build"},
        {id: $doing, name: "In Progress", color: YELLOW, description: "Actively being coded"},
        {            name: "Verify",      color: ORANGE, description: "Awaiting human testing"},
        {id: $done,  name: "Done",        color: GREEN,  description: "Verified and accepted"}
      ]}) { projectV2Field { ... on ProjectV2SingleSelectField { options { name } } } }
    }'
else
  echo "Status doesn't have the default Todo / In Progress / Done options; nothing changed."
fi
```

Then switch the default table view to a board. It groups by Status:

```bash
PROJECT_ID=$(gh project view "$NUMBER" --owner "$OWNER" --format json --jq .id)
VIEW=$(gh api graphql -f id="$PROJECT_ID" --jq '.data.node.views.nodes[0].id' -f query='
  query($id: ID!) { node(id: $id) { ... on ProjectV2 { views(first: 1) { nodes { id } } } } }')
gh api graphql -f view="$VIEW" -f query='
  mutation($view: ID!) {
    updateProjectV2View(input: {viewId: $view, name: "Board", layout: BOARD_LAYOUT}) { projectV2View { layout } }
  }'
```

Worked example: the [karaokeunderground](https://github.com/Johnesco/karaokeunderground) board was set up with these same API calls. The IDs they produced are recorded in its `CLAUDE.md`.

---

## Step 3: Set Up Automations

GitHub Projects has built-in workflow automations. Enable these in the UI: the API can list and delete workflows, but it can't create or enable them, and it doesn't show which status each one sets.

What a new board starts with varies. Boards made with `gh project create` have arrived with *Item added to project*, *Item closed* and *Pull request merged* already on and *Item reopened* off. Check before clicking through (`$PROJECT_ID` comes from Step 2's CLI path or Step 5):

```bash
gh api graphql -f id="$PROJECT_ID" --jq '.data.node.workflows.nodes[] | "\(.name): \(.enabled)"' -f query='
  query($id: ID!) { node(id: $id) { ... on ProjectV2 { workflows(first: 20) { nodes { name enabled } } } } }'
```

The list can include workflows this board doesn't need, such as Auto-close issue, Auto-add sub-issues and Pull request linked to issue. Leave them or turn them off. The four below are the ones that matter.

### Auto-set status when items are added
1. In the project, click **⋯** (menu) → **Workflows**
2. Find **Item added to project** → Enable it
3. Set: When an item is added → Set status to **Backlog**

### Auto-close items when done
1. Find **Item closed** → Enable it
2. Set: When an item is closed → Set status to **Done**

### Auto-reopen items
1. Find **Item reopened** → Enable it
2. Set: When an item is reopened → Set status to **In Progress**

### Pull request merged
1. Find **Pull request merged** → Enable it
2. Set: When a PR is merged → Set status to **Done**

### Summary of automations

| Trigger | Sets Status To |
|---------|---------------|
| Item added to project | **Backlog** |
| Item closed | **Done** |
| Item reopened | **In Progress** |
| Pull request merged | **Done** |

### Manual transitions

These transitions are **not** automated and must be set by the developer or AI during the workflow:

| Transition | When |
|------------|------|
| Backlog → Ready | Refinement checklist complete, acceptance criteria finalized |
| Ready → In Progress | Coding begins |
| In Progress → Verify | Code is complete, awaiting human testing |

---

## Step 4: Link Issues to the Board

This is the most important operational step.

> **`gh issue create` does NOT automatically add issues to the project board.**

After every `gh issue create`, you must also run:

```bash
gh project item-add [PROJECT_NUMBER] --owner [YOUR_USERNAME] --url [ISSUE_URL]
```

### Example workflow

```bash
# Create the issue
ISSUE_URL=$(gh issue create \
  --title "Add user authentication" \
  --label "feature" \
  --milestone "User Accounts" \
  --body "Users should be able to log in..." \
  | tail -1)

# Add it to the project board
gh project item-add 1 --owner myusername --url "$ISSUE_URL"
```

### Why this matters

If you skip the `item-add` step:
- The issue exists but is invisible on the board
- Board automations (like auto-moving to Done when closed) won't fire
- The issue effectively drops out of the workflow

This is a known GitHub limitation, not a bug. Build it into your muscle memory.

### A new board can look empty

On a brand-new board, `gh project item-list` (and the API's `items` field) can report no items long after `item-add` has succeeded. Check from the issue side instead:

```bash
gh issue view [ISSUE_NUMBER] --json projectItems
```

If the output shows the board and a status, the issue is on the board. `item-add` is idempotent, so running it again does no harm, but it won't fix the listing either.

---

## Step 5: Find Your Project IDs (Advanced)

If you're scripting board operations, you'll need the project's internal IDs.

### Get the project ID

```bash
gh project list --owner [YOUR_USERNAME]
```

This shows the project number. To get the full node ID (needed for GraphQL):

```bash
gh project view [PROJECT_NUMBER] --owner [YOUR_USERNAME] --format json --jq '.id'
```

### Get field and option IDs

To programmatically move items between columns, you need the Status field ID and option IDs:

```bash
gh project field-list [PROJECT_NUMBER] --owner [YOUR_USERNAME] --format json --jq '.fields[] | select(.name=="Status")'
```

Look for the "Status" field and note the field ID and each option's ID.

### Move an item programmatically

```bash
gh project item-edit \
  --project-id [PROJECT_ID] \
  --id [ITEM_ID] \
  --field-id [STATUS_FIELD_ID] \
  --single-select-option-id [OPTION_ID]
```

> Store these IDs in your project's CLAUDE.md or memory files so your AI assistant can move cards without looking them up each time.

---

## Checklist

After setup, verify:

- [ ] 5 columns in correct order: Backlog → Ready → In Progress → Verify → Done
- [ ] "Item added" automation sets status to Backlog
- [ ] "Item closed" automation sets status to Done
- [ ] "Item reopened" automation sets status to In Progress
- [ ] "PR merged" automation sets status to Done
- [ ] Test: create an issue, add it to the board, confirm it lands in Backlog
- [ ] Test: close the issue, confirm it moves to Done
