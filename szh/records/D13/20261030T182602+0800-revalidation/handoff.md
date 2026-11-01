# D13 修复重验记录

实际开始：2026-10-30T18:26:02.418470+08:00；本记录更新时间：2026-10-30T19:17:18.612313+08:00。来源A:block-260，A表第17行，总览第18行。

源验收M：每次调用和解析失败有记录，格式修复最多两次。

实际结果：20条开发轨迹实际发出20次HTTP调用并全部返回；20个提案通过结构和引用检查，图完整性18 Valid、2 Invalid；5项测试通过。

限制与保留项：请求deepseek-chat，服务返回deepseek-flash；150865 tokens，实际费用未提供。AL-005/AL-007原始返回绑定歧义保持Invalid。事件99拒收是注入反例，不是本次模型实际幻觉；未执行真实目标攻击。

环境：Python 3.12.7；Windows-11-10.0.26200-SP0。输入与原交付哈希见inputs.json，当前交付哈希见outputs.json；实际argv、时间、stdout/stderr、退出码见commands.md与command-*.json。

本次为修复重跑，旧运行及失败证据保持；前次记录由同日records目录及20261017复核报告追溯。正式代码版本以outputs.json哈希为准，未提交工作树见D25本轮Git记录。

验收：已保存并重新打开共享Excel；O:U与拟写一致。见excel-final-acceptance.json；源字段/公式与保护区域均校验。

证据：来源/节点/测试/资源/结果轴与Contract在各对应JSON；公开轨迹提案用途为抽取，工具效果无独立观察则Unknown。本地Hard Observable仅支持合成执行。

授权：用户明确授权使用自备DeepSeek key及D9/D13补缺和后续既有成果重验；依据用户要求，全部测试通过之前不改进度文件。配置只由进程读取，不抄录到证据。

跨区读取仅共享Excel与四个原始DOCX；未读取或修改zzy/lhy/data-generation。共享写入只限授权A行O:U；A:N、其他A行、B/C、其他ZIP部件受保护；无会议、不改讨论节点。

接口来源为本工作区版本化Schema，维护责任OAPT_A/szh，变更日2026-10-30；A→B TestPlan+CapabilityConstraint+Contract，B→A ExecutionTrace+EvidenceOutcome，B/C接入待确认。协议文件无本轮变更，未向其他成员写入。

文件审查：正式源代码、研究数据、冻结包和JSON/Markdown验收证据保留；Python -B且pytest禁用缓存，临时运行放系统临时目录；未新增szh/.gitignore。Git/凭据/忽略规则审查见D25本轮收尾证据。

下一步：继续顺序核对下一既有日；本轮最终收尾统一见D25。
