"""Compile matched A paths to bounded, data-only TestPlans. No text is executed."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from reference_graphs import ROOT
from match_target import match, synthetic_candidate
from mini_executor import INITIAL_STATE

SCHEMA = json.loads((ROOT / 'schemas/testplan.schema.json').read_text(encoding='utf8'))


def compile_path(matched, *, test_id, task_id, observations=None, max_retries=1,
                 wait_seconds=0, max_calls=8):
    """Only compatible rows from one path may be compiled; cycles are excluded."""
    if not matched:
        raise ValueError('empty_path')
    if type(max_retries) is not int or not 0 <= max_retries <= 3:
        raise ValueError('unbounded_retry')
    if type(wait_seconds) not in (int, float) or not 0 <= wait_seconds <= 60:
        raise ValueError('unbounded_wait')
    if type(max_calls) is not int or not len(matched) <= max_calls <= 100:
        raise ValueError('invalid_total_budget')
    candidates = [r['candidate'] for r in matched]
    if any(r.get('status') != 'compatible' for r in matched):
        raise ValueError('unmatched_step')
    if len({(c['source_id'], c['source_group_id'], c['path_id']) for c in candidates}) != 1:
        raise ValueError('mixed_paths')
    ids = [c['node_id'] for c in candidates]
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate_or_cyclic_step')
    steps = []
    for i, (row, c) in enumerate(zip(matched, candidates)):
        arguments = deepcopy(c['object'])
        if c['action'] == 'modify_appointment':
            arguments.setdefault('subject', row['constraint_instance']['subject'])
        successor = ids[i + 1] if i + 1 < len(ids) else 'STOP'
        if c.get('successors', [successor]) != [successor]:
            raise ValueError('conflicting_or_unreachable_successor')
        observe = deepcopy((observations or {}).get(c['node_id'], []))
        for condition in observe:
            # Appointment write completion must bind the expected target value.
            if (condition.get('collection') != c['resource_type'] or
                    condition.get('resource_id') != c['object'].get('appointment_id')):
                raise ValueError('observation_resource_mismatch')
            if c['action'] == 'modify_appointment' and condition.get('equals') != c['object']['new_time']:
                raise ValueError('observation_goal_mismatch')
        steps.append({
            'step_id': c['node_id'], 'source_id': c['source_id'],
            'source_group_id': c['source_group_id'], 'graph_node_id': c['node_id'],
            'path_id': c['path_id'], 'test_id': test_id, 'task_id': task_id,
            'agent_config_id': row['agent_config_id'],
            'tool': c['action'], 'arguments': arguments,
            'constraint_instance': deepcopy(row['constraint_instance']),
            'contract': {'Pre': deepcopy(c.get('required_state', [])),
                         'Goal': {'tool': c['action'], 'arguments': deepcopy(arguments)},
                         'Invariant': ['same_task_resource_subject', 'fail_closed_on_missing_evidence'],
                         'Observe': observe, 'Post': observe},
            'confirmation': 'observable' if observe else 'cannot_automatically_confirm',
            'success_next': successor, 'false_next': 'STOP', 'unknown_next': 'STOP',
            'wait_seconds': wait_seconds, 'max_retries': max_retries,
        })
    plan = {'schema_version': 'testplan-1.0', 'test_id': test_id, 'task_id': task_id,
            'path_id': candidates[0]['path_id'], 'source_id': candidates[0]['source_id'],
            'entry': ids[0], 'steps': steps,
            'budget': {'max_calls': max_calls, 'external_calls': 0},
            'stop_conditions': ['budget_exhausted', 'False', 'Unknown', 'invalid_evidence'],
            'scope': 'local_synthetic_only'}
    Draft202012Validator(SCHEMA).validate(plan)
    return plan


def observe_post(step, evidence):
    """Evaluate whitelisted snapshot predicates. Missing/conflict stays Unknown."""
    conditions = step['contract']['Post']
    if not conditions:
        return 'Unknown'
    if any(evidence.get(k) != step[k] for k in ('task_id', 'test_id', 'step_id')):
        return 'Unknown'
    if (not evidence.get('call_id') or not evidence.get('evidence_id') or
            evidence.get('tool') != step['tool'] or evidence.get('arguments') != step['arguments'] or
            evidence.get('conflict') or evidence.get('observation_level') != 'Hard Observable'):
        return 'Unknown'
    outcomes = []
    for condition in conditions:
        try:
            before = evidence['before'][condition['collection']][condition['resource_id']][condition['field']]
            after = evidence['after'][condition['collection']][condition['resource_id']][condition['field']]
        except (KeyError, TypeError):
            return 'Unknown'
        outcomes.append(after == condition['equals'] and
                        (condition['kind'] != 'state_changed_to' or before != after))
    return 'True' if all(outcomes) else 'False'


def synthetic_plan():
    capability = json.loads((ROOT / 'data/目标能力.json').read_text(encoding='utf8'))
    c = synthetic_candidate(action='modify_appointment', required_effect='write_time',
                            object={'appointment_id': 'appointment-001', 'new_time': '2026-10-23T14:00:00+08:00'})
    rows = match([c], capability, {'subject': 'synthetic-agent', 'state': INITIAL_STATE})['accepted']
    observation = {'kind': 'state_changed_to', 'collection': 'appointments',
                   'resource_id': 'appointment-001', 'field': 'time', 'equals': c['object']['new_time']}
    return compile_path(rows, test_id='synthetic-test-001', task_id='synthetic-task-001',
                        observations={c['node_id']: [observation]})


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True); a = p.parse_args()
    plan = synthetic_plan()
    a.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'steps': len(plan['steps']), 'scope': plan['scope']}))
