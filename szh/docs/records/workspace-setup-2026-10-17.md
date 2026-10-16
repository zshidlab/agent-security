# OAPT_A 工作区文档搭建记录

日期：2026-10-17；范围：仅 `agent-security/szh/`。本记录属于工作区维护，不属于 D1–D50 的实际执行证据。

## 变更和来源

建立五十日独立实施文档、源计划快照及路径清单，将 TASK 改为索引，补充结构、执行流程、实际记录模板和只读检查器；保留既有研究资料。AGENTS 保留原有研究边界和 Excel 门槛，补充专用工作区和按需读取日文档规则。

旧 `docs/Next-Session-Prompt.md` 按字节复制为 `docs/archive/Next-Session-Prompt-R1-2026-10-09.md` 后替换当前入口。原件与归档 SHA-256 均为 `2ed6740783e3207f71bb06133091ca9794688db9c1be726e8d8df7b09746cc90`。

只读核对四个 `../../OAPT_*.docx`、共享 Excel、适用 AGENTS 及父级忽略规则；没有读取或修改 zzy/lhy。完整源文件路径、DOCX 哈希与工作簿初始哈希见 [manifest](../tasks/manifest.json)。本次不改变共享接口、计划字段、原 DOCX 或工作簿任何进度。

## 实际验证

实际检查环境：Windows PowerShell；Python 3.12.7。正式检查器仅使用标准库；独立交叉复核使用当前已安装的 openpyxl 3.1.5，未安装新依赖。以下均为本次真实运行结果。

| 检查 | 结果 |
| --- | --- |
| 50 日结构、索引、源摘录与当前链接 | 通过；默认检查以及 D09、D50 单日检查退出码均为 0 |
| 原始 DOCX、A:N 字段与总览引用 | 通过；核对四个 DOCX、700 个字段、50 段源正文、650 个汇总引用、2500 个甘特公式及 50 个负责人公式 |
| 检查器错误检测与只读性 | 通过；缺失 D01 交付退出 1；D51 参数退出 2；临时副本中的源摘录改动、缺失日文档和越界路径均被拒绝；运行前后工作区文件哈希一致 |
| Git 格式、变更范围与忽略审查 | 通过；3 个既有入口文件修改、60 个新增正式文件均位于 szh；无 ignored 文件，无本地 .gitignore，无缓存，无空代码/测试占位文件 |
| 工作簿与四个 DOCX 未变化 | 通过；全部 SHA-256 与搭建时基线相同，D1–D50 仍为未开始、完成度 0 |

可复跑的正式检查（工作目录为 `szh/`）：

```powershell
python -B scripts/check_workspace.py
python -B scripts/check_workspace.py --day D09
python -B scripts/check_workspace.py --day D50
python -B scripts/check_workspace.py --sources
git diff --check -- .
git status --short --ignored --untracked-files=all -- .
```

上述正常命令均退出 0。Git 报告现有 autocrlf 设置下 LF 将在下次 Git 写回时变为 CRLF，此提示不属于格式检查失败。另用 `git check-ignore --stdin` 核对全部正式文件，没有匹配忽略项；对本次维护文本检查了尾随空格和末尾换行。

异常验证由系统临时目录中的 `oapt-verify-workspace-20261017.py` 执行：先运行正常模式，再在临时文档副本上制造源摘录改动和缺文件，不修改仓库原件；独立用 openpyxl 逐项展开并核对总览 A 区全部 3200 个公式。校验脚本执行前后再次比较全部工作区文件及原始来源哈希，确认只读。临时脚本不构成后续运行依赖，正式检查入口为仓库内 `scripts/check_workspace.py`。

首次公式核对发现实施设计错误地假定总览连续复制 A:U；随后按实际工作簿修正为 B:I→A:H、J:N→O/P/S/T/U，保留 O:BL 甘特公式。原始 OOXML 使用共享公式，检查器已支持相对引用展开，并通过独立读取器交叉复核；未为通过检查而修改工作簿。

## 限制和后续入口

所有日任务实施方案尚待实际执行。没有算法代码、行为测试通过结论或真实运行证据；不预建空交付物。D09 隔日复查、D13 模型抽取及 D44 真实调用等条件必须真实满足，未授权部分保留缺口。当前不新增 `szh/.gitignore`，不创建临时环境或缓存到仓库。

下一步由用户授权执行具体 Dn，从 [TASK](../../TASK.md) 与该日文档开始，按 Excel 真实状态回填。统一方案十三周与个人十周路线仍待导师确认；本次目录安排不解决该排期差异。
