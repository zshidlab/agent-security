# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:52:14.964267+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d22_local_pipeline.py -q` | exit 0 | command-01.json

- 2026-10-17T03:52:28.838513+08:00 | `python -B algorithm/src/run_local_pipeline.py --output records/D22/20261017T035147+0800-first/runs.jsonl` | exit 0 | command-02.json

- 2026-10-17T03:52:32.286321+08:00 | `python -B scripts/check_workspace.py --day D22 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:52:35.610397+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:52:35.654169+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
