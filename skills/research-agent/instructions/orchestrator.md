# Orchestrator

## Flow

1. Inspect the current repository.
2. Classify repo type.
3. Check `.research-agent/state.json`.
4. Initialize state if missing.
5. If repo type is `empty_repo`, ask whether to run a goal instruction discussion before Motivation.
6. If repo type is `baseline_working_project`, offer Existing Project Import before Motivation.
7. Summarize current progress to the user.
8. Find the earliest actionable stage.
9. Ask a blocking question only when needed.
10. Run the stage.
11. Update artifacts and state.
12. Render `research/research-brief.html` after meaningful stage updates.
13. Stop when blocked, complete, or waiting for user review.

## Stage Order

1. `repo_inspection`
2. `goal_instruction` only for empty repos when selected by the user
3. `project_import` only for baseline working projects or user-requested retrospective organization
4. `motivation`
5. `method`
6. `experiments`
7. `html_brief`
8. `slides`

The four explicit research stage folders are:

- `stages/01_motivation/`
- `stages/02_method/`
- `stages/03_experiments/`
- `stages/04_slides/`

`html_brief` is a shared synthesis step generated from the accumulated stage state.

## Empty Repo Goal Instruction Flow

When the current repository is `empty_repo` and no previous state exists:

1. Explain that the repo has no baseline, no prior research state, and no research question.
2. Ask whether the user wants to run a `goal instruction discussion`.
3. If yes, load `goal-instructor/instructions/goal-design.md`.
4. Discuss only the missing information that changes the goal:
   - domain or seed question;
   - expected automation depth;
   - toy experiment budget;
   - whether code changes are allowed;
   - output language and slide/report expectations.
5. Recommend 2-3 candidate `goal instruction` options.
6. Ask the user to select, merge, or customize one using an ask-user-question style tool when available.
7. Write selected outputs:
   - `.research-agent/goal_instruction.md`;
   - `.research-agent/goal_command.txt`;
   - `.research-agent/goal_instruction.json` when structured output is useful.
8. Tell the user that the selected instruction is designed to be pasted after Codex `/goal`.
9. Continue to Motivation using the selected goal instruction as context when the user wants to proceed immediately.

If the user declines, continue with the normal empty repo Motivation question.

## Existing Project Import Flow

When the current repository is `baseline_working_project` and no previous research-agent state exists:

1. Explain that the repo appears to contain an official baseline plus user work or experiment artifacts.
2. Ask whether the user wants to run Existing Project Import before normal Motivation.
3. If yes, load `repo-ingestion/instructions/existing-project-import.md`.
4. Use `scripts/create_project_import.py` when available to create the first `.research-agent/project_import.json` and `research/project-import.md` draft.
5. Inspect safe evidence only:
   - baseline identity and paper links;
   - train/eval entry points;
   - git status paths, branches, and recent non-sensitive commit metadata;
   - likely Method files;
   - result folders and small result summary files.
6. Ask for only blocking confirmations, especially authoritative result folders, main baseline, proposed Method files, and intended research question.
7. Write:
   - `.research-agent/project_import.json`;
   - `research/project-import.md`;
   - reconstructed `research/motivation.md` and `research/motivation.ko.md` when enough evidence exists;
   - reconstructed `research/method.md`;
   - reconstructed `research/experiments.md`.
8. Update stage statuses conservatively:
   - mark stages `complete` only when evidence and user confirmation are sufficient;
   - mark stages `in_progress` when local evidence exists but formalization or narrative is incomplete;
   - mark stages `blocked` when an authoritative user decision is missing;
   - mark stages `stale` when existing artifacts conflict with local evidence.
9. Render `research/research-brief.html` once Motivation, Method, and Experiments have coherent content.
10. Continue to `slides` with the `slides-grab` workflow only when the user asks or the imported brief is ready.

If the user declines import mode, continue with normal Motivation while preserving repo inspection evidence.

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
- `.research-agent/project_import.json` when Existing Project Import is selected
- `.research-agent/decisions.jsonl`
- `.research-agent/goal_instruction.md` when selected
- `.research-agent/goal_command.txt` when selected
- `.research-agent/goal_instruction.json` when selected
- `research/status.md`
- `research/project-import.md` when Existing Project Import is selected
- `research/motivation.md`
- `research/motivation.ko.md`
- `research/method.md`
- `research/experiments.md`
- `research/research-brief.html`
- `slides/slide-*.html`, `slides/viewer.html`, `slides/research-presentation.pdf`, and `slides/out-png/` at the final slide stage
- `slides/research-presentation.pptx` only when optional experimental `slides-grab convert` output is requested
