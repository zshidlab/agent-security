# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:31:46.346534+08:00 | `python -B algorithm/src/reference_graphs.py` | exit 0 | command-01.json

- 2026-10-17T03:31:49.770712+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d08_reference_graphs.py -q` | exit 0 | command-02.json

- 2026-10-17T03:31:53.782859+08:00 | `python -B scripts/check_workspace.py --day D08 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:31:57.554808+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:31:57.598085+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
