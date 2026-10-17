from mini_executor import MiniExecutor
from build_step_table import synthetic_plan
from run_local_pipeline import demo_adapter, RefusingExecutor
from retry_policy import retry_step


def step():
    s = synthetic_plan()['steps'][0]; s['max_retries'] = 2; return s


def test_three_technical_candidates_no_fourth_and_parent_chain_retained():
    calls = []
    def timeout(view): calls.append(view); raise TimeoutError('synthetic timeout')
    result = retry_step(step(), timeout)
    assert len(calls) == len(result['attempts']) == result['budget']['generation_calls'] == 3
    assert result['stop_reason'] == 'candidate_limit' and result['budget']['tool_calls'] == 0
    ids = [a['candidate']['candidate_id'] for a in result['attempts']]
    assert [a['parent_candidate_id'] for a in result['attempts']] == [None, ids[0], ids[1]]
    assert all(a['candidate']['reasons'] == ['adapter_error:TimeoutError'] for a in result['attempts'])


def test_unknown_only_reobserves_same_call_and_never_regenerates():
    result = retry_step(step(), demo_adapter('normal'), observer_mode='missing_after')
    assert result['stop_reason'] == '观察不足' and len(result['attempts']) == 1
    assert result['budget'] == {'generation_calls': 1, 'tool_calls': 2, 'observations': 3, 'external_calls': 0}
    assert all(o['judgment']['value'] == 'Unknown' for o in result['attempts'][0]['observations'])
    recovered = retry_step(step(), demo_adapter('normal'), observer_mode='missing_after', recover_observation=True)
    assert recovered['stop_reason'] == 'completed' and recovered['budget']['generation_calls'] == 1
    assert recovered['budget']['observations'] == 2


def test_explicit_rejection_stops_and_false_can_change_candidate():
    rejected = retry_step(step(), demo_adapter('normal'), executor=RefusingExecutor())
    assert rejected['stop_reason'] == 'safety_rejection' and len(rejected['attempts']) == 1
    class FirstNoOp(MiniExecutor):
        invocations = 0
        def modify_appointment(self, appointment_id, new_time, *, subject='synthetic-agent'):
            self.invocations += 1
            if self.invocations == 1:
                return self._call('modify_appointment', {'appointment_id': appointment_id, 'new_time': new_time, 'subject': subject},
                                  lambda: self.state['appointments'][appointment_id])
            return super().modify_appointment(appointment_id, new_time, subject=subject)
    recovered = retry_step(step(), demo_adapter('normal'), executor=FirstNoOp())
    assert recovered['stop_reason'] == 'completed' and len(recovered['attempts']) == 2
    assert recovered['attempts'][0]['observations'][0]['judgment']['value'] == 'False'
    assert recovered['attempts'][0]['classification'] == 'research_negative'
    limited = retry_step(step(), demo_adapter('normal'), executor=FirstNoOp(), max_tool_calls=2)
    assert limited['stop_reason'] == 'tool_budget_exhausted' and limited['budget']['generation_calls'] == 1
