# Agent Entry Point

本目录是任务的唯一权威状态入口。新 agent、compact 后恢复、换 agent 或接管前，必须先完成读取和
验证，再修改代码或运行有副作用的命令。

## 读取顺序

1. `AGENT.md`
2. `POLICIES.md`，若任务提供
3. `STATE.md`
4. `TRUTH.md`
5. `PLAN.md`
6. `LESSONS.md`
7. `REVIEW.md`
8. `HANDOFF.md`
9. `CANDIDATES.md`
10. `METRICS.md`
11. `INDEX.md`
12. 任务书：`{{TASK_DOC}}`
13. 目标仓库和测试说明

## 恢复验证

- 验证 repo、branch、commit、worktree 和源码 hash；
- 验证实际加载的二进制路径和 hash；
- 验证设备、CANN、编译器和依赖版本；
- 重跑最小 smoke 或一条关键证据；
- 任何不一致先标 `stale`，不要继续沿用旧结论。

## 文件所有权

同一时间只允许一个 writer 修改 STATE、TRUTH、PLAN、REVIEW、CANDIDATES 和生产源码。
Sub-agent 只写自己的 worklog/evidence，由 owner 汇总。

## 目标

{{GOAL}}

## 验收

{{ACCEPTANCE}}
