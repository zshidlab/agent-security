# 先前工作与相关工作矩阵 v1

**任务**：D2（2026-09-11）  
**目的**：在冻结研究协议前，对智能体安全基准、工具使用安全环境和工作流状态机测试生成工作进行比较。

## 1. 范围与证据纪律

研究计划指定的核心工作包括 AgentDojo、InjecAgent、ToolEmu、ASB，以及“工业软件工作流状态机 + LLM 测试用例生成”。文献元数据沿用研究计划 `[R1]-[R4]`；正式投稿前仍须回查论文原文和官方 Artifact。

本地项目事实只依据以下只读文件：`cogdefend/AGENTS.md`、`cogdefend/demo/agent/src/graph.ts`、`data-generation/README.md`、`data-generation/Vehicle-Agent-Safety-Data-Generation-Architecture.md` 及其 `constraint/` 契约。

- **已记录**：来源明确写出的能力或当前项目文档明确存在的行为；
- **推断**：根据来源范围作出的比较，投稿前必须回查原文；
- **拟验证缺口**：本研究准备实验验证的差异，不是对先前工作的绝对否定。

## 2. 特征矩阵

| 工作 | 主要问题与攻击面 | 环境/工具 | 动态执行反馈 | 状态模型 | 安全判定/证据 | 车辆/CPS 适配性 | 与本研究相关的局限 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **AgentDojo**（Debenedetti 等，NeurIPS 2024） | 工具型 Agent 的 Prompt Injection、防御和任务干扰 | 动态工具环境、用户任务、注入内容和效用任务 | **已记录**：攻击在动态环境中与工具结果交互 | **已记录**：任务/环境状态参与评测，具体字段需回查 Artifact | 任务完成、攻击成功和效用结果；Hard Observable 契约需进一步核对 | 通用工具 Agent，不是车载场景 | 最接近的动态基准，但本研究还需显式联合对话、权限、车辆和工具状态，以及逐边迁移契约 |
| **InjecAgent**（Zhan 等，Findings of ACL 2024） | 工具集成 LLM Agent 的间接 Prompt Injection | 工具任务和携带注入指令的不可信内容 | **已记录**：评估注入是否重定向工具使用；不把通用在线迁移运行时作为核心 | 主要是任务、工具和攻击上下文，不包含车辆状态与权限前置条件 | 以攻击成功率和任务结果为主，Hard Policy/State 证据不是核心贡献 | 无车辆/CPS 状态模型 | 是间接注入的重要基线，但较少覆盖依赖执行结果的车载多轮路径 |
| **ToolEmu**（工具使用安全评测） | 评估 LLM Agent 调用工具时的危险行为 | 通过模拟工具隔离有风险的工具使用 | **已记录**：工具行为被模拟；其反馈是否构成通用自适应迁移契约需回查 | 工具调用上下文和模拟结果，不是车载权限/Hard State Schema | 包含风险评估或 LLM 辅助评测；本研究要求确定性的 Hard Observable 判定 | 为安全隔离提供重要先例，但非车载/CPS | 需要进一步区分候选生成与确定性策略/状态判定，并量化静态方法漏检路径 |
| **ASB**（Agent Security Bench，Zhang 等，ICLR 2025） | LLM Agent 攻击、防御与安全评测的广泛分类和基准 | 多种 Agent 攻击/防御、工具和任务场景 | **已记录**：通过执行评估攻击与防御；是否重点支持联合状态迁移需回查 | 攻击、任务和工具上下文，跨轮 Hard/Semantic 联合状态需核对 | 攻击成功率、效用和防御结果；本研究增加策略、确认和状态增量证据 | 具有广泛 Agent 安全价值，但不是车载数字孪生 | 作为广度基线，本研究聚焦执行依赖违规路径、车辆前置条件和 held-out Flow 扩展性 |
| **工业工作流状态机 + LLM**（Sheng、Wang、Cheng，2026） | 使用工作流状态机约束工业软件测试用例生成 | 工业工作流状态和 LLM 生成测试用例 | 研究计划描述为状态机/路径验证；是否在线执行需回查原文 | 显式工作流状态机 | 关注状态/路径有效性，不是 Agent 安全策略 Oracle | 与 CPS 相邻，但不是车载 Agent 安全基准 | 是最接近的方法学基线，必须实验证明在线执行反馈能发现其漏掉的路径 |
| **当前 CogDefend**（本地项目） | 通过四阶段安全链路处理 Prompt Injection 和不安全座舱工具动作 | Gateway Vehicle Twin、座舱工具、Firewall、AgentGuard、ASV、确认和审计 | **本地已记录**：评估提议动作和车辆孪生状态；当前 Demo Agent 是确定性的离线/LangGraph 风格实现 | 车辆孪生、工具、Guard 和 ASV 状态 | Gateway PEP、Defender 判定、确认、审计和状态变化 | 直接面向车辆/CPS，但动作全部是 Demo/Twin 动作 | 是被测安全系统和研究来源，不是本研究的通用 TFIR Runtime；本目录不得复制或修改它 |
| **当前 data-generation**（本地项目） | 合成车载函数调用、多轮数据、授权和攻击标签 | 契约加载的工具池、授权映射和进程内模拟执行器 | **本地已记录**：记录本地模拟结果/状态增量，不调用真实工具、Gateway、Firewall、AgentGuard 或 ASV | 车辆/环境快照、任务图、工具依赖和授权字段 | Schema/授权/Oracle 确定性校验；`expected_outcome` 是正常安全环境预期，不是运行时判定 | 具备车载形态和安全本地模拟 | 是 Schema 与场景来源，但不是在线对抗运行时或安全发现 Oracle；必须保留 `execution_origin=local_simulation` |

## 3. 与拟议方法的对照

| 能力 | 先前工作的支持 | 本研究要求 |
| --- | --- | --- |
| 多轮攻击自适应 | AgentDojo 等基准提供动态任务交互 | Runtime 根据工具、结果和状态事实选择后继边，Generator 不能单独决定迁移 |
| 间接注入和上下文攻击 | InjecAgent 等提供注入场景 | F2-F5 保留来源可信度、历史上下文、记忆状态和工具效果 |
| 安全工具模拟 | ToolEmu 和 data-generation 提供隔离先例 | Mock Vehicle Runtime 明确 Schema、权限、前置条件、效果、超时和重放契约 |
| 攻击/防御比较 | ASB 提供广泛基准视角 | B0-B4、拟议 Runtime、防御和消融统一输出轨迹 |
| 状态约束生成 | 工作流状态机 + LLM 提供强离线基线 | B2 使用相同目标、模型、预算和工具 Schema 与在线 Runtime 对比 |
| 车辆/CPS 安全 | CogDefend 提供 PEP、Firewall、AgentGuard、ASV 和 Vehicle Twin | 车辆/环境前置条件与确认要求进入 Hard State，危险动作保持在 Mock/DT |
| 确定性安全判定 | CogDefend PEP 和 data-generation Oracle 提供本地先例 | LLM 只提出候选，Runtime/PEP/Guard/Observer 决定迁移和结果 |
| 扩展性 | 现有基准通常在自身 Schema 内增加任务/攻击 | 冻结 Runtime，加入 held-out F7，记录 Runtime 修改行数、节点复用和集成时间 |
| 漏检证据 | 先前工作按各自范围报告攻击/效用结果 | 用结构化路径签名定义 UVP/MVR，并人工复核代表性发现 |

## 4. 最接近工作与差异假设

三种接近性需要分开描述：AgentDojo 是最接近的动态 Agent 基准；InjecAgent 和 ASB 分别提供间接注入与广泛攻击/防御基线；工作流状态机 + LLM 是最接近的离线生成方法基线，ToolEmu 是最接近的安全隔离先例。

因此，本研究不应表述为“生成更多攻击 Prompt”，而应验证：在相同查询预算和工具任务下，结合 TFIR、Hard/Semantic Joint State、逐边 Transition Contract 和在线执行反馈的 Runtime，能否发现静态模板和离线状态机未发现的结构化状态依赖违规路径，同时保持可重放和 Mock Vehicle 隔离。

这只是待验证假设。只有 MVR/UVP、误报审计、跨模型/Agent 复现和 held-out Flow 结果共同支持时，才能形成安全贡献。

## 5. 投稿前必须补充的核查

- 回查五项工作的论文原文和官方 Artifact，把所有“推断”替换为准确引用、版本和章节；
- 记录各基准的工具数量/类型、攻击预算、任务状态、评测 Oracle、模型/Agent 配置和防御设置；
- 核对是否支持多轮状态变化、自适应攻击分支、确定性工具结果和可重放轨迹；
- 直接核查工作流状态机论文的在线/离线执行细节；
- 在不连接真实危险服务的前提下，将至少一个公开非车载工具 Schema 映射到拟议 Mock Tool 契约。

## 6. D3 决策规则

1. B2 必须是与拟议 Runtime 使用相同目标、模型、预算和工具 Schema 的公平离线基线；
2. AgentDojo/ASB 的广度只能作为基线背景，不能声称本研究在所有维度支配它们；
3. 主要安全终点是 Unsafe Tool Invocation、UVP 和 MVR，TVR/CFR/SVR 是系统质量终点；
4. 任何差异主张都必须由可复现实验证据支持，不能仅凭矩阵中缺少某一功能得出。

## 7. 研究计划中的参考文献

- `[R1]` Debenedetti 等，*AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*，NeurIPS 2024。
- `[R2]` Zhan、Liang、Ying、Kang，*InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents*，Findings of ACL 2024。
- `[R3]` Zhang 等，*Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents*，ICLR 2025。
- `[R4]` Sheng、Wang、Cheng，*Test Case Generation Method Based on Industrial Software Workflow State Machine and Large Language Model*，Fuzzy Systems and Data Mining XI，2026，DOI：10.3233/FAIA251652。
- ToolEmu 在研究计划的背景和相关工作部分被列出；正式引用信息和 Artifact 版本需按第 5 节补充。
