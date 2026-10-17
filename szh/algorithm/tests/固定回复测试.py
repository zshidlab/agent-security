from fixed_model import FixedReplyModel


def test_fixed_reply_is_deterministic():
    model = FixedReplyModel()
    request = {"request_id": "req-001", "prompt": "read synthetic booking", "synthetic": True}
    assert model.respond(request) == model.respond(request)
    assert model.respond(request)["model"] == "fixed_reply"


def test_fixed_reply_rejects_missing_fields():
    try:
        FixedReplyModel().respond({"request_id": "req-002", "synthetic": True})
    except ValueError as exc:
        assert "prompt" in str(exc)
    else:
        raise AssertionError("missing prompt must be rejected")
