# D25 修复重验记录

实际开始：2026-10-30T18:26:02.502835+08:00；本记录更新时间：2026-10-30T19:17:18.727455+08:00。来源A:block-404，A表第29行，总览第30行。

源验收M：三个例子均能独立运行，模拟结果不写成真实攻击成功率。

实际结果：新冻结演示版1.1含18文件，5项测试通过；三例在隔离目录独立执行exit均为0，新冻结包预算/Pre/可见历史探针通过；全量75通过。

限制与保留项：原1.0包保留原始哈希，当前展示用1.1；三例为local_mock，模型调用0，不支持真实攻击成功率；清洁安装属于后续任务。

环境：Python 3.12.7；Windows-11-10.0.26200-SP0。输入与原交付哈希见inputs.json，当前交付哈希见outputs.json；实际argv、时间、stdout/stderr、退出码见commands.md与command-*.json。

本次为修复重跑，旧运行及失败证据保持；前次记录由同日records目录及20261017复核报告追溯。正式代码版本以outputs.json哈希为准，未提交工作树见D25本轮Git记录。

验收：已保存并重新打开共享Excel；O:U与拟写一致。见excel-final-acceptance.json；源字段/公式与保护区域均校验。

证据：来源/节点/测试/资源/结果轴与Contract在各对应JSON；公开轨迹提案用途为抽取，工具效果无独立观察则Unknown。本地Hard Observable仅支持合成执行。

授权：用户明确授权使用自备DeepSeek key及D9/D13补缺和后续既有成果重验；依据用户要求，全部测试通过之前不改进度文件。配置只由进程读取，不抄录到证据。

跨区读取仅共享Excel与四个原始DOCX；未读取或修改zzy/lhy/data-generation。共享写入只限授权A行O:U；A:N、其他A行、B/C、其他ZIP部件受保护；无会议、不改讨论节点。

接口来源为本工作区版本化Schema，维护责任OAPT_A/szh，变更日2026-10-30；A→B TestPlan+CapabilityConstraint+Contract，B→A ExecutionTrace+EvidenceOutcome，B/C接入待确认。协议文件无本轮变更，未向其他成员写入。

文件审查：正式源代码、研究数据、冻结包和JSON/Markdown验收证据保留；Python -B且pytest禁用缓存，临时运行放系统临时目录；未新增szh/.gitignore。Git/凭据/忽略规则审查见D25本轮收尾证据。

下一步：本轮止于D25；D26未开始，清洁安装、真实目标集成与B/C接口接入属于后续任务。
