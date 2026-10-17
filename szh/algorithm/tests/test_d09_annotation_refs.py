import json
from datetime import datetime,timedelta,timezone
from annotation_review import review_status
from reference_graphs import ROOT,validate_reference

def test_initial_annotations_refer_to_actual_messages():
    rows=[json.loads(x) for x in (ROOT/'data/标注自查.jsonl').read_text(encoding='utf8').splitlines()]
    assert len(rows)==5
    for row in rows:
        g=row['graph']; assert g['source_id']==row['source_id']
        assert validate_reference(g,json.loads((ROOT/g['source_file']).read_text(encoding='utf8')))
        assert not review_status(row)['complete']

def test_real_gate_does_not_accept_same_day_or_missing_review():
    # Synthetic unit times test the gate only; no fabricated real second annotation.
    a={'source_id':'synthetic','annotated_at':'2026-10-17T01:00:00+08:00','graph':{'nodes':[]}}
    b={**a,'annotated_at':'2026-10-17T02:00:00+08:00'}
    assert not review_status(a,b)['complete']
    b['annotated_at']='2026-10-18T01:00:00+08:00';b['graph']={'nodes':[1]}
    assert review_status(a,b)['changed']
