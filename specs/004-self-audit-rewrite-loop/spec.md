# Feature Specification: Self-Audit Rewrite Loop

**Feature Branch**: `004-self-audit-rewrite-loop`  
**Created**: 2026-06-12  
**Status**: Draft  
**Input**: User description: "Self-audit rewrite loop: add adversarial self-audit step to humanizer and content-generator skills to catch higher-order AI tells that individual pattern checks miss"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Humanizer Catches Subtle AI Tells on Second Pass (Priority: P1)

A user submits AI-generated text to the humanizer for rewriting. The humanizer applies all pattern rules in its first rewrite pass, producing a draft that is technically clean (no individual pattern violations). The humanizer then performs a self-audit, asking "What makes this still obviously AI-generated?" and identifies higher-order tells like overly tidy rhythm, evenly paced paragraphs, or slogan-like closings. The humanizer performs a final rewrite addressing those findings and delivers the improved text along with the self-audit bullets.

**Why this priority**: The humanizer is the primary tool for fixing existing AI-generated text. Adding the self-audit step here delivers the most immediate, visible improvement in output quality. This is the core value proposition of the feature.

**Independent Test**: Can be tested by running the humanizer on any AI-generated text and verifying that (a) the final output addresses issues beyond individual pattern violations, and (b) the self-audit findings are included in the output.

**Acceptance Scenarios**:

1. **Given** AI-generated text with no individual pattern violations but obviously AI-like rhythm and structure, **When** the user runs the humanizer, **Then** the self-audit identifies at least one higher-order tell and the final rewrite addresses it.
2. **Given** text that the humanizer rewrites, **When** the rewrite is complete, **Then** the output includes the final rewrite, self-audit findings as brief bullets, and a change summary. The intermediate draft is not shown.
3. **Given** text containing em-dashes or en-dashes, **When** the final rewrite step runs, **Then** the output contains no em-dashes or en-dashes (verified alongside self-audit fixes).

---

### User Story 2 - Content-Generator Self-Audits After Generation (Priority: P2)

A user asks the content-generator to create new content (e.g., a blog post section, an email). The content-generator produces text following all style and voice rules, runs its existing rule-based self-validation, and then performs an additional self-audit asking "What makes this obviously AI-generated?" Any findings are addressed before delivering the final text.

**Why this priority**: The content-generator already has a self-validate step checking rules and stoplist compliance. The self-audit adds a complementary adversarial check that catches what rules miss. This is high value but secondary to the humanizer because the content-generator already has some self-checking.

**Independent Test**: Can be tested by generating content and verifying that the delivered text has been checked against both rule-based validation and the adversarial self-audit question. The output should show no obvious AI tells in rhythm, structure, or tone.

**Acceptance Scenarios**:

1. **Given** a content generation request with a voice profile, **When** the content-generator produces text, **Then** the self-audit step runs after the rule-based self-validate and before delivery.
2. **Given** content that passes all rule-based checks but has AI-like cadence, **When** the self-audit runs, **Then** it identifies the cadence issue and the final output addresses it.
3. **Given** a content generation request, **When** the content-generator delivers text, **Then** the existing rule-based self-validate (stoplist, style compliance) still runs; the self-audit does not replace it.

---

### User Story 3 - Self-Audit Respects Human Signals and False Positives (Priority: P3)

A user submits text that contains deliberate stylistic choices (e.g., intentional repetition for emphasis, a rhetorical list structure). The self-audit step recognizes these as human signals or false positives and does not flag them as AI tells. The self-audit is aware of the false-positive guidance established in brainstorm #03.

**Why this priority**: Without false-positive awareness, the self-audit could undo intentional human choices. This is important for trust and correctness but depends on the core self-audit mechanism working first.

**Independent Test**: Can be tested by running the humanizer or content-generator on text with known deliberate stylistic choices and verifying the self-audit does not flag or alter those sections.

**Acceptance Scenarios**:

1. **Given** text with intentional rhetorical repetition, **When** the self-audit runs, **Then** it does not flag the repetition as an AI tell.
2. **Given** text where the user has explicitly marked passages to preserve, **When** the self-audit runs, **Then** it respects those preservation markers.

---

### Edge Cases

- What happens when the self-audit finds no remaining AI tells? The process completes normally, reporting "no additional AI tells found" in the self-audit findings. The final rewrite step is skipped since there is nothing to address.
- What happens when the self-audit identifies issues that conflict with the voice profile? The voice profile takes precedence. The self-audit MUST NOT flag voice-consistent traits as AI tells.
- What happens when the self-audit introduces new pattern violations in the final rewrite? The final rewrite MUST comply with all humanizer pattern rules. If the rewrite addressing self-audit findings introduces a new violation, that violation MUST be caught and corrected (the pattern rules remain authoritative, per FR-010).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The humanizer MUST perform a self-audit step after its initial pattern-based rewrite, asking "What makes this still obviously AI-generated?" and listing remaining tells as brief bullets.
- **FR-002**: The humanizer MUST perform a final rewrite that addresses the findings from the self-audit step.
- **FR-003**: The humanizer MUST present only the final rewrite to the user (not the intermediate draft), along with the self-audit findings and a change summary.
- **FR-004**: The content-generator MUST perform a self-audit step after its existing rule-based self-validate, asking "What makes this obviously AI-generated?" and addressing any findings before delivery.
- **FR-005**: The content-generator MUST retain its existing rule-based self-validate step; the self-audit is an additional step, not a replacement.
- **FR-006**: The self-audit question MUST focus on higher-order signals (rhythm, cadence, structure, tone, specificity, emotional range) rather than individual pattern-rule compliance.
- **FR-007**: The self-audit MUST respect false-positive guidance and human signal preservation, not flagging deliberate stylistic choices as AI tells.
- **FR-008**: The final rewrite (humanizer) MUST verify that no em-dashes or en-dashes are present in the output.
- **FR-009**: When the self-audit finds no remaining AI tells, the system MUST skip the final rewrite step and report that no additional tells were found.
- **FR-010**: The humanizer MUST re-validate the final rewrite against all pattern rules before presenting it to the user. If the final rewrite introduces new pattern violations, those violations MUST be corrected.
- **FR-011**: The content-generator MUST include self-audit findings in its output when findings exist, so the user can see what the self-audit caught. When no findings exist, the output indicates that no additional AI tells were found.

### Key Entities

- **Self-Audit Finding**: A brief bullet describing a higher-order AI tell identified during the self-audit step. Contains the tell description and the area of text affected.
- **Draft Rewrite**: Internal working state produced by the humanizer's pattern-based rewrite. Not shown to the user. Serves as input to the self-audit step.
- **Final Rewrite**: The output produced after addressing self-audit findings. This is what the user sees.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Text processed through the humanizer with the self-audit step is rated as "less obviously AI-generated" compared to single-pass output, when evaluated by a human reader or by the pre-validator's scoring.
- **SC-002**: The self-audit step identifies at least one higher-order tell in 70% or more of texts that pass all individual pattern checks, demonstrating that it catches what patterns miss.
- **SC-003**: Content produced by the content-generator with the self-audit step shows no regression in rule-based compliance (stoplist violations, style rule violations remain at zero).
- **SC-004**: The self-audit step does not flag deliberate human stylistic choices as AI tells in 95% or more of cases where such choices are present.

## Assumptions

- The self-audit step adds acceptable processing time for typical use cases. Texts of typical length (200-2000 words) are the primary target; very short texts (under 100 words) may not benefit significantly from the self-audit.
- Self-audit findings are shown to the user by default (not hidden). This builds trust by showing what the second pass caught.
- The pre-validator does not need changes. It already performs multi-phase validation and reporting; the self-audit is a rewriting concern, not a validation concern.
- The false-positive guidance from feature #002 is available and integrated before or alongside this feature.
- The adversarial self-audit question is genuinely different from pattern-rule checking. It asks "would a reader say this is obviously AI?" rather than "does this violate rule X?"
