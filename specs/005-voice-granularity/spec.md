# Feature Specification: Voice Profile Granularity Refinement

**Feature Branch**: `005-voice-granularity`
**Created**: 2026-06-13
**Status**: Draft
**Input**: Brainstorm document `brainstorm/06-voice-granularity.md`

## Purpose

Current voice profiles capture broad strokes (formality, personality, contractions) but miss the finer dimensions that distinguish one human writer from another: how confident they sound, how they open paragraphs, whether they hedge or assert, how much emotional variation they allow. This feature adds those missing knobs to voice profiles, introduces a numeric `measurements` section derived from corpus analysis, and wires the expanded schema into every skill that consumes voice profiles. The result is generated prose that sounds like a specific person rather than a generic "natural" voice.

## User Scenarios & Testing

### User Story 1 - Content Creator Uses Expanded Voice Parameters (Priority: P1)

A content creator generates a blog post using the content-generator skill with a voice profile that includes the new parameters (confidence, paragraph patterns, directness, emotional range). The generated content reflects all specified voice dimensions, producing writing that sounds distinctly human and matches the intended personality.

**Why this priority**: The new human-readable parameters are the core deliverable. Without them, the other stories have nothing to consume.

**Independent Test**: Can be tested by creating a voice profile with the new parameters, generating content, and verifying the output matches the specified voice dimensions (e.g., assertive confidence produces text without hedging qualifiers).

**Acceptance Scenarios**:

1. **Given** a voice profile with `confidence: 0.9` and `directness: blunt`, **When** content is generated, **Then** the output contains no hedging qualifiers ("perhaps", "might", "somewhat") and uses direct assertions.
2. **Given** a voice profile with `paragraph_patterns.opening_style: anecdotal`, **When** content is generated, **Then** at least the opening paragraph begins with a specific example or story rather than a thesis statement.
3. **Given** a voice profile with `self_correction: true`, **When** content is generated, **Then** the output includes natural self-correction markers ("actually", "I mean", "well") at a rate that reads naturally (not forced).
4. **Given** a voice profile with `emotional_range: dynamic`, **When** content is generated, **Then** the output shows variation in emotional tone across paragraphs rather than maintaining a single flat register.

---

### User Story 2 - Humanizer Respects New Parameters During Rewriting (Priority: P1)

A user rewrites AI-generated text using the humanizer skill with a voice profile containing the new parameters. The humanizer preserves and reinforces the voice dimensions specified in the profile, rather than defaulting to a generic "natural" rewrite.

**Why this priority**: The humanizer is the other primary consumer of voice profiles. Both generation and rewriting must respect the expanded schema.

**Independent Test**: Can be tested by humanizing a block of AI-generated text with a profile specifying `confidence: 0.3` (heavily hedged) and verifying the rewrite preserves appropriate hedging rather than making everything assertive.

**Acceptance Scenarios**:

1. **Given** a voice profile with `confidence: 0.3` and `directness: hedged`, **When** text is humanized, **Then** the rewrite includes appropriate hedging language matching the specified confidence level.
2. **Given** a voice profile with `paragraph_patterns.transition_style: minimal`, **When** text with heavy transition words is humanized, **Then** explicit transitions ("Furthermore", "Moreover") are removed or replaced with paragraph breaks.
3. **Given** a voice profile with `specificity: concrete`, **When** abstract text is humanized, **Then** the rewrite replaces vague generalizations with specific examples or details where possible.

---

### User Story 3 - Voice Extractor Populates Measurements Section (Priority: P2)

A user runs the voice-extractor on a corpus of their writing samples. The extractor analyzes the corpus and populates the `measurements` section of the resulting voice profile with numeric targets (sentence length stats, hedge density, connector variety, etc.).

**Why this priority**: The measurements section enables the self-audit subagent to validate generated content against concrete numeric targets, closing the consistency gap.

**Independent Test**: Can be tested by running the extractor on a known writing corpus and verifying the measurements section contains accurate numeric values that match manual analysis of the same corpus.

**Acceptance Scenarios**:

1. **Given** a corpus of 5+ writing samples totaling 3000+ words, **When** the voice-extractor runs, **Then** the output profile contains a `measurements` section with all defined measurement fields populated.
2. **Given** a corpus with short, punchy sentences (avg 10 words, stdev 6), **When** the extractor runs, **Then** `measurements.sentence_length_mean` is within 2 words of the actual mean and `measurements.sentence_length_stdev` is within 1.5 of the actual stdev.
3. **Given** a corpus with heavy hedging language, **When** the extractor runs, **Then** `measurements.hedge_density_per_1000` reflects the actual hedging frequency.

---

### User Story 4 - Self-Audit Subagent Validates Against Measurements (Priority: P2)

During content generation or humanization, the self-audit subagent receives the measurements section (if present) alongside the draft text. It validates the draft against the numeric targets and reports concrete deviations.

**Why this priority**: Measurements without validation are inert data. The self-audit integration is what makes measurements actionable.

**Independent Test**: Can be tested by generating content with a profile that has measurements set to extreme values (e.g., `sentence_length_stdev: 12`) and verifying the self-audit flags the draft when it doesn't meet the target.

**Acceptance Scenarios**:

1. **Given** a voice profile with `measurements.sentence_length_stdev: 8.0`, **When** content is generated with uniform sentence lengths (stdev < 3), **Then** the self-audit reports the specific deviation ("sentence length stdev is 2.8, target is 8.0").
2. **Given** a voice profile with `measurements.passive_voice_pct: 5`, **When** content is generated with 25% passive voice, **Then** the self-audit flags passive voice as exceeding the target.
3. **Given** a voice profile with no `measurements` section, **When** content is generated, **Then** the self-audit runs normally using only the higher-order signal checks (no measurement validation).

---

### User Story 5 - Old-Format Voice Profiles Are Auto-Detected (Priority: P3)

A user has an existing voice profile in the old format (lacking the new parameters). When any skill loads this profile, it detects the old format and offers to migrate it by adding default values for the new parameters while leaving the measurements section empty.

**Why this priority**: Migration support ensures existing users aren't broken by the schema change, but it's not needed for new functionality to work.

**Independent Test**: Can be tested by loading a voice profile from the current format and verifying the migration prompt appears and produces a valid updated profile.

**Acceptance Scenarios**:

1. **Given** a voice profile without a `confidence` field, **When** the content-generator loads it, **Then** the skill detects the old format and offers to add default values for missing parameters.
2. **Given** a user accepts the migration, **When** the profile is updated, **Then** all new parameters are present with sensible defaults and no `measurements` section is added.
3. **Given** a user declines the migration, **When** the profile is used as-is, **Then** the skill falls back to default values for missing parameters without error.

---

### User Story 6 - Voice Architect Creates Profiles with New Schema (Priority: P3)

A user creates a new voice profile through the voice-architect's interactive questionnaire. The questionnaire includes questions for all new parameters, producing a complete profile in the updated schema.

**Why this priority**: The architect is the UI for profile creation. It must support the new schema, but users can also edit YAML directly.

**Independent Test**: Can be tested by running the voice-architect create workflow and verifying the resulting YAML includes all new parameter sections.

**Acceptance Scenarios**:

1. **Given** a user runs the voice-architect to create a new profile, **When** the questionnaire completes, **Then** the output YAML contains `confidence`, `paragraph_patterns`, `sentence_starters`, `emotional_range`, `self_correction`, `directness`, and `specificity` fields.
2. **Given** a user creates a profile, **When** the profile is saved, **Then** no `measurements` section is included (measurements are extractor-only).

---

### Edge Cases

- What happens when a voice profile has `confidence: 0.9` (assertive) but `directness: hedged`? The skills should treat these as independent dimensions: the writer is confident in their claims but softens delivery.
- What happens when measurements targets conflict with human-readable params (e.g., `confidence: 0.9` but `measurements.hedge_density_per_1000: 15`)? The human-readable params guide generation; measurements are for post-generation validation. The self-audit should report the discrepancy but not override the generation intent.
- What happens when the voice-extractor corpus is too small (< 500 words) for reliable measurements? The extractor should still populate measurements but add a `sample_confidence: low` marker to the measurements section (named `sample_confidence` to distinguish from the voice parameter `confidence`), and the self-audit should treat low-confidence measurements as advisory rather than strict targets.
- What happens when a voice profile has only the `measurements` section (from extraction) but no human-readable knobs? The skills should derive reasonable human-readable behavior from the measurements (e.g., high `hedge_density_per_1000` implies low `confidence`) but warn that explicit parameters produce better results.

## Clarifications

### Session 2026-06-13

- Q: What deviation from measurement targets triggers a self-audit flag vs. informational note? → A: Deviations > 25% from the numeric target are flagged as actionable findings. Deviations between 10-25% are reported as informational notes. Deviations < 10% are not reported.
- Q: Where does the `confidence` field live in the YAML schema hierarchy? → A: Under the `characteristics` group, alongside `formality` and `personality`, as a float 0.0-1.0.
- Q: How does the self-audit handle low-confidence measurements (from small corpora)? → A: Low-confidence measurements use a relaxed threshold (deviations > 50% flagged instead of 25%). The self-audit prefixes findings with "advisory" to indicate reduced reliability.

## Error Handling

- **Invalid parameter values** (e.g., `confidence: 2.0`, `directness: "aggressive"`): Skills MUST validate parameter values at load time, report the invalid field and value, and fall back to the default for that field. Processing continues with the valid fields.
- **Corrupted or unreadable files in extractor corpus**: The voice-extractor MUST skip unreadable files, log a warning identifying each skipped file, and continue processing the remaining files. If all files are unreadable, it MUST report an error and produce no output.
- **Measurement computation edge cases** (division by zero, NaN): When a corpus is too small or uniform to compute a specific metric (e.g., zero sentences for stdev), the extractor MUST omit that field from the measurements section rather than writing NaN or infinity.
- **Non-interactive contexts**: When FR-014 migration is triggered in a non-interactive context (piped input, CI), the skill MUST silently apply defaults without prompting and log an informational message noting the auto-migration.

## Requirements

### Functional Requirements

- **FR-001**: Voice profile schema MUST support a `confidence` field (float 0.0-1.0) controlling the hedged-to-assertive spectrum
- **FR-002**: Voice profile schema MUST support a `paragraph_patterns` group with `avg_length` (short/medium/long), `opening_style` (direct/contextual/anecdotal/varied), and `transition_style` (explicit/organic/minimal)
- **FR-003**: Voice profile schema MUST support a `sentence_starters` field (pronoun-heavy/varied/formal-lead) in the `sentence_patterns` group
- **FR-004**: Voice profile schema MUST support `emotional_range` (flat/moderate/dynamic), `self_correction` (boolean), and `directness` (hedged/balanced/blunt) in the `personality_traits` group
- **FR-005**: Voice profile schema MUST support a `specificity` field (abstract/balanced/concrete) in the `elaboration` group
- **FR-006**: Voice profile schema MUST support an optional `measurements` section containing numeric fields with defined units: `sentence_length_mean` (words), `sentence_length_stdev` (words), `paragraph_length_mean` (sentences), `passive_voice_pct` (percentage 0-100), `hedge_density_per_1000` (occurrences per 1000 words), `connector_variety` (unique connectors / total connectors, 0.0-1.0, where connectors are transition words and phrases like "however", "therefore", "in addition"), `concrete_abstract_ratio` (concrete nouns and specifics / abstract nouns and generalizations, 0.0+), `punctuation_entropy` (Shannon entropy over the distribution of punctuation marks used: periods, commas, semicolons, colons, dashes, exclamation marks, question marks), `one_sentence_paragraph_rate` (percentage 0-100), `contraction_rate_per_1000` (contractions per 1000 words)
- **FR-007**: The `measurements` section MUST only be populated by the voice-extractor, never by manual profile creation workflows
- **FR-008**: All 8 built-in voice templates MUST be updated with appropriate values for all new parameters
- **FR-009**: The content-generator MUST consume all new human-readable parameters during content generation
- **FR-010**: The humanizer MUST respect all new human-readable parameters during text rewriting
- **FR-011**: The self-audit subagent MUST receive the `measurements` section (when present) and validate the draft against numeric targets, reporting specific deviations
- **FR-012**: The voice-extractor MUST compute and populate all measurement fields from writing samples
- **FR-013**: The voice-architect MUST include new parameters in its create and edit workflows
- **FR-014**: Skills loading voice profiles MUST detect old-format profiles (missing new parameters) and offer migration with the following defaults: `confidence: 0.5`, `directness: balanced`, `emotional_range: moderate`, `self_correction: false`, `specificity: balanced`, `paragraph_patterns.avg_length: medium`, `paragraph_patterns.opening_style: varied`, `paragraph_patterns.transition_style: organic`, `sentence_starters: varied`. No `measurements` section is added during migration
- **FR-015**: The pre-validator MUST check voice consistency against the expanded parameter set including new parameters

### Key Entities

- **Voice Profile**: YAML configuration file defining a writing personality. Extended with new parameter groups (`paragraph_patterns`, expanded `personality_traits`, expanded `elaboration`) and an optional `measurements` section.
- **Measurements**: Numeric subsection of a voice profile containing statistical targets derived from corpus analysis. Read-only from the user's perspective; populated exclusively by the voice-extractor.
- **Voice Template**: Built-in profile shipped with the plugin (8 total: technical, conversational, analytical, narrative, pov, reasoning, tutorial, reference). Each must be updated with new parameter values.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Generated content with `confidence: 0.9` contains fewer than 1 hedging qualifier ("perhaps", "might", "somewhat", "arguably") per 500 words
- **SC-002**: Generated content with `confidence: 0.2` contains at least 3 hedging qualifiers per 500 words
- **SC-003**: The self-audit subagent reports concrete numeric deviations (e.g., "stdev is X, target is Y") when measurements are present, rather than vague assessments
- **SC-004**: Voice profiles extracted from a 3000+ word corpus produce measurements that are within 15% of independently computed reference values (using standard NLP tokenization) for sentence length stats and within 25% for density metrics
- **SC-005**: Old-format voice profiles load without errors and produce a migration prompt within 1 interaction
- **SC-006**: All 8 built-in templates pass validation against the updated schema with no missing required fields

## Assumptions

- The voice-extractor already supports corpus analysis with confidence scoring; the measurements section extends its output rather than replacing it
- The self-audit subagent (added in the prior feature) already runs in a fresh subagent context; measurement validation is added to its prompt, not a separate step
- Inline voice matching (from brainstorm #02) does not interact with the measurements section; inline samples are too short for reliable measurement extraction
- The `measurements` field list (10 fields) is a curated starting set; additional fields can be added in future iterations without schema changes
- Backward compatibility with old profiles is handled at load time by offering migration, not by maintaining dual schema support
