import json
from pathlib import Path

from fixed_model import FixedReplyModel


def test_booking_sample_and_fixed_model():
    booking = json.loads(Path("algorithm/examples/booking.json").read_text(encoding="utf-8"))
    result = FixedReplyModel().respond(
        {"request_id": booking["task_id"], "prompt": "read booking", "synthetic": booking["synthetic"]}
    )
    assert result["synthetic"] is True
    assert result["response"].startswith("FIXED_REPLY:")


def test_no_secret_or_network_configuration_is_needed():
    source = Path("algorithm/src/fixed_model.py").read_text(encoding="utf-8")
    assert "os.environ" not in source
    assert "requests." not in source
