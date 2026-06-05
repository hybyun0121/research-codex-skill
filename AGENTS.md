# Agent Instructions

This repository contains a portable Codex Skill, not a research project.

When editing this repo:

- Keep `skills/research-agent/SKILL.md` concise.
- Put stage-specific behavior in `skills/research-agent/stages/01_motivation`, `02_method`, `03_experiments`, and `04_slides`.
- Put shared workflow behavior in `skills/research-agent/instructions/`.
- Put deterministic helpers in `skills/research-agent/scripts/`.
- Do not add extra documentation files unless they are part of the declared structure.
- Do not include secrets, API keys, private templates, or user-specific run outputs.
- Generated research artifacts belong in the user's actual research repo, not this skill repo.

When using this skill in another repo:

- Inspect the current repo first.
- Classify repo type before starting research work.
- Resume from `.research-agent/state.json` when present.
- Ask the user only when a decision blocks progress.
- Use selectable options with a recommended choice whenever an ask-user-question style tool is available.
