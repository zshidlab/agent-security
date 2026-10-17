# Daily actual record

日期：2026-10-17T04:03:03.858445+08:00；D25；来源 A:block-404。

源验收：冻结包18文件及manifest，三例独立隔离运行全部exit0；逐步报告保留继续/停止理由与Evidence；全套算法68 tests passed；四DOCX及源/总览/甘特公式检查通过。

限制/剩余条件：D25本地演示日验收完成，真实模型调用0；D09仍75%等待真实24h重标，D13仍75%待兼容真实模型20输入实测。失败包分别保留于先前两个D25 run；非真实攻击成功率，未清洁安装、无B/C接口变化。本次停止D25，不启动D26。

输入版本、实际环境、依赖产物哈希见 inputs.json；产物哈希见 outputs.json；实际命令和退出码见 commands.md / command-*.json。

Excel 已保存关闭重开，O:U 一致；A:N、其他 A 行及 B/C/总览等 ZIP 部件未改；所有总览引用和甘特公式通过。证据见 excel-start.json / excel-finish.json。

跨区读取：仅共享 Excel 和四个源 DOCX；未读取或写入 zzy/lhy/data-generation。共享写入仅本日 A O:U。无会议，不改讨论节点。

接口：A 本地版本见产物 schema_version；维护 OAPT_A/szh；变更日见本记录。A→B TestPlan+CapabilityConstraint+Contract，B→A ExecutionTrace+EvidenceOutcome，双方接入待确认；无 B/C 文件或共享接口修改。

证据边界：公开轨迹仅研究输入；合成 Mock 的 Hard Observable 只支持本地行为。未证明真实攻击成功、模型质量或车辆安全增益。
