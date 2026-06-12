# Research: Inline Voice-Matching

## R1: Upstream humanizer voice calibration structure

**Decision**: Preserve the upstream Voice Calibration section exactly as-is and append new subsections.

**Rationale**: The upstream humanizer (v2.8.0) defines the Voice Calibration section with a specific structure (analysis dimensions, matching instructions, sample input methods). Modifying this structure would create merge conflicts on future upstream syncs. Appending priority order and cross-reference as new subsections avoids this.

**Alternatives considered**:
- Restructuring the entire section to add priority logic inline: rejected because it would diverge from upstream and complicate future syncs.
- Adding priority order as a comment: rejected because comments are not reliably preserved by LLMs processing the skill.

## R2: Content-generator voice section placement

**Decision**: Place the new "Voice Calibration (Optional)" section between "Your Mission" and "Configuration Loading" (after line ~72, before line ~74).

**Rationale**: Voice calibration is a pre-generation concern, similar to configuration loading. Placing it before Configuration Loading means the LLM reads it before the voice profile loading phase, establishing the priority order early. This mirrors the humanizer's placement (Voice Calibration appears before the pattern categories).

**Alternatives considered**:
- Placing it inside Step 2 (Apply Voice Profile): rejected because it mixes configuration instructions with workflow steps, and the section would be harder to find.
- Placing it at the end of the file: rejected because the LLM would process the entire generation workflow before learning about inline voice matching.

## R3: Voice priority resolution mechanics

**Decision**: Priority order is inline sample > configured voice profile > auto-detection > default. Implemented as a "first match wins" check at the start of Step 2.

**Rationale**: The inline sample is the most explicit user signal (they provided it right now, for this specific request). A configured voice profile is a persistent preference. Auto-detection is a fallback heuristic. This matches user expectations: what you say now overrides what you configured before.

**Alternatives considered**:
- Merging inline sample with voice profile (blend characteristics): rejected because blending is unpredictable and hard to debug. The user should get one clear voice, not a hybrid.
- Voice profile overrides inline sample (configured preference wins): rejected because the inline sample is more specific and intentional.

## R4: File validation approach

**Decision**: When a referenced file doesn't exist or is binary/unreadable, warn the user and fall back to the next voice source in priority order.

**Rationale**: Silent failure would confuse users who expect voice matching. Hard failure would block the rewrite/generation entirely, which is too aggressive for an optional feature. Warning + fallback gives the user information while still producing output.

**Alternatives considered**:
- Silent fallback (no warning): rejected because the user wouldn't know their sample was ignored.
- Hard failure (refuse to process): rejected because voice matching is optional, not required for the core operation.

## R5: Cross-reference wording

**Decision**: Reference "the voice-extractor capability" generically rather than the specific `/prose:voice extract` command path.

**Rationale**: Command paths may change. A generic reference to the capability is more resilient. The spec review agent flagged this as well.

**Alternatives considered**:
- Specific command reference (`/prose:voice extract`): initially proposed but the spec review correctly identified this as fragile.
