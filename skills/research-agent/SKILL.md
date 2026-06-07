---
name: research-agent
description: Use this skill to run a portable, state-aware research agent inside the current repository. It inspects empty repos, existing research repos, and official baseline implementations; initializes or resumes `.research-agent/state.json`; guides Motivation, Method, Experiments, HTML brief, and professor-facing English slides-grab slide reports; and can run an empty-repo goal-instruction discussion before starting research.
---

# Research Agent

## Purpose

Run `/research-agent` in the current research repository to inspect the repo, initialize or resume state, and guide the research process end to end.

## First Step

Always read `commands/research-agent.md` before acting. It defines the command behavior, state handling, safety rules, and output policy.

## Stage Folders

The research workflow is explicitly separated into four stage folders:

- `stages/01_motivation/`: MCP-assisted paper discovery, literature landscape, novelty criteria, candidate scoring, gaps, and selected direction.
- `stages/02_method/`: method claim, mathematical formulation, rigor review, pseudocode, and visuals.
- `stages/03_experiments/`: benchmark planning, sweeps, leaderboard, and qualitative analysis.
- `stages/04_slides/`: professor-facing English `slides-grab` HTML slides, PDF/PNG exports, optional experimental PPTX, and infographic-style visual reports.

Each stage folder owns its stage instructions, schema files, and markdown/template notes. Motivation also includes `mcp-requirements.md` because it depends on paper search, paper reading, citation graph, literature memory, and user decision capabilities.

## Shared Instructions

Load shared instruction files only when needed:

- `instructions/orchestrator.md`: stage selection, state updates, and resume behavior.
- `instructions/repo-inspection.md`: empty repo, user project, official baseline, and partial run detection.
- `instructions/user-interaction.md`: when and how to ask user questions.
- `instructions/html-brief.md`: final readable HTML synthesis.

## Goal Instructor

For `empty_repo` starts, use `goal-instructor/instructions/goal-design.md` when the user chooses to discuss automation goals before starting Motivation. This produces candidate `goal instruction` options for topic selection, Method construction, toy Experiments, and slide/report creation.

## Scripts

Use scripts when deterministic file creation or validation is useful:

- `scripts/inspect_repo.py`
- `scripts/init_run.py`
- `scripts/update_state.py`
- `scripts/render_html.py`
- `scripts/validate_state.py`

## Safety

Never read, summarize, or modify credential files. Never overwrite user code or baseline implementation files during planning unless the user explicitly asks.
