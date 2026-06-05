# HTML Brief

## Goal

Render the final readable web brief from stage 1-3 research state and markdown artifacts.

The HTML brief is the user-facing review surface: it should let a reader understand the current research question, why it matters, what method is proposed, how it will be evaluated, and how the final slide deck looks.

Design the brief as a polished research review page, not a raw markdown dump. Use a clear hero, claim cards, readable matrices, experiment tables, risk panels, and a slide gallery.

## Inputs

Read accumulated outputs from:

- `.research-agent/state.json`
- `research/motivation.md`
- `research/method.md`
- `research/experiments.md`
- `slides/research-presentation.pptx`, when generated

These inputs are the outputs produced by stages 1-3 in the user's actual research repository. Do not use sample data, temporary run directories, or files from this skill repository as research content.

## Structure

1. Research question and thesis
2. Repository understanding, if relevant
3. Motivation: landscape, gaps, selected direction
4. Method: claim, formulation, algorithm, visual plan
5. Experiments: benchmarks, sweeps, leaderboard, qualitative plan
6. Open questions and risks
7. Links and references
8. Slides preview as the final section, when `slides/research-presentation.pptx` exists

## Synthesis Rules

- Treat stage 1-3 outputs as the source of truth.
- Prefer concrete claims, tables, and linked evidence over generic prose.
- Keep incomplete sections explicit instead of filling gaps with invented results.
- Preserve links near the claims they support.
- Use the HTML brief as the final container for slide preview and downloadable deck links.
- Show generated SVG slide previews directly when available; do not require LibreOffice for the default web view.

## Output

Write `research/research-brief.html`.

Use `scripts/render_html.py` when available. Keep links near the claims they support. Mark incomplete sections clearly instead of pretending they are final.

When a final PPTX exists, render it at the end of the HTML brief. Prefer slide image thumbnails generated from the deck; use generated SVG slide previews when deck conversion tools are unavailable; fall back to an embedded PDF or PPTX download link when needed.
