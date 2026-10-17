import copy
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).parents[2]
SCHEMA = json.loads((ROOT / "algorithm/schemas/trace.schema.json").read_text(encoding="utf-8"))


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def semantic_errors(trace):
    errors = []
    for namespace in ("turn_id", "message_id", "event_id"):
        values = []
        for turn in trace["turns"]:
            values.append(turn[namespace] if namespace == "turn_id" else None)
            values.extend(item.get(namespace) for item in turn.get("messages", []) if namespace == "message_id")
        values.extend(item.get(namespace) for item in turn.get("events", []) if namespace in item)
        values = [v for v in values if v is not None]
        if len(values) != len(set(values)):
            errors.append(f"duplicate {namespace}")
    return errors


def test_valid_trace_schema_and_ids():
    trace = load("algorithm/data/轨迹示例.json")
    jsonschema.validate(trace, SCHEMA)
    assert semantic_errors(trace) == []


def test_missing_fields_report_json_path():
    trace = load("algorithm/tests/fixtures/trace_invalid.json")
    errors = sorted(jsonschema.Draft202012Validator(SCHEMA).iter_errors(trace), key=lambda e: list(e.path))
    assert errors
    assert any("messages" in ".".join(str(x) for x in error.absolute_path) for error in errors)


def test_duplicate_ids_are_rejected_and_text_does_not_make_effect():
    trace = load("algorithm/tests/fixtures/trace_duplicate_ids.json")
    jsonschema.validate(trace, SCHEMA)
    assert any("duplicate turn_id" == error for error in semantic_errors(trace))
    text_only = copy.deepcopy(load("algorithm/data/轨迹示例.json"))
    text_only["turns"][0]["events"] = []
    assert not any(event.get("effect") == "observed" for turn in text_only["turns"] for event in turn["events"])
