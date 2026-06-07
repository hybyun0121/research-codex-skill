# Slides-Grab Asset Contract

## Required Asset Rules

- Put slide assets under `slides/assets/`.
- Reference assets from each `slide-XX.html` with relative paths:
  - `./assets/example.png`
  - `./assets/system.svg`
  - `./assets/demo.mp4`
- Do not use absolute filesystem paths such as `/Users/...`.
- Do not use remote `http(s)://` images in saved slides.
- Download remote videos into `slides/assets/` before referencing them.
- `data:` URLs are allowed only when fully self-contained slides are more important than easy asset reuse.

## Generated Images

When a bespoke image is needed, prefer:

```bash
slides-grab image --slides-dir slides --prompt "..."
```

If image generation is unavailable, use web search or user-provided assets, download/copy them into `slides/assets/`, and reference them by relative path.

## Diagrams And Infographics

Use local SVG or HTML/CSS diagrams whenever possible. For tldraw diagrams:

```bash
slides-grab tldraw \
  --input slides/assets/system.tldr \
  --output slides/assets/system.svg \
  --width 640 \
  --height 320 \
  --padding 16
```

Then reference:

```html
<img src="./assets/system.svg" alt="System architecture diagram">
```

