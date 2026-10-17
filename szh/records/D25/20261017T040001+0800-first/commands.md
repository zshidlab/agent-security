# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T04:00:17.380527+08:00 | `python -B -c "from pathlib import Path; import shutil; r=Path.cwd().resolve(); s=(r/'algorithm/release/演示版').resolve(); d=(r/'records/D25/20261017T035735+0800-first/failed-release').resolve(); assert s.is_relative_to(r) and d.is_relative_to(r) and s.is_dir() and not d.exists(); shutil.move(str(s),str(d)); print('Failed package preserved at',d.relative_to(r))"` | exit 0 | command-01.json

- 2026-10-17T04:00:20.471136+08:00 | `python -B scripts/build_demo_release.py --output algorithm/release/演示版` | exit 0 | command-02.json

- 2026-10-17T04:00:23.627012+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d25_demo_release.py -q` | exit 0 | command-03.json

- 2026-10-17T04:00:28.537635+08:00 | `python -B scripts/verify_demo_release.py --package algorithm/release/演示版 --output records/D25/20261017T040001+0800-first/isolated-demo` | exit 0 | command-04.json

- 2026-10-17T04:00:52.861035+08:00 | `git diff --check -- .` | exit 0 | command-05.json

- 2026-10-17T04:00:52.904043+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-06.json
