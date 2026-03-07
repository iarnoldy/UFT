---
name: experiment-workflow
description: Pre-register, execute, and record experiments with falsification criteria
triggers:
  - run experiment
  - pre-register experiment
  - execute experiment
---

# Experiment Workflow

## Pre-Registration

Before executing any experiment:

1. Add entry to `docs/experiments/EXPERIMENT_REGISTRY.md` with:
   - Hypothesis (falsifiable statement)
   - Method (specific steps)
   - Falsification criteria (what disproves the hypothesis)
   - Expected outcome (honest prediction)
   - Dependencies (blocking experiments)
   - Downstream impact (what depends on this result)

2. Commit the pre-registration before executing.

## Execution

1. Write experiment runner in `src/experiments/`
2. Call `metadata.capture()` at start of run
3. Execute the experiment
4. Record results via `metadata.save()`

## Recording Results

Results go to `src/experiments/results/` following `results_schema.json`:

```json
{
  "experiment_id": "experiment-0-polyphase",
  "metadata": { "timestamp": "...", "git_commit": "..." },
  "results": {
    "verdict": "VERIFIED | DISPROVED | INCONCLUSIVE | ERROR",
    "evidence": "path to proof or log",
    "details": {}
  }
}
```

## Post-Execution

1. Update `analysis/CLAIM_TRIAGE.md` with new verdict
2. Update `analysis/VERIFICATION_RESULTS.md` if proof status changed
3. Note downstream impact in commit message
