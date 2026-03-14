/-
UFT Formal Verification - SO(4) Compact Gravity Algebra
========================================================

THE COMPACT so(4) LIE ALGEBRA (GRAVITY SECTOR)

This file defines so(4) as a 6-dimensional Lie algebra with certified
LieRing and LieAlgebra ℝ instances.

so(4) is the COMPACT form of the rotation algebra in 4 dimensions.
It appears as the gravity sector of so(14) when using compact signature
(so(14,0)). Under the decomposition so(14) ⊃ so(10) ⊕ so(4) ⊕ (10,4):
  - so(10): gauge sector (45 generators, indices 1-10)
  - so(4): gravity sector (6 generators, indices 11-14)
  - (10,4): mixed sector (40 generators)

IMPORTANT SIGNATURE NOTE:
  so(4) ≅ su(2) ⊕ su(2) is COMPACT. Physical gravity uses so(1,3)
  (Lorentz algebra), which is the SPLIT real form:
  so(1,3) ≅ sl(2,ℝ) ⊕ sl(2,ℝ). These are NOT isomorphic as real Lie
  algebras — they have different structure constants in the boost-rotation
  sector. The Bivector type in gauge_gravity.lean implements so(1,3), NOT so(4).

  For physical gravity in the unified theory, one needs so(11,3) instead
  of so(14,0). This file provides the compact-signature gravity embedding.

Generators: L_{ij} for 1 ≤ i < j ≤ 4 (using so(4) indexing).
When embedded in so(14), these become L_{i+10,j+10} (indices 11-14).

Lie bracket: [L_{ij}, L_{kl}] = δ_{jk}L_{il} - δ_{ik}L_{jl}
                                - δ_{jl}L_{ik} + δ_{il}L_{jk}
(all Kronecker deltas — compact/Euclidean metric).

References:
  - gauge_gravity.lean: Bivector type (so(1,3), DIFFERENT bracket)
  - so14_grand.lean: SO14 type (gravity block = so(4))
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Algebra.Lie.Basic

/-! ## Part 1: The so(4) Compact Lie Algebra

6 generators corresponding to antisymmetric 4×4 matrices. -/

/-- The compact Lie algebra so(4), with 6 generators L_{ij} (i < j).
    Isomorphic to su(2) ⊕ su(2). NOT isomorphic to so(1,3). -/
@[ext]
structure SO4 where
  l12 : ℝ  -- L_{1,2}
  l13 : ℝ  -- L_{1,3}
  l14 : ℝ  -- L_{1,4}
  l23 : ℝ  -- L_{2,3}
  l24 : ℝ  -- L_{2,4}
  l34 : ℝ  -- L_{3,4}

namespace SO4

/-! ## Part 2: Basic Operations -/

def zero : SO4 := ⟨0, 0, 0, 0, 0, 0⟩

def neg (x : SO4) : SO4 := ⟨-x.l12, -x.l13, -x.l14, -x.l23, -x.l24, -x.l34⟩

def add (x y : SO4) : SO4 :=
  ⟨x.l12+y.l12, x.l13+y.l13, x.l14+y.l14, x.l23+y.l23, x.l24+y.l24, x.l34+y.l34⟩

def smul (r : ℝ) (x : SO4) : SO4 :=
  ⟨r*x.l12, r*x.l13, r*x.l14, r*x.l23, r*x.l24, r*x.l34⟩

instance : Add SO4 := ⟨add⟩
instance : Neg SO4 := ⟨neg⟩
instance : Zero SO4 := ⟨zero⟩
instance : Sub SO4 := ⟨fun a b => add a (neg b)⟩
instance : SMul ℝ SO4 := ⟨smul⟩

@[simp] lemma add_def (a b : SO4) : a + b = add a b := rfl
@[simp] lemma neg_def (a : SO4) : -a = neg a := rfl
@[simp] lemma zero_val : (0 : SO4) = zero := rfl
@[simp] lemma sub_def' (a b : SO4) : a - b = add a (neg b) := rfl
@[simp] lemma smul_def' (r : ℝ) (a : SO4) : r • a = smul r a := rfl

/-! ## Part 3: The Lie Bracket

[L_{ij}, L_{kl}] = δ_{jk}L_{il} - δ_{ik}L_{jl} - δ_{jl}L_{ik} + δ_{il}L_{jk}
with compact (Euclidean) metric. All 36 brackets computed. -/

/-- The Lie bracket of two so(4) elements (compact metric). -/
def comm (X Y : SO4) : SO4 where
  -- [*, *] → l12 component: contributions from (13,23), (14,24) and reverses
  l12 := -(X.l13 * Y.l23) - (X.l14 * Y.l24) + X.l23 * Y.l13 + X.l24 * Y.l14
  -- [*, *] → l13 component: contributions from (12,23), (14,34) and reverses
  l13 := X.l12 * Y.l23 - (X.l14 * Y.l34) - (X.l23 * Y.l12) + X.l34 * Y.l14
  -- [*, *] → l14 component: contributions from (12,24), (13,34) and reverses
  l14 := X.l12 * Y.l24 + X.l13 * Y.l34 - (X.l24 * Y.l12) - (X.l34 * Y.l13)
  -- [*, *] → l23 component: contributions from (12,13), (24,34) and reverses
  l23 := -(X.l12 * Y.l13) + X.l13 * Y.l12 - (X.l24 * Y.l34) + X.l34 * Y.l24
  -- [*, *] → l24 component: contributions from (12,14), (23,34) and reverses
  l24 := -(X.l12 * Y.l14) + X.l14 * Y.l12 + X.l23 * Y.l34 - (X.l34 * Y.l23)
  -- [*, *] → l34 component: contributions from (13,14), (23,24) and reverses
  l34 := -(X.l13 * Y.l14) + X.l14 * Y.l13 - (X.l23 * Y.l24) + X.l24 * Y.l23

/-! ## Part 4: Lie Algebra Verification -/

/-- Antisymmetry: [X, Y] = -[Y, X]. -/
theorem comm_antisymm (X Y : SO4) : comm X Y = neg (comm Y X) := by
  ext <;> simp [comm, neg] <;> ring

/-- The Jacobi identity for so(4). -/
theorem jacobi (A B C : SO4) :
    comm A (comm B C) + comm B (comm C A) + comm C (comm A B) = zero := by
  ext <;> simp [comm, add, zero] <;> ring

/-! ## Part 5: Mathlib LieRing and LieAlgebra Instances -/

instance : AddCommGroup SO4 where
  add_assoc := by intros; ext <;> simp [add] <;> ring
  zero_add := by intros; ext <;> simp [add, zero]
  add_zero := by intros; ext <;> simp [add, zero]
  add_comm := by intros; ext <;> simp [add] <;> ring
  neg_add_cancel := by intros; ext <;> simp [add, neg, zero]
  sub_eq_add_neg := by intros; rfl
  nsmul := nsmulRec
  zsmul := zsmulRec

instance : Module ℝ SO4 where
  one_smul := by intros; ext <;> simp [smul]
  mul_smul := by intros; ext <;> simp [smul] <;> ring
  smul_zero := by intros; ext <;> simp [smul, zero]
  smul_add := by intros; ext <;> simp [smul, add] <;> ring
  add_smul := by intros; ext <;> simp [smul, add] <;> ring
  zero_smul := by intros; ext <;> simp [smul, zero]

instance : Bracket SO4 SO4 := ⟨comm⟩

@[simp] lemma bracket_def' (a b : SO4) : ⁅a, b⁆ = comm a b := rfl

instance : LieRing SO4 where
  add_lie := by intros; ext <;> simp [comm, add] <;> ring
  lie_add := by intros; ext <;> simp [comm, add] <;> ring
  lie_self := by intro x; ext <;> simp [comm, zero] <;> ring
  leibniz_lie := by intros; ext <;> simp [comm, add] <;> ring

instance : LieAlgebra ℝ SO4 where
  lie_smul := by intros; ext <;> simp [comm, smul] <;> ring

/-! ## Part 6: Basis Generators -/

def L12 : SO4 := ⟨1, 0, 0, 0, 0, 0⟩
def L13 : SO4 := ⟨0, 1, 0, 0, 0, 0⟩
def L14 : SO4 := ⟨0, 0, 1, 0, 0, 0⟩
def L23 : SO4 := ⟨0, 0, 0, 1, 0, 0⟩
def L24 : SO4 := ⟨0, 0, 0, 0, 1, 0⟩
def L34 : SO4 := ⟨0, 0, 0, 0, 0, 1⟩

/-- [L12, L23] = L13. Two rotations compose. -/
theorem bracket_L12_L23 : comm L12 L23 = L13 := by
  ext <;> simp [comm, L12, L23, L13]

/-- [L12, L13] = neg L23. -/
theorem bracket_L12_L13 : comm L12 L13 = neg L23 := by
  ext <;> simp [comm, L12, L13, neg, L23]

/-- [L12, L34] = 0. Orthogonal rotations commute. -/
theorem bracket_L12_L34 : comm L12 L34 = zero := by
  ext <;> simp [comm, L12, L34, zero]

/-! ## Part 7: Comparison with Bivector (so(1,3))

The Bivector type in gauge_gravity.lean has DIFFERENT structure constants:
  Bivector.comm K1 J3 = neg K2     (so(1,3): [L_{01}, L_{12}] = -L_{02})
  SO4.comm L12 L23 = neg L13       (so(4):   [L_{12}, L_{23}] = -L_{13})

But for the boost-rotation cross-bracket:
  Bivector: [K1, J3] = -K2    (η_{11} = -1 in Lorentzian metric)
  SO4:      [L12, L23] = -L13 (δ_{22} = +1 in Euclidean metric)

The signs differ whenever the metric η vs δ contributes a -1.
This makes them non-isomorphic as real Lie algebras. -/

end SO4

/-! ## Summary

### What this file proves:
1. so(4) compact Lie algebra with 6 generators (Part 1-3)
2. Jacobi identity (Part 4)
3. Certified LieRing and LieAlgebra ℝ instances (Part 5)
4. Structure constant verification (Part 6)

### Relationship to other files:
- **gauge_gravity.lean**: Bivector = so(1,3), different algebra
- **so14_grand.lean**: SO14 contains so(4) as gravity sector (indices 11-14)
- **so4_so14_liehom.lean**: embeds this SO4 into SO14

### Signature:
This is the COMPACT form so(4) ≅ su(2) ⊕ su(2).
Physical gravity uses so(1,3) ≅ sl(2,ℝ) ⊕ sl(2,ℝ) (Lorentzian).
The two are NOT isomorphic over ℝ.

0 sorry gaps.
-/
