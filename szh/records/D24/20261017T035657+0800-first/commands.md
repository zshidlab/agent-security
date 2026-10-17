# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:57:10.819618+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d24_budget.py algorithm/tests/test_d23_retry_policy.py algorithm/tests/test_d22_local_pipeline.py -q` | exit 0 | command-01.json

- 2026-10-17T03:57:15.020244+08:00 | `python -B algorithm/src/budget.py --output records/D24/20261017T035657+0800-first/budget-runs.jsonl` | exit 0 | command-02.json

- 2026-10-17T03:57:18.302949+08:00 | `python -B scripts/check_workspace.py --day D24 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:57:21.543117+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:57:21.592119+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
