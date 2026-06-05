# Experiments

## Goal

Design experiments that verify validity, contribution, and novelty.

## Workflow

1. Translate method claims into evaluation claims.
2. Select datasets, metrics, and baselines.
3. Prioritize main tables from recent competitive papers in trusted venues.
4. For LLM evaluations, consider whether Hugging Face Open LLM Leaderboard collections are relevant: https://huggingface.co/open-llm-leaderboard/collections
5. Define ablations that isolate the novel component.
6. Define hyperparameter sweeps with names, values, defaults, budget, and stopping rule.
7. Build a leaderboard schema for quantitative tracking.
8. Plan qualitative analysis that explains why the method works or fails.
9. List threats to validity and mitigation.

## Output

Write `research/experiments.md` and update:

- `experiments.claims`
- `experiments.plan`
- `experiments.sweeps`
- `experiments.leaderboard`
- `experiments.qualitative`
- `experiments.risks`

