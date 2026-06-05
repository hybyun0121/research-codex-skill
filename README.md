# Research Agent Skill

A portable Codex Skill for running an end-to-end research workflow inside any research repository.

Use it when you want Codex to inspect a local research project, understand its current state, and guide the process from Motivation to Method, Experiments, HTML brief, and final presentation slides.

## Skill Structure

The skill separates the research workflow into four explicit stage folders:

```text
skills/research-agent/
├── stages/
│   ├── 01_motivation/
│   │   ├── instructions.md
│   │   ├── research-question.schema.json
│   │   ├── paper.schema.json
│   │   └── template.md
│   ├── 02_method/
│   │   ├── instructions.md
│   │   ├── method.schema.json
│   │   └── template.md
│   ├── 03_experiments/
│   │   ├── instructions.md
│   │   ├── experiment.schema.json
│   │   ├── leaderboard.schema.json
│   │   └── template.md
│   └── 04_slides/
│       ├── instructions.md
│       └── pptx-template.md
├── instructions/
│   ├── orchestrator.md
│   ├── repo-inspection.md
│   ├── user-interaction.md
│   └── html-brief.md
└── scripts/
```

HTML brief generation is a shared synthesis step because it renders the accumulated state from the four research stages.

## Usage

Clone this skill repository:

```bash
git clone https://github.com/<org>/research-agent-skill.git
```

Open your actual research project:

```bash
cd <your-research-project>
codex
```

Run:

```text
/research-agent
```

The agent will inspect the repository, determine whether it is an empty repo, an existing research project, an official baseline implementation, or a partially completed research-agent project, then continue from the next required stage.

## Optional Vendor Install

You can vendor the skill into a research repo:

```bash
mkdir -p .codex/skills
cp -r ../research-agent-skill/skills/research-agent .codex/skills/
codex
```

Then run:

```text
/research-agent
```

## Files Generated In The Research Repo

The skill keeps outputs minimal:

```text
.research-agent/
├── state.json
├── config.json
├── repo_profile.json
└── decisions.jsonl
research/
├── status.md
├── motivation.md
├── method.md
├── experiments.md
└── research-brief.html
slides/
└── research-presentation.pptx
```

Slides are generated only when requested or when all earlier stages are complete.

## Safety

The agent must not read, summarize, or modify credential files such as `.env`, private keys, tokens, certificates, or files whose names include `secret`, `credential`, `password`, or `token`.
