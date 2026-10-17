# Source acceptance and limits

首次冻结18文件哈希检查通过；隔离运行2失败1通过，生成demo.py换行转义产生SyntaxError。保留失败包待归档。

尚未验收；修复模板转义，失败包归档前run并新run重建；D09/D13未完成，无B/C接口变化。

Actual command evidence: command-*.json. Structure/existence checks do not replace behavior.
New code, research data and JSON/Markdown command evidence are retained; no local cache/environment created. No szh/.gitignore added. Existing D01–D05 files preserved.
