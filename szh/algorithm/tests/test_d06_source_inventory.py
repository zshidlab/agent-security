import csv
import json
from pathlib import Path
import pytest
from source_inventory import ROOT, audit_row, features


def test_downloaded_candidate_integrity_and_counts():
    rows=list(csv.DictReader((ROOT/'data/历史来源清单.csv').open(encoding='utf-8')))
    report=json.loads((ROOT/'data/source-audit.json').read_text(encoding='utf-8'))
    observations=[audit_row(r) for r in rows]
    assert len(rows)==200==report['candidate_count']
    assert len({r['source_id'] for r in rows})==200
    assert sum(x['graph_candidate'] for x in observations)==report['graph_candidates']
    assert all(r['exclusion_reason'] for r,x in zip(rows,observations) if not x['graph_candidate'])


def test_no_text_to_tool_effect_inference():
    f=features([{'role':'user','content':'read'},{'role':'assistant','content':'Done, changed everything'}])
    assert f['tool_returns']==0 and not f['graph_candidate']


def test_tampered_and_unlicensed_sources_rejected(tmp_path):
    raw=tmp_path/'data/raw'; raw.mkdir(parents=True)
    (raw/'x.json').write_text('[]',encoding='utf-8')
    row={'local_file':'data/raw/x.json','sha256':'bad','source_id':'bad','license':'MIT','license_file':'none'}
    with pytest.raises(ValueError,match='hash mismatch'): audit_row(row,tmp_path)
    from source_inventory import sha
    row['sha256']=sha(b'[]')
    with pytest.raises(ValueError,match='license'): audit_row(row,tmp_path)
