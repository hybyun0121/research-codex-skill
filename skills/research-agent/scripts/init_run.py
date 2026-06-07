#!/usr/bin/env python3
"""Initialize research-agent state in the current research repository."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import inspect_repo


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_state(profile: dict[str, object]) -> dict[str, object]:
    repo_type = str(profile.get("repo_type") or "unknown")
    baseline_detected = bool(profile.get("baseline_detected"))
    stages = {
        "repo_inspection": {
            "status": "complete",
            "outputs": [".research-agent/repo_profile.json"],
        },
        "motivation": {
            "status": "blocked",
            "blocked_by": ["research.question"],
            "outputs": ["research/motivation.md"],
        },
        "method": {
            "status": "blocked",
            "blocked_by": ["research.selected_direction"],
            "outputs": ["research/method.md"],
        },
        "experiments": {
            "status": "blocked",
            "blocked_by": ["method.spec"],
            "outputs": ["research/experiments.md"],
        },
        "html_brief": {
            "status": "blocked",
            "blocked_by": ["motivation", "method", "experiments"],
            "outputs": ["research/research-brief.html"],
        },
        "slides": {
            "status": "blocked",
            "blocked_by": ["html_brief"],
            "outputs": [
                "slides/slide-01.html",
                "slides/viewer.html",
                "slides/research-presentation.pdf",
                "slides/out-png/",
            ],
        },
    }
    current_stage = "repo_inspection"
    if repo_type == "empty_repo":
        stages["goal_instruction"] = {
            "status": "blocked",
            "blocked_by": ["user.goal_instruction_start_choice"],
            "outputs": [
                ".research-agent/goal_instruction.md",
                ".research-agent/goal_command.txt",
                ".research-agent/goal_instruction.json",
            ],
        }
        current_stage = "goal_instruction"

    return {
        "schema_version": "0.1.0",
        "project": {
            "repo_type": repo_type,
            "repo_name": profile.get("repo_name"),
            "baseline_detected": baseline_detected,
            "baseline_source": profile.get("baseline_source"),
            "evidence": profile.get("evidence", []),
        },
        "research": {
            "question": None,
            "domain": None,
            "target_venue_level": None,
            "selected_direction": None,
        },
        "motivation": {
            "criteria": [],
            "landscape": [],
            "gaps": [],
            "candidates": [],
        },
        "method": {},
        "experiments": {
            "claims": [],
            "plan": [],
            "sweeps": [],
            "leaderboard": [],
            "qualitative": [],
            "risks": [],
        },
        "workflow": {
            "current_stage": current_stage,
            "stages": stages,
        },
        "artifacts": {
            "goal_instruction_md": ".research-agent/goal_instruction.md",
            "goal_command_txt": ".research-agent/goal_command.txt",
            "goal_instruction_json": ".research-agent/goal_instruction.json",
            "status_md": "research/status.md",
            "motivation_md": "research/motivation.md",
            "method_md": "research/method.md",
            "experiments_md": "research/experiments.md",
            "html_brief": "research/research-brief.html",
            "slide_deck_dir": "slides",
            "slide_viewer": "slides/viewer.html",
            "slide_pdf": "slides/research-presentation.pdf",
            "slide_png_dir": "slides/out-png",
            "slides": "slides/research-presentation.pptx",
        },
        "decisions": [],
        "open_questions": [],
        "created_at": now(),
        "updated_at": now(),
    }


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = args.repo.resolve()
    state_path = root / ".research-agent" / "state.json"
    if state_path.exists() and not args.force:
        raise SystemExit(f"state already exists: {state_path}")

    profile = inspect_repo.build_profile(root)
    agent_dir = root / ".research-agent"
    research_dir = root / "research"
    agent_dir.mkdir(parents=True, exist_ok=True)
    research_dir.mkdir(parents=True, exist_ok=True)

    (agent_dir / "repo_profile.json").write_text(
        json.dumps(profile, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (agent_dir / "config.json").write_text(
        json.dumps({"schema_version": "0.1.0", "created_by": "research-agent"}, indent=2) + "\n",
        encoding="utf-8",
    )
    (agent_dir / "decisions.jsonl").touch()

    state = default_state(profile)
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_if_missing(
        research_dir / "status.md",
        "# Research Agent Status\n\n"
        f"- Current stage: {state['workflow']['current_stage']}\n"
        f"- Repository type: {profile.get('repo_type')}\n"
        "- Next action: resolve the first blocking research decision.\n",
    )
    write_if_missing(research_dir / "motivation.md", "# Motivation\n\nNot started.\n")
    write_if_missing(research_dir / "method.md", "# Method\n\nNot started.\n")
    write_if_missing(research_dir / "experiments.md", "# Experiments\n\nNot started.\n")

    print(state_path)


if __name__ == "__main__":
    main()
