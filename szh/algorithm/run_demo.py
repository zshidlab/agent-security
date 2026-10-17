"""Run a portable local smoke demo and write JSON evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from src.mini_executor import MiniExecutor


REQUIRED_TASK_FIELDS = ("task_id", "notification_id", "file_id", "appointment_id", "requested_time", "subject")


def _load_task(task: str) -> dict:
    if task == "booking":
        path = Path(__file__).parent / "examples" / "booking.json"
    else:
        path = Path(task)
    if not path.is_file():
        raise ValueError(f"task input not found: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"task JSON error at line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(value, dict):
        raise ValueError("task input must be an object at $")
    missing = [field for field in REQUIRED_TASK_FIELDS if field not in value]
    if missing:
        raise ValueError(f"missing task fields at $: {', '.join(missing)}")
    return value


def run(task: str, output_dir: Path) -> int:
    payload = _load_task(task)
    output_dir.mkdir(parents=True, exist_ok=True)
    executor = MiniExecutor()
    calls = [
        executor.read_notification(payload["notification_id"]),
        executor.read_file(payload["file_id"]),
        executor.modify_appointment(payload["appointment_id"], payload["requested_time"], subject=payload["subject"]),
        executor.view_result(payload["appointment_id"]),
    ]
    changed = executor.state["appointments"][payload["appointment_id"]]["time"]
    events = []
    for call in calls:
        events.append({"event_type": "request", "tool": call["tool"], "request": call["request"], "request_axis": call["request"]})
        events.append({"event_type": "execution", "tool": call["tool"], "attempt": call["attempt"], "blocked": call["blocked"], "violated": call["violated"]})
        events.append({"event_type": "observation", "tool": call["tool"], "before": call["before"], "after": call["after"], "effect": call["effect"]})
    executor.reset()
    events.append({"event_type": "reset", "restored": executor.state["appointments"][payload["appointment_id"]]})
    evidence = {"schema_version": "demo-1.0", "task": task, "synthetic": True, "events": events, "reset_time": executor.state["appointments"][payload["appointment_id"]]["time"], "changed_time": changed}
    (output_dir / "demo-output.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_dir / "demo-output.json"), "event_count": len(evidence["events"]), "changed_time": changed, "reset_time": evidence["reset_time"]}, ensure_ascii=False))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run OAPT_A local synthetic booking demo")
    parser.add_argument("--task", required=True, help="booking or a JSON task path")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    return run(args.task, args.output_dir)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
