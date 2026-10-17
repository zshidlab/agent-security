import copy
from parse_trace import parse
from rule_extract import extract
from check_graph import check_graph

def sample():
    t=parse([{'role':'assistant','tool_calls':[{'id':'c','function':'read','args':{}}]},
             {'role':'tool','tool_call_id':'c','content':'resource-a'},
             {'role':'assistant','tool_calls':[{'id':'d','function':'send','args':{'body':'resource-a'}}]},
             {'role':'tool','tool_call_id':'d','content':'ok'}],'s')
    return t,extract(t)

def test_supported_dependency_and_empty_support_reverts_to_candidate():
    t,g=sample();a,b=g['nodes']
    edge={'from':a['node_id'],'to':b['node_id'],'kind':'dependency','evidence_refs':[],'quote':'resource-a'}
    g['edges'].append(edge);r=check_graph(g,t)
    assert r['status']=='Candidate' and r['graph']['edges'][-1]['status']=='candidate'
    edge['evidence_refs']=a['result_event_ids'];assert check_graph(g,t)['status']=='Valid'
    edge['evidence_refs']=b['result_event_ids'];assert check_graph(g,t)['status']=='Candidate'

def test_duplicate_node_empty_node_evidence_wrong_direction():
    t,g=sample();bad=copy.deepcopy(g);bad['nodes'].append(copy.deepcopy(bad['nodes'][0]))
    assert any(e['code']=='duplicate_or_empty_node' for e in check_graph(bad,t)['errors'])
    bad=copy.deepcopy(g);bad['nodes'][0]['evidence_refs']=[];assert check_graph(bad,t)['status']=='Invalid'
    g['edges'][0]['from'],g['edges'][0]['to']=g['edges'][0]['to'],g['edges'][0]['from']
    assert any(e['code']=='wrong_direction_or_parallel' for e in check_graph(g,t)['errors'])

def test_wrong_action_and_foreign_event_rejected():
    t,g=sample();g['nodes'][0]['action']='delete';g['nodes'][0]['evidence_refs'].append('other:e99')
    codes={e['code'] for e in check_graph(g,t)['errors']}
    assert {'request_action_mismatch','missing_or_foreign_evidence'}<=codes
