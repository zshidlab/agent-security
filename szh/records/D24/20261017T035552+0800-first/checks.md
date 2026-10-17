# Source acceptance and limits

相关9 tests通过，CLI暴露脚本模块与导入模块异常类型不同，目标超限未被捕获；保留command-02失败。

尚未验收；统一CLI模块入口并增加子进程回归后新run复测。D09/D13缺口保留，无B/C接口修改。

Actual command evidence: command-*.json. Structure/existence checks do not replace behavior.
New code, research data and JSON/Markdown command evidence are retained; no local cache/environment created. No szh/.gitignore added. Existing D01–D05 files preserved.
