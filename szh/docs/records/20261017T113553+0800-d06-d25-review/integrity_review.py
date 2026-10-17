"""Read-only provenance/progress inspection; writes only this review's evidence."""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_workspace as check


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding='utf8')
    manifest = json.loads((ROOT / 'docs/tasks/manifest.json').read_text(encoding='utf8'))
    workbook = (ROOT / manifest['workbook']['path']).resolve()
    workbook_hash = digest(workbook)
    cells, _ = check.workbook_cells(workbook, ('A_核心算法', '总览甘特图'))
    days = []
    hash_drift = []
    tracked_paths = set()
    for task in manifest['tasks'][5:25]:
        row = task['excel_row']
        values = {c: cells['A_核心算法'].get(f'{c}{row}', ('', None))[0] for c in 'OPQRSTU'}
        records = sorted((ROOT / 'records' / task['id']).glob('*/handoff.md'))
        record = records[-1].parent
        finish = json.loads((record / 'excel-finish.json').read_text(encoding='utf8'))
        commands = [json.loads(p.read_text(encoding='utf8')) for p in sorted(record.glob('command-*.json'))]
        saved = finish['saved_reopened_O_U']
        assert saved == list(values.values()), (task['id'], 'saved values differ')
        assert all(c['exit_code'] == 0 for c in commands), (task['id'], 'latest daily command failure')
        check.ERRORS.clear()
        check.check_structure(manifest, task['id'], True)
        assert not check.ERRORS, check.ERRORS
        outputs = json.loads((record / 'outputs.json').read_text(encoding='utf8'))['deliverables_sha256']
        for relative in task['deliverables']:
            path = ROOT / relative
            expected = outputs[relative]
            if path.is_file():
                tracked_paths.add(relative)
                if digest(path) != expected:
                    hash_drift.append({'day': task['id'], 'path': relative,
                                       'recorded_sha256': expected, 'current_sha256': digest(path)})
            else:
                actual = {str(p.relative_to(path)): digest(p) for p in path.rglob('*') if p.is_file()}
                assert actual == expected, (task['id'], 'frozen directory drift')
                tracked_paths.update(p.relative_to(ROOT).as_posix() for p in path.rglob('*') if p.is_file())
        days.append({'day': task['id'], 'excel_row': row, 'O_U': values,
                     'latest_record': record.relative_to(ROOT).as_posix(),
                     'saved_reopened_values_equal': True, 'latest_command_count': len(commands),
                     'latest_commands_all_exit_zero': True, 'structure_deliverables_check': 'passed'})
    tracked_paths.update(p.relative_to(ROOT).as_posix() for p in HERE.rglob('*') if p.is_file())
    ignored = subprocess.run(['git', 'check-ignore', '--stdin'], cwd=ROOT, text=True,
                             input='\n'.join(sorted(tracked_paths)) + '\n',
                             capture_output=True, encoding='utf8')
    assert ignored.returncode == 1 and not ignored.stdout, (ignored.stdout, ignored.stderr)
    assert digest(workbook) == workbook_hash
    summary = Counter(d['O_U']['O'] for d in days)
    first = [json.loads(line) for line in (ROOT / 'algorithm/data/标注自查.jsonl').read_text(encoding='utf8').splitlines()]
    result = {'schema_version': 'review-integrity-1.0', 'timestamp': datetime.now().astimezone().isoformat(),
              'scope': 'D06-D25 review; snapshot of formal workbook, not a second progress authority',
              'workbook_sha256_unchanged': workbook_hash, 'status_counts': dict(summary),
              'days': days, 'current_deliverables_differing_from_daily_hash': hash_drift,
              'git_check_ignore': {'argv': ['git', 'check-ignore', '--stdin'],
                                   'formal_and_review_files_probed': len(tracked_paths),
                                   'exit_code': ignored.returncode, 'stdout': ignored.stdout, 'stderr': ignored.stderr},
              'annotation_review_keys': sorted(first[0]) if first else [],
              'annotation_review_count': len(first),
              'limitations': 'Checks saved progress/provenance and file integrity; behavioral acceptance is assessed separately.'}
    with (HERE / 'integrity.json').open('x', encoding='utf8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status_counts': dict(summary), 'daily_output_hash_drift': hash_drift,
                      'formal_and_review_files_not_ignored': len(tracked_paths),
                      'workbook_unchanged': True}, ensure_ascii=False))
    for day in days:
        if day['O_U']['O'] != '已完成':
            print(json.dumps({'day': day['day'], 'O_U': day['O_U']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
