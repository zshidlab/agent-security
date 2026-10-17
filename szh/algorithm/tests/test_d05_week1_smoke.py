import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_demo_command_produces_four_events_and_reset():
    with tempfile.TemporaryDirectory(prefix="oapt-d05-") as directory:
        output = Path(directory)
        result = subprocess.run([sys.executable, "-B", "algorithm/run_demo.py", "--task", "booking", "--output-dir", str(output)], cwd=ROOT, text=True, capture_output=True)
        assert result.returncode == 0, result.stderr
        evidence = json.loads((output / "demo-output.json").read_text(encoding="utf-8"))
        assert {event["event_type"] for event in evidence["events"]} == {"request", "execution", "observation", "reset"}
        assert evidence["changed_time"].endswith("14:00:00+08:00")
        assert evidence["reset_time"].endswith("10:00:00+08:00")


def test_demo_stops_on_missing_field():
    with tempfile.TemporaryDirectory(prefix="oapt-d05-bad-") as directory:
        root = Path(directory)
        bad = root / "bad.json"
        bad.write_text('{"task_id":"task-bad"}', encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", "algorithm/run_demo.py", "--task", str(bad), "--output-dir", str(root / "bad-out")], cwd=ROOT, text=True, capture_output=True)
        assert result.returncode == 2
        assert "missing task fields" in result.stderr
