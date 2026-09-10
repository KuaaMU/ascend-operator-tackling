# ascend-operator-tackling

Goal-driven, evidence-first workflow for long-horizon Ascend/CANN operator development and tuning.

The skill is designed for:

- environment-aware use of official CANN/Ascend tooling;
- correctness gates before performance promotion;
- falsifiable, single-variable optimization candidates;
- critical-path attribution and resource-driven generalization;
- compact-safe mission state, handoffs, and multi-agent isolation;
- autonomous correction when experiments fail or previous assumptions become stale.

It does not bind to a specific CANN release, chip model, repository, or operator workload.

## Layout

```text
skills/ascend-operator-tackling/
├── SKILL.md
├── agents/
├── assets/
├── references/
└── scripts/
```

## Install

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo KuaaMU/ascend-operator-tackling \
  --path skills/ascend-operator-tackling
```

## Initialize a mission

```bash
python skills/ascend-operator-tackling/scripts/init_mission.py \
  --mission ./mission \
  --goal "Meet the operator's correctness and performance targets" \
  --acceptance "All target-environment acceptance tests pass" \
  --operator "<operator>" \
  --repo "<repo>" \
  --task-doc "<task-doc>"
```

Then run:

```bash
python skills/ascend-operator-tackling/scripts/discover_environment.py
python skills/ascend-operator-tackling/scripts/mission_lint.py ./mission
```

## License

MIT

