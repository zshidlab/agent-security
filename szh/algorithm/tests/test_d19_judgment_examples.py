import json
from judgment_examples import examples
from build_step_table import observe_post
from reference_graphs import ROOT


def test_completed_and_refusal_are_supported_by_actual_local_behavior():
    rows = {r['example_id']: r for r in examples()}
    yes = rows['completed']; no = rows['explicit_refusal']
    assert observe_post(yes['step'], yes['events'][0]) == yes['expected'] == 'True'
    refusal = no['events'][0]
    assert refusal['blocked'] == 'observed' and refusal['error']
    assert refusal['before'] == refusal['after']
    assert observe_post(no['step'], refusal) == no['expected'] == 'False'


def test_missing_conflicting_identity_and_result_inputs_explain_unknown():
    rows = {r['example_id']: r for r in examples()}
    text = rows['text_only']
    assert observe_post(text['step'], text['events'][0]) == 'Unknown'
    a, b = rows['conflicting_states']['events']
    assert a['call_id'] == b['call_id'] and a['sequence'] == b['sequence'] and a['after'] != b['after']
    identity = rows['identity_mismatch']
    assert identity['events'][0]['subject'] != identity['step']['constraint_instance']['subject']
    missing = rows['missing_result']
    assert observe_post(missing['step'], missing['events'][0]) == 'Unknown'
    assert all(rows[k]['expected'] == 'Unknown' for k in ('text_only', 'conflicting_states', 'identity_mismatch', 'missing_result'))


def test_saved_examples_reproduce_generator_and_keep_evidence_references():
    saved = [json.loads(line) for line in (ROOT / 'data/阶段判断示例.jsonl').read_text(encoding='utf8').splitlines()]
    assert saved == examples()
    for row in saved:
        assert row['evidence_refs'] == [e['evidence_id'] for e in row['events']]
        assert row['required_observation'] and row['reason'] and row['task_id'] and row['resource_id']
