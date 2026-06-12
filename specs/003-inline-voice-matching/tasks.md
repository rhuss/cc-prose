# Tasks: Inline Voice-Matching

**Input**: Design documents from `specs/003-inline-voice-matching/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md

**Organization**: Tasks grouped by skill file since changes are isolated to two SKILL.md files.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Humanizer Updates (US1, US2, US4, US5)

**Goal**: Document voice source priority order and add cross-reference to voice-extractor in the humanizer's existing Voice Calibration section.

**Independent Test**: Invoke the humanizer with an inline sample while a voice profile is configured. The humanizer should use the inline sample and mention voice-extractor for persistent profiles.

- [x] T001 [US4] Add "Voice source priority" subsection after "How to provide a sample" in prose/skills/humanizer/SKILL.md documenting the priority order: inline sample > configured voice profile > default behavior
- [x] T002 [US1] Add file validation guidance to the "How to provide a sample" subsection in prose/skills/humanizer/SKILL.md: when a referenced file doesn't exist, is unreadable, or is binary, warn and fall back to the next voice source
- [x] T003 [US5] Add cross-reference line at end of Voice Calibration section in prose/skills/humanizer/SKILL.md mentioning the voice-extractor capability for persistent reusable profiles

**Checkpoint**: Humanizer Voice Calibration section is complete with priority order, file validation, and cross-reference.

---

## Phase 2: Content-Generator Updates (US3, US4, US5)

**Goal**: Add inline voice-matching capability to the content-generator, matching the humanizer's feature set.

**Independent Test**: Invoke the content-generator with an inline writing sample and verify the generated content matches the sample's voice characteristics.

- [x] T004 [P] [US3] Add "Voice Calibration (Optional)" section after "Your Mission" section (before "Configuration Loading") in prose/skills/content-generator/SKILL.md with: six analysis dimensions (sentence length, word choice, paragraph openings, punctuation, recurring phrases, transitions), two input methods (inline text, file reference), file validation (warn + fall back for missing/binary files), and cross-reference to voice-extractor
- [x] T005 [US4] Modify "Step 2: Apply Voice Profile" in prose/skills/content-generator/SKILL.md to add inline sample as highest priority: check for inline sample first, if present use it and skip YAML profile loading, if not present continue with existing voice profile or auto-detection behavior
- [x] T006 [US3] Add note to Step 2 in prose/skills/content-generator/SKILL.md that project-level style rules (CLAUDE.md, copyedit config) override inline sample voice for specific prohibited patterns

**Checkpoint**: Content-generator has full inline voice-matching parity with the humanizer.

---

## Phase 3: Polish & Cross-Cutting

**Purpose**: Update tracking documents to reflect completion.

- [x] T007 [P] Update brainstorm/02-inline-voice-matching.md status from "active" to "spec-created" and update brainstorm/00-overview.md table
- [x] T008 Update brainstorm/00-overview.md to resolve the three open questions from brainstorm 02 (content-generator voice matching: yes, voice-extractor mention: yes, inline sample vs profile priority: inline wins)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Humanizer)**: No dependencies, can start immediately
- **Phase 2 (Content-Generator)**: No dependencies on Phase 1 (different file), can run in parallel
- **Phase 3 (Polish)**: Depends on Phase 1 and Phase 2 completion

### Within Each Phase

- Phase 1: T001 → T002 → T003 (sequential, same section of same file)
- Phase 2: T004 → T005 → T006 (sequential, same file, T005 depends on section from T004)
- Phase 3: T007 and T008 can run in parallel [P]

### Parallel Opportunities

- Phase 1 and Phase 2 operate on different files and can run fully in parallel
- T007 and T008 are independent documentation updates

---

## Parallel Example: Phase 1 + Phase 2

```text
# These can run simultaneously (different files):
Agent A: T001, T002, T003 in prose/skills/humanizer/SKILL.md
Agent B: T004, T005, T006 in prose/skills/content-generator/SKILL.md
```

---

## Implementation Strategy

### MVP First (Phase 1 Only)

1. Complete Phase 1: Humanizer priority order + cross-reference
2. **STOP and VALIDATE**: The humanizer already has inline voice matching from upstream. With priority order documented, it's a complete feature.

### Full Delivery

1. Phase 1: Humanizer updates (3 tasks)
2. Phase 2: Content-generator updates (3 tasks, can parallel with Phase 1)
3. Phase 3: Documentation cleanup (2 tasks)
4. Total: 8 tasks across 4 files

---

## Notes

- No new files created. All changes are edits to existing SKILL.md and brainstorm files.
- The humanizer already has the Voice Calibration section from upstream v2.8.0. Phase 1 only adds priority documentation, file validation, and cross-reference.
- The content-generator's new Voice Calibration section mirrors the humanizer's structure but is adapted for content generation context.
- Tests are not applicable: SKILL.md files are LLM instruction documents validated by manual invocation, not automated tests.
