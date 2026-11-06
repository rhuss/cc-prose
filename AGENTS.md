<!-- >>> spex managed Codex guidance >>>
This block is managed from .specify/spex.json. Keep project guidance outside it.
-->

## Spex workflow in Codex

Invoke Spex skills with `$`, for example `$speckit-specify`, `$speckit-plan`,
`$speckit-tasks`, and `$speckit-implement`. Do not print `/...` examples for
Codex skills. Use `$speckit-spex-help` for the current command list.

When a Spex skill needs a choice, present a short numbered list inline and wait
for the answer. Use Codex subagents only when the user requests parallel work.

<!-- <<< spex managed Codex guidance <<< -->

## cc-prose development and usage

cc-prose packages shared writing skills for Claude Code, Codex, and OpenCode.
Read `prose/docs/harnesses.md` for resource resolution, native tool and invocation mappings, configuration precedence, and consumer detection.

For human-readable prose, use content-generator for creation, humanizer for rewriting, pre-validator for checking, voice-architect for managing profiles, and voice-extractor for deriving profiles. An explicit voice mention routes creation or editing to the corresponding writing skill. Machine-readable code, configuration, and git metadata do not activate writing skills.

Global styles and voices are shared at `~/.claude/style/` on every harness. Project data uses `.style/`; existing legacy fallbacks remain supported.

Run `make test-multi-harness` for isolated checks and `make validate` for Claude packaging. Maintain the authoritative humanizer in this checkout; see `prose/commands/update-humanizer.md`.
