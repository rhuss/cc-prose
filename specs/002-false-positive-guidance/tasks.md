# Tasks: False-Positive Guidance and Human Signal Preservation

**Input**: Design documents from `specs/002-false-positive-guidance/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md

**Tests**: Not requested. No test tasks generated.

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No project initialization needed. Both target files already exist. This phase is empty.

---

## Phase 2: Foundational (Category Count Update)

**Purpose**: Update the category count from 24 to 33 in both files. This is a prerequisite for subsequent changes because the detection guidance sections reference the correct count.

- [x] T001 [P] [US5] Update all references from "24" to "33" humanizer categories in prose/skills/pre-validator/SKILL.md
- [x] T002 [P] [US5] Update all references from "24" to "33" humanizer categories in prose/skills/content-generator/SKILL.md

**Checkpoint**: Both files reference the correct category count (33).

---

## Phase 3: User Story 1 - Pre-validator stops over-penalizing isolated tells (Priority: P1)

**Goal**: Isolated AI tells (single tell with no others in the same paragraph) are classified as LOW severity instead of their default severity.

**Independent Test**: Run `/prose:check` on content with a single em dash and no other AI tells. Verify severity is LOW and overall score is PASS.

### Implementation for User Story 1

- [x] T003 [US1] Add "Detection Guidance" section to prose/skills/pre-validator/SKILL.md after Phase 1 (AI Pattern Scan) containing the 12-item false-positive list, cluster-detection principle, and isolation-aware severity rules
- [x] T004 [US1] Modify Phase 1 severity classification instructions in prose/skills/pre-validator/SKILL.md to downgrade isolated tells (no other tells in the same paragraph) to LOW severity, with explicit stoplist exception (stoplist words remain CRITICAL regardless)

**Checkpoint**: Pre-validator treats isolated tells as LOW severity. Stoplist words remain CRITICAL.

---

## Phase 4: User Story 2 - Pre-validator escalates clustered tells (Priority: P1)

**Goal**: When 3+ different AI tell types co-occur in the same paragraph, each tell is restored to its original default severity (removing the isolation downgrade).

**Independent Test**: Run `/prose:check` on a paragraph with 3+ different tell types. Verify severity is escalated vs. the same tells spread across separate paragraphs.

### Implementation for User Story 2

- [x] T005 [US2] Add cluster detection rules to the "Detection Guidance" section in prose/skills/pre-validator/SKILL.md specifying: 3+ different tell types in the same paragraph triggers cluster mode, restoring each tell to its original default severity

**Checkpoint**: Pre-validator detects clusters and restores default severity. Two tells in the same paragraph do not trigger escalation. Three identical tell types do not trigger escalation.

---

## Phase 5: User Story 3 - Pre-validator recognizes human writing signals (Priority: P2)

**Goal**: The pre-validator detects and reports human writing signals (specific details, mixed feelings, self-corrections) as positive indicators in a dedicated report section.

**Independent Test**: Run `/prose:check` on content with specific real-world details and self-corrections. Verify the report includes a "Human Writing Signals" subsection listing detected signals.

### Implementation for User Story 3

- [x] T006 [US3] Add the 6-item human writing signals list to the "Detection Guidance" section in prose/skills/pre-validator/SKILL.md with detection instructions for each signal type
- [x] T007 [US3] Add "Human Writing Signals Detected" subsection to the report format template in prose/skills/pre-validator/SKILL.md positioned between LOW Priority Issues and Readability Metrics, with signal type, example found, and location columns

**Checkpoint**: Pre-validator report includes human writing signals section. Signals are informational and do not modify the numeric score.

---

## Phase 6: User Story 4 - Content-generator preserves human signals during self-validation (Priority: P2)

**Goal**: The content-generator's self-validation step does not reject output for isolated tells (no other tells in the entire output) and preserves human writing signals it deliberately added.

**Independent Test**: Run `/prose:write` with voice personality enabled. Verify that asides, self-corrections, and varied sentence rhythms survive self-validation.

### Implementation for User Story 4

- [x] T008 [US4] Add false-positive awareness to the Humanizer Pattern Validation subsection in Step 6 of prose/skills/content-generator/SKILL.md: do not reject output for a single isolated tell when no other tells exist in the entire output
- [x] T009 [US4] Add "Preserve Human Writing Signals" guidance after Step 5 (Inject Personality) in prose/skills/content-generator/SKILL.md listing the 6 human signal types and instructing self-validation to recognize and keep these patterns

**Checkpoint**: Content-generator preserves personality markers through self-validation. Isolated tells do not trigger rejection.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency and separation-of-concerns cleanup.

- [x] T010 Add FR-010 guidance (style rules vs AI detection separation) to the Detection Guidance sections in both prose/skills/pre-validator/SKILL.md and prose/skills/content-generator/SKILL.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: Empty, no work needed
- **Phase 2 (Foundational)**: No dependencies, can start immediately. T001 and T002 are parallel.
- **Phase 3 (US1)**: Depends on T001 (pre-validator category count updated)
- **Phase 4 (US2)**: Depends on T003 (Detection Guidance section must exist before adding cluster rules)
- **Phase 5 (US3)**: Depends on T003 (Detection Guidance section must exist before adding human signals)
- **Phase 6 (US4)**: Depends on T002 (content-generator category count updated). Independent of US1-US3.
- **Phase 7 (Polish)**: Depends on T003 and T009 (both Detection Guidance sections must exist)

### User Story Dependencies

- **US5 (P3, Phase 2)**: No dependencies. Runs first as foundational.
- **US1 (P1, Phase 3)**: Depends on US5 for pre-validator file. Creates the Detection Guidance section.
- **US2 (P1, Phase 4)**: Depends on US1 (adds to the Detection Guidance section US1 created).
- **US3 (P2, Phase 5)**: Depends on US1 (adds to the Detection Guidance section US1 created).
- **US4 (P2, Phase 6)**: Depends on US5 for content-generator file. Independent of US1-US3.

### Parallel Opportunities

- T001 and T002 are parallel (different files)
- T008 and T009 are parallel (different sections of the same file, but T009 adds new content after Step 5 while T008 modifies Step 6)
- US1-US3 (pre-validator) and US4 (content-generator) target different files and can run in parallel after foundational phase

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 2: Update category counts (T001, T002)
2. Complete Phase 3: Isolation downgrade (T003, T004)
3. Complete Phase 4: Cluster detection (T005)
4. **VALIDATE**: Pre-validator correctly handles isolated vs. clustered tells

### Incremental Delivery

1. Category count update (US5) -> foundation ready
2. Isolation downgrade (US1) -> false positives reduced
3. Cluster detection (US2) -> AI content still caught
4. Human signal reporting (US3) -> full detection guidance
5. Content-generator updates (US4) -> self-validation improved
6. Polish (cross-cutting) -> style/detection separation explicit

---

## Notes

- All tasks edit existing SKILL.md files. No new files are created.
- Two target files: `prose/skills/pre-validator/SKILL.md` and `prose/skills/content-generator/SKILL.md`
- The humanizer skill (`prose/skills/humanizer/SKILL.md`) is reference-only. Do not modify it.
- Stoplist supremacy is maintained throughout: stoplist words are always CRITICAL regardless of isolation or false-positive guidance.
