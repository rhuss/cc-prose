---
agent: Claude Code
model: claude-opus-4-6
date: 2026-05-04T11:00:00Z
---

## Recommendation

**Verdict: eval harness is solid, two skill improvements remain.**

The judges are now calibrated correctly. AI pattern removal and filler/hedging pass at 100%. Meaning preservation averages 4.6/5, naturalness 4.0/5. Voice announcement works mechanically (the skill announces before rewriting) but the skill invents compound voice names instead of using the 8 defined ones from the detection table.

**Actions for next iteration:**
1. Constrain the humanizer SKILL.md to only use the 8 defined voice names (pov, reasoning, tutorial, narrative, analytical, reference, conversational, technical), not invented compounds
2. Improve naturalness for "technical" voice by adding personality guidance specific to technical writing in the SKILL.md

## Summary

| Judge | Score | Threshold | Status |
|-------|-------|-----------|--------|
| ai_patterns_removed | 100% pass | >= 100% | PASS |
| filler_and_hedging | 100% pass | >= 100% | PASS |
| meaning_preservation | 4.6/5 mean | >= 3.5 | PASS |
| naturalness | 4.0/5 mean | >= 3.5 | PASS |
| voice_announced | 40% pass | >= 100% | FAIL |

| Metric | Value |
|--------|-------|
| Cases | 5/5 passed execution |
| Duration | 205s total |
| Cost | $1.52 total, $0.30/case |

## Failure Patterns

**voice_announced (40%)**: The skill announces a voice in every case, but uses invented compound names instead of the 8 defined voices:
- `technical-direct` (expected `technical`) - PASS (contains "technical")
- `technical-neutral` (expected `technical`) - PASS (contains "technical")
- `direct-opinion` (expected `pov`) - FAIL (no relation to "pov")
- `technical-casual` (expected `tutorial`) - FAIL (wrong voice)
- `neutral-direct` (expected `technical`) - FAIL (no relation to "technical")

## Root Causes

The SKILL.md voice detection table defines 8 specific voices but doesn't explicitly forbid inventing new ones. The skill interprets the table as suggestions and creates ad-hoc descriptors. Fixing this requires adding a constraint like "ONLY use these exact voice names" to the SKILL.md.

## Cost Attribution

- $1.52 total, $0.30/case average
- Case 003 was most expensive ($0.41, 12 turns) due to invoking prose:check
- Case 005 cheapest ($0.14, 1 turn)
