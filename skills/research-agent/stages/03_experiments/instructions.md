# Experiments

## Goal

Design experiments that verify validity, contribution, and novelty, then make the full
experiment plan reachable from the shared HTML brief without changing shared scripts.

## Workflow

1. Translate method claims into evaluation claims.
2. Ask only for decisions that change the plan: target domain/task, compute ceiling,
   allowed benchmark scale, required baseline family, or target venue level.
3. Select datasets, metrics, and baselines in two tiers:
   - toy benchmarks for fast iteration, debugging, and failure analysis
   - full benchmarks for credible paper-level claims
4. Prioritize main tables from recent competitive papers in trusted venues. Reuse
   relevant papers and tables from the Motivation landscape when they match the task,
   dataset, metric, or baseline family. Record the method name, paper, venue/year,
   table number when available, metric, paper link, and Hugging Face link when available.
5. For LLM evaluations, consider whether Hugging Face Open LLM Leaderboard collections
   are relevant: https://huggingface.co/open-llm-leaderboard/collections
6. Define ablations that isolate the novel component, including at least one direct
   removal, one replacement with a prior method, and one sensitivity check when feasible.
7. Define hyperparameter sweeps with names, values, defaults, budget, stopping rule,
   expected signal, and failure trigger.
8. Recommend compute for each tier: GPU model/class, GPU count, memory need,
   estimated runtime, parallelism strategy, and cheaper fallback.
9. Build a leaderboard schema for quantitative tracking and prior-result comparison.
   Include each method name, paper name, paper link, Hugging Face link when available,
   source table, variance/confidence, seeds, hardware, runtime/cost, status, artifact
   links, and failure notes.
10. Plan qualitative analysis that explains why the method works or fails.
11. List threats to validity and mitigation.

## HTML Link Contract

The shared renderer only displays `experiments.claims`, `experiments.plan`, and
`experiments.qualitative`. Do not edit shared scripts from this stage.

To avoid losing detailed experiment content:

1. Write the normal markdown artifact to `research/experiments.md`.
2. Also write a companion detail page to `research/experiments-detail.html` using
   `detail-html.template.html`.
3. Add a first row to `experiments.plan` with:
   - `claim`: `Full experiment design`
   - `dataset`: `All planned benchmarks`
   - `metric`: `See linked detail page`
   - `baseline`: `See linked detail page`
   - `evidence`: one-sentence summary of the benchmark, sweep, leaderboard, qualitative,
     and compute plan
   - `reference`: `experiments-detail.html`
4. Use `experiments-detail.html` as the `reference` for any plan row whose details exceed
   the brief table.

## Output

Write `research/experiments.md`, write `research/experiments-detail.html`, and update:

- `experiments.claims`
- `experiments.plan`
- `experiments.toy_benchmarks`
- `experiments.full_benchmarks`
- `experiments.baseline_sources`
- `experiments.prior_result_leaderboard`
- `experiments.ablations`
- `experiments.sweeps`
- `experiments.compute_plan`
- `experiments.leaderboard`
- `experiments.qualitative`
- `experiments.risks`
- `experiments.detail_html`
