# Research Agent Skill

A portable Codex Skill for running an end-to-end research workflow inside any research repository.

Use it when you want Codex to inspect a local research project, understand its current state, and guide the process from Motivation to Method, Experiments, HTML brief, and final presentation slides.

For empty repositories, `research-agent` can first run a goal-instruction discussion. That discussion helps the user define automation scope, then recommends several candidate `goal instruction` options for topic selection, Method construction, toy Experiments, and slide/report creation.

## Skill Structure

The skill separates the research workflow into four explicit stage folders, with an optional goal-instructor module for empty repo onboarding:

```text
skills/research-agent/
├── goal-instructor/
│   ├── instructions/
│   ├── schemas/
│   └── templates/
├── stages/
│   ├── 01_motivation/
│   │   ├── instructions.md
│   │   ├── mcp-requirements.md
│   │   ├── report-template.md
│   │   ├── report-template.ko.md
│   │   ├── report-checklist.md
│   │   ├── research-question.schema.json
│   │   ├── paper.schema.json
│   │   ├── landscape.schema.json
│   │   ├── motivation-report.schema.json
│   │   ├── candidate-topic.schema.json
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
git clone https://github.com/hybyun0121/research-codex-skill.git
```

Open your actual research project:

```bash
cd <your-research-project>
codex
```

Run:

```text
$research-agent
```

You can also type `/skills` and select `research-agent`.

The agent will inspect the repository, determine whether it is an empty repo, an existing research project, an official baseline implementation, or a partially completed research-agent project, then continue from the next required stage.

## Optional Vendor Install

You can vendor the skill into a research repo:

```bash
mkdir -p .agents/skills
cp -r ../research-codex-skill/skills/research-agent .agents/skills/
codex
```

Then run:

```text
$research-agent
```

For an empty repo, the agent will ask whether you want to start with a goal-instruction discussion. If selected, it will recommend several candidate `goal instruction` options before continuing to Motivation.

```text
Use $research-agent to inspect this empty repo and discuss goal instruction options before starting Motivation.
```

## Files Generated In The Research Repo

The skill keeps outputs minimal:

```text
.research-agent/
├── state.json
├── config.json
├── repo_profile.json
├── decisions.jsonl
├── goal_instruction.md
└── goal_instruction.json
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
