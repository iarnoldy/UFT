# Research Council Charter: E₈ Geometric Mixing Angles

**Investigation ID:** e8-mixing-angles
**Date:** 2026-03-17
**Initiated by:** Ian M. Arnoldy

## Question

Is there a geometric mechanism for fermion mixing angles (CKM/PMNS) that lives
in the E₈ root geometry itself — not in flavon symmetry breaking — and if so,
what mathematical structure produces it?

## Prior Art (Test Run Findings, e8-geometric-flavor)

This investigation inherits established findings from the test run council:

| Finding | Confidence | Source |
|---------|-----------|--------|
| No mechanism derives 3 generations from E₈ without Z₃ input | 91% | R1-R5 |
| Z₃ eigenspace projection is scalar × identity (zero mixing info) | 95% | R4 KC-R3 |
| Generation labels have CP³ freedom (6 params > CKM's 4) | 95% | R4 KC-R4 |
| No discrete flavor model predicts all 8 mixing params at zero free parameters | 97% | R2-R4 |
| Singh's δ²=3/8 is Vieta formula at N=1/8, trace split 1:2:3 is free | 95% | R3-R4 |
| E₈→E₆×SU(3) resolves types/copies gap (tensor product) | 90% | R4 |
| Wilson PMNS angles match experiment at 0.2-0.5σ but feed in Cabibbo angle | 90% | M8.3b |
| The algebra gives the stage, not the script | — | R1 original vision |

**The test run's negative verdict:** E₈ accommodates 3 generations but does
not derive them. This real run asks the SHARPER question: even accepting 3
generations as given, can E₈ geometry determine the MIXING between them?

## What Success Looks Like

A mathematical construction where E₈ root geometry (Weyl group, root system
inner products, lattice automorphisms, or analogous invariants) constrains
the CKM and/or PMNS mixing matrices — producing specific angles as geometric
invariants, NOT as parameters of a flavon potential.

Partial success: identifying the precise mathematical obstruction to such a
construction (i.e., proving it CANNOT work and specifying exactly why).

## Pre-Registered Kill Conditions

| ID | Condition | Round | Severity |
|----|-----------|-------|----------|
| KC-M1 | No mathematical structure in E₈ connects root geometry to unitary rotation matrices | 2 | FATAL |
| KC-M2 | All candidate constructions reduce to flavon VEV alignment (recovered underdetermination) | 3 | FATAL |
| KC-M3 | Wilson's specific angle derivation is irreproducible or requires hidden inputs beyond Cabibbo | 4 | SERIOUS |
| KC-M4 | The only paths to mixing angles from E₈ are already covered by test run (Z₃ eigenspace, D₄ triality, J₃(O) eigenvalues) | 5 | FATAL |

FATAL = investigation stops with negative result. SERIOUS = requires explicit
justification to continue.

## Agent Assignments (7 Rounds)

| Round | Agent | Purpose |
|-------|-------|---------|
| 1. VISION | Heptapod B Architect | Characterize necessary structure of geometric mixing mechanism |
| 2. ARCHAEOLOGY | Polymathic Researcher | 2-3 TARGETED questions on mixing from geometry |
| 3. COMPUTATION | Clifford Unification Engineer | Kill-condition tests: root geometry → rotation matrices |
| 4. DEVIL'S ADVOCATE | Heptapod B Architect | Strongest case FOR geometric mixing surviving |
| 5. RIGOR | Dollard Theorist | Mathematical assessment informed by computation + devil's advocate |
| 6. SYNTHESIS | Heptapod B Architect | Final verdict, project implications |

## Accumulated Context Files

All test run artifacts in `research/council/e8-geometric-flavor/00-05`.

Additional:
- `src/experiments/results/wilson_pmns_verification.json` — M8.3b
- `src/experiments/z3_eigenspace_projections.py` — Z₃ triviality proof
- `src/experiments/singh_delta_verification.py` — δ²=3N verification
- `src/experiments/triality_sm_branching.py` — Branching rules
- `research/heptapod-b-yukawa-vision.md` — Prior vision
- `research/wilson-three-generation-comparison.md` — Wilson comparison
