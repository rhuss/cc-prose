# Tasks: Self-Audit Rewrite Loop

**Input**: Design documents from `/specs/004-self-audit-rewrite-loop/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not requested in the feature specification. No test tasks included.

**Organization**: Tasks are grouped by user story. This feature modifies 2 existing SKILL.md files; there is no project setup or foundational infrastructure to build.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No setup needed. This feature modifies existing SKILL.md files only. No new files, dependencies, or project initialization required.

*(No tasks in this phase)*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational work needed. Both skills are self-contained SKILL.md files; the self-audit prompt pattern is embedded inline in each skill rather than shared.

*(No tasks in this phase)*

**Checkpoint**: Ready to begin user story implementation.

---

## Phase 3: User Story 1 - Humanizer Catches Subtle AI Tells on Second Pass (Priority: P1) MVP

**Goal**: Formalize the humanizer's existing rudimentary self-audit into a structured flow with false-positive awareness, correction bound, and updated output format.

**Independent Test**: Run the humanizer on AI-generated text and verify that (a) the final output addresses issues beyond individual pattern violations, (b) self-audit findings appear after the content in a labeled section, (c) the intermediate draft is not shown, and (d) no em-dashes or en-dashes are present.

### Implementation for User Story 1

- [X] T001 [US1] Restructure the "Process and Output" section in prose/skills/humanizer/SKILL.md to implement the formalized self-audit flow. Replace current steps 1-4 (lines 596-601) and the delivery line (line 601) with the new flow: (1) Read input and identify patterns, (2) Write draft rewrite (pattern-based, internal only), (3) Self-audit using the single open-ended adversarial question "What makes this still obviously AI-generated?" with explicit focus on higher-order signals (rhythm, cadence, structure, tone, specificity, emotional range) per FR-006, (4) If findings exist: perform final rewrite addressing tells; if no findings: skip rewrite and report "no additional AI tells found" per FR-009, (5) Re-validate final rewrite against all pattern rules, (6) If new violations found: perform exactly one correction pass, then deliver as-is per FR-010, (7) Deliver: final rewrite only (not draft per FR-003), self-audit findings after content in a clearly labeled section, and change summary. The draft must not be shown to the user. When no self-audit findings exist, include "No additional AI tells found." Include inline false-positive guidance per FR-007: "Do not flag: intentional repetition for emphasis, rhetorical list structures, voice-consistent traits, genuine asides and self-corrections, mixed feelings or unresolved tension, short emphatic sentences for effect, specific concrete details, common transition words in isolation, formal vocabulary matching the content's register." Add em-dash/en-dash verification in the final rewrite step per FR-008.

- [X] T002 [US1] Update the full example section (lines 606-648) in prose/skills/humanizer/SKILL.md to demonstrate the new output format. The current example already shows draft, bullets, and final rewrite. Restructure to show: (1) the draft rewrite labeled as internal/not shown, (2) the self-audit question and findings as bullets, (3) the final rewrite as the primary output, (4) findings appearing after the final rewrite in a labeled section, (5) a change summary. Ensure the example is consistent with FR-003 (final only to user) and FR-009 (conditional rewrite).

- [X] T003 [US1] Update humanizer metadata and references in prose/skills/humanizer/SKILL.md. Bump version from 2.8.0 to 2.9.0 in the frontmatter. Update the introductory paragraph (line 35) that references "Process and Output" if the section heading or structure changed.

**Checkpoint**: Humanizer self-audit is fully functional. Run the humanizer on AI-generated text and verify acceptance scenarios 1-3 from the spec.

---

## Phase 4: User Story 2 - Content-Generator Self-Audits After Generation (Priority: P2)

**Goal**: Add a self-audit step to the content-generator, mirroring the humanizer's flow: generate, self-validate, self-audit, rewrite (if findings), deliver.

**Independent Test**: Generate content and verify that (a) the self-audit step runs after rule-based self-validation, (b) AI tells in rhythm/structure/tone are caught and addressed, (c) the existing self-validate still runs, and (d) findings appear after content in the output.

### Implementation for User Story 2

- [X] T004 [US2] Add new "Step 6b: Adversarial Self-Audit" section to prose/skills/content-generator/SKILL.md, inserted between existing Step 6 (Self-Validation, around line 423) and Step 7 (Present Content, around line 511). The new step must: (1) Use the same open-ended adversarial question as the humanizer: "What makes this still obviously AI-generated?", (2) Focus on higher-order signals per FR-006, not individual pattern rules (those are already checked in Step 6), (3) Include inline false-positive guidance per FR-007 matching the humanizer's list, (4) Explicitly reference Step 5b's protected categories and state that protected human writing signals must not be flagged, (5) If findings exist: perform a distinct rewrite pass addressing them before delivery, (6) If no findings: skip rewrite and note "no additional AI tells found" per FR-009.

- [X] T005 [US2] Modify Step 7 output format in prose/skills/content-generator/SKILL.md to include self-audit findings. Update the output template (around lines 517-533) to add a "Self-audit findings" section after the generated content and before the "Quality assurance applied" block. When findings exist, list them as brief bullets. When no findings exist, include "No additional AI tells found." Add "Self-audit: [findings count] tells caught and addressed" or "Self-audit: No additional AI tells found" to the QA checklist.

- [X] T006 [US2] Update content-generator metadata in prose/skills/content-generator/SKILL.md. Bump version from 1.1.0 to 1.2.0 in the frontmatter. Add "Adversarial self-audit for higher-order AI tells" to the capabilities list. Ensure the "Your Mission" section (around line 66) mentions the self-audit step in the workflow summary (between self-validate and deliver).

**Checkpoint**: Content-generator self-audit is fully functional. Generate content and verify acceptance scenarios 1-3 from the spec.

---

## Phase 5: User Story 3 - Self-Audit Respects Human Signals and False Positives (Priority: P3)

**Goal**: Verify that the self-audit in both skills correctly identifies deliberate stylistic choices as false positives and does not flag or alter them.

**Independent Test**: Run the humanizer or content-generator on text with known deliberate stylistic choices (intentional repetition, rhetorical lists, preservation markers) and verify the self-audit does not flag those sections.

### Implementation for User Story 3

- [X] T007 [US3] Verify and refine the inline false-positive guidance in the humanizer self-audit prompt (prose/skills/humanizer/SKILL.md). Cross-reference with the existing "What NOT to flag (false positives)" section (lines 559-576) to ensure all 13 categories are represented in the self-audit guidance. Cross-reference with "Signs of human writing (preserve these)" section (lines 579-589) to ensure all 7 preservation signals are protected. Add any missing categories to the inline guidance. Ensure the self-audit explicitly states: voice profile traits must not be flagged as AI tells.

- [X] T008 [US3] Verify and refine the inline false-positive guidance in the content-generator self-audit prompt (prose/skills/content-generator/SKILL.md). Cross-reference with "Preserve Human Writing Signals" (Step 5b, lines 409-419) to ensure all 6 protected signal categories are explicitly referenced in Step 6b. Ensure the self-audit prompt in Step 6b includes an explicit cross-reference: "Do NOT flag any content that falls into the protected categories defined in Step 5b." Verify that voice-consistent traits (matching the formality/personality settings from the voice profile) are protected.

**Checkpoint**: Both skills correctly handle false positives. Test with text containing intentional repetition and rhetorical list structures.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Consistency and integration verification across both modified skills.

- [X] T009 Cross-validate self-audit consistency between humanizer and content-generator. Verify both skills use the identical adversarial question wording. Verify both have equivalent false-positive guidance lists. Verify output format (findings after content) is consistent. Verify both handle the "no findings" case identically (skip rewrite, report "no additional AI tells found").

- [X] T010 Review prose/.humanizer-sync to determine if the "Process and Output" section changes need to be tracked as a local modification for upstream sync purposes. If the sync file tracks section-level changes, add an entry noting the self-audit formalization as a local addition that must be preserved during upstream merges from blader/humanizer.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Skipped (no setup needed)
- **Foundational (Phase 2)**: Skipped (no foundational work needed)
- **User Story 1 (Phase 3)**: Can start immediately. This is the MVP.
- **User Story 2 (Phase 4)**: Can start after Phase 3. Mirrors the humanizer pattern, so having US1 complete provides a reference.
- **User Story 3 (Phase 5)**: Depends on both Phase 3 and Phase 4. Verifies false-positive handling in both skills.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies. Start immediately.
- **User Story 2 (P2)**: Soft dependency on US1 (uses same pattern as reference). Can start independently but benefits from US1 being done first.
- **User Story 3 (P3)**: Depends on US1 and US2 (verifies false-positive handling in both).

### Within Each User Story

- T001 before T002 (restructure before updating example)
- T002 before T003 (example before metadata bump)
- T004 before T005 (add step before modifying output)
- T005 before T006 (output format before metadata bump)
- T007 and T008 are parallelizable [P] (different files)

### Parallel Opportunities

- T007 and T008 can run in parallel (different files: humanizer vs content-generator)
- T009 and T010 can run in parallel (different concerns: consistency vs sync tracking)
- US1 and US2 could theoretically run in parallel (different files), but sequential is recommended since US2 mirrors US1's pattern

---

## Parallel Example: User Story 3

```bash
# Launch false-positive verification for both skills together:
Task: "Verify false-positive guidance in humanizer SKILL.md"
Task: "Verify false-positive guidance in content-generator SKILL.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 (T001-T003)
2. **STOP and VALIDATE**: Run humanizer on AI-generated text, verify self-audit catches higher-order tells
3. Verify output format: final rewrite only, findings after content

### Incremental Delivery

1. User Story 1 (humanizer) → Test independently → Core value delivered
2. User Story 2 (content-generator) → Test independently → Both skills covered
3. User Story 3 (false-positive refinement) → Test with deliberate stylistic choices → Safety verified
4. Polish → Cross-validate consistency → Feature complete

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All changes are to existing SKILL.md files (no new files created)
- No automated tests exist for SKILL.md behavior; verification is manual
- The humanizer already has a rudimentary self-audit; US1 formalizes it
- The content-generator has no self-audit; US2 adds one from scratch
- Commit after each completed user story phase
