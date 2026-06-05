# Experiments

## Detail HTML

The full experiment design is available in `research/experiments-detail.html`.
The shared HTML brief should link to it through `experiments.plan[].reference =
"experiments-detail.html"`.

## Summary Dashboard

| Item | Value |
| --- | --- |
| Baseline/reference rows | ${baseline_count} |
| Toy benchmarks | ${toy_count} |
| Full benchmarks | ${full_count} |
| Estimated toy GPU-hours | ${toy_gpu_hours} |
| Estimated full GPU-hours | ${full_gpu_hours} |
| Recommended next action | ${next_action} |
| Toy execution status | ${toy_status} |

## Evaluation Claims

- ${claim}

## Baseline Sources

| Method | Paper | Venue/Year | Main Table | Task | Metric | Why Competitive | Paper Link | Hugging Face | GitHub Repo | Code Reuse |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Benchmark Plan

| Claim | Tier | Dataset | Metric | Baseline | Expected Evidence | Reference |
| --- | --- | --- | --- | --- | --- | --- |

## Toy Benchmarks

| Dataset | Purpose | Subset/Scale | Metric | Setup | Run Command | Expected Runtime | Success Criterion |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Full Benchmarks

| Dataset | Purpose | Scale | Metric | Baselines | Required Evidence |
| --- | --- | --- | --- | --- | --- |

## Ablations

| Ablation | Claim Isolated | Control Variant | Expected Signal | Failure Interpretation |
| --- | --- | --- | --- | --- |

## Hyperparameter Sweeps

| Parameter | Values | Default | Budget | Stopping Rule | Expected Signal | Failure Trigger |
| --- | --- | --- | --- | --- | --- | --- |

## GPU Inventory

| GPU Model | Count | Memory Per GPU | Best Use | Constraints |
| --- | --- | --- | --- | --- |
| RTX 4090 | 4 | 24GB | toy runs, small models, parallel sweeps | limited memory for large models or long contexts |
| RTX A6000 | 1 | 48GB | medium models, stable single-GPU baselines | lower count than 4090 pool |
| RTX PRO 6000 Blackwell Server Edition | 3 | 96GB | large models, long context, full benchmarks | reserve for runs that need memory headroom |

## Compute Plan

| Experiment | Tier | GPU Recommendation | GPU Count | Required Memory | Memory Margin | Estimated Runtime | GPU-Hours | Parallelism | Fallback | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Budget Summary

| Scope | Runs | Recommended GPU Pool | Total GPU-Hours | Wall-Clock Estimate | Budget Risk | Notes |
| --- | --- | --- | --- | --- | --- | --- |

## Toy Execution Gate

After this plan is shown, ask the user whether to run toy experiments.

Recommended option: run toy environment setup and smoke test only.

Do not start GPU-consuming runs until the user explicitly allows toy execution.

## Reference Code Reuse Plan

| Source Paper | GitHub Repo | License/Use Check | Local Path | Files To Adapt | Setup Command | Toy Run Command | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Toy Environment And Run Plan

| Step | Command/Action | Expected Output | Status | Notes |
| --- | --- | --- | --- | --- |

## Leaderboard

| Experiment ID | Method Name | Method Variant | Paper | Paper Link | Hugging Face | Dataset | Seed | Metrics | Hardware | Runtime/Cost | Status | Artifact | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Prior Results From Motivation

| Method | Paper | Source Table | Dataset | Metric | Reported Result | Paper Link | Hugging Face | Use In This Plan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Bilingual HTML Notes

- `research/experiments-detail.html` should include Korean and English text for all
  section titles and short descriptions.
- Use a language toggle that switches visible text without needing a server.
- Tables may keep method names, paper titles, metrics, and commands in English.

## Qualitative Analysis

- ${qualitative_plan}

## Reproducibility

- Code/config snapshot:
- Data split:
- Seeds:
- Logging artifacts:
- Statistical reporting:

## Risks

- ${risk}
