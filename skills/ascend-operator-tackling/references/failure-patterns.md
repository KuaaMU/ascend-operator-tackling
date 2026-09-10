# 历史失败家族与反模式

本文件不是任务清单，而是从多类 Ascend 算子攻坚中抽象出的可复用失败模式。命中时先检查机制，
不要机械套用结论。

## 1. 基线失效

### 症状

- 旧日志与新源码/二进制不匹配；
- local、remote、build、out 目录各有一份库；
- 结果在重建后整体漂移；
- dirty worktree 被当作权威。

### 防护

- 记录 source/binary/test/runner hash；
- 确认实际加载路径；
- clean build 或完整 dirty manifest；
- 关键结论只在可回滚状态上产生。

## 2. 摘要覆盖事实

### 症状

- STATE 顶部写 A，底部 session log 已推进到 B；
- REVIEW 长期 pending，但实现继续扩展；
- 旧报告仍自称权威；
- 新 agent 从过时 checkpoint 开始。

### 防护

- 单一权威规则；
- gate 关闭必须更新 REVIEW；
- HANDOFF 每日/每轮更新；
- 过期文档显式标 stale/superseded。

## 3. 参数扫描代替归因

### 症状

- 连续扫 tile、thread、slot、stream、batch split；
- 每个 case 需要不同参数才过；
- 收益不稳定、跨 run 翻转；
- 没有 phase/critical path 账本。

### 防护

- 先按 route 分类；
- 先测 floor 和阶段预算；
- 单变量实验；
- 三次无结构收益即停止。

## 4. Raw primitive 当作完整路径

### 症状

- 用 GEMM/vector/copy 单阶段 microbench 推断完整 API 过门；
- 忽略 transform、combine、launch、host 和同步；
- raw 很快但 full API 很慢。

### 防护

- 同时测量 raw、transform、combine、host 和 full；
- 解释完整差额；
- 以目标 API 口径验收。

## 5. Floor 忽略

### 症状

- 目标比 launch/transform/同步 floor 还小；
- 反复优化不可压缩部分；
- 多 launch/enqueue 被忽略。

### 防护

- 单独测 launch floor、copy floor、compute floor；
- 若 floor 超目标，改执行图或重新核对目标；
- 不为低于 floor 的 case 继续微调。

## 6. 内容型 Shortcut

### 症状

- 利用 benchmark 输入具有对角占优、密集、无交换等特性；
- fast path 没有严格证明或完整 fallback；
- 精度测试只覆盖相同分布。

### 防护

- 只允许结构性 gate 或严格数学 gate；
- 未命中必须 exact fallback；
- 加入非该分布、对抗和异常用例；
- 内部 marker 不复用用户输出。

## 7. 状态污染

### 症状

- 内部 marker 写在 API info/status 字段；
- 连续调用复用缓冲后行为不同；
- 上一轮 workspace 状态影响下一轮；
- cache key 不包含影响结果的维度。

### 防护

- 内部状态独立分配；
- 每次调用有明确初始化；
- cache key 覆盖所有影响结果的参数；
- 连续调用、buffer reuse、并发调用测试。

## 8. 并行神话

### 症状

- “增加 stream/thread/block 一定更快”；
- 多流、多核、多矩阵驻留导致调度和同步税；
- 局部并行但总 wall 变慢。

### 防护

- 先做串行 phase 预算；
- 证明可重叠的依赖；
- 同构建 A/B；
- 关注 critical path，不关注平均利用率。

## 9. 方差误判

### 症状

- 11-sample 或单次结果决定 promote；
- ±2% 翻转被当成算法收益；
- 同 case 不同会话差异大于候选差异；
- 近门限结果缺少重复实验。

### 防护

- 方向筛选和正式裁决分开；
- 正式 gate 用目标样本量和多次复现；
- 记录跨 run variance；
- 近门限必须留 margin。

## 10. Shape 白名单蔓延

### 症状

- route 表只含测试出现的精确 n/shape；
- 相邻 shape 落回慢路径；
- 每个新 case 增加一个 if 或 kernel；
- 代码通过“特例总和”而非统一模型。

### 防护

- 资源驱动的连续区间；
- 相同算法/primitive 参数化；
- 表 miss 自动 fallback；
- 泛化 case 和 holdout 回归。

## 11. 未验证的中途结论

### 症状

- 从理论、文档或参考代码直接得出 GO；
- 结论进入 STATE 后没有再实验；
- 后续 agent 在其上继续叠加。

### 防护

- 标 assumed/unverified；
- 写最小验证和 kill criterion；
- promote 前必须目标环境证据。

## 12. 上下文断层

### 症状

- 新 agent 重复失败实验；
- 找不到最后一条可执行命令；
- 只留聊天结论；
- 不知道当前二进制和分支。

### 防护

- HANDOFF 单一恢复路径；
- 候选关闭/重开条件；
- hash 和环境快照；
- 最小 smoke 复验。

## 13. 工程污染

### 症状

- 生产树遗留 probe/env/dump；
- `.orig/.pre` 备份；
- 未接线 kernel；
- 根构建偷偷加入实验依赖；
- 测试专用代码进入生产库。

### 防护

- 生产/实验 worktree 隔离；
- 交付前 allowlist；
- clean build；
- diff 审查；
- Reviewer 检查复用边界。

## 使用方式

当新问题与某个家族相似时：

1. 读该家族的“共同机制”，不要只抄旧结论；
2. 用当前环境最小实验确认是否命中；
3. 若命中，直接采用防护；
4. 若不命中，记录区别，不要关闭整个家族。
