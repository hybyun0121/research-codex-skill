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

- recommended: ask for domain or let agent propose candidate questions from a domain
- options: direct research question, domain-first discovery, venue/constraints first

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

