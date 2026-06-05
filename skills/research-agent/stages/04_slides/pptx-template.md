# PPTX Template

Use the bundled professor-facing PPT template:

`skills/research-agent/templates/pptx/template_yonsei.pptx`

This template is part of the distributed skill and should be used as the default design source for generated decks.

The slide deck should:

- be written in English;
- use Gothic A1;
- follow the provided template's layout and visual language;
- present claims with evidence;
- include tables or figures when they make the research argument easier to inspect.

## Generation Contract

- Generate `slides/research-presentation.pptx` in the user's research repo.
- Preserve the bundled template's slide masters, theme, media, and visual hierarchy.
- Fill content from `.research-agent/state.json` and `research/motivation.md`, `research/method.md`, and `research/experiments.md`.
- Use Gothic A1 for generated text runs. If the runtime cannot verify font installation, still set the PPTX font face to Gothic A1.
- Keep generated slide text concise enough for presentation; detailed evidence belongs in `research/research-brief.html`.
- Write web preview assets under `research/assets/slides/` so the HTML brief can show the deck even when local PPTX-to-image conversion tools are unavailable.
