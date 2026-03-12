# F3.0 Signature Audit — Detailed Triage of 10 Sensitive Files

**Date**: 2026-03-12
**Auditor**: clifford-unification-engineer agent
**Purpose**: Determine which of 10 signature-sensitive files need reproving for Lorentzian signature

## Critical Finding

**No file needs FULL reproving (Category A = 0).** The load-bearing mathematical content
(Jacobi identities, structure constants, embeddings, unification) is polynomial algebra
that holds in ALL signatures. Only the Clifford-level geometric products and Hodge duals
are signature-dependent.

## Classification

### Category B: Reinterpretation Only (4 files — NO WORK NEEDED)

| File | Lines | Why No Work Needed |
|------|-------|--------------------|
| `unification_gravity.lean` | 281 | Pure index arithmetic. `[so(1,3), so(10)] = 0` holds in any signature. |
| `hilbert_space.lean` | 330 | All theorems are trivial arithmetic (`norm_num`, `rfl`). Wightman axioms are just stated, not proved. |
| `mass_gap.lean` | 397 | Tautologies and arithmetic. Physical interpretation is Lorentzian but Lean content is signature-free. |
| `exterior_cube_chirality.lean` | 577 | Root systems and representation dimensions. File header states signature independence. |

### Category C: Partial — Some Theorems Depend on Signature (6 files)

| File | Lines | Sig-Dep | Sig-Indep | Notes |
|------|-------|---------|-----------|-------|
| `cl31_maxwell.lean` | 840 | ~50 | ~20 | `mul` (256 terms) must be regenerated for new signature |
| `gauge_gravity.lean` | 1,068 | ~25 | **~55** | **Lie algebra core (Jacobi, structure constants) is safe** |
| `dirac.lean` | 512 | ~15 | ~30 | SU(2), chirality, reversion survive. Even `mul` needs regen. |
| `lie_bridge.lean` | 254 | ~4 | ~11 | Auto-reproves after dirac rebuild |
| `e8_chirality_boundary.lean` | 501 | ~5 | ~25 | Already does the correct signature comparison! |
| `massive_chirality_definition.lean` | 940 | ~6 | ~61 | Already does the correct signature analysis |

## Key Insight

**The Lie algebra proofs are the load-bearing content, and they are ALL signature-independent.**

- `gauge_gravity.lean`: `Bivector.comm` computes the abstract so(n) bracket. The Jacobi identity
  is proved by `ext <;> simp [comm, add, zero] <;> ring` — pure polynomial algebra.
  Works identically for so(1,3), so(4), so(2,2), or any so(p,q) with p+q=4.

- `unification_gravity.lean`: The commutator `[so(1,3), so(10)] = 0` is pure index arithmetic
  (indices {1,2,3,4} vs {5,...,14} are disjoint).

- Structure constants, Bianchi, gauge covariance, LieRing instances: all polynomial identities.

The Clifford algebra proofs (`cl31_maxwell.mul`, `dirac.mul`) provide the physical DERIVATION
of the Lie algebra from the geometric product, but the Lie algebra results stand on their own.

## Effort Estimate (if Lorentzian Clifford reproofs are ever needed)

| Task | Hours |
|------|-------|
| Regenerate `STA.mul` for new signature via Python | 2 |
| Reprove cl31_maxwell signature theorems | 4-6 |
| Regenerate `Spinor.mul` for new even subalgebra | 2 |
| Reprove dirac.lean signature-dependent theorems | 4-6 |
| Reprove lie_bridge.lean (auto from dirac rebuild) | 2 |
| Redefine Hodge, inner product in gauge_gravity.lean | 4-6 |
| Reprove Riemann solutions for new inner product | 4-6 |
| **Total** | **~22-30 hours** |

## Recommended F3 Scope (Revised)

**Original plan**: Parametrize `Bivector` by signature, reprove 10 files. (Weeks of work)

**Revised plan**: The Lie algebra level is already correct. F3 reduces to:

1. **Add reinterpretation notes** to Category B files (trivial, 1 hour)
2. **Document** that gauge_gravity.lean's Lie algebra core is signature-independent (1 hour)
3. **Defer** Clifford-level reproofs (cl31_maxwell, dirac) unless specifically needed for physics
4. **Consider** parametric `Bivector(p,q)` as a future enhancement, not a blocker

**Net effect**: F3 is ~90% done by this audit. The remaining 10% is documentation, not reproving.

## Theorem Census

- Total theorems across 10 files: ~377
- Already correct in any signature: **~277 (73%)**
- Would need reproof for Lorentzian: **~100 (27%)**
- Concentrated in: cl31_maxwell (~50) and dirac (~15) geometric products
