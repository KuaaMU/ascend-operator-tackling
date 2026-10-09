---
name: ascend-operator-tackling
description: >-
  有明确验收标准的长周期工程攻坚：目标驱动、证据优先的自主循环。
  状态外置、分层评测、单变量可证伪候选、kill 止损、独立评审、多候选赛马。
  内核领域无关、模型/harness 无关；Ascend/CANN 等领域细节由 profiles/ 按需加载。
---

# Ascend Operator Tackling v2

## 这是什么

为**"有明确验收标准、需要长期迭代的工程攻坚"**设计的自主工作法：算子调优、
性能攻坚、复杂迁移、疑难 bug 狩猎。内核领域无关；它不教你写 Ascend 算子，
它教你**如何在任何硬骨头任务上不混乱、不跑偏、不重复踩坑**。

WHEN 任务同时满足以下三条 THEN 启用本 skill：
- 有书面验收标准（测试集、性能口径、正确性要求）；
- 需要超过一天的多轮迭代才能完成；
- 失败成本高（返工、跑偏、遗忘都会浪费大量时间）。

## 三层阅读协议（先读这段）

| 层 | 读什么 | 何时读 |
|---|---|---|
| L0+L1 | 本文件（第一性原理 + 决策框架） | 启动时必读，约 5 分钟 |
| L2 | `references/loop.md` | 进入自主循环前读 |
| L3 | `references/` 下其他文档 | 撞门禁 / 做评审 / 换人恢复 / 用到时按需加载 |

**弱模型模式**：只读 L0+L1，用 `scripts/` 的清单与脚本推进；
不读深层 references——规则越可执行，越不怕模型弱。

**Profile**：领域专属细节不在内核里。`references/profiles/` 按需加载，
例如 Ascend/CANN 算子任务加载 `profiles/ascend-cann.md`。

## L0 第一性原理（5 条）

1. **证据优先于记忆**：任何改变决策的结论，必须能回到可复现的证据；
   状态属于文件，不属于上下文。
2. **验收口径是唯一的锚**：先写清目标、验收口径、约束和可放弃项；
   WHEN 口径变化 THEN 所有旧结论重新验证，不偷换口径。
3. **归因先于修改**：先定位关键路径/失效机制，再做最小、单变量、
   可证伪的实验。不做"不知道为什么慢就先改改看"的实验。
4. **泛化先于特例**：优先结构性、跨用例的方案；禁止按测试用例堆特例
   （白名单蔓延是局部最优陷阱）。
5. **失败要有价格**：每个候选都有 kill criterion；连续失败必须换路径，
   不许换参数硬撑。

## L1 决策框架（触发式，按顺序检查）

1. WHEN 正确性/语义未闭环 THEN 不做任何性能推广，先关正确性门。
2. WHEN 基线不可信（hash 对不上、环境变了、口径变了） THEN 先重建基线，
   不在未知基线上叠新变量。
3. WHEN 同一结构连续 3 次无正收益 THEN 停止参数扫描，写失败复盘，
   只允许从新结构假设重开（见 `references/loop.md` 止损节）。
4. WHEN 连续 N 轮（建议 5，见 `references/hard-set.md`）整体只有个位数增长 THEN 强制换算法路线，不许再调参。
5. WHEN 多个候选并行 THEN 每 N 轮（建议 5）强制看一次记分牌，kill 落后者
   （见 `references/multi-agent.md` 赛马节）。
6. WHEN 验收口径冲突 / 不可逆高成本操作 / 目标资源缺失 THEN 升级给用户，
   附一页材料：当前目标、已验证事实、已关闭路线、最小请求、默认建议。

**默认优先级**（无触发时按此排序）：修失效契约 → 修正确性 →
建可信基线 → 关键路径归因 → 结构性改动 → 长尾收敛 → 清理交付。

## L2 自主循环（骨架）

每轮只执行一个最高价值闭环，顺序如下（详见 `references/loop.md`）：

```text
REANCHOR（重锚定：口径/hash/环境/HANDOFF 是否还成立）
→ CLASSIFY（分类：契约/正确性/环境/性能/证据/卫生，禁止混成"需要优化"）
→ BASELINE（最小可复现基线；先解释差异再叠变量）
→ ATTRIBUTE（关键路径/误差账本：时间花在哪、哪段不可压缩）
→ HYPOTHESIZE（可证伪候选：假设+唯一变量+预期+kill 线，用脚本登记）
→ PROBE（分层：最小 case → 代表性集 → 全量；成本递增）
→ GATE（按类别跑门禁：references/gates.md；二元裁决）
→ DECIDE（promote / iterate / revert / park / close 五选一）
→ PERSIST（更新状态文件；清理残留）
→ 赛马复盘点（到 N 轮（建议 5）了吗？看记分牌）
```

## 状态文件（速览）

`init_mission.py` 生成任务目录；权威文件各只有一份。
详见 `references/state-files.md`。

| 文件 | 内容 | 写者 |
|---|---|---|
| STATE.md | 当前 checkpoint、基线、阻塞、尝试次数 | 当前 owner |
| TRUTH.md | 带来源/版本/状态的已验证事实 | orchestrator |
| PLAN.md | 3–5 个 checkpoint（目的/实验/通过条件/kill 线） | orchestrator |
| CANDIDATES.md | 候选台账：假设/变量/结果/裁决/回退点 | drivers |
| HARDSET.md | 长期不过的困难用例，独立爆破 | orchestrator |
| LESSONS.md | 可复用失败模式 | orchestrator/reviewer |
| REVIEW.md | **独立** reviewer 的 gate 结论，非自评 | reviewer |
| METRICS.md | 攻坚效率记分牌 | orchestrator |
| HANDOFF.md | 新 agent 最短恢复路径（命令+预期+stop 条件） | 当前 owner |

单 writer 规则：同一时间只允许一个 writer 改权威文件；
sub-agent 写自己的 worklog/evidence，由 owner 汇总。

## 关键机制（索引）

- 分层评测与门禁 → `references/gates.md`
- 证据层级与 provenance → `references/evidence.md`
- 通用失败家族 → `references/failure-patterns.md`
- 多 agent 与赛马纪律 → `references/multi-agent.md`
- 文件财政纪律（目录契约/搜索配额/远端隔离） → `references/file-hygiene.md`
- 困难集 → `references/hard-set.md`
- 好/坏实例 → `references/examples.md`
- 效率信号与复盘 → `references/efficiency.md`
- 领域 profile → `references/profiles/ascend-cann.md`

## 脚本

- `scripts/init_mission.py --mission <dir> --goal ... --acceptance ... [--profile ascend-cann]`：初始化任务目录与模板。
- `scripts/discover_environment.py [--profile <name>]`：只读环境发现，不假设工具存在。
- `scripts/new_candidate.py`：登记可证伪候选（假设/单变量/预测/kill 线）。
- `scripts/mission_lint.py <mission>`：结构 lint——缺文件、占位符、HANDOFF 过期、
  无 hash、REVIEW pending、scratch 孤儿目录、research 超量。

## 模型/harness 无关声明

本 skill 是声明式的（验收什么、达到什么标准），不是命令式的
（点哪个按钮、调哪个 API）。换模型、换 harness（Claude Code / Codex /
DeepSeek Harness / 其他）不影响内核；`scripts/` 只做薄薄的脚手架调用。
