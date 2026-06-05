# Empty Repo Example

## Situation

The user runs `/research-agent` in a repository with no meaningful project files and no `.research-agent/state.json`.

## Expected Detection

- Repository type: `empty_repo`
- Current state: no research question, no baseline, no related work
- Recommended next action: start from Motivation

## Recommended Question

Ask how the user wants to start:

1. Enter a research question directly.
2. Enter an interest domain and let the agent propose candidate questions.
3. Set target venue, field, and constraints first.

Recommended option: domain-first discovery, because there is no baseline or prior state yet.

## Expected Generated Files

- `.research-agent/state.json`
- `.research-agent/config.json`
- `.research-agent/repo_profile.json`
- `.research-agent/decisions.jsonl`
- `research/status.md`
- `research/motivation.md`
- `research/method.md`
- `research/experiments.md`

