# Research: Multi-harness support

## Codex packaging
Decision: add `prose/.codex-plugin/plugin.json` with `skills: "./skills/"` and a repository marketplace.
Rationale: requested superpowers layout; compatibility manifests remain supported. The locally installed superpowers 7.0.1 package uses this format. Current official docs prefer portable root manifests for new packages but do not require converting existing Claude packages.
Alternative: root portable manifest; deferred to avoid unnecessary packaging migration.
Source: https://developers.openai.com/plugins/build/plugins (retrieved 2026-11-06). Local CLI confirms `codex plugin marketplace add` and `codex plugin add`.

## OpenCode packaging
Decision: dependency-free native plugin with V1 named/server export and V2 default setup, package.json and directory index.js, following superpowers. Register shared skills; command workflows are thin skills using the same command sources.
Rationale: installed OpenCode is 2.1.4. Current superpowers source provides a worked V2 native skill registration contract while official OpenCode docs describe V1 config hooks. No session bootstrap is needed because each prose skill loads its own guide.
Alternatives: install-script copies/symlinks require a second installation mechanism; custom command APIs differ across versions and add no workflow value beyond native skill equivalents.
Sources: https://github.com/obra/superpowers/blob/main/.opencode/plugins/superpowers.js ; https://github.com/obra/superpowers/blob/main/package.json ; https://opencode.ai/docs/plugins/ ; https://opencode.ai/docs/skills/ ; https://opencode.ai/docs/commands/ (retrieved 2026-11-06). V2 registration choice is based on the reference implementation; verify against the installed host.

## Shared data
Decision: `~/.claude/style/` stays shared on all harnesses; user explicitly chose this. Project `.style/` and legacy fallbacks remain. No data migration.
Rationale: copyedit interoperability and preservation of existing profiles. A read-only source-discovery helper makes precedence testable without adding a YAML dependency.

## Resource and tool adaptation
Decision: resolve resources relative to the discovered real skill/command path. Load common guide from every skill. Replace mandatory Claude tool names in workflow bodies with action wording and explicit supported mappings.
Rationale: repository AGENTS.md is not assumed to be injected into consumer sessions; plugin env vars vary; no reason to fork writing policies.

## Humanizer maintenance
Decision: retain the repository skill and tracking marker as authoritative. Require maintenance from a writable cc-prose checkout; installed skills explain this prerequisite. Remove the mandatory canonical Claude copy from update instructions and tracking metadata, while preserving upstream diff/merge rules and dry-run semantics.
Rationale: writing to a private Claude user skill is not needed for Codex or OpenCode and is not a valid package update mechanism.

## Native validation follow-up

OpenCode V2 documentation is at https://opencode.ai/v2/docs/plugins/ and https://opencode.ai/v2/docs/skills/. V1 docs above are used only for the legacy hook. V2 plugin startup is asynchronous: a one-shot standalone API request can return before the plugin registers. A persistent isolated server with its temporary authentication credentials discovers all eleven prose skills via GET /api/skill after activation. Codex app-server skills/list also confirms all eleven prose:* names. The host additionally generates source-command-* compatibility aliases from several existing command files; the documented thin skills remain the stable invocation surface.
