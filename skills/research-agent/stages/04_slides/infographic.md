# Infographic Support

## Does Slides-Grab Support Infographics?

Yes, but not as a single dedicated `infographic` command.

`slides-grab` supports infographic-style work through:

- HTML/CSS slide authoring;
- bundled design styles;
- `chart`/content-oriented slide templates;
- local SVG assets;
- `slides-grab tldraw` for diagram assets;
- `slides-grab image` for bespoke generated imagery;
- `slides-grab png` for high-resolution infographic/card exports;
- `card-news` square mode for Instagram-style cards.

## Recommended Research Infographic Types

Use these in professor-facing research slides:

- prior-work landscape matrix;
- novelty gap map;
- method pipeline;
- algorithm flow;
- dataset/metric evaluation grid;
- ablation/risk panel;
- experiment timeline;
- contribution triangle.

## How To Build Them

Prefer one of these approaches:

1. **Pure HTML/CSS infographic**
   - Build structured cards, matrices, timelines, or flow diagrams directly in `slide-XX.html`.
   - Best for editable research diagrams.

2. **Local SVG infographic**
   - Generate or hand-author SVG under `slides/assets/`.
   - Reference with `<img src="./assets/name.svg">`.

3. **Tldraw diagram asset**
   - Use `slides-grab tldraw` to export a `.tldr` diagram into slide-sized SVG.

4. **Generated image**
   - Use `slides-grab image` for editorial or conceptual imagery.
   - Avoid using generated images as the only evidence for scientific claims.

## Validation

Every infographic slide must pass:

```bash
slides-grab validate --slides-dir slides
```

The infographic should also export cleanly through:

```bash
slides-grab png --slides-dir slides --output-dir slides/out-png --resolution 2160p
```

