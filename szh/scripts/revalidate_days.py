"""Retain revision evidence; progress writes are a separate final action."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

import day_run

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'records/revalidation-current.json'


def init():
    stamp = datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%z') + '-revalidation'
    mapping = {}
    for n in [9, 13, *range(14, 26)]:
        p = ROOT / 'records' / f'D{n:02}' / stamp
        p.mkdir(parents=True, exist_ok=False)
        files = [ROOT / f'docs/tasks/D{n:02}.md', ROOT / 'docs/tasks/manifest.json']
        task = day_run.MANIFEST['tasks'][n-1]
        files += [ROOT / f for f in task['deliverables'] if (ROOT / f).is_file()]
        day_run.write_json(p / 'inputs.json', {
            'day': f'D{n:02}', 'started': day_run.now().isoformat(), 'python': sys.version,
            'authority': 'User authorized D09/D13 closure and sequential D14-D25 revalidation; workbook writes only after ALL acceptance passes.',
            'schema': 'daily-revalidation-1.0', 'source_block': task['source_block'],
            'input_hashes': {str(f.relative_to(ROOT)): day_run.digest(f) for f in files},
            'original_start_preserved': True})
        (p / 'commands.md').write_text('# Actual commands\n\nProgress writes deferred until final acceptance.\n', encoding='utf8')
        mapping[str(n)] = p.relative_to(ROOT).as_posix()
    book = ROOT / day_run.MANIFEST['workbook']['path']
    day_run.write_json(STATE, {'created_at': day_run.now().isoformat(), 'records': mapping,
                              'workbook_before_sha256': day_run.digest(book)})
    print(json.dumps(mapping))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['init', 'cmd'])
    p.add_argument('--day', type=int)
    raw = sys.argv[1:]
    split = raw.index('--') if '--' in raw else len(raw)
    a = p.parse_args(raw[:split])
    a.argv = raw[split+1:]
    if a.action == 'init':
        init(); return 0
    state = json.loads(STATE.read_text(encoding='utf8'))
    if a.day is None or not a.argv:
        p.error('cmd requires --day and a command following --')
    return day_run.command(ROOT / state['records'][str(a.day)], a.argv)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf8')
    raise SystemExit(main())
