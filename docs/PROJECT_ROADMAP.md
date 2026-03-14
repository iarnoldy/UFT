# The Bridge: Papers 3 & 4 Roadmap

> Tracks progress from current state to paper submission.
> Updated: 2026-03-13. Last milestone gate: M1 (PASSED).

## Current State

**66 proof files. ~2,650+ declarations. Zero sorry.**
**Certified LieHoms: SU5C →ₗ⁅ℝ⁆ SO10 →ₗ⁅ℝ⁆ SO14 ←ₗ⁅ℝ⁆ SO4**

Papers 1 & 2 submitted. Papers 3 & 4 held pending anomaly traces + E₈ chain (ADR-004).

## Target: Composable Chain (Compact Signature)

```
SU5C →ₗ⁅ℝ⁆ SO10 →ₗ⁅ℝ⁆ SO14 ←ₗ⁅ℝ⁆ SO4
(gauge)                            (gravity, compact)
```

**Signature note:** The gravity embedding uses compact so(4), NOT Lorentzian so(1,3).
Physical gravity requires so(11,3) — documented in `SIGNATURE_ANALYSIS.md`.

---

## MILESTONE 1: SO(14) FOUNDATION — COMPLETE

**Goal:** SO(14) as a Lean type with two converging LieHoms.
**Status: COMPLETE** (2026-03-12 → 2026-03-13)

| Step | Task | Status | File |
|------|------|--------|------|
| 1.0 | Python bracket generator for SO(14) | DONE | `scripts/so14_bracket_gen.py` |
| 1.1 | SO14 type + LieRing + LieAlgebra ℝ instances | DONE | `src/lean_proofs/clifford/so14_grand.lean` |
| 1.2 | SO10 →ₗ⁅ℝ⁆ SO14 LieHom (gauge sector) | DONE (365s compile) | `src/lean_proofs/clifford/so10_so14_liehom.lean` |
| 1.3a | SO4 compact type + instances | DONE | `src/lean_proofs/clifford/so4_gravity.lean` |
| 1.3b | SO4 →ₗ⁅ℝ⁆ SO14 LieHom (gravity sector) | DONE | `src/lean_proofs/clifford/so4_so14_liehom.lean` |
| 1.4 | Full `lake build` clean | DONE (3,385 jobs, 0 errors) | `lakefile.lean` (updated) |

**Design change from plan:** Original plan called for Bivector (so(1,3)) → SO14.
Discovered so(1,3) and so(4) are non-isomorphic real Lie algebras — no LieHom exists.
Created new SO4 compact type instead. Documented in `SIGNATURE_ANALYSIS.md`.

**Build stats:** SO14 LieRing needed ~200M heartbeats, ~20GB RAM. SO10→SO14 map_lie' took 365s.

### Gate Check (PASSED 2026-03-13)
- [x] `lake build` compiles all 4 new files (3,385 jobs, 0 errors)
- [x] README updated with new arrow count
- [x] Convergence diagram: `SU5C →ₗ⁅ℝ⁆ SO10 →ₗ⁅ℝ⁆ SO14 ←ₗ⁅ℝ⁆ SO4`

---

## MILESTONE 2: ANOMALY TRACES — COMPLETE

**Goal:** Anomaly cancellation via representation theory, not arithmetic.
**Status: COMPLETE** (2026-03-13)

| Step | Task | Status | File |
|------|------|--------|------|
| 2.1 | Research minimal proof approach | DONE (Option C-Lite) | `memory/project_anomaly_approach.md` |
| 2.2 | Prove Tr(ABC) = -Tr(ACB) for antisymmetric A,B,C | DONE [MV] | `src/lean_proofs/clifford/anomaly_trace.lean` |
| 2.3 | Prove Tr(A{B,C}) = 0 corollary | DONE [MV] | `src/lean_proofs/clifford/anomaly_trace.lean` |
| 2.4 | SO(n) fundamental rep anomaly-free | DONE [MV] | `src/lean_proofs/clifford/anomaly_trace.lean` |
| 2.5 | Adjoint + spinor anomaly axioms | DONE [SP] | `src/lean_proofs/clifford/anomaly_trace.lean` |

**Approach used: Option C-Lite** — General antisymmetric trace identity.
Works for any so(n) in the fundamental representation. No dimension restriction.
Adjoint and Dirac spinor anomaly-freedom stated as [SP] axioms with honest gaps documented.

**Mathematical note:** The original proof sketch had a subtle error — CBA is an
anti-cyclic permutation of ABC, not cyclic. Correct argument: Tr(ABC) = -Tr(CBA)
by transpose+antisymmetry, then Tr(CBA) = Tr(ACB) by genuine cyclicity.

---

## MILESTONE 3: SO(16) EXTENSION

**Goal:** SO(16) type + SO(14) ↪ SO(16) LieHom.
**Status: COMPILING** (started 2026-03-13)

| Step | Task | Status | File |
|------|------|--------|------|
| 3.0 | Python generator for SO(16) (120 fields) | DONE | `scripts/so16_bracket_gen.py` |
| 3.1 | SO16 type + LieRing + LieAlgebra ℝ | COMPILING (400M hb) | `src/lean_proofs/clifford/so16_grand.lean` |
| 3.2 | SO14 ↪ SO16 LieHom | WRITTEN, AWAITING SO16 | `src/lean_proofs/clifford/so14_so16_liehom.lean` |

**Generator stats:** 120 generators, 3360 non-zero brackets, 28 terms per component.
Jacobi verified numerically (100 random triples). so(14) and so(10) subalgebra closures verified.

**Heartbeat budgets (extrapolated from SO14):**
- LieRing: 400M (SO14 needed 200M at 91 gens; SO16 has 120 gens)
- LieAlgebra: 256M
- SO14 → SO16 map_lie': 256M

**Kill condition:** If SO(16) LieRing fails and cannot be split → stop here.
SO(14) chain is still publishable without E₈.

---

## MILESTONE 4: E₈ CONSTRUCTION (MOONSHOT)

**Goal:** E₈ as a Lean type. SO(16) ↪ E₈ LieHom.
**Status: NOT STARTED** (depends on M3)

| Step | Task | Status |
|------|------|--------|
| 4.0 | Architecture decision (monolithic vs composite vs native_decide) | NOT STARTED |
| 4.1 | Python generator for E₈ bracket (30,628 pairs) | NOT STARTED |
| 4.2 | E₈ type + instances | NOT STARTED |
| 4.3 | SO16 ↪ E₈ LieHom | NOT STARTED |

**Kill condition:** If E₈ infeasible in Lean → document why. Paper 3 proceeds.

---

## MILESTONE 5: SU(9) FOR PAPER 4

**Goal:** SU(9) ↪ E₈ + three-generation decomposition.
**Status: NOT STARTED** (depends on M4)

| Step | Task | Status |
|------|------|--------|
| 5.1 | SU(9) type + instances (80 fields) | NOT STARTED |
| 5.2 | SU(9) ↪ E₈ LieHom | NOT STARTED |
| 5.3 | 248 = 80 + 84 + 84* as subspace decomposition | NOT STARTED |

---

## MILESTONE 6: PAPER REWRITE & SUBMISSION

**Goal:** Papers 3 & 4 rewritten, audited, proofread, submitted.
**Status: NOT STARTED** (depends on M1-M4 for Paper 3, M1-M5 for Paper 4)

| Step | Task | Status |
|------|------|--------|
| 6.1 | Paper 3 rewrite (claims match proofs) | NOT STARTED |
| 6.2 | Paper 3 audit + proofread | NOT STARTED |
| 6.3 | Paper 4 rewrite | NOT STARTED |
| 6.4 | Paper 4 audit + proofread | NOT STARTED |
| 6.5 | Submit | NOT STARTED |

---

## Timeline Overview

```
Week 1-4:   M1 — SO(14) + two LieHoms        [COMPLETE — day 2]
Week 4-6:   M2 — Anomaly traces               [COMPLETE — day 2]
Week 6-9:   M3 — SO(16) + LieHom
Week 9-16:  M4 — E₈ (moonshot)
Week 14-17: M5 — SU(9) + LieHom
Week 17-19: M6 — Paper rewrite + submission
```

## Kill Condition Summary

| Point | Condition | Action |
|-------|-----------|--------|
| After M1.1 | SO(14) LieRing fails at 200M heartbeats | Axiomatic fallback |
| After M3.1 | SO(16) LieRing fails | Stop at SO(14). Paper 4 deferred. |
| After M4.0 | E₈ architecture infeasible | Stop at SO(16). Paper 4 downscoped. |
| After M4.2 | E₈ LieRing/native_decide fails | Document wall. Paper 3 still submittable. |
| After M5 | SU(9) ↪ E₈ fails | Paper 4 deferred. |

At each kill condition, work done so far is still publishable — just in a different venue or with different claims.
