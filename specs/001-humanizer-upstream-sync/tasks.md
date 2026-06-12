# Tasks: Humanizer Upstream Sync

**Input**: Design documents from `/specs/001-humanizer-upstream-sync/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Create directory structure and initial tracking file

- [ ] T001 Create `docs/sync-reports/` directory with `.gitkeep`
- [ ] T002 Create initial `prose/.humanizer-sync` JSON tracking file with baseline data per data-model.md schema, setting `last_sync_commit` to current upstream HEAD (`9600f2b7241cb4eed6ad803abee5ea01d67fe8e4`), `last_sync_date` to today, and `modified_skills` metadata listing local additions (rule-of-three density in category 10, filler phrases in category 22)

---

## Phase 2: User Story 1 - Check for upstream changes (Priority: P1)

**Goal**: Maintainer can run a single command to see if upstream has new commits since last sync.

**Independent Test**: Run `make check-upstream` and verify it reports upstream status correctly.

- [ ] T003 [US1] Create `scripts/check-upstream-changes.sh` that reads `prose/.humanizer-sync`, extracts `last_sync_commit`, checks for `gh` CLI availability, and queries upstream commit state via `gh api repos/blader/humanizer/commits/main` (or falls back to `git clone --depth 1` to a temp dir). Output: commit count since last sync, commit messages, and diff summary for SKILL.md. Handle edge cases: missing tracking file (error with instructions), unreachable upstream (error without modifying local files), invalid last_sync_commit (suggest baseline reset). Clean up temp directories on exit via trap.
- [ ] T004 [US1] Update `Makefile`: replace `sync-humanizer` target with `check-upstream` target that invokes `scripts/check-upstream-changes.sh`. Update `.PHONY` declaration and `help` target text.

---

## Phase 3: User Story 2 - AI-assisted merge (Priority: P1)

**Goal**: Maintainer can merge upstream changes while preserving local cc-prose additions via a Claude Code command.

**Independent Test**: Run `/update-humanizer` and verify SKILL.md has upstream additions while local sections remain intact.

- [ ] T005 [US2] Create `prose/commands/update-humanizer.md` Claude Code command. The command must: (1) Read `prose/.humanizer-sync` for current state. (2) Clone upstream to temp dir and extract changes since `last_sync_commit` as a patch. (3) Read the `modified_skills[].local_additions` metadata to identify sections to preserve. (4) Instruct the AI merge agent to apply upstream changes to `prose/skills/humanizer/SKILL.md` while preserving listed local sections. (5) Handle initial sync case (no tracking file) by creating baseline. (6) After successful merge, update `prose/.humanizer-sync` with new commit SHA and date. (7) Copy merged file to `~/.claude/skills/humanizer/SKILL.md` (canonical copy). (8) Generate sync report at `docs/sync-reports/sync-YYYY-MM-DD.md` following the template from research.md R4. (9) Handle same-day duplicate reports with suffix. (10) Commit changes with descriptive message.

---

## Phase 4: User Story 3 - Initial baseline (Priority: P2)

**Goal**: First-time setup creates the tracking file baseline.

**Independent Test**: Delete `.humanizer-sync`, run `/update-humanizer`, verify tracking file is created with correct upstream HEAD.

*Note: This is handled by T005's initial sync case (step 5 in the merge command). No separate task needed.*

---

## Phase 5: User Story 4 - Review sync history (Priority: P3)

**Goal**: Maintainer can read past sync reports to understand what changed.

**Independent Test**: After a sync, verify `docs/sync-reports/sync-YYYY-MM-DD.md` exists with expected structure.

*Note: This is handled by T005's sync report generation (step 8 in the merge command). No separate task needed.*

---

## Phase 6: Polish & Cross-Cutting

**Purpose**: Documentation and cleanup

- [ ] T006 Update `README.md` to document the new sync workflow: remove references to `make sync-humanizer`, add instructions for `make check-upstream` and `/update-humanizer` command
- [ ] T007 [P] Update `CLAUDE.md` "Humanizer Source" section to reference the new sync mechanism instead of the old `make sync-humanizer` workflow

---

## Dependencies

```text
T001 ──→ T002 ──→ T003 ──→ T004
                    │
                    └──→ T005
                          │
              T006 ←──────┤
              T007 ←──────┘
```

- T001, T002: Setup (sequential, T002 depends on T001 for directory)
- T003: Depends on T002 (needs tracking file to read)
- T004: Depends on T003 (Makefile target invokes the script)
- T005: Depends on T002 (needs tracking file schema established)
- T006, T007: Can run in parallel after T005 is complete

## Parallel Execution

- T006 and T007 can run in parallel (different files)
- T003 and T005 could start in parallel after T002 (different files, both read tracking file)

## Implementation Strategy

**MVP**: T001-T004 (check upstream status). This delivers immediate value by letting maintainers know when upstream has changes, without any merge functionality yet.

**Full feature**: T005 adds the merge command, T006-T007 update documentation.
