# Validation Quickstart

Prerequisites: Python 3, Node.js with node:test, optional installed Codex/Claude/OpenCode CLIs.

1. Run `make test-multi-harness` for isolated configuration, idempotence, source mapping, manifests and plugin hooks. It must pass without touching real user configuration.
2. Run `make validate` if Claude CLI is available.
3. Follow README's Codex installation using a temporary CODEX_HOME and the repository's absolute path. Check plugin installation and a fresh session's skill list for the five writing skills plus six invocation skills.
4. Use OpenCode's documented local directory plugin configuration in an isolated temporary project/config/data directory. Query native skill discovery without generation and verify all eleven entries and their source paths.
5. For manual generation, use the same sample document, project voice and stoplist in each harness, invoke write/rewrite/check, and verify selection and rules. LLM wording need not match. Record unrun steps explicitly.
6. Test humanizer update with --dry-run from a writable checkout; confirm no source/tracking changes. Do not run actual upstream merges during package validation.

## Validation record — 2026-11-06

- Python configuration/packaging/initialization checks: 11 passed (including stdin-closed reruns, preserved user bytes, all eight templates, source path precedence, and missing-resource error).
- Node V1/V2 adapter checks: 5 passed, including delayed registration rejection isolation and cwd-independent resources.
- Native Codex: temporary CODEX_HOME marketplace add/install/list all succeeded; app-server initialize then skills/list found all eleven prose:* skills at installed cache paths. Codex also generated source-command-* compatibility aliases from legacy command files; these are host-managed and not the documented invocation surface.
- Native OpenCode 2.1.4: temporary HOME and XDG directories, isolated consumer opencode.json with the absolute repository directory in plugins. A persistent authenticated local server returned all eleven prose skill ids with source paths via GET /api/skill. Immediate standalone queries can precede asynchronous plugin activation and must not be treated as discovery failures.
- Claude CLI plugin and marketplace validation passed. The stale marketplace version was aligned to 1.1.0. The existing missing-listing-icon warning is advisory.
- No model generation, voice extraction, or actual upstream merge was run. Cross-harness generated-text/profile behavior still needs a separate authenticated writing walkthrough; the local runbook covers configuration and adapter contracts only. OpenCode V1 was validated by hook contract tests, not an installed V1 host. Remote git-package installation awaits publishing this branch; the native local-directory path was exercised.
- Test sessions used isolated temporary state; normal user harness settings and profiles were not modified.

Finish walkthrough: all five local runbook steps passed on 2026-11-06, including the 16-test suite. The isolated workspace was removed afterward. The runbook includes observed outputs; it does not claim authenticated writing parity was exercised.
