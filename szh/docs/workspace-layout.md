# 工作区结构与路径约定

版本：1.0.0；2026-10-17。适用范围仅为 `agent-security/szh/`，维护责任为 OAPT_A/szh。所有路径默认相对 `szh/`。

## 文件责任

| 层 | 文件或目录 | 维护方式 |
| --- | --- | --- |
| 长期规则 | `AGENTS.md` | 写职责、安全边界、开始流程和完成门槛；不塞入五十日全部细节 |
| 任务导航 | `TASK.md` | 管理全部 A 日任务入口、顺序、排期与临时回填异常；正式状态只在 Excel |
| 任务设计 | `docs/tasks/DNN.md` | 读取该日所需的源任务、步骤、输入、产物、测试和回填位置 |
| 来源快照 | `docs/tasks/manifest.json` | 源文件路径与哈希、A:N 快照、日文档和交付路径；不存动态完成度 |
| 算法工程 | `algorithm/` | A 自己的代码、数据、说明、测试、教程和正式交付 |
| 实际证据 | `records/DNN/<run-id>/` | 每次运行单独保存；记录实际结果，不预填成功；修复不覆盖失败 |
| 工作区维护 | `docs/records/` | 记录文档搭建等维护活动，不冒充 Dn 任务证据 |
| 背景与历史 | 既有研究文档、`drafts/`、`docs/archive/` | 按原内容保留，现行入口只引用所需事实 |

`TASK.md` 是本项目任务管理入口；其文件名没有自动加载或自动调度含义。AGENTS 明确要求读取它，再按需读取单日文档，避免每次把五十日全部方案加载进上下文。

## 工程内路径

原始 A 计划使用 `src/mini_executor.py`、`data/轨迹示例.json`、`说明/研究任务.md` 等相对工程路径。统一映射到 `algorithm/` 下，原文件名不变，不改变交付内容：

```text
algorithm/                         对应 D02 源计划中的独立算法项目
  README.md                        工程说明，当前已存在
  pyproject.toml                   D02 配置导入与测试，执行时创建
  环境/依赖.txt                    D02 实测依赖版本
  src/                             A 算法模块和纯数据适配器
  schemas/                         版本化输入、能力、TestPlan 和事件格式
  data/                            来源清单、公开/合成输入及分组划分
    raw/                           经许可取得的原始公开输入，只保留实际来源
    四场景能力/                    D26 的 Email/File/Calendar/Vehicle
  examples/                        无害、可分发的最小例
  tests/                           行为测试、fixtures、故障样例、回归测试
  results/                         正式比较表与封闭留出结果
  说明/                            方法解释、来源说明、教程与结论边界
  记录/                            源计划指定的阶段自查/复跑/演示文档
  报告/算法阶段成果.docx           D48 正式交付；另留 Markdown 编辑源
  release/                         演示版、算法交付版、最终清单
records/DNN/<run-id>/               对应“另保存当天的实际命令和执行记录”
```

除当前 `algorithm/README.md` 外，上图为后续实施的路径约定，不代表文件已实现。每日日文档列出精确交付和测试路径；额外配套模块属于建议实现方式，可依据真实技术问题调整，但须同步日文档、manifest 与交接，不能减少源验收要求。不要在准备阶段创建空代码、空测试和假结果文件。

`algorithm/记录/` 中的正式周自查、清洁复跑和演示说明引用 `records/` 的实际证据。正式实验汇总放 `algorithm/results/` 并回指逐次证据，避免复制后内容不一致。目录类交付必须包含版本及文件清单。

## 版本、接口与时间

数据记录至少标明 Schema 版本、来源 ID/来源组、Graph/Path/Test/Run ID、任务与资源、目标能力约束、观察等级、预算、结果轴及失败原因；具体字段以执行日的冻结 Schema 为准。Schema 或接口变更注明来源、版本、维护责任、变更日期、兼容性与迁移办法。JSON/JSONL/CSV 使用 UTF-8，日期使用 ISO 格式。

`run-id` 使用真实时间加用途，例如 `20261019T091500+0800-first-run`；重跑另建目录。记录中的环境与命令使用实际值，机器临时路径只作为复现说明，不作为工程依赖。失败、拒绝、重复、Invalid 与 Unknown 全部保留。

## 权威来源和共享边界

四个原始 DOCX 位于 `../../OAPT_*.docx`，完整文件名与哈希在 manifest。共享工作簿位于 `../OAPT_研究方案进度管理_三人员分表与总览甘特图.xlsx`。DOCX 只读；源计划 A:N 不被日文档反向覆盖。实际回填只按当前用户授权处理 A 行 O:U 及相关会议记录，写入受公共约束与环境权限限制。

本次路径安排只改变 A 工作区内部组织，不宣告 B/C 接口改版，不要求 B/C 使用本地目录，也不修改他们的文件。`data-generation/` 和 references 仍只读。统一方案十三周与个人五十日的排期冲突待导师确认。

## 采用这套文档安排的依据

以下官方材料于 2026-10-17 查阅，用于指导智能体文档组织：

- [Codex：AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)：用项目指令说明工作方式及作用范围。
- [Codex：Best practices](https://learn.chatgpt.com/guides/best-practices)：提供明确任务、上下文、验证方式与可检查的结果。
- [Codex：Skills](https://learn.chatgpt.com/docs/build-skills)：技能用于可复用流程；五十个单项目日任务无需各建一个技能。
- [Codex：Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)：工具配置按实际需要添加，无需为任务目录预建配置文件。
- [Codex：Approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)：说明文件不能扩大执行环境赋予的权限。

这里的 `TASK.md`、`docs/tasks/`、`records/` 与 manifest 是针对 OAPT_A 的项目约定，官方没有要求必须使用这些文件名。当前不额外添加 `PLANS.md`、技能包、`.codex/config.toml` 或每目录 AGENTS；有具体重复流程或环境需求后再建立。按用户要求不创建 `szh/.gitignore`，临时产物放系统临时目录，继续执行父级忽略审查。
