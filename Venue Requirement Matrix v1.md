# 投稿要求矩阵 v1

**冻结日期**：2026-09-10（D1）  
**用途**：将威胁模型和后续实验结果映射到 TDSC、USENIX Security、NDSS 的审稿证据要求。

| 维度 | TDSC | USENIX Security | NDSS | 本研究统一证据 |
| --- | --- | --- | --- | --- |
| 安全问题 | 完整说明 Agent 安全与可靠性问题 | 必须是明确的系统安全问题 | 必须关联实际系统/CPS 风险 | 依赖执行结果的越权工具调用、策略违规和非法状态改变 |
| 威胁模型 | 攻击者、资产、假设清楚 | 强调攻击者、攻击面、泛化性和现实性 | 说明部署边界和实际攻击路径 | `Threat Model v1` 的能力、资产、攻击面、成功/失败和隔离定义 |
| 主要贡献 | 方法、系统机制、可复用 Benchmark | 优先展示漏检漏洞和安全发现 | 实用系统设计与实现 | TFIR + Joint State + Transition Contract + 在线执行反馈 |
| 安全判定 | 可审计、可重复 | 不得依赖 LLM-as-Judge | 工具、状态和策略链路可解释 | 工具调用、参数、PEP/Guard 判定、确认、状态增量 |
| 基线 | 覆盖模板、离线状态机等 | 强基线并量化漏检 | 与现有工具/Agent 系统比较 | Pure LLM、Template、Offline State Machine、Rule Flow、AgentDojo-style |
| 关键指标 | ASR、TVR、CFR、FPR、Utility | MVR、UVP、Unsafe Tool Invocation、FPR | 可用性、成本、鲁棒性、迁移性 | 配对实验、95% CI、效应量和多重比较校正 |
| 泛化性 | 多模型、多 Agent、多 Flow | 证明不是单一模型现象 | 至少一个接近真实协议/工具的映射 | 6 个以上模型、4 种 Agent、6 个主 Flow、held-out Flow |
| Artifact | 可复现代码、数据和配置 | Open Science Appendix、匿名可运行 | 可部署、可扩展测试平台 | 合成数据、固定种子、轨迹 Schema、运行说明、结果检查器 |
| 伦理与隔离 | 说明局限和双重用途 | 明确安全边界 | 说明车辆/CPS 风险控制 | 只连接 Mock/数字孪生，不连接真实危险执行器 |

## 采用标准

- 威胁模型、成功/失败标准和隔离边界在实验开始前冻结；
- 任何“安全发现”必须有结构化 Hard Observable 证据，文本只能作为输入或语义辅助；
- 每个主要结论至少报告样本量、随机种子、模型/Agent/Flow 条件和置信区间；
- 若 USENIX/NDSS 的真实安全发现、泛化性或 Artifact 条件未满足，不宣称达到投稿门禁，优先保留 TDSC 版本的完整系统与实验材料。
