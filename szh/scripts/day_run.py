"""Record actual daily commands and patch only the authorized A-row O:U cells.

XLSX entries other than the A sheet are copied byte-for-byte. The A sheet is
patched as text so styles, extensions, formulas and other rows stay intact.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

import check_workspace as check

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'docs/tasks/manifest.json').read_text(encoding='utf-8'))


def now():
    return datetime.now().astimezone()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def workbook_update(day, values, record, phase):
    task = MANIFEST['tasks'][day - 1]
    book = (ROOT / MANIFEST['workbook']['path']).resolve()
    if book.with_name('~$' + book.name).exists():
        raise RuntimeError('Workbook lock file exists; do not bypass its owner')
    check.ERRORS.clear()
    check.check_sources(MANIFEST)
    if check.ERRORS:
        raise RuntimeError(check.ERRORS)
    before_hash = digest(book)
    sheets, _ = check.workbook_cells(book, ('A_核心算法', '总览甘特图'))
    row = task['excel_row']
    old = [sheets['A_核心算法'].get(f'{c}{row}', ('', None))[0] for c in 'OPQRSTU']
    # Find the target XML through the workbook relationships, not a sheet number.
    import xml.etree.ElementTree as ET
    import posixpath
    with zipfile.ZipFile(book) as archive:
        entries = [(item, archive.read(item.filename)) for item in archive.infolist()]
    blobs = {item.filename: blob for item, blob in entries}
    wb = ET.fromstring(blobs['xl/workbook.xml'])
    rels = {x.attrib['Id']: x.attrib['Target'] for x in ET.fromstring(blobs['xl/_rels/workbook.xml.rels'])}
    sheet = next(s for s in wb.find(f'{{{check.MAIN}}}sheets') if s.attrib['name'] == 'A_核心算法')
    target = rels[sheet.attrib[f'{{{check.REL}}}id']]
    target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
    text = blobs[target].decode('utf-8')
    original = text
    for column, value in zip('OPQRSTU', values):
        address = f'{column}{row}'
        pattern = rf'<c\b[^>]*\br="{address}"[^>]*(?:/>|>.*?</c>)'
        match = re.search(pattern, text, re.S)
        if not match:
            raise RuntimeError('Missing expected progress cell: ' + address)
        style = re.search(r'\bs="([^"]+)"', match.group())
        attrs = f' r="{address}"' + (f' s="{style[1]}"' if style else '')
        replacement = (f'<c{attrs}><v>{value}</v></c>' if isinstance(value, (int, float))
                       else f'<c{attrs} t="inlineStr"><is><t xml:space="preserve">{escape(str(value))}</t></is></c>')
        text = text[:match.start()] + replacement + text[match.end():]
    # Also prove all A-sheet cells outside this row range are unchanged.
    def protected(xml):
        root = ET.fromstring(xml)
        return {c.attrib['r']: ET.tostring(c) for c in root.iter(f'{{{check.MAIN}}}c')
                if c.attrib['r'] not in {f'{x}{row}' for x in 'OPQRSTU'}}
    if protected(original) != protected(text):
        raise RuntimeError('Protected cells changed')
    with tempfile.TemporaryDirectory(prefix='oapt-xlsx-') as tmp:
        out = Path(tmp) / book.name
        with zipfile.ZipFile(out, 'w') as archive:
            for item, blob in entries:
                archive.writestr(item, text.encode('utf-8') if item.filename == target else blob)
        if digest(book) != before_hash:
            raise RuntimeError('Workbook changed concurrently; refusing stale write')
        # Opening the existing workbook for writing respects an Excel sharing lock.
        with book.open('r+b') as stream:
            stream.write(out.read_bytes())
            stream.truncate()
    reopened, _ = check.workbook_cells(book, ('A_核心算法', '总览甘特图'))
    actual = [reopened['A_核心算法'].get(f'{c}{row}', ('', None))[0] for c in 'OPQRSTU']
    if actual != values:
        raise RuntimeError(('Reopen values mismatch', actual, values))
    with zipfile.ZipFile(book) as archive:
        unchanged = all(archive.read(name) == blob for name, blob in blobs.items() if name != target)
    if not unchanged:
        raise RuntimeError('Other workbook parts changed')
    check.ERRORS.clear()
    check.check_sources(MANIFEST)
    if check.ERRORS:
        raise RuntimeError(check.ERRORS)
    write_json(record / f'excel-{phase}.json', {
        'timestamp': now().isoformat(), 'workbook': str(book), 'row': row,
        'source_A_N': task['source_fields'], 'before_O_U': old, 'saved_reopened_O_U': actual,
        'protected_A_cells_unchanged': True, 'other_zip_entries_byte_identical': True,
        'all_source_and_overview_formulas_verified': True, 'before_sha256': before_hash,
        'after_sha256': digest(book), 'date_note': 'Actual execution date; plan dates unchanged'})


def command(record, argv):
    stamp = now().isoformat()
    with tempfile.TemporaryDirectory(prefix='oapt-pytest-') as temporary:
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace',
                                env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1',
                                     'PYTEST_DEBUG_TEMPROOT': temporary})
    existing = sorted(record.glob('command-*.json'))
    path = record / f'command-{len(existing)+1:02}.json'
    write_json(path, {'timestamp': stamp, 'cwd': str(ROOT), 'argv': argv, 'exit_code': result.returncode,
                      'stdout': result.stdout, 'stderr': result.stderr})
    with (record / 'commands.md').open('a', encoding='utf-8') as stream:
        stream.write(f'\n- {stamp} | `{subprocess.list2cmdline(argv)}` | exit {result.returncode} | {path.name}\n')
    if argv[:2] == ['git', 'status']:
        print(f'Git status captured: {len(result.stdout.splitlines())} entries; {path.name}')
    else:
        print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, file=sys.stderr, end='')
    return result.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'cmd', 'finish'])
    parser.add_argument('--day', type=int, required=True)
    parser.add_argument('--record', type=Path)
    parser.add_argument('--status', default='已完成', choices=['已完成', '进行中', '阻塞'])
    parser.add_argument('--percent', type=int, default=100)
    parser.add_argument('--note', default='')
    parser.add_argument('--checks', default='')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    a = parser.parse_args()
    if not 6 <= a.day <= 25:
        parser.error('This authorization is D06–D25 only')
    task = MANIFEST['tasks'][a.day-1]
    if a.action == 'start':
        record = ROOT / 'records' / task['id'] / (now().strftime('%Y%m%dT%H%M%S%z') + '-first')
        record.mkdir(parents=True, exist_ok=False)
        files = [ROOT / 'docs/tasks/manifest.json', ROOT / task['plan']]
        for dep in task['prerequisites']:
            files += [ROOT / p for p in MANIFEST['tasks'][int(dep[1:])-1]['deliverables'] if (ROOT / p).is_file()]
        previous = sorted((ROOT / 'records' / task['id']).glob('*/handoff.md'))
        write_json(record / 'inputs.json', {'started': now().isoformat(), 'day': task['id'],
                   'previous_run': str(previous[-1].parent.relative_to(ROOT)) if previous else None,
                   'python': sys.version, 'platform': platform.platform(), 'schema': 'daily-evidence-1.0',
                   'source_block': task['source_block'], 'input_hashes': {str(p.relative_to(ROOT)): digest(p) for p in files},
                   'source_documents': MANIFEST['documents'], 'authority': 'User explicitly authorized D06–D25 and A O:U workbook writes',
                   'preexisting_changes': subprocess.run(['git','status','--short','--untracked-files=all','--','.'],cwd=ROOT,capture_output=True,text=True).stdout})
        (record / 'commands.md').write_text('# Actual commands\n\nCWD: szh/. stdout/stderr/exit codes are retained in command-NN.json.\n',encoding='utf-8')
        workbook_update(a.day, ['进行中',0,now().date().isoformat(),'','; '.join(task['deliverables']),str(record.relative_to(ROOT)),'实际提前执行；不改变源排期。'], record, 'start')
        print(record.relative_to(ROOT).as_posix())
        return 0
    record = a.record.resolve()
    if not record.is_relative_to(ROOT / 'records' / task['id']):
        parser.error('Record outside selected day')
    if a.action == 'cmd':
        return command(record, a.args[1:] if a.args[:1] == ['--'] else a.args)
    if (a.status == '已完成') != (a.percent == 100):
        parser.error('100% requires complete status and vice versa')
    commands = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(record.glob('command-*.json'))]
    if a.status == '已完成' and (not commands or any(c['exit_code'] for c in commands)):
        raise RuntimeError('Completion refused: failed/missing actual commands')
    if a.status == '已完成':
        check.ERRORS.clear()
        check.check_structure(MANIFEST, task['id'], True)
        if check.ERRORS:
            raise RuntimeError(check.ERRORS)
    inputs = json.loads((record / 'inputs.json').read_text(encoding='utf-8'))
    outputs = {}
    for p in task['deliverables']:
        path = ROOT / p
        if path.is_file(): outputs[p] = digest(path)
        elif path.is_dir(): outputs[p] = {str(f.relative_to(path)):digest(f) for f in path.rglob('*') if f.is_file()}
    write_json(record / 'outputs.json', {'timestamp': now().isoformat(), 'deliverables_sha256': outputs,
               'evidence_scope': 'Public research artifacts or local synthetic execution only',
               'request': 'See actual artifact', 'attempt': 'See actual artifact', 'blocked': 'See actual artifact',
               'effect': 'Unknown outside local observable state', 'violated': 'Unknown outside local observable state'})
    # Per-day file classification and whitespace verification, before progress closure.
    for argv in [['git','diff','--check','--','.'], ['git','status','--short','--ignored','--untracked-files=all','--','.']]:
        if command(record, argv): raise RuntimeError('Git review failed')
    (record / 'checks.md').write_text('# Source acceptance and limits\n\n' + a.checks + '\n\n' + a.note +
        '\n\nActual command evidence: command-*.json. Structure/existence checks do not replace behavior.\n'
        'New code, research data and JSON/Markdown command evidence are retained; no local cache/environment created. '
        'No szh/.gitignore added. Existing D01–D05 files preserved.\n',encoding='utf-8')
    start = inputs['started'][:10]
    workbook_update(a.day,[a.status,a.percent,start,now().date().isoformat() if a.status=='已完成' else '',
                    '; '.join(task['deliverables']), record.relative_to(ROOT).as_posix()+'; checks.md; command-*.json',a.note],record,'finish')
    common = (f"日期：{now().isoformat()}；{task['id']}；来源 A:block-{task['source_block']}。\n\n"
              f"源验收：{a.checks}\n\n限制/剩余条件：{a.note}\n\n"
              '输入版本、实际环境、依赖产物哈希见 inputs.json；产物哈希见 outputs.json；实际命令和退出码见 commands.md / command-*.json。\n\n'
              'Excel 已保存关闭重开，O:U 一致；A:N、其他 A 行及 B/C/总览等 ZIP 部件未改；所有总览引用和甘特公式通过。证据见 excel-start.json / excel-finish.json。\n\n'
              '跨区读取：仅共享 Excel 和四个源 DOCX；未读取或写入 zzy/lhy/data-generation。共享写入仅本日 A O:U。无会议，不改讨论节点。\n\n'
              '接口：A 本地版本见产物 schema_version；维护 OAPT_A/szh；变更日见本记录。A→B TestPlan+CapabilityConstraint+Contract，B→A ExecutionTrace+EvidenceOutcome，双方接入待确认；无 B/C 文件或共享接口修改。\n\n'
              '证据边界：公开轨迹仅研究输入；合成 Mock 的 Hard Observable 只支持本地行为。未证明真实攻击成功、模型质量或车辆安全增益。\n')
    (record / 'daily-record.md').write_text('# Daily actual record\n\n'+common,encoding='utf-8')
    (record / 'handoff.md').write_text('# Handoff\n\n'+common+'\n下一步：'+('进入本次授权的下一日，保留上述依赖缺口。' if a.day<25 else '停止于 D25；剩余门槛按记录继续，D26 未获本次授权。')+'\n',encoding='utf-8')
    print(json.dumps({'day':task['id'],'status':a.status,'percent':a.percent,'record':str(record.relative_to(ROOT))},ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
