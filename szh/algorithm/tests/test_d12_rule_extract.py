from parse_trace import parse,parse_development
from rule_extract import extract

def q(cid='a'):return {'role':'assistant','tool_calls':[{'id':cid,'function':'read','args':{}}]}
def r(cid='a'):return {'role':'tool','tool_call_id':cid,'content':'done'}

def test_empty_missing_and_normal_return():
    assert extract(parse([],'empty'))['nodes']==[]
    g=extract(parse([q()],'s'));n=g['nodes'][0]
    assert n['missing_reason']=='missing_result' and n['result_event_ids']==[] and n['axes']['effect']=='Unknown'
    g=extract(parse([q(),r()],'s'));assert len(g['nodes'][0]['result_event_ids'])==1
    assert g['nodes'][0]['request_event_id']!=g['nodes'][0]['result_event_ids'][0]

def test_duplicate_request_or_returns_and_out_of_order():
    for ms in ([q(),q(),r()],[q(),r(),r()],[r(),q()]):
        g=extract(parse(ms,'s'));assert all(n['result_event_ids']==[] for n in g['nodes'])
        assert g['status']=='Invalid'

def test_all_development_requests_conserved_no_invented_dependencies():
    for t in parse_development():
        g=extract(t)
        assert len(g['nodes'])==sum(e['kind']=='request' for e in t['events'])
        assert all(e['kind']=='temporal' for e in g['edges'])
