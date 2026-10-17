# Source acceptance and limits

6类参考结果均匹配；错任务/资源/调用不推进；Guard缺失、重复、缺结果、状态版本冲突失败关闭；相关回归9 passed。

三值判断只由同一调用的完整本地观察支持；Unknown不等于Safe；D09/D13缺口保留，未修改B/C接口。

Actual command evidence: command-*.json. Structure/existence checks do not replace behavior.
New code, research data and JSON/Markdown command evidence are retained; no local cache/environment created. No szh/.gitignore added. Existing D01–D05 files preserved.
