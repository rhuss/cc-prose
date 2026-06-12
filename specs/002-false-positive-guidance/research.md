# Research: False-Positive Guidance and Human Signal Preservation

**Date**: 2026-06-12

## Research Questions

### 1. What is the canonical false-positive list from upstream?

**Decision**: Use the 12-item list from the upstream humanizer v2.8.0 "DETECTION GUIDANCE" section.

**Rationale**: The upstream list is based on Wikipedia's "Signs of AI writing" guide and represents community consensus. Using the same list across all three skills (humanizer, pre-validator, content-generator) ensures consistency.

**Alternatives considered**:
- Custom-curated list: Rejected because diverging from upstream creates maintenance burden during future syncs.
- Superset of upstream + custom items: Rejected because additional items would need independent validation and could introduce inconsistencies.

### 2. How should cluster detection interact with the existing severity system?

**Decision**: Cluster detection acts as a modifier on the existing severity tiers. Isolated tells get downgraded to LOW. Clustered tells (3+ different types in one paragraph) get restored to their original default severity.

**Rationale**: This is the simplest rule that satisfies both goals (reduce false positives on isolated tells, catch actual AI content via clusters). No new severity tiers or point values are needed.

**Alternatives considered**:
- Add a new "CLUSTER" severity tier above HIGH: Rejected because it adds complexity to the scoring algorithm without clear benefit. Restoring to default severity is sufficient.
- Use a sliding scale based on cluster size (3 tells = MEDIUM, 5 tells = HIGH): Rejected because it overcomplicates the logic. The binary isolated/clustered distinction is clearer and easier to implement in a SKILL.md instruction.

### 3. How should human signals affect scoring?

**Decision**: Human signals are reported in the output but do not modify the numeric score. They are informational, providing context for the reader to interpret the score.

**Rationale**: Adding positive score adjustments would make the scoring algorithm harder to understand and predict. A score of 75 should mean the same thing regardless of whether human signals are present. The value of human signal detection is in the report, not the number.

**Alternatives considered**:
- Subtract points for human signals (positive adjustment): Rejected because it makes the score less predictable and could mask real issues.
- Use human signals to offset isolated tell penalties: Rejected for the same reason; it creates complex interactions between scoring mechanisms.

### 4. What is the correct category count after the upstream sync?

**Decision**: 33 categories. Verified by examining the synced humanizer SKILL.md.

**Rationale**: The upstream v2.8.0 sync expanded from 24 to 33 categories. Both the pre-validator and content-generator reference "24 categories" and need updating.

**Alternatives considered**: None. This is a factual correction.

### 5. How does isolation scope differ between pre-validator and content-generator?

**Decision**: Pre-validator uses paragraph-level scope (tells must co-occur in the same paragraph for cluster detection). Content-generator uses whole-output scope (a tell is isolated only if no other tells exist anywhere in the generated output).

**Rationale**: The pre-validator analyzes existing documents that may be many paragraphs long; paragraph-level scope prevents distant, unrelated tells from triggering cluster detection. The content-generator produces one coherent piece at a time and validates it holistically; whole-output scope matches its existing validation approach.

**Alternatives considered**:
- Same scope for both (paragraph-level): Rejected because the content-generator's existing self-validation does not operate paragraph-by-paragraph.
- Same scope for both (whole-output): Rejected because the pre-validator needs finer granularity to avoid false cluster detection across unrelated sections of a long document.
