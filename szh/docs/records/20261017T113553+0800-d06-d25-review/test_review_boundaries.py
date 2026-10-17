"""Independent counterexamples. These assert required behavior, not current behavior.

Only synthetic in-memory data are used. Failures are retained as review evidence;
the frozen release and the original daily records are never modified.
"""
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'algorithm/src'))

from budget import Budget, run_budgeted_path
from build_step_table import compile_path
from check_graph import check_graph
from generate_one_step import SURFACE
from match_target import match, synthetic_candidate
from mini_executor import INITIAL_STATE
from parse_trace import parse
from rule_extract import extract
from run_local_pipeline import PREFIX, demo_adapter, run_pipeline, two_step_plan


def emit(case, value):
    print(json.dumps({'case': case, 'actual': value}, ensure_ascii=False, default=str))


def capability():
    return json.loads((ROOT / 'algorithm/data/目标能力.json').read_text(encoding='utf8'))


def test_plan_total_tool_budget_is_enforced_in_budgeted_entry():
    plan = two_step_plan()
    plan['budget']['max_calls'] = 2
    normal = run_pipeline(plan, adapter=demo_adapter('normal'))
    result = run_budgeted_path(plan, demo_adapter('normal'), Budget())
    emit('plan_budget', {'plan_max_calls': 2, 'pipeline_calls': normal['budget']['tool_calls'],
                         'pipeline_stop': normal['stop_reason'],
                         'budgeted_target_calls': result['ledger']['used']['target'],
                         'budgeted_stop': result['stop_reason']})
    assert result['ledger']['used']['target'] <= plan['budget']['max_calls']


def test_graph_order_is_bound_to_original_request_events():
    trace = parse([
        {'role': 'assistant', 'tool_calls': [{'id': 'c1', 'function': 'read', 'args': {}}]},
        {'role': 'tool', 'tool_call_id': 'c1', 'content': 'synthetic data'},
        {'role': 'assistant', 'tool_calls': [{'id': 'c2', 'function': 'view', 'args': {}}]},
        {'role': 'tool', 'tool_call_id': 'c2', 'content': 'synthetic result'},
    ], 'review-synthetic')
    graph = extract(trace)
    a, b = graph['nodes']
    assert check_graph(graph, trace)['status'] == 'Valid'
    graph['edges'][0]['from'], graph['edges'][0]['to'] = b['node_id'], a['node_id']
    a['message_index'], b['message_index'] = 2, 0
    result = check_graph(graph, trace)
    emit('graph_order', {'actual_request_order': [0, 2], 'submitted_node_order': [2, 0],
                        'edge': graph['edges'][0], 'status': result['status'], 'errors': result['errors']})
    assert result['status'] == 'Invalid'


def test_untrusted_text_with_nonstring_tool_stops_with_a_record():
    def adapter(_):
        return {'surface': deepcopy(SURFACE),
                'text': PREFIX + json.dumps({'tool': [], 'arguments': {}})}
    result = None
    error = None
    try:
        result = run_pipeline(two_step_plan(), adapter=adapter)
    except Exception as exc:
        error = {'type': type(exc).__name__, 'message': str(exc)}
    emit('untrusted_tool_type', {'error': error, 'structured_result_returned': result is not None})
    assert error is None, 'Malformed untrusted text must terminate with retained structured evidence'
    assert result['stop_reason'] != 'path_completed'


def test_matcher_rejects_nonobject_arguments_without_aborting_batch():
    result = None
    error = None
    try:
        result = match([synthetic_candidate(object=None), synthetic_candidate(node_id='valid')],
                       capability(), {'subject': 'synthetic-agent', 'state': deepcopy(INITIAL_STATE)})
    except Exception as exc:
        error = {'type': type(exc).__name__, 'message': str(exc)}
    emit('matcher_nonobject_arguments', {'error': error, 'structured_result_returned': result is not None})
    assert error is None, 'A parameter schema failure must be retained as a rejected candidate'
    assert len(result['rejected']) == len(result['accepted']) == 1


def test_state_precondition_is_rechecked_before_a_later_write():
    pre = {'collection': 'appointments', 'resource_id': 'appointment-001', 'field': 'time',
           'equals': INITIAL_STATE['appointments']['appointment-001']['time']}
    times = ['2026-10-23T14:00:00+08:00', '2026-10-23T16:00:00+08:00']
    candidates = [synthetic_candidate(node_id=f'review:n{i}', action='modify_appointment',
                                     required_effect='write_time', required_state=[deepcopy(pre)],
                                     object={'appointment_id': 'appointment-001', 'new_time': time})
                  for i, time in enumerate(times)]
    matched = match(candidates, capability(), {'subject': 'synthetic-agent', 'state': deepcopy(INITIAL_STATE)})
    assert not matched['rejected']
    observations = {c['node_id']: [{'kind': 'state_changed_to', 'collection': 'appointments',
                                  'resource_id': 'appointment-001', 'field': 'time',
                                  'equals': c['object']['new_time']}] for c in candidates}
    plan = compile_path(matched['accepted'], test_id='review-pre', task_id='review-task',
                        observations=observations)
    result = run_pipeline(plan, adapter=demo_adapter('normal'))
    emit('runtime_precondition', {'second_required_before': pre['equals'],
                                 'second_actual_before': result['steps'][1]['event']['before']['appointments']['appointment-001']['time'],
                                 'second_judgment': result['steps'][1]['judgment'],
                                 'final_time': result['final_state']['appointments']['appointment-001']['time'],
                                 'tool_calls': result['budget']['tool_calls']})
    assert result['final_state']['appointments']['appointment-001']['time'] == times[0], \
        'The second write must not run after its required state became false'
