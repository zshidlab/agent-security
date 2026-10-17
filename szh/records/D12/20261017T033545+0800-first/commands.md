# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:37:07.840318+08:00 | `python -B algorithm/src/rule_extract.py --output records/D12/20261017T033545+0800-first/rule-graphs.jsonl` | exit 0 | command-01.json

- 2026-10-17T03:37:11.640514+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d12_rule_extract.py -q` | exit 0 | command-02.json

- 2026-10-17T03:37:15.705201+08:00 | `python -B scripts/check_workspace.py --day D12 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:37:19.214309+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:37:19.265846+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
