# Research: Self-Audit Rewrite Loop

**Feature**: 004-self-audit-rewrite-loop | **Date**: 2026-06-12

## Summary

All technical decisions were resolved during the clarification phase. No external research was required. This document consolidates the findings.

## Decisions

### 1. Correction Loop Bound (FR-010)

- **Decision**: Single correction pass
- **Rationale**: Prevents infinite loops. One re-validation round catches introduced violations without compounding. If text still has issues after two total rewrites, the problem is in the rewrite prompt.
- **Alternatives considered**: Up to 3 passes (unnecessary complexity), unbounded loop (risk of non-convergence)

### 2. Content-Generator Self-Audit Flow (FR-004)

- **Decision**: Mirror humanizer flow: generate, self-validate, self-audit, rewrite, deliver
- **Rationale**: Consistent architecture across both skills. Self-audit logic pattern is reusable and testable in the same way.
- **Alternatives considered**: Inline fixes during generation (loses separation of concerns), audit-only without rewrite (findings without action are low value)

### 3. Self-Audit Prompt Style (FR-006)

- **Decision**: Single open-ended adversarial question
- **Rationale**: Open-ended form surfaces unexpected tells that a fixed checklist would miss. A checklist risks becoming another pattern-rule system.
- **Alternatives considered**: Structured checklist (becomes another rule system), open-ended with hints (constrains adversarial nature)

### 4. Output Placement (FR-003, FR-011)

- **Decision**: Self-audit findings appear after content in a clearly labeled section
- **Rationale**: Primary deliverable stays front and center. User reads content first, then reviews what the audit caught.
- **Alternatives considered**: Before content (buries main output), inline annotations (clutters content)

### 5. False-Positive Access Mechanism (FR-007)

- **Decision**: Embed guidance inline in the self-audit prompt instructions
- **Rationale**: Keeps self-audit self-contained. No runtime file lookups needed.
- **Alternatives considered**: External file reference (adds runtime dependency), rely on existing pattern rules (insufficient for adversarial question)

## Existing Implementation Analysis

### Humanizer Self-Audit (Current State)

The humanizer already has a basic self-audit in "Process and Output" (SKILL.md lines 594-601):

```
1. Read the input carefully and identify every instance of the patterns above.
2. Write a draft rewrite.
3. Ask: "What makes the below so obviously AI generated?" Answer briefly.
4. Revise into a final rewrite that addresses them.
```

Current delivery: "Deliver the draft, the brief 'still-AI' bullets, the final rewrite, and (optionally) a short summary of changes."

**Gaps vs. spec requirements**:
- No false-positive guidance in the self-audit step
- No explicit focus on higher-order signals vs. pattern rules
- No correction pass bound (could theoretically loop)
- Delivers the draft (spec says final rewrite only)
- Findings not explicitly placed after content

### Content-Generator Self-Audit (Current State)

No self-audit exists. The flow ends with rule-based self-validation (Step 6) followed by content presentation (Step 7).

### False-Positive Guidance Sources

Two existing sections provide false-positive context:

1. **Humanizer "What NOT to flag"** (lines 559-576): 13 false-positive categories
2. **Content-generator "Preserve Human Writing Signals"** (Step 5b, lines 409-419): 6 protected signal categories

These will be distilled into inline false-positive guidance for the self-audit prompt.
