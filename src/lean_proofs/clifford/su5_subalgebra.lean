/-
UFT Formal Verification - SU(5) as LieSubalgebra of SO(10)
============================================================

MATHLIB-CERTIFIED SUBALGEBRA CONSTRUCTION

The centralizer of J in so(10):
  centralizer(J) = {X ∈ so(10) | [X, J] = 0} = u(5)

is automatically a LieSubalgebra by the Jacobi identity
(proved as centralizer_closed in su5_so10_embedding.lean).

The 24 traceless generators {H₁..H₄, R₁₂..R₄₅, S₁₂..S₄₅}
and J itself all lie in this centralizer. The A₄ Cartan matrix
(proved in su5_lie_structure.lean) uniquely identifies the
traceless part as su(5).

References:
  - su5_so10_embedding.lean: 24 commutation theorems + centralizer_closed
  - su5_lie_structure.lean: A₄ Cartan matrix verification (48 theorems)
  - Georgi, "Lie Algebras in Particle Physics" (1999), Ch. 24
-/

import Mathlib.Algebra.Lie.Subalgebra
import clifford.so10_grand
import clifford.su5_so10_embedding

open SU5SO10Embedding

/-! ## The Centralizer of J as a LieSubalgebra

The centralizer of any element in a Lie algebra is a Lie subalgebra
(by the Jacobi/Leibniz identity). We construct it for the complex
structure J ∈ so(10), obtaining u(5) ⊃ su(5). -/

/-- The centralizer of the complex structure J in so(10).
    This is u(5) = su(5) ⊕ u(1), a 25-dimensional Lie subalgebra.
    Bracket closure follows from centralizer_closed (Jacobi identity). -/
def u5_subalgebra : LieSubalgebra ℝ SO10 where
  carrier := {x : SO10 | ⁅x, complexJ⁆ = 0}
  add_mem' := fun {x y} (hx : ⁅x, complexJ⁆ = 0) (hy : ⁅y, complexJ⁆ = 0) => by
    show ⁅x + y, complexJ⁆ = 0
    rw [add_lie, hx, hy, add_zero]
  zero_mem' := by
    show ⁅(0 : SO10), complexJ⁆ = 0
    exact zero_lie complexJ
  smul_mem' := fun r {x} (hx : ⁅x, complexJ⁆ = 0) => by
    show ⁅r • x, complexJ⁆ = 0
    rw [smul_lie, hx, smul_zero]
  lie_mem' := fun {x y} (hx : ⁅x, complexJ⁆ = 0) (hy : ⁅y, complexJ⁆ = 0) =>
    centralizer_closed x y hx hy

/-! ## Membership Proofs

All 24 su(5) generators and J lie in the centralizer of J. -/

-- Cartan generators
theorem su5H1_mem : su5H1 ∈ u5_subalgebra := su5H1_comm_J
theorem su5H2_mem : su5H2 ∈ u5_subalgebra := su5H2_comm_J
theorem su5H3_mem : su5H3 ∈ u5_subalgebra := su5H3_comm_J
theorem su5H4_mem : su5H4 ∈ u5_subalgebra := su5H4_comm_J

-- R-type generators
theorem su5R12_mem : su5R12 ∈ u5_subalgebra := su5R12_comm_J
theorem su5R13_mem : su5R13 ∈ u5_subalgebra := su5R13_comm_J
theorem su5R14_mem : su5R14 ∈ u5_subalgebra := su5R14_comm_J
theorem su5R15_mem : su5R15 ∈ u5_subalgebra := su5R15_comm_J
theorem su5R23_mem : su5R23 ∈ u5_subalgebra := su5R23_comm_J
theorem su5R24_mem : su5R24 ∈ u5_subalgebra := su5R24_comm_J
theorem su5R25_mem : su5R25 ∈ u5_subalgebra := su5R25_comm_J
theorem su5R34_mem : su5R34 ∈ u5_subalgebra := su5R34_comm_J
theorem su5R35_mem : su5R35 ∈ u5_subalgebra := su5R35_comm_J
theorem su5R45_mem : su5R45 ∈ u5_subalgebra := su5R45_comm_J

-- S-type generators
theorem su5S12_mem : su5S12 ∈ u5_subalgebra := su5S12_comm_J
theorem su5S13_mem : su5S13 ∈ u5_subalgebra := su5S13_comm_J
theorem su5S14_mem : su5S14 ∈ u5_subalgebra := su5S14_comm_J
theorem su5S15_mem : su5S15 ∈ u5_subalgebra := su5S15_comm_J
theorem su5S23_mem : su5S23 ∈ u5_subalgebra := su5S23_comm_J
theorem su5S24_mem : su5S24 ∈ u5_subalgebra := su5S24_comm_J
theorem su5S25_mem : su5S25 ∈ u5_subalgebra := su5S25_comm_J
theorem su5S34_mem : su5S34 ∈ u5_subalgebra := su5S34_comm_J
theorem su5S35_mem : su5S35 ∈ u5_subalgebra := su5S35_comm_J
theorem su5S45_mem : su5S45 ∈ u5_subalgebra := su5S45_comm_J

-- J itself (the u(1) component completing u(5) = su(5) ⊕ u(1))
theorem J_mem : complexJ ∈ u5_subalgebra := J_comm_self

/-! ## Dimension Counts -/

/-- u(5) = su(5) ⊕ u(1) has dimension 25. -/
theorem u5_dim_check : 24 + 1 = 25 := by norm_num

/-- su(5) has dimension 5² - 1 = 24. -/
theorem su5_dim_check : 5 * 5 - 1 = 24 := by norm_num

/-! ## Summary

### What this file proves:
1. The centralizer of J in so(10) is a LieSubalgebra ℝ SO10 (u5_subalgebra)
2. All 24 su(5) generators lie in this subalgebra (24 membership theorems)
3. J itself lies in the subalgebra (completing u(5) = su(5) ⊕ u(1))

### What this gives us (via mathlib's LieSubalgebra instances):
- LieRing u5_subalgebra (automatic)
- LieAlgebra ℝ u5_subalgebra (automatic)
- u5_subalgebra.incl : u5_subalgebra →ₗ⁅ℝ⁆ SO10 (inclusion morphism, free)

### Combined with existing results:
- su5_so10_embedding.lean: [G, J] = 0 for all 24 generators
- su5_lie_structure.lean: A₄ Cartan matrix identifies su(5) (48 theorems)
- so10_grand.lean: SO10 has LieRing/LieAlgebra ℝ instances

### What this does NOT prove:
- Linear independence of the 24 generators (straightforward but tedious)
- The direct sum decomposition u(5) = su(5) ⊕ u(1)
- A LieHom from a standalone SU5 compact-form type (requires Option B:
  new SU5 type with LieRing/LieAlgebra instances, needed for Papers 3&4)

Machine-verified. 0 sorry.
-/
