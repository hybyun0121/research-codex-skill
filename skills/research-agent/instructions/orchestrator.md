# Orchestrator

## Flow

1. Inspect the current repository.
2. Classify repo type.
3. Check `.research-agent/state.json`.
4. Initialize state if missing.
5. Summarize current progress to the user.
6. Find the earliest actionable stage.
7. Ask a blocking question only when needed.
8. Run the stage.
9. Update artifacts and state.
10. Render `research/research-brief.html` after meaningful stage updates.
11. Stop when blocked, complete, or waiting for user review.

## Stage Order

1. `repo_inspection`
2. `motivation`
3. `method`
4. `experiments`
5. `html_brief`
6. `slides`

The four explicit research stage folders are:

- `stages/01_motivation/`
- `stages/02_method/`
- `stages/03_experiments/`
- `stages/04_slides/`

`html_brief` is a shared synthesis step generated from the accumulated stage state.

## Resume Rule

Resume from the earliest stage whose status is not `complete`, unless a later artifact is newer and clearly supersedes the state. When stale state is suspected, summarize the mismatch and ask before overwriting.

## Status Values

- `not_started`
- `in_progress`
- `blocked`
- `complete`
- `stale`

## Research Repo Outputs

Default outputs in the user's repo are:

- `.research-agent/state.json`
- `.research-agent/config.json`
- `.research-agent/repo_profile.json`
- `.research-agent/decisions.jsonl`
- `research/status.md`
- `research/motivation.md`
- `research/method.md`
- `research/experiments.md`
- `research/research-brief.html`
- `slides/research-presentation.pptx` only at the final slide stage
