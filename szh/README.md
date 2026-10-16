# OAPT_A 工作区

`agent-security/szh/` 只服务 OAPT_A“攻击样本生成”D1–D50：历史轨迹、步骤图、能力匹配、逐步输入生成、证据判断、有限反馈与个人交付。

从 [TASK.md](TASK.md) 选择当天任务，按 [执行流程](docs/workflow.md) 实现与验收。正式进度以 [共享工作簿](../OAPT_研究方案进度管理_三人员分表与总览甘特图.xlsx) 的 `A_核心算法` 为准。

```text
szh/
  AGENTS.md                  工作区长期约束；继承 ../AGENTS.md
  TASK.md                    五十日任务总索引
  README.md                  本入口
  docs/
    README.md                文档导航与历史资料说明
    workflow.md              开始→实现→验收→Excel→交接
    workspace-layout.md      路径映射、归属与维护原则
    tasks/D01.md … D50.md     逐日详细实现方案
    tasks/manifest.json      源计划快照、路径与来源哈希
    templates/daily-record.md 逐次真实记录模板
    records/                 工作区维护记录
    archive/                 已停用的历史启动提示
    Next-Session-Prompt.md    后续会话启动模板
  scripts/check_workspace.py 只读结构/来源/交付存在性检查
  algorithm/                 A 工程；当前仅说明，执行各日时建立代码等
  drafts/                    既有草稿，仅供核对
  records/DNN/<run-id>/      未来实际运行证据，执行时创建
```

详细结构和 `algorithm/` 内部规划见 [路径说明](docs/workspace-layout.md)。本次建立了五十份任务方案，尚未执行 D1–D50，也未填入实际运行记录。代码、测试、环境和交付包在对应日真实实施时创建。

从本目录进行文档核对：

```powershell
python -B scripts/check_workspace.py
python -B scripts/check_workspace.py --sources
```

检查器仅使用 Python 标准库，不安装依赖、不修改源文档或进度。通过检查表示文档与源计划一致，不表示算法已实现或日任务已完成。
