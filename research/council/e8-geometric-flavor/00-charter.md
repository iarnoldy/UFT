# Research Council Charter: E₈ Geometric Flavor Mechanism

**Investigation ID:** e8-geometric-flavor
**Date:** 2026-03-17
**Initiated by:** Ian M. Arnoldy

## Question

Is there a geometric mechanism for fermion mixing angles (CKM/PMNS) that lives
in the E₈ root geometry itself — not in flavon symmetry breaking — and if so,
what mathematical structure produces it?

## Why Standard Approaches Failed

1. **SU(3)_family Yukawa (M8.1-M8.2, 2026-03-16):** The SU(9) Yukawa coupling
   factorizes cleanly into SU(5) x SU(4). The SU(4) ~ SU(3)_family part
   contributes delta_ij in the symmetric limit (degenerate masses, zero mixing).
   Any realistic texture requires a flavon VEV with free parameters that E₈
   doesn't constrain. Outcome C: underdetermined survival.

2. **Wilson's geometric approach (arXiv:2407.18279):** Claims PMNS angles from
   E₈ geometry with striking matches (theta_13=8.586 vs exp 8.54+/-0.12,
   theta_23=49.077 vs exp 49.1+/-1.0). But feeds in the measured Cabibbo angle
   and uses an ad hoc splitting ratio (cos 10 / cos 50). Wilson himself calls
   it "purely conjectural" with "no theoretical justification."

3. **Algebraic scaffold is solid [MV]:** E₈ (248-dim) verified as Lie algebra.
   SU(9) subset E₈ verified. 248 = 80 + 84 + 84* decomposition verified.
   Z₃ eigenspace anomaly freedom verified. 88 proof files, ~2900 declarations,
   zero sorry gaps. The math works — the physics question is open.

## What Success Looks Like

A mathematical framework where the Z₃ automorphism of E₈ (or its eigenspace
geometry) constrains rotation angles in a way that produces specific mixing
matrices — WITHOUT feeding in measured values. This would be a PREDICTION,
not a fit.

Partial success: identifying the precise mathematical structure that WOULD
need to be computed, even if we can't compute it yet. (Knowing what to
calculate is half the battle.)

## Pre-Registered Kill Conditions

| ID | Condition | Round | Severity |
|----|-----------|-------|----------|
| KC-R1 | No coherent mathematical structure connects discrete automorphisms to continuous rotation angles | 1 | FATAL |
| KC-R2 | All prior work on discrete symmetry -> mixing angles requires free parameters | 2 | SERIOUS |
| KC-R3 | Z₃ eigenspace projections produce trivial rotation matrices (identity or maximally mixed) | 4 | FATAL |
| KC-R4 | Angles depend on arbitrary basis choices, not geometric invariants | 4 | FATAL |

FATAL = investigation stops. SERIOUS = requires explicit justification to continue.

## Agent Assignments

| Round | Agent | Purpose |
|-------|-------|---------|
| 1. VISION | Heptapod B Architect | Characterize necessary structure of geometric flavor mechanism |
| 2. ARCHAEOLOGY | Polymathic Researcher | Find prior work on discrete symmetries -> mixing angles |
| 3. RIGOR | Dollard Theorist | Evaluate mathematical viability of leads |
| 4. COMPUTATION | Direct (SageMath) | Test Z₃ eigenspace projections numerically |
| 5. SYNTHESIS | Heptapod B Architect | Revised vision with all evidence |

## Accumulated Context Files

- `src/experiments/results/su9_cg_coefficients.json` — M8.1 results
- `src/experiments/results/yukawa_texture_analysis.json` — M8.2 results
- `src/experiments/results/wilson_pmns_verification.json` — M8.3b results
- `research/heptapod-b-yukawa-vision.md` — Prior Heptapod B analysis
- `research/yukawa-kill-condition-research.md` — Prior polymathic research
- `research/wilson-three-generation-comparison.md` — Wilson comparison
