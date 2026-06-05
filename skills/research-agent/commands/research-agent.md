# /research-agent

Run the Research Agent workflow in the current repository.

## Purpose

This command helps the user conduct an end-to-end research workflow inside the current repository.

The workflow includes:

1. Repository inspection
2. Research question setup
3. Motivation
4. Method
5. Experiments
6. HTML research brief
7. Slides

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
- `slides/research-presentation.pptx`

If state exists, resume from the earliest incomplete or stale stage.

If state does not exist, initialize it with `scripts/init_run.py`.

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
- `research/status.md`
- `research/motivation.md`
- `research/method.md`
- `research/experiments.md`
- `research/research-brief.html`

Generate slides only when the user requests final presentation output or when all prior stages are complete.
