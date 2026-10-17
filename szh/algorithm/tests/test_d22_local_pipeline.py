import json
from mini_executor import MiniExecutor, INITIAL_STATE
from reference_graphs import ROOT
from run_local_pipeline import run_pipeline, two_step_plan, demo_adapter, RefusingExecutor


def test_ten_local_cases_terminate_and_never_advance_on_unknown_or_rejection():
    cases = [json.loads(x) for x in (ROOT / 'examples/local-cases.jsonl').read_text(encoding='utf8').splitlines()]
    shared = MiniExecutor(); run_ids = set()
    for case in cases:
        result = run_pipeline(two_step_plan(case['new_time']), adapter=demo_adapter(case['mode']),
                              executor=RefusingExecutor() if case['mode'] == 'refusal' else shared,
                              observer_mode=case.get('observer_mode', 'full'))
        assert result['stop_reason'] == case['expected_stop']
        assert len(result['steps']) == case['expected_steps']
        assert result['initial_state'] == INITIAL_STATE
        assert result['budget']['tool_calls'] <= 8 and result['budget']['external_calls'] == 0
        assert result['run_id'] not in run_ids; run_ids.add(result['run_id'])
        if result['stop_reason'] == 'path_completed':
            assert all(s['judgment']['value'] == 'True' for s in result['steps'])
            assert all(s['candidate'] and s['surface_read'] and s['event'] for s in result['steps'])
        else:
            assert not result['steps'][0].get('judgment') or not result['steps'][0]['judgment']['advance']


def test_generated_text_reaches_target_and_observation_is_independent():
    normal = run_pipeline(two_step_plan(), adapter=demo_adapter('normal'))
    no_action = run_pipeline(two_step_plan(), adapter=demo_adapter('no_action'))
    assert normal['final_state']['appointments'] != no_action['final_state']['appointments']
    assert no_action['final_state']['appointments'] == INITIAL_STATE['appointments']
    missing = run_pipeline(two_step_plan(), adapter=demo_adapter('normal'), observer_mode='missing_after')
    assert missing['final_state']['appointments'] != INITIAL_STATE['appointments']
    assert missing['stop_reason'] == 'Unknown'


def test_false_and_guard_unavailable_stop_before_next_step():
    plan = two_step_plan()
    # A repeated, unchanged target state is explicit non-completion of changed_to.
    from generate_one_step import SURFACE
    from copy import deepcopy
    def already_initial(view):
        command = deepcopy(view['current_goal']); command['arguments']['new_time'] = INITIAL_STATE['appointments']['appointment-001']['time']
        return {'surface': SURFACE, 'text': 'SYNTHETIC_REQUEST ' + json.dumps(command)}
    wrong = run_pipeline(plan, adapter=already_initial)
    assert len(wrong['steps']) == 1 and wrong['stop_reason'] == 'Unknown'  # Wrong arguments cannot be rebound.
    guard = run_pipeline(plan, adapter=demo_adapter('normal'), observer_mode='guard_unavailable')
    assert guard['stop_reason'] == 'Unknown' and len(guard['steps']) == 1
    refused = run_pipeline(plan, adapter=demo_adapter('normal'), executor=RefusingExecutor())
    assert refused['stop_reason'] == 'False' and len(refused['steps']) == 1
    assert refused['steps'][0]['event']['blocked'] == 'observed'
