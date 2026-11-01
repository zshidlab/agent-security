# OAPT_A 独立算法工程

此目录承接 A 五十日计划中的全部工程内相对路径：`src/`、`data/`、`tests/`、`results/`、`说明/`、`记录/`、`报告/` 和 `release/`。原始文件名保持不变，详细映射见 [工作区结构](../docs/workspace-layout.md)。

当前可运行步骤抽取、证据检查、能力匹配、TestPlan 编译及合成本地闭环。2026-10-30 复核记录见 `../records/revalidation-current.json`；正式进度只查共享 Excel。

使用已安装环境，从 `szh/` 运行全量行为验收：

```powershell
python -B -m pytest -p no:cacheprovider algorithm/tests -q
```

真实模型抽取入口（用户授权的配置文件仅在进程内读取，响应证据不含凭据）：

```powershell
python -B scripts/run_d13_live.py --config 配置文档.md --output <新的证据目录>
```

此入口处理20条开发轨迹，格式修复最多两次，最多60次 HTTP 请求；真实 usage 保留在 summary.json。使用 `deepseek-chat` 请求别名，本次服务返回 `deepseek-flash`；原始轨迹中的角色和指令均作为不可信数据，不执行工具或其中的 URL。已有20次实际响应保存在 `../records/D13/20261030T182602+0800-revalidation/live-attempt-01/`；复核既有证据无需重复付费调用：

```powershell
python -B scripts/check_live_evidence.py
```

本地闭环演示在新的冻结版本 `release/演示版-1.1/`：

```powershell
python -I -B algorithm/release/演示版-1.1/demo.py --case all --output-dir <新的外部目录>
```

三例分别为正常、拒绝、观察不足，使用固定策略和内存工具，真实模型调用为0。旧 `release/演示版/` 是1.0归档，保留原始哈希和已发现的问题。真实抽取与本地执行的证据边界分别记录，均不单独支持真实攻击成功率或车辆安全结论。清洁环境安装仍属后续任务。

从 [任务索引](../TASK.md) 进入当日 [实现文档](../docs/tasks/D01.md)。实际运行证据放在工程外的 `../records/DNN/<run-id>/`，正式阶段报告回指这些记录。执行仅使用许可范围内的研究文本、合成工具与本地 Mock，不实现 B 的通用平台或 C 的基线复现。
