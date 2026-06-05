#!/usr/bin/env python3
"""Small helper for updating research-agent state JSON."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, state: dict[str, object]) -> None:
    state["updated_at"] = now()
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def set_path(obj: dict[str, object], dotted: str, value: object) -> None:
    parts = dotted.split(".")
    cur: dict[str, object] = obj
    for part in parts[:-1]:
        nxt = cur.setdefault(part, {})
        if not isinstance(nxt, dict):
            raise SystemExit(f"cannot descend into non-object path: {part}")
        cur = nxt
    cur[parts[-1]] = value


def parse_value(raw: str) -> object:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path(".research-agent/state.json"))
    sub = parser.add_subparsers(dest="command", required=True)

    set_cmd = sub.add_parser("set")
    set_cmd.add_argument("path")
    set_cmd.add_argument("value")

    stage_cmd = sub.add_parser("stage-status")
    stage_cmd.add_argument("stage")
    stage_cmd.add_argument("status")

    decision_cmd = sub.add_parser("add-decision")
    decision_cmd.add_argument("--stage", required=True)
    decision_cmd.add_argument("--question", required=True)
    decision_cmd.add_argument("--selected-option", required=True)
    decision_cmd.add_argument("--rationale", default="")

    args = parser.parse_args()
    state = load(args.state)

    if args.command == "set":
        set_path(state, args.path, parse_value(args.value))
    elif args.command == "stage-status":
        stages = state.setdefault("workflow", {}).setdefault("stages", {})
        stage = stages.setdefault(args.stage, {"outputs": []})
        stage["status"] = args.status
        state.setdefault("workflow", {})["current_stage"] = args.stage
    elif args.command == "add-decision":
        decision = {
            "timestamp": now(),
            "stage": args.stage,
            "question": args.question,
            "selected_option": args.selected_option,
            "rationale": args.rationale,
        }
        state.setdefault("decisions", []).append(decision)
        decisions_path = args.state.parent / "decisions.jsonl"
        decisions_path.parent.mkdir(parents=True, exist_ok=True)
        with decisions_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(decision, ensure_ascii=False) + "\n")

    save(args.state, state)
    print(args.state)


if __name__ == "__main__":
    main()

