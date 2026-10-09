# Agent Entry Point

本目录是任务的唯一权威状态入口。新 agent、compact 后恢复、换 agent 或接管前，
必须先完成读取和验证，再修改代码或运行有副作用的命令。

## 三层阅读协议

| 层 | 读什么 | 何时 |
|---|---|---|
| L0+L1 | skill 的 SKILL.md（第一性原理 + 决策框架） | 现在，5 分钟 |
| L2 | skill `references/loop.md`（自主循环详细） | 进入循环前 |
| L3 | 按需：`references/gates.md`（撞门禁）、`references/state-files.md`（恢复交接）、`references/file-hygiene.md`（文件纪律）、`references/hard-set.md`（困难集）、`references/examples.md`（实例）、`references/profiles/{{PROFILE}}`（领域） | 用到时 |

弱模型模式：只读 L0+L1，用 `scripts/` 清单与脚本推进，不读深层 references。

## 本任务读取顺序

1. 本文件 `AGENT.md`
2. `STATE.md` → `TRUTH.md` → `PLAN.md`
3. `LESSONS.md` → `REVIEW.md` → `HARDSET.md`
4. `HANDOFF.md` → `CANDIDATES.md` → `METRICS.md` → `INDEX.md`
5. 任务书：`{{TASK_DOC}}`
6. 目标仓库和测试说明

不要只读摘要；至少核对当前 commit、工作树状态、源码 hash、
实际加载的构建产物 hash、目标环境版本和最近一次权威证据。

## 恢复验证

- 验证 repo、branch、commit、worktree 和源码 hash；
- 验证实际加载的构建产物路径和 hash；
- 验证目标环境、工具链和依赖版本；
- 重跑最小 smoke 或一条关键证据；
- 任何不一致先标 `stale`，不要继续沿用旧结论。

## 文件所有权

同一时间只允许一个 writer 修改 STATE、TRUTH、PLAN、REVIEW、
CANDIDATES、HARDSET 和生产源码。Sub-agent 只写自己的
`worklog/` 与 `evidence/`，由 owner 汇总。

## 文件去处（见 skill `references/file-hygiene.md`）

- 实验产物 → `scratch/<候选ID>/`，候选关闭时归档或删除；
- 外部资料 → `research/`（文件头：来源、日期、一句话结论）；
- 原始证据 → `evidence/<run>/`（manifest + 日志 + hash）；
- 困难用例 → `hard-set/`，清单记在 HARDSET.md。

## 目标

{{GOAL}}

## 验收

{{ACCEPTANCE}}

## Profile

{{PROFILE}}
