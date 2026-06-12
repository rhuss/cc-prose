# Brainstorm: Self-audit rewrite loop

**Date:** 2026-06-12
**Status:** active

## Problem Framing

Our humanizer and content-generator do a single pass: detect patterns, rewrite/generate, deliver. The upstream humanizer v2.8.0 introduced a 3-pass process that catches things the pattern list alone misses:

1. **Draft rewrite** (apply all pattern rules)
2. **Self-audit** ("What makes this still obviously AI-generated?")
3. **Final rewrite** (address the self-audit findings)

The self-audit step is the key innovation. It asks an adversarial question that goes beyond checklist matching. A rewrite can pass all 33 pattern checks and still "feel" AI-generated because of rhythm, structure, or cadence issues that no individual pattern covers. The self-audit catches those.

## Context

### Current process flows

**Humanizer (our v2.1.1):**
1. Read input
2. Detect voice
3. Announce voice
4. Identify pattern instances
5. Rewrite problematic sections
6. Present humanized version + optional change summary

**Content-generator:**
1. Load config (style + voice)
2. Apply voice profile
3. Generate content following all rules
4. Self-validate against humanizer patterns and style rules
5. Deliver publication-ready text

**Pre-validator:**
- 7-phase validation with scoring
- Reports findings but doesn't rewrite

### Upstream process (v2.8.0):
1. Read input, identify patterns
2. Write draft rewrite
3. Ask: "What makes the below so obviously AI generated?" Answer with remaining tells.
4. Revise into final rewrite that addresses them
5. Deliver: draft, self-audit bullets, final rewrite, change summary

### What the self-audit catches that patterns miss
From the upstream example, after a clean draft rewrite:
- "The rhythm is still a bit too tidy (clean contrasts, evenly paced paragraphs)"
- "The named people and study citations can read like plausible-but-made-up placeholders"
- "The closer leans a touch slogan-y rather than sounding like a person talking"

None of these are pattern-category violations. They're higher-order signals that emerge from the text as a whole.

## Approaches Considered

### A: Add self-audit to humanizer, adapt for content-generator (Recommended)
- Humanizer: Adopt the upstream's 3-pass process (draft → self-audit → final)
- Content-generator: Add a self-audit step after generation, before delivery. Same adversarial question: "What makes this obviously AI-generated?"
- Pre-validator: No change (it already does multi-phase validation; the self-audit is a rewriting concern, not a validation concern)

- Pros: Each skill gets the version appropriate to its role. Humanizer rewrites twice. Content-generator self-checks once. Pre-validator stays focused on reporting.
- Cons: Increases token usage (two rewrites instead of one for humanizer). Content-generator already has a self-validate step, adding self-audit is a second check.

### B: Add self-audit to humanizer only
- Only the humanizer gets the 3-pass process
- Content-generator keeps its current self-validate step
- Pros: Simpler change, fewer files
- Cons: Content-generator misses the benefit. Its self-validate checks against rules but doesn't ask the adversarial "does this still feel AI?" question.

### C: Replace content-generator's self-validate with self-audit
- Remove the current self-validate step from content-generator
- Replace with the adversarial self-audit question
- Pros: Simpler content-generator, catches more issues
- Cons: Loses the explicit rule-checking (stoplist, style compliance) that self-validate does

## Decision

Approach A: Add self-audit to both skills, keeping each skill's existing strengths. The humanizer gets the full 3-pass loop. The content-generator keeps its rule-based self-validate AND adds the adversarial self-audit as an additional step.

## Key Requirements

1. **Humanizer process change:**
   - Step 1-5: Same as current (read, detect voice, announce, identify patterns, rewrite)
   - Step 6 (NEW): Self-audit. Ask: "What makes this still obviously AI-generated?" List remaining tells as brief bullets.
   - Step 7 (NEW): Final rewrite addressing the self-audit findings. Also verify no em/en dashes remain.
   - Step 8: Present the final rewrite + self-audit findings + change summary
   - The draft rewrite is internal working state, not shown to user unless requested

2. **Content-generator process change:**
   - Steps 1-4: Same as current (load config, apply voice, generate, self-validate against rules)
   - Step 5 (NEW): Self-audit. Ask: "What makes this obviously AI-generated?" Address any findings.
   - Step 6: Deliver final text
   - The self-audit runs AFTER rule-based self-validate, catching what rules miss

3. **Output format for humanizer:**
   - Show: final rewrite, self-audit findings (brief bullets), change summary
   - Don't show the intermediate draft (it's working state)
   - The upstream shows both draft and final. We should show only the final to keep output concise, but include the self-audit bullets so the user understands what was caught.

4. **The adversarial question must be genuinely adversarial:**
   - Not "does this follow the rules?" (that's what pattern matching does)
   - But "if I showed this to someone, would they say 'this is obviously AI'?"
   - Focus on: rhythm, cadence, structure, tone, specificity, emotional range

## Open Questions

- Does the 3-pass process add noticeable latency? For short texts it shouldn't matter. For long documents, the extra rewrite pass could be significant. Should we add a threshold (e.g., skip self-audit for texts under 100 words)?
- Should the self-audit findings be visible to the user by default, or only on request? Upstream shows them. Showing them builds trust ("here's what I caught on second pass").
- How does this interact with brainstorm #03 (false-positive guidance)? The self-audit should also be aware of false positives and human signals to preserve.
