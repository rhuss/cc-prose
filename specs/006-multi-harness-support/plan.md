# Implementation Plan: Multi-harness support

**Branch:** `006-multi-harness-support` | **Date:** 2026-11-06
**Spec:** [spec.md](spec.md)

## Summary

Expose the five authoritative writing skills through Codex metadata and a native OpenCode plugin. Six tiny invocation skills delegate to existing command files, providing command equivalents where a harness does not discover Claude command files. Keep configuration at the user-approved shared locations. Adapt tools through one common harness guide loaded by every skill.

## Technical Context

Markdown skill instructions; Python 3 standard library for configuration inspection and initialization; dependency-free JavaScript ESM for OpenCode registration. Preserve `prose/` as the Claude and Codex plugin root. The repository root supplies OpenCode's package and directory entry points, pointing into `prose/skills/`. Validate with Python unittest, Node's test runner, Claude manifest validation, and isolated native installation/discovery checks. No model-generation tests run automatically.

## Constitution Check

The constitution is an unfilled template; no ratified constraints apply. The project guidance requires inline execution without subagents unless the user requests parallel work. Ship stages and reviews run inline accordingly. Check remains satisfied after design.

## Global Constraints

- Codex first, OpenCode second; Claude Code remains supported.
- All supported harnesses MUST use `~/.claude/style/` as the shared global directory.
- Existing profile schemas and writing algorithms remain unchanged.
- macOS and Linux with Python 3 and standard shell tooling are the initial supported environments.
- No automatic relocation or deletion of user configuration.
- Static checks must not be described as proof of generated-text behavior.

## Structure and Responsibilities

| Path | Responsibility |
|------|----------------|
| `prose/.codex-plugin/plugin.json` | Codex plugin identity and shared skill directory |
| `.agents/plugins/marketplace.json` | Local/repository Codex installation catalog |
| `prose/skills/{write,rewrite,voice,check,init,update-humanizer}/SKILL.md` | Thin invocation skills delegating to `prose/commands/*.md` |
| `prose/docs/harnesses.md` | Resource resolution, tool mappings, native invocation and consumer detection |
| `prose/scripts/resolve_style_config.py` | Deterministic configuration source and profile-path discovery, without parsing or changing YAML |
| `prose/scripts/init_style_config.py` | Idempotent project/global initialization; no interactive overwrite prompt |
| `prose/commands/init.md` | Resolve script location from packaged skill/command location |
| `prose/commands/update-humanizer.md`, `prose/.humanizer-sync` | Authoritative repository maintenance without required Claude canonical copy |
| `.opencode/plugins/prose.js` | Register shared skill files via V1 config hook and V2 skill transform |
| `package.json`, `index.js` | OpenCode git-package and directory entry points |
| `AGENTS.md`, `CLAUDE.md`, `README.md` | Repository guidance and per-harness installation/use |
| `tests/test_multi_harness.py`, `tests/opencode.test.mjs`, `Makefile` | Configuration, packaging, adapter and regression checks |

## Interfaces

- `resolve_style_config.resolve_paths(project_dir: Path, home: Path) -> dict`: `global_config` and `project_config` map filenames to existing absolute paths; `project_voice` is an absolute path or null; `voices` maps profile stems to absolute paths. Preserve existing directory-level fallback for global/project config; profile names merge legacy first then unified, with project active voice preferred. CLI emits JSON, using cwd and Path.home by default.
- Invocation skills locate their containing `prose/` directory using the discovered SKILL.md file's resolved real path, read `docs/harnesses.md`, then read the matching `commands/<action>.md`. `$ARGUMENTS` or the user's text is the command input. Missing resources produce a clear installation error.
- OpenCode V1 `ProsePlugin(context) -> Promise<{config(config): Promise<void>}>` appends the absolute skills directory to `config.skills.paths` once.
- OpenCode V2 default `{id: 'prose', server: ProsePlugin, setup(ctx)}` registers `{id,name,description,path,content}` for each shared skill through `ctx.skill.transform`. Missing files or rejected registrations log actionable errors; one rejection must not hide the other skills. V1-shaped setup contexts return without error.
- Thin wrappers are skills named `write`, `rewrite`, `voice`, `check`, `init`, `update-humanizer`. Claude's existing commands remain authoritative and unchanged in naming. Codex discovers names under the prose plugin; OpenCode discovers bare native skill ids.

## Design Decisions

Keep `.codex-plugin/plugin.json`, as requested and still supported by official documentation. Add a Codex repository marketplace so installation is executable. OpenCode follows superpowers' native package pattern and dual V1/V2 exports; no install script or copied skill tree. Command equivalents use native skills to avoid inventing a second command policy or depending on incompatible V1/V2 command registration APIs.

All five existing skills load the common guide before running; it maps questions, shell/file tools, skill loading, and self-audit delegation. User restrictions always apply. If no permitted delegation tool exists, the same audit runs inline and its weaker isolation is disclosed. Preserve writing policies outside those tool substitutions.

## Review Focus and Validation

- Configuration: empty home/project; global unified versus legacy directories; project overrides; duplicate profile names; legacy-only profiles beside unified profiles; no YAML parsing or writes by discovery.
- Initializer: rerun with stdin closed must succeed; existing bytes preserved; missing files filled; eight bundled templates copied; symlinked installation resolves real resources.
- Packaging: valid manifests, six wrapper-to-command mappings, all paths confined to packaged root, descriptions parse including folded YAML descriptions.
- OpenCode: V1 hook twice, V2 registration of all eleven skills, callback rejection isolation, absent context, resources resolved independently of cwd, real host discovery if available.
- Maintenance: update instructions target repository sources and preserve dry-run and local-addition handling; no forced writes into another harness's cache.

## Delivery Order

1. Shared configuration and tool guidance.
2. Codex package and thin invocation skills; validate primary integration.
3. OpenCode package adapter; validate secondary integration.
4. Documentation, full local checks, code/spec review, runbook draft.
