# D05 commands

- Working directory: `E:/Vehicle-Agent-Security/agent-security/szh`
- Date: `2026-10-17`; Python: `3.12.7`; synthetic/local-only execution.
- `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d05_week1_smoke.py -q` -> exit `0`; result: 2 passed; portable clean-copy valid run exit 0 with 13 events; missing-field run exit 2..
- `python -B scripts/check_workspace.py --day D05 --deliverables` -> exit `0`.
- `python -B scripts/check_workspace.py --sources` -> exit `0` (source verification).
- Output and evidence paths are listed in `outputs.json`; no external service or vehicle was contacted.
