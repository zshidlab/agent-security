"""Counterexamples run against an explicit source or frozen runtime, no network."""
import argparse
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import sys


def probe(runtime):
    sys.path.insert(0,str(runtime))
    from budget import Budget,run_budgeted_path
    from mini_executor import INITIAL_STATE
    from run_local_pipeline import two_step_plan,demo_adapter,run_pipeline,PREFIX
    plan=two_step_plan();plan['budget']['max_calls']=2
    limited=run_budgeted_path(plan,demo_adapter('normal'),Budget())
    assert limited['ledger']['used']['target']==2 and len(limited['steps'])==1
    assert limited['stop_reason']=='plan_tool_budget_exhausted'
    views=[]
    def adapter(view):
        views.append(deepcopy(view));return demo_adapter('normal')(view)
    normal=run_budgeted_path(two_step_plan(),adapter,Budget())
    assert normal['stop_reason']=='path_completed' and views[1]['visible_history']
    assert not any(k in json.dumps(views) for k in ('"before"','"after"','"final_state"'))
    for value in ([],{},42,None):
        result=run_pipeline(two_step_plan(),adapter=lambda v:{'surface':v['allowed_surface'],
            'text':PREFIX+json.dumps({'tool':value,'arguments':{}})})
        assert result['stop_reason']=='Unknown'
        assert result['final_state']['appointments']==INITIAL_STATE['appointments']
    plan=two_step_plan()
    second=plan['steps'][1]
    second['tool']='modify_appointment'
    second['arguments']={**plan['steps'][0]['arguments'],'new_time':'2026-10-23T16:00:00+08:00'}
    second['contract']['Goal']={'tool':second['tool'],'arguments':deepcopy(second['arguments'])}
    for field in ('Observe','Post'):
        second['contract'][field]=[{'kind':'state_changed_to','collection':'appointments',
            'resource_id':'appointment-001','field':'time','equals':second['arguments']['new_time']}]
    second['contract']['Pre']=[{'collection':'appointments','resource_id':'appointment-001','field':'time',
                              'equals':INITIAL_STATE['appointments']['appointment-001']['time']}]
    results=[]
    for mode in ('local','budgeted'):
        result=(run_pipeline(plan,adapter=demo_adapter('normal')) if mode=='local' else
                run_budgeted_path(plan,demo_adapter('normal'),Budget()))
        assert result['stop_reason']=='precondition_conflict'
        assert result['final_state']['appointments']['appointment-001']['time']==plan['steps'][0]['arguments']['new_time']
        assert result['steps'][1]['preflight']['target_invoked'] is False
        if mode=='budgeted': assert result['steps'][1]['attempts']==[]
        else: assert result['steps'][1]['event'] is None
        results.append({'mode':mode,'result':result})
    guard=run_pipeline(two_step_plan(),adapter=demo_adapter('normal'),observer_mode='guard_unavailable')
    assert guard['budget']['tool_calls']==0 and guard['final_state']==INITIAL_STATE
    return {'timestamp':datetime.now().astimezone().isoformat(),'runtime':str(runtime.resolve()),
            'all_passed':True,'plan_budget':limited,'visible_history':views,'precondition':results,
            'guard':guard,'scope':'local synthetic execution, zero model calls'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=probe(a.runtime)
    with a.output.open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({'all_passed':True,'runtime':str(a.runtime)}))
