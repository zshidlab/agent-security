"""Create a new immutable D25 demo directory; never overwrite an existing freeze."""
import argparse
from datetime import datetime
import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
import shutil

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ['mini_executor.py', 'reference_graphs.py', 'match_target.py', 'build_step_table.py',
           'generate_one_step.py', 'judgment_examples.py', 'check_step.py', 'run_local_pipeline.py',
           'retry_policy.py', 'budget.py']

DEMO = r'''"""Offline local_mock demonstration. No model or external system is contacted."""
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
    sys.stdout.reconfigure(encoding='utf8')
    sys.stderr.reconfigure(encoding='utf8')
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
'''


def build(output):
    algorithm = ROOT / 'algorithm'
    output.mkdir(parents=True, exist_ok=False)
    source_hashes = {}
    for relative in ([f'src/{name}' for name in RUNTIME] +
                     ['schemas/testplan.schema.json', 'schemas/capability.schema.json', 'data/目标能力.json']):
        source = algorithm / relative; destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, destination)
        source_hashes['algorithm/' + relative] = hashlib.sha256(source.read_bytes()).hexdigest()
    (output / 'demo.py').write_text(DEMO, encoding='utf8')
    config = {'schema_version': 'demo-config-1.0', 'scope': 'local_mock',
              'budget': {'limits': {'generation': 6, 'target': 8, 'observation': 6, 'repair': 0},
                         'total': 20, 'rounds': 4, 'candidates_per_step': 3, 'units': 100, 'seconds': 30},
              'cases': {'normal': {'target': 'fixed_policy', 'observer': 'full'},
                        'refusal': {'target': 'refusing', 'observer': 'full'},
                        'unknown': {'target': 'fixed_policy', 'observer': 'missing_after'}}}
    (output / 'config.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    packages = {name: metadata.version(name) for name in
                ('jsonschema', 'attrs', 'jsonschema-specifications', 'referencing', 'rpds-py')}
    (output / 'requirements.txt').write_text(''.join(f'{name}=={version}\n' for name, version in packages.items()), encoding='utf8')
    (output / 'environment.json').write_text(json.dumps({'python': platform.python_version(),
         'dependencies': packages, 'installation_note': 'Verified with existing installed packages; clean installation is not claimed.'}, indent=2) + '\n', encoding='utf8')
    (output / 'README.md').write_text('''# OAPT_A D25 演示版 1.0

这是可独立运行的 local_mock 包；只用合成通知与内存预约，不连接模型或真实系统。
固定策略刻意将合成文本命令映射到两个本地工具，用于验证生成→执行→独立观察→三值判断。
RefusingExecutor 是显式拒绝替身；信息不足例屏蔽完成观察。结果不代表真实攻击成功或车辆安全。

从本目录运行（Python >=3.10，实际测试环境见 environment.json）：

```powershell
python -I -B demo.py --case normal --output-dir <新的外部输出目录>
python -I -B demo.py --case refusal --output-dir <另一个新的外部输出目录>
python -I -B demo.py --case unknown --output-dir <第三个新的外部输出目录>
```

依赖已安装版本见 requirements.txt；本日未执行清洁安装。不要把输出放入冻结包，不覆盖既有运行。
每次启动先核对包文件哈希与清单；此清单用于版本复核，不是签名或来源真实性证明。
原始 JSON 保留候选、输入读取、工具结果、独立状态差分、观察、证据、判断、预算和停止原因；Markdown 解释每次继续/停止。
费用是离线模拟单位，真实 token/美元成本未知。耗时门禁只能拒绝后续调用，不能取消已运行的适配器。

责任：OAPT_A/szh；接口：testplan-1.0 / capability-1.0 / step-judgment-1.0；未更改 B/C 共享接口。
D09 的隔日至少24小时重标、D13 的真实模型抽取仍未完成；本包不代替这些源验收。
只冻结本地闭环需要的代码；不含真实模型、凭据、上游轨迹数据或留出集。
''', encoding='utf8')
    files = {p.relative_to(output).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(output.rglob('*')) if p.is_file()}
    manifest = {'schema_version': 'demo-release-1.0', 'release_id': 'OAPT_A-D25-local-demo-1.0',
                'created_at': datetime.now().astimezone().isoformat(), 'maintainer': 'OAPT_A/szh',
                'source_plan': 'A:block-404..415', 'source_code_hashes': source_hashes,
                'files': files, 'scope': 'local_mock; real_model_calls=0',
                'compatibility': 'A local internal prototype; no shared B/C interface change'}
    (output / 'release-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True); args = parser.parse_args()
    result = build(args.output)
    print(json.dumps({'release_id': result['release_id'], 'files': len(result['files'])}))
