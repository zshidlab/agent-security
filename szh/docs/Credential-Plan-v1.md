# 一次配置与跨终端凭据方案 v1

版本 1.0.0，2026-10-09，design only。本次没有询问、读取、输出或保存真实 key，也未检查用户凭据条目。诉求是启动自动加载，不是让 LLM 保存秘密。

## 决策

当前 Windows 优先 Windows Credential Manager 的 Generic Credential，由未来最小 provider broker 通过受控 CredWrite/CredRead 接口读取。拟议 target 为 graduation-agent/deepseek/pilot/v1，属于当前 OS 用户；该 target 名非秘密。只允许 provider transport 进程消费，LLM、tools、Oracle、memory 不接触凭据。账户内恶意进程仍可能读用户 vault，原生库并不隔离同用户所有进程。

若使用 Python keyring，先在不获取任何凭据的前提下检查版本、backend 模块/类和依赖，要求经验证的 Windows WinVault 原生后端；拒绝 fail/null/plaintext/不明 third-party/chained 回退。后端检测与实际存取是 I2 的后续验收，不宣称当前机器已具备。未来 Linux Secret Service/macOS Keychain 是迁移设计，不能默认此机可用，也不安装替代后端。

原生库不可用的备选：当前用户 profile 的专用 local-app-config 目录（不在仓库），文件 ACL 只给当前用户和必要系统主体，关闭继承，目录/文件权限先验收；若项目内必须有本地配置，必须先证明 Git 忽略和受限 ACL，位置不得与 checkpoint/trace 混合。配置文件是可读明文，对备份、同用户进程、误同步风险高于 vault；不自动退回，不把 base64 当加密。路径/忽略规则属于后续独立实现，不在本次创建 secret 文件。默认无合格 vault 时 fail closed，备选启用需对应任务明确选择。

## 未来设置流程

1. 在已授权 I2 中确认 OS/backend、受控 API endpoint 和凭据用途，检查日志脱敏；只用假 key 做错误路径测试，不枚举真实 vault。
2. 本地安全输入 UI 或 hidden prompt 录入一次真实 key；不作为 CLI 参数/命令历史，不经聊天/文档/环境持久脚本，不回显。只存该 provider target；输入成功只显示 target/版本及状态，不显示片段。
3. 启动读取非敏感 config：provider、endpoint allowlist、model/version、credential_target、timeout、retry、预算、log level；所有非敏感配置可版本化。默认不扫描多种 secret 来源，不从 prompt/checkpoint 恢复 key。
4. broker 运行时读取 vault，把 secret 只放传输内存的授权 header；避免 repr/debug/http dump/异常正文，子进程不继承。若适配既有生成器必须另明确授权；其现行 DEEPSEEK_API_KEY 规范不由此方案改写，也不把 key 持久写系统环境。
5. 新开终端/重启进程应自动找到相同用户 target；跨 Windows 用户、机器、远程会话不默认复用。为多个模型账号使用独立 target，不混用模型凭据。
6. 轮换先写新版本并原子切换 target，有限确认后清理旧条目并在服务端撤销旧 key；撤销时停止新请求、清内存缓存、删对应 target。只记录非敏感轮换日期/状态，不记录 key/hash/尾号。

## 故障与验收

| 条件 | 行为与后续检查 |
| --- | --- |
| 凭据缺失/库锁定/无后端/ACL 不符 | 启动 ERROR/CREDENTIAL_UNAVAILABLE，零 API；提示本机设置流程，不能回退伪 live defender |
| 401/403 | 停止该凭据请求，记录脱敏 auth_error；不无限重试、不把原响应/请求 header 写 trace |
| 429/5xx/超时 | 有限重试及 ledger；不显示 key，不用新 key 轮询规避预算 |
| checkpoint/reset/replay | 不读取或恢复 secret；离线 replay 不需 key，真实新请求重新从 vault 读取 |
| 日志/测试 | 用合成 secret sentinel 检查 prompt/trace/异常/导出/缓存中为零；Authorization 完全删除，不只遮一部分 |
| 跨终端 | 两个新进程在同 OS 用户下可加载；不输出 key，只返回 configured/unavailable |
| 轮换/撤销 | 新配置生效、旧 key 在服务端撤销、旧本地条目清理；无未授权测试调用 |

完成设置需后续实现、backend 检查和用户在本机安全录入，付费连通性仅在明确预算授权后测试。本次 PREP 的验收是流程/风险/失败行为完整，不是已配置凭据。任何 key 不进文档、Git、prompt、对话记忆、跨会话 store、checkpoint、trace 或样本。
