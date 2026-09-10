# 通用优化手册

## 优化顺序

按收益、风险和可泛化程度排序：

1. 删除不必要的工作；
2. 降低数据搬运和中间量放大；
3. 改善 locality 和布局；
4. 选择正确的执行单元；
5. 重叠独立阶段；
6. 调整 tile/partition/parallel mapping；
7. 最后做指令级微调。

不要从第 6/7 层开始。参数扫描只有在关键路径、floor 和 route 已明确后才有意义。

## 1. 删除工作

候选方向：

- 不读取未使用数据；
- 不写不会使用的中间结果；
- 不重复计算已缓存值；
- 跳过被严格证明为空的分支；
- 合并重复的 transform、scale、copy；
- 避免为 small case 启动不必要的 fallback。

风险：

- 改变语义或边界行为；
- fast path 掩盖未覆盖输入；
- 跳过的是“当前 benchmark 不需要”而不是“数学上不需要”。

证据：

- 正确性 gate；
- 路由命中/未命中统计；
- 删除前后阶段账。

## 2. 降低搬运

先算实际流量，不只看输入输出大小：

```text
真实数据量
中间量放大倍数
读写次数
有效带宽
每阶段 GM/on-chip 往返
```

候选方向：

- 中间结果留 UB/L1/L2；
- 融合相邻阶段；
- 避免 full-plane 物化；
- layout 转换一次完成；
- 以对齐批量搬运替代逐元素访问；
- 复用只读 operand；
- 对 streaming 中间量使用合适 cache policy；
- 让计算单元直接消费另一单元的片上结果。

风险：

- UB/L1 容量；
- 对齐和 padding；
- 跨核可见性；
- cache key 和生命周期；
- 融合后难以并行。

证据：

- traffic ledger；
- 阶段 profile；
- raw/transform/combine/full 四段对照；
- 资源占用和占用率。

## 3. 改善 Locality 和 Layout

候选方向：

- SoA/plane 布局服务向量化；
- AoS 与 SoA 在边界转换，而不是频繁转换；
- 连续 access 服务 MTE；
- 小矩阵常驻片上；
- 让 batch 维成为稳定的并行维；
- 避免 stride 导致 4-byte burst 或 cache-line 浪费。

判断标准：

- 每个 load/store 的有效字节比例；
- 相邻工作单元是否复用同一 operand；
- layout 转换成本是否能在多次使用中回收；
- 非连续性是否只存在于边界还是贯穿主循环。

## 4. 选择执行单元

候选单元可能包括 SIMT、SIMD/Reg、Vector、Cube、DMA、SDMA、CPU/STARS。
选择依据：

- 算术强度；
- 数据连续性和 shape；
- launch/pipeline 固定成本；
- 是否需要交换、搜索、分支或间接寻址；
- 与前后阶段的片上交接能力；
- 精度模式是否满足语义。

不要因为某单元“理论峰值高”就默认更快。必须证明完整路径、转换和同步成本后仍占优。

## 5. 重叠阶段

只重叠真正独立的依赖：

- 下一个 batch 与前一个 compute；
- layout transform 与独立 compute；
- 下一 panel 的输入准备与当前 panel 的输出；
- 读与写分别位于不同 stage buffer。

风险：

- 多 stream/event 固定税；
- 资源争用；
- 依赖表达错误；
- 测量时看似并行，实际 critical path 更差。

证据：

- event/timeline；
- 串行 vs 并行同构建 A/B；
- 任务数、launch 数和 gap；
- 设备占用和上下游 dependency。

## 6. Tiling、Partition 和并行映射

参数必须由资源预算驱动：

```text
tile = f(UB/L1/L0 capacity, work per element, reuse distance, alignment)
```

而不是：

```text
tile = benchmark_case 对应的常数
```

每个 route 要回答：

- 边界 shape 如何走；
- 尾块如何走；
- batch 不整除如何走；
- padding/stride 如何走；
- 不同 batch 是否仍使用同一执行图。

## 7. 指令级优化

只在前面已完成且 profile 指向该处时做：

- 减少同步；
- 选择正确对齐；
- 减少标量/向量往返；
- 减少寄存器压力；
- 循环展开；
- FMA/收缩/精度模式；
- 编译器 barrier 和 pipeline flag；
- 合并小 VF/micro-kernel 调用。

必须同时记录源码、编译选项、device binary 和运行时结果，因为这类优化最容易出现“源码等价、产物不等价”。

## 复用官方能力还是自研

优先顺序：

1. 目标仓库已有的正确公共 primitive；
2. 官方高阶 API 或算子，若能满足语义、性能和依赖边界；
3. 官方低层 instruction/API，若高阶能力不可控；
4. 自研 kernel。

选择高阶 API 时检查：

- 是否引入生产不需要的依赖；
- 是否能在关键路径上避免额外 GM 往返；
- 是否有公开的精度/异常值语义；
- 是否可配置到目标 tile 和数据布局；
- 是否仍能满足异步和 stream 语义。

选择自研时检查：

- 是否有独立 primitive 测试；
- 是否有清晰的回退路径；
- 是否只解决一个通用问题，而不是一个 case。

## 优化候选模板

```text
问题：
当前关键路径：
瓶颈量级：
优化家族：
为什么现在做：
单一变量：
泛化范围：
预期收益：
失败判定：
回退点：
需要的新证据：
```

