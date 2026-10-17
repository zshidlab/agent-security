# Source acceptance and limits

3 tests通过且三例退出0，但-I子进程中文stdout使用系统编码，捕获线程解码警告导致证据不完整；不结项。

关联首失败20261017T035735+0800-first，当前冻结包亦保留；修复显式UTF-8输出后新run。D09/D13缺口持续；无B/C接口变化。

Actual command evidence: command-*.json. Structure/existence checks do not replace behavior.
New code, research data and JSON/Markdown command evidence are retained; no local cache/environment created. No szh/.gitignore added. Existing D01–D05 files preserved.
