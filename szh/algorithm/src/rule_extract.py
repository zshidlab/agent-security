"""Minimal conservative rule baseline; one request creates one candidate."""
import argparse,json
from pathlib import Path
from parse_trace import parse_development

def extract(trace):
    events=trace['events'];nodes=[]
    for q in events:
        if q['kind']!='request': continue
        returns=[e for e in events if e['kind']=='result' and q['call_key'] and e['call_key']==q['call_key'] and e['task_id']==q['task_id'] and e['message_index']>q['message_index']]
        good=returns if len(returns)==1 and not returns[0]['missing_reason'] and not q['missing_reason'] else []
        reason=q['missing_reason'] or (None if good else 'missing_or_conflicting_result')
        nodes.append({'node_id':f'{trace["source_id"]}:n{len(nodes):02}', 'source_id':trace['source_id'],
            'task_id':trace['task_id'],'action':q['tool'],'object':q['args'],
            'request_event_id':q['event_id'],'result_event_ids':[e['event_id'] for e in good],
            'evidence_refs':[q['event_id']]+[e['event_id'] for e in good],
            'message_index':q['message_index'],'missing_reason':reason,
            'observation_level':'structured_trace' if good else 'request_only',
            'axes':{'request':'observed','attempt':'Unknown','blocked':'Unknown','effect':'Unknown','violated':'Unknown'},
            'contract':{'Pre':{'permission':'Unknown','state':'Unknown'},'Goal':{'tool':q['tool'],'object':q['args']},
                        'Invariant':['no privilege from low trust text'],'Observe':['independent state diff needed'],'Post':'Unknown'}})
    return {'schema_version':'candidate-graph-1.0','source_id':trace['source_id'],'source_group_id':trace['source_group_id'],
        'task_id':trace['task_id'],'method':'rule','nodes':nodes,
        'edges':[{'from':a['node_id'],'to':b['node_id'],'kind':'temporal','evidence_refs':[a['request_event_id'],b['request_event_id']]}
                 for a in nodes for b in nodes if a['message_index']<b['message_index']],
        'status':trace['status'],'issues':list(trace['issues']),
        'stop_reason':'empty_dialogue' if not trace['messages'] else 'no_tool_requests' if not nodes else 'extraction_only',
        'budget':{'external_execution':0}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    gs=[extract(t) for t in parse_development()]
    a.output.write_text(''.join(json.dumps(g,ensure_ascii=False)+'\n' for g in gs),encoding='utf8')
    a.output.with_suffix('.md').write_text('# Rule action/object table\n\n'+ '\n'.join(f"- {g['source_id']} / {n['node_id']}: {n['action']} {json.dumps(n['object'],ensure_ascii=False)}; {n['evidence_refs']}; {n['missing_reason'] or 'paired'}; effect Unknown" for g in gs for n in g['nodes'])+'\n',encoding='utf8')
    print(json.dumps({'graphs':len(gs),'nodes':sum(len(g['nodes']) for g in gs),'invalid_retained':sum(g['status']=='Invalid' for g in gs)}))
