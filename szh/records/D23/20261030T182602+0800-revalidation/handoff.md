# D23 修复重验记录

实际开始：2026-10-30T18:26:02.498004+08:00；本记录更新时间：2026-10-30T19:17:18.682096+08:00。来源A:block-380，A表第27行，总览第28行。

源验收M：拒绝、缺失和超时三类都能在预算内停止。

实际结果：3项测试通过；拒绝、观察不足、超时三类分别停止，生成次数1/1/3；历史不覆盖，并跨步传递经过滤的可见工具结果。

限制与保留项：不将before/after/final_state或Oracle隐藏状态送入生成视图；只验证有限本地重试策略。

环境：Python 3.12.7；Windows-11-10.0.26200-SP0。输入与原交付哈希见inputs.json，当前交付哈希见outputs.json；实际argv、时间、stdout/stderr、退出码见commands.md与command-*.json。

本次为修复重跑，旧运行及失败证据保持；前次记录由同日records目录及20261017复核报告追溯。正式代码版本以outputs.json哈希为准，未提交工作树见D25本轮Git记录。

验收：已保存并重新打开共享Excel；O:U与拟写一致。见excel-final-acceptance.json；源字段/公式与保护区域均校验。

证据：来源/节点/测试/资源/结果轴与Contract在各对应JSON；公开轨迹提案用途为抽取，工具效果无独立观察则Unknown。本地Hard Observable仅支持合成执行。

授权：用户明确授权使用自备DeepSeek key及D9/D13补缺和后续既有成果重验；依据用户要求，全部测试通过之前不改进度文件。配置只由进程读取，不抄录到证据。

跨区读取仅共享Excel与四个原始DOCX；未读取或修改zzy/lhy/data-generation。共享写入只限授权A行O:U；A:N、其他A行、B/C、其他ZIP部件受保护；无会议、不改讨论节点。

接口来源为本工作区版本化Schema，维护责任OAPT_A/szh，变更日2026-10-30；A→B TestPlan+CapabilityConstraint+Contract，B→A ExecutionTrace+EvidenceOutcome，B/C接入待确认。协议文件无本轮变更，未向其他成员写入。

文件审查：正式源代码、研究数据、冻结包和JSON/Markdown验收证据保留；Python -B且pytest禁用缓存，临时运行放系统临时目录；未新增szh/.gitignore。Git/凭据/忽略规则审查见D25本轮收尾证据。

下一步：继续顺序核对下一既有日；本轮最终收尾统一见D25。
