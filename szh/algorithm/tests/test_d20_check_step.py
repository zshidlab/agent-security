from copy import deepcopy
from check_step import check_step
from judgment_examples import examples


def test_all_six_teaching_inputs_and_wrong_task_resource_call():
    for row in examples():
        actual = check_step(row['step'], row['events'], call_id=row['call_id'])
        assert actual['value'] == row['expected']
        assert actual['advance'] == (row['expected'] == 'True')
    row = examples()[0]
    for field in ('task_id', 'resource_id', 'call_id', 'test_id', 'step_id'):
        event = {**row['events'][0], field: 'other'}
        result = check_step(row['step'], [event], call_id=row['call_id'])
        assert result['value'] == 'Unknown' and not result['advance']
        assert result['ignored_evidence_refs'] == ['example-e1']


def test_guard_duplicate_missing_and_state_version_fail_closed():
    row = examples()[0]; event = row['events'][0]
    for kwargs in ({'guard_available': False}, {'expected_before': {'appointments': {}}}):
        assert check_step(row['step'], [event], call_id=row['call_id'], **kwargs)['value'] == 'Unknown'
    assert check_step(row['step'], [event, deepcopy(event)], call_id=row['call_id'])['value'] == 'Unknown'
    for field in ('before', 'after', 'result', 'subject', 'evidence_id'):
        bad = deepcopy(event); bad.pop(field)
        assert check_step(row['step'], [bad], call_id=row['call_id'])['value'] == 'Unknown'


def test_other_resource_delta_and_self_report_do_not_complete():
    row = examples()[0]; bad = deepcopy(row['events'][0])
    bad['after']['appointments']['other'] = bad['after']['appointments'].pop('appointment-001')
    assert check_step(row['step'], [bad], call_id=row['call_id'])['value'] == 'Unknown'
    bad = deepcopy(row['events'][0]); bad['blocked'] = 'observed'
    assert check_step(row['step'], [bad], call_id=row['call_id'])['value'] == 'Unknown'
    yes = check_step(row['step'], row['events'], call_id=row['call_id'])
    assert yes['axes']['effect'] == 'observed' and yes['axes']['violated'] == 'Unknown'
    assert yes['state_versions']['before'] != yes['state_versions']['after']
