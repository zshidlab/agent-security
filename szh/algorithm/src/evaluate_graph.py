"""Recomputable counts against provisional single-annotator development references."""
from collections import Counter
import csv,json
from reference_graphs import ROOT
from parse_trace import parse
from rule_extract import extract
from check_graph import check_graph

MATCHING={'schema_version':'graph-matching-1.0','node_key':['source_id','original_request_index','call_index','tool','canonical_args'],
 'relations':'directed endpoint node keys and exact edge kind; temporal and dependency separate',
 'precision':'TP/(TP+FP)','recall':'TP/(TP+FN)','F1':'2TP/(2TP+FP+FN)',
 'zero_denominator':'null/undefined, including empty graphs; retain all counts',
 'scope':'rule vs ten single-annotator development references; D09 reannotation pending; no heldout/model quality claim'}

def metrics(tp,fp,fn):
    return {'tp':tp,'fp':fp,'fn':fn,'precision':tp/(tp+fp) if tp+fp else None,
            'recall':tp/(tp+fn) if tp+fn else None,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None}

def compare(expected,predicted):
    a,b=Counter(expected),Counter(predicted)
    tp=sum((a&b).values());fp=sum((b-a).values());fn=sum((a-b).values())
    return metrics(tp,fp,fn),list((b-a).elements()),list((a-b).elements())

def evaluate(reference, graph, trace):
    sid=reference['source_id'];events={e['event_id']:e for e in trace['events']}
    def key(i,j,tool,args):return (sid,i,j,tool,json.dumps(args,sort_keys=True,ensure_ascii=False))
    refkeys={n['node_id']:key(n['request_ref'],n['call_index'],n['tool_call']['function'],n['tool_call']['args']) for n in reference['nodes']}
    predkeys={n['node_id']:key(events[n['request_event_id']]['message_index'],events[n['request_event_id']]['call_index'],n['action'],n['object']) for n in graph['nodes']}
    rows=[];errors=[]
    for kind in ['node','temporal','dependency']:
        exp=list(refkeys.values()) if kind=='node' else [(refkeys[e['from']],refkeys[e['to']]) for e in reference['edges'] if e['kind']==kind]
        pred=list(predkeys.values()) if kind=='node' else [(predkeys[e['from']],predkeys[e['to']]) for e in graph['edges'] if e['kind']==kind]
        counts,fp,fn=compare(exp,pred)
        rows.append({'source_id':sid,'kind':kind,'method':'rule','graph_status':check_graph(graph,trace)['status'],**counts})
        for category,items in [('FP',fp),('FN',fn)]:
            for item in items:errors.append({'source_id':sid,'source_file':reference['source_file'],'kind':kind,'error':category,'key':item,'index_convention':'zero based original message index in node key'})
    return rows,errors

if __name__=='__main__':
    out=ROOT/'results';out.mkdir(exist_ok=True)
    # Persist the comparison rule before generating counts; no holdout inspection.
    (out/'graph-matching-v1.json').write_text(json.dumps(MATCHING,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    rows=[];errors=[]
    for line in (ROOT/'data/人工示范图.jsonl').read_text(encoding='utf8').splitlines():
        ref=json.loads(line);t=parse(json.loads((ROOT/ref['source_file']).read_text(encoding='utf8')),ref['source_id'],source_group_id=ref['source_group_id'])
        rs,es=evaluate(ref,extract(t),t);rows+=rs;errors+=es
    with (out/'图抽取初测.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/'graph-errors.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in errors),encoding='utf8')
    (out/'graph-evaluation-notes.md').write_text('# 抽取初测限制\n\n仅规则方法对十条单人参考开发图。节点按请求位置、调用序号、动作和参数精确匹配；关系按类型和有向端点。原始计数见 CSV，公式和零分母约定见 graph-matching-v1.json，错误原文位置见 graph-errors.jsonl。D09 隔日自查尚未执行，参考有标注偏差；D13 真实模型未调用，未评模型质量。未使用留出，不得据此宣称方法优越或真实攻击成功。\n',encoding='utf8')
    print(json.dumps({'graphs':10,'rows':len(rows),'errors':len(errors),'totals':{kind:{k:sum(r[k] for r in rows if r['kind']==kind) for k in ['tp','fp','fn']} for kind in ['node','temporal','dependency']}}))
