# D02 checks

## Contract

Pre: D01 scope. Goal: provide deterministic credential-free reply model and importable environment. Invariant: synthetic=true is required; no credentials or external calls. Observe: valid request returns fixed reply; missing/non-synthetic requests are rejected. Post: D03 consumes fixed-reply-1.0.

## Acceptance

| Check | Expected | Actual | Evidence | Result |
|---|---|---|---|---|
| Source fields and task plan | A:N and DOCX source excerpt unchanged | Source checker passed | `python -B scripts/check_workspace.py --sources` | PASS |
| Planned deliverables | Each listed file exists and is non-empty | All 5 deliverables present | `python -B scripts/check_workspace.py --day D02 --deliverables` | PASS |
| Behavior or document review | 4 passed | 4 passed | `outputs.json` and command output | PASS |
| Evidence axes | request/attempt/blocked/effect/violated retained; unavailable Hard Observable stays Unknown | Recorded in output/trace artifacts | `outputs.json`, algorithm fixtures | PASS |

## Limits

All observations are local synthetic/mock behavior. They do not establish real attack success, model quality, or vehicle safety. B/C interface acceptance remains pending confirmation.
