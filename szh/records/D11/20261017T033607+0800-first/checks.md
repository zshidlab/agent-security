# Source acceptance and limits

20输入逐条原消息与序号无损对账；请求/返回/状态差分分事件；缺失/重复/跨任务及null边界3 tests passed，实际计数见command-01。

修复首跑null列表错误，前次失败见20261017T033441+0800-first；D09隔日复查未完成；本地解析独立验收，B/C接口不变。

Actual command evidence: command-*.json. Structure/existence checks do not replace behavior.
New code, research data and JSON/Markdown command evidence are retained; no local cache/environment created. No szh/.gitignore added. Existing D01–D05 files preserved.
