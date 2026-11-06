---
runbook_version: 1
feature: 006-multi-harness-support
status: passed
mode: light
steps_total: 5
step_results: passed,passed,passed,passed,passed
drafted_at: 4e1b6b9
drafted_fingerprint: 1c89279ab4d98c2466e8e1df68d2525493c1ffff1b4e325729bdb4740e976065
tested_at: c04bc83
tested_fingerprint: 1c89279ab4d98c2466e8e1df68d2525493c1ffff1b4e325729bdb4740e976065
updated: 2026-11-06
---

# Try it: Shared writing setup across harnesses

<!-- runbook-status -->
> **Status:** passed · 5 of 5 steps (5 passed) · Mode: light · Tested at c04bc83 · 2026-11-06
<!-- /runbook-status -->







## What you're testing

Initialize an isolated writing project and global voice library, inspect configuration precedence, preserve custom settings on rerun, and check the packages that expose these workflows to Codex and OpenCode. This is the local part of the feature. The recorded run used no model credentials.

## Test environment

The agent created the isolated workspace `/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e` during Step 1 of 5 and removed it after all five steps passed. No background process, container, or external service was required. Teardown used Python shutil.rmtree on that verified temporary workspace. Output logs remain under `.walkthrough/`. To rerun, use one shell throughout so its variables persist. Python 3, Node.js, Git, and make are required.

## Steps

### Step 1 of 5: Prepare an isolated writing workspace (US2)

**Why this step:** Keep the trial's profiles and style files separate from your normal settings.

**Needs:** Start in the feature checkout; Python 3, Node.js, Git, and make on PATH.

**Run:**

```bash
PROSE_ROOT=$(git rev-parse --show-toplevel) &&
PROSE_DEMO=$(mktemp -d) &&
test -n "$PROSE_DEMO" &&
mkdir -p "$PROSE_DEMO/home" "$PROSE_DEMO/project" &&
python3 --version &&
node --version &&
make --version
```

**What you should see:** Python and Node version output; the temporary workspace is ready.

**If you see something else:** Install the missing runtime before continuing; verify you started in the feature checkout.

**Result:**

Agent-run: **passed**. Runtime versions reported; isolated home and project directories exist. Actual output: [.walkthrough/step-1.log](.walkthrough/step-1.log).

```text
Python 3.15.0
v26.13.0
GNU Make 3.81
Copyright (C) 2006  Free Software Foundation, Inc.
This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.

This program built for i386-apple-darwin11.3.0
```


### Step 2 of 5: Initialize global and project styles (US2)

**Why this step:** Both scopes use the same layout from every harness.

**Needs:** Step 1 variables in the same shell.

**Run:**

```bash
cd "${PROSE_DEMO:?Run step 1 successfully first}/project" &&
HOME="$PROSE_DEMO/home" python3 "${PROSE_ROOT:?Run step 1 successfully first}/prose/scripts/init_style_config.py" --init-global &&
HOME="$PROSE_DEMO/home" python3 "$PROSE_ROOT/prose/scripts/init_style_config.py" --init
```

**What you should see:** A shared global style directory with eight bundled voices and a project .style directory. All files are under the temporary workspace.

**If you see something else:** A missing-template error means the source package is incomplete; use an intact checkout.

**Result:**

Agent-run: **passed**. Bundled global voices: 8; project configuration exists. Actual output: [.walkthrough/step-2.log](.walkthrough/step-2.log).

```text

Created ~/.claude/style/ directory with:
  - config.yaml
  - styleguide.md
  - wordlist.txt
  - stoplist.txt
  - voices/reasoning.yaml
  - voices/pov.yaml
  - voices/conversational.yaml
  - voices/reference.yaml
  - voices/narrative.yaml
  - voices/tutorial.yaml
  - voices/analytical.yaml
  - voices/technical.yaml

Global configuration initialized at: /var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style

Next steps:
  1. Edit ~/.claude/style/stoplist.txt for your personal blocked words
  2. Edit ~/.claude/style/wordlist.txt for your preferred terms
  3. Edit ~/.claude/style/styleguide.md for your personal style rules
  4. Customize voice profiles in ~/.claude/style/voices/

These settings apply to ALL projects by default.
Create project-specific .style/ directories to override per-project.

Created .style/ directory with:
  - config.yaml
  - styleguide.md
  - wordlist.txt
  - stoplist.txt
  - voice.yaml

Next steps:
  1. Edit .style/stoplist.txt to add blocked words
  2. Edit .style/wordlist.txt to add preferred terms
  3. Edit .style/styleguide.md for project-specific rules
  4. Optionally configure .style/voice.yaml for voice profile
```


### Step 3 of 5: Customize and rerun without losing edits (US2)

**Why this step:** Initialization must preserve user data and fill only missing files.

**Needs:** Step 2.

**Run:**

```bash
cd "${PROSE_DEMO:?Run steps 1 and 2 successfully first}/project" &&
printf 'custom-blocked-word\n' > "${PROSE_DEMO:?Workspace path is required}/project/.style/stoplist.txt" &&
HOME="$PROSE_DEMO/home" python3 "${PROSE_ROOT:?Run step 1 successfully first}/prose/scripts/init_style_config.py" --init &&
cat "$PROSE_DEMO/project/.style/stoplist.txt"
```

**What you should see:** Existing files reported as skipped, no overwrite prompt, and the exact custom stoplist entry retained.

**If you see something else:** Stop and report the changed file before proceeding with real user configuration.

**Result:**

Agent-run: **passed**. Custom stoplist bytes preserved; initialization exited without a prompt. Actual output: [.walkthrough/step-3.log](.walkthrough/step-3.log).

```text
  Skipped: config.yaml (already exists)
  Skipped: styleguide.md (already exists)
  Skipped: wordlist.txt (already exists)
  Skipped: stoplist.txt (already exists)
  Skipped: voice.yaml (already exists)

Next steps:
  1. Edit .style/stoplist.txt to add blocked words
  2. Edit .style/wordlist.txt to add preferred terms
  3. Edit .style/styleguide.md for project-specific rules
  4. Optionally configure .style/voice.yaml for voice profile
custom-blocked-word
```


### Step 4 of 5: Inspect the shared source map (US2)

**Why this step:** Every harness reads the same project overrides and shared global voice library.

**Needs:** Step 3.

**Run:**

```bash
HOME="${PROSE_DEMO:?Run step 1 successfully first}/home" python3 "${PROSE_ROOT:?Run step 1 successfully first}/prose/scripts/resolve_style_config.py" --project-dir "$PROSE_DEMO/project"
```

**What you should see:** JSON global_config paths under the temporary home, project_config paths under the temporary project, the project voice placeholder path, and eight named global voices. No paths should use your real home directory.

**If you see something else:** Check the HOME assignment and --project-dir argument before using the result.

**Result:**

Agent-run: **passed**. Eight named voices; project override path selected; every source path is inside the isolated workspace. Actual output: [.walkthrough/step-4.log](.walkthrough/step-4.log).

```text
{
  "global_config": {
    "config.yaml": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/config.yaml",
    "styleguide.md": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/styleguide.md",
    "wordlist.txt": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/wordlist.txt",
    "stoplist.txt": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/stoplist.txt"
  },
  "project_config": {
    "config.yaml": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/project/.style/config.yaml",
    "styleguide.md": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/project/.style/styleguide.md",
    "wordlist.txt": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/project/.style/wordlist.txt",
    "stoplist.txt": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/project/.style/stoplist.txt"
  },
  "project_voice": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/project/.style/voice.yaml",
  "voices": {
    "analytical": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/voices/analytical.yaml",
    "conversational": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/voices/conversational.yaml",
    "narrative": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/voices/narrative.yaml",
    "pov": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/voices/pov.yaml",
    "reasoning": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/voices/reasoning.yaml",
    "reference": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/voices/reference.yaml",
    "technical": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/voices/technical.yaml",
    "tutorial": "/private/var/folders/3v/16m6pn090hl4d60grm1057ww0000gn/T/tmp.HlfV1Vsh0e/home/.claude/style/voices/tutorial.yaml"
  }
}
```


### Step 5 of 5: Check shared packaging and native adapter contracts (US1)

**Why this step:** The configuration and writing sources must remain exposed consistently to Codex and OpenCode.

**Needs:** Steps 1–4 and Node.js.

**Run:**

```bash
cd "${PROSE_ROOT:?Run step 1 successfully first}" &&
make test-multi-harness
```

**What you should see:** Eleven Python checks and five Node checks pass, including six wrapper mappings, original-skill guide links, shared manifests, V1 registration, V2 registration of eleven skills, and rejection isolation. This checks US1 and US3 adapter contracts, not generated prose.

**If you see something else:** Record the failed test and output; resolve it before installing into your normal harness settings.

**Result:**

Agent-run: **passed**. Eleven Python tests and five Node tests passed. Actual output: [.walkthrough/step-5.log](.walkthrough/step-5.log).

```text
python3 -m unittest discover -s tests -p 'test_multi_harness.py'
node --test tests/opencode.test.mjs
✔ V1 registration is idempotent and preserves other skills paths (0.556209ms)
✔ V2 registers all shared files with usable descriptions and real paths (1.43975ms)
✔ V2 delayed callback rejection does not prevent other registrations (0.476042ms)
✔ V1-shaped or absent setup context is harmless (0.04425ms)
✔ resource paths are independent of the consumer cwd (1.010708ms)
ℹ tests 5
ℹ suites 0
ℹ pass 5
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 80.721125
...........
----------------------------------------------------------------------
Ran 11 tests in 0.380s

OK
```


## Not covered here

A fresh authenticated writing session in each harness is still required to try voice extraction, generation, rewriting, and checking on the same document. OpenCode V1 needs a real V1 host for end-to-end validation. Actual upstream synchronization modifies source and tracking state and requires separate maintainer review. Remote Git installation requires publishing the branch. Native Codex and OpenCode V2 discovery already ran in isolated environments during implementation; details are in quickstart.md.

## Coverage

US2 is exercised through actual file creation, preservation and source discovery. US1 and US3 are exercised through local packaging and native adapter contract checks; model-driven writing behavior is outside this local journey.

## Results

Run completed 2026-11-06 by the agent: **5 of 5 passed, 0 failed, 0 skipped**. Global and project configuration were created in an isolated workspace, custom stoplist bytes survived reinitialization, the resolver selected project overrides and eight named global profiles, and all eleven Python plus five Node checks passed. The workspace was removed after the run. Authenticated model-driven writing, live upstream merges, and a native OpenCode V1 session were not run.
