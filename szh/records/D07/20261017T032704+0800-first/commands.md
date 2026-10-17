# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:27:40.917691+08:00 | `python -B algorithm/src/source_filter.py` | exit 0 | command-01.json

- 2026-10-17T03:27:41.526077+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d07_source_filter.py -q` | exit 0 | command-02.json

- 2026-10-17T03:27:42.635050+08:00 | `python -B scripts/check_workspace.py --day D07 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:27:43.164503+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:27:43.197967+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
