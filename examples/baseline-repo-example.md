# Baseline Repo Example

## Situation

The user runs `/research-agent` in an official baseline implementation repo.

## Expected Detection Evidence

- README describes training and evaluation.
- README contains a paper link or citation.
- Dependency files exist.
- Training or evaluation scripts exist.
- Config files or checkpoint references exist.

## Recommended First Action

Inspect the baseline method and find novelty gaps before asking the user to commit to a research question.

## Expected Initial Output

```text
Current repository inspection
Detected repository type:
- Official baseline implementation
Evidence:
- dependency file exists
- training/evaluation scripts detected
- README contains paper/citation signals
Current research-agent state:
- No previous run found
Recommended next action:
- Initialize a new research workflow for this baseline repo
```

## Recommended Question

Ask how to start:

1. User enters a research question directly.
2. Agent proposes candidate research questions from the baseline repo.
3. Agent finds novelty gaps from README, paper, and code.

Recommended option: novelty gap discovery from README, paper, and code.

