# Data Model

Existing voice/configuration YAML schemas are unchanged.

- Harness entry point: name `prose`, version matching Claude plugin, relative shared skills root. Codex marketplace source resolves `./prose`; OpenCode package root resolves `prose/skills`.
- Skill adapter: directory/name match; description is nonempty; action maps one-to-one to an existing command file. No writing-policy content is copied.
- Style source map: global_config and project_config are filename-to-absolute-path maps for config.yaml, styleguide.md, wordlist.txt, stoplist.txt. Existing preferred directory selects the config layer; legacy is used only when the preferred directory is absent. Project voice selects `.style/voice.yaml`, then `.prose/voice.yaml`; named global voices merge by stem with unified overriding legacy. No persisted state is introduced.
- Humanizer marker: existing upstream SHA/date and local additions remain; legacy canonical_file is no longer required or written by maintenance.
