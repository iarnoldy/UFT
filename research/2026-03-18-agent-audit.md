# Agent Audit — 2026-03-18

## Summary

QA'd 5 agents referenced in QPE workflow. All were stale — pointing to wrong repo paths, wrong project scope, or wrong model. Fixed all 5.

## Findings

### 1. experiment-designer — WAS STALE, FIXED
**Before**: Scoped to N-Phase signal processing. Referenced paths that don't exist in this repo:
- `src/fortescue/tests/`, `src/versor_algebra/tests/`, `src/neural_network/tests/` — none exist here
- `docs/MATHEMATICAL_SPECIFICATION.md`, `docs/ARCHITECTURE.md` — wrong docs
- No awareness of QPE, `EXPERIMENT_REGISTRY.md`, or Lean experiments

**After**: Updated with this repo's actual paths (`src/experiments/`, `src/experiments/qpe/`, `docs/experiments/EXPERIMENT_REGISTRY.md`). Added confound isolation as a design principle (learned from QPE Experiment A). Added "save all findings to disk" mandate. Model: opus → sonnet.

### 2. experiment-executor — WAS STALE, FIXED
**Before**: Scoped entirely to 4Q-RLHF validation. Referenced "Experiment 0 (Verify Baseline Mode Collapse)" — irrelevant. Output template was 4Q-RLHF specific.

**After**: Generalized for this repo. Updated paths (`src/experiments/results/`, `docs/experiments/`). Removed 4Q-RLHF specifics. Added "save all results to disk" mandate. Added "never overwrite existing results" rule. Model: opus → sonnet.

### 3. n-phase-architect — WAS STALE, FIXED
**Before**: Referenced files from N-Phase patent-ready repo: `src/fortescue/torch_decomposer.py`, `src/neural_network/sequence_network.py`, etc. None exist in this repo.

**After**: Updated to reference this repo's actual PyTorch code: `src/experiments/qpe/quaternary_encoding.py` and friends. N-Phase repo files listed as "upstream reference only." Added QPE architecture documentation. Model: opus → sonnet.

### 4. autograd-specialist — WAS STALE, FIXED
**Before**: Same as n-phase-architect — all file references pointed to N-Phase repo, not this one.

**After**: Updated for this repo's code. Documented QPE-specific gradient concerns (cosh overflow, log_scale clamp discontinuity). N-Phase repo files listed as reference only. Model: opus → sonnet.

### 5. droid-code-engineer — WRONG MODEL + WRONG WORKFLOW, FIXED
**Before**: Used `model: haiku` (too weak for physics/math codebase). Mandated PR for every change (overkill for research repo). Had Factory.ai references.

**After**: Model upgraded to sonnet. Removed PR mandate — this is a research repo. Removed Factory.ai references. Added project context (Lean + Python + LaTeX structure). Added "save all work to disk" mandate. Simplified to match research workflow.

## Key Pattern

All agents were written for the N-Phase patent-ready repo and/or the 4Q-RLHF project, then used in this repo without updating paths. The fix: make each agent reference THIS repo's actual structure while noting upstream repos as read-only reference.

## Changes Applied

All 5 files at `~/.claude/agents/`:
- `experiment-designer.md` — rewritten
- `experiment-executor.md` — rewritten
- `n-phase-architect.md` — rewritten
- `autograd-specialist.md` — rewritten
- `droid-code-engineer.md` — rewritten

All agents now have "save all findings to disk" as a critical mandate.
