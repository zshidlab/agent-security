# Daily actual record

日期：2026-10-17T03:27:44.400018+08:00；D07；来源 A:block-188。

源验收：200输入逐条保留；按套件/原始user_task归组，同模型和不同注入变体不拆组；完整、重复和不足条件数量守恒。3项行为测试通过，详细数量filter-summary.json。

限制/剩余条件：公开基准合成轨迹；不完整与重复另存incomplete-reference.jsonl并回指原文件；组归并保守，未宣称案例独立或真实效果。

输入版本、实际环境、依赖产物哈希见 inputs.json；产物哈希见 outputs.json；实际命令和退出码见 commands.md / command-*.json。

Excel 已保存关闭重开，O:U 一致；A:N、其他 A 行及 B/C/总览等 ZIP 部件未改；所有总览引用和甘特公式通过。证据见 excel-start.json / excel-finish.json。

跨区读取：仅共享 Excel 和四个源 DOCX；未读取或写入 zzy/lhy/data-generation。共享写入仅本日 A O:U。无会议，不改讨论节点。

接口：A 本地版本见产物 schema_version；维护 OAPT_A/szh；变更日见本记录。A→B TestPlan+CapabilityConstraint+Contract，B→A ExecutionTrace+EvidenceOutcome，双方接入待确认；无 B/C 文件或共享接口修改。

证据边界：公开轨迹仅研究输入；合成 Mock 的 Hard Observable 只支持本地行为。未证明真实攻击成功、模型质量或车辆安全增益。
