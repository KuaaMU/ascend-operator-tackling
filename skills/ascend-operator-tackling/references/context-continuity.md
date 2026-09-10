# 长上下文、Compact 与换 Agent

## 目标

上下文可能被压缩、轮换或替换，但任务状态不能因此丢失。恢复过程必须短、可验证，并能主动发现
旧摘要已经过期。

## 持续维护的恢复资产

### HANDOFF.md

始终只保留当前可执行恢复点：

```text
Updated:
Objective:
Current checkpoint:
Authority:
  repo/branch/commit:
  worktree:
  source hashes:
  binary hashes:
Environment:
Verified facts:
Open blockers:
Closed routes:
Next action:
  command:
  expected:
  stop condition:
Latest evidence:
Do not repeat:
Cleanup/ledger:
```

### STATE.md

记录当前状态，不保留完整历史：

- checkpoint 状态；
- 权威候选；
- 尝试次数；
- blocker；
- 远端残留和进程；
- 最近一次 session 摘要。

### TRUTH.md

按事实 ID 保存当前有效事实。旧版本保留为 stale 或 superseded，不静默删除。

### CANDIDATES.md

用于防止换 agent 后重复失败：

```text
ID:
status:
hypothesis:
single variable:
baseline:
result:
evidence:
decision:
rollback:
reopen condition:
```

## Compact 前协议

1. 停止新的有副作用操作。
2. 清理或记录正在运行的进程、后台任务和临时文件。
3. 对当前源码、二进制、脚本和输入记录 hash。
4. 把未完成实验标为 `in-progress` 或 `abandoned`，写清回退点。
5. 更新 HANDOFF，最少包含“下一条命令 + 预期输出 + stop condition”。
6. 确认没有权威状态仅存在于聊天上下文。

## 新 Agent 恢复协议

严格按顺序：

1. 读 AGENT、POLICIES、STATE、TRUTH、PLAN、LESSONS、REVIEW、HANDOFF。
2. 不直接相信 SUMMARY；检查 HANDOFF 的版本和日期。
3. 验证 repo、branch、commit、worktree 状态和源码 hash。
4. 验证实际加载的二进制路径与 hash。
5. 验证设备、工具、依赖和数据版本。
6. 重跑最小 smoke 或一条代表性证据；结果不符时先把旧事实标 stale。
7. 对比 CANDIDATES，确认当前动作没有重复已关闭路线。
8. 只从 HANDOFF 的下一步或新证据提出的新路径继续。

## 恢复判定

### 完全一致

- hash 一致；
- 环境一致；
- smoke 一致；
- 可以继续 HANDOFF 的下一步。

### 部分不一致

- 先定位变化来源；
- 更新 TRUTH；
- 重新选择基线；
- 不沿用受影响的历史性能/精度结论。

### 无法验证

- 把当前状态视为 `assumed`；
- 从最小可复现基线重建；
- 禁止在未验证状态上做不可逆操作或最终结论。

## 换 Agent 的交接清单

移交者：

- 冻结候选和 hash；
- 写 HANDOFF；
- 标记已关闭路线；
- 记录所有设备/进程/临时文件；
- 指出当前最容易误判的一个点。

接手者：

- 独立验证 hash 和 smoke；
- 不重读所有历史，只按 HANDOFF 链接读取必要证据；
- 对冲突事实发起最小实验，不依赖口头解释。

## 防止“记忆漂移”

- 不把摘要中的数字升级为 verified；
- 不在新版本上复用旧版本的性能结论；
- 不把“上次讨论倾向”当作决策；
- 不因上下文缺失就重开已关闭路线；
- 每次重要决策都写入文件并附证据。

