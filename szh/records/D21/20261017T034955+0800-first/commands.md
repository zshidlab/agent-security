# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:50:11.967207+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d21_generate_one_step.py -q` | exit 0 | command-01.json

- 2026-10-17T03:50:15.777300+08:00 | `python -B algorithm/src/generate_one_step.py --output records/D21/20261017T034955+0800-first/candidates.jsonl` | exit 0 | command-02.json

- 2026-10-17T03:50:19.180964+08:00 | `python -B scripts/check_workspace.py --day D21 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:50:22.422176+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:50:22.464341+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
