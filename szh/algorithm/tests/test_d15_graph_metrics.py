import pytest
from evaluate_graph import compare,metrics

def test_hand_computed_eight_two_one():
    m,fp,fn=compare(list(range(9)),list(range(8))+[10,11])
    assert (m['tp'],m['fp'],m['fn'])==(8,2,1)
    assert m['precision']==0.8 and m['recall']==pytest.approx(8/9)
    assert m['f1']==pytest.approx(16/19)
    assert fp==[10,11] and fn==[8]

def test_relation_kind_direction_and_duplicate_count():
    m,fp,fn=compare([('a','b','dependency')],[('a','b','temporal'),('b','a','dependency')])
    assert (m['tp'],m['fp'],m['fn'])==(0,2,1)
    assert compare(['a'],['a','a'])[0]['fp']==1

def test_zero_denominators_retained():
    m,fp,fn=compare([],[]);assert m['tp']==0 and m['precision'] is None and m['recall'] is None and m['f1'] is None
    assert metrics(0,0,1)['recall']==0 and metrics(0,0,1)['precision'] is None
