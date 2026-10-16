import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1].parent))
from platform.core import MockRuntime, SecurityOracle
from platform.attack_test import run_fixture


def test_document_policy_blocks_public_sink():
    result = run_fixture("S-DOC", True)
    assert result["oracle"]["attacker_goal"] == "not_achieved"
    assert result["oracle"]["security_violation"] == "none"


def test_expense_malicious_submission_is_blocked():
    result = run_fixture("S-EXP", True)
    assert result["oracle"]["attacker_goal"] == "not_achieved"
    assert result["oracle"]["security_violation"] == "none"


def test_expense_benign_path_commits_with_fresh_confirmation():
    result = run_fixture("S-EXP", False)
    assert result["oracle"]["attacker_goal"] == "not_achieved"
    assert result["oracle"]["security_violation"] == "none"
    assert result["oracle"]["benign_utility"] == "completed"


def test_runtime_reset_isolation():
    runtime = MockRuntime("S-DOC")
    runtime.execute("publish_note", {"task_id": "t", "destination": "task-private", "text": "x"})
    runtime.reset()
    assert runtime.snapshot()["event_seq"] == 0
    assert runtime.docs.sinks == []

