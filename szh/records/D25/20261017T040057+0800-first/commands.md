# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T04:01:10.658106+08:00 | `python -B -c "from pathlib import Path; import shutil; r=Path.cwd().resolve(); s=(r/'algorithm/release/演示版').resolve(); d=(r/'records/D25/20261017T040001+0800-first/encoding-release').resolve(); assert s.is_relative_to(r) and d.is_relative_to(r) and s.is_dir() and not d.exists(); shutil.move(str(s),str(d)); print('Previous package preserved at',d.relative_to(r))"` | exit 0 | command-01.json

- 2026-10-17T04:01:13.730325+08:00 | `python -B scripts/build_demo_release.py --output algorithm/release/演示版` | exit 0 | command-02.json

- 2026-10-17T04:01:16.902509+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests -q` | exit 0 | command-03.json

- 2026-10-17T04:01:23.025520+08:00 | `python -B scripts/verify_demo_release.py --package algorithm/release/演示版 --output records/D25/20261017T040057+0800-first/isolated-demo` | exit 0 | command-04.json

- 2026-10-17T04:01:57.332245+08:00 | `python -B scripts/check_workspace.py` | exit 0 | command-05.json

- 2026-10-17T04:02:00.841307+08:00 | `python -B scripts/check_workspace.py --day D25 --deliverables` | exit 0 | command-06.json

- 2026-10-17T04:02:04.211146+08:00 | `python -B scripts/check_workspace.py --sources` | exit 0 | command-07.json

- 2026-10-17T04:03:02.685086+08:00 | `git diff --check -- .` | exit 0 | command-08.json

- 2026-10-17T04:03:02.725731+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-09.json

- 2026-10-17T04:03:20.272073+08:00 | `python -B scripts/audit_d06_d25.py --output records/D25/20261017T040057+0800-first/session-audit.json` | exit 0 | command-10.json

- 2026-10-17T04:03:57.548383+08:00 | `git diff --check -- .` | exit 0 | command-11.json
