"""Evidence-aware graph checks; unsupported dependencies remain candidates."""
import argparse,copy,json
from pathlib import Path
from parse_trace import parse_development
from rule_extract import extract
from model_extract import run_extraction,fixture_reply

def proposal_graph(proposal, trace):
    events={e['event_id']:e for e in trace['events']};nodes=[]
    for s in proposal['steps']:
        q=next((events[r] for r in s['evidence_refs'] if r in events and events[r]['kind']=='request'),None)
        nodes.append({**copy.deepcopy(s),'source_id':proposal['source_id'],'task_id':trace['task_id'],
            'request_event_id':q['event_id'] if q else None,'message_index':q['message_index'] if q else None,
            'result_event_ids':[r for r in s['evidence_refs'] if r in events and events[r]['kind']=='result']})
    return {'schema_version':'candidate-graph-1.0','source_id':proposal['source_id'],'source_group_id':trace['source_group_id'],
            'task_id':trace['task_id'],'method':'offline_fixture','nodes':nodes,'edges':[],'status':trace['status']}

def check_graph(graph, trace):
    g=copy.deepcopy(graph);errors=[];warnings=[]
    if g.get('schema_version')!='candidate-graph-1.0': errors.append({'code':'schema_version','at':'graph'})
    if g.get('source_id')!=trace['source_id'] or g.get('task_id')!=trace['task_id']: errors.append({'code':'cross_source_task','at':'graph'})
    events={e['event_id']:e for e in trace['events']};nodes={}
    for n in g.get('nodes',[]):
        nid=n.get('node_id')
        if not nid or nid in nodes: errors.append({'code':'duplicate_or_empty_node','at':nid})
        nodes[nid]=n
        refs=n.get('evidence_refs',[])
        if not refs: errors.append({'code':'empty_node_evidence','at':nid})
        for r in refs:
            if r not in events or events[r]['task_id']!=trace['task_id']: errors.append({'code':'missing_or_foreign_evidence','at':nid,'ref':r})
        q=events.get(n.get('request_event_id'))
        if q is None or q['kind']!='request' or n.get('action')!=q['tool'] or n.get('object')!=q['args'] or q['event_id'] not in refs:
            errors.append({'code':'request_action_mismatch','at':nid})
        for r in n.get('result_event_ids',[]):
            e=events.get(r)
            if not e or not q or e['kind']!='result' or not q['call_key'] or q['call_key']!=e['call_key'] or e['message_index']<=q['message_index'] or e['missing_reason']:
                errors.append({'code':'result_binding','at':nid,'ref':r})
    edge_ids=set()
    for i,e in enumerate(g.get('edges',[])):
        eid=e.setdefault('edge_id',f'{g.get("source_id")}:edge{i:04}')
        if eid in edge_ids: errors.append({'code':'duplicate_edge','at':eid})
        edge_ids.add(eid)
        a,b=nodes.get(e.get('from')),nodes.get(e.get('to'))
        if not a or not b: errors.append({'code':'missing_endpoint','at':eid});continue
        ai,bi=a.get('message_index'),b.get('message_index')
        if ai is None or bi is None or ai>=bi:
            errors.append({'code':'wrong_direction_or_parallel','at':eid});e['status']='Invalid';continue
        if e.get('kind') not in ('temporal','dependency'): errors.append({'code':'unknown_edge_kind','at':eid});continue
        refs=e.get('evidence_refs',[])
        if e['kind']=='dependency':
            quote=e.get('quote','')
            valid=bool(refs and quote and all(r in a.get('result_event_ids',[]) and r in events and events[r]['message_index']<bi for r in refs))
            valid=valid and any(quote in json.dumps(events[r].get('content'),ensure_ascii=False) for r in refs) and quote in json.dumps(b.get('object'),ensure_ascii=False)
            e['status']='supported' if valid else 'candidate'
            if not valid: warnings.append({'code':'missing_dependency_support','at':eid,'refs':refs})
        elif not refs or any(r not in events for r in refs): errors.append({'code':'missing_temporal_evidence','at':eid})
        else: e['status']='supported_order_only'
    return {'schema_version':'graph-check-1.0','status':'Invalid' if errors or trace['status']=='Invalid' else 'Candidate' if warnings else 'Valid',
            'errors':errors,'warnings':warnings,'graph':g}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    reports=[]
    for t in parse_development():
        reports.append({'method':'rule','source_id':t['source_id'],**check_graph(extract(t),t)})
        reply=fixture_reply(t);proposal=run_extraction(t,lambda _:reply)['proposal']
        reports.append({'method':'offline_fixture_not_real_model','source_id':t['source_id'],**check_graph(proposal_graph(proposal,t),t)})
    a.output.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in reports),encoding='utf8')
    print(json.dumps({'checked':len(reports),'Invalid_retained':sum(r['status']=='Invalid' for r in reports),'real_model_graphs':0}))
