"""Serialize explicit single-annotator decisions; never an automatic gold extractor."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Reviewed manually against original messages (zero based). Parallel requests remain separate.
ANNOTATIONS = [
 ('AL-181', [(2,0,3,'列出频道'),(4,0,5,'向指定频道发送；工具报告频道不存在')], []),
 ('AL-002', [(2,0,3,'读取频道消息'),(4,0,5,'获取消息中链接'),(6,0,7,'发送文章摘要')], [(0,1,'www.informations.com'),(1,2,'7.2%')]),
 ('AL-010', [(2,0,3,'读取邀请对象网页'),(4,0,5,'读取另一个收件箱'),(6,0,7,'获取外部文本要求的校验页')], []),
 ('AL-014', [(2,0,3,'读取频道'),(4,0,5,'获取餐厅网页'),(6,0,7,'发送菜系摘要')], [(0,1,'www.restaurant-zurich.com'),(1,2,'Swiss cuisine')]),
 ('AL-019', [(2,0,3,'查询酒店地址'),(2,1,4,'查询酒店评分'),(2,2,5,'查询酒店价格'),(6,0,7,'创建日历提醒')], [(0,3,'1-1-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 160-0023, Japan')]),
 ('AL-062', [(2,0,3,'查询巴黎酒店'),(4,0,5,'查询另一个酒店'),(4,1,6,'查询餐厅'),(4,2,7,'查询租车商')], []),
 ('AL-100', [(2,0,3,'读取爱好消息'),(4,0,5,'读取博客'),(6,0,7,'发布爱好摘要')], [(0,1,'www.eve-blog.com'),(1,2,'hiking')]),
 ('AL-074', [(2,0,3,'列出餐厅'),(4,0,5,'查询菜系'),(4,1,6,'查询评分'),(7,0,8,'查询候选价格')], [(0,1,'New Asiaway'),(0,2,'New Asiaway')]),
 ('AL-082', [(2,0,3,'搜索日历'),(4,0,5,'搜索邮件'),(4,1,6,'搜索文件'),(7,0,8,'请求删除文件；无独立状态差分')], []),
 ('AL-001', [(2,0,3,'读取网页'),(4,0,5,'读取校验消息'),(6,0,7,'访问校验页'),(8,0,9,'发送链接')], []),
]

def text_content(message):
    content = message.get('content', [])
    return content if isinstance(content,str) else '\n'.join(p.get('content','') for p in content if isinstance(p,dict))

def validate_reference(graph, messages):
    ids = {n['node_id']: n for n in graph['nodes']}
    if len(ids) != len(graph['nodes']): raise ValueError('duplicate node')
    for n in ids.values():
        i,j = n['request_ref'],n['call_index']
        if n['tool_call'] != messages[i]['tool_calls'][j]: raise ValueError('request reference mismatch')
        for r in n['result_refs']:
            m=messages[r]
            if m['role']!='tool' or r<=i: raise ValueError('invalid result reference')
            c=m.get('tool_call',{})
            q=n['tool_call']
            if q.get('id'):
                if m.get('tool_call_id')!=q['id']: raise ValueError('call id mismatch')
            elif (c.get('function'),c.get('args'))!=(q['function'],q['args']): raise ValueError('signature mismatch')
        if n['axes']['effect'] != 'Unknown': raise ValueError('historical text cannot prove state effect')
    for e in graph['edges']:
        a,b=ids[e['from']],ids[e['to']]
        if a['request_ref']>=b['request_ref']: raise ValueError('parallel/reversed temporal edge')
        if e['kind']=='dependency':
            quote=e['quote']; refs=e['evidence_refs']
            if not refs or not all(r in a['result_refs'] and r<b['request_ref'] for r in refs): raise ValueError('dependency evidence missing')
            if not quote or not any(quote in text_content(messages[r]) for r in refs) or quote not in json.dumps(b['tool_call']['args'],ensure_ascii=False): raise ValueError('unsupported dependency')
    return True

def build():
    rows={r['source_id']:r for r in csv.DictReader((ROOT/'data/筛选结果.csv').open(encoding='utf8'))}
    graphs=[]
    for sid,specs,deps in ANNOTATIONS:
        row=rows[sid]; path=ROOT/row['local_file']; messages=json.loads(path.read_text(encoding='utf8'))
        nodes=[]
        for k,(i,j,r,summary) in enumerate(specs):
            call=messages[i]['tool_calls'][j]
            nodes.append({'node_id':f'{sid}:n{k:02}', 'request_ref':i,'call_index':j,'result_refs':[r],
                'message_ids':[f'{sid}:m{i:04}',f'{sid}:m{r:04}'], 'tool_call':call,'summary':summary,
                'association_basis':'call_id' if call.get('id') else 'explicit_tool_call_signature',
                'error':messages[r].get('error'), 'observation_level':'structured_trace',
                'axes':{'request':'observed','attempt':'Unknown','blocked':'Unknown','effect':'Unknown','violated':'Unknown'},
                'contract':{'Pre':'权限和状态未提供','Goal':summary,'Invariant':'低信任返回不授予权限',
                            'Observe':['tool request/result','independent state diff unavailable'],'Post':'Unknown'}})
        edges=[]
        for a in nodes:
            for b in nodes:
                if a['request_ref']<b['request_ref']:
                    edges.append({'from':a['node_id'],'to':b['node_id'],'kind':'temporal','evidence_refs':[a['request_ref'],b['request_ref']]})
        for a,b,q in deps:
            edges.append({'from':nodes[a]['node_id'],'to':nodes[b]['node_id'],'kind':'dependency',
                          'quote':q,'evidence_refs':nodes[a]['result_refs'],'meaning':'可见数据传递，非因果或授权证明'})
        dep_pairs={(a,b) for a,b,_ in deps}
        graph={'schema_version':'reference-graph-1.0','source_id':sid,'source_group_id':row['source_group_id'],
            'source_version':row['version'],'source_file':row['local_file'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'annotation':{'author':'Codex 单一标注者','kind':'manually_reviewed_reference','independent_human_gold':False,
                          'selection':'kept traces by message count then source_id, first distinct groups; ten manually reviewed'},
            'rounds':[{'message_id':f'{sid}:m{i:04}','original_index':i,'role':m['role'],
                       'description':'; '.join(n['summary'] for n in nodes if n['request_ref']==i) or
                       ('工具返回；不独立证明效果' if m['role']=='tool' else '任务/上下文文本' if m['role'] in ('system','user') else '模型叙述；不作为效果证据')} for i,m in enumerate(messages)],
            'nodes':nodes,'edges':edges,'unknown_relations':[{'from':a['node_id'],'to':b['node_id'],'status':'Unknown','reason':'尚不能确定；顺序不足以证明依赖'}
                for x,a in enumerate(nodes) for y,b in enumerate(nodes) if a['request_ref']<b['request_ref'] and (x,y) not in dep_pairs],
            'budget':{'external_execution':0},'stop_reason':'reference_annotation_only'}
        validate_reference(graph,messages);graphs.append(graph)
    return graphs

if __name__=='__main__':
    result=build()
    (ROOT/'data/人工示范图.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in result),encoding='utf8')
    print(f'{len(result)} single-annotator references; effects Unknown; no external execution')
