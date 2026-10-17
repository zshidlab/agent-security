"""Freeze complete source groups, with a twenty-record working subset."""
import csv,hashlib,json
from pathlib import Path
from reference_graphs import ROOT

def split(rows, exposed_ids, reference_ids, count=20):
    kept=[dict(r) for r in rows if r['keep'] in (True,'True')]
    dev_groups={r['source_group_id'] for r in rows if r['source_id'] in set(exposed_ids)|set(reference_ids)}
    development=[r for r in kept if r['source_group_id'] in dev_groups]
    holdout=[r for r in kept if r['source_group_id'] not in dev_groups]
    ordered=sorted(development,key=lambda r:(r['source_id'] not in reference_ids,r['source_id']))
    selected={r['source_id'] for r in ordered[:count]}
    for r in development: r.update(split='development',selected_for_development=r['source_id'] in selected)
    for r in holdout: r.update(split='holdout',selected_for_development=False)
    return development,holdout

def load_development(selected=True):
    rows=[json.loads(x) for x in (ROOT/'data/开发集.jsonl').read_text(encoding='utf8').splitlines()]
    return [r for r in rows if r['selected_for_development']] if selected else rows

if __name__=='__main__':
    source=ROOT/'data/筛选结果.csv';rows=list(csv.DictReader(source.open(encoding='utf8')))
    refs=[json.loads(x)['source_id'] for x in (ROOT/'data/人工示范图.jsonl').read_text(encoding='utf8').splitlines()]
    dev,held=split(rows,[f'AL-{i:03}' for i in range(1,11)],refs)
    for filename,rs in [('开发集.jsonl',dev),('留出集.jsonl',held)]:
        (ROOT/'data'/filename).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs),encoding='utf8')
    manifest={'schema_version':'split-1.0','maintainer':'OAPT_A/szh','changed_on':'2026-10-17','seed':None,
        'rule':'deterministic by source_id; all D06 first-ten inspected groups and D08 reference groups go to development',
        'development_count':len(dev),'working_subset_count':sum(r['selected_for_development'] for r in dev),
        'holdout_count':len(held),'qualified_count':len(dev)+len(held),'qualified_gap_to_200':200-len(dev)-len(held),
        'development_groups':sorted({r['source_group_id'] for r in dev}),'holdout_groups':sorted({r['source_group_id'] for r in held}),
        'working_source_ids':[r['source_id'] for r in dev if r['selected_for_development']],
        'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'holdout_sha256':hashlib.sha256((ROOT/'data/留出集.jsonl').read_bytes()).hexdigest(),
        'restrictions':['holdout not used for prompt/ranking/matching tuning','task/original-case groups separated; tools shared across groups; path-level separation not established',
                        'D09 elapsed-day review pending; current annotation protocol provisional',
                        'public synthetic benchmark only; cannot support real agent generalization'],
        'design_resolution':'All variants stay in development file; exactly twenty flagged working records. Larger pool prevents annotation leakage. Source wording retained; no acceptance threshold lowered.'}
    (ROOT/'data/split-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:manifest[k] for k in ['development_count','working_subset_count','holdout_count','qualified_gap_to_200']},ensure_ascii=False))
