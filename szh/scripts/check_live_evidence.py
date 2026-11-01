"""Verify saved real responses without repeating paid API calls."""
from collections import Counter
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'algorithm/src'))
from parse_trace import parse_development
from model_extract import run_extraction
from check_graph import proposal_graph,check_graph
from rule_extract import extract


def main():
    state=json.loads((ROOT/'records/revalidation-current.json').read_text(encoding='utf8'))
    folder=ROOT/state['records']['13']/'live-attempt-01'
    rows=[json.loads(x) for x in (folder/'extractions.jsonl').read_text(encoding='utf8').splitlines()]
    traces={t['source_id']:t for t in parse_development()}
    assert len(rows)==20 and {r['source_id'] for r in rows}==set(traces)
    reports=[];models=Counter();usage=Counter()
    for row in rows:
        trace=traces[row['source_id']]
        assert row['mode']=='real_deepseek_api' and 1<=len(row['calls'])<=3
        assert len(row['transport_calls'])==len(row['calls'])
        for log,call in zip(row['calls'],row['transport_calls']):
            response=call['response']
            assert call['status']=='returned' and response['id'] and response['created']
            assert response['choices'][0]['message']['content']==log['raw_reply']
            assert call['request']['messages'][1]['content']==json.dumps(log['request'],ensure_ascii=False)
            assert 'Authorization' not in call and 'headers' not in call
            models[response['model']]+=1
            usage.update({k:v for k,v in response['usage'].items() if type(v)is int})
        # Replay parsing only: model callback returns the exact recorded response.
        replies=iter(c['raw_reply'] for c in row['calls'])
        replay=run_extraction(trace,lambda _:next(replies))
        assert replay['status']==row['status'] and replay['proposal']==row['proposal']
        for method,graph in [('rule',extract(trace)),('real_deepseek_api',proposal_graph(row['proposal'],trace))]:
            result=check_graph(graph,trace)
            reports.append({'source_id':row['source_id'],'method':method,'input_issues':trace['issues'],**result})
    summary={'verified_inputs':20,'real_http_calls':sum(models.values()),'resolved_models':dict(models),'usage':dict(usage),
             'graph_checks':{method:dict(Counter(r['status'] for r in reports if r['method']==method))
                            for method in ('rule','real_deepseek_api')},
             'invalid_policy':'Preserve ambiguous input bindings; do not promote to Valid.',
             'scope':'Model extraction and graph integrity, not observed target attack effects.'}
    (ROOT/state['records']['13']/'live-evidence-check.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (ROOT/state['records']['14']/'real-and-rule-graphs.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in reports),encoding='utf8')
    print(json.dumps(summary))


if __name__=='__main__':main()
