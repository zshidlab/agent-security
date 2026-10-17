# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:59:28.751716+08:00 | `python -B scripts/build_demo_release.py --output algorithm/release/演示版` | exit 0 | command-01.json

- 2026-10-17T03:59:32.103299+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d25_demo_release.py -q` | exit 1 | command-02.json

- 2026-10-17T03:59:57.389934+08:00 | `git diff --check -- .` | exit 0 | command-03.json

- 2026-10-17T03:59:57.449731+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-04.json
