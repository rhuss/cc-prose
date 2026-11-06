# Brainstorm: Multi-harness support (Codex, OpenCode)

**Date:** 2026-11-06
**Status:** active

## Problem Framing

cc-prose ships as a Claude Code plugin only. The repository carries a single
`prose/.claude-plugin/plugin.json`, its description reads "for Claude Code",
and there is no manifest, installer, or agent-instruction file for any other
harness. The five skills (`content-generator`, `humanizer`, `pre-validator`,
`voice-architect`, `voice-extractor`) and the slash commands therefore resolve
only under Claude Code.

This now blocks real work. The cc-guide plugin is being ported to run its full
command set on Codex (primary) and OpenCode (secondary). cc-guide's page
writing uses cc-prose when present (voice profiles via `prose:content-generator`,
an AI-pattern gate via `prose:check`) and falls back to a built-in style-rules
file when absent. On Codex, cc-prose is absent, so guides written there lose
named voice profiles and the automated AI-slop gate and run on the fallback.
Any other writing task a user runs on Codex or OpenCode loses the same.

superpowers, which cc-guide also depends on, already solved exactly this and is
the model to copy. Its 7.0.0 package carries per-harness manifests
(`.codex-plugin/`, `.opencode/`, `.cursor-plugin/`, `.devin-plugin/`, and
more), an `AGENTS.md`, a `gemini-extension.json`, and a set of
`skills/using-superpowers/references/<harness>-tools.md` files that map
harness-specific tool differences (for example `codex-tools.md` covers Codex's
`spawn_agent`/`wait_agent` multi-agent dispatch). All harnesses share one
`skills/` directory; each manifest just points `"skills": "./skills/"`.

**Success:** the prose skills resolve and run with identical behavior on Codex
and OpenCode, installed through each harness's own plugin mechanism, so a
consumer (cc-guide, or a user writing directly) detects `prose:*` as available
and gets voice profiles plus the AI-pattern check, not the fallback.

**Non-goals / anti-goals:**
- Not a rewrite of any skill's prose logic. The skills are text-processing and
  should already be harness-neutral in substance; this is packaging plus a
  small audit, not new writing behavior.
- Do not fork behavior per harness. One `skills/` directory, one source of
  truth. A per-harness file exists only where a genuine tool difference forces
  it (the superpowers `references/<harness>-tools.md` pattern).
- Do not break the existing Claude Code install or the humanizer upstream-sync
  flow (see brainstorm 05).

## Approaches Considered

### A: Mimic superpowers packaging (recommended)

Add per-harness entry points alongside the existing `prose/.claude-plugin/`,
mirroring superpowers one-for-one:

- `prose/.codex-plugin/plugin.json` with `"skills": "./skills/"` (Codex reads
  its own manifest, ignores the others).
- `prose/.opencode/` (plus OpenCode command shims, see Open Questions) so the
  commands install on OpenCode.
- An `AGENTS.md` at the repo root for AGENTS-based harnesses.
- `skills/.../references/<harness>-tools.md` only for skills that need
  harness-specific tool guidance. cc-prose skills are text transforms, so this
  set is expected to be small or empty.
- Keep one shared `skills/` directory; every manifest points at it.

- Pros: proven pattern in a sibling plugin by the same author; all harnesses
  share one skill source so behavior cannot drift; extends cleanly to the other
  harnesses superpowers already supports (Cursor, Devin, Gemini, Droid,
  Copilot) if wanted later.
- Cons: commands exist in two shapes (Claude `commands/`, OpenCode command
  files), so command parity needs its own small shim layer; each added harness
  is a new install path to document and test.

### B: Thin AGENTS.md + OpenCode install script (cc-review variant)

cc-review supports the same harnesses with a lighter touch: a `.codex-plugin/`
manifest, an `opencode/install.sh` that copies command shims into
`.opencode/plugins/`, and an `AGENTS.md`. No per-harness reference files because
its skills delegate to a harness-neutral `core/`.

- Pros: fewer files; the OpenCode install is explicit and scriptable.
- Cons: diverges from the superpowers template the user asked to follow; the
  install-script path is more to maintain than a declarative manifest; still
  needs the same command-parity work.

### C: Do nothing, rely on consumers' fallback (status quo, rejected)

Leave cc-prose Claude-only; consumers like cc-guide keep using their built-in
style rules on other harnesses.

- Pros: zero work.
- Cons: this is exactly the gap that triggered this brainstorm. Codex and
  OpenCode users permanently lose voice profiles and the AI-pattern gate.

## Decision

Adopt **Approach A**: package cc-prose for multiple harnesses by mimicking the
superpowers layout, Codex first and OpenCode second. Prefer superpowers' set of
files and conventions over cc-review's install-script variant, since the user
asked to follow the superpowers way and it keeps one shared skill source.

## Key Requirements

- Add `prose/.codex-plugin/plugin.json` (mirror the Claude manifest, point
  `"skills": "./skills/"`) and the OpenCode entry point, modeled directly on
  superpowers 7.0.0.
- Add a repo-root `AGENTS.md` with the agent instructions for AGENTS-based
  harnesses, following superpowers' `AGENTS.md`.
- Keep a single shared `skills/` directory; no per-harness behavior fork.
- Audit each skill and command for Claude-only assumptions (tool names, hooks,
  `.claude/settings*.json` permission reads, fixed `~/.claude/...` paths,
  MCP use) and replace them with harness-neutral equivalents or a
  `references/<harness>-tools.md` note where a real tool difference exists.
- Preserve the humanizer upstream-sync flow (the `.humanizer-sync` marker and
  `prose:update-humanizer`, from brainstorm 05) across harnesses: it must not
  depend on a Claude-only path.
- Keep `prose/scripts/init_style_config.py` invocable without a Claude-specific
  path (it is Python, so portable; confirm the skills call it by a resolved
  path, not a hard-coded plugin location).
- Behavior parity is the acceptance bar: on Codex and OpenCode a consumer that
  detects `prose:humanizer`/`prose:content-generator` as available gets the
  same voice profiles and AI-pattern check as on Claude Code.

## Open Questions

- Command vs skill parity: Claude Code uses `prose/commands/` plus `skills/`;
  Codex discovers skills from the manifest; OpenCode expects command files (as
  in cc-review's `opencode/command/*.md`). What is the minimal shim that keeps
  the slash commands working on OpenCode without duplicating skill logic?
- Does any cc-prose skill, command, or hook rely on Claude-only mechanisms
  (hooks wired in `plugin.json`, `.claude/settings*.json`, MCP)? The audit sets
  the real size of this work.
- Where do voice profiles get stored per harness? Claude Code uses
  `~/.claude/...`; Codex and OpenCode have their own config homes. Profiles
  created on one harness should resolve predictably, and `voice-architect` /
  `voice-extractor` need a home that each harness can read.
- Detection contract for consumers: standardize on "is `prose:humanizer`
  exposed in this session" (the method cc-review uses) and document it, so
  cc-guide and others detect cc-prose the same way on every harness instead of
  reading a plugin registry.
- Which harnesses beyond Codex and OpenCode are in scope now versus later? The
  superpowers template makes Cursor, Devin, Gemini, Droid, and Copilot cheap
  follow-ons, but each adds an install path to document and test.

## Reference implementations

- superpowers 7.0.0 (the template to copy): per-harness manifests, `AGENTS.md`,
  `gemini-extension.json`, and `skills/using-superpowers/references/<harness>-tools.md`.
  Repo: https://github.com/obra/superpowers
- cc-review (a second worked example by the same author): `review/.codex-plugin/`,
  `review/opencode/install.sh`, repo-root `AGENTS.md`.
  Repo: https://github.com/rhuss/cc-review
