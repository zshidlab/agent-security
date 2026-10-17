# D05 checks

## Contract

Pre: D01-D04 deliverables. Goal: run portable booking smoke. Invariant: missing fields stop before tool calls and no output file is produced; reset restores initial time. Observe: request/execution/observation/reset events and explicit error path. Post: D06 can use demo-1.0 evidence.

## Acceptance

| Check | Expected | Actual | Evidence | Result |
|---|---|---|---|---|
| Source fields and task plan | A:N and DOCX source excerpt unchanged | Source checker passed | `python -B scripts/check_workspace.py --sources` | PASS |
| Planned deliverables | Each listed file exists and is non-empty | All 2 deliverables present | `python -B scripts/check_workspace.py --day D05 --deliverables` | PASS |
| Behavior or document review | 2 passed; portable clean-copy valid run exit 0 with 13 events; missing-field run exit 2. | 2 passed; portable clean-copy valid run exit 0 with 13 events; missing-field run exit 2. | `outputs.json` and command output | PASS |
| Evidence axes | request/attempt/blocked/effect/violated retained; unavailable Hard Observable stays Unknown | Recorded in output/trace artifacts | `outputs.json`, algorithm fixtures | PASS |

## Limits

All observations are local synthetic/mock behavior. They do not establish real attack success, model quality, or vehicle safety. B/C interface acceptance remains pending confirmation.
