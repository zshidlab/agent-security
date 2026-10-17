# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:54:01.997470+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d23_retry_policy.py algorithm/tests/test_d22_local_pipeline.py -q` | exit 0 | command-01.json

- 2026-10-17T03:54:05.797487+08:00 | `python -B algorithm/src/retry_policy.py --output records/D23/20261017T035342+0800-first/retry-runs.jsonl` | exit 0 | command-02.json

- 2026-10-17T03:54:09.197726+08:00 | `python -B scripts/check_workspace.py --day D23 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:54:12.477923+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:54:12.518221+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
