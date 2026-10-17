# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:41:29.400808+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d16_capability.py -q` | exit 0 | command-01.json

- 2026-10-17T03:41:33.066367+08:00 | `python -B scripts/check_workspace.py --day D16 --deliverables` | exit 0 | command-02.json

- 2026-10-17T03:41:36.457724+08:00 | `git diff --check -- .` | exit 0 | command-03.json

- 2026-10-17T03:41:36.507247+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-04.json
