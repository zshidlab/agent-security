# D14 验收

| 项目 | 实际与证据 | 判定 |
| --- | --- | --- |
| 源M | 故意构造的空证据、重复节点、错误方向三例均被发现。；4项测试通过：空证据、重复节点、逆序、伪造节点位置/端点证据均受检；真实与规则图各18 Valid、2 Invalid。；commands.md、command-*.json、outputs.json | 通过 |
| 结构与交付 | check_workspace --day --deliverables；实际退出码见本轮命令收据 | 通过，仅存在性 |
| 完成门禁 | 已保存并重新打开共享Excel；O:U与拟写一致。见excel-final-acceptance.json；源字段/公式与保护区域均校验。 | 通过 |

顺序从原始请求事件推导；歧义输入拒绝，不静默修复；图Valid不等于效果成立。
