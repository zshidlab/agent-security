# D24 修复重验记录

实际开始：2026-10-30T18:26:02.500456+08:00；本记录更新时间：2026-10-30T19:17:18.687311+08:00。来源A:block-392，A表第28行，总览第29行。

源验收M：计数与原始调用日志一致，超限测试会在调用前被挡住。

实际结果：4项单测及4项历史反例通过；新集成探针通过：计划max_calls=2仅调用2次，第二次写入Pre冲突在写入前停止，可见历史存在且无隐藏快照。

限制与保留项：历史Pre诊断依赖event.before，现正确停止event=None，改以新探针验证更强的调用前拦截；原测试不改。一次-k拼写错误exit5原样保留，改正后4通过1未选；预调用耗时门禁不取消已运行调用。

环境：Python 3.12.7；Windows-11-10.0.26200-SP0。输入与原交付哈希见inputs.json，当前交付哈希见outputs.json；实际argv、时间、stdout/stderr、退出码见commands.md与command-*.json。

本次为修复重跑，旧运行及失败证据保持；前次记录由同日records目录及20261017复核报告追溯。正式代码版本以outputs.json哈希为准，未提交工作树见D25本轮Git记录。

验收：已保存并重新打开共享Excel；O:U与拟写一致。见excel-final-acceptance.json；源字段/公式与保护区域均校验。

证据：来源/节点/测试/资源/结果轴与Contract在各对应JSON；公开轨迹提案用途为抽取，工具效果无独立观察则Unknown。本地Hard Observable仅支持合成执行。

授权：用户明确授权使用自备DeepSeek key及D9/D13补缺和后续既有成果重验；依据用户要求，全部测试通过之前不改进度文件。配置只由进程读取，不抄录到证据。

跨区读取仅共享Excel与四个原始DOCX；未读取或修改zzy/lhy/data-generation。共享写入只限授权A行O:U；A:N、其他A行、B/C、其他ZIP部件受保护；无会议、不改讨论节点。

接口来源为本工作区版本化Schema，维护责任OAPT_A/szh，变更日2026-10-30；A→B TestPlan+CapabilityConstraint+Contract，B→A ExecutionTrace+EvidenceOutcome，B/C接入待确认。协议文件无本轮变更，未向其他成员写入。

文件审查：正式源代码、研究数据、冻结包和JSON/Markdown验收证据保留；Python -B且pytest禁用缓存，临时运行放系统临时目录；未新增szh/.gitignore。Git/凭据/忽略规则审查见D25本轮收尾证据。
