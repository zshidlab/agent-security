import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from reference_graphs import ROOT

PACKAGE = ROOT / 'release/演示版'


def test_frozen_hashes_match_local_source_and_full_inventory():
    manifest = json.loads((PACKAGE / 'release-manifest.json').read_text(encoding='utf8'))
    actual_files = {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file() and p.name != 'release-manifest.json'}
    assert actual_files == set(manifest['files'])
    for relative, expected in manifest['files'].items():
        assert hashlib.sha256((PACKAGE / relative).read_bytes()).hexdigest() == expected
    for relative, expected in manifest['source_code_hashes'].items():
        assert hashlib.sha256((ROOT.parent / relative).read_bytes()).hexdigest() == expected


def test_three_cases_run_independently_with_only_frozen_package(tmp_path):
    isolated = tmp_path / 'package'; shutil.copytree(PACKAGE, isolated)
    expected = {'normal': 'path_completed', 'refusal': 'safety_rejection', 'unknown': '观察不足'}
    runs = []
    for name, stop in expected.items():
        output = tmp_path / ('out-' + name)
        process = subprocess.run([sys.executable, '-I', '-B', str(isolated / 'demo.py'), '--case', name,
                                  '--output-dir', str(output)], cwd=tmp_path, capture_output=True, text=True, encoding='utf8')
        assert process.returncode == 0, process.stderr
        row = json.loads((output / (name + '.json')).read_text(encoding='utf8')); runs.append(row)
        assert row['stop_reason'] == stop and row['mode'] == 'local_mock' and row['real_model_calls'] == 0
        report = (output / (name + '.md')).read_text(encoding='utf8')
        assert 'Evidence：' in report and '决定：' in report and '理由：' in report
        assert '不计算真实攻击成功率' in report
    assert len({r['run_id'] for r in runs}) == 3
    assert all(r['initial_state'] == runs[0]['initial_state'] for r in runs)
    assert len(runs[0]['steps']) == 2
    assert len(runs[1]['steps']) == len(runs[2]['steps']) == 1
    assert all(o['judgment']['value'] == 'Unknown' for o in runs[2]['steps'][0]['attempts'][0]['observations'])


def test_changed_code_is_rejected_before_execution(tmp_path):
    isolated = tmp_path / 'tampered'; shutil.copytree(PACKAGE, isolated)
    with (isolated / 'src/mini_executor.py').open('a', encoding='utf8') as stream: stream.write('\n# simulated change\n')
    output = tmp_path / 'must-not-exist'
    process = subprocess.run([sys.executable, '-I', '-B', str(isolated / 'demo.py'), '--case', 'normal',
                              '--output-dir', str(output)], cwd=tmp_path, capture_output=True, text=True, encoding='utf8')
    assert process.returncode != 0 and 'package hash mismatch' in process.stderr
    assert not output.exists()
