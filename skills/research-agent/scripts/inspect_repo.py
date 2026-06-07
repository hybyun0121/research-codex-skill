#!/usr/bin/env python3
"""Inspect the current repository and emit a safe research-agent repo profile."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path


SECRET_PATTERNS = (
    ".env",
    ".pem",
    ".key",
    "id_rsa",
    "id_ed25519",
    "token",
    "secret",
    "credential",
    "password",
)

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".vite",
    "outputs",
    "data",
    "dataset",
    "datasets",
    "checkpoints",
    "models",
    "weights",
    "artifacts",
}

MAX_SAFE_FILES = 5000

RESULT_DIR_NAMES = {
    "results",
    "result",
    "runs",
    "logs",
    "log",
    "outputs",
    "output",
    "wandb",
    "tensorboard",
    "lightning_logs",
    "mlruns",
    "eval_results",
    "predictions",
}

RESULT_FILE_SUFFIXES = {".csv", ".tsv", ".json", ".jsonl", ".md", ".txt", ".log"}

METHOD_FILE_SUFFIXES = {".py", ".ipynb", ".sh", ".yaml", ".yml", ".json", ".toml"}


def is_secret_path(path: Path) -> bool:
    lowered = str(path).lower()
    return any(pattern in lowered for pattern in SECRET_PATTERNS)


def iter_safe_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_dir = current.relative_to(root)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in SKIP_DIRS and not is_secret_path(rel_dir / dirname)
        ]
        for filename in filenames:
            rel = (current / filename).relative_to(root)
            if is_secret_path(rel):
                continue
            files.append(rel)
            if len(files) >= MAX_SAFE_FILES:
                return files
    return files


def read_text_limited(path: Path, limit: int = 20000) -> str:
    if not path.exists() or is_secret_path(path):
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def has_any(files: list[Path], names: set[str]) -> bool:
    return any(path.name in names for path in files)


def contains_part(files: list[Path], part_names: set[str]) -> bool:
    return any(any(part in part_names for part in path.parts) for path in files)


def run_git(root: Path, args: list[str], limit: int = 20000) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout[:limit]


def parse_git_status(root: Path) -> list[str]:
    output = run_git(root, ["status", "--porcelain=v1"])
    paths: list[str] = []
    for line in output.splitlines():
        if len(line) < 4:
            continue
        raw = line[3:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        path = Path(raw)
        if is_secret_path(path):
            continue
        paths.append(str(path))
    return paths[:100]


def git_remote_detected(root: Path) -> bool:
    return bool(run_git(root, ["remote"], limit=2000).strip())


def current_branch(root: Path) -> str | None:
    branch = run_git(root, ["branch", "--show-current"], limit=1000).strip()
    return branch or None


def find_result_artifacts(root: Path, files: list[Path]) -> tuple[list[str], list[str]]:
    artifact_dirs: set[str] = set()
    result_files: list[str] = []

    for path in files:
        if any(part.lower() in RESULT_DIR_NAMES for part in path.parts):
            artifact_dirs.add(path.parts[0])
            lowered_name = path.name.lower()
            if path.suffix.lower() in RESULT_FILE_SUFFIXES or re.search(
                r"(result|metric|leaderboard|score|summary|sweep|ablation)", lowered_name
            ):
                result_files.append(str(path))

    # Detect heavy result directories that are intentionally skipped by iter_safe_files.
    for child in root.iterdir():
        if child.is_dir() and child.name.lower() in RESULT_DIR_NAMES:
            artifact_dirs.add(child.name)

    return sorted(artifact_dirs)[:50], sorted(set(result_files))[:100]


def candidate_method_files(files: list[Path], modified_files: list[str]) -> list[str]:
    modified = {Path(path) for path in modified_files}
    candidates: list[str] = []
    for path in files:
        lowered = str(path).lower()
        if path.suffix.lower() not in METHOD_FILE_SUFFIXES:
            continue
        if path in modified or re.search(r"(model|method|module|layer|loss|trainer|train|eval|config)", lowered):
            candidates.append(str(path))
    return sorted(set(candidates))[:80]


def classify(
    root: Path,
    files: list[Path],
    readme_text: str,
    modified_files: list[str],
    artifact_dirs: list[str],
    result_files: list[str],
) -> tuple[str, list[str]]:
    evidence: list[str] = []

    if (root / ".research-agent" / "state.json").exists():
        evidence.append(".research-agent/state.json exists")
        return "partial_research_agent_project", evidence

    meaningful = [
        path
        for path in files
        if path.parts[0] not in {".research-agent", "research", "slides"}
        and path.name not in {".DS_Store"}
    ]
    if not meaningful:
        evidence.append("no meaningful project files found")
        return "empty_repo", evidence

    dep_files = {"pyproject.toml", "requirements.txt", "environment.yml", "package.json", "setup.py"}
    if has_any(files, dep_files):
        evidence.append("dependency file exists")

    train_eval = [
        path
        for path in files
        if re.search(r"(train|finetune|eval|evaluate|benchmark)", path.name, re.I)
    ]
    if train_eval:
        evidence.append("training/evaluation scripts detected")

    if contains_part(files, {"configs", "config", "checkpoints", "scripts"}):
        evidence.append("configs/scripts/checkpoints directory detected")

    paper_signals = re.search(r"(arxiv|openreview|acl anthology|proceedings|citation|bibtex|paper)", readme_text, re.I)
    if paper_signals:
        evidence.append("README contains paper/citation signals")

    baseline_like = bool(readme_text and (train_eval or paper_signals) and len(evidence) >= 2)
    user_work_like = bool(modified_files or artifact_dirs or result_files)
    if baseline_like and user_work_like:
        if modified_files:
            evidence.append("git status indicates user modifications or untracked files")
        if artifact_dirs or result_files:
            evidence.append("experiment/result artifacts detected")
        return "baseline_working_project", evidence

    if baseline_like:
        return "official_baseline", evidence

    evidence.append("source or project files exist")
    return "existing_user_project", evidence


def extract_links(text: str) -> list[str]:
    return sorted(set(re.findall(r"https?://[^\s)\]>\"']+", text)))


def build_profile(root: Path) -> dict[str, object]:
    files = iter_safe_files(root)
    readme_candidates = [root / name for name in ("README.md", "README.rst", "README.txt")]
    readme_text = ""
    for candidate in readme_candidates:
        readme_text = read_text_limited(candidate)
        if readme_text:
            break

    modified_files = parse_git_status(root)
    artifact_dirs, result_files = find_result_artifacts(root, files)
    repo_type, evidence = classify(root, files, readme_text, modified_files, artifact_dirs, result_files)
    paper_links = [
        url for url in extract_links(readme_text)
        if re.search(r"(arxiv|openreview|aclanthology|doi|proceedings|paper|pdf)", url, re.I)
    ]

    license_file = next((str(path) for path in files if path.name.lower().startswith("license")), None)

    import_signals = []
    if repo_type == "baseline_working_project":
        import_signals.append("official baseline evidence plus existing user work detected")
    if modified_files:
        import_signals.append("git status has modified or untracked files")
    if artifact_dirs:
        import_signals.append("result artifact directories exist")
    if result_files:
        import_signals.append("result summary files exist")

    method_files = candidate_method_files(files, modified_files)
    config_files = [str(path) for path in files if path.suffix.lower() in {".yaml", ".yml", ".json", ".toml"}][:80]

    return {
        "repo_type": repo_type,
        "repo_name": root.name,
        "baseline_detected": repo_type in {"official_baseline", "baseline_working_project"},
        "baseline_source": paper_links[0] if paper_links else None,
        "import_recommended": repo_type == "baseline_working_project",
        "import_signals": import_signals,
        "git_remote_detected": git_remote_detected(root),
        "git_branch": current_branch(root),
        "evidence": evidence,
        "safe_file_count": len(files),
        "paper_links": paper_links,
        "license": license_file,
        "main_task": None,
        "implemented_method": None,
        "claimed_contributions": [],
        "training_pipeline": [str(path) for path in files if re.search(r"(train|finetune)", path.name, re.I)][:20],
        "evaluation_pipeline": [str(path) for path in files if re.search(r"(eval|evaluate|benchmark)", path.name, re.I)][:20],
        "reusable_components": [str(path) for path in files if path.suffix in {".py", ".ipynb", ".sh", ".yaml", ".yml", ".json"}][:50],
        "modified_files": modified_files,
        "candidate_method_files": method_files,
        "candidate_config_files": config_files,
        "experiment_artifact_dirs": artifact_dirs,
        "result_files": result_files,
        "risks": [],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--write", action="store_true", help="Write .research-agent/repo_profile.json")
    args = parser.parse_args()

    root = args.repo.resolve()
    profile = build_profile(root)
    if args.write:
        out = root / ".research-agent" / "repo_profile.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(profile, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
