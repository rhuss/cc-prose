# Brainstorm Overview

Last updated: 2026-06-12

## Sessions

| # | Date | Topic | Status | Spec | Issue |
|---|------|-------|--------|------|-------|
| 01 | 2026-06-12 | humanizer-pattern-sync | active | - | - |
| 02 | 2026-06-12 | inline-voice-matching | active | - | - |
| 03 | 2026-06-12 | false-positive-guidance | active | - | - |
| 04 | 2026-06-12 | self-audit-rewrite-loop | active | - | - |
| 05 | 2026-06-12 | humanizer-upstream-sync | active | - | - |

## Open Threads
- Contribute rule-of-three density detection back to upstream? (from #01)
- Adopt upstream's 3-pass process in content sync or wait for #04? (from #01)
- Content sync (#01) depends on sync mechanism (#05) being implemented first (from #01)
- Should content-generator also get inline voice-matching? (from #02)
- Should humanizer mention voice-extractor for persistent profiles? (from #02)
- If both inline sample AND voice profile present, which wins? (from #02)
- How to handle tension between CLAUDE.md "no em dashes" rule and false-positive guidance? (from #03)
- Should pre-validator subtract points for human signals or just not penalize? (from #03)
- Contribute cluster-detection principle back to upstream? (from #03)
- Should self-audit findings be visible to user by default? (from #04)
- How does self-audit interact with false-positive guidance (#03)? (from #04)
- Should self-audit have a word-count threshold to skip for short texts? (from #04)
- Eliminate canonical copy at ~/.claude/skills/humanizer/ and sync directly from upstream? (from #05)
- Should make check-upstream be a pre-install hook? (from #05)

## Parked Ideas
(none)
