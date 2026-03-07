# src/experiments/ -- Sharp Edges

## Purpose
Python experiment runners that execute pre-registered experiments.

## Rules
1. Every script here must correspond to a pre-registered experiment in
   `docs/experiments/EXPERIMENT_REGISTRY.md`
2. Results go to `results/` (append-only, protected by hook)
3. Every run must call `metadata.capture()` for reproducibility
4. No experiment modifies source data or Lean proofs

## Known Issues
- No Lean 4 Python bindings yet -- experiments call `lake env lean` via subprocess
- Results schema is minimal; extend as needed
