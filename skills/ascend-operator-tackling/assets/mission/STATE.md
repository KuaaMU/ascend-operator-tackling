# State

Updated: {{DATE}}
Operator: {{OPERATOR}}
Repo: {{REPO}}

## Current Checkpoint

`CP0` - initialize and verify the live authority. No final claim yet.

## Status

| Item | Status | Owner | Note |
|---|---|---|---|
| Goal/acceptance contract | in-progress | orchestrator | Confirm from task doc |
| Environment discovery | not-started | driver | Run discover_environment.py |
| Authority source/binary | not-started | driver | Record commit and hashes |
| Correctness baseline | not-started | driver | Reference oracle |
| Performance baseline | not-started | driver | Official metric only |
| Independent review | pending | reviewer | No verdict |

## Active Decisions

1. Correctness and provenance precede performance promotion.
2. Every candidate changes one primary variable and has a kill criterion.
3. Target-environment evidence is required for PASS/GO.

## Blocked

| Problem | Attempts | Evidence | Next |
|---|---:|---|---|
| none | 0 | - | - |

## Workspace / Device Ledger

| Type | Path/Device | Owner | Purpose | Status | Cleanup |
|---|---|---|---|---|---|
| repo | {{REPO}} | unassigned | target checkout | unverified | record hashes |

## Session Log

```text
{{DATE}} | agent/role | bootstrap | started | CP0
```

