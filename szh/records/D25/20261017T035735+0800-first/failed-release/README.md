# OAPT_A D25 演示版 1.0

这是可独立运行的 local_mock 包；只用合成通知与内存预约，不连接模型或真实系统。
固定策略刻意将合成文本命令映射到两个本地工具，用于验证生成→执行→独立观察→三值判断。
RefusingExecutor 是显式拒绝替身；信息不足例屏蔽完成观察。结果不代表真实攻击成功或车辆安全。

从本目录运行（Python >=3.10，实际测试环境见 environment.json）：

```powershell
python -I -B demo.py --case normal --output-dir <新的外部输出目录>
python -I -B demo.py --case refusal --output-dir <另一个新的外部输出目录>
python -I -B demo.py --case unknown --output-dir <第三个新的外部输出目录>
```

依赖已安装版本见 requirements.txt；本日未执行清洁安装。不要把输出放入冻结包，不覆盖既有运行。
每次启动先核对包文件哈希与清单；此清单用于版本复核，不是签名或来源真实性证明。
原始 JSON 保留候选、输入读取、工具结果、独立状态差分、观察、证据、判断、预算和停止原因；Markdown 解释每次继续/停止。
费用是离线模拟单位，真实 token/美元成本未知。耗时门禁只能拒绝后续调用，不能取消已运行的适配器。

责任：OAPT_A/szh；接口：testplan-1.0 / capability-1.0 / step-judgment-1.0；未更改 B/C 共享接口。
D09 的隔日至少24小时重标、D13 的真实模型抽取仍未完成；本包不代替这些源验收。
只冻结本地闭环需要的代码；不含真实模型、凭据、上游轨迹数据或留出集。
