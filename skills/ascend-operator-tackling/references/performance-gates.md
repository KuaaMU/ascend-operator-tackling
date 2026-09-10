# 性能归因与门禁

## 先定义“性能”

明确以下口径，任何一项变化都视为新测量：

- 端到端、API submit-to-complete、kernel-only、device task time 或某单阶段；
- 算术平均、中位数、最小值、P95/P99 或最大值；
- warmup、有效采样、输入恢复、同步位置；
- 批大小、shape、dtype、布局、stride、异常值和分布；
- 设备、频率、负载、并发进程和功耗/热状态。

验收只接受任务书或用户指定的口径。其他口径用于归因，不能偷换验收。

## 测量纪律

1. 测前确认设备状态和占用，记录环境快照。
2. 每样本恢复全部可变输入和必要状态，避免上一轮结果污染下一轮。
3. 使用稳定 warmup，并在报告中记录。
4. 方向筛选可用少量样本，promote 和最终裁决使用正式样本量。
5. 同时保存统计值、原始样本、最大值和异常样本。
6. 不静默剔除异常；先用设备、调度、内存、热状态或输入解释。
7. 同机、同构建、同输入 A/B；变更前后都要跑控制组。
8. 跨 run 方差大时先测量方差，不要把近门限翻转解释为代码收益。

## 归因顺序

### 1. 路由与语义

先确认 case 实际走了哪条 route，以及 route 是否正确地解决了目标问题。
同一个 shape 在不同版本、batch、layout 或 gate 下可能走完全不同的图。

### 2. 端到端与任务级

用官方 profiling 分离：

- host 准备、构建和提交；
- launch/enqueue 数量与间隔；
- device kernel/task 组成；
- 同步、event 和 stream 依赖；
- API 与 device 时间差。

### 3. 阶段账本

把主路径拆成互斥阶段，例如：

- gate / search；
- transform / pack / deinterleave；
- compute；
- exchange / combine；
- writeback；
- host/sync gap。

阶段之和与端到端差值必须解释。存在“未知 gap”时，先查测量和路由，不要拍脑袋归因。

### 4. Floor 与预算

分别测量：

- copy/transform floor；
- launch floor；
- minimum compute cost；
- 同步或 barrier floor；
- 可压缩和不可压缩部分。

若 floor 已超过目标，继续调 kernel 参数没有意义，必须改执行图或目标边界。

## 候选实验

每个候选只改变一个主变量：

- 路由条件；
- tile/partition；
- 数据布局；
- 并行映射；
- 同步策略；
- 融合/拆分；
- 数值算法或精度补偿。

同时改变 host route、kernel tile、线程数和 stream 配置，即使结果变好也无法泛化。

必须记录：

```text
candidate:
baseline:
single variable:
target cases:
control cases:
prediction:
kill criterion:
measured:
decision:
best delta:
regressions:
evidence:
rollback:
```

## 泛化判断

候选是否值得推广，不看单个最好 shape，而看：

1. 是否命中多 case 的共同关键路径；
2. 是否能用资源模型或结构条件解释；
3. 是否避免针对 CSV/benchmark shape 的白名单；
4. 是否在不同 batch、相邻 shape、padding/stride 和分布下成立；
5. 是否保持已通过区间不回归；
6. 是否能作为公共 primitive 复用；
7. 失败时是否有明确关闭和重开条件。

当收益只集中在少数 case，先检查：

- route cliff；
- 输入分布差异；
- 单次方差；
- 编译/内联差异；
- batch 摊薄效应；
- 设备占用或频率差异。

## Promote 门

只有同时满足才可 promote：

- 正确性 gate 通过；
- 目标性能口径通过；
- 代表性集合和全量回归通过；
- 没有未解释的 P0/P1；
- 至少一次独立复现；
- 关键区间收益有结构解释；
- 失败路线和回退点已记录；
- 生产树不含实验开关和未接线代码。

## 常见误判

- 用 median 通过代替任务书 mean；
- 用 raw primitive 时间代表完整 API；
- 用 kernel-only 代表端到端；
- 用 no-reset 的快速重复代表真实输入处理；
- 用理想输入分布代替通用语义；
- 用 11 次方向结果代表正式通过；
- 用同 run 顺序效应当作算法改善；
- 用单个 best sample 代替稳定结果。

