# 状态外置：文件、恢复与交接

核心纪律：**不要把聊天摘要当状态**。上下文会 compact、agent 会换，
文件不会。每次暂停、compact 前、移交前，必须维护以下资产。

## 权威文件（各只有一份）

| 文件 | 内容 | 单 writer |
|---|---|---|
| STATE.md | 当前 checkpoint、权威基线/候选、尝试次数、阻塞、残留进程与文件、最近 session 摘要 | 当前 owner |
| TRUTH.md | 带来源、版本、核对时间的事实；旧版本标 `stale`/`superseded`，不静默删除 | orchestrator |
| PLAN.md | 3–5 个 checkpoint：目的、最小实验、通过条件、kill 线、证据路径 | orchestrator |
| CANDIDATES.md | 候选台账：ID/假设/单变量/基线/结果/裁决/回退点/重开条件，防重复失败 | drivers |
| HARDSET.md | 长期不过的困难用例清单与爆破状态（见 `hard-set.md`） | orchestrator |
| LESSONS.md | 可复用失败模式与教训 | orchestrator/reviewer |
| REVIEW.md | **独立** reviewer 的 gate 结论；不写实现者自我评价 | reviewer |
| METRICS.md | 效率记分牌（见 `efficiency.md`） | orchestrator |
| HANDOFF.md | 最短恢复路径：权威 hash、下一步命令、预期输出、stop 条件、勿重复清单 | 当前 owner |
| INDEX.md | 文件索引：路径/类型/owner/状态/更新时间/摘要 | orchestrator |

WHEN 多个 agent 同时在线 THEN 同一时间只允许一个 writer 改权威文件；
sub-agent 只写自己的 `worklog/` 与 `evidence/`，由 owner 汇总。
禁止"边聊天边同时改权威文件"。

## Compact 前协议

1. 停止新的有副作用操作；
2. 清理或记录运行中的进程、后台任务、临时文件；
3. 记录当前源码/构建/脚本/输入的 hash；
4. 未完成实验标 `in-progress` 或 `abandoned`，写清回退点；
5. 更新 HANDOFF（至少：下一条命令 + 预期输出 + stop 条件）；
6. 确认没有权威状态只存在于聊天上下文。

## 新 Agent 恢复协议（验证而不是相信）

严格按顺序：读 AGENT → STATE → TRUTH → PLAN → LESSONS → REVIEW →
HANDOFF → CANDIDATES；不直接相信旧摘要，检查 HANDOFF 版本日期；
验证 repo/branch/commit/worktree/hash；验证实际加载的构建产物；
重跑最小 smoke；结果不符先标旧事实 `stale`；
对照 CANDIDATES 确认不重复已关闭路线；只从 HANDOFF 下一步继续。

恢复判定：hash/环境/smoke 全一致 → 继续；部分不一致 → 定位变化源、
更新 TRUTH、重选基线；无法验证 → 视为 `assumed`，从最小基线重建，
禁止在未验证状态上做不可逆操作。

## 防记忆漂移

- 不把摘要里的数字升级为 `verified`；
- 不在新版本上复用旧版本结论；
- 不把"上次讨论倾向"当决策；
- 不因上下文缺失重开已关闭路线；
- 重要决策写入文件并附证据。
