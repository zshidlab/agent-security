"""Run frozen D25 examples from a temporary package copy; preserve actual evidence."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def verify(package, output):
    output.mkdir(parents=True, exist_ok=False)
    evidence = []
    with tempfile.TemporaryDirectory(prefix='oapt-d25-isolated-') as temporary:
        isolated = Path(temporary)
        shutil.copytree(package, isolated / 'package')
        for case in ('normal', 'refusal', 'unknown'):
            destination = isolated / ('output-' + case)
            argv = [sys.executable, '-I', '-B', str(isolated / 'package/demo.py'), '--case', case, '--output-dir', str(destination)]
            process = subprocess.run(argv, cwd=isolated, capture_output=True, text=True, encoding='utf8',
                                     env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
            row = {'timestamp': datetime.now().astimezone().isoformat(), 'argv': argv, 'cwd': str(isolated),
                   'exit_code': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr,
                   'package_copy': 'Temporary isolated directory; -I ignores PYTHONPATH and user site.'}
            evidence.append(row)
            if destination.exists(): shutil.copytree(destination, output / case)
            if process.returncode: break
    (output / 'actual-commands.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    if len(evidence) != 3 or any(r['exit_code'] for r in evidence):
        raise RuntimeError('Isolated demo failed; evidence retained')
    print(json.dumps({'isolated_cases': 3, 'exit_codes': [r['exit_code'] for r in evidence]}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--package', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True); a = p.parse_args()
    verify(a.package.resolve(), a.output.resolve())
