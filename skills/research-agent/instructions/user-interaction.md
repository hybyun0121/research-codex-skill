# User Interaction

## Principle

Ask only when the answer changes the next action. Otherwise make a conservative assumption and record it in `.research-agent/state.json`.

## Question Format

When an ask-user-question style tool is available, use it with:

- short reason
- recommended option first
- 2-3 mutually exclusive choices
- custom answer enabled by the client

If the tool is unavailable, use the same structure in plain text.

## Common First Questions

For an empty repo:

- recommended: ask whether to run a `goal instruction discussion` before Motivation
- reason: an empty repo has no baseline, no prior state, and no research question, so a goal instruction can define automation scope before the agent starts topic discovery
- first options: goal instruction discussion, direct research question, domain-first discovery

If the user chooses goal instruction discussion:

- discuss only details that affect automation behavior;
- recommend 2-3 candidate `goal instruction` options at the end;
- ask the user to select, merge, or customize one;
- record the final choice in `.research-agent/decisions.jsonl`;
- save selected outputs to `.research-agent/goal_instruction.md` and optionally `.research-agent/goal_instruction.json`.

For a baseline repo:

- recommended: inspect baseline method and find novelty gaps
- options: direct research question, candidate questions from repo, novelty gap discovery from README/paper/code

For an existing user project:

- recommended: summarize current artifacts and ask whether to resume or reframe
- options: resume existing direction, audit project for gaps, start a new research question

## Decision Logging

Append material decisions to `.research-agent/decisions.jsonl` with:

- timestamp
- stage
- question
- selected_option
- rationale
