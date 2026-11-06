# Brainstorm Overview

Last updated: 2026-11-06

## Sessions

| # | Date | Topic | Status | Spec | Issue |
|---|------|-------|--------|------|-------|
| 01 | 2026-06-12 | humanizer-pattern-sync | spec-created | 001 | - |
| 02 | 2026-06-12 | inline-voice-matching | spec-created | 003 | - |
| 03 | 2026-06-12 | false-positive-guidance | implemented | 002 | - |
| 04 | 2026-06-12 | self-audit-rewrite-loop | implemented | 004 | - |
| 05 | 2026-06-12 | humanizer-upstream-sync | spec-created | 001 | - |
| 06 | 2026-06-13 | voice-granularity | active | - | - |
| 07 | 2026-11-06 | multi-harness-support | active | - | - |

## Open Threads
- Contribute rule-of-three density detection back to upstream? (from #01)
- ~~Should content-generator also get inline voice-matching? (from #02)~~ **Resolved in spec 003**: Yes, content-generator gets inline voice-matching with the same six analysis dimensions.
- ~~Should humanizer mention voice-extractor for persistent profiles? (from #02)~~ **Resolved in spec 003**: Yes, both skills include a cross-reference to the voice-extractor.
- ~~If both inline sample AND voice profile present, which wins? (from #02)~~ **Resolved in spec 003**: Inline sample wins (most explicit signal). No blending.
- Pre-validator scoring: subtract points for human signals or just not penalize? (from #03)
- CLAUDE.md "no em dashes" rule vs false-positive guidance: coexist as style vs detection (from #03)
- Should self-audit findings be visible to user by default? (from #04)
- How does self-audit interact with false-positive guidance (#03)? (from #04)
- Should self-audit have a word-count threshold to skip for short texts? (from #04)
- Eliminate canonical copy at ~/.claude/skills/humanizer/ and sync directly from upstream? (from #05)
- Should make check-upstream be a pre-install hook? (from #05)
- Which specific measurements should the extractor compute? Full ngpepin set (~86) or curated subset? (from #06)
- Should the self-audit subagent receive measurements, or should a separate validation step check them? (from #06)
- How should measurements interact with inline voice matching (#02)? Inline samples are too short for reliable extraction. (from #06)
- Should we add a `prose:measure` command for standalone text analysis? (from #06)
- What is the minimal OpenCode command shim that reuses shared skill logic? (from #07)
- Which skills, commands, or hooks rely on Claude-only mechanisms? (from #07)
- Where should voice profiles live so they resolve predictably across supported harnesses? (from #07)
- How should consumers detect cc-prose consistently across harnesses? (from #07)

## Parked Ideas
(none)
