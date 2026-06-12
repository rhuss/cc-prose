# Data Model: Humanizer Upstream Sync

## Tracking File (`prose/.humanizer-sync`)

JSON document storing sync state. Created on first sync, updated after each subsequent sync.

### Schema

```json
{
  "upstream_repo": "https://github.com/blader/humanizer",
  "last_sync_commit": "<40-char SHA>",
  "last_sync_date": "YYYY-MM-DD",
  "modified_skills": [
    {
      "upstream_file": "SKILL.md",
      "local_file": "prose/skills/humanizer/SKILL.md",
      "canonical_file": "~/.claude/skills/humanizer/SKILL.md",
      "local_additions": [
        {
          "section": "<section heading>",
          "description": "<what was added locally>"
        }
      ]
    }
  ]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `upstream_repo` | string (URL) | yes | GitHub URL of the upstream humanizer repo |
| `last_sync_commit` | string (SHA) | yes | Full 40-character commit SHA of last synced upstream commit |
| `last_sync_date` | string (ISO date) | yes | Date of last sync in YYYY-MM-DD format |
| `modified_skills` | array | yes | List of tracked files with local modification metadata |
| `modified_skills[].upstream_file` | string | yes | Filename in upstream repo |
| `modified_skills[].local_file` | string | yes | Path to plugin copy relative to repo root |
| `modified_skills[].canonical_file` | string | yes | Path to canonical local copy (may use `~`) |
| `modified_skills[].local_additions` | array | yes | Sections containing cc-prose-specific content |
| `modified_skills[].local_additions[].section` | string | yes | Section heading containing local addition |
| `modified_skills[].local_additions[].description` | string | yes | Human-readable description of what was added |

### Lifecycle

1. **Created**: On first `/update-humanizer` run (initial baseline)
2. **Updated**: After each successful sync (new commit SHA and date)
3. **Read**: By `check-upstream-changes.sh` and `/update-humanizer` command
4. **Never deleted**: Persists across the project lifetime

### Validation Rules

- `last_sync_commit` must be a valid 40-character hex string
- `last_sync_date` must be a valid ISO date
- `modified_skills` must have at least one entry
- `local_additions` may be empty (no local changes to preserve)

## Sync Report (`docs/sync-reports/sync-YYYY-MM-DD.md`)

Markdown document generated after each sync. Immutable once created.

### Structure

- Header with upstream repo, previous/current commit SHAs, dates, commit count
- Upstream Changes section (per-commit summary)
- Changes Integrated section (what was merged)
- Local Additions Preserved section (confirmation)
- Conflicts section (if any)
- Action Items section (follow-up tasks)

### Naming Convention

- Format: `sync-YYYY-MM-DD.md`
- Same-day duplicates: `sync-YYYY-MM-DD-2.md`, `sync-YYYY-MM-DD-3.md`
