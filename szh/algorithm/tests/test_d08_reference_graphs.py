import copy
import hashlib
import json
import pytest
from reference_graphs import ROOT, validate_reference

def graphs():
    return [json.loads(x) for x in (ROOT/'data/人工示范图.jsonl').read_text(encoding='utf8').splitlines()]

def test_all_references_and_parallel_calls():
    gs=graphs(); assert len(gs)==10
    for g in gs:
        p=ROOT/g['source_file']; ms=json.loads(p.read_text(encoding='utf8'))
        assert hashlib.sha256(p.read_bytes()).hexdigest()==g['sha256']
        assert len(g['rounds'])==len(ms)
        assert validate_reference(g,ms)
    travel=next(g for g in gs if g['source_id']=='AL-019')
    assert len([n for n in travel['nodes'] if n['request_ref']==2])==3
    assert not any(e['from']=='AL-019:n00' and e['to']=='AL-019:n01' for e in travel['edges'])

def test_order_is_not_dependency_and_missing_is_unknown():
    g=graphs()[0]; ms=json.loads((ROOT/g['source_file']).read_text(encoding='utf8'))
    assert not any(e['kind']=='dependency' for e in g['edges'])
    bad=copy.deepcopy(g);bad['edges'].append({'from':g['nodes'][0]['node_id'],'to':g['nodes'][1]['node_id'],'kind':'dependency','quote':'invented','evidence_refs':[3]})
    with pytest.raises(ValueError,match='unsupported'): validate_reference(bad,ms)
    bad=copy.deepcopy(g); bad['nodes'][1]['result_refs']=[];bad['nodes'][1]['axes']['effect']='observed'
    with pytest.raises(ValueError,match='state effect'): validate_reference(bad,ms)

def test_wrong_result_binding_rejected():
    g=graphs()[1];ms=json.loads((ROOT/g['source_file']).read_text(encoding='utf8'))
    g['nodes'][0]['result_refs']=[5]
    with pytest.raises(ValueError,match='signature mismatch'): validate_reference(g,ms)
