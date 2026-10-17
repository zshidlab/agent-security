# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:25:08.483046+08:00 | `python -B algorithm/src/source_inventory.py` | exit 0 | command-01.json

- 2026-10-17T03:25:58.786235+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d06_source_inventory.py -q` | exit 1 | command-02.json

- 2026-10-17T03:26:01.310902+08:00 | `python -B scripts/check_workspace.py --day D06 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:26:21.862057+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:26:21.899650+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
