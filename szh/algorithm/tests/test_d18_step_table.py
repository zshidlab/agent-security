from copy import deepcopy
import json
import pytest
from build_step_table import compile_path, synthetic_plan, observe_post
from match_target import match, synthetic_candidate
from mini_executor import MiniExecutor, INITIAL_STATE
from reference_graphs import ROOT


def test_actual_snapshot_completion_is_bound_to_task_and_resource():
    plan = synthetic_plan(); step = plan['steps'][0]; executor = MiniExecutor()
    event = executor.modify_appointment(**step['arguments'])
    evidence = {**event, 'arguments': event['request'], 'call_id': 'call-1', 'evidence_id': 'ev-1',
                'step_id': step['step_id'], 'test_id': plan['test_id'], 'task_id': plan['task_id'],
                'observation_level': 'Hard Observable'}
    assert observe_post(step, evidence) == 'True'
    assert observe_post(step, {**evidence, 'task_id': 'other'}) == 'Unknown'
    assert observe_post(step, {**evidence, 'after': {}}) == 'Unknown'
    assert observe_post(step, {**evidence, 'after': event['before']}) == 'False'
    assert observe_post(step, {**evidence, 'conflict': True}) == 'Unknown'


def test_no_observation_is_explicit_and_cannot_confirm():
    cap = json.loads((ROOT / 'data/目标能力.json').read_text(encoding='utf8'))
    rows = match([synthetic_candidate()], cap, {'subject': 'synthetic-agent', 'state': INITIAL_STATE})['accepted']
    step = compile_path(rows, test_id='t', task_id='task')['steps'][0]
    assert step['confirmation'] == 'cannot_automatically_confirm'
    assert observe_post(step, {'text': 'done'}) == 'Unknown'


def test_unbounded_retry_cycle_conflict_and_code_conditions_rejected():
    cap = json.loads((ROOT / 'data/目标能力.json').read_text(encoding='utf8'))
    rows = match([synthetic_candidate()], cap, {'subject': 'synthetic-agent', 'state': INITIAL_STATE})['accepted']
    for changes in ({'max_retries': -1}, {'max_retries': float('inf')}, {'wait_seconds': 61}, {'max_calls': 0}):
        with pytest.raises(ValueError): compile_path(rows, test_id='t', task_id='task', **changes)
    altered = deepcopy(rows); altered[0]['candidate']['successors'] = ['x', 'y']
    with pytest.raises(ValueError): compile_path(altered, test_id='t', task_id='task')
    with pytest.raises(ValueError): compile_path(rows + rows, test_id='t', task_id='task')
    with pytest.raises(ValueError): compile_path(rows, test_id='t', task_id='task', observations={'synthetic:n0': [{'eval': 'anything'}]})
