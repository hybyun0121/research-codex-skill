#!/usr/bin/env python3
"""Render `.research-agent/state.json` into `research/research-brief.html`."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from string import Template
from typing import Optional


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value))


def list_items(items: object) -> str:
    if not isinstance(items, list) or not items:
        return '<p class="muted">Not specified yet.</p>'
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def link(url: object, label: str = "source") -> str:
    if not url:
        return ""
    safe = esc(url)
    return f'<a href="{safe}">{esc(label)}</a>'


@dataclass
class SlideAssets:
    deck_dir: Optional[Path] = None
    viewer: Optional[Path] = None
    pptx: Optional[Path] = None
    pdf: Optional[Path] = None
    images: list[Path] = field(default_factory=list)
    slide_html: list[Path] = field(default_factory=list)
    note: Optional[str] = None


def slide_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"(\d+)(?=\.(?:png|svg)$)", path.name)
    return (int(match.group(1)) if match else 0, path.name)


def existing_slide_images(preview_dir: Path) -> list[Path]:
    return sorted(
        [*preview_dir.glob("slide-*.png"), *preview_dir.glob("slide-*.svg")],
        key=slide_sort_key,
    )


def existing_slide_html(deck_dir: Path) -> list[Path]:
    return sorted(deck_dir.glob("slide-*.html"), key=lambda p: slide_sort_key(p.with_suffix(".png")))


def infer_repo_root(state_path: Path) -> Path:
    resolved = state_path.resolve()
    if resolved.parent.name == ".research-agent":
        return resolved.parent.parent
    return Path.cwd().resolve()


def artifact_path(repo_root: Path, state: dict[str, object], key: str, default: str) -> Path:
    artifacts = state.get("artifacts") if isinstance(state.get("artifacts"), dict) else {}
    raw = artifacts.get(key) if isinstance(artifacts, dict) else None
    value = raw if isinstance(raw, str) and raw else default
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def relative_href(output_path: Path, target_path: Path) -> str:
    return Path(os.path.relpath(target_path.resolve(), output_path.resolve().parent)).as_posix()


def prepare_slide_assets(
    state: dict[str, object],
    repo_root: Path,
    output_path: Path,
    generate_previews: bool,
) -> SlideAssets:
    deck_dir = artifact_path(repo_root, state, "slide_deck_dir", "slides")
    if not deck_dir.exists():
        return SlideAssets(note="Final slides-grab deck has not been generated yet.")

    assets = SlideAssets(deck_dir=deck_dir)
    assets.viewer = artifact_path(repo_root, state, "slide_viewer", "slides/viewer.html")
    assets.pdf = artifact_path(repo_root, state, "slide_pdf", "slides/research-presentation.pdf")
    assets.pptx = artifact_path(repo_root, state, "slides", "slides/research-presentation.pptx")
    assets.slide_html = existing_slide_html(deck_dir)

    if not assets.viewer.exists():
        assets.viewer = None
    if not assets.pdf.exists():
        assets.pdf = None
    if not assets.pptx.exists():
        assets.pptx = None

    if not generate_previews:
        assets.note = "Slide preview discovery was disabled."
        return assets

    preview_dir = artifact_path(repo_root, state, "slide_png_dir", "slides/out-png")
    assets.images = existing_slide_images(preview_dir)
    if not assets.images:
        assets.images = existing_slide_images(output_path.parent / "assets" / "slides")
    if not assets.images:
        assets.note = "Run `slides-grab png --slides-dir slides --output-dir slides/out-png` to generate slide previews."
    return assets


def landscape_table(rows: object) -> str:
    if not isinstance(rows, list) or not rows:
        return '<p class="muted">No landscape entries yet.</p>'
    body = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        body.append(
            "<tr>"
            f"<td>{esc(row.get('title'))}<br>{link(row.get('url'))}</td>"
            f"<td>{esc(row.get('venue') or row.get('venue_year'))}</td>"
            f"<td>{esc(row.get('task'))}</td>"
            f"<td>{esc(row.get('main_contribution') or row.get('contribution'))}</td>"
            f"<td>{esc(row.get('limitation'))}</td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>Paper</th><th>Venue/Year</th><th>Task</th>"
        "<th>Contribution</th><th>Limitation</th></tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table>"
    )


def experiment_table(rows: object) -> str:
    if not isinstance(rows, list) or not rows:
        return '<p class="muted">No experiment plan yet.</p>'
    body = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        body.append(
            "<tr>"
            f"<td>{esc(row.get('claim'))}</td>"
            f"<td>{esc(row.get('dataset'))}</td>"
            f"<td>{esc(row.get('metric'))}</td>"
            f"<td>{esc(row.get('baseline'))}</td>"
            f"<td>{esc(row.get('evidence'))}<br>{link(row.get('reference'), 'reference')}</td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>Claim</th><th>Dataset</th><th>Metric</th>"
        "<th>Baseline</th><th>Evidence</th></tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table>"
    )


def compact_text(value: object, fallback: str = "Not specified yet.") -> str:
    text = "" if value is None else str(value)
    text = " ".join(text.split())
    return text or fallback


def card_grid(items: object, empty: str) -> str:
    if not isinstance(items, list) or not items:
        return f'<p class="muted">{esc(empty)}</p>'
    cards = []
    for index, item in enumerate(items[:3], start=1):
        cards.append(
            '<article class="info-card">'
            f'<span class="card-index">{index:02d}</span>'
            f'<p>{esc(compact_text(item))}</p>'
            '</article>'
        )
    return '<div class="card-grid">' + "".join(cards) + '</div>'


def claim_panel(label: str, value: object) -> str:
    return (
        '<article class="claim-panel">'
        f'<span>{esc(label)}</span>'
        f'<p>{esc(compact_text(value))}</p>'
        '</article>'
    )


def open_questions_html(items: object) -> str:
    if not isinstance(items, list) or not items:
        return '<p class="muted">No open questions recorded.</p>'
    values = [item.get("question", item) if isinstance(item, dict) else item for item in items]
    return card_grid(values, "No open questions recorded.")


def render_project_import_section(
    state: dict[str, object],
    repo_root: Path,
    output_path: Path,
) -> str:
    project = state.get("project") if isinstance(state.get("project"), dict) else {}
    import_recommended = bool(project.get("import_recommended"))
    signals = project.get("import_signals")
    import_md = artifact_path(repo_root, state, "project_import_md", "research/project-import.md")
    import_json = artifact_path(repo_root, state, "project_import_json", ".research-agent/project_import.json")

    if not import_recommended and not import_md.exists() and not import_json.exists():
        return ""

    links = []
    if import_md.exists():
        links.append(
            f'<a class="button-link" href="{esc(relative_href(output_path, import_md))}">Open Import Summary</a>'
        )
    if import_json.exists():
        links.append(
            f'<a class="button-link" href="{esc(relative_href(output_path, import_json))}">Open Import JSON</a>'
        )
    link_html = f'<div class="slide-links">{"".join(links)}</div>' if links else ""

    return f"""
<section id="project-import">
  <div class="section-head">
    <p class="eyebrow">Import</p>
    <h2>Existing Project Import</h2>
    <p>Baseline repository evidence, user Method changes, and experiment artifacts collected before reconstructing the research stages.</p>
  </div>
  {link_html}
  <h3>Import Signals</h3>
  {card_grid(signals, 'No import signals recorded yet.')}
</section>
"""


def render_slides_section(assets: SlideAssets, output_path: Path) -> str:
    if not assets.deck_dir:
        return f"""
<section id="slides">
  <h2>Slides</h2>
  <p class="muted">{esc(assets.note or 'Final slides-grab deck has not been generated yet.')}</p>
</section>
"""

    links = []
    if assets.viewer:
        links.append(
            f'<a class="button-link" href="{esc(relative_href(output_path, assets.viewer))}">Open Slides Viewer</a>'
        )
    if assets.pdf:
        links.append(
            f'<a class="button-link" href="{esc(relative_href(output_path, assets.pdf))}">Open PDF</a>'
        )
    if assets.pptx:
        links.append(
            f'<a class="button-link" href="{esc(relative_href(output_path, assets.pptx))}">Download Experimental PPTX</a>'
        )
    if not links:
        links.append(
            f'<a class="button-link" href="{esc(relative_href(output_path, assets.deck_dir))}">Open Slides Directory</a>'
        )

    if assets.images:
        figures = []
        for index, image in enumerate(assets.images, start=1):
            image_href = esc(relative_href(output_path, image))
            figures.append(
                '<figure class="slide-card">'
                f'<a href="{image_href}"><img src="{image_href}" alt="Slide {index} preview" loading="lazy"></a>'
                f"<figcaption>Slide {index}</figcaption>"
                "</figure>"
            )
        preview = '<div class="slide-grid">' + "".join(figures) + "</div>"
    elif assets.pdf:
        pdf_href = esc(relative_href(output_path, assets.pdf))
        preview = (
            f'<object class="slide-pdf" data="{pdf_href}" type="application/pdf">'
            f'<p class="muted">PDF preview is unavailable in this browser. <a href="{pdf_href}">Open PDF</a>.</p>'
            "</object>"
        )
    elif assets.slide_html:
        items = []
        for index, slide in enumerate(assets.slide_html, start=1):
            slide_href = esc(relative_href(output_path, slide))
            items.append(
                '<figure class="slide-card">'
                f'<a href="{slide_href}"><div class="slide-html-thumb">HTML</div></a>'
                f"<figcaption>Slide {index}</figcaption>"
                "</figure>"
            )
        preview = '<div class="slide-grid">' + "".join(items) + "</div>"
    else:
        preview = '<p class="muted">Slide preview is unavailable. Use slides-grab validate/png/pdf to complete exports.</p>'

    note = f'<p class="muted">{esc(assets.note)}</p>' if assets.note else ""
    return f"""
<section id="slides">
  <h2>Slides</h2>
  <div class="slide-links">{"".join(links)}</div>
  {note}
  {preview}
</section>
"""


def render_body(state: dict[str, object], slide_assets: SlideAssets, repo_root: Path, output_path: Path) -> str:
    project = state.get("project") if isinstance(state.get("project"), dict) else {}
    research = state.get("research") if isinstance(state.get("research"), dict) else {}
    motivation = state.get("motivation") if isinstance(state.get("motivation"), dict) else {}
    method = state.get("method") if isinstance(state.get("method"), dict) else {}
    experiments = state.get("experiments") if isinstance(state.get("experiments"), dict) else {}
    workflow = state.get("workflow") if isinstance(state.get("workflow"), dict) else {}
    project_import_section = render_project_import_section(state, repo_root, output_path)
    project_import_nav = '<a href="#project-import">Import</a>' if project_import_section else ""

    return f"""
<nav class="topbar">
  <a href="#brief">Brief</a>
  {project_import_nav}
  <a href="#motivation">Motivation</a>
  <a href="#method">Method</a>
  <a href="#experiments">Experiments</a>
  <a href="#slides">Slides</a>
</nav>
<header id="brief" class="hero">
  <p class="eyebrow">Research Agent Brief</p>
  <h1>{esc(research.get('question') or 'Untitled Research Question')}</h1>
  <p class="lede">{esc(research.get('domain') or '')}</p>
  <div class="hero-grid">
    {claim_panel('Selected Direction', research.get('selected_direction') or 'Not selected yet.')}
    {claim_panel('Method Claim', method.get('claim') or 'Not specified yet.')}
    {claim_panel('Current Stage', workflow.get('current_stage') or 'unknown')}
  </div>
</header>
{project_import_section}
<section id="motivation">
  <div class="section-head">
    <p class="eyebrow">Stage 1</p>
    <h2>Motivation</h2>
    <p>Why the problem is worth a paper, where prior work stops, and what opening the project claims.</p>
  </div>
  <h3>Paper Criteria</h3>
  {card_grid(motivation.get('criteria'), 'No motivation criteria recorded yet.')}
  <h3>Existing Landscape</h3>
  {landscape_table(motivation.get('landscape'))}
  <h3>Novelty Gap</h3>
  {card_grid(motivation.get('gaps'), 'No novelty gaps recorded yet.')}
</section>
<section id="method">
  <div class="section-head">
    <p class="eyebrow">Stage 2</p>
    <h2>Method</h2>
    <p>The method section should make the mechanism inspectable before any result is claimed.</p>
  </div>
  <div class="method-grid">
    <article>
      <h3>Claim</h3>
      <p>{esc(compact_text(method.get('claim')))}</p>
    </article>
    <article>
      <h3>Formulation</h3>
      <pre>{esc(compact_text(method.get('formulation')))}</pre>
    </article>
    <article>
      <h3>Algorithm</h3>
      <pre>{esc(compact_text(method.get('algorithm')))}</pre>
    </article>
  </div>
  <h3>Rigor Review</h3>
  {card_grid(method.get('rigor_review'), 'No rigor review recorded yet.')}
</section>
<section id="experiments">
  <div class="section-head">
    <p class="eyebrow">Stage 3</p>
    <h2>Experiments</h2>
    <p>Evaluation claims are mapped to datasets, metrics, baselines, and failure analysis.</p>
  </div>
  <h3>Evaluation Claims</h3>
  {card_grid(experiments.get('claims'), 'No evaluation claims recorded yet.')}
  <h3>Experiment Matrix</h3>
  {experiment_table(experiments.get('plan'))}
  <h3>Qualitative and Risk Analysis</h3>
  <div class="split-grid">
    <div>{card_grid(experiments.get('qualitative'), 'No qualitative analysis plan recorded yet.')}</div>
    <div>{card_grid(experiments.get('risks'), 'No risks recorded yet.')}</div>
  </div>
</section>
<section>
  <div class="section-head">
    <p class="eyebrow">Review</p>
    <h2>Open Questions</h2>
  </div>
  {open_questions_html(state.get('open_questions', []))}
</section>
{render_slides_section(slide_assets, output_path)}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, help="Repository root. Defaults to the parent of .research-agent.")
    parser.add_argument("--state", type=Path, default=Path(".research-agent/state.json"))
    parser.add_argument("--output", type=Path, default=Path("research/research-brief.html"))
    parser.add_argument(
        "--no-slide-preview",
        action="store_true",
        help="Do not discover slides-grab PNG/SVG previews.",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "templates" / "html" / "research-brief.template.html",
    )
    args = parser.parse_args()

    repo_root = args.repo.resolve() if args.repo else infer_repo_root(args.state)
    state_path = args.state if args.state.is_absolute() else repo_root / args.state
    output_path = args.output if args.output.is_absolute() else repo_root / args.output
    state = json.loads(state_path.read_text(encoding="utf-8"))
    template = Template(args.template.read_text(encoding="utf-8"))
    research = state.get("research") if isinstance(state.get("research"), dict) else {}
    title = research.get("question") or "Research Brief"
    slide_assets = prepare_slide_assets(state, repo_root, output_path, not args.no_slide_preview)
    html_text = template.safe_substitute(
        title=esc(title),
        body=render_body(state, slide_assets, repo_root, output_path),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
