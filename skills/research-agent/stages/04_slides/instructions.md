# Slides

## Goal

Create an English PPT deck suitable for presenting the stage 1-3 research result to a professor.

The deck should be generated from the accumulated Motivation, Method, and Experiments artifacts, then shown at the end of the HTML brief.

## Inputs

Use:

- `.research-agent/state.json`
- `research/motivation.md`
- `research/method.md`
- `research/experiments.md`
- bundled template: `skills/research-agent/templates/pptx/template_yonsei.pptx`

The first four inputs must come from the user's actual research repository and should reflect the completed or in-progress outputs of stages 1-3. The bundled template only provides presentation design.

## Requirements

- Use the bundled PPT template.
- Use Gothic A1 font.
- Keep slides in English.
- Use claim-evidence structure.
- Include tables and figures when they improve inspection.
- Do not invent finished results when stage 1-3 artifacts are incomplete; mark expected evidence or open risks clearly.
- Preserve the template's visual language, slide masters, layout, colors, and media.
- Build conference-quality slides: use visual argument structures such as claim cards, prior-work matrices, method diagrams, comparison panels, experiment tables, and ablation/risk panels. Do not render the deck as long prose or generic bullet lists.

## Default Outline

1. Title and research question
2. Motivation: why the problem matters
3. Existing landscape and limitations
4. Gap and novelty claim
5. Proposed method overview
6. Mathematical formulation
7. Algorithm or system flow
8. Experimental design
9. Expected or observed quantitative evidence
10. Qualitative analysis plan
11. Risks, limitations, and next steps

## Output

Write `slides/research-presentation.pptx`.

Use `scripts/generate_slides_polished.mjs` when Node dependencies are available. The script should derive slide content from stage 1-3 state and write an editable PPTX using the bundled template.

Also write SVG slide preview assets under `research/assets/slides/` so the HTML brief can display the deck without requiring LibreOffice or PPTX-to-image conversion tools. After generating the PPTX, render or refresh `research/research-brief.html` so the web brief displays the slide deck preview at the end.

Generate slides only when the user requests final presentation output or all earlier stages are complete.
