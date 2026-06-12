# Implementation Plan: Humanizer Upstream Sync

**Branch**: `001-humanizer-upstream-sync` | **Date**: 2026-06-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-humanizer-upstream-sync/spec.md`

## Summary

Implement a delta-aware upstream sync mechanism for the humanizer skill, replacing the current blind `cp` workflow. The system tracks the last synced upstream commit, detects changes via `gh api` or shallow clone, and provides an AI-assisted Claude Code command for intelligent merging that preserves local cc-prose additions. Every sync generates an audit report.

## Technical Context

**Language/Version**: Bash (POSIX-compatible scripts), Markdown (Claude Code command)
**Primary Dependencies**: `git`, `gh` CLI (optional, with fallback), `jq`
**Storage**: JSON tracking file (`prose/.humanizer-sync`), Markdown sync reports
**Testing**: Manual verification via `make check-upstream` and `/update-humanizer` command
**Target Platform**: macOS/Linux (Claude Code plugin environment)
**Project Type**: Claude Code plugin (cc-prose)
**Performance Goals**: Check upstream status in under 30 seconds
**Constraints**: Must work without `gh` CLI (git clone fallback); must preserve local additions during merge
**Scale/Scope**: Single file sync (SKILL.md), single upstream repo (blader/humanizer)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution is a template placeholder with no project-specific principles. No gates to evaluate. Pass by default.

## Project Structure

### Documentation (this feature)

```text
specs/001-humanizer-upstream-sync/
├── plan.md              # This file
├── research.md          # Phase 0: cc-spex sync pattern analysis
├── data-model.md        # Phase 1: .humanizer-sync JSON schema
└── tasks.md             # Phase 2 output (via /speckit-tasks)
```

### Source Code (repository root)

```text
prose/
├── .humanizer-sync                    # NEW: JSON tracking file
├── commands/
│   └── update-humanizer.md            # NEW: AI-assisted merge command
├── skills/
│   └── humanizer/
│       └── SKILL.md                   # EXISTING: target of sync
scripts/
└── check-upstream-changes.sh          # NEW: non-destructive upstream check
docs/
└── sync-reports/
    └── sync-YYYY-MM-DD.md             # NEW: generated per sync
Makefile                               # MODIFIED: replace sync-humanizer with check-upstream
```

**Structure Decision**: Follows existing cc-prose layout. New files integrate into existing `prose/commands/`, `scripts/`, and `docs/` directories. No new directory hierarchy needed.

## Implementation Approach

### Phase 1: Tracking File and Check Script

Create the `.humanizer-sync` JSON tracking file with initial baseline data. Implement `scripts/check-upstream-changes.sh` that reads the tracking file, queries upstream state (via `gh api` or shallow clone), and reports changes. Add `make check-upstream` Makefile target.

### Phase 2: Claude Code Merge Command

Create `prose/commands/update-humanizer.md` as a Claude Code slash command. The command reads the tracking file, clones upstream changes since last sync, instructs the AI to merge upstream additions while preserving sections listed in `modified_skills` metadata, updates the tracking file, generates a sync report, and updates the canonical copy at `~/.claude/skills/humanizer/SKILL.md`.

### Phase 3: Makefile and Cleanup

Replace the old `make sync-humanizer` target with `make check-upstream`. Update help text. Ensure `docs/sync-reports/` directory exists.

## Complexity Tracking

No constitution violations to justify.
