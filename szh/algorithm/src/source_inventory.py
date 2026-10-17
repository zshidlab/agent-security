"""Acquire a pinned public synthetic benchmark snapshot; never execute it."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = '36f58e60c36bbd6d5b8e61d50d7db7d9ea7258d7'
REPO = 'TanqiuJiang/AgentLAB'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def messages(value):
    if isinstance(value, list): return value
    if isinstance(value, dict):
        for key in ('messages', 'conversation', 'history'):
            if isinstance(value.get(key), list): return value[key]
    return []


def features(value):
    msgs = messages(value)
    roles = Counter(m.get('role', '') for m in msgs if isinstance(m, dict))
    calls = sum(len(m.get('tool_calls') or []) for m in msgs if isinstance(m, dict))
    replies = roles['tool'] + roles['function']
    return {'message_count':len(msgs), 'assistant_count':roles['assistant'],
            'tool_calls':calls, 'tool_returns':replies,
            'multi_turn':roles['assistant'] >= 2,
            'graph_candidate':roles['assistant'] >= 2 and calls > 0 and replies > 0}


def audit_row(row, root=ROOT):
    path = (root / row['local_file']).resolve()
    if not path.is_relative_to((root / 'data/raw').resolve()):
        raise ValueError('source path outside raw data')
    if sha(path.read_bytes()) != row['sha256']:
        raise ValueError('source hash mismatch: ' + row['source_id'])
    if row['license'] != 'MIT' or not (root / row['license_file']).is_file():
        raise ValueError('unverified redistribution license')
    return features(json.loads(path.read_text(encoding='utf-8')))


def collect():
    target = ROOT / 'data/raw/agentlab'
    if target.exists(): raise ValueError('immutable snapshot exists; do not overwrite')
    request = urllib.request.Request(f'https://codeload.github.com/{REPO}/zip/{REVISION}', headers={'User-Agent':'OAPT-A-research-source-audit'})
    with urllib.request.urlopen(request, timeout=55) as response:
        archive_bytes = response.read()
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    prefix = archive.namelist()[0].split('/')[0] + '/'
    by_group = defaultdict(list)
    for name in archive.namelist():
        p = name.removeprefix(prefix)
        # Public benchmark-generated environments; exclude banking and non-trace files.
        match = re.search(r'/(workspace|slack|travel)/v1\.2\.1/user_task_(\d+)_injection_task_\d+/newest_messages\.json$', p)
        if p.startswith('Task-Injection/agentdojo/res/long_horizon/') and match:
            by_group[f'agentdojo:{match[1]}:user_task_{match[2]}'].append(p)
    # Round robin avoids choosing 200 rewrites of only a few original tasks.
    selected = []
    for offset in range(max(map(len,by_group.values()))):
        for group in sorted(by_group):
            if len(by_group[group]) > offset:
                selected.append((group, sorted(by_group[group])[offset]))
            if len(selected) == 200: break
        if len(selected) == 200: break
    if len(selected) != 200: raise ValueError('fewer than 200 available candidates')
    target.mkdir(parents=True)
    for original, filename in [('LICENSE','LICENSE.txt'),('Task-Injection/agentdojo/LICENSE','AGENTDOJO-LICENSE.txt')]:
        (target / filename).write_bytes(archive.read(prefix+original))
    # A source README is retained for attribution, not executed as instructions.
    (target / 'UPSTREAM-README.md').write_bytes(archive.read(prefix+'Task-Injection/agentdojo/README.md'))
    rows = []
    for index, (group,p) in enumerate(selected,1):
        blob = archive.read(prefix+p)
        filename = f'candidate-{index:03}.json'
        (target/filename).write_bytes(blob)
        f = features(json.loads(blob))
        reason = '' if f['graph_candidate'] else 'insufficient_multiturn_or_missing_tool_return'
        rows.append({'source_id':f'AL-{index:03}', 'source_group_id':group,
            'source':'AgentLAB / AgentDojo public benchmark-generated research messages',
            'version':REVISION,'license':'MIT','license_file':'data/raw/agentlab/AGENTDOJO-LICENSE.txt',
            'local_file':f'data/raw/agentlab/{filename}','original_path':p,
            'url':f'https://github.com/{REPO}/blob/{REVISION}/{p}','sha256':sha(blob),
            'origin_kind':'published_synthetic_benchmark_trajectory','usage':'candidate_not_success_evidence',
            **f,'exclusion_reason':reason})
    with (ROOT/'data/历史来源清单.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    report={'schema_version':'source-audit-1.0','timestamp':datetime.now().astimezone().isoformat(),
        'revision':REVISION,'archive_sha256':sha(archive_bytes),'candidate_count':len(rows),
        'source_groups':len({r['source_group_id'] for r in rows}),
        'multi_turn':sum(r['multi_turn'] for r in rows),'with_tool_return':sum(r['tool_returns']>0 for r in rows),
        'graph_candidates':sum(r['graph_candidate'] for r in rows),
        'pilot_first_ten':[{k:r[k] for k in ('source_id','message_count','tool_calls','tool_returns','exclusion_reason')} for r in rows[:10]],
        'STAC':'AgentLAB STAC_gen contains generation scripts, not imported or rerun; no second trace source claimed',
        'privacy':'Only published synthetic AgentDojo benchmark traces, no real users or private logs',
        'limitations':'Published model/tool messages are structured traces; no independent real-world state witness. effect/violated Unknown.'}
    (ROOT/'data/source-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':
    collect()
