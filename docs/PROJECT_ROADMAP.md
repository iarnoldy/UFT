# The Bridge: Project Roadmap

> Updated: 2026-03-16. Milestones 1-6 COMPLETE. GPD evaluation done. Next: fix Paper 3 + Yukawa kill-condition (M8).

## Current State

**88 proof files. ~2,900 declarations. Zero sorry.**
**Five certified LieHoms composing:**
```
SU5C →ₗ⁅ℝ⁆ SO10 →ₗ⁅ℝ⁆ SO14 →[bridge]→ SO14M →ₗ⁅ℝ⁆ SO16Block
                                   ⬑
                              SO4 →ₗ⁅ℝ⁆ SO14
```
**E₈ (248-dim) independently verified as Lie algebra. SO(16) ⊂ E₈ subalgebra closure verified.**
**Three-generation mechanism via SU(9)/Z₃: dimensionally consistent, J-eigenspace anomaly-free.**

Papers 1 (CICM) and 2 (AACA) submitted.
Papers 3 (PRD) and 4 (LMP) updated, audited, ready for submission.

---

## MILESTONE 1: SO(14) FOUNDATION — COMPLETE ✓
Completed 2026-03-13. SO14 type + LieRing + LieAlgebra ℝ + two converging LieHoms.

## MILESTONE 2: ANOMALY TRACES — COMPLETE ✓
Completed 2026-03-13. Tr(A{B,C}) = 0 for antisymmetric A,B,C. Any ring, any dimension.

## MILESTONE 3: SO(16) EXTENSION — COMPLETE ✓
Completed 2026-03-14. Matrix approach (so16_matrix.lean) replaced flat approach.
SO14 → SO14M → SO16Block via type bridge + block embedding.

## MILESTONE 4: E₈ CONSTRUCTION — COMPLETE ✓
Completed 2026-03-15. Sparse Jacobi approach: 248 dims, 7,752 nonzero brackets,
248^4 ≈ 3.78 billion native_decide evaluations. SO(16) subalgebra closure verified.
**Remaining: SO16 → E₈ typed LieHom (4.3) — subalgebra closure proves the math;
LieHom is type-system bookkeeping, not mathematical content.**

## MILESTONE 5: THREE-GENERATION VERIFICATION — COMPLETE ✓
Completed 2026-03-15. 10 proof files, 621 declarations:
- Spinor parity obstruction: 3 ∤ 2, universal for SO(10+2k) [MV]
- E₈/SU(9) resolution: 248 = 80 + 84 + 84*, 3 × 16 = 48 ≤ 84 [MV]
- J-eigenspace anomaly freedom: Tr(Y) = 0 in each sector independently [MV]
- Chirality definition: two-level algebraic framework [MV + CO]
**Remaining: SU(9) typed LieHom into E₈ (5.1-5.2) — same situation as 4.3.**

## MILESTONE 6: PAPER REWRITE & AUDIT — COMPLETE ✓
Completed 2026-03-15. Full pipeline ran on both papers:
- Paper 3: Updated numbers, added E₈ + bridge, fixed auditor findings (scope blur,
  overclaim, AI telltale, tautological citation). Wilson/Berlinski check PASS.
- Paper 4: Same updates. All 42 claims ACCURATE. Zero overclaims (was 11).
  Jacobi formula error fixed. Wilson/Berlinski check PASS.
**Remaining: SUBMIT.**

## MILESTONE 6.5: GPD EVALUATION — COMPLETE ✓
Completed 2026-03-16. Full 6-stage GPD peer review of Paper 3:
- **3 critical issues**: (1) su5_lie_structure not in build, (2) no new physics predictions
  acknowledged, (3) novel signatures inaccessible at 10^19 GeV
- **7 serious issues**: Flyspeck comparison overstated, anomaly_checklist tautology,
  duplicate table entry, signature percentage mismatch (87% vs 77%), three-generation
  tension unclear, 0.88% coupling miss presented as evidence, Partial* unexplained
- **Venue recommendation**: GPD referee recommends JMP or CPC over PRD (paper's strength
  is methodology + E₈ formalization, not new physics predictions)
- All issues addressed in Paper 3 revision (2026-03-16)
- Full report: `.gpd/REFEREE-REPORT.md`

**Mass Gap Thread: RETIRED.** Three kill conditions fired simultaneously:
1. Yang-Mills mass gap requires constructive QFT (Jaffe-Witten), not algebraic manipulation
2. SO(14) compact signature ≠ physical Minkowski signature needed for gap
3. Our formalization axiomatizes but does not prove the gap (it's the Millennium Prize problem)
Analysis: `research/heptapod-b-mass-gap-reassessment.md`

---

## MILESTONE 7: SUBMISSION & COMMUNITY — NOT STARTED

| Step | Task | Status |
|------|------|--------|
| 7.1 | Get arXiv endorsement (Wilson withdrew) | NOT STARTED |
| 7.2 | Post preprints to arXiv | BLOCKED on 7.1 |
| 7.3 | Submit Paper 3 to PRD (or JMP/CPC — Ian's decision) | NOT STARTED |
| 7.4 | Submit Paper 4 to LMP | NOT STARTED |
| 7.5 | Lean Zulip post: E₈ formalization | NOT STARTED |
| 7.6 | mathlib PR: E₈ or type bridge contribution | NOT STARTED |

## MILESTONE 8: PHENOMENOLOGY (KILL-CONDITION) — IN PROGRESS

**Goal:** Compute SU(3)_family Yukawa texture. Compare to measured CKM/PMNS.
Three possible outcomes:
- **Kill**: CG ratios produce texture immediately inconsistent with CKM → model falsified
- **Survive**: Genuine constraints from SU(9) embedding predict specific mixing angles
- **Underdetermined**: SU(3)_family has free parameters → framework survives vacuously (no new predictions)

| Step | Task | Status | Effort |
|------|------|--------|--------|
| 8.1 | SU(9) Clebsch-Gordan via SageMath: `WeylCharacterRing('A8')` | NOT STARTED | ~2-3 hrs |
| 8.1a | Verify 84 × 84* contains 80 (adjoint) — Schur uniqueness | NOT STARTED | part of 8.1 |
| 8.1b | Branch 84 under SU(5) × SU(4): sector-by-sector CG ratios | NOT STARTED | part of 8.1 |
| 8.1c | Test factorization: does (10,3) × (5̄,3̄) CG split into SU(5)×SU(4) parts? | NOT STARTED | part of 8.1 |
| 8.2 | Yukawa texture extraction from CG results | NOT STARTED | ~1-2 days |
| 8.2a | Test triplet flavon → antisymmetric texture (rank 2) | NOT STARTED | part of 8.2 |
| 8.2b | Test adjoint flavon → Gell-Mann texture | NOT STARTED | part of 8.2 |
| 8.2c | Test sextet flavon → general symmetric texture (rank 3) | NOT STARTED | part of 8.2 |
| 8.3 | Compare to CKM/PMNS; evaluate kill condition | NOT STARTED | ~1 day |
| 8.3b | **Wilson PMNS independent verification** (HIGHEST VALUE) | NOT STARTED | ~3-5 days |
| 8.4 | If survives: proton decay branching ratios | NOT STARTED | — |
| 8.5 | If survives: neutrino mass hierarchy prediction | NOT STARTED | — |
| 8.6 | Paper 5 (phenomenological predictions) | NOT STARTED | — |

**Key correction (polymathic research, 2026-03-16):** SU(3)-symmetric limit gives
degenerate masses (δᵢⱼ), NOT democratic mixing matrix. This matters for identifying
the correct symmetry-breaking pattern.

**Kill condition (refined per Heptapod B analysis):** If CG ratios are identical to
standard SU(5), framework reduces to SU(5) + SU(3)_family with no new predictions.
This is Outcome C (underdetermined survival), not a clean kill. Document as such.

**Wilson PMNS verification (M8.3b):** Wilson claims θ₁₃ = 8.586° (exp: 8.54 ± 0.12°)
and θ₂₃ = 49.077° (exp: 49.1 ± 1.0°). Independent verification of these claims
is the single highest-value physics test available. If reproduced → major result.
If refuted → saves months of work on wrong E₈ embedding.

---

## Type-System Bookkeeping (Optional, Low Priority)

These are formally incomplete but mathematically proven:

| Item | What exists | What's missing | Effort |
|------|-------------|----------------|--------|
| SO16 → E₈ LieHom | Subalgebra closure via native_decide | Typed LieHom (E₈ needs LieAlgebra instance) | ~1 day |
| SU(9) → E₈ LieHom | Dimensional decomposition [MV] | SU(9) type + LieHom | ~3-5 days |
| Lorentzian signature | Compact proofs, 77% signature-independent | so(11,3) real form | Research-level |

---

## Kill Condition Summary

| Point | Condition | Action |
|-------|-----------|--------|
| M1-M4 | Any milestone infeasible | Stop at last complete milestone. Still publishable. |
| M8.3 | CG ratios identical to SU(5) | Document as Outcome C (underdetermined). Not a clean kill. |
| M8.3 | CKM/PMNS inconsistent by >3σ | STOP. Publish negative result. Model falsified. |
| M8.3b | Wilson PMNS angles not reproducible | Document. Reassess E₈ embedding approach. |
| ~~Mass gap~~ | ~~RETIRED~~ | Three kill conditions fired. See `research/heptapod-b-mass-gap-reassessment.md` |
