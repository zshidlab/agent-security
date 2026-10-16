# 现状审计 v1

版本 1.0.0，2026-10-09；源码/测试只读审阅，不是本次执行复验。范围仅 data-generation/、graduation-project/ 及上层规则。导师 docx 通过 ZIP 内 word/document.xml 以 UTF-8 读取段落与表格；未依赖乱码、未改原文。

## 源事实与环境

根目录及 graduation-project/ 无 Git 仓库；data-generation/ 为独立仓库，HEAD 7bcaa37a2dc7a575078ba11de84b8b9b56ca6b8f（2026-10-06）。开始已有 docs/车载智能体安全数据集评价标准.md 用户修改，全部保留。当前工作副本标准 v2.2（2026-10-09）优先于旧提交中的标准，不能把 dirty 文件回退。Windows PowerShell 5.1.26100.9444，Python 3.12.7；未安装/激活环境。

读过的依据：[原始计划](面向TDSC_USENIX_NDSS的车载智能体安全测试研究计划.docx)、三份 v1 文档、原 AGENTS/TASK；data-generation/AGENTS.md、TASK.md、README.md、Vehicle-Agent-Safety-Data-Generation-Architecture.md v3.0、docs/数据合成使用指南.md、docs/合成系统架构图.md、相关流程/GenesisFunc 设计、最新评价标准、docs/长对话恶意攻击类型调研与优先级.md、docs/长对话恶意攻击研究与资产方案.md、attack-paths 全局与十类四文件，以及下表所列必要实现/测试。历史看板记录的 pilot/smoke 等只属历史，本次未重跑、不扩写成功结论。

## 能力分类和定位

下列路径均相对于 data-generation/；“已实现/有测试定义”不等于此次测试通过。

表内 pipeline.py、generation.py、execution.py 等未重复目录的文件名统一指 src/vehicle_data_gen/ 下同名文件；测试均为 tests/，不是历史临时 test/ 产物。

| 分类 | 路径与符号定位 | 事实和边界 |
| --- | --- | --- |
| 已实现/有测试定义 | src/vehicle_data_gen/contracts.py:48 ContractLoader；tests/test_pipeline.py:22 | 从 constraint/ 加载样本/工具/授权/分类/策略契约；根目录 legacy 文件不是运行源。provenance 是资产，不能推断 loader 全部消费 |
| 已实现/有测试定义 | pipeline.py:110 GenerationPipeline.generate；generation.py:SampleAgent、ScenarioCompiler | 冻结目标/身份/状态→生成输入→候选→目标 Oracle→本地模拟→轨迹/静态预期→校验 |
| 已实现/有测试定义 | generation.py:976 AssistantAgent.propose；1126 ActionOracle.select；tests/test_pipeline.py:86,283 | 默认确定性候选；可选 provider callback。Oracle 对齐冻结目标并生成 gold，不是独立被测防守 Agent 或安全 Oracle |
| 已实现/有测试定义 | pipeline.py:430 _turn_count；tests/test_pipeline.py:737 | single_turn=1，multi_turn 随机 5-7；16/32/64 仅未来研究 profile |
| 已实现/有测试定义 | pipeline.py:198 历史合成；tests/test_pipeline.py:296,335,363,377 | 历史重复/派生 gold 调用并各自从初始 state 模拟；有调用/结果/ID 校验，不是连续真实模型交互/状态反馈闭环 |
| 已实现/有测试定义 | generation.py:426 MemoryAgent；tests/test_pipeline.py:512 | 进程内 split 覆盖计数与会话事件元数据，不是持久任务记忆/检索存储 |
| 已实现/有测试定义 | execution.py:12 SimulatedToolExecutor.execute、_initial_overlay、_apply_state_changes；tests/test_pipeline.py:458,481 | 每次 execute 新建 overlay，可模拟单次调用链效果/Schema/前置条件；execution_origin=local_simulation；不执行真实防护/授权 PEP，不访问车/网络 |
| 已实现/有测试定义 | pipeline.py:789 _expected_outcome、966 _validate_expected_outcome；tests/test_pipeline.py:107,283 | Firewall→AgentGuard→ASV 静态期望，不是实际 defense verdict |
| 已实现/有测试定义 | pipeline.py:_validate_sample、_validate_trajectory、_validate_source_boundaries；tests/test_pipeline.py:538,647,665,724 | 标签/授权/调用引用/确认/外部内容/文本边界等确定性检查；Schema 合法不证明攻击有效 |
| 文档设计但未实现 | docs/长对话恶意攻击研究与资产方案.md；graph.json profiles | 自动渐进编排、长轮、摘要转换、持久记忆与执行反馈需另实现 |
| 离线研究资产 | docs/attack-paths/README.md、selection.json、sources.json、十类 graph/templates/README/references | 十类三十路径配对；自然语言观察/边条件，不是可执行 TFIR/Contract |
| 当前不支持 | 全部审阅源码无 graph.json/templates.json 的运行加载路径；attack_taxonomy.py:_PATHS | generator 不消费 Top-10；只消费 constraint/attack_taxonomy.json 等。分类附带的三节点路径注解不等于运行研究图 |
| 当前不支持 | constraint/tool_pool/vehicle_tools.json:memory_read、memory_write | catalog-only，runtime=false、mock=false；可生成候选，不能宣称真实读写记忆 |
| 当前不支持 | 同上 send_message；execution.py:_output_value | mock-only 的固定 sent/message_id，不是真实多 Agent 总线/签名/委派 |
| 当前不支持 | pipeline.py external_content、历史 fixture | 可表达低信任内容；尚无真实工具返回拦截/注入编译闭环，fixture 不算在线注入 |
| 当前不支持 | pipeline.py:1053 export_firewall、1056 export_agentguard、1059 export_asv | 未使用导出桩，不能声称防护训练/评测已接入 |
| 尚待核实 | Provider 原生 tool calling/具体模型服务能力、凭据库后端、依赖版本 | 本次不联网/不读凭据/不装依赖；留 I1/I2/X2 验证 |

工具池共四十项：runtime-backed 8、mock-only 27、catalog-only 5。这是静态声明，runtime-backed 不能当作本次真实环境可调用证据。样本 Schema 1.0.0、工具池 1.2.0、授权表 1.2.0、ASV policy 3；兼容迁移需连同哈希冻结。

## 三种节点不能混用

| 节点 | 来源 | 含义 |
| --- | --- | --- |
| 研究因果节点 | attack-paths/<type>/graph.json | seed/reference/carry/activate 与成功/拒绝/unsupported；turn_slot 是相对槽，不是实际 turn_id；condition 是研究描述 |
| 生成工作流节点 | pipeline.py:398 _attack_path | attack_normalized、template_selected、identity_frozen、state_environment_generated、user_payload_generated、attack_evidence_located、assistant_candidate_generated、oracle_selected、local_simulation、static_security_expectation、trajectory_assembled 共十一项，记录生成步骤 |
| LangGraph 执行节点 | 后续 I2/I3 设计 | Agent 模型/工具/观察/迁移运行节点；当前审阅生成器没有 LangGraph 实现，逻辑 Agent 类不等于真实自主多智能体 |

## Top-10 配对覆盖

| attack_type | 三个同 path_id 图/模板 |
| --- | --- |
| prompt_injection | progressive_reference；tool_return_instruction；summary_laundering |
| agent_goal_hijack | auxiliary_becomes_goal；task_switch；repair_pretext |
| tool_misuse_and_exploitation | forbidden_tool；legitimate_chain；parameter_substitution |
| sensitive_information_disclosure | read_then_route；fragment_reassembly；memory_recall_disclosure |
| memory_and_context_poisoning | query_induced_write；summary_memory；retrieval_trigger |
| identity_and_privilege_abuse | approval_replay；impersonated_delegate；role_alias_confusion |
| human_agent_trust_exploitation | confirmation_scope_drift；repair_trust；hidden_parameter_summary |
| agentic_supply_chain_vulnerabilities | descriptor_rug_pull；tool_shadowing；malicious_component_route |
| excessive_agency | task_scope_expansion；temporary_to_persistent；retry_expansion |
| insecure_inter_agent_communication | spoofed_message；forwarding_laundering；cross_task_replay |

selection 有二十一恶意候选、十个入选；memory_operation 为非恶意对照。sources 有二十一来源、八个便利抽样案例，来源核验日期主要为 2026-10-06；只读继承核验级别，不代表本次浏览/攻击复现。病例重叠、二手/争议来源和宽口径通信归类保留，不能由排序推断总体发生率。人的批准、消息转发、组件加载、检索命中等当前均 fixture/研究抽象，缺能力要 unsupported，不能以同名候选冒充执行。

## Provider 的实际边界

src/vehicle_data_gen/providers/deepseek.py:DeepSeekProvider 继承 openai_compatible.py:OpenAICompatibleProvider。静态默认 deepseek-v4-pro、https://api.deepseek.com/chat/completions；这不是本次 API 版本/价格核验。

| 项目 | 源码行为 | 后续要求 |
| --- | --- | --- |
| 凭据 | __init__: 显式 api_key 或 DEEPSEEK_API_KEY；缺失 RuntimeError | 无原生库；新平台 broker 独立设计，不修改生成器限制 |
| 请求 | complete_json: system/user、temperature=.2、max_tokens=256、json_object | 没有 tools/tool_choice/tool_calls，不是原生 Function Calling |
| 结构化输出 | JSON object 解析，失败尝试提取首尾大括号 | 无严格 JSON Schema；必须另校验，不能自述契约成立 |
| 超时/重试 | 45s、默认 max_retries=2、backoff=.8 指数；HTTP 429/5xx 或无 status 异常重试 | 解析/形状错误无 HTTP code 也可能重试，与文档“格式不重试”有差异；失败 payload 后 value 未赋值路径有待验证的鲁棒性风险 |
| 成本/随机性 | 主要取最后 payload usage；本地声明价格；没有传 seed | 重试/失败用量不可假定零；记录不可确定性；缓存/恢复不是已实现 |
| CLI | cli.py --candidate-generator provider 可生成 JSON actions；默认文本生成，异常可确定性 fallback | 候选 prompt 含目标/工具 schema，不是盲测 defender；fallback 单列，不能算真实模型成功 |
| 测试 | tests/test_deepseek.py 价格计算/缺凭据定义 | 未执行原生工具调用、状态循环、真实 API 测试；本次不运行 |

## 数据判定现状

generation_target_met：冻结恶意 Assistant 目标调用/参数和路径证据；local_result_present：本地模拟结果存在；defense_attack_succeeded：需真实被测防护/策略/状态证据，目前生成管线不提供。三者没有蕴含关系。

gold 是候选目标调用及参考回复，仍为 proposed；expected_outcome 是静态安全期望；actual verdict 必须由后续隔离平台 Observer/Oracle 产生，禁止拿 gold 对齐当真实安全攻击成功。

当前 malicious 正例过滤目标调用，拒绝另存 negative/evaluation；未来攻击评测试验保留阻断恶意样本，不能套用生成正例筛选来提高 ASR。v2.2 A1-A9 是数据质量，A10 JEV 是独立分类 sidecar（隐藏标签、置信阈值 .70，macro-F1 .85/benign FPR .05 是目标），均不等于真实攻击效果。标准已明确有待实现项，本次未逐条复验 CLI 实现符合 v2.2；不把文档阈值当达成。

结论：可以复用契约、候选流程、模拟/验证模式及三十研究配对；尚无通用被测 Agent、安全 Oracle、持久记忆/真实通信、Top-10 执行解释器或反馈 Runtime。PREP 只准备这些接口与证据门禁。
