# Existing Project Import

## Purpose

Use this mode when the current repository is an official baseline clone or a user-modified baseline project where experiments may already have been run. The goal is to reconstruct the completed work into the research-agent workflow without rewriting user code.

This mode is retrospective: it organizes existing evidence into Motivation, Method, Experiments, HTML brief, and slides-ready artifacts.

## When To Run

Run this mode before Motivation when repo inspection suggests:

- an official baseline repository was cloned;
- baseline paper, citation, training, evaluation, or benchmark signals exist;
- user modifications, new branches, result folders, logs, sweeps, notebooks, or generated tables exist;
- no `.research-agent/state.json` exists yet.

Do not run this mode for an empty repo. Do not run it when the user wants to start a new research idea from scratch.

## Safe Inspection Scope

Allowed:

- `README`, paper links, citation metadata, license, dependency files;
- train/eval scripts, configs, benchmark entry points;
- small result files such as `.csv`, `.json`, `.jsonl`, `.tsv`, `.md`, `.txt`, and `.log` when clearly experiment summaries;
- git metadata from `git status`, `git branch`, and recent commit messages;
- directory names under likely result folders.

Avoid:

- credential files;
- private keys, tokens, `.env`, certificates;
- checkpoints, model weights, datasets, raw generated samples, and large binary files;
- destructive git operations;
- editing baseline implementation files.

## Import Questions

Ask only for decisions that cannot be inferred safely. Use an ask-user-question style tool when available.

High-value questions:

- Which result folder is authoritative for the final comparison?
- Which implementation files represent the proposed Method?
- Which baseline setting should be treated as the main baseline?
- What is the intended research question or paper claim?
- Should the import preserve raw experiment names, or normalize them into paper-style labels?

## Output Artifacts

Create or update:

- `.research-agent/project_import.json`
- `research/project-import.md`
- `research/status.md`
- `research/motivation.md`
- `research/motivation.ko.md` when Motivation is reconstructed
- `research/method.md`
- `research/experiments.md`
- `.research-agent/state.json`

After these artifacts are coherent, render `research/research-brief.html`. Generate `slides/` only when the user asks for final presentation output or all imported stage artifacts are ready.

## Import Summary Structure

The import summary must include:

1. Baseline identity
2. Official paper or repository evidence
3. User modification evidence
4. Method implementation map
5. Experiment artifact map
6. Baseline-vs-proposed result candidates
7. Missing confirmations
8. Proposed stage reconstruction plan

## Stage Reconstruction

Map evidence into stages conservatively:

- Motivation: use paper links, baseline limitations, related work notes, and user-stated research question. If novelty cannot be justified from local evidence, mark Motivation as `stale` or `blocked`.
- Method: use modified source files, configs, notebooks, and user explanation. If the mathematical definition is missing, mark Method as `in_progress`.
- Experiments: use result files, benchmark scripts, logs, and sweep configs. If metrics are ambiguous, mark Experiments as `blocked` by user confirmation.
- HTML brief: render only after Motivation, Method, and Experiments have enough coherent content.
- Slides: use the `slides-grab` workflow after the HTML brief is coherent.

## User-Facing Language

Talk with the user in Korean/English mixed style:

- keep technical terms such as `baseline`, `Method`, `Experiments`, `leaderboard`, `ablation`, `sweep`, `artifact`, and `claim` in English;
- use Korean for ordinary explanation and decision prompts.
