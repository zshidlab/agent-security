"""Honest elapsed-time gate for single-annotator review."""
from datetime import datetime, timedelta

def review_status(first, second=None):
    if second is None: return {'complete':False,'reason':'second_annotation_not_performed'}
    if first['source_id'] != second['source_id']: raise ValueError('different source')
    a,b=(datetime.fromisoformat(x['annotated_at']) for x in (first,second))
    if a.tzinfo is None or b.tzinfo is None: raise ValueError('timezone required')
    if b-a < timedelta(days=1): return {'complete':False,'reason':'elapsed_less_than_one_day'}
    return {'complete':True,'reason':'single_annotator_only',
            'changed':first['graph']!=second['graph']}
