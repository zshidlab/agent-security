"""Pre-call ledger for local generation/target/observation/repair units, not dollars."""
import argparse
from copy import deepcopy
import json
import math
from pathlib import Path
import time

KINDS = ('generation', 'target', 'observation', 'repair')


class BudgetExceeded(RuntimeError):
    pass


class Budget:
    def __init__(self, limits=None, *, total=30, rounds=6, candidates_per_step=3,
                 units=100, unit_costs=None, seconds=30, clock=time.monotonic):
        self.limits = dict(limits or dict.fromkeys(KINDS, 10))
        costs = dict(unit_costs or dict.fromkeys(KINDS, 1))
        if set(self.limits) != set(KINDS) or set(costs) != set(KINDS):
            raise ValueError('all_call_categories_required')
        if any(type(v) is not int or v < 0 for v in [*self.limits.values(), *costs.values(), total, rounds, units]):
            raise ValueError('finite_nonnegative_integer_budget_required')
        if type(candidates_per_step) is not int or not 1 <= candidates_per_step <= 3:
            raise ValueError('candidate_limit_must_be_1_to_3')
        if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds < 0:
            raise ValueError('finite_elapsed_limit_required')
        self.total_limit = total; self.round_limit = rounds; self.candidate_limit = candidates_per_step
        self.unit_limit = units; self.costs = costs; self.seconds = seconds; self.clock = clock
        self.started = clock(); self.used = dict.fromkeys(KINDS, 0); self.units = 0
        self.rounds = []; self.calls = []; self.blocked = []

    def deny(self, reason, kind, reference):
        self.blocked.append({'reason': reason, 'kind': kind, 'reference': reference,
                             'invoked': False, 'elapsed_seconds': self.clock() - self.started})
        raise BudgetExceeded(reason)

    def check_time(self, kind, reference):
        if self.clock() - self.started >= self.seconds:
            self.deny('elapsed_budget', kind, reference)

    def start_round(self, step_id):
        self.check_time('round', step_id)
        if len(self.rounds) >= self.round_limit: self.deny('round_budget', 'round', step_id)
        if self.rounds.count(step_id) >= self.candidate_limit: self.deny('candidate_budget', 'round', step_id)
        self.rounds.append(step_id)

    def call(self, kind, function, *args, reference=None, **kwargs):
        if kind not in KINDS: raise ValueError('unknown_call_category')
        self.check_time(kind, reference)
        if self.used[kind] >= self.limits[kind]: self.deny(kind + '_budget', kind, reference)
        if sum(self.used.values()) >= self.total_limit: self.deny('total_call_budget', kind, reference)
        charge = self.costs[kind]
        if self.units + charge > self.unit_limit: self.deny('simulated_unit_budget', kind, reference)
        # Reserve before invocation. Errors/timeouts consume the call; never refund.
        self.used[kind] += 1; self.units += charge
        entry = {'call_id': f'budget-call-{len(self.calls)+1}', 'kind': kind, 'reference': reference,
                 'invoked': True, 'simulated_units': charge, 'tokens': None, 'actual_cost_usd': None,
                 'started_elapsed_seconds': self.clock() - self.started, 'status': 'started'}
        self.calls.append(entry)
        try:
            value = function(*args, **kwargs)
        except Exception as exc:
            entry.update(status='timeout' if isinstance(exc, TimeoutError) else 'error', error_type=type(exc).__name__)
            raise
        else:
            entry['status'] = 'returned'; return value
        finally:
            entry['finished_elapsed_seconds'] = self.clock() - self.started

    def snapshot(self):
        return deepcopy({'schema_version': 'budget-ledger-1.0', 'limits': self.limits,
                         'used': self.used, 'total_calls': sum(self.used.values()), 'rounds': self.rounds,
                         'simulated_units': self.units, 'tokens': None, 'actual_cost_usd': None,
                         'unit_definition': 'configured offline units, not model tokens or currency',
                         'calls': self.calls, 'blocked_before_call': self.blocked,
                         'elapsed_seconds': self.clock() - self.started,
                         'stop_limitation': 'pre-call elapsed gate; no cancellation of an already running adapter'})


def run_budgeted_path(plan, adapter, budget, *, executor=None, observer_mode='full'):
    from mini_executor import MiniExecutor
    from retry_policy import retry_step
    from build_step_table import SCHEMA
    from jsonschema import Draft202012Validator
    from uuid import uuid4
    Draft202012Validator(SCHEMA).validate(plan)
    executor = executor or MiniExecutor(); initial = executor.reset(); run_id = 'budgeted-' + uuid4().hex
    nodes = {s['step_id']: s for s in plan['steps']}; current = plan['entry']; seen = set(); results = []
    reason = None
    while current != 'STOP':
        if current in seen or current not in nodes:
            reason = 'invalid_or_cyclic_successor'; break
        seen.add(current); step = nodes[current]
        result = retry_step(step, adapter, executor=executor, observer_mode=observer_mode,
                            meter=budget, reset=False, run_id=f'{run_id}:{len(results)+1}')
        results.append(result)
        if result['stop_reason'] != 'completed': reason = result['stop_reason']; break
        current = step['success_next']
    return {'schema_version': 'budgeted-path-1.0', 'run_id': run_id, 'test_id': plan['test_id'],
            'path_id': plan['path_id'], 'initial_state': initial, 'steps': results,
            'final_state': deepcopy(executor.state), 'stop_reason': reason or 'path_completed',
            'ledger': budget.snapshot(), 'scope': 'local_fixed_policy_only'}


def demo_main():
    from run_local_pipeline import two_step_plan, demo_adapter
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True); a = p.parse_args()
    limited = Budget({'generation': 2, 'target': 1, 'observation': 2, 'repair': 0})
    rows = [run_budgeted_path(two_step_plan(), demo_adapter('normal'), limited),
            run_budgeted_path(two_step_plan(), demo_adapter('normal'), Budget())]
    a.output.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf8')
    print(json.dumps({'runs': len(rows), 'stop_reasons': [r['stop_reason'] for r in rows],
                      'calls': [r['ledger']['total_calls'] for r in rows]}))


if __name__ == '__main__':
    # Use one module identity, including BudgetExceeded used by retry_policy.
    from budget import demo_main as canonical_main
    canonical_main()
