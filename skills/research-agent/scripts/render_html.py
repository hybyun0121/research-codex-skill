#!/usr/bin/env python3
"""Render `.research-agent/state.json` into `research/research-brief.html`."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from string import Template


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


def render_body(state: dict[str, object]) -> str:
    project = state.get("project") if isinstance(state.get("project"), dict) else {}
    research = state.get("research") if isinstance(state.get("research"), dict) else {}
    motivation = state.get("motivation") if isinstance(state.get("motivation"), dict) else {}
    method = state.get("method") if isinstance(state.get("method"), dict) else {}
    experiments = state.get("experiments") if isinstance(state.get("experiments"), dict) else {}
    workflow = state.get("workflow") if isinstance(state.get("workflow"), dict) else {}

    return f"""
<header>
  <p class="muted">Research Agent Brief</p>
  <h1>{esc(research.get('question') or 'Untitled Research Question')}</h1>
  <p>{esc(research.get('domain') or '')}</p>
</header>
<section>
  <h2>Status</h2>
  <div class="callout">
    <strong>Current stage:</strong> {esc(workflow.get('current_stage'))}<br>
    <strong>Repo type:</strong> {esc(project.get('repo_type'))}<br>
    <strong>Selected direction:</strong> {esc(research.get('selected_direction') or 'Not selected yet.')}
  </div>
</section>
<section>
  <h2>Motivation</h2>
  <h3>Criteria</h3>
  {list_items(motivation.get('criteria'))}
  <h3>Existing Landscape</h3>
  {landscape_table(motivation.get('landscape'))}
  <h3>Gaps</h3>
  {list_items(motivation.get('gaps'))}
</section>
<section>
  <h2>Method</h2>
  <h3>Claim</h3>
  <p>{esc(method.get('claim') or 'Not specified yet.')}</p>
  <h3>Formulation</h3>
  <pre>{esc(method.get('formulation') or 'Not specified yet.')}</pre>
  <h3>Algorithm</h3>
  <pre>{esc(method.get('algorithm') or 'Not specified yet.')}</pre>
  <h3>Rigor Review</h3>
  {list_items(method.get('rigor_review'))}
</section>
<section>
  <h2>Experiments</h2>
  <h3>Evaluation Claims</h3>
  {list_items(experiments.get('claims'))}
  <h3>Experiment Plan</h3>
  {experiment_table(experiments.get('plan'))}
  <h3>Qualitative Analysis</h3>
  {list_items(experiments.get('qualitative'))}
</section>
<section>
  <h2>Open Questions</h2>
  {list_items([q.get('question', q) if isinstance(q, dict) else q for q in state.get('open_questions', [])])}
</section>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path(".research-agent/state.json"))
    parser.add_argument("--output", type=Path, default=Path("research/research-brief.html"))
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "templates" / "html" / "research-brief.template.html",
    )
    args = parser.parse_args()

    state = json.loads(args.state.read_text(encoding="utf-8"))
    template = Template(args.template.read_text(encoding="utf-8"))
    research = state.get("research") if isinstance(state.get("research"), dict) else {}
    title = research.get("question") or "Research Brief"
    html_text = template.safe_substitute(title=esc(title), body=render_body(state))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_text, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()

