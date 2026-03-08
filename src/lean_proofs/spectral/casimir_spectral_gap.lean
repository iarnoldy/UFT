/-
UFT Formal Verification - Casimir Spectral Gap Theorem
======================================================

SPECTRAL THEORY FOUNDATION 3: THE MAIN THEOREM

For any nonzero antisymmetric 3×3 matrix H (element of so(3)),
H² ≠ 0 and Tr(H²) < 0. This is the finite-dimensional spectral gap.

The Killing form B(H,H) = Tr(H²) = -2(a²+b²+c²) is negative definite,
meaning every nonzero so(3) element has nonzero norm.

This is the algebraic precursor to the mass gap: in representation
theory, the Casimir eigenvalue bounds energies from below.

References:
  - Humphreys, "Introduction to Lie Algebras" (1972), Ch. 6
  - Hall, "Lie Groups, Lie Algebras, and Representations" (2015), Ch. 6
-/

import spectral.casimir_eigenvalues

namespace Mat3

/-! ## Part 1: General so(3) Elements -/

/-- A general so(3) element: H = a·L₁ + b·L₂ + c·L₃. -/
def so3_element (a b c : ℝ) : Mat3 :=
  add (add (smul a L1) (smul b L2)) (smul c L3)

/-- A general so(3) element is antisymmetric: Hᵀ = -H. -/
def transpose (X : Mat3) : Mat3 where
  a11 := X.a11; a12 := X.a21; a13 := X.a31
  a21 := X.a12; a22 := X.a22; a23 := X.a32
  a31 := X.a13; a32 := X.a23; a33 := X.a33

theorem so3_element_antisymmetric (a b c : ℝ) :
    transpose (so3_element a b c) = neg (so3_element a b c) := by
  ext <;> simp [so3_element, transpose, neg, add, smul, L1, L2, L3] <;> ring

/-! ## Part 2: The Killing Form -/

/-- H² for a general so(3) element. -/
def so3_element_squared (a b c : ℝ) : Mat3 :=
  mul (so3_element a b c) (so3_element a b c)

/-- THE KILLING FORM: Tr(H²) = -2(a² + b² + c²).

    This is negative definite on so(3), which means:
    - Every nonzero element has nonzero norm
    - The Lie algebra is COMPACT (negative Killing form)
    - Compactness is REQUIRED for the mass gap -/
theorem so3_sq_trace (a b c : ℝ) :
    tr (so3_element_squared a b c) = -(2 * (a^2 + b^2 + c^2)) := by
  simp only [so3_element_squared, so3_element, tr, mul, add, smul, L1, L2, L3]
  ring

/-! ## Part 3: The Spectral Gap -/

/-- If (a,b,c) ≠ (0,0,0), then Tr(H²) ≠ 0.
    Nonzero so(3) elements have nonzero Killing norm. -/
theorem so3_nonzero_killing (a b c : ℝ)
    (h : ¬(a = 0 ∧ b = 0 ∧ c = 0)) :
    tr (so3_element_squared a b c) ≠ 0 := by
  rw [so3_sq_trace]
  intro heq
  have hab : a^2 + b^2 + c^2 = 0 := by linarith
  have ha : a = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg c]
  have hb : b = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg c]
  have hc : c = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg c]
  exact h ⟨ha, hb, hc⟩

/-- The Killing form is strictly negative for nonzero elements.
    This is the signature property of a COMPACT Lie algebra.

    For so(n): Killing form B(X,Y) = (n-2)Tr(XY).
    For so(3): B(H,H) = Tr(H²) < 0 when H ≠ 0.

    Compactness → all representations finite-dimensional →
    discrete spectrum → Casimir eigenvalues are algebraic numbers →
    mass gap is an algebraic property. -/
theorem killing_form_negative (a b c : ℝ)
    (h : ¬(a = 0 ∧ b = 0 ∧ c = 0)) :
    tr (so3_element_squared a b c) < 0 := by
  rw [so3_sq_trace]
  have : a^2 + b^2 + c^2 > 0 := by
    by_contra hle
    push_neg at hle
    have ha : a = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg c]
    have hb : b = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg c]
    have hc : c = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg c]
    exact h ⟨ha, hb, hc⟩
  linarith

/-- H² ≠ 0 when H ≠ 0 in so(3).
    This is the FINITE-DIMENSIONAL SPECTRAL GAP.

    Any state with nonzero gauge charge has nonzero energy. -/
theorem so3_sq_nonzero (a b c : ℝ)
    (h : ¬(a = 0 ∧ b = 0 ∧ c = 0)) :
    so3_element_squared a b c ≠ (0 : Mat3) := by
  intro heq
  have htr := so3_nonzero_killing a b c h
  apply htr
  rw [heq]
  simp [tr, zero3]

/-- The diagonal entries of H² are all ≤ 0.
    H is antisymmetric, so H² = -HᵀH is negative semidefinite. -/
theorem so3_sq_a11 (a b c : ℝ) :
    (so3_element_squared a b c).a11 = -(b^2 + c^2) := by
  simp [so3_element_squared, so3_element, mul, add, smul, L1, L2, L3]
  ring

theorem so3_sq_a22 (a b c : ℝ) :
    (so3_element_squared a b c).a22 = -(a^2 + c^2) := by
  simp [so3_element_squared, so3_element, mul, add, smul, L1, L2, L3]
  ring

theorem so3_sq_a33 (a b c : ℝ) :
    (so3_element_squared a b c).a33 = -(a^2 + b^2) := by
  simp [so3_element_squared, so3_element, mul, add, smul, L1, L2, L3]
  ring

theorem so3_sq_diagonal_nonpositive (a b c : ℝ) :
    (so3_element_squared a b c).a11 ≤ 0 ∧
    (so3_element_squared a b c).a22 ≤ 0 ∧
    (so3_element_squared a b c).a33 ≤ 0 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [so3_sq_a11]; nlinarith [sq_nonneg b, sq_nonneg c]
  · rw [so3_sq_a22]; nlinarith [sq_nonneg a, sq_nonneg c]
  · rw [so3_sq_a33]; nlinarith [sq_nonneg a, sq_nonneg b]

/-! ## Part 4: The Casimir Spectral Gap Statement -/

/-- THE CASIMIR SPECTRAL GAP (finite-dimensional):

    C₂ = L₁² + L₂² + L₃² = -2·I₃

    Every vector in ℝ³ is an eigenvector with eigenvalue -2.
    Since -2 ≠ 0, there is NO zero eigenvalue.
    spec(C₂|fund) = {-2} — a spectral gap of |2|.

    For so(n): spec(C₂|fund) = {-(n-1)} with gap |n-1|.
    For so(14): spec(C₂|fund) = {-13} with gap 13. -/
theorem casimir_spectral_gap :
    casimir_fund = smul (-2) id3 := casimir_fund_val

end Mat3

/-!
## Summary: The Casimir Spectral Gap

### Theorems proved (0 sorry):

1. **Killing form**: Tr(H²) = -2(a²+b²+c²) — negative definite
2. **Nondegenerate**: H ≠ 0 → Tr(H²) ≠ 0
3. **Strictly negative**: H ≠ 0 → Tr(H²) < 0 — compact algebra
4. **H² nonzero**: H ≠ 0 → H² ≠ 0 — spectral gap
5. **Diagonal bounds**: (H²)ᵢᵢ ≤ 0 — negative semidefinite
6. **Casimir gap**: C₂ = -2·I₃ — no zero eigenvalue

### The mass gap hierarchy:

```
  Casimir ≠ 0  (algebraic, this file)  ← PROVED
       ↓
  H² ≠ 0 for H ∈ so(n)  (finite-dim)  ← PROVED
       ↓
  Lattice Ĥ has gap  (numerical)       ← OBSERVED (lattice QCD)
       ↓
  Continuum Ĥ has gap  (analysis)      ← MILLENNIUM PRIZE
```
-/
