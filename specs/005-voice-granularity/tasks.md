# Tasks: Voice Profile Granularity Refinement

**Input**: Design documents from `specs/005-voice-granularity/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not explicitly requested. No test tasks included.

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

---

## Phase 1: Schema Foundation (Voice Templates)

**Purpose**: Update all 8 built-in voice templates with new parameters. This is the foundation all skill changes depend on.

- [x] T001 [P] Add new parameters (confidence, paragraph_patterns, sentence_starters, emotional_range, self_correction, directness, specificity) to prose/knowledge-base/voice-templates/technical.yaml
- [x] T002 [P] Add new parameters to prose/knowledge-base/voice-templates/conversational.yaml
- [x] T003 [P] Add new parameters to prose/knowledge-base/voice-templates/analytical.yaml
- [x] T004 [P] Add new parameters to prose/knowledge-base/voice-templates/narrative.yaml
- [x] T005 [P] Add new parameters to prose/knowledge-base/voice-templates/pov.yaml
- [x] T006 [P] Add new parameters to prose/knowledge-base/voice-templates/reasoning.yaml
- [x] T007 [P] Add new parameters to prose/knowledge-base/voice-templates/reference.yaml
- [x] T008 [P] Add new parameters to prose/knowledge-base/voice-templates/tutorial.yaml

**Values per template** (from plan.md):

| Template | confidence | opening_style | transition_style | sentence_starters | emotional_range | self_correction | directness | specificity | paragraph avg |
|----------|-----------|---------------|-----------------|-------------------|----------------|----------------|------------|-------------|---------------|
| technical | 0.6 | direct | explicit | varied | flat | false | balanced | concrete | medium |
| conversational | 0.5 | anecdotal | organic | varied | dynamic | true | balanced | concrete | short |
| analytical | 0.7 | direct | explicit | formal-lead | flat | false | balanced | concrete | long |
| narrative | 0.5 | anecdotal | organic | varied | dynamic | true | balanced | concrete | medium |
| pov | 0.8 | contextual | organic | varied | dynamic | true | blunt | concrete | medium |
| reasoning | 0.6 | contextual | explicit | formal-lead | moderate | false | balanced | balanced | long |
| reference | 0.8 | direct | explicit | formal-lead | flat | false | balanced | concrete | medium |
| tutorial | 0.4 | contextual | organic | pronoun-heavy | moderate | true | hedged | concrete | short |

**Checkpoint**: All 8 templates updated with consistent schema. No `measurements` section (extractor-only).

---

## Phase 2: User Story 1 - Content Generator Consumes New Parameters (Priority: P1)

**Goal**: The content-generator skill reads and applies all new voice parameters during content generation.

**Independent Test**: Generate content with a profile using `confidence: 0.9` and `directness: blunt`, verify output has no hedging qualifiers.

### Implementation for User Story 1

- [x] T009 [US1] Add `confidence` parameter interpretation to the voice application section (Step 3) in prose/skills/content-generator/SKILL.md: map 0.0-0.3 to heavy hedging, 0.4-0.6 to moderate, 0.7-1.0 to assertive
- [x] T010 [US1] Add `paragraph_patterns` consumption section in prose/skills/content-generator/SKILL.md: instructions for opening_style (direct/contextual/anecdotal/varied), transition_style (explicit/organic/minimal), avg_length (short/medium/long)
- [x] T011 [US1] Add `sentence_starters` to sentence pattern instructions in prose/skills/content-generator/SKILL.md: pronoun-heavy starts most sentences with I/You/We, varied mixes approaches, formal-lead uses topic-first constructions
- [x] T012 [US1] Add `emotional_range`, `self_correction`, `directness` to personality injection section in prose/skills/content-generator/SKILL.md
- [x] T013 [US1] Add `specificity` to elaboration instructions in prose/skills/content-generator/SKILL.md: abstract allows generalizations, concrete demands examples and details, balanced mixes both
- [x] T014 [US1] Add old-format detection logic to voice profile loading in prose/skills/content-generator/SKILL.md: if profile lacks `confidence` field, warn user and offer to add defaults

**Checkpoint**: Content-generator respects all new params. Test by creating content with extreme values (confidence: 0.9, directness: blunt).

---

## Phase 3: User Story 2 - Humanizer Respects New Parameters (Priority: P1)

**Goal**: The humanizer skill preserves and reinforces new voice dimensions during rewriting.

**Independent Test**: Humanize AI text with `confidence: 0.3` and `directness: hedged`, verify rewrite preserves appropriate hedging.

### Implementation for User Story 2

- [x] T015 [US2] Add `confidence` and `directness` to voice matching guidance in prose/skills/humanizer/SKILL.md: low confidence preserves hedging, high confidence removes it, directness controls delivery softness
- [x] T016 [US2] Add `paragraph_patterns` to rewrite guidance in prose/skills/humanizer/SKILL.md: respect opening_style preferences, adjust transition density per transition_style setting
- [x] T017 [US2] Add `emotional_range`, `self_correction`, `specificity` to personality preservation in prose/skills/humanizer/SKILL.md
- [x] T018 [US2] Add old-format detection logic to voice profile loading in prose/skills/humanizer/SKILL.md: same logic as content-generator (check for `confidence` field)

**Checkpoint**: Humanizer respects all new params during rewriting. Test with low-confidence profile on assertive text.

---

## Phase 4: User Story 3 - Voice Extractor Populates Measurements (Priority: P2)

**Goal**: The voice-extractor computes and populates the `measurements` section from writing samples.

**Independent Test**: Run extractor on a 3000+ word corpus, verify measurements section has all 10 fields populated with accurate values.

### Implementation for User Story 3

- [x] T019 [US3] Add measurement computation step to the extraction workflow in prose/skills/voice-extractor/SKILL.md: after parameter extraction, compute all 10 measurement fields (sentence_length_mean, sentence_length_stdev, paragraph_length_mean, passive_voice_pct, hedge_density_per_1000, connector_variety, concrete_abstract_ratio, punctuation_entropy, one_sentence_paragraph_rate, contraction_rate_per_1000)
- [x] T020 [US3] Add `sample_confidence` computation to prose/skills/voice-extractor/SKILL.md: < 1000 words = low, 1000-5000 = medium, > 5000 = high
- [x] T021 [US3] Add measurements section to the output YAML template in prose/skills/voice-extractor/SKILL.md: include all 10 fields plus sample_confidence, with field descriptions as comments
- [x] T022 [US3] Add new human-readable parameter extraction logic for confidence, paragraph_patterns, sentence_starters, emotional_range, self_correction, directness, specificity in prose/skills/voice-extractor/SKILL.md

**Checkpoint**: Extractor produces complete profiles with new params and measurements section.

---

## Phase 5: User Story 4 - Self-Audit Validates Against Measurements (Priority: P2)

**Goal**: The self-audit subagent validates generated content against measurement targets and reports specific deviations.

**Independent Test**: Generate content with a profile with `measurements.sentence_length_stdev: 8.0`, produce uniform sentences, verify self-audit reports the specific deviation.

### Implementation for User Story 4

- [x] T023 [US4] Update self-audit subagent prompt in prose/skills/content-generator/SKILL.md: when measurements section is present, append measurement validation instructions with thresholds (>25% deviation = flagged, 10-25% = informational, <10% = pass)
- [x] T024 [US4] Update self-audit subagent prompt in prose/skills/humanizer/SKILL.md: same measurement validation logic as content-generator
- [x] T025 [US4] Add low-confidence measurement handling: when sample_confidence is "low", use relaxed threshold (>50% = flagged) and prefix findings with "advisory"

**Checkpoint**: Self-audit reports concrete numeric deviations when measurements present, runs normally without measurements.

---

## Phase 6: User Story 5 - Old-Format Auto-Detection (Priority: P3)

**Goal**: Skills detect old-format profiles and offer migration with sensible defaults.

**Independent Test**: Load a profile without `confidence` field, verify migration prompt appears.

### Implementation for User Story 5

- [x] T026 [US5] Verify old-format detection already added in T014 (content-generator) and T018 (humanizer), ensure consistent migration defaults across both skills
- [x] T027 [US5] Add fallback behavior documentation: when user declines migration, skills use defaults silently (confidence: 0.5, directness: balanced, emotional_range: moderate, self_correction: false, specificity: balanced, paragraph_patterns: medium/varied/organic, sentence_starters: varied)

**Checkpoint**: Old profiles load without errors in both content-generator and humanizer.

---

## Phase 7: User Story 6 - Voice Architect New Schema (Priority: P3)

**Goal**: Voice architect creates profiles with the full expanded schema.

**Independent Test**: Run voice-architect create workflow, verify output YAML contains all new parameters, no measurements section.

### Implementation for User Story 6

- [x] T028 [US6] Add questions for new parameters to the interactive create workflow in prose/skills/voice-architect/SKILL.md: confidence (slider 0.0-1.0), paragraph avg_length, opening_style, transition_style, sentence_starters, emotional_range, self_correction, directness, specificity
- [x] T029 [US6] Add new parameters to the edit workflow in prose/skills/voice-architect/SKILL.md: support editing individual new params
- [x] T030 [US6] Ensure voice-architect never generates a measurements section (add explicit note: measurements are extractor-only)

**Checkpoint**: Architect produces complete profiles in updated schema without measurements.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Pre-validator update and final consistency checks.

- [x] T031 Add new parameter voice consistency checks to prose/skills/pre-validator/SKILL.md: validate confidence, directness, emotional_range, specificity against generated content
- [x] T032 Add measurement deviation check to prose/skills/pre-validator/SKILL.md: when measurements present, report deviations using same thresholds as self-audit
- [x] T033 Verify all 8 templates pass schema validation: each template has all required new fields with valid enum/range values
- [x] T034 Add measurements-only profile handling to prose/skills/content-generator/SKILL.md and prose/skills/humanizer/SKILL.md: when a profile has a `measurements` section but no human-readable knobs (confidence, directness, etc.), derive reasonable defaults from measurements (e.g., high hedge_density_per_1000 implies low confidence) and warn that explicit parameters produce better results
- [x] T035 Add parameter validation at load time in prose/skills/content-generator/SKILL.md and prose/skills/humanizer/SKILL.md: validate that confidence is in [0.0, 1.0], directness is one of hedged/balanced/blunt, emotional_range is one of flat/moderate/dynamic, etc. Report the invalid field and value, fall back to defaults for invalid fields, continue processing
- [x] T036 Add error handling for corrupted/unreadable corpus files in prose/skills/voice-extractor/SKILL.md: skip unreadable files with a warning identifying each skipped file, continue processing remaining files. If all files are unreadable, report an error and produce no output
- [x] T037 Add measurement computation edge case handling in prose/skills/voice-extractor/SKILL.md: when corpus is too small or uniform to compute a metric (e.g., zero sentences for stdev, division by zero), omit that field from the measurements section rather than writing NaN or infinity
- [x] T038 Add non-interactive migration handling in prose/skills/content-generator/SKILL.md and prose/skills/humanizer/SKILL.md: when old-format detection triggers in a non-interactive context (piped input, CI), silently apply defaults without prompting and log an informational message noting the auto-migration

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Templates)**: No dependencies, can start immediately
- **Phase 2 (US1 Content-Generator)**: Depends on Phase 1 (needs templates for reference values)
- **Phase 3 (US2 Humanizer)**: Depends on Phase 1. Can run in parallel with Phase 2 (different file)
- **Phase 4 (US3 Voice-Extractor)**: Depends on Phase 1. Can run in parallel with Phase 2 and 3 (different file)
- **Phase 5 (US4 Self-Audit)**: Depends on Phase 2 and 3 (modifies same files as US1 and US2)
- **Phase 6 (US5 Old-Format)**: Depends on Phase 2 and 3 (verifies work done in those phases)
- **Phase 7 (US6 Voice-Architect)**: Depends on Phase 1. Can run in parallel with Phase 2-4 (different file)
- **Phase 8 (Polish)**: Depends on all previous phases

### Parallel Opportunities

- **Phase 1**: All 8 template tasks (T001-T008) can run in parallel
- **Phases 2, 3, 4, 7**: Can run in parallel (each modifies a different SKILL.md file)
- **Phase 5**: Must run after Phases 2 and 3 (appends to same files)

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: All 8 templates updated
2. Complete Phase 2: Content-generator consumes new params
3. Complete Phase 3: Humanizer respects new params
4. **STOP and VALIDATE**: Test both skills with new param profiles
5. This delivers the core value: new voice dimensions in generation and rewriting

### Incremental Delivery

1. Templates (Phase 1) -> Foundation ready
2. Content-generator + Humanizer (Phase 2-3) -> MVP: new params in both primary skills
3. Voice-extractor (Phase 4) + Self-audit (Phase 5) -> Measurements pipeline complete
4. Old-format + Architect + Pre-validator (Phase 6-8) -> Full schema support across all skills

---

## Notes

- All changes are to SKILL.md prompt files and YAML templates. No compiled code.
- Total tasks: 38
- Parallel template tasks: 8 (Phase 1)
- Parallel skill tasks: Phases 2, 3, 4, 7 can run concurrently (different files)
- MVP scope: Phases 1-3 (16 tasks) delivers core value
- T034-T038 added by plan review to cover spec error handling and edge cases
