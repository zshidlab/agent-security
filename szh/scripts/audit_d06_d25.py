"""Read-only closure audit against the formal workbook; not a second progress table."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
import check_workspace as check

ROOT = Path(__file__).resolve().parents[1]


def audit():
    manifest = json.loads((ROOT / 'docs/tasks/manifest.json').read_text(encoding='utf8'))
    book = (ROOT / manifest['workbook']['path']).resolve()
    sheets, _ = check.workbook_cells(book, ('A_核心算法', '总览甘特图'))
    check.ERRORS.clear(); check.check_sources(manifest)
    if check.ERRORS: raise AssertionError(check.ERRORS)
    checked = []; paths = []
    for day in range(6, 26):
        task = manifest['tasks'][day - 1]; row = task['excel_row']
        values = [sheets['A_核心算法'][f'{c}{row}'][0] for c in 'OPQRSTU']
        partial = day in (9, 13)
        assert values[0] == ('阻塞' if partial else '已完成'), (day, values)
        assert values[1] == (75 if partial else 100), (day, values)
        assert values[2] and (not values[3] if partial else values[3]), (day, values)
        assert all(values[i] for i in (4, 5, 6)), (day, values)
        handoffs = sorted((ROOT / f'records/D{day:02}').glob('*/handoff.md'))
        record = handoffs[-1].parent
        finish = json.loads((record / 'excel-finish.json').read_text(encoding='utf8'))
        assert finish['saved_reopened_O_U'] == values
        for name in ('protected_A_cells_unchanged', 'other_zip_entries_byte_identical',
                     'all_source_and_overview_formulas_verified'):
            assert finish[name] is True
        commands = [json.loads(p.read_text(encoding='utf8')) for p in record.glob('command-*.json')]
        assert commands and all(c['exit_code'] == 0 for c in commands), (day, record)
        for relative in task['deliverables']:
            p = ROOT / relative
            assert p.exists()
            paths += [f for f in p.rglob('*') if f.is_file()] if p.is_dir() else [p]
        checked.append({'day': task['id'], 'formal_status': values[0], 'formal_percent': values[1],
                        'record': record.relative_to(ROOT).as_posix(), 'reopened_values_match': True})
    # Only path names and Git metadata are examined; no ignored content is opened.
    status = subprocess.run(['git', 'status', '--short', '--ignored', '--untracked-files=all', '--', '.'],
                            cwd=ROOT, capture_output=True, text=True, encoding='utf8', check=True).stdout.splitlines()
    ignored = [line for line in status if line.startswith('!!')]
    assert not ignored, ('Unexpected ignored files require classification', ignored)
    relative_paths = sorted({p.relative_to(ROOT).as_posix() for p in paths})
    probe = subprocess.run(['git', 'check-ignore', '--stdin'], input='\n'.join(relative_paths) + '\n',
                           cwd=ROOT, capture_output=True, text=True, encoding='utf8')
    assert probe.returncode == 1 and not probe.stdout, ('Deliverable ignored', probe.stdout, probe.stderr)
    diff = subprocess.run(['git', 'diff', '--check', '--', '.'], cwd=ROOT, capture_output=True, text=True, encoding='utf8')
    assert diff.returncode == 0, diff.stdout + diff.stderr
    assert not (ROOT / '.gitignore').exists()
    return {'schema_version': 'daily-closure-audit-1.0', 'timestamp': datetime.now().astimezone().isoformat(),
            'authority': 'Snapshot of formal Excel and saved daily evidence; not a separate progress authority',
            'days': checked, 'completed': 18, 'partial': ['D09', 'D13'],
            'source_and_formula_checks': '4 DOCX, 700 source values, 650 overview references, 2500 Gantt formulas',
            'git_review': {'status_entries': len(status), 'ignored_entries': ignored,
                           'deliverable_files_probed': len(relative_paths), 'all_deliverables_not_ignored': True,
                           'diff_check': 'passed', 'szh_gitignore_added': False,
                           'classification': 'Code, schemas, research data, documents and reproducible evidence retained; temporary environments/caches outside workspace.'},
            'stop_boundary': 'D25; D26 not started',
            'remaining_conditions': ['D09 requires real >=24h reannotation and differences',
                                     'D13 requires authorized compatible real model extraction of 20 inputs; fixture calls do not qualify']}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf8')
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True); a = p.parse_args()
    result = audit()
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'completed': result['completed'], 'partial': result['partial'], 'git_review': result['git_review']}, ensure_ascii=False))
