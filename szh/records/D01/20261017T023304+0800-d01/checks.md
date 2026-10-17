# D01 checks

## Contract

Pre: D01 source fields and dependency-free workspace available. Goal: freeze A scope and contracts. Invariant: source DOCX/XLSX facts remain unchanged. Observe: document contains scope, threat boundary, contracts and axes. Post: D02 can consume the frozen scope.

## Acceptance

| Check | Expected | Actual | Evidence | Result |
|---|---|---|---|---|
| Source fields and task plan | A:N and DOCX source excerpt unchanged | Source checker passed | `python -B scripts/check_workspace.py --sources` | PASS |
| Planned deliverables | Each listed file exists and is non-empty | All 1 deliverables present | `python -B scripts/check_workspace.py --day D01 --deliverables` | PASS |
| Behavior or document review | Document review completed; no code behavior test required. | Document review completed; no code behavior test required. | `outputs.json` and command output | PASS |
| Evidence axes | request/attempt/blocked/effect/violated retained; unavailable Hard Observable stays Unknown | Recorded in output/trace artifacts | `outputs.json`, algorithm fixtures | PASS |

## Limits

All observations are local synthetic/mock behavior. They do not establish real attack success, model quality, or vehicle safety. B/C interface acceptance remains pending confirmation.
