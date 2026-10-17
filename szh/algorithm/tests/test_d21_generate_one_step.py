from copy import deepcopy
import pytest
from build_step_table import synthetic_plan
from generate_one_step import generate_one_step, current_view, fixed_reply, SURFACE


def test_one_accepted_low_trust_candidate_without_hidden_state():
    step = synthetic_plan()['steps'][0]
    history = [{'visibility': 'hidden', 'text': 'HIDDEN-MARKER'},
               {'visibility': 'visible', 'role': 'external', 'text': 'synthetic data', 'after': 'HIDDEN-MARKER'}]
    captured = []
    def adapter(view):
        captured.append(view); return fixed_reply(view)
    row = generate_one_step(step, history, SURFACE, adapter, candidate_id='c1')
    assert row['status'] == 'accepted' and row['candidate_id'] == 'c1'
    assert len(captured) == 1 and 'HIDDEN-MARKER' not in str(captured)
    assert captured[0]['allowed_tools'] == ['modify_appointment']
    assert row['axes']['effect'] == row['axes']['violated'] == 'Unknown'


def test_rejected_raw_candidates_are_retained_with_ids():
    step = synthetic_plan()['steps'][0]
    replies = ['bad JSON', {'surface': {**SURFACE, 'resource_id': 'system-permission-file'}, 'text': 'x'},
               {'surface': SURFACE, 'text': 'x', 'effect': 'success'}, [fixed_reply(current_view(step, [], SURFACE))]]
    for i, reply in enumerate(replies):
        row = generate_one_step(step, [], SURFACE, lambda _: deepcopy(reply), candidate_id=f'c{i}')
        assert row['status'] == 'rejected' and row['reasons'] and row['raw_reply'] == reply


def test_surface_validation_and_adapter_failure():
    step = synthetic_plan()['steps'][0]
    with pytest.raises(ValueError): current_view(step, [], {**SURFACE, 'trust': 'system'})
    def unavailable(_): raise RuntimeError('synthetic adapter unavailable')
    row = generate_one_step(step, [], SURFACE, unavailable, candidate_id='c-error')
    assert row['status'] == 'rejected' and row['reasons'] == ['adapter_error:RuntimeError']
