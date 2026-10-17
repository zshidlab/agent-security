import json
import pytest
from model_extract import run_extraction,fixture_reply
from parse_trace import parse,parse_development
from reference_graphs import ROOT

def test_twenty_offline_inputs_accept_existing_refs_and_retain_raw():
    for t in parse_development():
        reply=fixture_reply(t);r=run_extraction(t,lambda _:reply)
        assert r['status']=='Valid' and len(r['calls'])==1
        assert r['calls'][0]['raw_reply']==reply
        assert r['calls'][0]['request']['input_data']==t

def test_unknown_evidence_direct_rejection_without_repair():
    fs=[json.loads(x) for x in (ROOT/'data/model-replies-fixture.jsonl').read_text(encoding='utf8').splitlines()]
    r=run_extraction(parse([],'synthetic'),lambda _:fs[2]['raw_reply'])
    assert r['status']=='Invalid' and len(r['calls'])==1
    assert r['calls'][0]['raw_reply']==fs[2]['raw_reply']

def test_two_repairs_only_and_all_failures_retained():
    t=parse([],'s');r=run_extraction(t,lambda _:'{bad')
    assert len(r['calls'])==3 and r['stop_reason']=='format_budget_exhausted'
    assert all(x['error'] and x['raw_reply']=='{bad' for x in r['calls'])
    replies=iter(['bad','bad',fixture_reply(t)])
    assert run_extraction(t,lambda _:next(replies))['status']=='Valid'
    with pytest.raises(ValueError):run_extraction(t,lambda _:'{}',3)
    def unavailable(_):raise TimeoutError()
    r=run_extraction(t,unavailable);assert len(r['calls'])==1 and r['status']=='Invalid'
