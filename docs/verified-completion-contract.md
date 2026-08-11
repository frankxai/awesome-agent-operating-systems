# Verified completion contract (OmO-absorbed)

Portable contract for Starlight Queen + any Class A worker. Origin: oh-my-openagent plan→verify culture, without installing OmO.

## Loop

```text
PLAN → EXECUTE → VERIFY (≠ maker) → ABSORB or HOLD
```

## PLAN must include

- Goal + non-goals
- Exact repo/worktree (4-fact git)
- Done-when evidence paths
- Kill criteria
- Class A–F (execution/ownership) or S (supporting substrate) of any new tool considered

## EXECUTE

- One writer per worktree
- Path ban on Windows host
- Git-first: status before, diff --stat after
- No `git add -A` on foreign dirty lanes

## VERIFY

- Different CLI/provider than maker when possible
- Mechanical checks preferred (tests, scripts, HTTP)
- Reject `false_verify_claim`

## ABSORB

- Skill patch, routing matrix row, or PR note
- Prefer pattern docs over new installs under BOUNDED disk

## HOLD

- Missing evidence, security advisory, disk CRITICAL/TIGHT for fanout, human gate

## CLI

```bash
python scripts/absorb_recommend.py --need <keyword>
```
