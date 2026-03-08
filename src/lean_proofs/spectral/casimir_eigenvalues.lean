/-
UFT Formal Verification - Casimir Eigenvalues for so(n)
=======================================================

SPECTRAL THEORY FOUNDATION 2:
  The quadratic Casimir C₂ has eigenvalue -2·I₃ in the fundamental
  representation of so(3) (3×3 antisymmetric matrices).

  For general so(n): C₂(fund) = -(n-1)·I_n (with [Lᵢ,Lⱼ]=εᵢⱼₖLₖ normalization).
  With half-normalization Tr(TₐTᵦ) = (1/2)δₐᵦ: c₂(fund) = (n-1)/2.

This file proves:
  1. The so(3) generators as 3×3 matrices
  2. Structure constants [Lᵢ, Lⱼ] = εᵢⱼₖ Lₖ
  3. The Casimir C₂ = L₁² + L₂² + L₃² = -2·I₃
  4. The Casimir is nonzero (spectral gap)
  5. The Casimir commutes with all generators (Schur centrality)

References:
  - Humphreys, "Introduction to Lie Algebras" (1972), §6.2
  - Hall, "Lie Groups, Lie Algebras, and Representations" (2015), Ch. 6
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-! ## Part 1: 3×3 Real Matrices

Concrete representation for computing with so(3). -/

/-- A 3×3 real matrix. -/
@[ext]
structure Mat3 where
  a11 : ℝ
  a12 : ℝ
  a13 : ℝ
  a21 : ℝ
  a22 : ℝ
  a23 : ℝ
  a31 : ℝ
  a32 : ℝ
  a33 : ℝ

namespace Mat3

/-- Matrix multiplication. -/
def mul (X Y : Mat3) : Mat3 where
  a11 := X.a11*Y.a11 + X.a12*Y.a21 + X.a13*Y.a31
  a12 := X.a11*Y.a12 + X.a12*Y.a22 + X.a13*Y.a32
  a13 := X.a11*Y.a13 + X.a12*Y.a23 + X.a13*Y.a33
  a21 := X.a21*Y.a11 + X.a22*Y.a21 + X.a23*Y.a31
  a22 := X.a21*Y.a12 + X.a22*Y.a22 + X.a23*Y.a32
  a23 := X.a21*Y.a13 + X.a22*Y.a23 + X.a23*Y.a33
  a31 := X.a31*Y.a11 + X.a32*Y.a21 + X.a33*Y.a31
  a32 := X.a31*Y.a12 + X.a32*Y.a22 + X.a33*Y.a32
  a33 := X.a31*Y.a13 + X.a32*Y.a23 + X.a33*Y.a33

instance : Mul Mat3 := ⟨mul⟩

/-- Matrix addition. -/
def add (X Y : Mat3) : Mat3 where
  a11 := X.a11+Y.a11
  a12 := X.a12+Y.a12
  a13 := X.a13+Y.a13
  a21 := X.a21+Y.a21
  a22 := X.a22+Y.a22
  a23 := X.a23+Y.a23
  a31 := X.a31+Y.a31
  a32 := X.a32+Y.a32
  a33 := X.a33+Y.a33

instance : Add Mat3 := ⟨add⟩

/-- The 3×3 identity matrix. -/
def id3 : Mat3 where
  a11 := 1; a12 := 0; a13 := 0
  a21 := 0; a22 := 1; a23 := 0
  a31 := 0; a32 := 0; a33 := 1
instance : One Mat3 := ⟨id3⟩

/-- The 3×3 zero matrix. -/
def zero3 : Mat3 where
  a11 := 0; a12 := 0; a13 := 0
  a21 := 0; a22 := 0; a23 := 0
  a31 := 0; a32 := 0; a33 := 0
instance : Zero Mat3 := ⟨zero3⟩

/-- Scalar multiplication. -/
def smul (r : ℝ) (X : Mat3) : Mat3 where
  a11 := r*X.a11; a12 := r*X.a12; a13 := r*X.a13
  a21 := r*X.a21; a22 := r*X.a22; a23 := r*X.a23
  a31 := r*X.a31; a32 := r*X.a32; a33 := r*X.a33

/-- Matrix negation. -/
def neg (X : Mat3) : Mat3 where
  a11 := -X.a11; a12 := -X.a12; a13 := -X.a13
  a21 := -X.a21; a22 := -X.a22; a23 := -X.a23
  a31 := -X.a31; a32 := -X.a32; a33 := -X.a33

instance : Neg Mat3 := ⟨neg⟩

/-- The trace. -/
def tr (X : Mat3) : ℝ := X.a11 + X.a22 + X.a33

@[simp] lemma mul_def' (a b : Mat3) : a * b = mul a b := rfl
@[simp] lemma add_def' (a b : Mat3) : a + b = add a b := rfl
@[simp] lemma neg_def' (a : Mat3) : -a = neg a := rfl
@[simp] lemma one_val' : (1 : Mat3) = id3 := rfl
@[simp] lemma zero_val' : (0 : Mat3) = zero3 := rfl

/-! ## Part 2: The so(3) Generators -/

/-- L₁ = rotation generator about axis 1 (in the 23-plane). -/
def L1 : Mat3 where
  a11 := 0; a12 := 0; a13 := 0
  a21 := 0; a22 := 0; a23 := -1
  a31 := 0; a32 := 1; a33 := 0

/-- L₂ = rotation generator about axis 2 (in the 13-plane). -/
def L2 : Mat3 where
  a11 := 0; a12 := 0; a13 := 1
  a21 := 0; a22 := 0; a23 := 0
  a31 := -1; a32 := 0; a33 := 0

/-- L₃ = rotation generator about axis 3 (in the 12-plane). -/
def L3 : Mat3 where
  a11 := 0; a12 := -1; a13 := 0
  a21 := 1; a22 := 0; a23 := 0
  a31 := 0; a32 := 0; a33 := 0

/-- The matrix commutator [X, Y] = XY - YX. -/
def comm (X Y : Mat3) : Mat3 := X * Y + -(Y * X)

/-! ### Structure Constants -/

/-- [L₁, L₂] = L₃. -/
theorem comm_L1_L2 : comm L1 L2 = L3 := by
  ext <;> simp [comm, L1, L2, L3, mul, add, neg]

/-- [L₂, L₃] = L₁. -/
theorem comm_L2_L3 : comm L2 L3 = L1 := by
  ext <;> simp [comm, L2, L3, L1, mul, add, neg]

/-- [L₃, L₁] = L₂. -/
theorem comm_L3_L1 : comm L3 L1 = L2 := by
  ext <;> simp [comm, L3, L1, L2, mul, add, neg]

/-! ### Trace Normalization -/

/-- Tr(L₁²) = -2. -/
theorem tr_L1_sq : tr (L1 * L1) = -2 := by
  simp [tr, L1, mul]; norm_num

/-- Tr(L₂²) = -2. -/
theorem tr_L2_sq : tr (L2 * L2) = -2 := by
  simp [tr, L2, mul]; norm_num

/-- Tr(L₃²) = -2. -/
theorem tr_L3_sq : tr (L3 * L3) = -2 := by
  simp [tr, L3, mul]; norm_num

/-- Tr(L₁L₂) = 0 (orthogonality). -/
theorem tr_L1_L2 : tr (L1 * L2) = 0 := by
  simp [tr, L1, L2, mul]

/-- Tr(L₁L₃) = 0. -/
theorem tr_L1_L3 : tr (L1 * L3) = 0 := by
  simp [tr, L1, L3, mul]

/-- Tr(L₂L₃) = 0. -/
theorem tr_L2_L3 : tr (L2 * L3) = 0 := by
  simp [tr, L2, L3, mul]

/-! ## Part 3: The Casimir Operator -/

/-- The quadratic Casimir of so(3) in the fundamental representation. -/
def casimir_fund : Mat3 := L1 * L1 + L2 * L2 + L3 * L3

/-- THE CASIMIR EIGENVALUE THEOREM (fundamental of so(3)):
    C₂ = L₁² + L₂² + L₃² = -2 · I₃ -/
theorem casimir_fund_val : casimir_fund = smul (-2) id3 := by
  ext <;> simp [casimir_fund, L1, L2, L3, mul, add, smul, id3] <;> norm_num

/-- The Casimir eigenvalue is nonzero. -/
theorem casimir_fund_nonzero : casimir_fund ≠ (0 : Mat3) := by
  intro h
  have := congr_arg Mat3.a11 h
  simp [casimir_fund, L1, L2, L3, mul, add, zero3] at this

/-- The Casimir commutes with L₁. -/
theorem casimir_commutes_L1 : comm casimir_fund L1 = zero3 := by
  ext <;> simp [comm, casimir_fund, L1, L2, L3, mul, add, neg, zero3]

/-- The Casimir commutes with L₂. -/
theorem casimir_commutes_L2 : comm casimir_fund L2 = zero3 := by
  ext <;> simp [comm, casimir_fund, L1, L2, L3, mul, add, neg, zero3]

/-- The Casimir commutes with L₃. -/
theorem casimir_commutes_L3 : comm casimir_fund L3 = zero3 := by
  ext <;> simp [comm, casimir_fund, L1, L2, L3, mul, add, neg, zero3]

/-! ## Part 4: Eigenvalue Verification

C₂ · eᵢ = -2 · eᵢ for each standard basis vector. -/

/-- C₂ acts as -2 on the first basis vector. -/
theorem casimir_eigenvalue_e1 :
    mul casimir_fund (Mat3.mk 1 0 0 0 0 0 0 0 0) =
    smul (-2) (Mat3.mk 1 0 0 0 0 0 0 0 0) := by
  ext <;> simp [casimir_fund, L1, L2, L3, mul, add, smul] <;> norm_num

/-- C₂ acts as -2 on the second basis vector. -/
theorem casimir_eigenvalue_e2 :
    mul casimir_fund (Mat3.mk 0 0 0 1 0 0 0 0 0) =
    smul (-2) (Mat3.mk 0 0 0 1 0 0 0 0 0) := by
  ext <;> simp [casimir_fund, L1, L2, L3, mul, add, smul] <;> norm_num

/-- C₂ acts as -2 on the third basis vector. -/
theorem casimir_eigenvalue_e3 :
    mul casimir_fund (Mat3.mk 0 0 0 0 0 0 1 0 0) =
    smul (-2) (Mat3.mk 0 0 0 0 0 0 1 0 0) := by
  ext <;> simp [casimir_fund, L1, L2, L3, mul, add, smul] <;> norm_num

end Mat3

/-!
## Summary: Casimir Eigenvalues

### Theorems proved (0 sorry):

1. **Structure constants**: [Lᵢ, Lⱼ] = εᵢⱼₖ Lₖ in 3×3 matrices
2. **Trace normalization**: Tr(LᵢLⱼ) = -2δᵢⱼ (Killing form)
3. **Casimir eigenvalue**: C₂ = -2·I₃ in the fundamental
4. **Nonzero**: C₂ ≠ 0 (spectral gap)
5. **Centrality**: [C₂, Lᵢ] = 0 for all generators
6. **Eigenvalue equations**: C₂·eᵢ = -2·eᵢ for each basis vector

### The mass gap connection:

| Algebra | C₂(fund) | Mass gap eligible? |
|---------|----------|-------------------|
| so(3)   | -2·I₃   | Yes (compact)     |
| so(14)  | -13·I₁₄ | Yes (compact)     |

### Next: `casimir_spectral_gap.lean`
-/
