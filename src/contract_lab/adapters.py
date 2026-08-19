from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import canonical_digest


@dataclass(frozen=True, slots=True)
class AdapterReceipt:
    source: str
    source_status: str
    verdict: str
    payload_digest: str

    def as_dict(self) -> dict[str, str]:
        return {
            "source": self.source,
            "source_status": self.source_status,
            "verdict": self.verdict,
            "payload_digest": self.payload_digest,
        }


def _receipt(source: str, source_status: str, verdict: str, payload: Any) -> AdapterReceipt:
    return AdapterReceipt(source, source_status, verdict, canonical_digest(payload))


def adapt_schema_validation(result: Any) -> AdapterReceipt:
    required = {"status", "errors", "errors_truncated", "records"}
    if not isinstance(result, dict) or set(result) != required:
        return _receipt("schema-contract-tester", "invalid", "BLOCKED", {"reason": "malformed_source_result"})
    status = result["status"]
    errors = result["errors"]
    if (
        status not in {"compatible", "blocked"}
        or not isinstance(errors, list)
        or not isinstance(result["errors_truncated"], bool)
        or not isinstance(result["records"], int)
        or isinstance(result["records"], bool)
        or result["records"] < 0
    ):
        return _receipt("schema-contract-tester", "invalid", "BLOCKED", {"reason": "malformed_source_result"})
    if status == "compatible" and not errors:
        verdict = "PASS"
    elif status == "blocked" and errors:
        verdict = "FAIL"
    else:
        verdict = "BLOCKED"
    return _receipt("schema-contract-tester", status, verdict, result)


def adapt_webhook(result: Any) -> AdapterReceipt:
    required = {"accepted", "errors", "assurance", "request_sha256", "bytes"}
    if (
        not isinstance(result, dict)
        or not required <= set(result)
        or not isinstance(result.get("accepted"), bool)
        or not isinstance(result.get("errors"), list)
        or not isinstance(result.get("assurance"), str)
        or not isinstance(result.get("request_sha256"), str)
        or not isinstance(result.get("bytes"), int)
        or isinstance(result.get("bytes"), bool)
        or result.get("bytes", -1) < 0
    ):
        return _receipt("webhook-sandbox", "invalid", "BLOCKED", {"reason": "malformed_source_result"})
    accepted = result["accepted"]
    return _receipt("webhook-sandbox", "accepted" if accepted else "rejected", "PASS" if accepted else "FAIL", result)


def adapt_mock(result: Any) -> AdapterReceipt:
    required = {"project", "status", "reason", "record", "responses", "evidence_sha256"}
    if not isinstance(result, dict) or not required <= set(result) or result.get("project") != "api-contract-mock-server":
        return _receipt("api-contract-mock-server", "invalid", "BLOCKED", {"reason": "malformed_source_result"})
    status = result.get("status")
    mapping = {"passed": "PASS", "failed": "FAIL", "blocked": "BLOCKED"}
    if status not in mapping:
        return _receipt("api-contract-mock-server", "invalid", "BLOCKED", {"reason": "malformed_source_result"})
    return _receipt("api-contract-mock-server", status, mapping[status], result)
