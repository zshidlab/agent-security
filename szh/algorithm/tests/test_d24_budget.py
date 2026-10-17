from collections import Counter
import pytest
from budget import Budget, BudgetExceeded, run_budgeted_path
from run_local_pipeline import two_step_plan, demo_adapter
from mini_executor import INITIAL_STATE


def test_last_budget_unit_blocks_before_call_and_preserves_unexecuted_candidate():
    meter = Budget({'generation': 2, 'target': 1, 'observation': 2, 'repair': 0})
    result = run_budgeted_path(two_step_plan(), demo_adapter('normal'), meter)
    assert result['stop_reason'] == 'budget:target_budget'
    assert meter.used['target'] == 1
    assert result['final_state']['appointments'] == INITIAL_STATE['appointments']
    attempt = result['steps'][0]['attempts'][0]
    assert attempt['candidate']['status'] == 'accepted' and attempt['event'] is None
    assert attempt['classification'] == 'unexecuted_candidate_budget'
    assert len(meter.calls) == 2 and len(meter.blocked) == 1


def test_raw_logs_reconcile_success_error_timeout_and_unknown_cost():
    meter = Budget(); invoked = []
    def operation(value):
        invoked.append(value)
        if value == 'error': raise ValueError('synthetic error')
        if value == 'timeout': raise TimeoutError('synthetic timeout')
        return value
    assert meter.call('generation', operation, 'ok') == 'ok'
    with pytest.raises(ValueError): meter.call('target', operation, 'error')
    with pytest.raises(TimeoutError): meter.call('observation', operation, 'timeout')
    meter.call('repair', operation, 'repair')
    assert len(invoked) == len(meter.calls) == sum(meter.used.values()) == 4
    assert dict(Counter(c['kind'] for c in meter.calls)) == meter.used
    assert [c['status'] for c in meter.calls] == ['returned', 'error', 'timeout', 'returned']
    assert meter.snapshot()['actual_cost_usd'] is None and meter.snapshot()['tokens'] is None


def test_round_total_units_elapsed_and_path_budget_boundaries():
    invoked = []
    for kwargs in ({'total': 0}, {'units': 0}, {'seconds': 0}):
        meter = Budget(**kwargs)
        with pytest.raises(BudgetExceeded): meter.call('generation', lambda: invoked.append(1))
        assert not meter.calls
    assert invoked == []
    meter = Budget(rounds=1)
    meter.start_round('s')
    with pytest.raises(BudgetExceeded): meter.start_round('s')
    normal = run_budgeted_path(two_step_plan(), demo_adapter('normal'), Budget())
    assert normal['stop_reason'] == 'path_completed'
    assert normal['ledger']['used'] == {'generation': 2, 'target': 4, 'observation': 2, 'repair': 0}
    assert normal['steps'][1]['initial_state']['appointments'] == normal['steps'][0]['final_state']['appointments']
    counts = Counter(c['kind'] for c in normal['ledger']['calls'])
    assert all(counts[k] == v for k, v in normal['ledger']['used'].items())


def test_cli_handles_pre_call_budget_exception_with_canonical_module(tmp_path):
    import json
    import subprocess
    import sys
    from reference_graphs import ROOT
    output = tmp_path / 'budget-runs.jsonl'
    process = subprocess.run([sys.executable, '-B', str(ROOT / 'src/budget.py'), '--output', str(output)],
                             capture_output=True, text=True, encoding='utf8')
    assert process.returncode == 0, process.stderr
    rows = [json.loads(x) for x in output.read_text(encoding='utf8').splitlines()]
    assert [r['stop_reason'] for r in rows] == ['budget:target_budget', 'path_completed']
