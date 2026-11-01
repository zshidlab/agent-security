# Actual commands

Progress writes deferred until final acceptance.

- 2026-10-30T18:34:58.736348+08:00 | `python -B scripts/build_demo_release.py --output algorithm/release/演示版-1.1` | exit 0 | command-01.json

- 2026-10-30T18:34:59.293017+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d25_demo_release.py -q` | exit 0 | command-02.json

- 2026-10-30T18:35:33.113521+08:00 | `python -B scripts/verify_demo_release.py --package algorithm/release/演示版-1.1 --output records/D25/20261030T182602+0800-revalidation/isolated-examples` | exit 0 | command-03.json

- 2026-10-30T18:35:34.519816+08:00 | `python -B scripts/probe_runtime.py --runtime algorithm/release/演示版-1.1/src --output records/D25/20261030T182602+0800-revalidation/frozen-integration.json` | exit 0 | command-04.json

- 2026-10-30T18:36:08.841687+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests -q` | exit 0 | command-05.json

- 2026-10-30T18:36:14.570269+08:00 | `python -B scripts/check_workspace.py --sources` | exit 0 | command-06.json

- 2026-10-30T18:42:18.187977+08:00 | `D:\anaconda\python.exe -B scripts/check_workspace.py --day D25 --deliverables` | exit 0 | command-07.json

- 2026-10-30T18:42:18.370395+08:00 | `git diff --check -- .` | exit 0 | command-08.json

- 2026-10-30T18:42:18.443414+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-09.json

- 2026-10-30T18:47:11.494135+08:00 | `git diff --check -- .` | exit 0 | command-10.json

- 2026-10-30T18:47:11.567943+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-11.json

- 2026-10-30T19:17:17.937494+08:00 | `D:\anaconda\python.exe -B scripts/check_workspace.py --sources` | exit 0 | command-12.json

- 2026-10-30T19:17:18.743311+08:00 | `git diff --check -- .` | exit 0 | command-13.json

- 2026-10-30T19:17:18.828411+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-14.json
