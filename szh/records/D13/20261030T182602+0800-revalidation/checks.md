# D13 验收

| 项目 | 实际与证据 | 判定 |
| --- | --- | --- |
| 源M | 每次调用和解析失败有记录，格式修复最多两次。；20条开发轨迹实际发出20次HTTP调用并全部返回；20个提案通过结构和引用检查，图完整性18 Valid、2 Invalid；5项测试通过。；commands.md、command-*.json、outputs.json | 通过 |
| 结构与交付 | check_workspace --day --deliverables；实际退出码见本轮命令收据 | 通过，仅存在性 |
| 完成门禁 | 已保存并重新打开共享Excel；O:U与拟写一致。见excel-final-acceptance.json；源字段/公式与保护区域均校验。 | 通过 |

请求deepseek-chat，服务返回deepseek-flash；150865 tokens，实际费用未提供。AL-005/AL-007原始返回绑定歧义保持Invalid。事件99拒收是注入反例，不是本次模型实际幻觉；未执行真实目标攻击。
