# Goal Instruction Design

## Objective

Draft a goal instruction that lets Codex run an automated research workflow while still pausing at high-impact decision points.

This module is part of `research-agent`, not a separate skill. Use it primarily when `/research-agent` detects an `empty_repo` and the user chooses to discuss automation goals before Motivation.

The goal should cover:

1. research topic selection;
2. Motivation report;
3. Method construction;
4. toy experiment design and execution;
5. slide/report creation.

## Required Inputs

Ask only for missing information that materially changes the goal instruction:

- target domain or initial research question;
- baseline repo availability;
- compute/time budget;
- desired output depth;
- whether toy experiments may modify code;
- preferred language for reports/slides.

If missing details are not critical, make conservative assumptions and include them in the generated instruction.

## User Interaction

Use Korean/English mixed style while discussing the goal:

- keep technical terms in English: `goal instruction`, `research question`, `Motivation`, `Method`, `Experiments`, `toy experiment`, `slide report`, `decision gate`, `success criteria`;
- use Korean for ordinary explanation, tradeoffs, and recommendations;
- write final `goal instruction` candidates in English unless the user requests Korean.

The discussion must end by recommending 2-3 candidate `goal instruction` options and asking the user to select, merge, or customize one.

When choosing among candidate `goal instruction` options:

- use an ask-user-question style tool when available;
- present the recommended option first;
- provide 2-3 mutually exclusive choices;
- let the user provide a custom option;
- explain the recommendation in Korean while keeping option labels in English.

Do not finish the discussion by merely listing candidates. The user must make or confirm a selection.

## Goal Structure

A strong goal instruction must include:

- mission statement;
- repo inspection requirement;
- safety constraints;
- workflow stages;
- decision gates;
- artifact outputs;
- toy experiment scope;
- success criteria;
- stop conditions;
- reporting language requirements;
- provenance and evidence logging.
- a final form that can be pasted after Codex `/goal`.

## Automation Rules

- The agent should inspect the current repo before proposing research topics.
- The agent should use `$research-agent` when available.
- The agent should not read or expose credential files.
- The agent should avoid modifying baseline implementation files unless explicitly allowed.
- The agent should make progress autonomously when a reasonable assumption is safe.
- The agent should ask the user only when a decision changes the research direction, method, experiment budget, or final artifact format.
- Toy experiments must be small, reproducible, and cheap by default.
- If full experiments are expensive, the agent should run a toy proxy and write down what evidence it does and does not provide.

## Decision Gates

Include these gates by default:

1. Topic gate: before committing to a selected research direction.
2. Method gate: before implementing or claiming a specific method.
3. Experiment gate: before running code that changes files, consumes meaningful compute, or downloads large data.
4. Slide gate: before generating the final presentation deck.

Each gate should offer 2-3 options plus a custom path when the UI supports it.

## Default Artifacts

Recommended artifacts in the target research repo:

- `.research-agent/goal_instruction.md`
- `.research-agent/goal_instruction.json`
- `.research-agent/goal_command.txt`
- `.research-agent/state.json`
- `.research-agent/decisions.jsonl`
- `research/motivation.md`
- `research/motivation.ko.md`
- `research/method.md`
- `research/experiments.md`
- `research/toy-experiment-report.md`
- `research/research-brief.html`
- `slides/slide-*.html`
- `slides/viewer.html`
- `slides/research-presentation.pdf`
- `slides/out-png/`

## Toy Experiment Requirements

The goal instruction should require:

- minimal dataset or synthetic data;
- clear hypothesis;
- baseline or control;
- implementation plan;
- metrics;
- expected runtime;
- reproducibility command;
- result table;
- failure analysis;
- limitations of the toy evidence.

## Final Output

Return:

1. a concise recommendation;
2. 2-3 candidate goal instructions in fenced blocks;
3. a short comparison table;
4. an ask-user-question style selection prompt when the tool is available;
5. a selected final goal instruction after the user chooses;
6. a `/goal` ready payload in a fenced block;
7. optional JSON object if useful;
8. suggested first command or prompt to run in the target repo.

## `/goal` Usage Contract

The selected output must be usable with Codex `/goal`.

After the user selects a candidate, provide:

```text
/goal <selected goal instruction>
```

Also write the selected instruction without the `/goal` prefix to `.research-agent/goal_instruction.md`, and write the full command form to `.research-agent/goal_command.txt` when files are being generated.

Keep the `/goal` payload concise enough to paste into the command, but specific enough to preserve:

- mission;
- workflow stages;
- decision gates;
- toy experiment scope;
- output artifacts;
- success criteria;
- stop conditions.
