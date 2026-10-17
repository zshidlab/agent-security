"""Capture review commands without starting days or updating the workbook."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def write_new(path, value):
    with path.open('x', encoding='utf8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, default=str)
        stream.write('\n')


def main():
    sys.stdout.reconfigure(encoding='utf8')
    sys.stderr.reconfigure(encoding='utf8')
    argv = sys.argv[1:]
    if argv[:1] == ['--']:
        argv = argv[1:]
    if not argv:
        raise ValueError('command required')
    manifest = json.loads((ROOT / 'docs/tasks/manifest.json').read_text(encoding='utf8'))
    workbook = (ROOT / manifest['workbook']['path']).resolve()
    protected = [workbook, ROOT / 'docs/prompt.md']
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    started = datetime.now().astimezone().isoformat()
    with tempfile.TemporaryDirectory(prefix='oapt-review-') as temporary:
        process = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                                 encoding='utf8', errors='replace', timeout=180,
                                 env={**os.environ, 'PYTHONIOENCODING': 'utf-8',
                                      'PYTHONDONTWRITEBYTECODE': '1',
                                      'PYTEST_DEBUG_TEMPROOT': temporary})
    after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    number = len(list(HERE.glob('command-*.json'))) + 1
    target = HERE / f'command-{number:02}.json'
    write_new(target, {'started': started, 'finished': datetime.now().astimezone().isoformat(),
                      'purpose': 'D06-D25 review only', 'cwd': str(ROOT), 'argv': argv,
                      'python': sys.version, 'platform': platform.platform(),
                      'exit_code': process.returncode, 'stdout': process.stdout,
                      'stderr': process.stderr, 'protected_before_sha256': before,
                      'protected_after_sha256': after,
                      'protected_unchanged': before == after})
    print(f'{target.relative_to(ROOT).as_posix()} | exit {process.returncode} | protected unchanged: {before == after}')
    if argv[:2] != ['git', 'status']:
        print(process.stdout, end='')
    else:
        print(f'Git status captured: {len(process.stdout.splitlines())} entries')
    if process.stderr:
        print(process.stderr, file=sys.stderr, end='')
    if before != after:
        raise RuntimeError('Review command changed a protected file')
    return process.returncode


if __name__ == '__main__':
    raise SystemExit(main())
