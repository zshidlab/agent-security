import csv
from copy import deepcopy
from source_inventory import ROOT
from source_filter import filter_records


def rows():
    return list(csv.DictReader((ROOT/'data/历史来源清单.csv').open(encoding='utf-8')))


def test_conservation_and_reason_ledger():
    result=filter_records(rows())
    assert len(result)==200
    assert all(r['source_group_id'] for r in result)
    assert sum(r['keep'] for r in result)+sum(not r['keep'] for r in result)==200
    assert all(r['reason'] for r in result if not r['keep'])


def test_three_variants_stay_grouped_and_duplicate_preserved():
    original=rows()[0]; variants=[deepcopy(original) for _ in range(3)]
    for i,r in enumerate(variants): r['source_id']=f'variant-{i}'
    result=filter_records(variants)
    assert len({r['source_group_id'] for r in result})==1
    assert [r['keep'] for r in result]==[True,False,False]
    assert all(r['reason']=='duplicate_raw_content' for r in result[1:])


def test_single_turn_not_in_complete_set():
    original=next(r for r in rows() if r['source_id']=='AL-009')
    assert filter_records([original])[0]['reason']=='single_turn'
