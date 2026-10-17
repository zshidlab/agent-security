# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:45:49.386700+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d18_step_table.py -q` | exit 1 | command-01.json

- 2026-10-17T03:46:00.301617+08:00 | `git diff --check -- .` | exit 0 | command-02.json

- 2026-10-17T03:46:00.358933+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-03.json
