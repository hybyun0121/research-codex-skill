# Research Automation Goal Instruction

## Mission

You are running an automated research workflow in the current repository. Your goal is to move from topic selection to Method, toy Experiments, and final slide/report artifacts while preserving evidence, decisions, and user checkpoints.

## Repo Inspection

Start by inspecting the current repository. Classify it as:

- empty research repo;
- existing user project;
- official baseline implementation;
- partial research-agent project.

Never read or expose credential files such as `.env`, private keys, tokens, certificates, or files whose names contain `secret`, `credential`, `password`, or `token`.

## Workflow

1. Use `$research-agent` if available.
2. Run Motivation:
   - identify or propose research topics;
   - build literature landscape;
   - record MCP/tool usage and source provenance;
   - write English and Korean Motivation reports.
3. Run Method:
   - convert the selected direction into a method claim;
   - define assumptions, variables, objective, pseudocode, and expected mechanism;
   - check mathematical and conceptual rigor.
4. Run Experiments:
   - design validation experiments;
   - define toy experiment;
   - use a small or synthetic setup unless the user approves larger compute;
   - run the toy experiment when safe;
   - write result table and failure analysis.
5. Create final artifacts:
   - update `research/research-brief.html`;
   - create a professor-facing English `slides-grab` slide report when prior stages are complete or when the user approves.

## Decision Gates

Pause and ask the user before:

- selecting the final research direction;
- committing to a method design;
- running non-trivial compute or modifying baseline code;
- generating the final slide deck.

When asking, provide a recommended option first, 2-3 alternatives, and a custom path.

## Default Outputs

- `.research-agent/goal_instruction.md`
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

## Success Criteria

- A research direction is selected with evidence-backed novelty.
- A Method is specified enough to implement or prototype.
- A toy experiment is run or fully specified with clear limitations.
- Results are summarized honestly.
- Final report and slides are generated from recorded evidence.

## Stop Conditions

Stop and ask the user if:

- required data, paper access, or code is unavailable;
- the proposed method is not feasible under the stated budget;
- toy results contradict the core Motivation claim;
- a safety or credential boundary is encountered;
- the next step would require large compute, external spending, or destructive code changes.

## `/goal` Command Form

Paste the selected instruction after Codex `/goal`:

```text
/goal ${selected_goal_instruction}
```
