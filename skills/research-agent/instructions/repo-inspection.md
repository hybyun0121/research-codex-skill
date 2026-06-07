# Repository Inspection

## Goal

Understand the current repository before doing research work.

## Safe Checks

Inspect:

- file tree, excluding hidden credential paths and large generated outputs
- README
- paper links or citations
- license
- dependency files
- training scripts
- evaluation scripts
- configs
- dataset references
- checkpoints or model references
- existing `.research-agent` state

Never read credential files or files whose names contain `token`, `secret`, `credential`, or `password`.

## Repo Types

`empty_repo`:

- no meaningful source files
- no research-agent state
- no baseline README or scripts

`existing_user_project`:

- source files or notebooks exist
- project appears user-authored
- no clear official baseline evidence

`official_baseline`:

- README describes a method, paper, training/evaluation, or benchmark
- citation or paper link exists
- train/eval scripts, configs, requirements, or checkpoints exist

`baseline_working_project`:

- official baseline evidence exists
- user modifications, untracked files, new configs, notebooks, result folders, or experiment summaries exist
- the project appears to contain both baseline code and user-applied Method/Experiments work
- import mode should be offered before normal Motivation/Method/Experiments stages

`partial_research_agent_project`:

- `.research-agent/state.json` or research-agent artifacts exist

## Repo Profile Output

Write `.research-agent/repo_profile.json` with:

- `repo_type`
- `evidence`
- `main_task`
- `implemented_method`
- `claimed_contributions`
- `training_pipeline`
- `evaluation_pipeline`
- `reusable_components`
- `risks`
- `paper_links`
- `license`
- `import_recommended`
- `import_signals`
- `modified_files`
- `candidate_method_files`
- `candidate_config_files`
- `experiment_artifact_dirs`
- `result_files`

For baseline repos, also create `research/repo-understanding.md` only when it materially helps later stages.

For `baseline_working_project`, load `repo-ingestion/instructions/existing-project-import.md` before reconstructing stage artifacts.
