# Tasks: Multi-harness support

**Input:** [plan.md](plan.md), [spec.md](spec.md), research, data model and harness contract.
**Execution:** Inline, dependency order. Configuration/adapter tests are required by SC-001 through SC-005.

## Phase 1: Setup

- [x] T001 Record the portability audit and resource/tool/configuration contract in `prose/docs/harnesses.md`, plus repository guidance in `AGENTS.md`; preserve the supplied Spex guidance.

## Phase 2: Shared foundation

- [x] T002 Implement source-only `resolve_paths(project_dir: Path, home: Path) -> dict` and JSON CLI in `prose/scripts/resolve_style_config.py`; test empty roots, preferred directory fallback, duplicate and legacy-only named voices in `tests/test_multi_harness.py`. **Interface:** JSON keys global_config, project_config, project_voice, voices as specified in plan; no writes or YAML parsing.
- [x] T003 Make both modes of `prose/scripts/init_style_config.py` noninteractive and idempotent; preserve bytes, fill missing files and resolve templates via real file path. Extend `tests/test_multi_harness.py` with stdin-closed reruns and symlink resource checks. **Interface:** existing --init and --init-global CLI retained.

## Phase 3: US1 - Codex first

Goal: install and invoke the shared workflows in Codex. Independent check: isolated native plugin installation plus manifest/wrapper tests.

- [x] T004 [US1] Add `prose/.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and six thin invocation skills under `prose/skills/{write,rewrite,voice,check,init,update-humanizer}/SKILL.md`; test valid manifests and exact wrapper-to-command mapping in `tests/test_multi_harness.py`. **Interface:** command sources remain `prose/commands/<action>.md`; resolve prose root using real discovered SKILL.md path.
- [x] T005 [US1] Load the common guide from all five existing `prose/skills/*/SKILL.md`; replace mandatory Claude question/Agent calls in bodies with portable actions while preserving audit prompts and writing policies. Update `prose/commands/init.md` resource invocation. **Interface:** use T002's source map and the T001 guide; allow shell execution in Claude frontmatter where required.
- [x] T006 [US1] Update `prose/commands/update-humanizer.md`, `prose/.humanizer-sync`, `CLAUDE.md`, and relevant maintenance docs so writable checkout sources are authoritative; remove required canonical Claude copy, preserve dry-run/local additions/network failure behavior. Check instructions and metadata in `tests/test_multi_harness.py`.

## Phase 4: US2 - Shared configuration

Goal: all harnesses resolve identical style sources and profile names. Independent check: shared source-map fixtures and initializer reruns.

- [x] T007 [US2] Align configuration instructions in all five `prose/skills/*/SKILL.md`, `prose/commands/{check,init,voice}.md` and `prose/docs/harnesses.md` with T002 source-map precedence; distinguish the shared global data path from harness installation locations. Exercise precedence using `tests/test_multi_harness.py`.

## Phase 5: US3 - OpenCode second

Goal: install the same sources through native OpenCode plugin packaging. Independent check: V1/V2 adapter contract tests and native discovery when available.

- [x] T008 [US3] Add dependency-free `.opencode/plugins/prose.js`, root `package.json` and `index.js`; register every shared skill using the V1 config path and V2 skill transform. Add `tests/opencode.test.mjs` for repeated config hooks, all eleven skills, folded descriptions, absent context, rejection isolation and cwd independence. **Interface:** ProsePlugin(context) -> hooks; default {id,server,setup}; Skill.Info fields id/name/description/path/content; no policy copies.

## Phase 6: Cross-cutting validation and documentation

- [x] T009 Add `make test-multi-harness` in `Makefile`; update `README.md`, `prose/docs/help.md` and `prose/docs/tutorial.md` with native installation, invocation matrix, capability detection, shared data paths and maintenance prerequisites. Run Python/Node checks and available Claude validation; record actual results in `specs/006-multi-harness-support/quickstart.md`.
- [x] T010 Exercise isolated native Codex installation and OpenCode discovery without model generation; review all changes against the spec and record runtime limits in `specs/006-multi-harness-support/quickstart.md`. Draft `RUNBOOK.md` after code review via walkthrough.

## Dependencies and delivery

T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T010. Codex capability is established before OpenCode. Shared configuration is used by every harness rather than being a second subsystem. No parallel execution is requested; Python packaging tests and JavaScript hook tests could be maintained separately after their dependencies, but execute inline here.

## Requirement coverage

FR-001 T004/T010; FR-002 T008/T010; FR-003 T004/T005/T008; FR-004 T004/T009; FR-005 T005/T007/T010; FR-006 T002/T007; FR-007 T003/T005; FR-008 T004/T009/T010; FR-009 T001/T005/T008; FR-010 T006; FR-011 T003/T006/T009; FR-012 T009/T010. SC-001 T004/T008/T010; SC-002 T002/T007; SC-003 T004/T008/T009; SC-004 T003; SC-005 T009/T010.
