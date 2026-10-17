# D04 checks

## Contract

Pre: D02/D03 interfaces. Goal: implement local dictionary executor. Invariant: only synthetic in-memory dictionaries are touched; blocked calls leave state unchanged. Observe: request/attempt/blocked/effect/violated plus before/after state diff. Post: D05 demo can invoke four tools and reset.

## Acceptance

| Check | Expected | Actual | Evidence | Result |
|---|---|---|---|---|
| Source fields and task plan | A:N and DOCX source excerpt unchanged | Source checker passed | `python -B scripts/check_workspace.py --sources` | PASS |
| Planned deliverables | Each listed file exists and is non-empty | All 1 deliverables present | `python -B scripts/check_workspace.py --day D04 --deliverables` | PASS |
| Behavior or document review | 2 passed | 2 passed | `outputs.json` and command output | PASS |
| Evidence axes | request/attempt/blocked/effect/violated retained; unavailable Hard Observable stays Unknown | Recorded in output/trace artifacts | `outputs.json`, algorithm fixtures | PASS |

## Limits

All observations are local synthetic/mock behavior. They do not establish real attack success, model quality, or vehicle safety. B/C interface acceptance remains pending confirmation.
