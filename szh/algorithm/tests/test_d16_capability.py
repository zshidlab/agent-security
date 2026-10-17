import copy,inspect,json
import pytest
from jsonschema import Draft202012Validator,ValidationError
from reference_graphs import ROOT
from mini_executor import MiniExecutor

def capability():return json.loads((ROOT/'data/目标能力.json').read_text(encoding='utf8'))

def test_four_real_functions_signature_and_schema():
    cap=capability();schema=json.loads((ROOT/'schemas/capability.schema.json').read_text(encoding='utf8'))
    Draft202012Validator(schema).validate(cap)
    assert len({t['name'] for t in cap['tools']})==4
    for t in cap['tools']:
        params=inspect.signature(getattr(MiniExecutor,t['name'])).parameters
        assert set(params)-{'self'}==set(t['parameters']['properties'])
        assert {n for n,p in params.items() if n!='self' and p.default is inspect.Parameter.empty}==set(t['parameters']['required'])
    bad=copy.deepcopy(cap);bad['tools'][0]['name']='cancel_appointment'
    with pytest.raises(ValidationError):Draft202012Validator(schema).validate(bad)
    assert not hasattr(MiniExecutor,'cancel_appointment')

def test_read_write_observables_and_permissions_match_runtime():
    e=MiniExecutor();before=copy.deepcopy(e.state)
    for t,args in [('read_notification',{'notification_id':'notification-maintenance-001'}),('read_file',{'file_id':'file-maintenance-001'}),('view_result',{'appointment_id':'appointment-001'})]:
        event=getattr(e,t)(**args);assert event['before']==event['after']==before and 'result' in event
    denied=e.modify_appointment('appointment-001','later',subject='other')
    assert denied['blocked']=='observed' and denied['after']==before
    changed=e.modify_appointment('appointment-001','later');assert changed['after']['appointments']['appointment-001']['time']=='later'
    assert changed['before']!=changed['after']
    missing=e.view_result('missing');assert 'error' in missing and missing['before']==missing['after']

def test_parameter_constraints_and_observation_limit():
    cap=capability();tool=next(t for t in cap['tools'] if t['name']=='modify_appointment')
    with pytest.raises(ValidationError):Draft202012Validator(tool['parameters']).validate({'appointment_id':'a','new_time':''})
    assert any('without state snapshots' in s for s in cap['observation_limits'])
