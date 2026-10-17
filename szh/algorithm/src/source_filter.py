"""Conservative provenance grouping and lossless exclusion ledger."""
from collections import Counter
import csv
import json
from pathlib import Path
from source_inventory import ROOT, audit_row, features


def filter_records(rows):
    rows=[dict(r) for r in rows]
    parent={r['source_group_id']:r['source_group_id'] for r in rows}
    def find(x):
        while parent[x]!=x: x=parent[x]
        return x
    # Exact duplicate raw files across tasks must not leak across splits either.
    hashes={}
    for r in rows:
        group=r['source_group_id']
        if r['sha256'] in hashes:
            a,b=find(group),find(hashes[r['sha256']]); parent[max(a,b)]=min(a,b)
        hashes[r['sha256']]=group
    seen=set()
    for r in rows:
        r['source_group_id']=find(r['source_group_id'])
        f=audit_row(r)
        if r['sha256'] in seen: reason='duplicate_raw_content'
        elif f['assistant_count']==0: reason='missing_reply'
        elif not f['multi_turn']: reason='single_turn'
        elif not f['tool_calls']: reason='no_tool_request'
        elif f['tool_returns']<f['tool_calls']: reason='missing_tool_return'
        else: reason=''
        seen.add(r['sha256'])
        r.update(keep=not reason,reason=reason,usage='graph_input' if not reason else 'incomplete_or_duplicate_reference_only')
    return rows


def main():
    with (ROOT/'data/历史来源清单.csv').open(encoding='utf-8') as stream: rows=filter_records(list(csv.DictReader(stream)))
    with (ROOT/'data/筛选结果.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    excluded=[r for r in rows if not r['keep']]
    (ROOT/'data/incomplete-reference.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in excluded),encoding='utf-8')
    summary={'schema_version':'source-filter-1.0','input':len(rows),'kept':len(rows)-len(excluded),'excluded':len(excluded),
        'reasons':dict(Counter(r['reason'] for r in excluded)), 'group_count':len({r['source_group_id'] for r in rows}),
        'group_rule':'same suite/user_task across injections/models; also union identical raw hashes',
        'count_conserved':len(rows)==len(excluded)+sum(r['keep'] for r in rows)}
    (ROOT/'data/filter-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__': main()
