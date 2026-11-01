"""Execute twenty development traces through the authorized DeepSeek adapter."""
import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'algorithm/src'))
from deepseek_adapter import DeepSeekAdapter
from model_extract import run_extraction
from parse_trace import parse_development
from check_graph import proposal_graph, check_graph


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--model', default='deepseek-chat')
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    adapter = DeepSeekAdapter(a.config, model=a.model)
    traces = parse_development()
    assert len(traces) == 20
    results = []
    for trace in traces:
        start = len(adapter.calls)
        result = run_extraction(trace, adapter)
        row = {'source_id': trace['source_id'], 'mode': 'real_deepseek_api', **result,
               'transport_calls': adapter.calls[start:]}
        if result['proposal']:
            graph = proposal_graph(result['proposal'], trace)
            graph['method'] = 'deepseek_real_model'
            row['graph_check'] = check_graph(graph, trace)
        results.append(row)
        with (a.output / 'extractions.jsonl').open('a', encoding='utf8') as f:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
        print(json.dumps({'source_id': trace['source_id'], 'status': result['status'],
                          'calls': len(result['calls']), 'stop': result['stop_reason']}), flush=True)
        # Authentication/network failure requires a new run, not twenty repeated failures.
        if result['stop_reason'] == 'adapter_failure':
            break
    usage = Counter()
    for call in adapter.calls:
        for k, v in (call.get('response') or {}).get('usage', {}).items():
            if type(v) is int:
                usage[k] += v
    summary = {'timestamp': datetime.now().astimezone().isoformat(), 'model_requested': a.model,
               'inputs': len(results), 'expected_inputs': 20, 'real_http_calls': len(adapter.calls),
               'statuses': dict(Counter(r['status'] for r in results)), 'usage': dict(usage),
               'actual_cost_usd': None, 'scope': 'real model extraction, not target attack execution',
               'all_inputs_called': len(results) == 20 and all(r['transport_calls'] for r in results),
               'all_responses_received': all(c['status'] == 'returned' for c in adapter.calls)}
    (a.output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    print(json.dumps(summary), flush=True)
    return 0 if summary['all_inputs_called'] and summary['all_responses_received'] else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf8')
    raise SystemExit(main())
