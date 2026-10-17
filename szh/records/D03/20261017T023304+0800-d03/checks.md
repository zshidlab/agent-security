# D03 checks

## Contract

Pre: D02 fixed-reply-1.0. Goal: freeze trace-1.0 and validation fixtures. Invariant: event_id, turn_id and message_id are unique; request/result tool_call_id linkage is explicit. Observe: valid trace validates and malformed/duplicate fixtures fail with paths. Post: D04 event records use versioned axes.

## Acceptance

| Check | Expected | Actual | Evidence | Result |
|---|---|---|---|---|
| Source fields and task plan | A:N and DOCX source excerpt unchanged | Source checker passed | `python -B scripts/check_workspace.py --sources` | PASS |
| Planned deliverables | Each listed file exists and is non-empty | All 5 deliverables present | `python -B scripts/check_workspace.py --day D03 --deliverables` | PASS |
| Behavior or document review | 3 passed | 3 passed | `outputs.json` and command output | PASS |
| Evidence axes | request/attempt/blocked/effect/violated retained; unavailable Hard Observable stays Unknown | Recorded in output/trace artifacts | `outputs.json`, algorithm fixtures | PASS |

## Limits

All observations are local synthetic/mock behavior. They do not establish real attack success, model quality, or vehicle safety. B/C interface acceptance remains pending confirmation.
