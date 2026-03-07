# Contributing

## Workflow

1. **Pre-register**: Add hypothesis + falsification criteria to `experiments/EXPERIMENT_REGISTRY.md`
2. **Implement**: Write Lean proof or Python experiment
3. **Execute**: Run with reproducibility metadata
4. **Record**: Write results (append-only, protected by hook)
5. **Update triage**: Modify `analysis/CLAIM_TRIAGE.md` with new evidence

## Adding a Lean Proof

1. Place in appropriate subdirectory under `src/lean_proofs/`
2. Import dependencies explicitly
3. Use `sorry` only for acknowledged gaps -- never silently
4. Update `analysis/CLAIM_TRIAGE.md` when a claim moves to VERIFIED or DISPROVED

## Adding an Experiment

1. Pre-register in `docs/experiments/EXPERIMENT_REGISTRY.md`
2. Write runner in `src/experiments/`
3. Include `metadata.py` for reproducibility
4. Results go to `src/experiments/results/` (append-only)

## Commit Messages

Follow conventional commits: `feat:`, `fix:`, `docs:`, `proof:`, `experiment:`

## Downstream: N-Phase Signal Processing System

This project feeds mathematical verification results to the N-Phase system.

### Sync Protocol

When a claim's status changes in `analysis/CLAIM_TRIAGE.md`:

| Status | N-Phase Action |
|--------|---------------|
| VERIFIED | Safe to depend on -- no action needed |
| DISPROVED | Must remove dependency on this claim |
| UNRESOLVED | Track but do not depend on |
| UNFALSIFIABLE | Do not depend on |

### Change Categories

- **VERIFIED**: Lean proof accepted, claim is mathematically sound
- **DISPROVED**: Lean proof shows contradiction or counterexample
- **UNRESOLVED**: Not yet verified, insufficient evidence
- **UNFALSIFIABLE**: Cannot be tested with formal methods (physics claims)
- **EXTRAORDINARY**: Requires extraordinary evidence before acceptance

### Notification

When updating CLAIM_TRIAGE.md, note the downstream impact in the commit message:
```
proof: disprove versor form equivalence

DOWNSTREAM: N-Phase must not assume h(XB+RG) = (XB+RG)
```
