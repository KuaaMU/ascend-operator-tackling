---
name: ascend-operator-tackling
description: >-
  以目标驱动、证据优先的方式推进 Ascend/CANN 算子从实现、正确性闭环到性能攻坚：
  不绑定特定 CANN 版本、芯片或算子，优先发现并使用当前环境提供的官方工具做瓶颈归因，
  再以单变量候选实验、真实硬件门禁和可回退证据推进；用 STATE/TRUTH/PLAN/REVIEW/HANDOFF、
  候选台账和多 agent 隔离抵御长上下文、compact、换 agent 与需求漂移；通过持续定位关键路径、
  归纳失败家族和主动重规划，尽量实现无人干预下的自主纠正与长程交付。
---

# Ascend Operator Tackling

## 使用目标

当任务需要在任意 Ascend/CANN 环境中长期开发、迁移或调优算子，并且必须靠真实硬件证据决定
“继续、回退、重构或止损”时使用本 skill。它适用于单 agent 和 Orchestrator + 多 agent 模式，
也适用于上下文已 compact、旧 agent 已离开、需要从半成品继续推进的情况。

本 skill 不假定固定命令、芯片型号、CANN 版本或仓库结构。先发现环境，再选择工具和策略。
不以“某个 benchmark shape 变快”为完成，以目标语义、目标口径和真实环境证据为完成。

## 核心契约

1. **目标优先于局部指标**：先写清最终目标、验收口径、约束和可以放弃的指标。
2. **事实优先于记忆**：任何结论必须能回到当前源码、二进制、命令、原始日志或官方来源。
3. **正确性先于性能**：语义、边界、精度和 fallback 未闭环前，不做激进性能推广。
4. **归因先于修改**：先定位关键路径和量级，再做最小、单变量、可证伪的实验。
5. **证据先于宣传**：没有真实目标环境证据，不得写 PASS、GO、已解决或可交付。
6. **泛化先于特例**：优先做算法不变量、公共 primitive 和资源驱动 route；禁止只按 CSV/benchmark
   shape 堆白名单。
7. **可回退先于冒险**：每个候选都要有基线、kill criterion、证据路径和回退点。
8. **连续失败必须换路径**：同一问题、同一结构连续 3 次无正收益，停止参数扫描，写复盘并重规划。
9. **状态属于文件，不属于上下文**：每轮结束都留下可恢复的 STATE/TRUTH/HANDOFF 和原始证据。
10. **少而准确的信息优于文档堆积**：只维护权威事实、决策、失败家族和下一步，不复制聊天记录。

## 启动

在对源码做有副作用操作前，按以下顺序完成启动：

1. 定位 skill 目录、任务工作区、上游仓库、任务书、测试数据和当前运行环境。
2. 运行 `scripts/discover_environment.py`，记录实际存在的编译器、NPU 工具、设备和版本；
   不要凭旧记录假设工具存在。需要硬件状态时再显式运行状态探测。
3. 若尚无任务治理目录，运行：

   ```bash
   python scripts/init_mission.py --mission <path> --goal "<goal>" \
     --operator "<operator>" --repo "<repo>" --task-doc "<path-or-url>" \
     --acceptance "<acceptance>"
   ```

4. 按 `mission/AGENT.md` 的读取顺序重建事实。不要只读摘要；至少核对当前 commit、工作树状态、
   源码 hash、实际加载的二进制 hash、目标环境版本和最近一次权威证据。
5. 用 `mission/PLAN.md` 记录 3-5 个面向真实证据的 checkpoint。每个 checkpoint 必须有：
   目的、最小实验、通过条件、kill criterion、证据路径。
6. 用 `mission/METRICS.md` 建立效率基线，至少记录可信基线耗时、候选排除成本、重复探索和
   handoff 恢复情况。
7. 运行 `scripts/mission_lint.py <mission>`，修复结构性缺失后再开始长任务。

## 自主循环

每一轮只执行一个最高价值闭环：

1. **重新锚定**：重新读取任务书/验收口径，检查是否漂移；验证当前权威源码、二进制和环境是否
   仍与最近的 HANDOFF 一致。不一致时先把旧事实标为 `stale`，不要继续沿用。
2. **分类问题**：把当前阻碍归入 `契约/语义`、`正确性`、`环境/构建`、`性能关键路径`、
   `证据/状态` 或 `工程卫生`。不同类别使用不同 gate，禁止混成一个“优化问题”。
3. **建立/恢复基线**：选择当前最小可复现基线。若结果与权威记录不一致，先解释差异，
   不要在一个未知基线上叠加新变量。
4. **做归因**：优先使用当前环境可用的官方观测工具和最小 probe，建立 phase、route、launch、
   memory、compute、sync、host 或数值误差账本。先回答“为什么慢/错/不稳定”，再回答“怎么改”。
5. **提出可证伪候选**：写一条假设、一个变量、预期方向、目标量级和 kill criterion。用
   `scripts/new_candidate.py` 登记。模板和决策树见 `references/autonomous-loop.md`。
6. **执行最小实验**：先跑最小区分性 case，再做代表性集合，最后才做全量。过程证据不能替代
   目标环境验收。
7. **按 gate 裁决**：
   - 正确性/语义问题：按 `references/correctness-gates.md` 验证。
   - 性能/泛化问题：按 `references/performance-gates.md` 验证。
   - 证据/交接问题：按 `references/evidence-and-truth.md` 验证。
8. **记录并决定**：promote、iterate、revert、park 或 close。失败也要留下“失败原因 + 关闭条件 +
   重开条件”，避免换 agent 后重复投入。
9. **写恢复点**：更新 STATE、TRUTH、CANDIDATES、LESSONS、METRICS 和 HANDOFF，清理不必要残留。

循环不需要等待用户逐步指令；只有验收口径冲突、不可逆风险、外部资源缺失或连续失败需要改变
目标时，才升级给用户。升级前必须提供当前事实、已尝试路径、最小请求和推荐的默认选择。

## 决策优先级

按以下顺序选择下一步，不要凭“看起来最有潜力”跳级：

1. 修复会让所有性能结论失效的契约、语义、构建或 provenance 问题。
2. 修复 P0 正确性、数据破坏、越界、竞态、精度或 fallback 问题。
3. 建立可信基线和可复现证据，消除 stale binary、dirty tree、错误设备或错误口径。
4. 做官方工具驱动的关键路径归因，区分 launch、host、memory、compute、sync、layout 和 variance。
5. 选择能跨多个用例泛化的结构改动；不要先追单个 shape 的最后一微秒。
6. 提升 near-gate 和残余长尾，最后再做局部微调。
7. 清理实验代码、route 白名单和交付树，进行独立评审。

## 官方工具优先

先运行环境发现脚本，再读取 `references/official-tools.md`。原则是：

- 先用官方 profiling、logging、sanitizer、debugger、compiler diagnostics 和 correctness tools，
  再用自建 microbenchmark 解释原因。
- 保留工具原始输出；摘要只能作为派生信息。
- 任何工具结论都要写清目标、过滤条件、采样方式、版本、设备、命令和原始日志。
- 工具不可用、版本不兼容或语义不明时，记录限制并选择最低风险的替代证据，不要伪装成等价证据。
- 官方文档、样例和当前安装头文件优先于历史总结或第三方文章。

## 正确性与性能门禁

**正确性门禁**必须覆盖：

- 目标 API/格式的完整语义，而不只是数值主路径。
- 边界、空值、非法参数、奇异/退化、非有限值、极值、padding、stride、broadcast/别名等适用场景。
- fast path 与 fallback 的一致性；内部状态不得污染用户可见输出。
- 随机输入之外的结构化、对抗和分布变化输入。
- 目标硬件上的真实运行，CPU 模拟和 local mock 只能作为过程证据。

**性能门禁**必须覆盖：

- 任务书/用户定义的目标口径，不偷换 kernel-only、host wall、中位数或单次最优值。
- 输入重置、warmup、有效采样、设备空闲、机器负载和统计方法。
- 同机器、同构建、同输入下的 A/B；每次只改变一个主变量。
- 最小 case、代表性 case、全量回归和至少一次独立复现。
- 提升必须说明作用区间和泛化边界；新 route 不能造成已通过区间静默回归。
- 近门限结果要区分真实提升、跨 run variance 和顺序/热状态效应。

详细规则见 `references/correctness-gates.md` 和 `references/performance-gates.md`。

## 长上下文、compact 与换 agent

不要把聊天摘要当作状态。每次暂停、compact 前或移交前，必须维护：

- `STATE.md`：当前 checkpoint、权威基线、阻塞、尝试次数、残留进程/文件。
- `TRUTH.md`：带来源、版本和核对时间的当前事实，明确 `verified/assumed/stale/contradicted`。
- `HANDOFF.md`：最短恢复路径、权威 hash、下一条可执行命令、必须避开的失败家族。
- `CANDIDATES.md`：候选、预测、结果、裁决、回退点和重开条件。
- `REVIEW.md`：独立 Reviewer 的 gate 结论，不写实现者自我评价。
- `METRICS.md`：攻坚效率、重复探索、证据返工和恢复成本的趋势。

新 agent 的第一条纪律是“验证而不是相信”：复算 hash、检查工作树与设备、重跑一个最小 smoke，
再决定是否继续旧路线。完整恢复协议见 `references/context-continuity.md`。

## 多 agent 模式

多 agent 只用于真正独立的专业工作，不用于增加“看起来在并行”的噪声。

- **Orchestrator**：维护目标、检查点、路由冲突、证据准入和最终裁决；不替 Driver 写实现。
- **Driver**：独占一个 worktree 和一个检查点，产出实现、原始证据和回退点。
- **Specialist**：做方案、算法、硬件、API 或测量方法研究，输出选择与风险，不改生产代码。
- **Reviewer**：从交付物、出口标准和原始证据独立验收，不读实现者结论。
- **Guard**：审查不可逆操作、共享设备冲突、数据/凭据泄露和测量污染，不代执行。
- **Integrator**：只从已评审的候选和证据合并，负责最终 diff、兼容性和交付清理。

隔离、租约、消息和合并协议见 `references/multi-agent.md`。

## 信息纪律

每轮信息分成四类：

1. **权威事实**：进入 TRUTH，必须有来源和核对时间。
2. **决策记录**：进入 STATE/PLAN/REVIEW，说明为什么继续、回退或关闭。
3. **过程证据**：进入 evidence/worklog，保留命令、原始输出和 hash。
4. **噪声**：推测、重复摘要、无来源数字、已被取代的中间结论，不进入权威状态。

只记录会改变下一步动作的信息。优先保留：

- 当前关键路径和量级；
- 失败结构家族与已经排除的路线；
- 能跨 shape/版本/任务复用的 invariant 和 primitive；
- 会让旧结论失效的版本、hash、分布或口径变化。

文档模型和去噪规则见 `references/information-hygiene.md`。

## 长程目标推进

当直接达成目标困难时，不要降低目标；把目标拆成“结果 + 证据 + 资源”的连续关卡：

- 先锁定不可变正确性契约和目标测量口径；
- 再建立真实基线；
- 再建立关键路径预算；
- 再消除结构瓶颈；
- 再提高泛化与稳定性；
- 最后做交付与独立复审。

允许路线变化，不允许验收口径静默变化。若目标本身变化，更新 TRUTH/PLAN 并明确说明哪些旧证据
失效。

## 结束条件

只有同时满足以下条件才可宣布完成：

1. 目标语义和所有适用边界在真实目标环境通过。
2. 性能/资源目标按官方口径通过，并有原始证据和独立复现。
3. 结果绑定到干净或完整可重建的源码/二进制状态。
4. 全量回归没有未解释的 P0/P1 回归。
5. Reviewer 从证据独立给出通过结论。
6. 实验代码、临时状态、未证 route 和敏感信息已从交付物清理。
7. HANDOFF 和复现命令足以让新 agent 从零重建结果。

若未满足，输出的是当前最佳状态、剩余风险、下一条最短路径和明确 blocker，不写“基本完成”。

## 参考文件路由

- 自主循环、决策树和止损：`references/autonomous-loop.md`
- 事实、证据等级和 provenance：`references/evidence-and-truth.md`
- 官方工具发现与使用：`references/official-tools.md`
- 性能归因和调优：`references/performance-gates.md`
- 正确性与数值门禁：`references/correctness-gates.md`
- 多 agent 隔离与协作：`references/multi-agent.md`
- compact/换 agent 恢复：`references/context-continuity.md`
- 文档与信息去噪：`references/information-hygiene.md`
- 上游交付与 PR 纪律：`references/upstream-delivery.md`
- 历史失败家族与反模式：`references/failure-patterns.md`
- 攻坚效率和切入点评估：`references/optimization-efficiency.md`
- 通用优化家族与执行顺序：`references/optimization-playbook.md`
