# PREP 决策、风险与复现清单 v1

版本 1.0.0，2026-10-09。文档准备验收不代替后续代码/环境/API/实验验证。当前进度见 TASK.md。

## 关键决策与替代方案

| 决策 | 选择/理由 | 替代/限制与依据 |
| --- | --- | --- |
| 路线 | 通用管线→真实 Mock 证据→领域适配 | 直接车载迁移会混淆数据/环境贡献；保留导师 O5/完整矩阵，见映射 |
| 编排 | LangGraph 作为被测 Agent 候选编排，TFIR Runtime 独立接口 | 普通状态循环也可实现；LangGraph 不证明创新；现源码无此能力 |
| 非车载场景 | DOC 信息流、EXP 状态确认 | 两种机制覆盖反馈差异，仍是合成 Mock，不能推广生产漏洞 |
| Oracle | 确定性效果/权限/任务谓词，语义辅助 | 单 LLM Judge 不足；复杂语义泄露/隐写 unknown |
| 当前 provider | 不复用 JSON actions 当原生工具防守 Agent | 需新隔离 adapter；保留旧生成器规则/接口不改 |
| 凭据 | Windows native vault，检查后可用 keyring WinVault | ACL 明文 config 是降级备选，禁止静默退回；未验证后端 |
| 比较 | 表示×反馈因子，保留 B0-B4 | 只比图+反馈/模板无反馈无法归因 |
| 标签 | 五个主轴加防护/阶段/终止等辅助轴 | 单 PASS/FAIL 混淆研究/防守/运行结果 |
| 兼容 | 新通用 envelope + legacy sidecar | 不直接覆盖车载 Schema，不把 agent_id 解析成可信身份 |
| 训练 | 仅预留版本化导出/证据/split接口 | 实际防护微调独立授权/外部测试；适配不是微调 |

## 风险与尚待核实

| 风险/未知 | 控制 / 后续阶段 | 是否阻塞本次 PREP |
| --- | --- | --- |
| Top-10 不接入且部分 catalog/fixture | 支持矩阵/unsupported、I3 编译与真实能力验收 | 否，已明确记录 |
| 原 provider 无原生 tools、重试与文档差异 | I2 offline fixture/API capability 后实现；不计 fallback 为 live | 否 |
| Windows backend/依赖实际可用性 | I2 不枚举凭据的后端检查，安全录入由后续流程 | 否，未读取 key |
| 具体 DeepSeek model/价格/版本/seed | I2 授权后核对及最小 smoke | 否；现静态默认不当现行服务证据 |
| 六+模型访问、费用额度、算力 | X2/X3 需实际资源/预算授权；无额度不得 API | 否，属于未来真实资源依赖 |
| 双人标注与独立 held-out/复现者 | X2/W1 需人员安排，F7 独立作者 | 否，不伪造已有人手 |
| 同模型生成/被测偏差 | 跨家族生成×被测矩阵/盲审，pilot 限定范围 | 否 |
| 完美 PEP 下 effect ASR 为零 | 仍报告尝试/阻断和效用；不弱化政策制造成功 | 否，可能可证伪研究假设 |
| 参数包装图/模板实际差异不足 | X1 manipulation 检查/报告零差异，不靠标签自证 | 否 |
| MVR参考集选择、UVP人为增计 | 独立 R_ref/方法无关签名/盲审/敏感性 | 否 |
| Split同源污染、test调参 | 按来源/场景/路径/模板家族关联分组；冻结测试 | 否 |
| 模型随机/版本漂移 | 原始请求/响应/usage、三seed、重放与真实重跑分开 | 否 |
| 投稿窗口/来源与专利状态未在线核验 | R1 私有交底；W1 核验 venue/专利提交/发布授权 | 否；公开发布有门禁 |

需要用户提供的未来资源只有可用模型/预算/算力、真实凭据安全录入、人员和专利/发布决策；不得因此反复确认本次已有授权。常规设计已选择。没有本次文档无法推进的外部阻塞。

## 复现登记与版本

- data-generation HEAD：7bcaa37a2dc7a575078ba11de84b8b9b56ca6b8f；开始/结束 git status 应只有原有评价标准修改。
- 导师 docx：SHA256 571D1E7BF16DB4935F63BE960F3057C722E037E2ED8DAE799B8E6B977A021EEB；正文/表格 UTF-8 只读 ZIP XML 提取。
- 当前标准 v2.2 / 2026-10-09 是用户工作副本，历史 prior-art/venue/Threat v1 原样保留。
- Top-10 research_version 1.0.0 / as_of 2026-10-06；21 来源/8 案例，仅历史资料核验。
- 样本 Schema 1.0.0、tool pool 1.2.0、auth 1.2.0、ASV 3；完整迁移需后续固定哈希。
- 本次环境：Windows、PowerShell 5.1.26100.9444、Python 3.12.7（仅只读提取/文档检查）；未安装或运行 LangGraph/DeepSeek。
- 未来依赖：Python/JSON Schema parser、LangGraph/checkpointer、HTTP/DeepSeek tool adapter、可用 vault 后端、pytest；版本本次未装/核实。I1/I2 选择固定版本/锁定范围，禁止为方便擅自改现生成环境。

## 本次验收证据

执行环境为上述 PowerShell；全部命令在 E:/Vehicle-Agent-Security 运行，Git 命令指定 data-generation 工作目录。下面是本次检查实际结果，不是运行实现测试/正式实验。

| 检查/命令 | 结果与证据范围 |
| --- | --- |
| Get-Content -Raw -Encoding UTF8 与 ConvertFrom-Json；遍历 graph/templates、Compare-Object path_id、检查 edge from/to 与 node_id、比 fixed_stages.phase/generation_instruction | 十类入选与目录一致；30 配对、210 节点、180 边、120 对同 phase/指令、462 次 source_ref 引用全部通过；21来源/8案例引用均存在；README/references含全部路径 |
| 遍历当前新增/修订 Markdown 的相对链接，URI 解码后 Test-Path | 11 份当前 Markdown、53 个本地链接通过；历史原文/v1 中外部链接不联网核验 |
| 对映射表行 ID 作唯一性检查 | 77 行完整：10 O、6 RQ、50 D、11 G，无缺失/重复 |
| 两 JSON ConvertFrom-Json；逐项验证 contract_ref、normative_documents、predicate registry、tool catalog、scenario pair_asset | 两份语法合法；8注册谓词/2场景/8工具；草案/未执行/无付费授权标记正确；内部引用通过。它们是数据契约草案，不声称已通过完整 JSON Schema validator |
| 核对 Outcome 文档与 contracts.outcome_axes；检查指标/预算关键词和人工语义审阅 | 11 独立标签轴、47枚举一致；ITT/eligible/unknown、MVR参考集、FPR/FDR、Utility、重试全记账、B0-B4/反馈控制、split/held-out/安全边界一致 |
| 开始/结束的 SHA256 比较：Get-ChildItem（排除 .git、__pycache__、.pytest*、artifacts、test）→Get-FileHash | 相同133文件（132 data-generation静态/源码文件+导师docx），0改变/新增/缺失；排除的运行时目录未复验，不能据此声称所有隐藏/运行时文件哈希均已比较 |
| 开始/结束 git status --short；结束 git diff --stat / --numstat | data-generation 只有开始已存在的评价标准修改（129增/15删），未被本次修改；未恢复用户改动；根目录/毕业目录无Git，无法做其git diff或宣称整个工作区clean |
| 历史归档 Get-Content 与编辑前保存全文比较（规范化行尾） | 旧 AGENTS/TASK 两份内容匹配；D1/D2证据和旧日期保留。只写 graduation-project，不含 docx/v1研究文件 |

只读来源清单 SHA256 对比与所有 apply_patch 目标共同支持本次范围核验；未将 Git 已有 dirty 修改说成本次产物。运行时目录、外部资料、实际 API/模型与后端均未复验。

初次范围检查曾使用过窄 .pytest_cache 排除，列出额外52个既有pytest临时文件；这不是本次新增证据。随后使用与开始一致的 .pytest* 排除重新比对，133对133零差异。初次历史文字比较的 PowerShell 扩展 string 类型也已用显式 string 读取修正。最终结果以上述通过检查为准，未改任何临时产物。

最终 JSON/协议版本复核：11当前Markdown、53本地链接、77映射行、2JSON、11标签轴/47枚举、8注册谓词、2场景/8工具，0错误；新增/修订文档中凭据形状扫描0匹配（仅补充检查，不以此取代零凭据访问规则）。语义复核已明确 PreValidator 只检查研究输入可提交/隔离，不会因攻击拟违反防守策略而预先清掉攻击。

对两份归档与当前 AGENTS/TASK 执行 git diff --no-index --stat，exit 1 是存在预期修订差异，非检查失败；新文件清单均为文档/草案/历史副本。最终状态 PREP DONE，仅当前前置验收；R1及以后全TODO。未运行源码测试/付费API/大型实验，无环境/攻击有效性结果。

## 交接

所有本次可完成的审计、映射、方案、草案和清单在 PREP 内交付，不把缺文档留给下一会话。R1 仅将未来资源与研究预注册选择绑定冻结；I1/I2 才验证当前平台/API/凭据行为。下次提示见 [Next-Session-Prompt](Next-Session-Prompt.md)。完成 PREP 后停止。
