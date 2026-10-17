# D06–D25 实现与验收复核

本轮是 2026-10-17 的复核，不是日任务执行或新的完成状态。发现 6 项实现问题及 1 项进度字段问题；原有 68 项测试通过不能覆盖以下反例。源码和已冻结演示包尚待修复、复验，尤其 D24 的预算验收结论需要重新核验。

1. **[P1] 前置状态失效后仍执行写入。** `algorithm/src/run_local_pipeline.py:102` 先执行工具，直到 `check_step.py:66` 才验证 Pre；`retry_policy.py:64` 的集成入口也有同样顺序。构造两次修改预约的合法匹配路径，两步 Pre 均要求初态 10:00。第一步改至 14:00 后，第二步仍改至 16:00，随后才返回 Unknown/Pre 冲突。这里没有阻止不满足前置条件的调用；事后 Unknown 无法撤回状态变化。需在生成/目标调用前以当前状态核验 Pre，失败时保留停止证据和已经观察到的独立结果轴。反例见 `test_state_precondition_is_rechecked_before_a_later_write`；冻结包重现见 `frozen-integration.json.runtime_pre`。

2. **[P1] 带预算的路径入口忽略 TestPlan 的总工具调用上限。** `algorithm/src/budget.py:96` 调用 `retry_step` 时采用其默认局部工具预算，未合并 `plan.budget.max_calls`。相同两步计划设 `max_calls=2`，`run_pipeline` 用完两次工具调用后停止；`run_budgeted_path(..., Budget())` 却执行四次目标工具调用，并返回 `path_completed`。独立 Budget 的分类/总量计数正确也不能替代计划中已声明的上限。需合并各层限制并在跨步骤的实际调用前扣减。见 `test_plan_total_tool_budget_is_enforced_in_budgeted_entry` 和冻结包诊断的 `plan_budget`。

3. **[P2] 图顺序验证信任节点自报的消息位置。** `algorithm/src/check_graph.py:45` 用节点的 `message_index` 判断边方向，却不核对该值是否等于绑定请求事件的位置。反例保留所有正确请求/返回引用，把真实位置 0→2 的边反向，再交换节点自报位置，检查结果仍为 `Valid`、errors 为空。错误的模型或输入图可因此通过方向检查。需从已核验的请求事件推导顺序，并拒绝不一致的节点位置和端点证据。见 `test_graph_order_is_bound_to_original_request_events`。

4. **[P2] 允许输入位置中的畸形工具字段导致闭环异常退出。** `algorithm/src/run_local_pipeline.py:53` 对外部文本中的 `command['tool']` 直接查字典，没有检查它是字符串。候选文本为 `SYNTHETIC_REQUEST {"tool": [], "arguments": {}}`，控制面与候选格式均合法，但闭环抛出 `TypeError: unhashable type: 'list'`，不返回结构化停止记录。预算集成入口也调用同一函数。需先校验嵌入命令的完整 Schema，并将拒绝和异常保留为运行证据。见 `test_untrusted_text_with_nonstring_tool_stops_with_a_record`。

5. **[P2] 匹配器在参数 Schema 失败后仍处理非对象参数。** `algorithm/src/match_target.py:15` 发现参数不兼容后仍运行至 `:22` 的 `args.get(...)`。将一个候选的 object 设为 null，再放入一个有效候选，整个批次抛出 `AttributeError`，既不保存该候选的拒绝原因，也不处理后续有效项。需隔离单项结构错误，保留拒绝记录，再处理其他候选。见 `test_matcher_rejects_nonobject_arguments_without_aborting_batch`。

6. **[P2] 预算/重试集成丢失可见历史。** `algorithm/src/retry_policy.py:43` 总是向生成器传入 `[]`；`run_budgeted_path` 没有跨步骤维护或传递历史。正常两步路径中，原 `run_pipeline` 的第二次生成收到前一步的可见工具记录，冻结演示包第二次生成收到空列表。固定回复替身只看当前 Goal，所以演示仍完成，测试没有发现多轮输入已退化。需在集成入口保留可见历史，并通过现有过滤器传入，继续隔离隐藏状态/Oracle。证据见 `frozen-integration.json.visible_history`。

7. **[P3] 阻塞说明没有写入规定的 T 列。** 当前 D09、D13 的 T 都只有 records 路径、checks.md 和 command 通配符；原因、发现日期和解除条件放在 U。`scripts/day_run.py` 的 finish 分支统一拼接 T，无法满足用户要求的阻塞字段。信息未丢失，但正式回填未完全遵循列责任。应在后续进度修正中将这些真实字段写入 T，保留 U 的限制与接口说明。实际单元格快照见 `integrity.json` 的 D09/D13 `O_U`。

本轮命令均从 `E:\Vehicle-Agent-Security\agent-security\szh` 运行。解释器、平台、实际 argv、时间、stdout/stderr、退出码和工作簿/用户 `docs/prompt.md` 的前后哈希见 `command-*.json`。Python 使用 `-B`，pytest 禁用缓存；临时测试目录位于系统临时目录。

- `command-01.json`：`python -B -m pytest -p no:cacheprovider algorithm/tests -q`，exit 0，**68 passed in 3.14s**。包括冻结包哈希、三例隔离执行和篡改拒绝验证；未执行清洁安装或真实模型调用。
- `command-02.json`：本目录 `test_review_boundaries.py -q -s`，exit 1，**5 failed in 0.27s**。五项失败分别对应上列前五项实现问题，断言要求正确行为，没有把已知缺陷写成通过条件。记录 JSON 本身以 UTF-8 保存；早期捕获器在终端转发中文时有编码问题，随后已修正转发器，未覆盖原始证据。
- `command-03.json`：`python -B scripts/check_workspace.py --sources`，exit 0。四个原始 DOCX、700 个 A:N 值、50 个来源块、650 个总览引用、2500 个甘特公式和 50 个负责人公式一致。此项只读检查不能证明行为验收。
- `command-04.json`：`integrity_review.py`，exit 0。逐个核对 D06–D25 交付、最后一次运行、保存重开值和原命令；输出 `integrity.json`。正式状态仍为 Excel 中的 18 日已完成、D09/D13 各阻塞 75%，二者结束日期为空。本轮未更新 Excel，也未把这些既有完成标记作为新增反例通过的证据。
- `command-05.json`：`python -I -B .../frozen_integration_probe.py`，exit 0 表示**诊断保存成功**。模块全部来自冻结 D25 包；预算、运行时 Pre、可见历史三项 `acceptance_passed` 均为 false，不能解释为通过验收。

来源与范围：按当前 AGENTS、README、TASK、workflow、workspace-layout、D06–D25 manifest 源字段及相关日文档复核；通过现有只读入口核验四个 DOCX 与共享工作簿。没有读取或修改 zzy/lhy/data-generation，没有模型调用、凭据访问、真实车辆或外部副作用。所有反例均为本地合成输入；结论只涉及实现行为。

额外追溯注意：D23 `outputs.json` 保存的 retry_policy.py 哈希与当前文件不同。D24 交接已说明添加 meter/reset 参数，现有回归覆盖其兼容性，因此本轮将其记为后续修改导致的版本差异，不计为未解释的篡改，也不宣称复跑了 D23 当时字节完全相同的版本。其余指定文件及 D25 冻结目录与各自最后运行的交付哈希一致。

下一步先修复运行时 Pre 和各层预算，再处理图证据绑定、畸形输入和历史传递；保留本轮失败反例作为回归依据。修复另建真实运行记录，重新验证受影响日与演示版本，再按真实结果维护正式 Excel。D09 至少真实 24 小时后的重标与差异记录、D13 真实模型抽取仍为未完成条件；不在本轮继续执行。B/C 共享接口无变更。

本轮新增的 Python 文件是复核工具/反例，JSON 是可复现实测和 Git 审查证据，Markdown 是维护复核记录，均应保留。`command-06.json` / `closeout.json` 保存实际解释器路径、输入版本哈希、文件分类、Git 状态、忽略、工作树及暂存区空白检查；`command-07.json` 保存新增收尾证据后的最终 Git 状态。工作簿和用户文档的最终哈希与 `command-01.json` 一致。不新增 szh/.gitignore；缓存、临时环境和日志路径检查结果见 `closeout.json`。
