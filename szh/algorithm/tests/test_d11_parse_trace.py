import json
from parse_trace import parse,parse_development
from group_split import load_development
from reference_graphs import ROOT

def request(cid='c',task=None):
    m={'role':'assistant','tool_calls':[{'id':cid,'function':'read','args':{'resource':'a'}}]}
    if task: m['task_id']=task
    return m

def reply(cid='c'):
    return {'role':'tool','tool_call_id':cid,'tool_call':{'id':cid,'function':'read','args':{'resource':'a'}},'content':'ok'}

def test_twenty_roundtrip_and_unique_event_ids():
    rs=parse_development();assert len(rs)==20
    for r,source in zip(rs,load_development()):
        original=json.loads((ROOT/source['local_file']).read_text(encoding='utf8'))
        assert [m['raw'] for m in r['messages']]==original
        assert len({e['event_id'] for e in r['events']})==len(r['events'])
        assert [m['original_index'] for m in r['messages']]==list(range(len(original)))

def test_request_return_separate_and_missing_preserved():
    assert parse([{'role':'assistant','tool_calls':None}],'null')['events']==[]
    r=parse([request(),reply(),{'role':'tool','state_delta':{'before':0,'after':1}}],'s')
    assert r['events'][0]['event_id']!=r['events'][1]['event_id']
    assert r['events'][0]['call_key']==r['events'][1]['call_key']
    assert any(e['kind']=='state_delta' for e in r['events'])
    assert parse([request()],'s')['events'][0]['missing_reason']=='missing_result'

def test_cross_task_and_duplicate_ids_fail_closed_without_dropping():
    r=parse([request(task='other'),reply()],'s','task')
    assert r['status']=='Invalid' and r['events'][1]['call_key'] is None
    r=parse([request(),request(),reply()],'s')
    assert len(r['messages'])==3 and r['status']=='Invalid'
    assert all(e['call_key'] is None for e in r['events'])
    r=parse([{'role':'user','message_id':'same'},{'role':'assistant','message_id':'same'}],'s')
    assert r['status']=='Invalid' and len(r['messages'])==2
