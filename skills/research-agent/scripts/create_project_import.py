#!/usr/bin/env python3
"""Create project import artifacts for a user-modified baseline repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import inspect_repo


def load_or_build_profile(root: Path) -> dict[str, object]:
    profile_path = root / ".research-agent" / "repo_profile.json"
    if profile_path.exists():
        return json.loads(profile_path.read_text(encoding="utf-8"))
    return inspect_repo.build_profile(root)


def stage_import(status: str, evidence: list[str], outputs: list[str], blocked_by: list[str] | None = None) -> dict[str, object]:
    item: dict[str, object] = {
        "suggested_status": status,
        "evidence": evidence,
        "outputs": outputs,
    }
    if blocked_by:
        item["blocked_by"] = blocked_by
    return item


def build_manifest(root: Path, profile: dict[str, object]) -> dict[str, object]:
    paper_links = list(profile.get("paper_links") or [])
    modified_files = list(profile.get("modified_files") or [])
    method_files = list(profile.get("candidate_method_files") or [])
    config_files = list(profile.get("candidate_config_files") or [])
    artifact_dirs = list(profile.get("experiment_artifact_dirs") or [])
    result_files = list(profile.get("result_files") or [])
    import_signals = list(profile.get("import_signals") or [])

    open_questions = []
    if not paper_links:
        open_questions.append({
            "id": "baseline_paper",
            "question": "Which paper or official baseline should be treated as the canonical baseline?",
            "recommended_option": None,
            "options": [],
            "blocks": ["motivation", "experiments"],
        })
    if method_files:
        open_questions.append({
            "id": "proposed_method_files",
            "question": "Which modified files define the proposed Method rather than experiment plumbing?",
            "recommended_option": method_files[0],
            "options": method_files[:5],
            "blocks": ["method"],
        })
    else:
        open_questions.append({
            "id": "proposed_method_files",
            "question": "Which files define the proposed Method?",
            "recommended_option": None,
            "options": [],
            "blocks": ["method"],
        })
    if artifact_dirs or result_files:
        options = [*artifact_dirs[:3], *result_files[:3]]
        open_questions.append({
            "id": "authoritative_results",
            "question": "Which result artifact should be treated as authoritative for the main comparison?",
            "recommended_option": options[0] if options else None,
            "options": options,
            "blocks": ["experiments", "html_brief", "slides"],
        })
    else:
        open_questions.append({
            "id": "authoritative_results",
            "question": "Where are the baseline and proposed experiment results stored?",
            "recommended_option": None,
            "options": [],
            "blocks": ["experiments"],
        })

    return {
        "schema_version": "0.1.0",
        "repo": {
            "name": str(profile.get("repo_name") or root.name),
            "type": str(profile.get("repo_type") or "unknown"),
            "root": str(root),
            "remote_detected": bool(profile.get("git_remote_detected")),
            "branch": profile.get("git_branch"),
        },
        "baseline": {
            "detected": bool(profile.get("baseline_detected")),
            "paper_links": paper_links,
            "repo_evidence": list(profile.get("evidence") or []),
            "training_pipeline": list(profile.get("training_pipeline") or []),
            "evaluation_pipeline": list(profile.get("evaluation_pipeline") or []),
            "evidence": list(profile.get("evidence") or []),
        },
        "user_work": {
            "detected": bool(modified_files or method_files or artifact_dirs or result_files),
            "signals": import_signals,
            "modified_files": modified_files,
            "candidate_method_files": method_files,
            "candidate_config_files": config_files,
            "notes": [],
        },
        "experiments": {
            "artifact_dirs": artifact_dirs,
            "result_files": result_files,
            "leaderboard_candidates": [
                path for path in result_files if "leaderboard" in path.lower() or "score" in path.lower()
            ],
            "sweep_candidates": [
                path for path in [*result_files, *config_files] if "sweep" in path.lower() or "ablation" in path.lower()
            ],
            "qualitative_candidates": [
                path for path in result_files if "qual" in path.lower() or "sample" in path.lower()
            ],
        },
        "stage_reconstruction": {
            "motivation": stage_import(
                "in_progress" if paper_links else "blocked",
                paper_links or list(profile.get("evidence") or []),
                ["research/motivation.md", "research/motivation.ko.md"],
                None if paper_links else ["baseline_paper", "research.question"],
            ),
            "method": stage_import(
                "in_progress" if method_files else "blocked",
                method_files,
                ["research/method.md"],
                None if method_files else ["proposed_method_files"],
            ),
            "experiments": stage_import(
                "in_progress" if artifact_dirs or result_files else "blocked",
                [*artifact_dirs, *result_files],
                ["research/experiments.md"],
                None if artifact_dirs or result_files else ["authoritative_results"],
            ),
            "html_brief": stage_import(
                "blocked",
                [],
                ["research/research-brief.html"],
                ["motivation", "method", "experiments"],
            ),
            "slides": stage_import(
                "blocked",
                [],
                ["slides/slide-01.html", "slides/viewer.html", "slides/research-presentation.pdf"],
                ["html_brief"],
            ),
        },
        "open_questions": open_questions,
    }


def bullet(items: list[object]) -> str:
    if not items:
        return "- Not detected.\n"
    return "".join(f"- {item}\n" for item in items)


def markdown_summary(manifest: dict[str, object]) -> str:
    baseline = manifest["baseline"]
    user_work = manifest["user_work"]
    experiments = manifest["experiments"]
    repo = manifest["repo"]
    questions = manifest["open_questions"]

    return (
        "# Existing Project Import Summary\n\n"
        "## Import Decision\n\n"
        f"- Import mode: pending user confirmation\n"
        f"- Repository type: {repo.get('type')}\n"
        f"- Current branch: {repo.get('branch') or 'unknown'}\n"
        "- Authoritative result source: pending\n"
        "- Main baseline: pending\n"
        "- Proposed method label: pending\n\n"
        "## Baseline Identity\n\n"
        "- Official repository evidence:\n"
        f"{bullet(list(baseline.get('repo_evidence') or []))}"
        "- Paper or citation links:\n"
        f"{bullet(list(baseline.get('paper_links') or []))}"
        "- Training pipeline candidates:\n"
        f"{bullet(list(baseline.get('training_pipeline') or []))}"
        "- Evaluation pipeline candidates:\n"
        f"{bullet(list(baseline.get('evaluation_pipeline') or []))}"
        "\n## User Work Evidence\n\n"
        "- Import signals:\n"
        f"{bullet(list(user_work.get('signals') or []))}"
        "- Modified files:\n"
        f"{bullet(list(user_work.get('modified_files') or [])[:30])}"
        "- Candidate Method files:\n"
        f"{bullet(list(user_work.get('candidate_method_files') or [])[:30])}"
        "- Candidate config files:\n"
        f"{bullet(list(user_work.get('candidate_config_files') or [])[:30])}"
        "\n## Experiment Artifact Map\n\n"
        "- Artifact directories:\n"
        f"{bullet(list(experiments.get('artifact_dirs') or []))}"
        "- Result files:\n"
        f"{bullet(list(experiments.get('result_files') or [])[:40])}"
        "\n## Stage Reconstruction Plan\n\n"
        "| Stage | Suggested Status | Missing Confirmation |\n"
        "|---|---|---|\n"
        + "".join(
            f"| {name} | {spec.get('suggested_status')} | {', '.join(spec.get('blocked_by', [])) or 'None'} |\n"
            for name, spec in manifest["stage_reconstruction"].items()
        )
        + "\n## Open Questions\n\n"
        + "".join(f"{index}. {item.get('question')}\n" for index, item in enumerate(questions, start=1))
        + "\n## Next Actions\n\n"
        "- Confirm the authoritative baseline, proposed Method files, and main result artifact.\n"
        "- Reconstruct Motivation, Method, and Experiments from confirmed evidence.\n"
        "- Render the HTML brief, then create slides with the slides-grab workflow.\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = args.repo.resolve()
    agent_dir = root / ".research-agent"
    research_dir = root / "research"
    import_json = agent_dir / "project_import.json"
    import_md = research_dir / "project-import.md"

    if (import_json.exists() or import_md.exists()) and not args.force:
        raise SystemExit("project import artifacts already exist; pass --force to overwrite")

    profile = load_or_build_profile(root)
    manifest = build_manifest(root, profile)

    agent_dir.mkdir(parents=True, exist_ok=True)
    research_dir.mkdir(parents=True, exist_ok=True)
    import_json.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    import_md.write_text(markdown_summary(manifest), encoding="utf-8")
    print(import_json)
    print(import_md)


if __name__ == "__main__":
    main()
