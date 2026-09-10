# 多 Agent 隔离与协作

## 原则

多 agent 的价值来自独立视角、并行验证和职责隔离，不来自同时修改同一个文件。
长程算子的主要风险是状态冲突、重复探索、证据复制失真和设备争抢，因此先定所有权，再谈并行。

## 角色

### Orchestrator

- 维护目标、验收 contract、checkpoint 和优先级；
- 分配 worktree、设备、任务边界和允许修改路径；
- 裁决候选是否进入生产；
- 汇总证据，不替 Driver 修改核心实现；
- 检测 stale 状态、重复路线和跨候选冲突。

### Driver

- 独占一个 worktree 和一个 checkpoint；
- 完成单变量实验，产出原始证据和回退点；
- 不修改其他 Driver 的文件；
- 实验结束更新自己的 worklog 与候选记录；
- 将合并请求交给 Orchestrator，不自行发布最终结论。

### Specialist

- 研究算法、API、硬件、编译器、数据布局或测量方法；
- 输出 2-3 个方案、取舍、风险和最小验证；
- 不直接改生产代码；
- 结论标注证据等级，不用“看起来”替代测量。

### Reviewer

- 只读取交付物、出口标准和原始证据；
- 不接受 Driver 的口头结论；
- 独立复现至少一条关键证据；
- 检查语义、数值、性能、provenance 和回归；
- 输出 P0/P1/P2 与明确 verdict。

### Guard

- 在不可逆操作、共享设备、凭据、数据删除或高成本实验前审查；
- 检查是否会覆盖他人工作、污染测量或泄漏信息；
- 只给安全边界和建议，不代执行。

### Integrator

- 只合并已通过 gate 的候选；
- 维护交付分支和最终 diff；
- 处理 rebase、接口兼容、文件清理和发布检查；
- 不把实验 worklog、调试脚本或失败 diff 带入交付。

## Worktree 与设备租约

### Worktree

- 一个可写任务只允许一个 worktree 和一个 owner；
- 共享只读基线可以复制，不能让多个 agent 同时写；
- 实验分支/目录必须唯一命名；
- 合并前记录 source hash、diff hash 和基线 commit。

### NPU/设备租约

租约至少包含：

```text
owner:
device:
start/end:
purpose:
process IDs:
worktree:
expected load:
cleanup:
```

没有租约时，不启动可能影响测量或占用资源的任务。测量前检查设备空闲、进程、频率/热状态和
并发任务。

### 文件所有权

同一时间只允许一个 writer 修改：

- `STATE.md`
- `TRUTH.md`
- `PLAN.md`
- `REVIEW.md`
- `CANDIDATES.md`
- 生产源码路径

Sub-agent 写自己的 worklog/evidence，由 owner 汇总。禁止“边聊天边同时改权威文件”。

## 消息协议

Agent 之间不传“我觉得已经好了”，只交换结构化记录：

```text
task:
owner:
base authority:
worktree/hash:
goal:
allowed paths:
forbidden paths:
commands:
evidence:
result:
regressions:
open risks:
decision request:
stop condition:
```

消息必须可独立存档。关键决策同步到文件，不依赖对话历史。

## 并行模式

### 调研并行

多个 Specialist 研究不同工具/API/架构方向，产出报告。只有 Orchestrator 汇总后进入实现。

### 独立验证并行

一个 Driver 实现，一个 Reviewer 复现。二者不反复交流中间假设，避免 Reviewer 被带偏。

### 分阶段并行

不同 agent 负责稳定边界清晰的阶段，例如：

- 环境/构建；
- 正确性；
- 性能归因；
- 通用化；
- 交付清理。

前提是文件所有权和设备不冲突。

### 分设备并行

若有多台目标设备，可并行跑不同候选。但必须记录设备差异，不能把跨设备数字直接合并。

## 合并协议

候选满足以下条件才可交给 Integrator：

1. 有独立候选记录和回退点；
2. gate 结论来自原始证据；
3. 没有未解释的已通过区间回归；
4. diff 只包含目标变更；
5. 实验开关和临时 route 已移除或明确关闭；
6. 版本、hash、命令和测试数据完整；
7. Reviewer 已独立验证。

合并时只按逻辑变更拆分，不把“平台兼容”“性能”“格式化”“测试补充”混成一个提交。

## 常见故障

| 故障 | 后果 | 防护 |
|---|---|---|
| 多个 agent 同时写 STATE | 状态互相覆盖 | 单 writer + 追加式 worklog |
| 多个 agent 同一工作树 | 无法分辨变更来源 | 独立 worktree |
| 共享设备无租约 | 性能数据失真 | 设备租约 + 测前快照 |
| Reviewer 读取 Driver 结论 | 失去独立性 | 只给交付物/证据/标准 |
| 复制别人的摘要当事实 | provenance 断链 | 回到原始证据重新核验 |
| 并行探索后直接合并 | 冲突和重复路线 | 统一候选台账与集成门 |

