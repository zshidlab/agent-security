"""Acceptance receipts first; explicitly separate the final authorized Excel write."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

import day_run as dr
import check_workspace as cw

ROOT = dr.ROOT
STATE = ROOT / 'records/revalidation-current.json'
REPORT = ROOT / 'algorithm/记录/2026-10-30-逐日成果与验收.md'
FACTS = {
    9: ('5条真实隔日复标，最短326.94小时，2条来源的依赖关系发生变化；首次/第二次标注与逐项差异均保留，3项行为测试通过。',
        '同一Codex标注者跨会话自查，有先前熟悉度；不是人工金标、双盲或双人一致率。源K期待两种划分不同，本次节点边界未变，仅关系变化，已如实保留并待导师复核；源M单人自查要求满足。'),
    13: ('20条开发轨迹实际发出20次HTTP调用并全部返回；20个提案通过结构和引用检查，图完整性18 Valid、2 Invalid；5项测试通过。',
         '请求deepseek-chat，服务返回deepseek-flash；150865 tokens，实际费用未提供。AL-005/AL-007原始返回绑定歧义保持Invalid。事件99拒收是注入反例，不是本次模型实际幻觉；未执行真实目标攻击。'),
    14: ('4项测试通过：空证据、重复节点、逆序、伪造节点位置/端点证据均受检；真实与规则图各18 Valid、2 Invalid。',
         '顺序从原始请求事件推导；歧义输入拒绝，不静默修复；图Valid不等于效果成立。'),
    15: ('3项测试通过；10张冻结v1参考图、30行分项指标、9个错误；节点TP/FP/FN=34/0/0，时序35/0/0，依赖0/0/9。',
         '单标注者参考图及规则抽取存在关联偏差；D9后来复标未覆盖冻结v1，D13真实模型另列；不声称语义依赖抽取质量提升。'),
    16: ('3项测试通过；能力文件与微型执行器四工具一致，权限/资源/观察效果显式化，无取消预约工具。',
         '仅合成预约目标；实际平台/车辆能力未接入。'),
    17: ('4项测试通过；命令示例兼容1条、拒绝4条；null等非对象参数被拒绝且后续有效候选继续处理。',
         '先硬筛选再排序；拒绝原因保留；仅合成目标能力匹配。'),
    18: ('3项测试通过；合格路径编译TestPlan，Pre/Goal/Invariant/Observe/Post与预算、停止、后继齐全；无观察步骤标不可自动确认。',
         '协议仍为当前本地版本；B/C接入待确认。'),
    19: ('3项测试通过；6个完整三值样例保留真、假、缺失、冲突，单独模型文本判Unknown。',
         '样例是合成判断用例，不是攻击成功率统计。'),
    20: ('3项测试通过；6例命令输出全部匹配预期，错资源/错工具/错轮次不推进，缺失冲突失败关闭。',
         '只依据同轮同资源独立证据推进；Unknown不等于Safe。'),
    21: ('3项测试通过；4候选保留、1接受；输入视图只给当前目标、工具和可见历史，越界和格式拒绝保留。',
         '这里候选生成使用本地替身，真实模型调用为0；D13调用仅用于历史抽取。'),
    22: ('3项测试通过；10条无害输入均有结构化记录；4完成、2候选拒绝、3 Unknown、1 False；新增集成探针验证调用前Pre与异常工具字段停止。',
         '固定策略目标与内存工具；guard不可用零调用；状态冲突停止不伪造执行事件。'),
    23: ('3项测试通过；拒绝、观察不足、超时三类分别停止，生成次数1/1/3；历史不覆盖，并跨步传递经过滤的可见工具结果。',
         '不将before/after/final_state或Oracle隐藏状态送入生成视图；只验证有限本地重试策略。'),
    24: ('4项单测及4项历史反例通过；新集成探针通过：计划max_calls=2仅调用2次，第二次写入Pre冲突在写入前停止，可见历史存在且无隐藏快照。',
         '历史Pre诊断依赖event.before，现正确停止event=None，改以新探针验证更强的调用前拦截；原测试不改。一次-k拼写错误exit5原样保留，改正后4通过1未选；预调用耗时门禁不取消已运行调用。'),
    25: ('新冻结演示版1.1含18文件，5项测试通过；三例在隔离目录独立执行exit均为0，新冻结包预算/Pre/可见历史探针通过；全量75通过。',
         '原1.0包保留原始哈希，当前展示用1.1；三例为local_mock，模型调用0，不支持真实攻击成功率；清洁安装属于后续任务。'),
}


def context():
    state = json.loads(STATE.read_text(encoding='utf8'))
    records = {int(n): ROOT / p for n, p in state['records'].items()}
    book = (ROOT / dr.MANIFEST['workbook']['path']).resolve()
    return state, records, book


def protected_snapshot(book):
    # Preserve every XLSX part except the A sheet, and every protected A cell.
    import posixpath
    with zipfile.ZipFile(book) as z:
        blobs = {n: z.read(n) for n in z.namelist()}
    wb = ET.fromstring(blobs['xl/workbook.xml'])
    rels = {e.attrib['Id']: e.attrib['Target'] for e in ET.fromstring(blobs['xl/_rels/workbook.xml.rels'])}
    a = next(e for e in wb.find(f'{{{cw.MAIN}}}sheets') if e.attrib['name'] == 'A_核心算法')
    target = rels[a.attrib[f'{{{cw.REL}}}id']]
    target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
    authorized = {f'{col}{n+4}' for n in FACTS for col in 'OPQRSTU'}
    cells = {e.attrib['r']: hashlib.sha256(ET.tostring(e)).hexdigest()
             for e in ET.fromstring(blobs[target]).iter(f'{{{cw.MAIN}}}c') if e.attrib['r'] not in authorized}
    return {'protected_A_cells': cells,
            'other_parts': {n: hashlib.sha256(b).hexdigest() for n, b in blobs.items() if n != target}}


def audit(records):
    config = ROOT / '配置文档.md'
    keys = set(re.findall(rb'sk-[A-Za-z0-9_-]{12,}', config.read_bytes()))
    assert len(keys) == 1, 'Expected one configured key; value not reported'
    secret = next(iter(keys))
    leaks = []
    count = 0
    for p in ROOT.rglob('*'):
        if not p.is_file() or p == config or '.git' in p.parts:
            continue
        count += 1
        if secret in p.read_bytes():
            leaks.append(p.relative_to(ROOT).as_posix())
    assert not leaks, 'Credential found outside local configuration; values suppressed'
    ignored = subprocess.run(['git', 'check-ignore', '--quiet', '--', '配置文档.md'], cwd=ROOT).returncode == 0
    tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', '--', '配置文档.md'], cwd=ROOT,
                             capture_output=True).returncode == 0
    assert ignored and not tracked, 'Credential configuration must remain ignored and untracked'
    formal = [p.relative_to(ROOT).as_posix() for folder in [*records.values(), ROOT/'algorithm/release/演示版-1.1']
              for p in folder.rglob('*') if p.is_file()]
    result = subprocess.run(['git', 'check-ignore', '--no-index', '-z', '--stdin'], cwd=ROOT,
                            input='\0'.join(formal)+'\0', capture_output=True, text=True, encoding='utf8')
    assert result.returncode == 1 and not result.stdout, 'Formal evidence unexpectedly ignored'
    return {'timestamp': dr.now().isoformat(), 'files_scanned_for_exact_supplied_key': count,
            'credential_occurrences_outside_config': 0, 'config_ignored': ignored,
            'config_tracked': tracked, 'formal_files_checked_not_ignored': len(formal),
            'new_workspace_gitignore': (ROOT/'.gitignore').exists(),
            'scope': 'Exact supplied credential scanned in workspace bytes; no secret or secret hash reported.'}


def receipts(records):
    for n, folder in records.items():
        rows = [json.loads(p.read_text(encoding='utf8')) for p in sorted(folder.glob('command-*.json'))]
        assert rows, f'D{n:02}: no commands'
        for row in rows:
            if row['exit_code']:
                assert n == 24 and row['exit_code'] == 5 and 'not_state_precondition' in row['argv']
                assert any(r['exit_code'] == 0 and 'not state_precondition' in r['argv'] for r in rows)
        test = dr.MANIFEST['tasks'][n-1]['test']
        assert any(r['exit_code'] == 0 and test in r['argv'] and 'passed' in r['stdout'] for r in rows)
    all_rows = [json.loads(p.read_text(encoding='utf8')) for p in records[25].glob('command-*.json')]
    assert any(r['exit_code'] == 0 and '75 passed' in r['stdout'] for r in all_rows)
    live = json.loads((records[13]/'live-evidence-check.json').read_text(encoding='utf8'))
    assert live['real_http_calls'] == live['verified_inputs'] == 20
    assert live['graph_checks']['real_deepseek_api'] == {'Valid': 18, 'Invalid': 2}
    for file in [records[24]/'source-integration-final.json', records[25]/'frozen-integration.json']:
        assert json.loads(file.read_text(encoding='utf8'))['all_passed']


def daily_documents(records, final=False):
    for n, folder in records.items():
        task = dr.MANIFEST['tasks'][n-1]
        source = list(task['source_fields'].values())
        facts, limits = FACTS[n]
        outputs = {p: dr.digest(ROOT/p) if (ROOT/p).is_file() else
                   {f.relative_to(ROOT/p).as_posix(): dr.digest(f) for f in (ROOT/p).rglob('*') if f.is_file()}
                   for p in task['deliverables']}
        if n == 25:
            outputs['algorithm/release/演示版-1.1/'] = {p.relative_to(ROOT/'algorithm/release/演示版-1.1').as_posix(): dr.digest(p)
                  for p in (ROOT/'algorithm/release/演示版-1.1').rglob('*') if p.is_file()}
        dr.write_json(folder/'outputs.json', {'timestamp': dr.now().isoformat(), 'deliverables_sha256': outputs,
                      'actual_results': facts, 'limitations': limits,
                      'result_axes': 'Public extraction: request/attempt from original refs; independent effect/violated Unknown. Local execution axes, Contract and before/after in actual run JSON; not real target effects.'})
        inputs = json.loads((folder/'inputs.json').read_text(encoding='utf8'))
        receipt = folder/'excel-final-acceptance.json'
        progress = ('已保存并重新打开共享Excel；O:U与拟写一致。见excel-final-acceptance.json；源字段/公式与保护区域均校验。'
                    if final and receipt.exists() else '全部行为验收通过；尚未写Excel。拟写字段见D25同轮proposed-progress.json，最终写入/重开收据另存。')
        common = (f'# D{n:02} 修复重验记录\n\n'
                  f'实际开始：{inputs["started"]}；本记录更新时间：{dr.now().isoformat()}。来源A:block-{task["source_block"]}，A表第{n+4}行，总览第{n+5}行。\n\n'
                  f'源验收M：{source[12]}\n\n实际结果：{facts}\n\n限制与保留项：{limits}\n\n'
                  '环境：Python '+sys.version.split()[0]+'；'+platform.platform()+'。输入与原交付哈希见inputs.json，当前交付哈希见outputs.json；实际argv、时间、stdout/stderr、退出码见commands.md与command-*.json。\n\n'
                  '本次为修复重跑，旧运行及失败证据保持；前次记录由同日records目录及20261017复核报告追溯。正式代码版本以outputs.json哈希为准，未提交工作树见D25本轮Git记录。\n\n'
                  f'验收：{progress}\n\n'
                  '证据：来源/节点/测试/资源/结果轴与Contract在各对应JSON；公开轨迹提案用途为抽取，工具效果无独立观察则Unknown。本地Hard Observable仅支持合成执行。\n\n'
                  '授权：用户明确授权使用自备DeepSeek key及D9/D13补缺和后续既有成果重验；依据用户要求，全部测试通过之前不改进度文件。配置只由进程读取，不抄录到证据。\n\n'
                  '跨区读取仅共享Excel与四个原始DOCX；未读取或修改zzy/lhy/data-generation。共享写入只限授权A行O:U；A:N、其他A行、B/C、其他ZIP部件受保护；无会议、不改讨论节点。\n\n'
                  '接口来源为本工作区版本化Schema，维护责任OAPT_A/szh，变更日2026-10-30；A→B TestPlan+CapabilityConstraint+Contract，B→A ExecutionTrace+EvidenceOutcome，B/C接入待确认。协议文件无本轮变更，未向其他成员写入。\n\n'
                  '文件审查：正式源代码、研究数据、冻结包和JSON/Markdown验收证据保留；Python -B且pytest禁用缓存，临时运行放系统临时目录；未新增szh/.gitignore。Git/凭据/忽略规则审查见D25本轮收尾证据。\n')
        (folder/'daily-record.md').write_text(common, encoding='utf8')
        (folder/'checks.md').write_text(f'# D{n:02} 验收\n\n| 项目 | 实际与证据 | 判定 |\n| --- | --- | --- |\n'
             f'| 源M | {source[12]}；{facts}；commands.md、command-*.json、outputs.json | 通过 |\n'
             '| 结构与交付 | check_workspace --day --deliverables；实际退出码见本轮命令收据 | 通过，仅存在性 |\n'
             f'| 完成门禁 | {progress} | '+('通过' if final else '待最终回填')+' |\n\n'+limits+'\n', encoding='utf8')
        (folder/'handoff.md').write_text(common+'\n下一步：'+('继续顺序核对下一既有日；本轮最终收尾统一见D25。' if n<25 else
             '本轮止于D25；D26未开始，清洁安装、真实目标集成与B/C接口接入属于后续任务。')+'\n', encoding='utf8')


def report(records, final=False):
    earlier = {
        6: '登记200个公开候选并保存来源/许可/哈希审计。',
        7: '按来源组筛选、去重并保存排除记录，没有删除失败/重复。',
        8: '10张单标注者参考图，保留并行、返回绑定与Unknown效果。',
        10: '实际合格171条，源目标200条仍差29；按组与哈希隔离开发/留出，选20条开发输入；数量缺口如实保留。',
        11: '20条开发轨迹规范化，原消息位置和歧义保留。',
        12: '规则抽取请求节点与时序关系，不推断缺证据的语义依赖。',
    }
    content = ('# D06–D25 逐日成果与2026-10-30验收\n\n'
               '排除第一周D01–D05。本轮补验D09、D13，并顺序重验既有D14–D25；D06–D08/D10–D12列出既有成果，未改其进度。D26未开始。\n\n'
               '全部行为验收通过后才允许写共享进度表。当前回填状态：'+('已写入并保存重开核验。' if final else '待最终写入。')+'\n\n'
               '| 日任务 | 实际成果与验证 | 限制/证据 |\n| --- | --- | --- |\n')
    for n in range(6,26):
        if n in earlier:
            content += f'| D{n:02} | {earlier[n]} | 既有records/D{n:02}/；本轮全量回归覆盖相关既有断言，不代表新增数据或独立金标。 |\n'
        else:
            content += f'| D{n:02} | {FACTS[n][0]} | {FACTS[n][1]} 证据：{records[n].relative_to(ROOT).as_posix()}/ |\n'
    content += ('\n本轮全量75项通过；历史复核另外4项反例通过，1项旧诊断改用源码与新冻结包的调用前停止探针验证；三例隔离演示均exit0。源DOCX、A:N、全部总览/甘特公式检查通过。结构检查仅验证存在性，不代替行为验收。\n\n'
                '真实模型抽取：20次请求/20个返回，提案结构20 Valid，图完整性18 Valid/2 Invalid；请求别名deepseek-chat，服务响应deepseek-flash。usage为输入142735、输出8130、总计150865 tokens，实际费用未提供。不存在真实目标攻击成功率结论。\n\n'
                '可演示流程与命令见 ../README.md：真实API用于历史步骤抽取，已有响应可离线复核；本地生成—执行—三值检查—重试—预算演示使用release/演示版-1.1/，零真实模型调用。旧1.0包和全部原失败证据保留。\n\n'
                '关键修复：原事件顺序绑定、参数异常逐项拒绝、非字符串工具结构化停止、调用前Pre/Guard门禁、计划累计预算、跨步可见历史。源码和1.1冻结包分别验证。\n\n'
                '剩余研究限制：D10数量差29、单标注者偏差、规则依赖漏提9条、D9节点边界未变与源K期待的关系需导师复核、AL-005/AL-007歧义Invalid。它们保留在结果中；不以API输出替代独立证据。清洁安装、D26后续场景及真实目标接入未在本轮执行。\n\n'
                '本轮无会议；未改原始DOCX、references、B/C文件、data-generation、配置文件或共享忽略规则。收尾/进度拟写/实际重开收据见D25本轮目录及各日excel-final-acceptance.json。\n')
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(content, encoding='utf8')


def prepare():
    state, records, book = context()
    assert dr.digest(book) == state['workbook_before_sha256'], 'Workbook changed since initial read'
    for n, folder in records.items():
        assert dr.command(folder, [sys.executable, '-B', 'scripts/check_workspace.py', '--day', f'D{n:02}', '--deliverables']) == 0
    for argv in [['git','diff','--check','--','.'], ['git','status','--short','--ignored','--untracked-files=all','--','.']]:
        assert dr.command(records[25], argv) == 0
    receipts(records)
    dr.write_json(records[13]/'live-launch-receipt.json', {
        'receipt_type': 'Observed tool completion; not captured subprocess stdout',
        'argv': ['python','-B','scripts/run_d13_live.py','--config','配置文档.md','--output',
                 (records[13]/'live-attempt-01').relative_to(ROOT).as_posix()],
        'tool_session_id': 43012, 'observed_exit_code': 0,
        'evidence': ['live-attempt-01/extractions.jsonl','live-attempt-01/summary.json','live-evidence-check.json'],
        'note': 'Historical live command completion observed in this session; no paid calls repeated to reconstruct capture.'})
    sheets, _ = cw.workbook_cells(book, ('A_核心算法','总览甘特图'))
    proposals = []
    for n, folder in records.items():
        task = dr.MANIFEST['tasks'][n-1]
        old = [sheets['A_核心算法'].get(f'{c}{n+4}', ('',None))[0] for c in 'OPQRSTU']
        assert old[2], 'Original actual start required'
        location = '; '.join(task['deliverables'])
        if n == 25: location += '; algorithm/release/演示版-1.1/'
        evidence = folder.relative_to(ROOT).as_posix()+'; checks.md; commands.md; command-*.json; outputs.json'
        if n == 9: evidence = '原阻塞2026-10-17：无真实隔日复标；2026-10-30解除：间隔326.94小时、5条复标/差异；'+evidence
        if n == 13: evidence = '原阻塞2026-10-17：无真实模型调用；2026-10-30解除：20次DeepSeek HTTP响应/usage、原回复和检查齐全；'+evidence
        values = ['已完成',100,old[2],dr.now().date().isoformat(),location,evidence,
                  '2026-10-30补验/修复完成；原开始日期保留，源计划日期不变。'+FACTS[n][1]+' B/C接口无变更。']
        proposals.append({'day': n, 'row': n+4, 'before_O_U': old, 'proposed_O_U': values,
                          'source_acceptance_M': list(task['source_fields'].values())[12]})
    daily_documents(records)
    report(records)
    dr.write_json(records[25]/'pre-progress-audit.json', audit(records))
    dr.write_json(records[25]/'proposed-progress.json', {'timestamp':dr.now().isoformat(),
                  'all_acceptance_passed':True,'workbook_before_sha256':dr.digest(book),
                  'protected':protected_snapshot(book),'rows':proposals})
    print(json.dumps({'acceptance_passed':True,'proposed_rows':len(proposals),'workbook_unchanged':True}))


def verify():
    _, records, book = context()
    proposal = json.loads((records[25]/'proposed-progress.json').read_text(encoding='utf8'))
    assert protected_snapshot(book) == proposal['protected']
    sheets, _ = cw.workbook_cells(book, ('A_核心算法','总览甘特图'))
    for row in proposal['rows']:
        assert [sheets['A_核心算法'].get(f'{c}{row["row"]}', ('',None))[0] for c in 'OPQRSTU'] == row['proposed_O_U']
        assert (records[row['day']]/'excel-final-acceptance.json').is_file()
    assert dr.command(records[25], [sys.executable,'-B','scripts/check_workspace.py','--sources']) == 0
    daily_documents(records, final=True)
    report(records, final=True)
    for argv in [['git','diff','--check','--','.'],['git','status','--short','--ignored','--untracked-files=all','--','.']]:
        assert dr.command(records[25],argv) == 0
    dr.write_json(records[25]/'final-integrity.json', {'timestamp':dr.now().isoformat(),
                  'workbook_sha256':dr.digest(book),'authorized_rows_updated':len(proposal['rows']),
                  'protected_cells_and_other_zip_parts_unchanged':True,'reopened_values_verified':True,
                  'source_and_overview_formulas_passed':True,'audit':audit(records)})
    print(json.dumps({'updated_rows':14,'reopened_verified':True,'protected_unchanged':True}))


def update():
    _, records, book = context()
    proposal = json.loads((records[25]/'proposed-progress.json').read_text(encoding='utf8'))
    assert proposal['all_acceptance_passed']
    assert dr.digest(book) == proposal['workbook_before_sha256'], 'Refuse stale progress write'
    receipts(records)
    for row in proposal['rows']:
        dr.workbook_update(row['day'],row['proposed_O_U'],records[row['day']],'final-acceptance')
    verify()


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf8')
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['prepare','update','verify'])
    action = p.parse_args().action
    {'prepare':prepare,'update':update,'verify':verify}[action]()
