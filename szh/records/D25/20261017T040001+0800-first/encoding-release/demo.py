"""Offline local_mock demonstration. No model or external system is contacted."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE / 'src'))


def verify():
    manifest = json.loads((PACKAGE / 'release-manifest.json').read_text(encoding='utf8'))
    actual = {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()
              and p.name != 'release-manifest.json'}
    if actual != set(manifest['files']): raise ValueError('package inventory mismatch')
    for relative, expected in manifest['files'].items():
        if hashlib.sha256((PACKAGE / relative).read_bytes()).hexdigest() != expected:
            raise ValueError('package hash mismatch: ' + relative)
    return manifest


def report(case_name, result):
    lines = ['# D25 本地逐步报告', '', '模式：local_mock；固定文本策略；真实模型调用 0。',
             '仅证明本地控制流与状态证据，不计算真实攻击成功率。', '',
             '样例：' + case_name, 'Run-ID：' + result['run_id'],
             '停止原因：' + result['stop_reason'], '']
    for step in result['steps']:
        lines += ['步骤：' + step['step_id'], '步骤停止原因：' + step['stop_reason'], '']
        for attempt in step['attempts']:
            c = attempt['candidate']
            lines += ['候选：' + c['candidate_id'], '控制面检查：' + c['status'],
                      '分类：' + str(attempt['classification']),
                      '原始候选：`' + json.dumps(c['raw_reply'], ensure_ascii=False) + '`', '']
            for observation in attempt['observations']:
                j = observation['judgment']
                lines += ['观察：' + observation['observation_id'],
                          '决定：' + j['decision'] + ('；继续' if j['advance'] else '；停止/补观察'),
                          '理由：' + j['reason'], 'Evidence：' + ', '.join(j['evidence_refs']),
                          '缺失字段：' + ', '.join(j['missing_fields']),
                          '结果轴：`' + json.dumps(j['axes'], ensure_ascii=False) + '`',
                          '状态版本：`' + json.dumps(j['state_versions']) + '`', '']
    lines += ['预算：`' + json.dumps(result['ledger']['used']) + '`',
              '真实 token/美元成本：未知；模拟单位：' + str(result['ledger']['simulated_units']), '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=['normal', 'refusal', 'unknown', 'all'], default='all')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    verify()
    from budget import Budget, run_budgeted_path
    from run_local_pipeline import two_step_plan, demo_adapter, RefusingExecutor
    config = json.loads((PACKAGE / 'config.json').read_text(encoding='utf8'))
    args.output_dir.mkdir(parents=True, exist_ok=False)
    names = list(config['cases']) if args.case == 'all' else [args.case]
    summary = []
    for name in names:
        case = config['cases'][name]
        result = run_budgeted_path(two_step_plan(), demo_adapter('normal'), Budget(**config['budget']),
                                   executor=RefusingExecutor() if case['target'] == 'refusing' else None,
                                   observer_mode=case['observer'])
        result['case'] = name; result['mode'] = 'local_mock'; result['real_model_calls'] = 0
        (args.output_dir / (name + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
        (args.output_dir / (name + '.md')).write_text(report(name, result), encoding='utf8')
        summary.append({'case': name, 'run_id': result['run_id'], 'stop_reason': result['stop_reason']})
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
