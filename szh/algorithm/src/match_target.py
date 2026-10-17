"""Hard constraints precede optional deterministic similarity ranking."""
import argparse,json
from pathlib import Path
from jsonschema import Draft202012Validator
from reference_graphs import ROOT
from mini_executor import INITIAL_STATE

def match(candidates, capability, context, score=None):
    tools={t['name']:t for t in capability['tools']};accepted=[];rejected=[]
    for candidate in candidates:
        c=dict(candidate);reasons=[];tool=tools.get(c.get('action'))
        if not tool: reasons.append('tool_not_available')
        else:
            args=c.get('object',{})
            if list(Draft202012Validator(tool['parameters']).iter_errors(args)): reasons.append('parameter_schema_incompatible')
            if c.get('resource_type')!=tool['resource_type']: reasons.append('resource_type_mismatch_or_unknown')
            if c.get('required_effect')!=tool['effect']: reasons.append('effect_semantics_mismatch_or_unknown')
            if not context.get('subject') or c.get('subject')!=context.get('subject'): reasons.append('subject_mismatch_or_unknown')
            if tool['permissions']['mode']=='subject_allowlist':
                if context.get('subject') not in tool['permissions']['subjects']: reasons.append('permission_denied')
                if args.get('subject',context.get('subject'))!=context.get('subject'): reasons.append('subject_argument_conflict')
            state=context.get('state');resource=args.get(tool['resource_parameter'])
            if not isinstance(state,dict) or resource not in state.get(tool['resource_type'],{}): reasons.append('resource_missing_or_state_unknown')
            for pre in c.get('required_state',[]):
                try: actual=state[pre['collection']][pre['resource_id']][pre['field']]
                except (TypeError,KeyError):reasons.append('state_precondition_unknown');continue
                if actual!=pre.get('equals'): reasons.append('state_precondition_conflict')
        row={'schema_version':'target-match-1.0','candidate':c,'agent_config_id':capability['agent_config_id'],
             'constraint_instance':{'subject':context.get('subject'),'resource_type':c.get('resource_type'),'required_state':c.get('required_state',[])},
             'status':'rejected' if reasons else 'compatible','reasons':reasons,'score':None}
        if reasons: rejected.append(row)
        else:
            row['score']=score(c) if score else len(set(c.get('description','').lower().split())&set(c['action'].replace('_',' ').split()))
            accepted.append(row)
    accepted.sort(key=lambda r:(-r['score'],r['candidate'].get('path_id',''),r['candidate'].get('node_id','')))
    return {'schema_version':'target-match-batch-1.0','accepted':accepted,'rejected':rejected,'budget':{'external_calls':0}}

def synthetic_candidate(**changes):
    c={'source_id':'synthetic-booking','source_group_id':'synthetic-only','node_id':'synthetic:n0','path_id':'synthetic:p0',
       'action':'view_result','object':{'appointment_id':'appointment-001'},'resource_type':'appointments',
       'required_effect':'read_only','subject':'synthetic-agent','required_state':[],'description':'view result'}
    return {**c,**changes}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    cap=json.loads((ROOT/'data/目标能力.json').read_text(encoding='utf8'))
    candidates=[synthetic_candidate(),synthetic_candidate(path_id='synthetic:p1',action='send_email'),
        synthetic_candidate(path_id='synthetic:p2',subject='other'),
        synthetic_candidate(path_id='synthetic:p3',object={'appointment_id':'missing'}),
        synthetic_candidate(path_id='synthetic:p4',required_state=[{'collection':'appointments','resource_id':'appointment-001','field':'time','equals':'wrong'}])]
    result=match(candidates,cap,{'subject':'synthetic-agent','state':INITIAL_STATE})
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'compatible':len(result['accepted']),'rejected':len(result['rejected'])}))
