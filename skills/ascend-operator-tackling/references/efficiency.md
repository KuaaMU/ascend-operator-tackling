# 攻坚效率：信号与复盘

长程攻坚最大的浪费不是一次失败实验，而是：无可信基线反复测量、
在错误路线上参数扫描、同一失败结构被反复重开、旧产物造成返工。

## 效率记分牌（METRICS.md）

每个 checkpoint 更新一次，看趋势不看单点。建议只跟踪 3–5 个，
不要为填表而填表：

| 指标 | 含义 | 理想方向 |
|---|---|---|
| Time to trusted baseline | 接手到获得可复现权威基线的时间 | ↓ |
| Cost per eliminated hypothesis | 排除一个假设的平均成本 | ↓ |
| Duplicate reopen rate | 重开已关闭路线的次数 | → 0 |
| Stale-evidence escapes | 用过期证据决策后才发现的次数 | → 0 |
| Cross-case reuse | 一个结构改动覆盖的用例数 | ↑ |
| Rework ratio | 因环境/hash/口径错误浪费的时间占比 | ↓ |

早期可用相对单位（"一个 probe 成本"），不要为精确数字引入不稳定测量。

## 效率下降信号

WHEN 出现以下任一 THEN 暂停加实验，先修方法：
1. 连续多轮无新增 verified fact；
2. 还在争论权威基线或 hash；
3. Candidate 快速增长但关闭条件不清；
4. 同一失败家族被不同 agent 重开；
5. REVIEW 长期 pending；
6. HANDOFF 旧于 STATE；
7. 文档增长快于可验证结论。

## Checkpoint 复盘（5 问）

1. 这轮最重要的 verified fact 是什么？
2. 哪个不确定性被消除了？哪个候选被关闭，重开条件是什么？
3. 下一步为什么比第二选择更值得做？
4. 哪些信息该删除或降级？
5. 换 agent 能否 10 分钟内按 HANDOFF 恢复？
