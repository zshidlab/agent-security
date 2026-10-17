# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:38:15.694743+08:00 | `python -B algorithm/src/model_extract.py --output records/D13/20261017T033733+0800-first/offline-calls.jsonl` | exit 0 | command-01.json

- 2026-10-17T03:38:19.017114+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d13_model_extract.py -q` | exit 0 | command-02.json

- 2026-10-17T03:38:22.679231+08:00 | `python -B scripts/check_workspace.py --day D13 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:38:25.869977+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:38:25.910801+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
