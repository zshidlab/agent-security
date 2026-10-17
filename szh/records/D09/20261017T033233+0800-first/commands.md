# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:32:47.272866+08:00 | `python -B scripts/freeze_annotation_first.py` | exit 0 | command-01.json

- 2026-10-17T03:32:50.667145+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d09_annotation_refs.py -q` | exit 0 | command-02.json

- 2026-10-17T03:32:54.685024+08:00 | `python -B scripts/check_workspace.py --day D09 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:32:58.250602+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:32:58.298363+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
