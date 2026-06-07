# Slides

## Goal

Create an English professor-facing slide report using `slides-grab`.

The deck must be HTML-first: generate `slides/slide-*.html` files as the source of truth, then export PDF/PNG and optional experimental PPTX from those files.

## Inputs

Use accumulated outputs from the user's research repository:

- `.research-agent/state.json`
- `research/motivation.md`
- `research/motivation.ko.md`
- `research/method.md`
- `research/experiments.md`
- `research/research-brief.html`

Read:

- `slides-grab-workflow.md`
- `asset-contract.md`
- `infographic.md`
- `export-checklist.md`

## Requirements

- Use `slides-grab` as the slide generation, validation, editing, and export workflow.
- Keep slide content in English.
- Use Gothic A1 where practical in HTML/CSS.
- Use claim-evidence structure.
- Include infographic-style visual structures when they improve inspection.
- Do not invent finished results when stage 1-3 artifacts are incomplete; mark expected evidence or open risks clearly.
- Build conference-quality slides with visual argument structures: claim cards, prior-work matrices, novelty gap maps, method diagrams, comparison panels, experiment tables, ablation/risk panels, and contribution summaries.
- Do not render the deck as long prose or generic bullet lists.

## Default Outline

1. Title and research question
2. One-sentence thesis
3. Motivation: why the problem matters
4. Prior-work landscape infographic
5. Gap and novelty claim
6. Proposed method overview
7. Mathematical formulation or algorithm flow
8. Experimental design
9. Expected or observed quantitative evidence
10. Qualitative analysis and failure modes
11. Risks, limitations, and next steps

## Output

Primary outputs:

- `slides/slide-01.html`
- `slides/slide-02.html`
- additional `slides/slide-*.html`
- `slides/assets/`
- `slides/viewer.html`
- `slides/research-presentation.pdf`
- `slides/out-png/`

Optional outputs:

- `slides/research-presentation-searchable.pdf`
- `slides/research-presentation.pptx` using `slides-grab convert`, labeled experimental/unstable
- `slides/research-presentation-figma.pptx` using `slides-grab figma`, labeled experimental/unstable

After generating slides, run validation/export commands and refresh `research/research-brief.html` so it displays PNG previews and links to the `slides-grab` viewer/PDF.

Generate slides only when the user requests final presentation output or all earlier stages are complete.
