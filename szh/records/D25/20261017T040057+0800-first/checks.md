# Source acceptance and limits

冻结包18文件及manifest，三例独立隔离运行全部exit0；逐步报告保留继续/停止理由与Evidence；全套算法68 tests passed；四DOCX及源/总览/甘特公式检查通过。

D25本地演示日验收完成，真实模型调用0；D09仍75%等待真实24h重标，D13仍75%待兼容真实模型20输入实测。失败包分别保留于先前两个D25 run；非真实攻击成功率，未清洁安装、无B/C接口变化。本次停止D25，不启动D26。

Actual command evidence: command-*.json. Structure/existence checks do not replace behavior.

Final closure audit: command-10.json / session-audit.json matches the saved/reopened workbook to daily evidence. Eighteen days accepted; D09 and D13 remain 75% without end dates. Isolated example commands and reports: isolated-demo/actual-commands.json and its three case directories. No D26 execution.
New code, research data and JSON/Markdown command evidence are retained; no local cache/environment created. No szh/.gitignore added. Existing D01–D05 files preserved.
