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
5. Build a baseline set before proposing new runs:
   - minimum 8 baseline or reference rows for a full plan when enough literature exists
   - at least 3 rows imported or adapted from Motivation landscape tables when relevant
   - include recent SOTA, strong classical/simple baselines, ablations of the proposed
     method, and published table results that can anchor the leaderboard
   - mark any unverified result as `needs_source_check` instead of inventing numbers
6. For LLM evaluations, consider whether Hugging Face Open LLM Leaderboard collections
   are relevant: https://huggingface.co/open-llm-leaderboard/collections
7. Define ablations that isolate the novel component, including at least one direct
   removal, one replacement with a prior method, and one sensitivity check when feasible.
8. Define hyperparameter sweeps with names, values, defaults, budget, stopping rule,
   expected signal, and failure trigger.
9. Use the available GPU inventory when the user provides it. For each experiment,
   estimate model/data memory, activation/KV/cache overhead, batch size, expected
   runtime, GPU-hours, and whether the run fits on each GPU class. Prefer the smallest
   GPU that safely fits the run, reserve 96GB GPUs for large models, long-context
   inference, multi-sample verification, or parallel full benchmarks, and show a cheaper
   fallback.
10. If no inventory is supplied, ask for it or state conservative assumptions. When this
   inventory is available, use it by default:
   - 4x RTX 4090 24GB
   - 1x RTX A6000 48GB
   - 3x RTX PRO 6000 Blackwell Server Edition 96GB
11. Build a leaderboard schema for quantitative tracking and prior-result comparison.
   Include each method name, paper name, paper link, Hugging Face link when available,
   source table, variance/confidence, seeds, hardware, runtime/cost, status, artifact
   links, and failure notes.
12. Plan qualitative analysis that explains why the method works or fails.
13. List threats to validity and mitigation.
14. After presenting the experiment plan, ask the user whether to run toy experiments.
    Use an ask-user-question style tool when available. Recommended option: run toy
    setup and smoke test only. Do not start GPU-consuming runs until the user allows it.
15. Before toy execution, inspect reference papers for available code. If a relevant
    GitHub repository exists, prefer using it as the starting point over rewriting the
    experiment from scratch:
    - clone or vendor it into a clearly named external/reference-code area in the user's
      research repo
    - inspect license, README, requirements, entrypoints, configs, datasets, and scripts
    - adapt the smallest possible wrapper/config for the toy benchmark
    - keep modifications isolated and record changed files, commands, and rationale
    - do not read or copy secrets, checkpoints, private data, or credential files
16. If the user allows toy execution, create or update only minimal experiment-run files
    in the user's research repo, set up the toy environment, run the toy benchmark, save
    logs/results, append rows to the leaderboard, and summarize outcome, failures, and
    next recommended full run.

## Detail HTML Requirements

`research/experiments-detail.html` is the full user-facing experiment result. It must be
readable enough to inspect without opening markdown or JSON.

Include:

- Korean/English language toggle using static HTML, CSS, and JavaScript.
- A compact summary dashboard: claims, baseline count, toy/full benchmarks, estimated
  GPU-hours, recommended next action, and toy-run status.
- Baseline tables with method name, paper name, venue/year, source table, reported
  metric/result, paper link, and Hugging Face link when available.
- GPU inventory and per-experiment compute recommendation tables.
- Toy setup commands, toy run command, expected outputs, and result summary area.
- Reference code reuse plan: GitHub repo, license/check status, files to adapt, patch
  summary, setup command, run command, and fallback if the repo cannot be used.
- Leaderboard rows that combine published results, toy results, and planned full runs.
- Warnings for unverified paper values, missing Hugging Face links, or budget risks.

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
- `experiments.gpu_inventory`
- `experiments.compute_plan`
- `experiments.budget_summary`
- `experiments.reference_code_reuse`
- `experiments.toy_execution`
- `experiments.leaderboard`
- `experiments.qualitative`
- `experiments.risks`
- `experiments.detail_html`
