"""Deterministic, credential-free model stand-in for local tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FixedReplyModel:
    """Return a fixed reply only for an explicit synthetic request."""

    reply: str = "FIXED_REPLY: synthetic request accepted for local testing"
    schema_version: str = "fixed-reply-1.0"

    def respond(self, request: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(request, dict):
            raise TypeError("request must be an object")
        missing = [key for key in ("request_id", "prompt", "synthetic") if key not in request]
        if missing:
            raise ValueError("missing request fields: " + ", ".join(missing))
        if request["synthetic"] is not True:
            raise ValueError("fixed model accepts synthetic=true only")
        if not isinstance(request["request_id"], str) or not request["request_id"]:
            raise ValueError("request_id must be a non-empty string")
        if not isinstance(request["prompt"], str):
            raise ValueError("prompt must be a string")
        return {
            "schema_version": self.schema_version,
            "model": "fixed_reply",
            "request_id": request["request_id"],
            "response": self.reply,
            "synthetic": True,
        }
