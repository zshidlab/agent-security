"""Sequential CLI acceptance with per-day retained stdout and generated artifacts."""
import json
from pathlib import Path
import sys
import day_run

ROOT=Path(__file__).resolve().parents[1]


def main():
    state=json.loads((ROOT/'records/revalidation-current.json').read_text(encoding='utf8'))
    modules={14:'check_graph',17:'match_target',18:'build_step_table',19:'judgment_examples',
             20:'check_step',21:'generate_one_step',22:'run_local_pipeline',23:'retry_policy',24:'budget'}
    for day,module in modules.items():
        record=ROOT/state['records'][str(day)]
        out=record/(module+('.json' if day in (17,18) else '.jsonl'))
        if out.exists():raise RuntimeError('Do not overwrite existing run artifacts')
        code=day_run.command(record,[sys.executable,'-B',f'algorithm/src/{module}.py','--output',str(out.relative_to(ROOT))])
        if code:return code
    return 0


if __name__=='__main__':raise SystemExit(main())
