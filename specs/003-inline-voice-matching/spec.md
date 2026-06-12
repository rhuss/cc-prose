# Feature Specification: Inline Voice-Matching

**Feature Branch**: `003-inline-voice-matching`
**Created**: 2026-06-12
**Status**: Draft
**Input**: Brainstorm 02 - Inline voice-matching in the humanizer

## User Scenarios & Testing

### User Story 1 - Ad-hoc voice matching with inline sample (Priority: P1)

A user has text they want humanized to match their own writing style. They paste a sample of their writing alongside the rewrite request. The humanizer reads the sample, notes the voice characteristics, and rewrites the text to match that voice in a single pass, without requiring the user to create a persistent voice profile first.

**Why this priority**: This is the core gap identified in the brainstorm. Users currently need three steps (extract, save profile, rewrite) for something that should be one step. This is the most common ad-hoc scenario.

**Independent Test**: Can be fully tested by providing a writing sample alongside text to humanize and verifying the output matches the sample's voice characteristics.

**Acceptance Scenarios**:

1. **Given** a user provides text to humanize along with an inline writing sample, **When** the humanizer processes the request, **Then** the output matches the voice characteristics (sentence length, word choice level, punctuation habits) of the provided sample.
2. **Given** a user provides text to humanize along with an inline writing sample that uses short, punchy sentences, **When** the humanizer rewrites the text, **Then** the output uses similarly short sentences rather than long compound ones.
3. **Given** a user provides only text to humanize with no sample and no voice profile configured, **When** the humanizer processes the request, **Then** the humanizer falls back to its default behavior (natural, varied voice from the PERSONALITY AND SOUL section).

---

### User Story 2 - Voice matching from a file reference (Priority: P1)

A user wants text humanized to match the voice of an existing document on disk. They reference a file path instead of pasting inline content. The humanizer reads the referenced file, analyzes its voice characteristics, and matches them in the rewrite.

**Why this priority**: Equally important as inline samples because users often have existing writing they want to match but don't want to copy-paste large documents into the prompt.

**Independent Test**: Can be tested by providing a file path to existing writing alongside text to humanize and verifying the output matches the file's voice.

**Acceptance Scenarios**:

1. **Given** a user provides text to humanize and references a file path for voice matching, **When** the humanizer processes the request, **Then** the humanizer reads the referenced file and matches its voice characteristics in the output.
2. **Given** a user references a file path that does not exist, **When** the humanizer attempts to read the file, **Then** the humanizer warns about the missing file and falls back to default behavior.

---

### User Story 3 - Inline voice matching in content-generator (Priority: P2)

A user wants new content generated matching the voice of an existing writing sample. They provide a sample (inline or file reference) alongside their content generation request. The content-generator analyzes the sample and generates new content matching that voice, without requiring a persistent voice profile.

**Why this priority**: Extends the same convenience to content generation. Less critical than humanizer because the content-generator already has a voice profile workflow, but the ad-hoc path fills the same friction gap.

**Independent Test**: Can be tested by providing a writing sample alongside a content generation request and verifying the generated content matches the sample's voice.

**Acceptance Scenarios**:

1. **Given** a user requests new content and provides an inline writing sample, **When** the content-generator processes the request, **Then** the generated content matches the voice characteristics of the sample.
2. **Given** a user requests new content with both a voice profile configured and an inline sample provided, **When** the content-generator processes the request, **Then** the inline sample takes priority over the configured voice profile.

---

### User Story 4 - Voice source priority resolution (Priority: P2)

When multiple voice sources are available (configured profile, inline sample, default behavior), the system resolves them in a defined priority order so the user always gets predictable results.

**Why this priority**: Without clear priority rules, conflicting voice sources could produce unpredictable output. The priority order (inline sample > voice profile > default) matches user expectations because an inline sample is the most explicit signal.

**Independent Test**: Can be tested by configuring a voice profile and also providing an inline sample, then verifying the inline sample wins.

**Acceptance Scenarios**:

1. **Given** a voice profile is configured AND an inline writing sample is provided, **When** either skill processes the request, **Then** the inline sample takes priority and the voice profile is ignored for this request.
2. **Given** a voice profile is configured and no inline sample is provided, **When** either skill processes the request, **Then** the voice profile is used as before (no behavior change).
3. **Given** no voice profile and no inline sample are provided, **When** either skill processes the request, **Then** the skill falls back to its default voice behavior.

---

### User Story 5 - Cross-reference to persistent profiles (Priority: P3)

After an inline voice match, the skill mentions that persistent voice profiles are available for repeated use, guiding users toward the full pipeline when appropriate.

**Why this priority**: A discovery mechanism, not core functionality. Helps users find the more powerful workflow when they need it.

**Independent Test**: Can be tested by running an inline voice match and verifying the output includes a mention of the voice-extractor for persistent profiles.

**Acceptance Scenarios**:

1. **Given** a user provides an inline writing sample for voice matching, **When** the skill completes the rewrite or generation, **Then** the output includes a brief note that persistent voice profiles are available via `/prose:voice extract`.

---

### Edge Cases

- What happens when the inline writing sample is very short (under 50 words)? The skill should still attempt to match what it can, since there is no minimum word count for inline matching.
- What happens when the writing sample contains AI-generated text? The skill should match the sample's voice regardless, since the user explicitly asked for it.
- What happens when the inline sample conflicts with explicit style rules (e.g., the sample uses em dashes but project rules forbid them)? Project-level style rules (from CLAUDE.md or copyedit config) take precedence over sample voice matching for specific prohibited patterns.

## Requirements

### Functional Requirements

- **FR-001**: The content-generator skill MUST support inline voice-matching, analyzing a user-provided writing sample and matching its voice characteristics during content generation.
- **FR-002**: The content-generator MUST accept writing samples provided inline (pasted in the request) or by file reference (a path to an existing document).
- **FR-003**: Both skills (humanizer and content-generator) MUST resolve voice sources in this priority order: inline sample > configured voice profile > default behavior.
- **FR-004**: Inline voice matching MUST have no minimum word count requirement for the writing sample.
- **FR-005**: Inline voice matching MUST be ephemeral: no YAML output, no persistence, no side effects on existing voice profiles.
- **FR-006**: The inline voice analysis MUST note: sentence length patterns, word choice level, paragraph opening patterns, punctuation habits, recurring phrases or verbal tics, and transition handling.
- **FR-007**: Both skills MUST include a brief cross-reference to the voice-extractor for users who want persistent profiles, mentioning `/prose:voice extract`.
- **FR-008**: When a referenced file for voice matching does not exist, the skill MUST warn the user and fall back to the next available voice source.
- **FR-009**: Project-level style rules MUST take precedence over inline voice matching for specific prohibited patterns (e.g., em dash rules from CLAUDE.md).

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can match a writing sample's voice in a single request, reducing the current 3-step workflow to 1 step.
- **SC-002**: Content-generator achieves voice matching parity with the humanizer's existing inline calibration capability.
- **SC-003**: Voice priority resolution produces consistent, predictable results across both skills when multiple voice sources are present.
- **SC-004**: Writing samples under 100 words are accepted and produce recognizable voice matching for the characteristics that are detectable.

## Assumptions

- The humanizer's "Voice Calibration (Optional)" section already exists from the upstream v2.8.0 sync and does not need to be added. The work for the humanizer is limited to adding the cross-reference to voice-extractor and documenting the priority order.
- The content-generator's existing voice profile loading (Phase 2 in its SKILL.md) remains unchanged. Inline voice matching is an additional capability that layers on top of the existing workflow.
- The voice-extractor and voice-architect skills are not modified by this feature. They remain the path for persistent, high-fidelity voice profiles.
- The pre-validator skill is not affected by this feature since it does not perform rewriting or content generation.
