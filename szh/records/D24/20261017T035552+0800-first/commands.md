# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:56:03.311653+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d24_budget.py algorithm/tests/test_d23_retry_policy.py algorithm/tests/test_d22_local_pipeline.py -q` | exit 0 | command-01.json

- 2026-10-17T03:56:23.809260+08:00 | `python -B algorithm/src/budget.py --output records/D24/20261017T035552+0800-first/budget-runs.jsonl` | exit 1 | command-02.json

- 2026-10-17T03:56:53.484583+08:00 | `git diff --check -- .` | exit 0 | command-03.json

- 2026-10-17T03:56:53.526935+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-04.json
