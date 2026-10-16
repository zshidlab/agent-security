# 毕业研究分级任务看板 v3

版本：3.0.0；2026-10-12。参考 data-generation/TASK.md 的分类和嵌套勾选，增加时间顺序、依赖和一级交付物。实际目录为 graduation-project/（请求中的 graduation/ 按此处理）。

## 完成、状态与授权规则

- 父任务完成条件：全部子任务完成（递归），或人工明确声明父任务完成。
- 人工完成记录声明人、时间、来源原话、理由、未完成子项及影响，标记 DONE（人工声明）；不得伪造子项证据，不绕过安全/费用/发布门禁；下游仍检查必要输入。
- TODO未开始；IN_PROGRESS当前授权；BLOCKED真实外部依赖；DONE交付验收完整。P0近期关键链，P1导师必需，P2后续接口。
- 当前活动 DOC-REV：本次文档重组；PREP历史DONE；其余任务全TODO。本次不实现、不读取key、不调用API、不安装、不实验、不训练、不部署、不commit/push。
- 现有DeepSeek key是用户声明资源，其后端、位置及有效性尚未核实，不能算I2完成。
- 每子项执行时登记状态、Evidence、Blockers、Handoff。人工声明不自动勾选未完成子项。

导师最终目标保持 TFIR + Joint State + Transition Contract + Execution-Feedback Runtime。V1验证生成数据对独立通用被测Agent的实际攻击效果，不替代强基线、完整模型/Agent矩阵、消融、held-out、Artifact与论文。

## 时间顺序和一级交付物

T为相对顺序，不是工期或批准日期；实际起止日期执行时登记。旧日期完整保留于历史附录。

| 顺序 | 一级任务/分类 | 优先级 | 依赖 | 状态 | 完成交付物 |
| --- | --- | --- | --- | --- | --- |
| T0 | PREP 前置准备（文档） | P0 | 无 | DONE（历史2026-10-09） | 审计、映射、架构、凭据、判定、比较、草案和交接 |
| T1 | R1 研究协议冻结（文档） | P0 | PREP | TODO | Research Protocol v1、通用威胁补充、pilot manifest、预算与授权清单 |
| T2 | I1 隔离 Mock 与 Observer（代码及离线测试） | P0 | R1 | TODO | Mock/PEP/Oracle、reset/replay、测试报告 |
| T3 | I2 通用 LangGraph + DeepSeek 被测 Agent（代码及受限 API 验证） | P0 | I1 | TODO | Direct Agent、provider、凭据加载和 capability/smoke 报告 |
| T4 | V1 现有生成数据的真实攻击有效性验证（数据适配及小规模真实模型实验） | P0 | I2及R1冻结规格 | TODO | 来源 manifest、映射 sidecar、支持矩阵、脱敏 trace、pilot 报告 |
| T5 | I3 TFIR/Contract 执行反馈运行时（代码与验证） | P1 | V1；技术输入I1/I2 | TODO | Parser/Compiler/Interpreter/Validators/Joint State、F1-F6和冻结记录 |
| T6 | X1 公平基线比较 pilot（基线代码及实验） | P1 | I3及I2/V1 | TODO | B0-B4、30对支持矩阵、比较和G6报告 |
| T7 | X2 泛化与语义 Gold（代码、标注及实验） | P1 | X1 | TODO | Gold、extractor、A1-A4、泛化/污染审计报告 |
| T8 | A1 车载领域适配（适配代码及Mock实验） | P1 | X2（排期）；X1（技术） | TODO | vehicle adapter、兼容/领域留出/效用报告 |
| T9 | X3 主实验与防护评测（正式实验及分析） | P1 | X2+A1及预算冻结 | TODO | 主表/CI、脱敏轨迹、违规路径、防护矩阵 |
| T10 | X4 消融、held-out与鲁棒性（代码及独立盲测） | P1 | X3及I3/A1封存 | TODO | 七消融、F7、扩展性/鲁棒性/G9报告 |
| T11 | T1 数据与训练接口（文档及导出代码/离线验证） | P2 | X3+X4（排期）；接口可在X1后设计，标签等X2/X3 | TODO | 导出接口、数据字典、许可/split/标签审计和训练门禁 |
| T12 | W1 Artifact、论文与发布（复现及文档） | P1 | X3+X4+T1 | TODO | RC1/RC2、独立复现、D46-D50稿件/门禁 |

主链：PREP→R1→I1→I2→V1→I3→X1→X2→A1→X3→X4→T1→W1。
I3技术上可在I1后开展离线工作，但当前优先V1；A1技术依赖X1，排在X2后；T1设计可在X1后，完整交付等X3/X4。调整或并行须记录理由和输入条件，不自动启动。

## 分类与分级子任务

文档只写graduation-project/。后续代码拟写其中platform/，实验拟写experiments/和analysis/，导出协议拟写data-protocols/；每次实施必须另明确目录、环境、命令和预算授权。data-generation/及导师docx只读；缺数据时不得擅自生成。
当前文档检查用PowerShell/Python标准库；工程选择并记录固定环境后运行实际新增测试，例如python -m pytest platform/tests；实验CLI与预算在实施时登记，不虚构已存在命令。Mock不连接真实账号/车辆/外部sink，网络仅批准provider。
依据：[架构](Architecture-Platform-v1.md)、[凭据](Credential-Plan-v1.md)、[判定](Outcome-Protocol-v1.md)、[比较](Experiment-Protocol-v1.md)、[映射](Advisor-Route-Mapping-v2.md)。

### PREP：前置准备

- [x] PREP 一级任务（文档）
  - [x] PREP.1 完成现状审计及导师目标映射
  - [x] PREP.2 完成架构、平台和凭据设计
  - [x] PREP.3 完成判定、比较、泛化与契约草案
  - [x] PREP.4 完成引用、覆盖和只读完整性验收

**顺序/依赖**：依赖无；内部 PREP.1→PREP.2→PREP.3→PREP.4，后项使用前项产物。

**一级交付物**：审计、映射、架构、凭据、判定、比较、草案和交接。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：PREP证据保留于v2全文和Readiness-v1.md，无PREP外部阻塞；交接R1。

### R1：研究协议冻结

- [ ] R1 一级任务（文档）
  - [ ] R1.1 冻结研究假设、合法任务、攻击目标、入口和独立结果轴
  - [ ] R1.2 冻结 V1 抽样、控制组、规模、预算与停止规则
  - [ ] R1.3 冻结工具、权限、Oracle、trace、split和映射规格
  - [ ] R1.4 登记模型/环境/复核资源及私有专利交底，明确后续代码授权边界

**顺序/依赖**：依赖PREP；内部 R1.1→R1.2→R1.3→R1.4，后项使用前项产物。

**一级交付物**：Research Protocol v1、通用威胁补充、pilot manifest、预算与授权清单。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置PREP待完成，环境资源执行时核实；交接时间表下一任务。

### I1：隔离 Mock 与 Observer

- [x] I1 一级任务（代码及离线测试；DONE，离线子任务完成）
  - [x] I1.1 实现 S-DOC/S-EXP 工具、权限、确认与原子状态提交
  - [x] I1.2 实现独立 Observer/Oracle 和完整事件关联
  - [x] I1.3 实现隔离、reset、checkpoint、幂等与重放
  - [x] I1.4 验证良性成功、恶意阻断和异常失败关闭

**顺序/依赖**：依赖R1；内部 I1.1→I1.2→I1.3→I1.4，后项使用前项产物。

**一级交付物**：Mock/PEP/Oracle、reset/replay、测试报告。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：`platform/core.py`、`platform/attack_test.py`、`platform/tests/test_platform.py`；2026-10-13，`PYTHONPATH=graduation-project python -m pytest graduation-project/platform/tests -q`，4 passed。fixture 验证 S-DOC sink 阻断、S-EXP 旧确认阻断、合法新确认提交和 reset 隔离。仅为离线 Mock 证据，不支持真实模型攻击结论；R1冻结仍是正式实验前置。下一步 I2。

### I2：通用 LangGraph + DeepSeek 被测 Agent

- [ ] I2 一级任务（代码及受限 API 验证；IN_PROGRESS）
  - [ ] I2.1 检查原生凭据后端并安全复用现有 key，不枚举或输出密钥
  - [ ] I2.2 固定模型/环境，实现原生工具调用、结果循环、超时重试及 usage 账本
  - [ ] I2.3 实现 LangGraph 编排和轮次/token/API预算，隔离研究目标与 Agent
  - [ ] I2.4 离线测试后，在明确费用授权下完成真实模型最小工具闭环；缺凭据或能力记录 ERROR/UNSUPPORTED

**顺序/依赖**：依赖I1；内部 I2.1→I2.2→I2.3→I2.4，后项使用前项产物。

**一级交付物**：Direct Agent、provider、凭据加载和 capability/smoke 报告。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：已完成 `platform/core.py` 的 OpenAI-compatible `DeepSeekProvider`、Direct Agent 工具结果循环和无密钥失败路径；尚未读取 key、调用 API 或核实原生 tools 能力。真实模型、模型版本、预算、凭据后端和 LangGraph 依赖仍是阻塞项；完成 I2 后交接 V1。

### V1：现有生成数据的真实攻击有效性验证

- [ ] V1 一级任务（数据适配及小规模真实模型实验；TODO）
  - [ ] V1.1 只读选取 data-generation 管线已生成样本，登记 sample_id、文件哈希、Schema、模型和 execution_origin；缺数据时另立生成授权任务
  - [ ] V1.2 保真映射车载工具/权限/状态到 S-DOC/S-EXP；保留原数据，派生集单独报告，无法保真列 UNSUPPORTED
  - [ ] V1.3 构造合法任务与低信任攻击入口，配对无污染、恶意污染、恢复可信来源和含攻击词汇的合法负例；不投递 gold、原 Assistant 目标调用、模拟结果或 Oracle
  - [ ] V1.4 冻结样本、split、模型参数、seed、轮次/token/API/重试/费用上限；每 trial reset，记录真实 DeepSeek 工具闭环
  - [ ] V1.5 独立统计目标达成、其他违规、提议/尝试/阻断/效果、良性效用和终止原因；基于可信工具/策略/状态或确定性文本证据，报告分母、区间和成本
  - [ ] V1.6 复核成功、阻断与未知案例；零成功也可完成验证，不降低策略；单模型不等于泛化或导师 D25

**顺序/依赖**：依赖I2及R1冻结规格；内部 V1.1→V1.2→V1.3→V1.4→V1.5→V1.6，后项使用前项产物。

**一级交付物**：来源 manifest、映射 sidecar、支持矩阵、脱敏 trace、pilot 报告。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：已提供 `platform/sample_adapter.py`，仅生成低信任输入并剔除 gold、expected_outcome、trajectory、tool_result、Oracle/evidence；尚未读取 data-generation 样本、运行生成管线或调用真实 Agent。前置 I2 与 R1 冻结、样本路径/哈希、API预算和人工复核规则待完成；完成后交接 I3。

### I3：TFIR/Contract 执行反馈运行时

- [ ] I3 一级任务（代码与验证）
  - [ ] I3.1 实现 Schema/Parser及至少20检查用例
  - [ ] I3.2 实现 Compiler、K候选、PreValidator和预算
  - [ ] I3.3 实现可信 Joint State、Observer/PostValidator和确定性迁移
  - [ ] I3.4 完成F1至少4分支/30 traces及F2-F6共享运行时；车载G5留A1

**顺序/依赖**：依赖V1；技术输入I1/I2；内部 I3.1→I3.2→I3.3→I3.4，后项使用前项产物。

**一级交付物**：Parser/Compiler/Interpreter/Validators/Joint State、F1-F6和冻结记录。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置V1；技术输入I1/I2待完成，环境资源执行时核实；交接时间表下一任务。

### X1：公平基线比较 pilot

- [ ] X1 一级任务（基线代码及实验）
  - [ ] X1.1 实现B0-B4及固定模板/离线图/在线反馈分离
  - [ ] X1.2 同path_id配对；表示比较控制反馈，反馈比较控制其余条件
  - [ ] X1.3 至少2模型×2 Agent×6 Flow完成D25
  - [ ] X1.4 报告数据质量、路径、ASR/UVP/参考MVR、FPR/Utility、异常、成本及修订

**顺序/依赖**：依赖I3及I2/V1；内部 X1.1→X1.2→X1.3→X1.4，后项使用前项产物。

**一级交付物**：B0-B4、30对支持矩阵、比较和G6报告。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置I3及I2/V1待完成，环境资源执行时核实；交接时间表下一任务。

### X2：泛化与语义 Gold

- [ ] X2 一级任务（代码、标注及实验）
  - [ ] X2.1 至少500节点双人标注、一致性和裁决
  - [ ] X2.2 比较规则/NLI/结构化语义抽取
  - [ ] X2.3 扩展Direct/Planner/Memory/Guarded，落实闭源/开源及六+模型计划
  - [ ] X2.4 验证未见任务/工具/来源/路径/模型家族留出和污染

**顺序/依赖**：依赖X1；内部 X2.1→X2.2→X2.3→X2.4，后项使用前项产物。

**一级交付物**：Gold、extractor、A1-A4、泛化/污染审计报告。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置X1待完成，环境资源执行时核实；交接时间表下一任务。

### A1：车载领域适配

- [ ] A1 一级任务（适配代码及Mock实验）
  - [ ] A1.1 映射工具、单位、权限、状态，旧Schema只读
  - [ ] A1.2 至少4工具类/3权限类/4状态
  - [ ] A1.3 验证版本保真、未知版本拒绝和隔离
  - [ ] A1.4 完成领域留出、良性效用及原G2/G5，不将适配称微调

**顺序/依赖**：依赖X2（排期）；X1（技术）；内部 A1.1→A1.2→A1.3→A1.4，后项使用前项产物。

**一级交付物**：vehicle adapter、兼容/领域留出/效用报告。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置X2（排期）；X1（技术）待完成，环境资源执行时核实；交接时间表下一任务。

### X3：主实验与防护评测

- [ ] X3 一级任务（正式实验及分析）
  - [ ] X3.1 冻结6-8模型×4 Agent×6 Flow×30-50实例×3seed或正式预注册分层范围
  - [ ] X3.2 分批配对实验，记录预算和可信状态
  - [ ] X3.3 复核额外路径、跨模型/Agent及2-3防护
  - [ ] X3.4 完成D28-D35/D41/D42与G7/G8证据，报告负结果

**顺序/依赖**：依赖X2+A1及预算冻结；内部 X3.1→X3.2→X3.3→X3.4，后项使用前项产物。

**一级交付物**：主表/CI、脱敏轨迹、违规路径、防护矩阵。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置X2+A1及预算冻结待完成，环境资源执行时核实；交接时间表下一任务。

### X4：消融、held-out与鲁棒性

- [ ] X4 一级任务（代码及独立盲测）
  - [ ] X4.1 封存Runtime哈希后才由独立作者定义F7
  - [ ] X4.2 统计集成时间、修改LOC、复用与首次成功时间
  - [ ] X4.3 完成Joint/Contract/Hard/Semantic/反馈/K/PreValidator消融
  - [ ] X4.4 验证超时、缺状态、无边、冲突、格式和长上下文

**顺序/依赖**：依赖X3及I3/A1封存；内部 X4.1→X4.2→X4.3→X4.4，后项使用前项产物。

**一级交付物**：七消融、F7、扩展性/鲁棒性/G9报告。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置X3及I3/A1封存待完成，环境资源执行时核实；交接时间表下一任务。

### T1：数据与训练接口

- [ ] T1 一级任务（文档及导出代码/离线验证）
  - [ ] T1.1 定义来源、许可、结果轴、证据级别与版本导出
  - [ ] T1.2 保留良性/阻断恶意，未知标签隔离
  - [ ] T1.3 验证场景/来源/路径/模板家族split及污染
  - [ ] T1.4 分别规定防护训练、适配、权重微调门禁；不执行训练

**顺序/依赖**：依赖X3+X4（排期）；接口可在X1后设计，标签等X2/X3；内部 T1.1→T1.2→T1.3→T1.4，后项使用前项产物。

**一级交付物**：导出接口、数据字典、许可/split/标签审计和训练门禁。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置X3+X4（排期）；接口可在X1后设计，标签等X2/X3待完成，环境资源执行时核实；交接时间表下一任务。

### W1：Artifact、论文与发布

- [ ] W1 一级任务（复现及文档）
  - [ ] W1.1 固定依赖、最小运行、数据字典和隐私审查
  - [ ] W1.2 非开发者复现关键表图及一Flow，记录G10
  - [ ] W1.3 完成方法、实验、相关工作、伦理局限和三venue材料
  - [ ] W1.4 核实专利、发布授权及投稿规则，满足G3/G11才公开

**顺序/依赖**：依赖X3+X4+T1；内部 W1.1→W1.2→W1.3→W1.4，后项使用前项产物。

**一级交付物**：RC1/RC2、独立复现、D46-D50稿件/门禁。

**完成标准**：全部子项和验收证据齐全，或按人工声明规则登记；实验完成是如实执行与报告，不要求攻击必然成功。

**Evidence / Blockers / Handoff**：无本次实现/实验；前置X3+X4+T1待完成，环境资源执行时核实；交接时间表下一任务。

## 会话交接与本次记录

每次记录：日期/ID/状态/实际起止时间；性质/授权目录/命令/环境；子项验收；交付物版本与哈希；Evidence；Blockers及责任方；人工声明（如有）；Handoff及必要输入。

2026-10-12 DOC-REV：重组13个一级任务，新增V1并安排I2后、I3前；history两份全文分别整合入TASK和AGENTS附录，原归档不删除。D1/D2/PREP证据不变；后续全TODO。检查：历史全文匹配、任务ID/子项/依赖、Markdown链接及两份JSON语法；仅修订毕业目录五份文档，无实现/API。

## 历史附录 A：v2看板全文与pre-PREP原文

以下旧活动、许可、顺序和状态只作历史；现行以v3为准。pre-PREP原始日期、D1/D2证据及D3标题/任务行差异完整保留。其他项目读取记录不授权重新访问。

# 毕业研究任务看板 v2

版本 2.0.0，2026-10-09。导师目标与旧日期见 [逐项映射](Advisor-Route-Mapping-v2.md)；原始任务表/证据完整归档于 [历史 TASK](history/TASK.pre-PREP.2026-09-13.md)。新表按依赖门禁，不沿用已经过去的日期作为进度。

## 状态与当前活动

| 字段 | 内容 |
| --- | --- |
| 当前活动 | PREP - 独立前置准备 |
| PREP 状态 | DONE（2026-10-09，仅前置文档验收） |
| 原活动 D3 | 暂停原活动指针；历史标题 IN_PROGRESS/任务行 TODO 原样保留，不认定已完成 |
| 历史 DONE | D1 Threat/Venue；D2 Prior-art；仅历史证据，非本次复验 |
| 后续状态 | 全部 TODO；本次不启动 |
| 当前权限 | 仅 graduation-project/ 文档、草案契约/清单；两目录只读研究，docx 只读 |
| 禁止 | 实现、API、依赖安装、正式试验、训练、部署、commit/push、访问其他项目/沙盒 |
| 导航 | [索引](README.md)、[规则](AGENTS.md)、[验证/依赖](Readiness-v1.md) |

状态：TODO 未开始；IN_PROGRESS 当前授权阶段；DONE 当前交付与证据全满足；BLOCKED 需明确外部资源/研究决策，不以未做后续实验阻塞 PREP。

## PREP 交付与验收

| 编号 | 交付物 | 依赖 / 验收 | 状态 |
| --- | --- | --- | --- |
| P-AUDIT | [现状审计](Current-State-Audit-v1.md) | 两目录必要来源、docx 正文/表格；能力分类/路径符号；不伪造复验 | DONE |
| P-MAP | [路线映射](Advisor-Route-Mapping-v2.md) | O1-O10/RQ1-RQ6/D1-D50/G1-G11 逐项，历史保留 | DONE |
| P-ARCH | [通用架构](Architecture-Platform-v1.md) | 职责隔离、版本兼容、两 Mock、LangGraph/DeepSeek 边界 | DONE |
| P-CRED | [凭据方案](Credential-Plan-v1.md) | OS vault 优先/后端检查/备选 ACL/生命周期；零 key 访问 | DONE |
| P-ORACLE | [判定协议](Outcome-Protocol-v1.md) | 独立结果轴、可信效果、异常、配对合成案例 | DONE |
| P-EXP | [比较与泛化](Experiment-Protocol-v1.md) | B0-B4、反馈因子、预算/分母/CI/split、训练独立门禁 | DONE |
| P-DRAFT | [契约](drafts/contracts.v0.1.json)、[manifest](drafts/scenario-manifest.v0.1.json) | draft 标记、语法与内部引用、无 held-out 实现 | DONE |
| P-HANDOFF | [Readiness](Readiness-v1.md)、[下次提示](Next-Session-Prompt.md) | 风险/决策/版本/检查证据、真实阻塞、首任务 | DONE |

PREP DONE 仅表示 A-H 准备文档与本次文档验收完成；草案未部署、实验预注册未绑定真实资源，绝不表示 G2-G11 或后续工程完成。

## 依赖驱动阶段

“拟议代码目录”只有下一实施任务明确授权才可写，当前不存在写许可。每阶段先读 AGENTS/TASK/指定协议，检查前置 DONE，只做一阶段；示例命令是未来验收类别，不表示本次运行或依赖已存在。

| 阶段 | 性质 / 依赖 | 允许目录与命令/环境 | 完成标准 / Evidence |
| --- | --- | --- | --- |
| R1 研究协议冻结 | 文档；PREP | graduation-project/；PowerShell/stdlib JSON 与引用检查，不 API/安装 | 将当前完整草案绑定后续可用资源、明确 pilot规模/阈值/停止规则、版本哈希、模型清单及授权条件；冻结 Research Protocol/Threat 补充/manifest v1；保留修订日志，专利私有交底。资源未知列条件不伪造批准 |
| I1 通用 Mock/Observer | 代码+离线测试；R1 | 拟 graduation-project/platform/，须单独授权；选定 Python 环境后 python -m pytest platform/tests；不付费 API | DOC/EXP 工具/ACL/确认/原子状态/reset/replay、关联和独立 Oracle；良性成功/恶意阻断/异常失败关闭；可信证据、G4 Hard 层 |
| I2 DeepSeek/LangGraph MVP | 代码+授权 API pilot；I1 | 拟 platform/；固定环境/版本，离线 fixture 测试；有凭据/预算授权后最小 provider smoke | A1 原生 tools/结果循环；OS backend 确认、跨终端加载、脱敏/缺失/撤销；无 key trace；记录真实 usage/失败；不把单模型预试当 D25 |
| I3 TFIR/Contract Runtime | 代码+离线/已授权小验证；I1，模型验证需 I2 | 拟 platform/runtime/、platform/tests/、graduation-project/protocols/；pytest 静态/重放和受限 smoke | Parser≥20 用例；Interpreter/Compiler/K/Pre/Post/Joint/Observer 可信闭环；F1≥4分支/30 traces；F1-F6 共享 Runtime；声明通用冻结范围，车载 G5 待 A1 |
| X1 公平比较 pilot | 基线代码+小实验；I2+I3 | 拟 platform/baselines/、graduation-project/experiments/；冻结环境和带预算 pilot 命令，需实验授权 | B0-B4与配对30资产支持矩阵；控制反馈；至少二模型×二 Agent×六 Flow 的 D25（不足则不通过）；预算/异常/效用/CI；G6 修订或通过 |
| X2 泛化/语义 Gold | 代码+标注+实验；X1 | 拟 platform/、experiments/、graduation-project/data-protocols/；固定模型/提取器命令/环境与预算 | ≥500节点双人/一致率/裁决；规则/NLI/结构化抽取；A1-A4、六+模型计划落实，跨任务/工具/来源/路径/模型家族留出、污染审计 |
| A1 车载领域适配 | 适配代码+Mock实验；X1，泛化结论需 X2 | 拟 platform/adapters/vehicle/；data-generation 仍只读，需明确授权才扩大；固定环境 adapter/replay smoke | O5 四工具类/三权限类/四状态；单位/Schema版本/授权保真，无真实车辆；完成原 G2/G5 范围，领域留出及良性效用 |
| X3 主实验与防护 | 正式实验+分析；X2+A1；预算/矩阵冻结 | 拟 experiments/、graduation-project/analysis/；冻结命令/依赖/seed，预批准分批预算 | 六至八模型×四 Agent×六 Flow×30-50实例×三seed的完整/预注册分层范围；D28-D35/D41/D42；二至三防护、原始轨迹、20-30代表额外路径目标、CI/反例/成本；G7/G8 |
| X4 消融/held-out/鲁棒性 | 代码+独立盲测实验；I3+A1冻结，X3 | 拟 platform/flows/、experiments/、analysis/；封存 Runtime 哈希后独立作者 F7；命令环境固定 | 七消融、异常/长上下文；held-out Runtime LOC/复用/时间；禁止提前编写 F7；G9，负结果如实 |
| T1 数据/训练接口 | 文档+导出接口/离线验证；X1，可信训练标签需 X2/X3 | 拟 platform/export/、data-protocols/；仅合成导出验收，训练命令禁用 | 版本/来源/许可/split/结果轴/证据等级；良性/阻断恶意保留；防护训练与领域微调独立门禁。无权重训练，不把 adapter 称微调 |
| W1 Artifact/论文 | 打包/复现/论文；X3+X4+T1 | graduation-project/；具体打包实现目录另授权；固定环境离线复现，独立复现者执行 | RC1/RC2、独立关键表图与一Flow、G10；D46-D50三venue证据组织/伦理局限/Open Science，核验现行要求；专利提交及发布授权后才公开，G3/G11 |

依赖 DAG：PREP→R1→I1→I2；I1→I3（真实模型部分等 I2）；I2+I3→X1→X2；X1→A1；X2+A1→X3；Runtime 冻结+X3→X4；X1→T1（训练标签验收等 X2/X3）；X3+X4+T1→W1。不同阶段可设计依赖，不在此会话并行启动。

## 历史与修订理由

原 D1/D2 DONE 与 2026-09-13 交接见历史 TASK，不删旧证据，不重现其其他项目访问。D3-D50 的旧日期、交付/验收和门禁逐项保留映射。本次用户明确授权路线/规范修订，优先于旧“当前 D3”活动限制；仅切换当前活动为 PREP，不把 D3 研究冻结等价为本次 draft 完成。

原威胁模型中的 PASS/FAIL、vehicle ID 和 INVALID 排除与现行独立轴/通用 ID/ITT 的差异见 README 版本勘误；v1 文件未覆盖。所有新成功主张均待实验。

## Evidence / Blockers / Handoff

### 2026-10-09 - PREP - DONE

- 范围：授权的 A-H 前置文档、AGENTS/TASK 修订及旧版归档，使用请求的 GPT-6-Astra 执行。
- 来源/版本：见 Current-State-Audit-v1.md；导师 docx 只读；data-generation HEAD 及现有 dirty 标准保留。
- 修改文件：AGENTS.md、TASK.md；新增 README.md、Current-State-Audit-v1.md、Advisor-Route-Mapping-v2.md、Architecture-Platform-v1.md、Credential-Plan-v1.md、Outcome-Protocol-v1.md、Experiment-Protocol-v1.md、Readiness-v1.md、Next-Session-Prompt.md、两份 drafts JSON、两份 history 原版归档；共2改/13新，均在 graduation-project/。
- 命令/环境：PowerShell 5.1、Python 3.12.7；只读 rg/Get-Content、ZIP/XML正文表格提取、Git状态及SHA256；ConvertFrom-Json/Test-Path/Compare-Object及逐项引用检查。详细范围与结果见 Readiness。
- Evidence：11当前Markdown/53链接、77映射行、2JSON、11标签轴/47枚举、8谓词/2场景/8工具通过；10类型/30配对/210节点/180边/120阶段及462来源引用通过；相同133只读文件哈希零差异，历史两份全文匹配；git diff --no-index确认两修订差异（exit 1表示存在预期差异）。
- 范围：data-generation git status只有原有评价标准修改；根/毕业目录无Git，未宣称全工作区clean；导师docx未变；未运行源码测试/API/正式实验，未实施、训练、部署或commit/push。
- Blockers：PREP 无外部阻塞；API/凭据后端/软件版本、模型预算/人员、正式实验与专利发布状态留对应后续门禁，均未冒充已验证。
- Handoff：PREP验收满足后停止，后续全TODO，不启动R1。下次仅按 [启动提示](Next-Session-Prompt.md) 执行R1；本次草案完成不等于未来研究冻结或工程通过。


## ???? B?pre-PREP ?????2026-09-13?

??????D1/D2???D3??/???????????????????????????????

# 毕业设计任务看板

**项目**：车载/工具型 LLM 智能体多轮安全测试  
**计划来源**：`面向TDSC_USENIX_NDSS的车载智能体安全测试研究计划.docx`（只读）  
**研究周期**：2026-09-10 至 2026-11-18  
**工作区规则**：本看板记录的任务只能修改 `graduation-project/` 内文件。

## 状态说明

- `TODO`：未开始
- `IN_PROGRESS`：当前会话可处理
- `DONE`：交付物和验收证据已记录
- `BLOCKED`：存在明确依赖阻塞，不得静默跳过

## 当前状态

| 字段 | 内容 |
| --- | --- |
| 当前阶段 | D3 - 研究问题与安全贡献协议 |
| 总体状态 | IN_PROGRESS |
| 最近完成 | D2 - 先前工作与相关工作矩阵 |
| 下一门禁 | D5 完成后的 G2 |
| 冻结输入 | `Threat Model v1.md`；`Venue Requirement Matrix v1.md` |
| 只读系统 | `cogdefend/`；`data-generation/` |
| 安全边界 | 仅 Mock/数字孪生/本地模拟，不连接真实危险执行器 |
| 文档语言 | 中文；技术专有名词和代码标识保留英文 |

## 阶段看板

### 第一阶段：基础定义

| 编号 | 日期 | 交付物 | 验收条件 | 状态 |
| --- | --- | --- | --- | --- |
| D1 | 2026-09-10 | Threat Model v1；Venue Requirement Matrix | G1 条件满足 | DONE |
| D2 | 2026-09-11 | 先前工作与相关工作矩阵 v1 | 比较 AgentDojo、InjecAgent、ToolEmu、ASB、工作流状态机 + LLM 的攻击面、执行反馈、状态、工具和 Oracle | DONE |
| D3 | 2026-09-14 | Research Protocol v1 | 冻结 RQ1-RQ6、假设、主要/次要指标、排除规则和决策规则 | TODO |
| D4 | 2026-09-15 | Vehicle Tool Model | 至少 4 个 Mock 工具、3 类权限、4 类车辆/环境状态、Schema、效果、策略和单元测试计划 | TODO |
| D5 | 2026-09-16 | Joint State 规范 | Hard/Semantic 字段、更新日志、重放格式、Hard Observable 优先级和 Gold Set 计划 | TODO |

**G2**：D1-D5 均验收通过，攻击者模型、工具/权限模型、状态字段和隔离边界没有未解决歧义。

### 第二阶段：运行时契约

| 编号 | 日期 | 交付物 | 验收条件 | 状态 |
| --- | --- | --- | --- | --- |
| D6 | 2026-09-17 | TFIR Schema | 定义节点、边、Guard、Action、终止和 Flow/Generator 接口 | TODO |
| D7 | 2026-09-18 | Transition Contract Schema | 定义 Pre/Goal/Invariant/Observe/Post、多出口和优先级冲突规则 | TODO |
| D8 | 2026-09-21 | Parser/静态检查协议 | 覆盖未知节点、不可达节点、缺失终止和错误 Guard 引用 | TODO |
| D9 | 2026-09-22 | Flow Interpreter 契约 | 独立于 LLM，实现 `(Node, State, Result) -> Task/Next candidates` | TODO |
| D10 | 2026-09-23 | 专利准备材料 | 核心权利要求候选在公开实现细节前记录 | TODO |

**G3**：D10 完成后再公开核心实现细节或 Flow 定义。

### 第三阶段：运行时与攻击流程

| 编号 | 日期 | 交付物 | 验收条件 | 状态 |
| --- | --- | --- | --- | --- |
| D11 | 2026-09-24 | Generation Compiler 协议 | Contract + State + History 编译为 K 候选生成任务 | TODO |
| D12 | 2026-09-25 | 模型适配器协议 | 至少一个闭源和一个开源模型接口，包含缓存和成本日志 | TODO |
| D13 | 2026-09-28 | Pre-Validator 协议 | Hard 规则、语义约束、排序和重试预算 | TODO |
| D14 | 2026-09-29 | Mock Vehicle Runtime 协议 | 工具执行、权限、效果、超时/异常和重放行为 | TODO |
| D15 | 2026-09-30 | Observer/轨迹 Schema | 回复、工具调用、参数、策略、结果、状态增量和关联 ID | TODO |
| D16 | 2026-10-01 | Post-Validator/迁移协议 | 根据执行结果判定 PASS/FAIL/RETRY/ABORT/ABNORMAL | TODO |
| D17 | 2026-10-02 | F1 流程规范 | 受保护数据/维修记录多轮注入，至少 4 个分支 | TODO |
| D18 | 2026-10-05 | F2-F3 流程规范 | 间接注入和权限假设流程复用契约 | TODO |
| D19 | 2026-10-06 | F4-F6 流程规范 | 上下文、工具选择和状态前置条件流程 | TODO |
| D20 | 2026-10-07 | Runtime v1 冻结记录 | 6 个 Flow、重放、Flow/Runtime 分离、确定性轨迹字段 | TODO |

**G4**：D15 的轨迹和状态更新契约完成。  
**G5**：D20 的端到端 Runtime v1 验收通过。

### 第四阶段：基线与试验

| 编号 | 日期 | 交付物 | 验收条件 | 状态 |
| --- | --- | --- | --- | --- |
| D21 | 2026-10-08 | B0/B1 基线协议 | Pure LLM 和 Template 使用相同目标、预算和模型 | TODO |
| D22 | 2026-10-09 | B2 基线协议 | Offline State Machine + LLM 与在线 Runtime 严格分离 | TODO |
| D23 | 2026-10-12 | B3/B4 基线协议 | Rule Flow 和 AgentDojo-style 使用统一轨迹输出 | TODO |
| D24 | 2026-10-13 | 模型/Agent 矩阵清单 | 模型、A1-A4、Prompt、工具和版本固定 | TODO |
| D25 | 2026-10-14 | Pilot 报告 | 2 模型 × 2 Agent × 6 Flow，检查 ASR/TVR/FPR/成本/失败模式 | TODO |

**G6**：Pilot 显示可行性信号，或记录有依据的 Flow/Threat Model 修订。

### 第五阶段：主实验

| 编号 | 日期 | 交付物 | 验收条件 | 状态 |
| --- | --- | --- | --- | --- |
| D26 | 2026-10-15 | Semantic State Gold Set | 至少 500 个节点、双人标注、一致性和裁决记录 | TODO |
| D27 | 2026-10-16 | Semantic Extractor 验证 | 规则/NLI/结构化抽取比较和 F1 报告 | TODO |
| D28-D30 | 2026-10-19 至 21 | 主实验批次 A-C | 原始轨迹、随机种子、配对基线、模型/Provider 记录 | TODO |
| D31 | 2026-10-22 | 违规分类 | 结构化路径签名和代表性发现人工复核 | TODO |
| D32 | 2026-10-23 | MVR/UVP 结果集 | 验证基线漏检路径并记录代表案例 | TODO |
| D33 | 2026-10-26 | 防御矩阵 | 2-3 类防御，报告 ASR 和 Utility Preservation | TODO |
| D34 | 2026-10-27 | 跨 Agent 分析 | Direct/Planner/Memory/Guarded 对比 | TODO |
| D35 | 2026-10-28 | 跨模型分析 | 6 个以上模型，混合效应分析初稿 | TODO |

**G7**：主实验原始结果齐全。  
**G8**：跨模型/Agent 的安全贡献有证据支持。

### 第六阶段：扩展性、鲁棒性与复现

| 编号 | 日期 | 交付物 | 验收条件 | 状态 |
| --- | --- | --- | --- | --- |
| D36 | 2026-10-29 | Held-out Flow 协议 | Runtime 冻结、独立实现、Runtime 哈希封存 | TODO |
| D37 | 2026-10-30 | 扩展性结果 | 集成时间、Runtime 修改行数、节点复用、首次成功时间 | TODO |
| D38-D39 | 2026-11-02 至 03 | 消融结果 | Joint State、Contract、反馈、Hard/Semantic、K、Validator 消融 | TODO |
| D40 | 2026-11-04 | 鲁棒性表 | 超时、状态缺失、无迁移边、Guard 冲突、格式错误、长上下文 | TODO |
| D41 | 2026-11-05 | 统计分析 Notebook | 排除规则、配对检验、CI、效应量和校正 | TODO |
| D42 | 2026-11-06 | 误报审计 | 人工/规则复核和 FPR 置信区间 | TODO |
| D43 | 2026-11-09 | 外部迁移试验 | 公开/第二领域 Schema 映射，危险动作仍隔离 | TODO |
| D44 | 2026-11-10 | Artifact RC1 | 固定依赖、最小运行、数据字典和隐私审查 | TODO |
| D45 | 2026-11-11 | 独立复现 | 非开发者复现关键表/图和一个端到端 Flow | TODO |

**G9**：消融实验证明机制必要。  
**G10**：独立复现成功，或明确记录阻塞项。

### 第七阶段：论文与投稿门禁

| 编号 | 日期 | 交付物 | 验收条件 | 状态 |
| --- | --- | --- | --- | --- |
| D46 | 2026-11-12 | 安全故事章节 | 引言、Threat Model、贡献 | TODO |
| D47 | 2026-11-13 | 方法/系统草稿 | TFIR、Joint State、Contract、Runtime、实现 | TODO |
| D48 | 2026-11-16 | 实验草稿 | 基线、结果、消融、扩展性、防御、FPR | TODO |
| D49 | 2026-11-17 | TDSC 稿件 v1 | 相关工作、讨论、伦理、局限性和范围检查 | TODO |
| D50 | 2026-11-18 | USENIX/NDSS 提纲和 Artifact RC2 | 13 页结构、Open Science Appendix、实用系统提纲 | TODO |

**G11**：选择证据最充分的投稿路线，不得在安全发现、实用性和可复现 Artifact 不足时宣称达到 USENIX/NDSS 投稿条件。

## 指标契约

主要安全指标：ASR、Unsafe Tool Invocation Rate、Unique Violation Paths（UVP）、Missed Vulnerability Rate（MVR）。

系统质量指标：State Validity Rate（SVR）、Transition Validity Rate（TVR）、Complete Flow Rate（CFR）、Tool Executability Rate、False Positive Rate、Utility Preservation。

扩展性指标：Runtime Modification Rate、Node Reuse Rate、Flow Integration Time。

UVP 必须预注册为结构化签名：`权限状态 × 车辆状态 × 工具 × 违反策略 × 触发节点序列`。

## 会话交接模板

```markdown
### YYYY-MM-DD - Dn - <状态>
- 工作范围：
- 修改文件（仅 graduation-project）：
- 检查过的来源路径/版本：
- 命令、环境和检查结果：
- 证据：
- 阻塞项：
- 下一步交接：
```

## 当前交接记录

### 2026-09-13 - D2 完成，D3 开始

- 工作范围：完成 D2 先前工作比较，并将看板切换到 D3。
- 修改文件：`Prior-art Matrix v1.md`、`TASK.md`，以及本次中文化更新的 `AGENTS.md`。
- 来源：研究计划、当前 CogDefend 文档和 data-generation 文档，均以只读方式检查。
- 核验：所有变更均位于 `graduation-project`；研究计划 `.docx` 和同级项目未修改。
- 下一步：完成研究协议 v1，冻结 RQ1-RQ6、假设、变量、主要/次要指标和排除规则。

## 2026-10-13 V1 十类小规模测试补充记录（不修改代码）

本次用户授权建立测试数据/文档目录并尝试5–10条小规模测试。交付：[测试文档](platform/attack-tests/top10-20261013/测试文档.md)、cases.json、generated-samples.jsonl、results.json、evidence.json、cli-preflight.txt（均位于该目录）。10类各选一条配对路径；15个已有生成样本文件中匹配3类，实际执行3次适配检查。CLI缺凭据检查实际执行，真实API请求0次。V1真实攻击测试保持BLOCKED/未完成，不以离线检查替代。

Evidence：当前CLI未消费--samples，live分支仅打印提示；DirectAgent仅公布fetch_document。工具进程未继承用户终端凭据（仅检查存在性）；未搜索密钥。完整记忆、跨Agent、供应链及确认攻击机制当前不支持。样本/源码哈希及逐项unknown判定见evidence.json/results.json。

Blockers：真实样本执行入口未实现；本进程无凭据；十类完整路径能力及生成样本覆盖不足。Handoff：独立授权代码任务后接通入口、保真映射、工具和预算/trace，先良性闭环再运行支持的5–10条真实攻击。不修改现有历史完成声明；I1历史DONE不能证明checkpoint/replay/完整关联实现，实际源码边界优先，后续须重新验收这些项。
