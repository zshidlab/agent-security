"""Offline transport boundary tests; never read the user's credential."""
import io
import json
import urllib.error
import pytest
from deepseek_adapter import DeepSeekAdapter


def test_transport_redacts_key_and_checks_budget_before_sending(tmp_path):
    key = 'sk-synthetic-test-credential-only'
    config = tmp_path/'config.md'; config.write_text(key, encoding='utf8')
    sent=[]
    def transport(req, **kwargs):
        sent.append(json.loads(req.data))
        return io.BytesIO(json.dumps({'choices':[{'finish_reason':'stop','message':{'content':key}}]}).encode())
    adapter=DeepSeekAdapter(config,max_calls=1,transport=transport)
    assert adapter({'input_data':{'text':'untrusted'}})=='[REDACTED]'
    assert key not in repr(adapter) and key not in json.dumps(adapter.calls)
    with pytest.raises(RuntimeError,match='budget'): adapter({})
    assert len(sent)==1 and sent[0]['messages'][0]['role']=='system'


def test_http_errors_and_incomplete_responses_retain_safe_failures(tmp_path):
    config=tmp_path/'config.md'; config.write_text('sk-synthetic-test-credential-only',encoding='utf8')
    def denied(req, **kwargs):
        raise urllib.error.HTTPError(req.full_url,401,'SECRET ERROR',{},None)
    adapter=DeepSeekAdapter(config,transport=denied)
    with pytest.raises(RuntimeError,match='deepseek_http_401'): adapter({})
    assert adapter.calls[0]['http_status']==401
    assert 'SECRET ERROR' not in json.dumps(adapter.calls)
    adapter=DeepSeekAdapter(config,transport=lambda *a,**kw:io.BytesIO(b'{"choices":[{"finish_reason":"length"}]}'))
    with pytest.raises(RuntimeError):adapter({})
    assert adapter.calls[0]['status']=='error'
