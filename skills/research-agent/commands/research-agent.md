# /research-agent

Run the Research Agent workflow in the current repository.

## Purpose

This command helps the user conduct an end-to-end research workflow inside the current repository.

The workflow includes:

1. Repository inspection
2. Optional goal instruction discussion for empty repos
3. Research question setup
4. Motivation
5. Method
6. Experiments
7. HTML research brief
8. Slides

The four explicit research stages live under:

- `stages/01_motivation/`
- `stages/02_method/`
- `stages/03_experiments/`
- `stages/04_slides/`

## First Action

Always inspect the current repository before doing any research work.

Check whether the repository is:

- empty
- an existing user project
- an official baseline implementation
- a partially completed research-agent project

Use `scripts/inspect_repo.py` when available, then read only safe, relevant files needed to confirm the result.

## State Handling

Look for:

- `.research-agent/state.json`
- `.research-agent/config.json`
- `research/status.md`
- `research/motivation.md`
- `research/method.md`
- `research/experiments.md`
- `research/research-brief.html`
- `slides/slide-*.html`
- `slides/viewer.html`
- `slides/research-presentation.pdf`
- `slides/out-png/`
- `slides/research-presentation.pptx` when optional experimental PPTX export is requested

If state exists, resume from the earliest incomplete or stale stage.

If state does not exist, initialize it with `scripts/init_run.py`.

If the repository is `empty_repo`, ask whether the user wants to start with a goal instruction discussion before Motivation. If yes, load `goal-instructor/instructions/goal-design.md`, discuss the automation target, then recommend multiple candidate goal instructions and ask the user to select one.

Use an ask-user-question style tool when available for the final candidate selection. The selected result must be formatted as a payload the user can paste after Codex `/goal`.

## Repository Safety

Never read or modify private credential files.

Do not open or summarize:

- `.env`
- `.env.*`
- `*.pem`
- `*.key`
- `id_rsa`
- `id_ed25519`
- files containing `token`, `secret`, `credential`, or `password` in the filename

Do not overwrite user code unless explicitly asked.

Do not modify baseline implementation files during research planning.

## User Interaction

Ask questions only when a decision blocks progress.

When asking a question, provide:

- a short reason
- a recommended option
- selectable options
- a custom option

If an ask-user-question style tool is available, use it. If not, ask in plain text with the same structure.

## Output Policy

Keep generated files minimal.

Default generated files:

- `.research-agent/state.json`
- `.research-agent/config.json`
- `.research-agent/repo_profile.json`
- `.research-agent/decisions.jsonl`
- `.research-agent/goal_instruction.md` when goal discussion is selected
- `.research-agent/goal_command.txt` when goal discussion is selected
- `.research-agent/goal_instruction.json` when goal discussion is selected
- `research/status.md`
- `research/motivation.md`
- `research/method.md`
- `research/experiments.md`
- `research/research-brief.html`

Generate slides only when the user requests final presentation output or when all prior stages are complete. Slides must use the `slides-grab` HTML-first workflow.
