# Running cc-prose across harnesses

Read this guide before executing a prose skill or command. The writing rules and audit prompts in shared skills remain authoritative. Follow the user's instructions and the current harness's permissions.

## Locate resources

Use the real path of the discovered SKILL.md (resolve symlinks) to find the containing prose plugin directory: skills/<name>/SKILL.md is two directory levels below prose/. Commands live at commands/<action>.md under that same root. Resolve scripts/, knowledge-base/, and docs/ there. Do not assume the consumer's cwd is a cc-prose checkout, or that PLUGIN_ROOT or a Claude cache exists. If a resource is missing, report its path and ask the user to reinstall/update the prose package.

## Tools and interaction

| Action | Claude Code | Codex | OpenCode |
|---|---|---|---|
| Read/edit/search files | Read, Edit, Write, Glob, Grep | available file/shell tools | available read/edit/patch/search tools |
| Run Python or Git | Bash | exec_command or available shell tool | V1 bash; V2 shell |
| Ask a question | AskUserQuestion | available user-input tool or a short numbered question in the conversation | available question tool or conversation |
| Load a skill | Skill tool | load its discovered SKILL.md | native skill tool (V1 name, V2 id) |
| Audit with a fresh worker | Agent | spawn_agent/wait_agent if available and permitted | V1 task; V2 subagent, if available and permitted |

Ask one question at a time where the workflow requires user preferences; offer the choices described by the skill. JSON question examples in skills describe question content, not a requirement to call a tool with that exact schema. If delegation is unavailable or prohibited by the user, perform the same audit inline, then disclose that the review did not have independent context. Preserve audit criteria and rewrite limits. Never grant permissions or override user restrictions to make a workflow run.

Slash-command examples in shared workflows show Claude syntax. On Codex invoke the corresponding discovered invocation skill with `$prose:<action>`; on OpenCode load its bare action skill using the native skill tool and provide the arguments. If a host displays a different qualified name, use its displayed name. For write/rewrite/voice/check/init/update-humanizer the action skill reads commands/<action>.md; these files are the single command-workflow source.

## Shared configuration

`~/.claude/style/` is deliberately the shared global data location on all three harnesses, including when Claude Code is not installed. It is not an installation/cache path. Project configuration remains `.style/`.

Before loading configuration, run Python 3 on the resolved `scripts/resolve_style_config.py` path from the consumer project directory. Its JSON is the authoritative source-path map:

- global_config: config.yaml, styleguide.md, wordlist.txt, stoplist.txt from ~/.claude/style/ if that directory exists; otherwise ~/.claude/copyedit/config/ (legacy defaults.yaml supplies config.yaml when present).
- project_config: those files from .style/ if that directory exists, otherwise .copyedit/.
- project_voice: .style/voice.yaml when present, otherwise .prose/voice.yaml, otherwise null. A comment-only placeholder supplies no voice parameters.
- voices: named YAML profiles from ~/.claude/style/voices/ and ~/.claude/prose/voices/. Unified wins when names collide; legacy-only names remain available.

Read the returned paths with available file tools. Missing optional sources are omitted and use built-in defaults. Apply thresholds global then project. Combine global/project wordlists, stoplists and styleguides as the existing workflow specifies. Select an active project voice before a named global profile; inline writing samples retain the precedence defined in the writing skill. Existing shell snippets in workflows illustrate the same directory-level config fallback; use the source map for profile discovery so legacy-only names are not hidden by a unified voices directory.

Initialization writes only missing files and never prompts to overwrite. Run the resolved init_style_config.py with --init or --init-global. A second run fills missing files and preserves existing bytes.

## Consumer detection

Inspect session-visible skill capabilities. Do not inspect plugin registries or assume a cache path means a skill is usable.

| Capability | Claude / Codex plugin-qualified skill | OpenCode native id |
|---|---|---|
| Generate | prose:content-generator | content-generator |
| Humanize | prose:humanizer | humanizer |
| Validate | prose:pre-validator | pre-validator |
| Manage profiles | prose:voice-architect | voice-architect |
| Extract profiles | prose:voice-extractor | voice-extractor |

Require the capabilities the consumer actually needs. If absent, state which are unavailable and use the consumer's documented fallback. The check workflow invokes pre-validator; it is not a separate detection requirement.

## Humanizer maintenance

update-humanizer is a maintainer workflow. Run it from a writable cc-prose checkout containing prose/skills/humanizer/SKILL.md and its tracking state (the marker may be absent for initial baseline setup). Installed plugin caches are distribution artifacts; do not merge upstream changes there or write a separate ~/.claude/skills/humanizer copy. If invoked in a consumer project, request the checkout path, then use it as the maintenance root. --dry-run preserves every source and tracking file. Reinstall or refresh each harness after a source update.
