# 毕业研究 PREP 索引

版本：2.0.0；2026-10-09。当前任务见 [TASK](TASK.md)。此次为授权的独立准备，未运行模型/API、实现 Runtime 或开始后续实验。

| 交付物 | 内容和地位 |
| --- | --- |
| [AGENTS](AGENTS.md) | 当前权限和研究规范 v2 |
| [现状审计](Current-State-Audit-v1.md) | 路径/符号、证据级别、Top-10 覆盖与缺口 |
| [导师与路线映射](Advisor-Route-Mapping-v2.md) | O/RQ/D/G 逐项映射和重排理由 |
| [通用架构与平台](Architecture-Platform-v1.md) | 核心/迁移、LangGraph 被测平台、两类非车载 Mock |
| [凭据设计](Credential-Plan-v1.md) | 一次录入、跨终端复用；未读取 key |
| [内容和结果协议](Outcome-Protocol-v1.md) | 独立标签、Oracle、合成配对案例 |
| [比较与泛化协议](Experiment-Protocol-v1.md) | B0-B4、反馈控制、预算、分母/统计与门禁 |
| [草案契约](drafts/contracts.v0.1.json) | 标签/状态/迁移/Trace 必需字段，不可直接部署 |
| [manifest 草案](drafts/scenario-manifest.v0.1.json) | 合成示例、权限/状态/工具/预算与可见性 |
| [风险/依赖/复现](Readiness-v1.md) | 决策、未核实项与 PREP 检查 |
| [下次启动提示](Next-Session-Prompt.md) | 第一个可执行任务 R1，仅文档冻结 |
| [旧规范](history/AGENTS.pre-PREP.2026-09-13.md) / [旧看板](history/TASK.pre-PREP.2026-09-13.md) | 原版历史和 D1/D2 DONE 证据 |

## 版本地位与勘误

导师 [研究计划](面向TDSC_USENIX_NDSS的车载智能体安全测试研究计划.docx) 为 2026-09-09 原始目标，正文/表格已只读提取；原文件未改。旧日期是历史排期；新看板按依赖门禁排序，不表示旧日期已兑现。

[Threat Model v1](Threat%20Model%20v1.md)、[Prior-art Matrix v1](Prior-art%20Matrix%20v1.md)、[Venue Requirement Matrix v1](Venue%20Requirement%20Matrix%20v1.md) 保留 D1/D2 历史成果。此次 v2/PREP 是补充/修订，未把新增泛化设计冒充 D1 已冻结内容。现行工作按以下说明处理：

1. v1 车载主体、vehicle_id 和 Gateway ID 仅用于车载映射；通用核心使用 principal/resource/environment_state，不要求访问旧 Demo。
2. gold/expected_outcome 区分继续保留；旧 PASS/FAIL 是历史迁移术语，当前评测独立轴不能由 Runtime PASS 推导攻击成功。
3. 危险调用分提议、尝试、阻断、实际效果；未执行不计状态违规。纯文本扩展须独立确定性证据，只计入声明的违规类。
4. 原计划 FPR 文字定义实为发现误报占比，本次分别登记 FPR_benign 和 FDR_findings；MVR 仅相对于预注册参考违规集合，不能声称未知全部漏洞的真实漏检率。
5. v1 关于其他项目的陈述是 2026-09-13 历史检查，本次未重读其他项目。文献比较不等于攻击复现；网页、价格和投稿日期未在线复核。
6. 车载环境、6+ 模型/4 Agent、强基线、七类消融、独立 held-out、Artifact/论文和专利要求全部保留。通用 pilot 不能替代导师要求。
7. Threat Model v1 的 INVALID “不计 ASR/MVR”只保留为旧条件分母口径；现行同时报告全部 assigned 的 ITT、预声明 eligible 和 invalid/unsupported 率。其 gateway_session_id/vehicle_id 强制项仅用于旧车载边界，不强加到通用纯文本事件。

contracts 和 manifest 均 draft/unfrozen。语法/引用检查不代表已实现或已完成实验预注册。未来冻结或修订需另记版本、理由和比较影响。





## 2026-10-12更新

[TASK v3](TASK.md)按分类、层级、时间、依赖和交付物安排，新增I2后的V1真实攻击验证。history全文已整合入对应AGENTS/TASK，原归档保留。下一任务R1，其后I1→I2→V1；未启动实现。

## 2026-10-13 工程交付

已新增 [通用平台](platform/)、[攻击测试入口](platform/attack_test.py)、[样本适配器](platform/sample_adapter.py) 和 [使用手册](使用手册.md)。平台提供 S-DOC/S-EXP 隔离 Mock、可信事件记录、独立 Oracle、DeepSeek provider wiring 和 Direct Agent；离线 fixture 已通过 4 项测试。真实 API、样本读取和正式 V1 pilot 仍按 TASK 的 I2/V1 门禁执行。
