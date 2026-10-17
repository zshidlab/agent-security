"""Observe integration boundaries using the frozen D25 package alone.

Exit zero means the observations were saved, not that acceptance passed.
"""
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE = ROOT / 'algorithm/release/演示版'
sys.path.insert(0, str(PACKAGE / 'src'))

import budget
import build_step_table
import check_step
import match_target
import retry_policy
import run_local_pipeline
from mini_executor import INITIAL_STATE


def main():
    sys.stdout.reconfigure(encoding='utf8')
    plan = run_local_pipeline.two_step_plan()
    plan['budget']['max_calls'] = 2
    limited = budget.run_budgeted_path(plan, run_local_pipeline.demo_adapter('normal'), budget.Budget())

    views = []
    def adapter(view):
        views.append(deepcopy(view))
        return run_local_pipeline.demo_adapter('normal')(view)
    normal = budget.run_budgeted_path(run_local_pipeline.two_step_plan(), adapter, budget.Budget())
    local = run_local_pipeline.run_pipeline(run_local_pipeline.two_step_plan(),
                                           adapter=run_local_pipeline.demo_adapter('normal'))

    capability = json.loads((PACKAGE / 'data/目标能力.json').read_text(encoding='utf8'))
    pre = {'collection': 'appointments', 'resource_id': 'appointment-001', 'field': 'time',
           'equals': INITIAL_STATE['appointments']['appointment-001']['time']}
    times = ['2026-10-23T14:00:00+08:00', '2026-10-23T16:00:00+08:00']
    candidates = [match_target.synthetic_candidate(node_id=f'frozen-review:n{i}', action='modify_appointment',
                    required_effect='write_time', required_state=[deepcopy(pre)],
                    object={'appointment_id': 'appointment-001', 'new_time': time}) for i, time in enumerate(times)]
    accepted = match_target.match(candidates, capability, {'subject': 'synthetic-agent', 'state': INITIAL_STATE})['accepted']
    observations = {c['node_id']: [{'kind': 'state_changed_to', 'collection': 'appointments',
                                  'resource_id': 'appointment-001', 'field': 'time',
                                  'equals': c['object']['new_time']}] for c in candidates}
    path = build_step_table.compile_path(accepted, test_id='frozen-review-pre', task_id='frozen-review-task',
                                        observations=observations)
    conflict = budget.run_budgeted_path(path, run_local_pipeline.demo_adapter('normal'), budget.Budget())
    last = conflict['steps'][1]['attempts'][0]
    modules = [budget, build_step_table, check_step, match_target, retry_policy, run_local_pipeline]
    result = {'schema_version': 'frozen-integration-review-1.0', 'timestamp': datetime.now().astimezone().isoformat(),
              'scope': 'Frozen local_mock package; synthetic state only; no model call',
              'module_paths': {m.__name__: m.__file__ for m in modules},
              'plan_budget': {'required_max_calls': 2, 'actual_target_calls': limited['ledger']['used']['target'],
                              'actual_stop': limited['stop_reason'], 'acceptance_passed': limited['ledger']['used']['target'] <= 2},
              'visible_history': {'generation_calls': len(views),
                                  'budgeted_second_step_history': views[1]['visible_history'],
                                  'local_second_step_history': local['steps'][1]['candidate']['generation_view']['visible_history'],
                                  'budgeted_stop': normal['stop_reason'],
                                  'acceptance_passed': bool(views[1]['visible_history'])},
              'runtime_pre': {'second_pre_requires': pre['equals'],
                              'second_actual_before': last['event']['before']['appointments']['appointment-001']['time'],
                              'second_actual_after': last['event']['after']['appointments']['appointment-001']['time'],
                              'second_judgment': last['observations'][0]['judgment'],
                              'acceptance_passed': conflict['final_state']['appointments']['appointment-001']['time'] == times[0]}}
    with (HERE / 'frozen-integration.json').open('x', encoding='utf8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
