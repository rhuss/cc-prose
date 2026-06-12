# Brainstorm: Humanizer upstream sync mechanism

**Date:** 2026-06-12
**Status:** spec-created

## Problem Framing

The current humanizer sync is a blind `cp` from `~/.claude/skills/humanizer/SKILL.md` into the plugin directory (`make sync-humanizer`). This has several problems:

1. No version tracking. We don't know which upstream commit we last synced from.
2. No delta awareness. Every sync overwrites the entire file, making it impossible to tell what actually changed.
3. Two-hop chain. Upstream repo -> local canonical copy -> plugin copy. The middle step is manual and untracked.
4. No merge intelligence. Local additions (rule-of-three density, filler phrase entries) get overwritten on sync.
5. No audit trail. No sync reports documenting what changed and why.

The cc-spex project solved this exact problem for superpowers integration with a well-proven pattern: a `.superpowers-sync` tracking file, a check script, an AI-assisted merge command, and sync reports. We should adopt the same approach.

## Context

### cc-spex sync pattern (proven)
- `.superpowers-sync` JSON file tracks upstream repo, last sync commit, last sync date, and per-file modification metadata
- `scripts/check-upstream-changes.sh` detects upstream changes since last sync without modifying files
- `/update-superpowers` Claude Code command performs AI-assisted merge, preserving local additions
- `docs/sync-reports/sync-YYYY-MM-DD.md` documents each sync

### Upstream repo structure (blader/humanizer)
- Simple repo: `SKILL.md`, `AGENTS.md`, `README.md`, `LICENSE`
- Current HEAD: `9600f2b` (v2.8.0)
- Only `SKILL.md` needs syncing

### Our local additions to preserve
- Rule-of-three density detection (count triples across whole text)
- Filler phrase entries ("Here's the twist/kicker/...")
- Any future cc-prose-specific additions

## Approaches Considered

### A: Adapt cc-spex pattern (Recommended)
- Create `.humanizer-sync` tracking file in `prose/`
- Create `scripts/check-upstream-changes.sh` for non-destructive checking
- Create `/update-humanizer` Claude Code command for AI-assisted merge
- Generate sync reports in `docs/sync-reports/`
- Track only `SKILL.md` (single file, simpler than cc-spex's multi-file tracking)
- Pros: Proven pattern, delta-aware, preserves local additions, auditable
- Cons: Some setup effort; but the cc-spex implementation is a clear template

### B: Git submodule
- Add blader/humanizer as a git submodule, merge at build time
- Pros: Automatic version tracking via git
- Cons: Submodules are fragile, poor UX, overkill for tracking one file

### C: Keep current approach with version annotation
- Keep the `cp`-based sync but add version comments to the file header
- Pros: Minimal change
- Cons: Still overwrites local additions, no merge intelligence, no audit trail

## Decision

Approach A: Adapt the cc-spex sync pattern. The upstream repo is simpler (single file vs. multiple skills), which makes this even more straightforward than cc-spex's implementation.

## Key Requirements

1. **Tracking file** (`prose/.humanizer-sync`):
   - `upstream_repo`: `https://github.com/blader/humanizer`
   - `last_sync_commit`: SHA of last synced upstream commit
   - `last_sync_date`: ISO date
   - `modified_skills`: metadata for `SKILL.md` including local additions to preserve

2. **Check script** (`scripts/check-upstream-changes.sh`):
   - Read last sync commit from `.humanizer-sync`
   - Clone/fetch upstream to temp dir
   - Show diff since last sync
   - Makefile target: `make check-upstream`

3. **Merge command** (`prose/.claude/commands/update-humanizer.md`):
   - AI-assisted merge preserving local additions
   - Update `.humanizer-sync` with new commit hash and date
   - Generate sync report
   - Also update `~/.claude/skills/humanizer/SKILL.md` (canonical copy) to keep them aligned

4. **Sync reports** (`docs/sync-reports/sync-YYYY-MM-DD.md`):
   - Document upstream changes, what was integrated, what was preserved

5. **Remove old sync target**: Replace `make sync-humanizer` (blind cp) with `make check-upstream`

6. **Initial baseline**: Set `.humanizer-sync` to current upstream HEAD (`9600f2b`, v2.8.0) after first full sync

## Open Questions

- Should the canonical copy at `~/.claude/skills/humanizer/` be eliminated entirely, syncing directly from upstream to plugin? That removes the two-hop chain.
- Should `make check-upstream` be a pre-install hook (warn on outdated sync)?
