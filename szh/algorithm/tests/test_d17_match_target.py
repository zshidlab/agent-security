import copy,json
from match_target import match,synthetic_candidate
from mini_executor import INITIAL_STATE
from reference_graphs import ROOT

def cap():return json.loads((ROOT/'data/目标能力.json').read_text(encoding='utf8'))
def ctx():return {'subject':'synthetic-agent','state':copy.deepcopy(INITIAL_STATE)}

def test_compatible_sorted_only_after_hard_filter_and_stable_ties():
    seen=[]
    def score(c):seen.append(c['path_id']);return 999
    rows=[synthetic_candidate(path_id='p2'),synthetic_candidate(path_id='p1'),synthetic_candidate(path_id='bad',action='send_email')]
    r=match(rows,cap(),ctx(),score)
    assert [x['candidate']['path_id'] for x in r['accepted']]==['p1','p2']
    assert set(seen)=={'p1','p2'} and r['rejected'][0]['score'] is None

def test_permission_schema_resource_and_state_reject():
    rows=[synthetic_candidate(subject='other'),synthetic_candidate(object={'appointment_id':'missing'}),
          synthetic_candidate(object={'unexpected':1}),synthetic_candidate(resource_type='files'),
          synthetic_candidate(required_state=[{'collection':'appointments','resource_id':'appointment-001','field':'time','equals':'different'}])]
    result=match(rows,cap(),ctx());assert not result['accepted'] and len(result['rejected'])==5
    assert all(r['reasons'] for r in result['rejected'])

def test_writer_permission_and_unknown_state_fail_closed():
    c=synthetic_candidate(action='modify_appointment',required_effect='write_time',subject='other',object={'appointment_id':'appointment-001','new_time':'later'})
    r=match([c],cap(),{'subject':'other','state':INITIAL_STATE})
    assert 'permission_denied' in r['rejected'][0]['reasons']
    assert match([synthetic_candidate()],cap(),{'subject':'synthetic-agent','state':None})['rejected']
