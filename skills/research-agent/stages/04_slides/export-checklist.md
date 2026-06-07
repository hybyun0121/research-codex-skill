# Slides Export Checklist

Before marking Slides complete:

- `slides/slide-01.html` and following `slide-*.html` files exist.
- All assets are local under `slides/assets/`.
- No saved slide uses absolute filesystem paths.
- No saved slide depends on remote image/video URLs.
- `slides-grab validate --slides-dir slides` passes.
- `slides/viewer.html` is generated.
- `slides/research-presentation.pdf` is generated.
- `slides/out-png/` contains slide PNG previews.
- `research/research-brief.html` links to the slide viewer and PDF.
- Optional `slides/research-presentation.pptx` is generated only if requested and labeled experimental/unstable.

