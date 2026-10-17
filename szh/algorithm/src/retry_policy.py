"""Bounded single-step retries; Unknown permits observation only, never regeneration."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
from uuid import uuid4
from mini_executor import MiniExecutor
from generate_one_step import generate_one_step, SURFACE
from run_local_pipeline import local_target, demo_adapter, RefusingExecutor
from build_step_table import synthetic_plan
from judgment_examples import bind_event
from check_step import check_step
from budget import BudgetExceeded


def retry_step(step, adapter, *, executor=None, max_candidates=3, max_observations=3,
               max_tool_calls=8, observer_mode='full', recover_observation=False, run_id=None,
               meter=None, reset=True):
    for value, upper in ((max_candidates, 3), (max_observations, 3), (max_tool_calls, 100)):
        if type(value) is not int or not 1 <= value <= upper:
            raise ValueError('invalid_finite_budget')
    max_candidates = min(max_candidates, step['max_retries'] + 1)
    executor = executor or MiniExecutor()
    initial = executor.reset() if reset else deepcopy(executor.state)
    run_id = run_id or 'retry-' + uuid4().hex
    record = {'schema_version': 'retry-run-1.0', 'run_id': run_id, 'step_id': step['step_id'],
              'test_id': step['test_id'], 'task_id': step['task_id'], 'path_id': step['path_id'],
              'source_id': step['source_id'], 'initial_state': initial, 'attempts': [],
              'budget': {'generation_calls': 0, 'tool_calls': 0, 'observations': 0, 'external_calls': 0},
              'limits': {'candidates': max_candidates, 'observations_per_candidate': max_observations,
                         'tool_calls': max_tool_calls}, 'stop_reason': None}
    parent = None
    for number in range(1, max_candidates + 1):
        if meter:
            try: meter.start_round(step['step_id'])
            except BudgetExceeded as exc:
                record['stop_reason'] = 'budget:' + str(exc); break
        if record['budget']['tool_calls'] + 2 > max_tool_calls:
            record['stop_reason'] = 'tool_budget_exhausted'; break
        candidate_id = f'{run_id}:c{number}'
        def metered_adapter(view):
            return meter.call('generation', adapter, view, reference=candidate_id) if meter else adapter(view)
        candidate = generate_one_step(step, [], SURFACE, metered_adapter, candidate_id=candidate_id)
        if 'adapter_error:BudgetExceeded' not in candidate['reasons']:
            record['budget']['generation_calls'] += 1
        attempt = {'attempt_id': f'{run_id}:a{number}', 'parent_candidate_id': parent,
                   'candidate': candidate, 'surface_read': None, 'event': None,
                   'observations': [], 'classification': None}
        record['attempts'].append(attempt); parent = candidate['candidate_id']
        if 'adapter_error:BudgetExceeded' in candidate['reasons']:
            attempt['classification'] = 'not_generated_budget'; record['stop_reason'] = 'budget:generation'; break
        if candidate['status'] == 'rejected':
            if 'outside_authorized_control_surface' in candidate['reasons']:
                attempt['classification'] = 'safety_rejection'; record['stop_reason'] = 'safety_rejection'; break
            attempt['classification'] = 'technical_failure'
            continue
        executor.state[SURFACE['kind']][SURFACE['resource_id']][SURFACE['field']] = candidate['candidate']['text']
        try:
            read = (meter.call('target', executor.read_notification, SURFACE['resource_id'], reference=candidate_id)
                    if meter else executor.read_notification(SURFACE['resource_id']))
            attempt['surface_read'] = read; record['budget']['tool_calls'] += 1
            before = deepcopy(executor.state)
            event = (meter.call('target', local_target, executor, read['result']['body'], reference=candidate_id)
                     if meter else local_target(executor, read['result']['body']))
        except BudgetExceeded as exc:
            attempt['classification'] = 'unexecuted_candidate_budget'
            record['stop_reason'] = 'budget:' + str(exc); break
        call_id = f'{run_id}:call{number}'
        if event is not None:
            record['budget']['tool_calls'] += 1
            event = bind_event(step, event, evidence_id=f'{run_id}:e{number}')
            event.update(before=before, after=deepcopy(executor.state), call_id=call_id, run_id=run_id)
        attempt['event'] = deepcopy(event)
        for observation_number in range(1, max_observations + 1):
            evidence = deepcopy(event)
            if evidence is not None:
                evidence['evidence_id'] += f':o{observation_number}'
                if observer_mode == 'missing_after' and not (recover_observation and observation_number > 1):
                    evidence.pop('after', None)
                elif observation_number > 1:
                    # A fresh local snapshot without any intervening target call.
                    evidence['after'] = deepcopy(executor.state)
            def observe():
                return check_step(step, [evidence] if evidence is not None else [], call_id=call_id,
                                  expected_before=before, guard_available=observer_mode != 'guard_unavailable')
            try:
                judgment = meter.call('observation', observe, reference=call_id) if meter else observe()
            except BudgetExceeded as exc:
                record['stop_reason'] = 'budget:' + str(exc); break
            attempt['observations'].append({'observation_id': f'{run_id}:a{number}:o{observation_number}',
                                            'evidence': evidence, 'judgment': judgment})
            record['budget']['observations'] += 1
            if judgment['value'] != 'Unknown': break
        if record['stop_reason'] is not None: break
        last = attempt['observations'][-1]['judgment']
        if last['value'] == 'True':
            attempt['classification'] = 'local_completion'; record['stop_reason'] = 'completed'; break
        if last['value'] == 'Unknown':
            attempt['classification'] = 'insufficient_observation'; record['stop_reason'] = '观察不足'; break
        if event and event.get('blocked') == 'observed':
            attempt['classification'] = 'safety_rejection'; record['stop_reason'] = 'safety_rejection'; break
        attempt['classification'] = 'research_negative'
    if record['stop_reason'] is None: record['stop_reason'] = 'candidate_limit'
    record['final_state'] = deepcopy(executor.state)
    if meter: record['ledger'] = meter.snapshot()
    return record


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True); a = p.parse_args()
    step = synthetic_plan()['steps'][0]; step['max_retries'] = 2
    def timeout(_): raise TimeoutError('synthetic timeout signal; no blocking operation')
    rows = [retry_step(step, demo_adapter('normal'), executor=RefusingExecutor()),
            retry_step(step, demo_adapter('normal'), observer_mode='missing_after'),
            retry_step(step, timeout)]
    a.output.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf8')
    print(json.dumps({'sequences': len(rows), 'stop_reasons': [r['stop_reason'] for r in rows],
                      'generation_calls': [r['budget']['generation_calls'] for r in rows]}, ensure_ascii=False))
