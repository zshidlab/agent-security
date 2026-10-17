"""Freeze the actual first annotation only. Refuse overwriting it."""
from datetime import datetime
import hashlib,json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
source=root/'algorithm/data/人工示范图.jsonl'
target=root/'algorithm/data/标注自查.jsonl'
rows=[json.loads(x) for x in source.read_text(encoding='utf8').splitlines()][:5]
with target.open('x',encoding='utf8') as stream:
    for graph in rows:
        stream.write(json.dumps({'schema_version':'annotation-review-1.0','source_id':graph['source_id'],
            'annotated_at':datetime.now().astimezone().isoformat(),'author':'Codex single annotator',
            'source_graph_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'graph':graph,'second_annotation':None,'differences':None,'status':'pending_elapsed_day'},ensure_ascii=False)+'\n')
print('Five first annotations frozen; second annotation NOT performed.')
