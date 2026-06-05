#!/usr/bin/env python3
"""Validate `.research-agent/state.json` without requiring external packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "project",
    "research",
    "workflow",
    "artifacts",
    "decisions",
    "open_questions",
}

REQUIRED_STAGES = {
    "repo_inspection",
    "motivation",
    "method",
    "experiments",
    "html_brief",
    "slides",
}


def validate(state: dict[str, object]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_TOP_LEVEL - set(state)
    if missing:
        errors.append(f"missing top-level keys: {', '.join(sorted(missing))}")

    workflow = state.get("workflow")
    if not isinstance(workflow, dict):
        errors.append("workflow must be an object")
        return errors

    stages = workflow.get("stages")
    if not isinstance(stages, dict):
        errors.append("workflow.stages must be an object")
        return errors

    missing_stages = REQUIRED_STAGES - set(stages)
    if missing_stages:
        errors.append(f"missing stages: {', '.join(sorted(missing_stages))}")

    for name, spec in stages.items():
        if not isinstance(spec, dict):
            errors.append(f"stage {name} must be an object")
            continue
        if "status" not in spec:
            errors.append(f"stage {name} missing status")
        if "outputs" not in spec:
            errors.append(f"stage {name} missing outputs")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path(".research-agent/state.json"))
    args = parser.parse_args()

    state = json.loads(args.state.read_text(encoding="utf-8"))
    errors = validate(state)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"ok: {args.state}")


if __name__ == "__main__":
    main()

