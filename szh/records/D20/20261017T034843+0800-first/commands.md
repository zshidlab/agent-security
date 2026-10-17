# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:48:58.876333+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d20_check_step.py algorithm/tests/test_d18_step_table.py algorithm/tests/test_d19_judgment_examples.py -q` | exit 0 | command-01.json

- 2026-10-17T03:49:02.888212+08:00 | `python -B algorithm/src/check_step.py --output records/D20/20261017T034843+0800-first/judgments.jsonl` | exit 0 | command-02.json

- 2026-10-17T03:49:06.156841+08:00 | `python -B scripts/check_workspace.py --day D20 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:49:09.572049+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:49:09.611668+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
