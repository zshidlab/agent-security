from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def adapt_sample(sample: dict[str, Any], source: str) -> dict[str, Any]:
    """Create a low-trust test input; never forwards gold, Oracle or local results."""
    forbidden = {"gold", "expected_outcome", "trajectory", "tool_result", "oracle", "evidence"}
    user_input = sample.get("user_input") or sample.get("request") or ""
    if not isinstance(user_input, str): user_input = json.dumps(user_input, ensure_ascii=False)
    return {"sample_id": sample.get("sample_id", hashlib.sha256(user_input.encode()).hexdigest()[:16]), "source": source, "source_hash": hashlib.sha256(json.dumps(sample, sort_keys=True, ensure_ascii=False).encode()).hexdigest(), "content_class": "malicious" if sample.get("dialogue_label") == "malicious" or sample.get("label") == "malicious" else "benign", "untrusted_content": user_input, "redacted_fields": sorted(forbidden & set(sample))}


def load_samples(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip(): rows.append(json.loads(line))
    return rows

