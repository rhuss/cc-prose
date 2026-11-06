---
description: Sync humanizer skill from upstream with intelligent merge
argument-hint: "[--dry-run]"
---

# /update-humanizer - Upstream Humanizer Sync

Merge upstream humanizer changes while preserving local cc-prose additions.

## Usage

```
/update-humanizer
/update-humanizer --dry-run
```

## What This Command Does

This command performs an intelligent sync of the humanizer skill from the
upstream repository (blader/humanizer), preserving local cc-prose additions
like rule-of-three density detection and custom filler phrase entries.

## Execution Steps

Follow these steps in order. Do not skip steps or reorder them.

### Step 0: Resolve the Maintenance Checkout

Read `docs/harnesses.md`. This is a source-maintenance workflow. Use a writable cc-prose checkout containing `prose/skills/humanizer/SKILL.md` (the tracking marker `prose/.humanizer-sync` may be absent on first use); do not edit an installed plugin cache. If the current directory is a consumer project, ask for the maintenance checkout path and resolve all following repository-relative paths there. If no writable checkout is available, explain how to clone cc-prose and stop before any fetch or write.

Parse `--dry-run` before any state changes. It suppresses all writes, including initial-baseline creation, canonical source changes, tracking updates, and reports.

### Step 1: Read Tracking State

Read `prose/.humanizer-sync` to get the current sync state.

- If the file does not exist, go to **Step 1a: Initial Baseline** below.
- If the file exists, extract `last_sync_commit`, `last_sync_date`, and `modified_skills`.

### Step 1a: Initial Baseline (only if no tracking file exists)

This is the first-time setup path.

1. Get the current upstream HEAD commit SHA:
   ```bash
   gh api repos/blader/humanizer/commits/main --jq '.sha'
   ```
   If `gh` is unavailable, use:
   ```bash
   TEMP_DIR=$(mktemp -d)
   git clone --depth 1 https://github.com/blader/humanizer.git "$TEMP_DIR"
   git -C "$TEMP_DIR" rev-parse HEAD
   rm -rf "$TEMP_DIR"
   ```

2. For `--dry-run`, show the proposed baseline SHA and metadata, then exit without creating a tracking file or report. Otherwise create `prose/.humanizer-sync` with this content (replace SHA and date):
   ```json
   {
     "upstream_repo": "https://github.com/blader/humanizer",
     "last_sync_commit": "<SHA from above>",
     "last_sync_date": "<today's date YYYY-MM-DD>",
     "modified_skills": [
       {
         "upstream_file": "SKILL.md",
         "local_file": "prose/skills/humanizer/SKILL.md",
         "local_additions": [
           {
             "section": "10. Rule of Three Overuse",
             "description": "Density detection counting triples across whole text"
           },
           {
             "section": "22. Filler Phrases",
             "description": "Added 'Here's the twist/kicker/...' entries"
           }
         ]
       }
     ]
   }
   ```

3. Report that the initial baseline has been established and exit.
   No merge is needed on the first run since the baseline just marks the starting point.

### Step 2: Check for Upstream Changes

Get the current upstream HEAD and compare with `last_sync_commit`:

```bash
UPSTREAM_HEAD=$(gh api repos/blader/humanizer/commits/main --jq '.sha')
```

If `gh` is unavailable, clone to a temp directory:
```bash
TEMP_DIR=$(mktemp -d)
git clone --depth 50 https://github.com/blader/humanizer.git "$TEMP_DIR"
UPSTREAM_HEAD=$(git -C "$TEMP_DIR" rev-parse HEAD)
```

If `UPSTREAM_HEAD` equals `last_sync_commit`, report "No upstream changes since last sync" and exit.

### Step 3: Fetch Upstream Changes

Clone the upstream repo (if not already cloned in Step 2) and extract the
diff between `last_sync_commit` and HEAD for SKILL.md:

```bash
TEMP_DIR=$(mktemp -d)
git clone https://github.com/blader/humanizer.git "$TEMP_DIR"
git -C "$TEMP_DIR" diff <last_sync_commit>..HEAD -- SKILL.md
```

Read both files:
- The upstream version: `$TEMP_DIR/SKILL.md` (at HEAD)
- The local version: `prose/skills/humanizer/SKILL.md`

Clean up the temp directory when done:
```bash
rm -rf "$TEMP_DIR"
```

### Step 4: Intelligent Merge

This is the core AI-assisted step. Read the `modified_skills[0].local_additions`
array from the tracking file to identify sections with local cc-prose content.

**Merge rules:**

1. **New upstream categories or sections**: Add them to the local file in the
   correct position, preserving the existing structure.

2. **Modified upstream sections that have NO local additions**: Accept the
   upstream version directly.

3. **Modified upstream sections that HAVE local additions** (listed in
   `local_additions` metadata): Merge carefully. Keep the local additions
   intact while incorporating upstream improvements around them. If a conflict
   exists where upstream and local changes overlap in the same paragraph,
   flag it in the sync report and prefer the local version.

4. **Deleted upstream sections**: Remove them from the local file, unless
   they contain local additions (flag in sync report instead).

5. **Local-only sections** (not in upstream): Preserve them unchanged.

If the `--dry-run` argument was provided, show what would change without
modifying any files, then exit.

### Step 5: Write Merged File

Write the merged content to `prose/skills/humanizer/SKILL.md`.

### Step 6: Keep the Checkout Authoritative

The merged `prose/skills/humanizer/SKILL.md` is the authoritative copy. Do not copy it to a separate Claude user skill or edit another harness's installed cache. After reviewing the source changes, refresh/reinstall each harness's plugin from this checkout.

### Step 7: Update Tracking File

Update `prose/.humanizer-sync` with:
- `last_sync_commit`: set to the upstream HEAD SHA from Step 2
- `last_sync_date`: set to today's date (YYYY-MM-DD)
- Keep all other fields unchanged

### Step 8: Generate Sync Report

Create a sync report at `docs/sync-reports/sync-YYYY-MM-DD.md`.

If a file with that name already exists (same-day duplicate sync), use a
suffix: `sync-YYYY-MM-DD-2.md`, `sync-YYYY-MM-DD-3.md`, etc.

Use this template:

```markdown
# Sync Report: YYYY-MM-DD

**Upstream**: blader/humanizer
**Previous sync**: <old-commit-sha> (<old-date>)
**Current sync**: <new-commit-sha> (<today>)
**Commits synced**: <count>

## Upstream Changes

[Per-commit summary of what changed in SKILL.md]

## Changes Integrated

[What was merged into the local copy]

## Local Additions Preserved

[Confirmation that local sections listed in modified_skills remained intact]

## Conflicts

[Any conflicts between upstream changes and local additions, or "None"]

## Action Items

[Follow-up tasks if any, or "None"]
```

### Step 9: Summary

Report what was done:
- Number of upstream commits integrated
- Sections added, modified, or removed
- Local additions that were preserved
- Any conflicts that need manual review
- Path to the sync report

## Edge Cases

- **Network failure**: If upstream is unreachable, report the error clearly
  and do not modify any local files.
- **Invalid last_sync_commit**: If the tracked commit no longer exists upstream
  (force-push/rebase), report that a manual baseline reset is needed. Suggest
  deleting `prose/.humanizer-sync` and re-running to establish a new baseline.
- **Missing local additions**: Before merging, verify that the sections listed
  in `modified_skills[0].local_additions` still exist in the local file. If any
  are missing, warn the user before proceeding.
