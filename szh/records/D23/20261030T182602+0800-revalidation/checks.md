# D23 验收

| 项目 | 实际与证据 | 判定 |
| --- | --- | --- |
| 源M | 拒绝、缺失和超时三类都能在预算内停止。；3项测试通过；拒绝、观察不足、超时三类分别停止，生成次数1/1/3；历史不覆盖，并跨步传递经过滤的可见工具结果。；commands.md、command-*.json、outputs.json | 通过 |
| 结构与交付 | check_workspace --day --deliverables；实际退出码见本轮命令收据 | 通过，仅存在性 |
| 完成门禁 | 已保存并重新打开共享Excel；O:U与拟写一致。见excel-final-acceptance.json；源字段/公式与保护区域均校验。 | 通过 |

不将before/after/final_state或Oracle隐藏状态送入生成视图；只验证有限本地重试策略。
