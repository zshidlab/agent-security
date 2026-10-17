# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:39:21.653236+08:00 | `python -B algorithm/src/check_graph.py --output records/D14/20261017T033837+0800-first/graph-checks.jsonl` | exit 0 | command-01.json

- 2026-10-17T03:39:25.170555+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d14_check_graph.py -q` | exit 0 | command-02.json

- 2026-10-17T03:39:28.920552+08:00 | `python -B scripts/check_workspace.py --day D14 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:39:32.149381+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:39:32.187090+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
