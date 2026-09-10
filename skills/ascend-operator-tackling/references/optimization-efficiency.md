# 攻坚效率与切入点评估

## 目标

长程攻坚最容易出现的浪费不是一次失败实验，而是：

- 在没有可信基线的状态下反复测量；
- 在错误 route 上做参数扫描；
- 同一个失败结构被不同 agent 重开；
- 旧二进制、旧摘要或脏工作树造成返工；
- 重要结论没有及时进入恢复资产。

本文件定义如何评价“切入点是否准、信息是否有用、效率是否提高”。

## 任务经济学指标

每个 checkpoint 更新一次，趋势比单点绝对值更重要。

| 指标 | 定义 | 理想方向 |
|---|---|---|
| Time to trusted baseline | 从接手到获得可复现权威基线的时间 | 下降 |
| Cost per eliminated hypothesis | 排除一个候选/结构假设的平均时间、设备费和返工 | 下降 |
| Promotion yield | promote 数 / 完成候选数 | 上升，但必须伴随泛化 |
| Duplicate reopen rate | 重开已有关闭条件路线的次数 | 趋零 |
| Stale-evidence escapes | 使用过期 hash/版本/摘要后才发现的次数 | 趋零 |
| Review lag | 新证据产生到独立评审之间的时间 | 下降 |
| Recovery time | 新 agent 从 HANDOFF 到可继续实验的时间 | 下降 |
| Regression escape | 已通过区间在生产变更后静默回归的次数 | 趋零 |
| Critical-path coverage | 已解释的目标缺口 / 总目标缺口 | 上升 |
| Cross-case reuse | 一个结构改动覆盖的 case/route 数 | 上升 |
| Rework ratio | 因环境、hash、输入、口径错误浪费的时间占比 | 下降 |

可在早期使用相对单位（例如“一个 probe 成本”“一个 session 成本”），不要为了精确数字引入
不稳定测量。

## 切入点评分

候选优先级可近似为：

```text
priority =
  target_impact
  * generalization
  * attribution_confidence
  * evidence_gain
  / (experiment_cost * risk * duplicate_probability)
```

各项用相对分：

- `target_impact`：能否覆盖显著的目标缺口；
- `generalization`：是公共 primitive/route，还是单个 case 特例；
- `attribution_confidence`：当前证据是否把它锁定为关键路径；
- `evidence_gain`：成功或失败后能排除多少不确定性；
- `experiment_cost`：实现、设备、等待和人工成本；
- `risk`：正确性、回归、不可逆或共享设备风险；
- `duplicate_probability`：是否已有失败家族或关闭条件。

必须优先选择“能显著减少不确定性”的实验，而不是只选理论收益最大的实验。

## 切入点是否准

### 好切入点

- 直接命中已测量的关键路径或 floor；
- 失败也能排除一个重要机制；
- 可跨多个 shape/route 泛化；
- 与现有失败家族有明确区别；
- 有明确 kill criterion 和回退点。

### 坏切入点

- 没有 phase/route 归因；
- 同时改变多个变量；
- 只在单个 benchmark case 上可复现；
- 需要不断增加白名单；
- 结果依赖未验证内容 gate；
- 目标量级小于 launch/transform floor；
- 与已关闭路线本质相同，只换参数。

## 信息价值

每类信息按“是否改变下一步动作”评分：

### 高价值

- 会让路线继续、回退或关闭的测量；
- 能解释多个失败 case 的共同机制；
- 会改变权威 hash/环境/口径的事实；
- 能减少未来重复实验的 lesson。

### 低价值

- 不影响决策的漂亮数字；
- 重复已有结论的日志摘要；
- 没有 provenance 的历史数字；
- 只对单个 case 的参数 sweep；
- 在错误路由上得到的量级。

### 噪声

- 聊天转述；
- 旧摘要；
- 未复现的第一次观察；
- 被新版本取代的 profile；
- 与本目标口径无关的吞吐/延迟指标。

## 效率下降信号

出现以下信号时暂停增加实验，先修复方法：

1. 连续多轮没有新增 verified fact；
2. 仍在争论权威基线或二进制 hash；
3. Candidate 数量快速增长但关闭条件不清晰；
4. 同一失败家族被不同 agent 重开；
5. REVIEW 长期 pending；
6. HANDOFF 旧于 STATE；
7. 每次实验都需要重新解释 route；
8. 近门限 case 频繁翻转；
9. 文档增长速度快于可验证结论；
10. 生产树持续累积实验开关和未接线代码。

## Checkpoint 复盘问题

每个 checkpoint 结束时回答：

1. 这轮最重要的 verified fact 是什么？
2. 哪个不确定性被消除？
3. 哪个候选被关闭，重开条件是什么？
4. 有哪些重复劳动可以避免？
5. 下一步为什么比第二选择更值得做？
6. 当前信息里哪些应该删除或降级？
7. 如果换 agent，能否在 10 分钟内恢复？

