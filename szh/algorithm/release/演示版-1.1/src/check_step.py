"""Independent evidence-driven three-valued Contract check, local scope only."""
import argparse
import hashlib
import json
from pathlib import Path
from reference_graphs import ROOT

LABELS = {'True': '已完成', 'False': '明确未完成', 'Unknown': '暂不能确定'}


def state_version(state):
    return hashlib.sha256(json.dumps(state, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()


def check_step(step, events, *, call_id, guard_available=True, expected_before=None):
    result = {'schema_version': 'step-judgment-1.0', 'test_id': step['test_id'],
              'task_id': step['task_id'], 'step_id': step['step_id'], 'path_id': step['path_id'],
              'call_id': call_id, 'value': 'Unknown', 'decision': LABELS['Unknown'],
              'evidence_refs': [], 'ignored_evidence_refs': [], 'missing_fields': [], 'reason': '',
              'advance': False, 'state_versions': {},
              'axes': {'request': 'Unknown', 'attempt': 'Unknown', 'blocked': 'Unknown',
                       'effect': 'Unknown', 'violated': 'Unknown'}}

    def finish(value, reason, missing=()):
        result.update(value=value, decision=LABELS[value], reason=reason,
                      missing_fields=list(missing), advance=value == 'True')
        return result

    if not guard_available:
        return finish('Unknown', 'Guard/观察不可用，失败关闭。', ['guard'])
    if not call_id:
        return finish('Unknown', '缺少绑定调用编号。', ['call_id'])
    resource = step['arguments'].get('appointment_id')
    relevant = []
    for event in events:
        if (event.get('task_id') == step['task_id'] and event.get('test_id') == step['test_id']
                and event.get('step_id') == step['step_id'] and event.get('resource_id') == resource
                and event.get('call_id') == call_id):
            relevant.append(event)
        else:
            result['ignored_evidence_refs'].append(event.get('evidence_id', 'missing'))
    result['evidence_refs'] = [e.get('evidence_id', 'missing') for e in relevant]
    if not relevant:
        return finish('Unknown', '未找到同一任务、资源和调用的证据。', ['matching_event'])
    result['axes']['request'] = 'observed'
    # Preserve all duplicate/conflicting inputs and never select a favorable row.
    if len(relevant) != 1:
        return finish('Unknown', '重复或冲突观察；调用必须有唯一完整结果。', ['unique_consistent_result'])
    event = relevant[0]
    if (event.get('subject') != step['constraint_instance'].get('subject') or
            event.get('arguments') != step['arguments'] or event.get('tool') != step['tool'] or
            event.get('request', event.get('arguments')) != event.get('arguments')):
        return finish('Unknown', '主体、工具或参数不符。', ['matching_identity_tool_arguments'])
    if (event.get('conflict') or event.get('observation_level') != 'Hard Observable' or
            event.get('complete') is not True or event.get('event_type') != 'result' or
            not event.get('evidence_id') or type(event.get('sequence')) is not int):
        return finish('Unknown', '缺少完整 Hard Observable 或存在冲突。', ['complete_hard_observation'])
    missing = [k for k in ('before', 'after') if not isinstance(event.get(k), dict)]
    if 'result' not in event and not event.get('error'):
        missing.append('result_or_explicit_rejection')
    if missing:
        return finish('Unknown', '缺少完成检查必要证据。', missing)
    result['state_versions'] = {k: state_version(event[k]) for k in ('before', 'after')}
    if expected_before is not None and state_version(expected_before) != result['state_versions']['before']:
        return finish('Unknown', '状态版本与本次执行上下文不符。', ['matching_state_version'])
    for pre in step['contract']['Pre']:
        try:
            value = event['before'][pre['collection']][pre['resource_id']][pre['field']]
        except (KeyError, TypeError):
            return finish('Unknown', '前置状态不可观察。', ['Pre'])
        if value != pre['equals']:
            return finish('Unknown', '前置状态冲突。', ['Pre'])
    conditions = step['contract']['Post']
    if not conditions:
        return finish('Unknown', '步骤没有自动确认接口。', ['Post_observable'])
    values = []
    for condition in conditions:
        if (condition.get('kind') not in ('state_equals', 'state_changed_to') or
                condition.get('collection') != 'appointments' or condition.get('field') != 'time' or
                condition.get('resource_id') != resource):
            return finish('Unknown', '不支持或异资源观察条件。', ['valid_condition'])
        try:
            before = event['before']['appointments'][resource]['time']
            after = event['after']['appointments'][resource]['time']
        except (KeyError, TypeError):
            return finish('Unknown', '目标资源的状态差分缺失。', ['target_state_delta'])
        values.append(after == condition['equals'] and
                      (condition['kind'] != 'state_changed_to' or before != after))
    result['axes'].update(attempt=event.get('attempt', 'Unknown'),
                          blocked=event.get('blocked') or 'Unknown',
                          effect='observed' if event['before'] != event['after'] else 'Unknown')
    if all(values) and (event.get('error') or event.get('blocked') == 'observed'):
        return finish('Unknown', '完成状态与拒绝事件相互冲突。')
    return finish('True' if all(values) else 'False',
                  '完整一致的本地状态证据支持完成。' if all(values) else '完整效果检查提供明确未完成反证。')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True); a = p.parse_args()
    rows = [json.loads(line) for line in (ROOT / 'data/阶段判断示例.jsonl').read_text(encoding='utf8').splitlines()]
    checked = [{'example_id': r['example_id'], 'expected': r['expected'],
                'actual': check_step(r['step'], r['events'], call_id=r['call_id'])} for r in rows]
    a.output.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in checked), encoding='utf8')
    print(json.dumps({'examples': len(checked), 'matched': sum(r['expected'] == r['actual']['value'] for r in checked)}))
