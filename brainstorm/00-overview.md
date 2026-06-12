# Brainstorm Overview

Last updated: 2026-06-12

## Sessions

| # | Date | Topic | Status | Spec | Issue |
|---|------|-------|--------|------|-------|
| 01 | 2026-06-12 | humanizer-pattern-sync | spec-created | 001 | - |
| 02 | 2026-06-12 | inline-voice-matching | active | - | - |
| 03 | 2026-06-12 | false-positive-guidance | active | - | - |
| 04 | 2026-06-12 | self-audit-rewrite-loop | active | - | - |
| 05 | 2026-06-12 | humanizer-upstream-sync | spec-created | 001 | - |

## Open Threads
- Contribute rule-of-three density detection back to upstream? (from #01)
- Should content-generator also get inline voice-matching? (from #02)
- Should humanizer mention voice-extractor for persistent profiles? (from #02)
- If both inline sample AND voice profile present, which wins? (from #02)
- Pre-validator scoring: subtract points for human signals or just not penalize? (from #03)
- CLAUDE.md "no em dashes" rule vs false-positive guidance: coexist as style vs detection (from #03)
- Should self-audit findings be visible to user by default? (from #04)
- How does self-audit interact with false-positive guidance (#03)? (from #04)
- Should self-audit have a word-count threshold to skip for short texts? (from #04)
- Eliminate canonical copy at ~/.claude/skills/humanizer/ and sync directly from upstream? (from #05)
- Should make check-upstream be a pre-install hook? (from #05)

## Parked Ideas
(none)
