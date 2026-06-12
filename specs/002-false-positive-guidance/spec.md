# Feature Specification: False-Positive Guidance and Human Signal Preservation

**Feature Branch**: `002-false-positive-guidance`
**Created**: 2026-06-12
**Status**: Draft
**Input**: Brainstorm document `brainstorm/03-false-positive-guidance.md`

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pre-validator stops over-penalizing isolated tells (Priority: P1)

A writer runs the pre-validator on a polished article that contains a single em dash and formal vocabulary. Today, the pre-validator flags the em dash as HIGH severity and the formal words as AI vocabulary, inflating the score toward FAIL. After this change, isolated tells are scored as LOW severity, and the article receives a fair score reflecting its actual quality.

**Why this priority**: The pre-validator produces the numeric pass/fail verdict. False positives here directly cause incorrect FAIL recommendations on genuinely human-written content, which is the most visible and damaging problem.

**Independent Test**: Run the pre-validator on content with a single isolated AI tell (one em dash, one formal word). Verify the severity is LOW and the overall score does not drop below PASS threshold from that single tell alone.

**Acceptance Scenarios**:

1. **Given** content with exactly one em dash and no other AI tells, **When** the pre-validator runs, **Then** the em dash is scored as LOW severity (not HIGH) and the overall recommendation is PASS (assuming no other issues).
2. **Given** content with formal academic vocabulary ("nevertheless", "furthermore") but no AI-specific vocabulary ("delve", "tapestry"), **When** the pre-validator runs, **Then** the formal vocabulary is not flagged as an AI pattern.
3. **Given** content with one instance of "however" as a transition word, **When** the pre-validator runs, **Then** it is not flagged (common transition words in isolation are not tells).

---

### User Story 2 - Pre-validator escalates clustered tells (Priority: P1)

A writer runs the pre-validator on content where a single paragraph contains an em dash, a rule-of-three list, and the word "tapestry." Today, each is scored independently. After this change, the pre-validator detects the cluster and escalates the severity because three co-occurring tells in one paragraph are a strong AI signal.

**Why this priority**: Cluster detection is the complement of false-positive reduction. Without it, reducing isolated tell severity would let actual AI-generated content pass too easily.

**Independent Test**: Run the pre-validator on a paragraph containing 3+ different AI tells. Verify the severity is escalated beyond what each individual tell would produce.

**Acceptance Scenarios**:

1. **Given** a paragraph containing an em dash, a rule-of-three pattern, and the word "vibrant", **When** the pre-validator runs, **Then** the cluster is flagged with escalated severity (higher than each individual tell).
2. **Given** three different AI tells spread across three separate paragraphs (one tell per paragraph), **When** the pre-validator runs, **Then** no cluster escalation occurs (tells must co-occur within the same paragraph).
3. **Given** two AI tells in the same paragraph, **When** the pre-validator runs, **Then** no cluster escalation occurs (threshold is 3+ different tells).

---

### User Story 3 - Pre-validator recognizes human writing signals (Priority: P2)

A writer runs the pre-validator on content that includes specific hard-to-fabricate details, mixed feelings, and self-corrections. Today, these are ignored. After this change, the pre-validator recognizes these as positive indicators of human writing and does not penalize surrounding content as harshly.

**Why this priority**: Human signal awareness completes the false-positive picture. Recognizing positive human markers prevents the pre-validator from penalizing authentic writing that happens to also contain a couple of AI-pattern matches.

**Independent Test**: Run the pre-validator on content rich in human signals (specific details, self-corrections, mixed feelings). Verify the overall score is not dragged down by minor AI-pattern coincidences.

**Acceptance Scenarios**:

1. **Given** content containing specific real-world details (actual place names, unusual quotes, precise dates) alongside one isolated AI tell, **When** the pre-validator runs, **Then** the human signals are noted positively in the report and the overall score reflects the human quality.
2. **Given** content with self-corrections ("I keep wanting to say 'almost' here") and mixed feelings ("I think this is mostly good, but it bothers me"), **When** the pre-validator runs, **Then** these are identified as human writing markers in the report output.

---

### User Story 4 - Content-generator preserves human signals during self-validation (Priority: P2)

A user generates content using the content-generator. The generated output includes a self-correction aside and some sentence-length variety. Today, the self-validation step might reject these as pattern violations. After this change, the content-generator recognizes human-like personality markers and preserves them.

**Why this priority**: The content-generator's self-validation loop can strip out the personality it just created. Fixing this prevents the generator from fighting itself.

**Independent Test**: Generate content with voice personality enabled. Verify that self-validation does not strip genuine asides, self-corrections, or varied sentence rhythms that the generator deliberately added.

**Acceptance Scenarios**:

1. **Given** the content-generator produces text with a genuine aside (parenthetical self-correction), **When** self-validation runs, **Then** the aside is preserved in the final output.
2. **Given** the content-generator produces text with one isolated formal word that matches the voice profile's formality setting, **When** self-validation runs, **Then** the word is not rejected as an AI vocabulary violation.
3. **Given** the content-generator produces text containing mixed sentence lengths including one short emphatic sentence, **When** self-validation runs, **Then** the short sentence is preserved (not flagged as a style violation).

---

### User Story 5 - Updated category count references (Priority: P3)

Both skills currently reference "24 humanizer categories" in their documentation and internal logic. The upstream sync brought the category count to 33. After this change, both skills reference the correct count of 33 categories.

**Why this priority**: This is a simple consistency fix. The wrong number does not affect behavior but creates confusion and suggests the skills are out of date.

**Independent Test**: Search both skill files for the number "24" in the context of humanizer categories. Verify all instances are updated to 33.

**Acceptance Scenarios**:

1. **Given** the pre-validator skill file, **When** searching for references to humanizer category counts, **Then** all references say 33 (not 24).
2. **Given** the content-generator skill file, **When** searching for references to humanizer category counts, **Then** all references say 33 (not 24).

---

### Edge Cases

- What happens when content has exactly 3 tells but they are all the same type (e.g., three em dashes)? Cluster detection requires 3+ *different* tell types, so this should not trigger escalation.
- What happens when a project-level style rule (like CLAUDE.md's "no em dashes") conflicts with false-positive guidance? The style rule is a style preference enforced separately; the false-positive guidance only affects AI *detection* scoring. Both coexist: the em dash is still a style violation but not an AI detection signal when isolated.
- What happens when content has zero AI tells but also zero human signals? The score should be based on the absence of tells alone. Human signals are a positive indicator, not a requirement.
- What happens when the pre-validator encounters a false-positive item from the list (e.g., curly quotes) that is also on the project stoplist? The stoplist is a CRITICAL rule that overrides false-positive guidance. Stoplist words are always flagged regardless of isolation.

## Clarifications

### Session 2026-06-12

- Q: What severity level do clustered tells escalate to? → A: Restore each tell to its original default severity (the level defined in the humanizer categories, before isolation downgrade). Isolation downgrades to LOW; clustering removes the downgrade.
- Q: How are human writing signals reported in the pre-validator output? → A: Add a "Human Writing Signals" subsection in the report, between the severity issue lists and the readability metrics section, listing each detected signal type with examples found.
- Q: What scope defines "isolation" for the content-generator's self-validation? → A: The entire generated output. Since the content-generator validates one complete piece holistically, "isolation" means no other tells anywhere in the output (not paragraph-level like the pre-validator).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The pre-validator MUST classify isolated AI tells (a single tell with no other tells in the same paragraph) as LOW severity instead of their default severity level.
- **FR-002**: The pre-validator MUST detect clusters of 3 or more different AI tell types within the same paragraph and restore each tell to its original default severity (removing the isolation downgrade).
- **FR-003**: The pre-validator MUST recognize a defined list of false-positive patterns (items that are not reliable AI indicators on their own) and not flag them when they appear in isolation.
- **FR-004**: The pre-validator MUST recognize human writing signals (specific details, mixed feelings, self-corrections, era-bound references, varied sentence length) and report them in a dedicated "Human Writing Signals" subsection in the report, positioned between severity issue lists and readability metrics.
- **FR-005**: The pre-validator MUST maintain stoplist supremacy: stoplist words are always CRITICAL regardless of isolation or false-positive guidance.
- **FR-006**: The pre-validator MUST update all references from 24 humanizer categories to 33.
- **FR-007**: The content-generator MUST not reject its own output during self-validation for patterns that appear in isolation (single tells with no other tells anywhere in the generated output).
- **FR-008**: The content-generator MUST preserve human writing signals (asides, self-corrections, mixed feelings, sentence variety) that it deliberately added during generation.
- **FR-009**: The content-generator MUST update all references from 24 humanizer categories to 33.
- **FR-010**: Both skills MUST treat project-level style rules (from CLAUDE.md or style configuration) as separate from AI detection scoring. A style violation is not an AI detection signal.

### False-Positive List (items NOT reliable AI indicators on their own)

- Perfect grammar and consistent style
- Mixed casual and formal registers
- Generic dry prose without specific AI tells
- Formal or academic vocabulary (unless it is a specific AI vocabulary word)
- Letter-style opening/closing on a comment
- Common transition words in isolation (one "however" is not a tell)
- Curly quotes alone (auto-curled by editors)
- Em dashes alone (used frequently by journalists and editors)
- One short emphatic sentence
- "Honestly" or "look" mid-sentence
- Unsourced claims
- Correct, complex formatting

### Human Writing Signals (preserve these)

- Specific, unusual, hard-to-fabricate detail (real addresses, unusual quotes)
- Mixed feelings and unresolved tension
- Dated, era-bound references
- First-person editorial choices the writer can defend
- Variety in sentence length (short and long alternating)
- Genuine asides, parentheticals, self-corrections

### Key Entities

- **AI Tell**: A specific textual pattern that may indicate AI-generated content. Each tell belongs to a category (e.g., "AI vocabulary", "rule of three") and has a default severity.
- **Cluster**: Three or more different AI tell types co-occurring within the same paragraph. Clusters indicate stronger AI signal than any individual tell.
- **False Positive**: A textual pattern that resembles an AI tell but is common in human writing and should not be treated as a reliable AI indicator when it appears alone.
- **Human Writing Signal**: A textual pattern that positively indicates human authorship, such as specific details, mixed feelings, or self-corrections.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Content with a single isolated AI tell (and no other tells) receives a pre-validator score of 85 or above (PASS threshold), assuming no other quality issues.
- **SC-002**: Content with 3+ different AI tells clustered in one paragraph receives escalated severity scoring, resulting in a lower score than the same tells spread across separate paragraphs.
- **SC-003**: The content-generator produces output with personality markers (asides, varied sentence length, self-corrections) that survive self-validation at least 90% of the time.
- **SC-004**: All references to "24 categories" in both skill files are updated to "33 categories" with zero remaining instances of the old count.

## Assumptions

- The upstream humanizer skill (v2.8.0) is already synced and contains the full "DETECTION GUIDANCE" section. No changes to the humanizer skill are needed.
- The false-positive list and human writing signals list match the upstream humanizer's guidance. If the upstream list changes in a future sync, the pre-validator and content-generator lists should be updated to match.
- The pre-validator's scoring algorithm (100-point scale, category weights) remains structurally the same. Changes are to severity classification and scoring adjustments, not to the overall scoring framework.
- The content-generator's self-validation step structure remains the same. Changes add awareness of false positives and human signals, not a new validation phase.
- Stoplist rules always take precedence over false-positive guidance. If a word is on the stoplist, it is CRITICAL regardless of context.
