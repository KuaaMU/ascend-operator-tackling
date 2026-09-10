# Plan

方向：先锁定语义和可复现基线，再定位关键路径，做可泛化的结构优化，最后独立验收与交付。

## Checkpoints

| ID | Goal | Minimum experiment | Pass evidence | Kill criterion |
|---|---|---|---|---|
| CP0 | Live authority and environment | hash + device + tool discovery + smoke | reproducible authority record | any authority mismatch |
| CP1 | Correctness contract | reference + adversarial cases | target correctness gate | unclosed P0/P1 |
| CP2 | Performance attribution | official tooling + phase budget | critical-path ledger | unexplained gap |
| CP3 | Structural optimization | one-variable candidates | target gains + no regression | three no-gain attempts |
| CP4 | Generalization and delivery | full regression + independent review | clean reproducible package | any unresolved P0/P1 |

## Change Control

- 目标或验收变化：更新 TRUTH 和本文件，标记失效证据。
- 同一问题连续三次无结构收益：停止参数扫描并重规划。
- 任何 promote 必须有正确性、性能、回归、provenance 和回退证据。

