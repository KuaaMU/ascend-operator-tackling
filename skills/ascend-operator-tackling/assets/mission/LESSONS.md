# Lessons and Hard Gates

只记录可复用的失败机制和防止重复投入的硬规则。

| ID | Scenario | Mechanism | Hard gate | Reopen condition | Evidence |
|---|---|---|---|---|---|
| L001 | pending | - | - | - | - |

## Rules

1. 不盲测、不盲改：先归因，再单变量实验。
2. 不用 raw primitive 或局部指标替代目标 API 验收。
3. 不用内容型 shortcut 绕过完整语义和 fallback。
4. 不用一次近门限结果推广路线。
5. 不把未提交、未复现的代码当作权威基线。
6. 连续三次同结构无收益后停止并重规划。

