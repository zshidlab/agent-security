"""Lossless local normalization of public benchmark messages (never executes text)."""
import argparse,copy,csv,json
from collections import Counter
from pathlib import Path
from reference_graphs import ROOT
from group_split import load_development

def signature(call):
    return json.dumps([call.get('function'),call.get('args')],sort_keys=True,ensure_ascii=False)

def parse(messages, source_id, task_id=None, source_group_id='Unknown'):
    if not isinstance(messages,list): raise ValueError('messages must be a list')
    task_id=task_id or source_id
    result={'schema_version':'normalized-trace-1.0','source_id':source_id,'source_group_id':source_group_id,
            'task_id':task_id,'messages':[],'events':[],'issues':[],'status':'Valid'}
    original_ids=[m.get('message_id') for m in messages if m.get('message_id') is not None]
    if len(set(original_ids))!=len(original_ids): result['issues'].append('duplicate_message_id')
    for i,m in enumerate(messages):
        mid=f'{source_id}:m{i:04}'
        result['messages'].append({'message_id':mid,'original_id':m.get('message_id'),'original_index':i,'raw':copy.deepcopy(m)})
        if m.get('task_id',task_id)!=task_id: result['issues'].append(f'cross_task_message:{mid}')
        def emit(kind,call,extra=None):
            e={'event_id':f'{mid}:e{len([e for e in result["events"] if e["message_id"]==mid]):02}',
               'message_id':mid,'message_index':i,'task_id':m.get('task_id',task_id),'kind':kind,
               'original_call_id':call.get('id'), 'tool':call.get('function'),'args':copy.deepcopy(call.get('args')),
               'call_key':None,'missing_reason':None,'source_id':source_id}
            e.update(extra or {});result['events'].append(e)
        for j,call in enumerate(m.get('tool_calls') or []):
            emit('request',call,{'call_index':j,'raw_call':copy.deepcopy(call)})
        if m.get('role')=='tool':
            call=copy.deepcopy(m.get('tool_call') or {})
            call['id']=m.get('tool_call_id') or call.get('id')
            emit('result',call,{'content':copy.deepcopy(m.get('content')),'error':m.get('error'),'raw_call':call})
        if 'state_delta' in m: emit('state_delta',{}, {'state_delta':copy.deepcopy(m['state_delta'])})
    requests=[e for e in result['events'] if e['kind']=='request']
    idcounts=Counter(e['original_call_id'] for e in requests if e['original_call_id'])
    sigcounts=Counter(signature(e['raw_call']) for e in requests)
    for q in requests:
        cid=q['original_call_id']
        if cid and idcounts[cid]!=1: q['missing_reason']='duplicate_call_id'
        elif not cid and sigcounts[signature(q['raw_call'])]!=1: q['missing_reason']='ambiguous_null_id_signature'
        else: q['call_key']=f'{task_id}:{cid}' if cid else f'{task_id}:signature:{q["event_id"]}'
    for e in result['events']:
        if e['kind']!='result': continue
        candidates=[q for q in requests if q['task_id']==e['task_id'] and q['message_index']<e['message_index']
                    and (q['original_call_id']==e['original_call_id'] if e['original_call_id']
                         else not q['original_call_id'] and signature(q['raw_call'])==signature(e['raw_call']))]
        if len(candidates)==1 and candidates[0]['call_key']:
            q=candidates[0]
            if e['tool'] and (e['tool'],e['args'])!=(q['tool'],q['args']): e['missing_reason']='conflicting_result_signature'
            else:
                e['call_key']=q['call_key']; e['association_basis']='call_id' if e['original_call_id'] else 'explicit_unique_tool_signature'
        else: e['missing_reason']='unmatched_or_ambiguous_result'
    for q in requests:
        matches=[e for e in result['events'] if e['kind']=='result' and e['call_key'] and e['call_key']==q['call_key']]
        if len(matches)>1:
            q['missing_reason']='duplicate_result'
            for e in matches: e['missing_reason']='duplicate_result'
        elif not matches and not q['missing_reason']: q['missing_reason']='missing_result'
    for e in result['events']:
        if e['missing_reason'] and e['missing_reason']!='missing_result': result['issues'].append(f'{e["event_id"]}:{e["missing_reason"]}')
    if result['issues']: result['status']='Invalid'
    return result

def parse_development():
    return [parse(json.loads((ROOT/r['local_file']).read_text(encoding='utf8')),r['source_id'],source_group_id=r['source_group_id']) for r in load_development()]

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    rows=parse_development();a.output.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf8')
    with a.output.with_suffix('.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f);w.writerow(['source_id','message_id','original_index','role','event_ids'])
        for r in rows:
            for m in r['messages']: w.writerow([r['source_id'],m['message_id'],m['original_index'],m['raw'].get('role'),';'.join(e['event_id'] for e in r['events'] if e['message_id']==m['message_id'])])
    print(json.dumps({'inputs':len(rows),'messages':sum(len(r['messages']) for r in rows),'events':sum(len(r['events']) for r in rows),'invalid_preserved':sum(r['status']=='Invalid' for r in rows)}))
