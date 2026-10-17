# Actual commands

CWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.

- 2026-10-17T03:36:24.356273+08:00 | `python -B algorithm/src/parse_trace.py --output records/D11/20261017T033607+0800-first/parsed.jsonl` | exit 0 | command-01.json

- 2026-10-17T03:36:27.778619+08:00 | `python -B -m pytest -p no:cacheprovider algorithm/tests/test_d11_parse_trace.py -q` | exit 0 | command-02.json

- 2026-10-17T03:36:31.643076+08:00 | `python -B scripts/check_workspace.py --day D11 --deliverables` | exit 0 | command-03.json

- 2026-10-17T03:36:35.369187+08:00 | `git diff --check -- .` | exit 0 | command-04.json

- 2026-10-17T03:36:35.406393+08:00 | `git status --short --ignored --untracked-files=all -- .` | exit 0 | command-05.json
