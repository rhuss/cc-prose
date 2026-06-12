# Feature Specification: Humanizer Upstream Sync

**Feature Branch**: `001-humanizer-upstream-sync`
**Created**: 2026-06-12
**Status**: Draft
**Input**: Implement delta-aware upstream sync mechanism for the humanizer skill, modeled on cc-spex's superpowers integration pattern.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Check for upstream changes (Priority: P1)

A plugin maintainer wants to know whether the upstream humanizer (blader/humanizer) has new commits since the last sync, without modifying any local files. They run `make check-upstream` and see a summary of what changed upstream, so they can decide whether to sync.

**Why this priority**: This is the foundation. Without knowing what changed, there is no informed sync decision.

**Independent Test**: Run `make check-upstream` against a known upstream state and verify it reports the correct diff summary.

**Acceptance Scenarios**:

1. **Given** the upstream repo has new commits since the last sync, **When** the maintainer runs `make check-upstream`, **Then** the script shows a diff summary with commit messages and changed lines for `SKILL.md`.
2. **Given** the upstream repo has no new commits, **When** the maintainer runs `make check-upstream`, **Then** the script reports "No upstream changes since last sync" with the last sync date.
3. **Given** the `.humanizer-sync` tracking file does not exist, **When** the maintainer runs `make check-upstream`, **Then** the script reports an error with instructions to run the initial sync first.

---

### User Story 2 - Perform AI-assisted merge (Priority: P1)

A plugin maintainer wants to pull upstream changes into the local humanizer while preserving cc-prose-specific additions (rule-of-three density detection, custom filler phrases). They run the `/update-humanizer` Claude Code command, which performs an intelligent merge, updates the tracking file, and generates a sync report.

**Why this priority**: This is the core value proposition. Intelligent merge with local preservation is what differentiates this from a blind copy.

**Independent Test**: Run `/update-humanizer` against a known upstream delta and verify the merged SKILL.md contains both upstream additions and preserved local content.

**Acceptance Scenarios**:

1. **Given** upstream has new pattern categories, **When** the maintainer runs `/update-humanizer`, **Then** the new categories are added to the local SKILL.md while all local additions remain intact.
2. **Given** upstream has modified an existing category that also has local additions, **When** the maintainer runs `/update-humanizer`, **Then** the upstream improvements are merged in and the local additions are preserved, with any conflicts flagged in the sync report.
3. **Given** a successful merge completes, **When** the command finishes, **Then** the `.humanizer-sync` file is updated with the new upstream commit SHA and today's date.
4. **Given** a successful merge completes, **When** the command finishes, **Then** a sync report is generated at `docs/sync-reports/sync-YYYY-MM-DD.md` documenting what was integrated and what was preserved.

---

### User Story 3 - Establish initial baseline (Priority: P2)

A new contributor or first-time setup needs to establish the initial sync baseline. The tracking file is created with the current upstream HEAD, marking the starting point for future delta tracking.

**Why this priority**: Required for first use, but only happens once per project setup.

**Independent Test**: Run initial sync on a fresh clone and verify `.humanizer-sync` is created with correct upstream commit and date.

**Acceptance Scenarios**:

1. **Given** no `.humanizer-sync` file exists, **When** the maintainer runs `/update-humanizer`, **Then** the file is created with the current upstream HEAD commit SHA, today's date, and metadata about local additions to preserve.
2. **Given** the initial sync completes, **When** the maintainer inspects the tracking file, **Then** it contains `upstream_repo`, `last_sync_commit`, `last_sync_date`, and `modified_skills` fields.

---

### User Story 4 - Review sync history (Priority: P3)

A maintainer wants to understand what was changed during past syncs, what was integrated from upstream, and what local additions were preserved. They read the sync reports in `docs/sync-reports/`.

**Why this priority**: Audit trail is valuable but not blocking for core functionality.

**Independent Test**: After performing a sync, verify a report file exists with the expected structure and content.

**Acceptance Scenarios**:

1. **Given** a sync has been performed, **When** the maintainer reads `docs/sync-reports/sync-YYYY-MM-DD.md`, **Then** the report contains the upstream commit range, per-category change details, and what local additions were preserved.

---

### Edge Cases

- What happens when the upstream repo is unreachable (network failure)? The check and merge commands report a clear error and do not modify any local files.
- What happens when the upstream repo has been force-pushed or rebased, making the last sync commit invalid? The check script detects the missing commit and reports that a manual baseline reset is needed.
- What happens when local additions have been accidentally removed? The merge command compares against the `modified_skills` metadata and warns if expected local sections are missing before proceeding.
- What happens when two syncs are performed on the same day? The sync report filename includes a suffix (e.g., `sync-2026-06-12-2.md`) to avoid overwriting.

## Clarifications

### Session 2026-06-12

- Q: How are local additions identified for merge preservation? → A: The `modified_skills` metadata in `.humanizer-sync` lists section headings containing local additions. The merge agent reads this metadata to know what to preserve. No inline markers in SKILL.md are needed.
- Q: What network strategy should the check script use? → A: Prefer `gh api` for speed (no clone needed). Fall back to `git clone --depth 1` (shallow clone) when `gh` is unavailable. Clean up temp directories in both paths.
- Q: What structure should sync reports follow? → A: Follow the cc-spex pattern: upstream commit range, per-file change summary, changes integrated, local additions preserved, conflicts (if any), and action items.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST maintain a `prose/.humanizer-sync` JSON tracking file that records upstream repo URL, last synced commit SHA, last sync date, and metadata about local modifications to preserve.
- **FR-002**: System MUST provide a `scripts/check-upstream-changes.sh` script that compares the local tracking state against the current upstream HEAD and reports changes without modifying local files.
- **FR-003**: System MUST provide a `make check-upstream` Makefile target that invokes the check script.
- **FR-004**: System MUST provide a `prose/commands/update-humanizer.md` Claude Code command that performs AI-assisted merge of upstream changes while preserving local additions.
- **FR-005**: The merge command MUST update the `.humanizer-sync` tracking file with the new upstream commit SHA and sync date after a successful merge.
- **FR-006**: The merge command MUST generate a sync report at `docs/sync-reports/sync-YYYY-MM-DD.md` after each sync.
- **FR-007**: The merge command MUST also update the canonical copy at `~/.claude/skills/humanizer/SKILL.md` to keep it aligned with the plugin copy.
- **FR-008**: System MUST replace the existing `make sync-humanizer` target (blind copy) with the new `make check-upstream` target.
- **FR-009**: The `.humanizer-sync` tracking file MUST document which local additions need to be preserved during merges by listing section headings containing local content (rule-of-three density detection, custom filler phrase entries) in the `modified_skills` metadata.
- **FR-010**: The check script MUST prefer `gh api` for upstream comparison when available, falling back to a shallow `git clone --depth 1` to a temporary directory, and clean up temp directories after use.
- **FR-011**: The merge command MUST handle the initial sync case (no tracking file exists) by creating the baseline tracking file.

### Key Entities

- **Tracking File** (`.humanizer-sync`): JSON document storing sync state. Contains upstream_repo URL, last_sync_commit SHA, last_sync_date, and modified_skills metadata.
- **Sync Report** (`docs/sync-reports/sync-YYYY-MM-DD.md`): Markdown document following the cc-spex pattern with sections for: upstream commit range, per-file change summary, changes integrated, local additions preserved, conflicts (if any), and action items.
- **Upstream Repo** (blader/humanizer): The canonical community-maintained humanizer. Only `SKILL.md` is tracked for sync purposes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Maintainer can determine upstream sync status in under 30 seconds by running a single command.
- **SC-002**: All upstream pattern additions are correctly integrated without losing any local cc-prose additions after a merge.
- **SC-003**: Every sync produces an audit trail documenting what changed, enabling review of any past sync decision.
- **SC-004**: The old blind-copy workflow (`make sync-humanizer`) is fully replaced, eliminating the risk of accidental local addition loss.

## Out of Scope

- Bidirectional sync (pushing local additions back upstream to blader/humanizer)
- Automatic sync on plugin install or update
- Syncing files beyond `SKILL.md` from the upstream repo
- Resolving merge conflicts automatically without human review when conflicts are detected
- Version pinning or tracking multiple upstream branches

## Dependencies

- `git` - Required for shallow clone fallback and commit history inspection
- `gh` CLI - Preferred for fast upstream checks via GitHub API (optional, falls back to git)
- `jq` - Required for reading and writing the `.humanizer-sync` JSON tracking file
- Claude Code - Required for the `/update-humanizer` AI-assisted merge command

## Assumptions

- The upstream repo (blader/humanizer) remains publicly accessible on GitHub and uses a standard git workflow (no force-pushes on main).
- The `gh` CLI is available for API access to check upstream state. The check script falls back to `git clone` if `gh` is unavailable.
- Claude Code is available for running the `/update-humanizer` merge command. The check script works without Claude Code.
- The canonical local copy at `~/.claude/skills/humanizer/SKILL.md` continues to exist and should be kept in sync with the plugin copy.
- Local additions are identifiable via the `modified_skills` metadata in `.humanizer-sync`, which lists section headings containing local content. No inline markers in SKILL.md are needed.
