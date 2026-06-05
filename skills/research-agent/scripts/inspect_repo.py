#!/usr/bin/env python3
"""Inspect the current repository and emit a safe research-agent repo profile."""

from __future__ import annotations

import argparse
import json
import re
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
}


def is_secret_path(path: Path) -> bool:
    lowered = str(path).lower()
    return any(pattern in lowered for pattern in SECRET_PATTERNS)


def iter_safe_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if is_secret_path(rel):
            continue
        if path.is_file():
            files.append(rel)
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


def classify(root: Path, files: list[Path], readme_text: str) -> tuple[str, list[str]]:
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

    if readme_text and (train_eval or paper_signals) and len(evidence) >= 2:
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

    repo_type, evidence = classify(root, files, readme_text)
    paper_links = [
        url for url in extract_links(readme_text)
        if re.search(r"(arxiv|openreview|aclanthology|doi|proceedings|paper|pdf)", url, re.I)
    ]

    license_file = next((str(path) for path in files if path.name.lower().startswith("license")), None)

    return {
        "repo_type": repo_type,
        "repo_name": root.name,
        "baseline_detected": repo_type == "official_baseline",
        "baseline_source": paper_links[0] if paper_links else None,
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

