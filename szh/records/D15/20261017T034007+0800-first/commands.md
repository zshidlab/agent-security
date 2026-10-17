# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:40:23.901583+08:00 | `python -B algorithm/src/evaluate_graph.py` | exit 0 | command-01.json

- 2026-10-17T03:40:27.266285+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d15_graph_metrics.py -q` | exit 0 | command-02.json

- 2026-10-17T03:40:31.018734+08:00 | `python -B scripts/check_workspace.py --day D15 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:40:34.200764+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:40:34.244239+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
