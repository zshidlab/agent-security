# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:42:30.686053+08:00 | `python -B algorithm/src/match_target.py --output records/D17/20261017T034215+0800-first/matches.json` | exit 0 | command-01.json

- 2026-10-17T03:42:34.146028+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d17_match_target.py -q` | exit 0 | command-02.json

- 2026-10-17T03:42:37.921473+08:00 | `python -B scripts/check_workspace.py --day D17 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:42:41.423757+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:42:41.466716+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
