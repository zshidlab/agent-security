# 毕业研究工作区规范 v2

版本：2.1.0；2026-10-12（v2：2026-10-09）。此次修订由用户明确授权，作为独立 PREP，不是 /szh 迁移 P0-P6，也不是 D3 工程实施。旧版见 [历史规范](history/AGENTS.pre-PREP.2026-09-13.md)，D1/D2 证据见 [历史看板](history/TASK.pre-PREP.2026-09-13.md)。

## 1. 目标与来源

最终问题始终是：TFIR + Joint State + Transition Contract + Execution-Feedback Runtime 能否发现静态模板或离线状态机遗漏的、依赖执行反馈及状态变化的多轮智能体安全违规。更多攻击文本、LangGraph、Schema 合法或模型自述均不构成此贡献。

导师研究计划 docx 是目标依据，只读。阶段路线先提炼领域无关管线、验证数据和隔离平台、公平比较，再进行车载适配、跨模型/Agent 主实验、消融、held-out Flow、Artifact/论文。保留 O1-O10、RQ1-RQ6、D1-D50、G1-G11 全部要求，见 [路线映射](Advisor-Route-Mapping-v2.md)。安全增益只能作为待检验假设。

每次先读本文件、TASK.md、README.md 和当前阶段协议；事实判断只查看 data-generation/、graduation-project/ 的必要文件及适用 AGENTS.md。不得使用其他项目作为依据，不访问 cogdefend/、NemoClaw/OpenClaw 沙盒或 /szh。扩大范围须由对应任务明确授权。

## 2. 分阶段权限

研究准备：仅修改 graduation-project/ 内中文文档、协议、标明 draft 的机器可读契约和清单；data-generation/ 全部只读；导师 docx 不修改。本次不写实现、不安装依赖、不读或录入凭据、不调用 API、不实验、不训练、不部署。

后续工程：看板中拟议代码目录不是当前写权限；实施任务必须明确授权目录、性质、环境、命令与预算。未经授权仍仅文档。禁止把未来阶段标为 DONE，禁止把 PREP 草案当作已实现或已通过运行验证。

不自动 commit/push 或公开发布；不提交缓存、模型、auth store、运行时 checkpoint、生产日志、秘密。保留用户改动；不回退只读研究资产。当前根目录及本目录不是 Git 仓库，用历史副本、文件哈希及可用子仓库 diff 检查范围，不伪造 Git 状态。

## 3. 证据级别

| 级别 | 能支持 | 不能支持 |
| --- | --- | --- |
| 原始计划/冻结协议 | 目标、预注册要求 | 已实现或成功 |
| 离线图/模板/来源 | 路径设计、研究配对 | Runtime 消费、真实记忆/通信 |
| 已读源码/测试定义 | 实现位置、测试覆盖意图 | 本次测试通过 |
| 本次运行 | 指定环境/输入/版本的实际结果 | 未运行模型或领域的结果 |
| 历史记录 | 标明日期范围的历史证据 | 本次复验 |
| 模型文本/fixture/模拟 | 候选或模拟观测 | 真实执行、防护失败、安全发现 |

现行生成器以 constraint/ 和实际源码为源事实；文档愿景不能覆盖源码边界。审计给路径/符号，未知项单列。旧 v1 文档保留，版本地位与勘误见 README.md，旧分母及 PASS/FAIL 不能覆盖新判定协议。

## 4. 架构和安全不变量

通用核心使用 task、resource、principal、permission、environment_state；vehicle_id、车辆工具/状态放领域适配器。不直接改写现有车载 Schema，制定保真、版本化映射。

攻击生成器、被测 Agent、安全 Oracle 隔离；被测端不得获得 gold、攻击目标、Oracle 规则或可信状态写权限。LangGraph 只是编排；研究因果图、生成工作流节点、执行节点分开。迁移仅由可信 Runtime 根据可观察事实和 Contract 决定，不执行模型生成的任意谓词。

只用隔离 Mock，不连接真实车辆、账号、邮件、支付、外传网络或 CAN/ECU。可信层控制权限、策略、确认及状态提交；攻击者不得修改。不得弱化 Guard/PEP、扩大权限、修改预期或 Oracle 制造成功。

关联缺失、畸形消息、超时、Guard/Oracle 不可用、状态冲突均失败关闭并记录原因。提议、尝试、阻断、实际效果分别记录。纯文本泄露/劫持须独立确定性证据，否则 unknown。

## 5. 凭据、判定和比较

真实 key 不进入 prompt、memory、checkpoint、trace、样本、文档或 Git。本次不询问、不读、不输出、不存 key。后续优先 Windows Credential Manager；keyring 必须检查原生后端，禁止默默退回明文，见 [凭据设计](Credential-Plan-v1.md)。现有生成器 DEEPSEEK_API_KEY 规则不在此次修改。

内容、意图、有效性、目标达成、安全违规、良性效用、运行状态使用独立轴；阻断恶意样本仍保留。gold 是生成目标，expected_outcome 是防守预期，actual_outcome 是观测，见 [判定](Outcome-Protocol-v1.md)。

同 path_id 图/模板配对，保留 B0-B4；表示比较控制反馈，反馈比较控制其他条件。冻结 manifest、模型/上下文、权限/状态、seed、轮次/token/API/重试预算和 Oracle；失败/重试/裁判全记账。unsupported/异常/无效不静默删除。按场景/来源/路径/模板家族分组隔离，同源改写和配对样本不得跨 split。held-out Flow 在 Runtime 冻结前不得实现或调参。

## 6. 会话、版本与交接

只执行授权阶段；编辑前说明范围；检查后在 TASK.md 记录来源、命令、环境、结果、Evidence、Blockers、Handoff。文档任务仅做相称的语法/引用/覆盖/一致性检查。所有当前验收通过才 DONE；API、环境和实验能力留待对应门禁。

中文文档，技术标识保留英文。修改冻结版本说明差异、理由和比较影响；保留原版及旧日期。原专利/发布门禁继续有效：私有 PREP 可进行，公开核心细节/Flow/Artifact 前须核实专利提交及发布授权。投稿规则/日期后续复核，不把历史窗口当作当前有效。





# 毕业设计工作区规范

## 1. 目的与范围

本目录用于保存车载/工具型 LLM 智能体多轮安全测试研究的计划、协议、实验记录、论文和 Artifact 材料。实现源码仍位于同级的 `cogdefend/` 和 `data-generation/`，除非任务明确授权，否则不得在本目录复制或修改它们。

研究主题为：

> 使用 TFIR、联合状态（Joint State）、迁移契约（Transition Contract）和执行反馈运行时（Execution-Feedback Runtime）测试车载/工具型 LLM 智能体的多轮安全问题。

**文档语言规则**：今后本目录新增或修改的说明、协议、记录和任务文档默认使用中文。TFIR、Joint State、Transition Contract、AgentDojo、API、Schema、Runtime、Flow、Mock Vehicle 等技术专有名词、论文名和代码标识可以保留英文。

## 2. 每次会话必须先读

1. `AGENTS.md`；
2. `TASK.md`；
3. `Threat Model v1.md`；
4. `Venue Requirement Matrix v1.md`；
5. 需要核对原始计划时读取 `面向TDSC_USENIX_NDSS的车载智能体安全测试研究计划.docx`。该文件只读，绝不能编辑。

涉及实现事实时，只读查看 `cogdefend/` 或 `data-generation/` 中的相关文件，并把路径、版本或日期记录到 `TASK.md`。不得复制完整项目。

## 3. 工作区边界

允许修改的内容仅限本目录内的研究文档、协议、实验清单、结果摘要、论文提纲、Artifact 说明和 `TASK.md`。

禁止：

- 修改研究计划 `.docx`；
- 修改 `cogdefend/`、`data-generation/` 或其他同级目录；
- 写入 API 密钥、Token、凭据、真实个人信息、车辆秘密、生产日志或真实车辆轨迹；
- 提交缓存、临时日志、模型文件或未在任务中定义的原始大文件。

若发现必须修改实现源码，应在 `TASK.md` 记录需求并停止本目录内的实现性修改，由后续独立任务处理。

## 4. 固定安全与研究不变量

1. 所有潜在危险动作只能在 Mock Vehicle 或数字孪生环境中执行，绝不连接真实车辆、CAN 总线、ECU、制动、转向、动力、车门或其他安全关键执行器。
2. 数据生成框架的执行事实必须是进程内本地模拟，并保留 `execution_origin=local_simulation`。
3. 安全发现必须有工具、参数、授权/策略判定、确认状态和/或状态增量等 Hard Observable 证据；仅有危险措辞或 LLM-as-Judge 结论不算发现。
4. 不得弱化 Guard、PEP、策略、验证器或预期结果来让测试通过。
5. 攻击者自报的身份、权限、车辆状态、允许结果和执行结果都必须视为不可信声明。
6. 关联 ID 缺失或冲突、畸形消息、超时、Guard 断开或验证器不可用时必须失败关闭，记录为 `ABORT`、`ERROR` 或 `INVALID`，不得静默记为 `PASS` 或 `FAIL`。
7. 区分恶意目标调用（`gold`）与正常安全环境的预期处理结果（`expected_outcome`）。

跨边界事件应尽量关联：`request_id`、`gateway_session_id`、`graph_thread_id`、`task_id`、`tool_call_id`、`agent_id`、`vehicle_id`。

## 5. 模块化研究结构

| 模块 | 职责 | 典型产物 |
| --- | --- | --- |
| 威胁模型 | 攻击者、资产、攻击面、判定和伦理边界 | `Threat Model vN.md` |
| 投稿要求 | TDSC、USENIX Security、NDSS 的证据要求 | `Venue Requirement Matrix vN.md` |
| 相关工作 | 论文与系统特征比较 | 先前工作矩阵 |
| 问题协议 | RQ、假设、变量、排除规则 | 研究协议 |
| Schema | TFIR、Joint State、Transition Contract、轨迹契约 | Schema 草案 |
| Flow | F1-F8 攻击流程定义 | Flow 清单 |
| 实验 | 模型、Agent、基线、随机种子、预算、指标 | 实验清单 |
| 分析 | 统计计划、路径签名、FPR/MVR/UVP | 分析记录 |
| Artifact | 复现、打包、局限性和伦理 | Artifact 清单 |
| 论文 | TDSC、USENIX、NDSS 论文结构 | 论文提纲/草稿 |

各主题使用独立文档和版本号。修改冻结协议时必须说明改动内容和原因，不得静默覆盖。

## 6. 阶段工作流

1. 读取本文件、`TASK.md` 和冻结输入，确认当前阶段。
2. 只处理当前阶段，不提前开始后续阶段。
3. 编辑前说明目标文件，保持范围最小。
4. 对待评估数据优先使用 Markdown 表格、JSON/YAML Schema、CSV 清单等结构化格式。
5. 检查链接、标识符、必填字段和内部一致性。
6. 在 `TASK.md` 记录命令、来源、结果、阻塞项和交接事项。
7. 只有交付物和验收证据齐全时才能标记 `DONE`，否则保持 `IN_PROGRESS` 或 `BLOCKED`。

不得自动提交或推送，也不得从本目录向真实沙盒部署；除非后续任务明确授权安全的只读验证。

## 7. 证据与可复现性

每个实验或结论至少记录：来源路径及版本/日期、模型和 Provider、Agent 配置、Flow、随机种子、温度/top-p、Token/查询/轮次/重试预算、工具 Schema 和权限快照、原始轨迹或隐私安全摘要、判定字段、排除规则、命令、环境、时间和结果。

尽量使用配对比较，报告样本量、效应量、置信区间和多重比较处理。Semantic State 只能辅助流程控制，必须用人工标注 Gold Set 验证；主要安全结论必须基于 Hard State/Hard Observable。

## 8. 完成标准

任务完成必须同时满足：目标文档存在；内容与冻结威胁模型一致；包含明确验收条件；`TASK.md` 有对应证据。证据不足时必须明确说明，不得把缺失实验写成正面结果，也不得宣称论文必然被录用。


## 分级任务与历史地位

TASK v3父任务由全部子任务完成或人工声明完成；人工声明记录人/时间/来源/理由/未完成项，不伪造结果、不绕过安全门禁。新增V1使用现有生成数据测试独立通用DeepSeek被测Agent；本次仍仅文档。上方嵌入的旧规范全文仅为历史，其其他项目参考权限和旧完成规则不覆盖本版；history原归档保留。
