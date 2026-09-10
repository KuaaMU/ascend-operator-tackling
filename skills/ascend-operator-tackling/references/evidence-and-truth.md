# 事实、证据与 Provenance

## 原则

状态文件不是聊天摘要。它是新 agent 在当前环境中做出决策所需的可验证事实集合。

任何会改变下一步动作的陈述都应有：

- 稳定 ID；
- 可复核来源；
- 版本或日期；
- 核对时间；
- 状态；
- 适用范围。

## 状态语义

| 状态 | 含义 |
|---|---|
| `verified` | 有原始证据或一手来源，并已独立核对 |
| `assumed` | 当前用于推进的工作假设，不能作为最终结论 |
| `unverified` | 只有他人转述、公开文章摘要或未复现实验 |
| `stale` | 来源版本、代码、环境或测试口径已经变化 |
| `contradicted` | 新证据与旧结论冲突，不能继续直接使用 |
| `closed` | 已明确达到重开条件的否定结论 |

## 证据层级

### A 级：目标环境可复现证据

- 目标硬件/系统的真实运行；
- 原始日志、trace、profile、CSV/JSON；
- 明确命令、源码/二进制 hash、环境版本；
- 可独立复跑。

这是验收和 promote 的必要条件。

### B 级：受控过程证据

- 单阶段 probe；
- CPU 模拟、host mock、静态分析、编译诊断；
- 小样本方向筛选；
- 旧版本或邻近硬件结果。

可用于归因和选择实验，不能单独宣布最终通过。

### C 级：外部或二手证据

- 官方文档的未验证解释；
- 上游 PR、论文、博客、他人报告；
- 与目标版本/硬件不同环境的性能数字。

可用于形成假设，必须转化成本地最小实验后才能 promote。

## 数字 Provenance

任何进入 STATE、TRUTH、REVIEW 或交付报告的关键数字，至少要能追溯：

```text
value:
unit:
scope:
machine/device:
runtime/compiler:
source repo:
source hash:
binary hash:
command:
input/reset:
warmup/samples:
statistic:
raw evidence:
recorded_at:
```

缺失 provenance 的数字只能存在于临时分析中，不能作为决策依据。

## 证据目录

建议每个实验目录至少包含：

```text
manifest.md
commands/
logs/
outputs/
hashes.txt
artifacts/
```

`manifest.md` 必需信息：

- 目的、假设和 kill criterion；
- 目标 case/route；
- 环境与设备；
- 源码、二进制、输入和脚本 hash；
- 构建命令、运行命令、环境变量；
- warmup、采样数、统计方法、输入恢复方式；
- 期望与实际；
- 退出码、原始 stdout/stderr；
- 结论、限制与下一步。

## 事实失效规则

以下变化必须让相关事实重新核验：

- 任务书或验收口径变化；
- 上游仓库 HEAD、分支基线或依赖版本变化；
- 编译器、CANN、驱动或设备变化；
- 测试数据、随机种子、生成规则或阈值变化；
- 性能二进制或实际加载路径变化；
- worktree 从 clean 变为 dirty，或 dirty diff 变化；
- 发现旧结论只在特定输入分布/顺序/热状态下成立。

更新时保留历史，不要静默覆盖。把旧记录标为 `stale` 或指向新证据。

## 冲突处理

两个事实冲突时：

1. 优先一手来源和目标环境原始证据；
2. 若证据强度接近，暂停依赖该事实的优化；
3. 设计一个最小实验区分两者；
4. 在实验中同时记录环境、输入和路由；
5. 未解决前，不把任一版本写入交付结论。

## 权威文档

每个主题只能有一个权威版本：

- 当前状态：`STATE.md`
- 可复用事实：`TRUTH.md`
- 当前计划：`PLAN.md`
- 独立验收：`REVIEW.md`
- 候选实验：`CANDIDATES.md`
- 恢复路径：`HANDOFF.md`
- 过程细节：`worklog/` 和 `evidence/`

被取代的报告必须标记 `superseded` 或归档，不能与权威版本同时声称最终结论。

