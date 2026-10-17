import csv,json,hashlib
from reference_graphs import ROOT
from group_split import split,load_development

def test_actual_split_groups_hashes_and_twenty_working_examples():
    dev=load_development(False); held=[json.loads(x) for x in (ROOT/'data/留出集.jsonl').read_text(encoding='utf8').splitlines()]
    assert not {r['source_group_id'] for r in dev}&{r['source_group_id'] for r in held}
    assert not {r['sha256'] for r in dev}&{r['sha256'] for r in held}
    assert len(load_development())==20
    manifest=json.loads((ROOT/'data/split-manifest.json').read_text(encoding='utf8'))
    assert len(dev)+len(held)==171 and manifest['qualified_gap_to_200']==29
    assert hashlib.sha256((ROOT/'data/留出集.jsonl').read_bytes()).hexdigest()==manifest['holdout_sha256']

def test_rewritten_case_follows_exposed_group_and_small_pool_reportable():
    rows=[{'source_id':'a','source_group_id':'case1','keep':True},{'source_id':'rewrite','source_group_id':'case1','keep':True},
          {'source_id':'b','source_group_id':'case2','keep':True}]
    d,h=split(rows,['a'],[],20)
    assert {r['source_id'] for r in d}=={'a','rewrite'}
    assert [r['source_id'] for r in h]==['b']
    assert sum(r['selected_for_development'] for r in d)==2
