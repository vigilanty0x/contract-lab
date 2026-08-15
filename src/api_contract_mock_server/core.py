from __future__ import annotations
from datetime import datetime
from hashlib import sha256
import json
import re
from typing import Any

PROJECT = "api-contract-mock-server"
REQUIRED_FIELDS = ["contract","routes","modes","default_status"]

def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())

def _string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_text(item) for item in value)

def _integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)

def build_mock_scenarios(record: dict[str, Any]) -> dict[str, Any]:
    if not _text(record["contract"]) or not _string_list(record["routes"]):
        raise ValueError("contract and routes are required")
    modes = record["modes"]
    if not _string_list(modes) or not {"success", "degraded", "invalid"}.issubset(set(modes)):
        raise ValueError("success, degraded, and invalid modes are mandatory")
    status = record["default_status"]
    if not _integer(status) or not 100 <= status <= 599:
        raise ValueError("default status must be an HTTP integer")
    responses: dict[str, Any] = {}
    for route in record["routes"]:
        responses[route] = {
            "success": {"status": status, "body": {"ok": True}},
            "degraded": {"status": 206, "body": {"ok": False, "state": "degraded"}},
            "invalid": {"status": 500, "body": "invalid-contract-response"},
        }
    return responses

def evaluate(record: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    artifact: Any = None
    if missing:
        status = "blocked"
        reason = "missing required fields: " + ", ".join(missing)
    else:
        try:
            artifact = build_mock_scenarios(record)
            status = "passed"
            reason = "build_mock_scenarios completed"
        except (TypeError, ValueError, KeyError) as exc:
            status = "failed"
            reason = str(exc)
    receipt = {"project": PROJECT, "status": status, "reason": reason, "record": record, "responses": artifact}
    receipt["evidence_sha256"] = sha256(_canonical(receipt).encode()).hexdigest()
    return receipt

