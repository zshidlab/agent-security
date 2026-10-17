# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:46:24.656087+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d18_step_table.py -q` | exit 0 | command-01.json

- 2026-10-17T03:46:28.580090+08:00 | `python -B algorithm/src/build_step_table.py --output records/D18/20261017T034611+0800-first/testplan.json` | exit 0 | command-02.json

- 2026-10-17T03:46:31.912559+08:00 | `python -B scripts/check_workspace.py --day D18 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:46:35.150908+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:46:35.201372+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
