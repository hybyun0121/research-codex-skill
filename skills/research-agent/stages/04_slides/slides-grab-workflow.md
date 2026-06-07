# Slides-Grab Workflow

## Goal

Generate the final slide report with `slides-grab` as an HTML-first workflow.

The slide source of truth is a `slides-grab` deck directory containing `slide-*.html` files and local assets. PDF, PNG, PPTX, and Figma outputs are exports derived from those HTML slides.

## Installation Check

Before generating or exporting slides, verify `slides-grab` is available:

```bash
slides-grab --help
```

If missing, recommend:

```bash
npm install slides-grab
npx playwright install chromium
npx skills add ./node_modules/slides-grab -g -a codex --yes --copy
```

Restart Codex after installing shared skills.

## Deck Workspace

Use one deck workspace per research project:

```text
slides/
├── slide-01.html
├── slide-02.html
├── ...
├── assets/
├── viewer.html
├── out-png/
├── research-presentation.pdf
├── research-presentation-searchable.pdf
└── research-presentation.pptx
```

## Required Workflow

1. Plan a slide outline from `.research-agent/state.json`, `research/motivation.md`, `research/method.md`, and `research/experiments.md`.
2. Generate each slide as a self-contained `slide-XX.html` file.
3. Store every local image, SVG, video, and generated infographic asset under `slides/assets/`.
4. Use relative asset references such as `./assets/figure-01.svg`.
5. Build `slides/viewer.html`.
6. Run validation.
7. Export PDF and PNG previews.
8. Export PPTX only when requested, and mark it experimental/unstable.
9. Refresh `research/research-brief.html` so it links to the viewer, PDF, PNG previews, and optional PPTX.

## Commands

```bash
slides-grab build-viewer --slides-dir slides
slides-grab validate --slides-dir slides
slides-grab pdf --slides-dir slides --output slides/research-presentation.pdf
slides-grab pdf --slides-dir slides --mode print --output slides/research-presentation-searchable.pdf
slides-grab png --slides-dir slides --output-dir slides/out-png --resolution 2160p
slides-grab convert --slides-dir slides --output slides/research-presentation.pptx
```

Use `slides-grab edit --slides-dir slides` when the user wants visual editing and bbox-based agent feedback.

## Export Policy

- PDF is the default final distribution format.
- PNG previews are used in `research/research-brief.html`.
- PPTX export is optional and experimental/unstable.
- Figma export is optional and experimental/unstable.

