# CHANGES.md — v2 优化清单

v1 是用户在一次 Ascend/CANN 算子攻坚（最终未彻底达标）中总结的 skill。
v2 的目标：**把领域通用的攻坚内核抽出来，把 Ascend 专属内容下沉为 profile，
把实战教训编译成可执行的纪律**。skill 名保持 `ascend-operator-tackling`
（历史兼容），但内核已领域无关。

---

## 一、新增

| # | 内容 | 位置 | 为什么 |
|---|---|---|---|
| A1 | L0 第一性原理（5 条） | SKILL.md | v1 的 10 条契约平铺、无主次；压缩为 5 条常驻原则，其余降级为 L1/L2 触发式规则，对抗指令稀释 |
| A2 | 三层阅读协议 | SKILL.md + assets/mission/AGENT.md | 渐进披露：启动只读 L0+L1，进循环读 L2，撞门禁按需读 L3；弱模型可只用 L0+L1+L4（清单+脚本） |
| A3 | 触发式改写 | 全 skill | 陈述式→WHEN…THEN…；弱模型对"如果…就…"的执行远好过对抽象原则的领悟 |
| A4 | 赛马纪律 | references/multi-agent.md | v1 有 CANDIDATES 台账但无"定期处决"；用户实战教训：单路线死磕 40→170 渐近线。新增：worktree 零成本并行、统一记分牌、每 N 轮强制处决、决赛圈才上稀缺硬件 |
| A5 | 文件财政纪律 | references/file-hygiene.md | 用户实战教训：agent 产出/爬取/远端文件混乱。新增：目录契约（scratch/research/hard-set）、搜索配额、远端隔离、工具降级链；`mission_lint.py` 加对应检查 |
| A6 | 困难集纪律 | references/hard-set.md + assets/mission/HARDSET.md | 用户实战教训：极端用例拿常规路线没办法。新增：准入条件、独立爆破、换算法路线触发器（连续 N 轮个位数增长 THEN 强制换路线） |
| A7 | 好/坏实例（few-shot） | references/examples.md | 3 个实例（困难集换路线 / 白名单+口径偷换 / 赛马处决）；examples > rules，尤其对弱模型 |
| A8 | Profile 机制 | references/profiles/ascend-cann.md + .tools.json | 内核领域无关；Ascend/CANN 专属（数值门禁细节、7 层优化 playbook、官方工具、算子失败家族）下沉为 profile，按需加载 |
| A9 | `init_mission.py --profile` | scripts/ | 初始化时选定 profile，AGENT.md 模板自动引用 |
| A10 | `discover_environment.py --profile` | scripts/ | 工具列表 profile 驱动（base 通用 + profile JSON 增补），不再硬编码 CANN 工具 |

## 二、修改

| # | v1 | v2 | 为什么 |
|---|---|---|---|
| M1 | SKILL.md 216 行：契约/启动/循环/优先级/门禁全塞一起 | SKILL.md：只放 L0+L1+循环骨架+索引，细节下沉 references/ | SKILL.md 是每次必读的上下文，越薄越好；细节按需加载 |
| M2 | 10 条核心契约 | 5 条第一性原理 + 触发式 L1 规则 | 主次分明；触发式可执行 |
| M3 | autonomous-loop.md（状态机+纠错） | references/loop.md（精简，触发式） | 去掉重复叙述，保留状态机骨架与两条止损规则 |
| M4 | 六角色（Orchestrator/Driver/Specialist/Reviewer/Guard/Integrator） | 三核心角色 + 三可选角色 | 六角色是那次复杂协作的疤痕；多数任务三角色够用 |
| M5 | METRICS.md 11 个指标 | 建议跟踪 3–5 个，看趋势 | 11 个指标会诱使 agent 为填表而填表 |
| M6 | 切入点评分公式（乘除七项） | 启发式七维度粗评（高/中/低） | 伪量化给人精确的幻觉；粗评+铁律更诚实 |
| M7 | NPU/设备租约 | 稀缺资源租约（通用化） | 机制通用，NPU 只是实例 |
| M8 | 证据 A 级"目标硬件真实运行" | A 级"目标环境可复现证据" | 去硬件绑定 |
| M9 | mission_lint：缺文件/占位符/HANDOFF 过期 | + scratch 孤儿目录 ERROR、research 超量 WARN、根目录游荡 md WARN | 给文件财政纪律配牙齿 |
| M10 | AGENT.md 读取顺序 13 项 | 三层阅读协议 + 本任务 6 步顺序 | v1 的 13 项清单无优先级，agent 会抓瞎 |

## 三、删除 / 降级 / 移动

| # | v1 内容 | 处理 | 去向/理由 |
|---|---|---|---|
| D1 | optimization-playbook.md（7 层 NPU 优化顺序）全文 | 移动 | profiles/ascend-cann.md（压缩版）。这是 NPU kernel 专属 playbook，不属于通用内核 |
| D2 | correctness-gates.md 中数值细节（ULP/FMA/NaN/Inf/AIC-AIV/并发状态机） | 移动 | profiles/ascend-cann.md。通用门禁骨架保留在 references/gates.md |
| D3 | official-tools.md 全文（profiling/logging/sanitizer/debugger/compiler 五节） | 移动+压缩 | profiles/ascend-cann.md（一页清单）。内核只保留"一手观测工具归因"原则 |
| D4 | failure-patterns.md 中 5 个算子专属家族（floor 忽略、raw primitive、内容型 shortcut、状态污染、并行神话） | 移动 | profiles/ascend-cann.md。通用 8 家族保留在 references/failure-patterns.md |
| D5 | upstream-delivery.md 全文 | 压缩并入 | references/gates.md 第三道门（交付门）。原文件多为通用交付常识，独立成文件是过度拆分 |
| D6 | information-hygiene.md 全文 | 合并 | 精华并入 references/file-hygiene.md 与 state-files.md；原文件的"信息分层"理论保留骨架，删去重复论述 |
| D7 | context-continuity.md 全文 | 压缩并入 | references/state-files.md。原文件 200+ 行，多为同一协议的不同表述 |

---

## 四、疤痕审计（v1 规则逐条 verdict）

背景：v1 写于一次**未彻底达标**的攻坚之后。以下规则疑似"疤痕组织"——
针对那次特定失败的过度纠正。逐条审计：

| 规则 | Verdict | 理由 |
|---|---|---|
| "禁止只按 CSV/benchmark shape 堆白名单" | **保留并泛化** | 这是真教训，且跨领域成立（任何"按测试用例打补丁"都是局部最优）。泛化为"禁止按测试用例堆特例"，触发器进 hard-set.md |
| "正确性先于性能"（第3条契约） | **保留** | 通用第一性原理，与那次失败无关 |
| "连续三次无正收益即止损" | **保留** | 通用，与领域无关；触发式已是最优形态 |
| 七节数值正确性门禁（ULP/NaN/FMA…） | **降级为 profile** | 只适用于数值计算/加速器；对通用工程任务是噪音。移入 ascend-cann.md |
| 7 层优化顺序（删工作→指令级） | **降级为 profile** | NPU kernel 专属；通用版压缩为"先删工作、再降水位、最后微调"一句话，放在 gates.md 归因节 |
| 六 agent 角色 | **简化** | 那次任务用了复杂编排，不代表通用最优；三核心+三可选 |
| 11 个效率指标 | **降级为建议** | 有"为填表而填表"的风险；保留 6 个，看趋势 |
| "官方工具优先"整套流程 | **保留原则，移动清单** | "一手观测先于猜测"是通用原则；具体工具清单是 CANN 专属，移入 profile |
| 设备租约（含 process IDs、频率/热状态） | **泛化保留** | 机制通用（任何稀缺/共享资源）；字段示例保留 NPU 痕迹作例子 |
| "失败家族 13 个" | **拆分** | 8 个通用保留，5 个算子专属移入 profile。v1 把一次任务的全部伤疤都写成了"通用规律"，这是典型的疤痕过度泛化 |
| 切入点评分公式 | **降级为启发式** | 乘除公式是"精确的幻觉"；那次任务后为了"科学化"而加的，实战中没人真算 |
| "证据先于宣传：不得写 PASS/GO" | **保留** | 通用，且是 agent 任务最高频的作弊模式 |
| "新 agent 验证而不是相信" | **保留** | 通用，这是整个 skill 最值钱的一句话之一 |

**审计结论**：v1 的内核（状态外置、分层评测、单变量+kill 线、独立评审、
失败家族）是真金，跨任务成立；疤痕主要集中在**领域绑定**（CANN/数值细节
写进内核）和**过度细化**（六角色、11 指标、评分公式）两处。v2 的改动
90% 是"分层"（该下沉的下沉），不是"删除"——没有扔掉任何真教训。

---

## 五、行数预算（v2）

- SKILL.md：~150 行（<250 ✓）
- references/ 单文件：均 <150 行 ✓（loop.md 最长，约 120 行）
- profiles/ascend-cann.md：约 110 行 ✓
