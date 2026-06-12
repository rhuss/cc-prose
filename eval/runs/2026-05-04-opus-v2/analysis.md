---
agent: Claude Code
model: claude-opus-4-6
date: 2026-05-04T19:00:00Z
---

## Recommendation

**The humanizer skill performs well on content quality (pattern removal, meaning preservation, naturalness). The only regression is voice_announced at 40%, driven by two fixable issues: a regex bug in the judge and the skill's use of compound voice names.**

Top actions:
1. Fix the `voice_announced` judge regex to exclude articles ("a", "an") from capture groups
2. Decide whether compound voice names (technical-direct, technical-neutral) should be accepted as matching their base profile
3. Ensure score.py runs with the `~/.venvs/agent-eval` Python to avoid the `anthropic` import error recurring

## Summary

| Judge | Score | Threshold | Status |
|-------|-------|-----------|--------|
| ai_patterns_removed | 100% pass | 100% | PASS |
| filler_and_hedging | 100% pass | 100% | PASS |
| meaning_preservation | 4.73/5.0 mean | 3.5 | PASS |
| naturalness | 4.60/5.0 mean | 3.5 | PASS |
| voice_announced | 40% pass | 100% | FAIL |

- **15 cases**, all executed successfully
- **511s** wall-clock, **$3.77** total cost
- **$0.067/turn**, 83.6% cache hit rate

## Failure Patterns

### voice_announced (9 failures out of 15)

| Case | Expected | Announced | Issue |
|------|----------|-----------|-------|
| case-003 | pov | "a" | Regex captures article |
| case-004 | tutorial | technical | Skill auto-detected wrong |
| case-005 | technical | direct | Non-canonical voice name |
| case-007 | analytical | technical-direct | Compound name |
| case-008 | reference | technical-neutral | Compound name |
| case-010 | reasoning | technical | Skill doesn't use reasoning |
| case-012 | pov | "a" | Regex captures article |
| case-014 | narrative | technical | Inline text defaults to technical |
| case-015 | analytical | technical | Skill doesn't use analytical |

## Root Causes

1. **Regex bug in judge**: Pattern captures "a" from "using a direct voice"
2. **Skill voice vocabulary mismatch**: The skill uses compound names (technical-direct, technical-neutral, technical-tutorial) and doesn't expose all 8 canonical profiles (analytical, reasoning, reference are absent)

## Cost Attribution

- Total: **$3.77** across 15 cases, 56 turns
- Cost per case: **$0.25** average
- Cost per turn: **$0.067**
- Most expensive: case-006 ($0.37, 8 turns, self-validation loop)
- Cheapest: case-005, case-014 ($0.14 each, inline text, 1 turn)
