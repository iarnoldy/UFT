/-
UFT Formal Verification - Block-Tridiagonal Structure from Grade Selection
==========================================================================

SPECTRAL THEORY FOUNDATION 4:
  Grade selection rules in Cl(3,0) constrain how Clifford products
  map between grades. Specifically:

  (grade 2) × (grade 2) → grade 0 ⊕ grade 2    (NO grade 1 or 3)

  This is the algebraic origin of the block-tridiagonal Hamiltonian
  structure that constrains the mass gap spectrum.

References:
  - Lounesto, "Clifford Algebras and Spinors" (2001), Ch. 3, 14
-/

import spectral.grade2_lie_algebra

namespace Cl30

/-! ## Part 1: Grade Projection Operators

Cl(3,0) has 8 basis elements distributed across 4 grades:
  Grade 0: {1}             — 1 element  (scalar)
  Grade 1: {e1, e2, e3}    — 3 elements (vectors)
  Grade 2: {e12, e13, e23} — 3 elements (bivectors)
  Grade 3: {e123}          — 1 element  (pseudoscalar)

Total: 1 + 3 + 3 + 1 = 8 = 2³ ✓ -/

/-- Project onto grade 0 (scalar). -/
def grade0 (x : Cl30) : Cl30 :=
  ⟨x.s, 0, 0, 0, 0, 0, 0, 0⟩

/-- Project onto grade 1 (vector). -/
def grade1 (x : Cl30) : Cl30 :=
  ⟨0, x.v1, x.v2, x.v3, 0, 0, 0, 0⟩

/-- Project onto grade 2 (bivector). -/
def grade2 (x : Cl30) : Cl30 :=
  ⟨0, 0, 0, 0, x.b12, x.b13, x.b23, 0⟩

/-- Project onto grade 3 (pseudoscalar). -/
def grade3 (x : Cl30) : Cl30 :=
  ⟨0, 0, 0, 0, 0, 0, 0, x.ps⟩

/-- Any element decomposes into graded components.
    x = grade₀(x) + grade₁(x) + grade₂(x) + grade₃(x) -/
theorem grade_decomposition (x : Cl30) :
    x = grade0 x + grade1 x + grade2 x + grade3 x := by
  ext <;> simp [grade0, grade1, grade2, grade3, add]

/-- Grade projections are idempotent. -/
theorem grade0_idempotent (x : Cl30) : grade0 (grade0 x) = grade0 x := by
  ext <;> simp [grade0]

theorem grade1_idempotent (x : Cl30) : grade1 (grade1 x) = grade1 x := by
  ext <;> simp [grade1]

theorem grade2_idempotent (x : Cl30) : grade2 (grade2 x) = grade2 x := by
  ext <;> simp [grade2]

theorem grade3_idempotent (x : Cl30) : grade3 (grade3 x) = grade3 x := by
  ext <;> simp [grade3]

/-- Grade projections are orthogonal. -/
theorem grade0_grade1 (x : Cl30) : grade0 (grade1 x) = zero := by
  ext <;> simp [grade0, grade1, zero]

theorem grade0_grade2 (x : Cl30) : grade0 (grade2 x) = zero := by
  ext <;> simp [grade0, grade2, zero]

theorem grade1_grade2 (x : Cl30) : grade1 (grade2 x) = zero := by
  ext <;> simp [grade1, grade2, zero]

/-! ## Part 2: Product Grade Selection

When a bivector (grade 2) multiplies another element, it shifts grade.
The KEY structural result:

  (grade 2) × (grade 2) → grade 0 ⊕ grade 2

This means: no grade-1 or grade-3 components in a bivector product.
This is what creates the block-tridiagonal Hamiltonian structure. -/

/-- A bivector times a scalar gives a bivector.
    (grade 2) × (grade 0) ⊆ grade 2. -/
theorem grade2_times_grade0 (B : Cl30) (hB : isPureBivector B) :
    isPureBivector (B * one) := by
  obtain ⟨hBs, hBv1, hBv2, hBv3, hBps⟩ := hB
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
  simp [mul_def, mul, one, hBs, hBv1, hBv2, hBv3, hBps]

/-- A bivector times a bivector has no grade-1 or grade-3 components.
    (grade 2) × (grade 2) ⊆ grade 0 ⊕ grade 2.

    This is THE selection rule that creates block-tridiagonal structure. -/
theorem grade2_times_grade2_selection (A B : Cl30)
    (hA : isPureBivector A) (hB : isPureBivector B) :
    (A * B).v1 = 0 ∧ (A * B).v2 = 0 ∧ (A * B).v3 = 0 ∧ (A * B).ps = 0 := by
  obtain ⟨hAs, hAv1, hAv2, hAv3, hAps⟩ := hA
  obtain ⟨hBs, hBv1, hBv2, hBv3, hBps⟩ := hB
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
  simp [mul_def, mul, hAs, hAv1, hAv2, hAv3, hAps,
    hBs, hBv1, hBv2, hBv3, hBps] <;> ring

/-- The product of two bivectors has no grade-1 component. -/
theorem bivector_product_no_vector (A B : Cl30)
    (hA : isPureBivector A) (hB : isPureBivector B) :
    grade1 (A * B) = zero := by
  obtain ⟨hAs, hAv1, hAv2, hAv3, hAps⟩ := hA
  obtain ⟨hBs, hBv1, hBv2, hBv3, hBps⟩ := hB
  ext <;> simp [grade1, mul_def, mul, zero,
    hAs, hAv1, hAv2, hAv3, hAps, hBs, hBv1, hBv2, hBv3, hBps] <;>
  ring

/-- The product of two bivectors has no grade-3 component. -/
theorem bivector_product_no_pseudoscalar (A B : Cl30)
    (hA : isPureBivector A) (hB : isPureBivector B) :
    grade3 (A * B) = zero := by
  obtain ⟨hAs, hAv1, hAv2, hAv3, hAps⟩ := hA
  obtain ⟨hBs, hBv1, hBv2, hBv3, hBps⟩ := hB
  ext <;> simp [grade3, mul_def, mul, zero,
    hAs, hAv1, hAv2, hAv3, hAps, hBs, hBv1, hBv2, hBv3, hBps] <;>
  ring

/-! ## Part 3: Concrete Grade Shifting Verification

Verify how e12 maps each basis element between grades. -/

/-- e12 · 1 = e12 (grade 0 → grade 2). -/
theorem e12_on_scalar : e12 * (1 : Cl30) = e12 := by
  ext <;> simp [e12, one, mul]

/-- e12 · e1 = -e2 (grade 1 → grade 1, rotation action). -/
theorem e12_on_e1 : e12 * e1 = neg e2 := by
  ext <;> simp [e12, e1, e2, mul, neg]

/-- e12 · e3 = e123 (grade 1 → grade 3, shift by +2). -/
theorem e12_on_e3 : e12 * e3 = e123 := by
  ext <;> simp [e12, e3, e123, mul]

/-- e12 · e23 = e13 (grade 2 → grade 2, no grade shift). -/
theorem e12_on_e23 : e12 * e23 = e13 := by
  ext <;> simp [e12, e23, e13, mul]

/-- e12 · e123 = -e3 (grade 3 → grade 1, shift by -2). -/
theorem e12_on_e123 : e12 * e123 = neg e3 := by
  ext <;> simp [e12, e123, e3, mul, neg]

/-! ## Part 4: The Casimir as Sum of Squares (Grade Analysis)

The Casimir C₂ = e12² + e13² + e23² is a sum of products of
grade-2 elements. By the selection rule, each eij² lies in
grade 0 ⊕ grade 2. In fact, each eij² is pure grade 0 (= -1). -/

/-- e12² has only grade-0 component. -/
theorem e12_sq_grade0 : grade0 (e12 * e12) = smul (-1) one := by
  ext <;> simp [grade0, e12, mul, smul, one]

theorem e12_sq_grade2 : grade2 (e12 * e12) = zero := by
  ext <;> simp [grade2, e12, mul, zero]

/-- e12 · e13 is pure grade-2 (no scalar part). -/
theorem e12_e13_grade0 : grade0 (e12 * e13) = zero := by
  ext <;> simp [grade0, e12, e13, mul, zero]

/-- e12 · e13 = -e23 (a bivector). -/
theorem e12_e13_is_neg_e23 : e12 * e13 = neg e23 := by
  ext <;> simp [e12, e13, e23, mul, neg]

end Cl30

/-!
## Summary: Block-Tridiagonal Structure from Grade Selection

### Theorems proved (0 sorry):

1. **Grade decomposition**: x = grade₀ + grade₁ + grade₂ + grade₃
2. **Projector properties**: idempotent and orthogonal
3. **THE selection rule**: (grade 2)² has no grade 1 or grade 3 components
4. **Concrete verification**: e12 maps between specific grades
5. **Casimir grade structure**: eij² is pure grade 0

### For the mass gap:

The block-tridiagonal structure means:
```
  H |ψ₀⟩ → |ψ₀⟩ ⊕ |ψ₂⟩           (grade 0 ↔ grade 2)
  H |ψ₁⟩ → |ψ₁⟩ ⊕ |ψ₃⟩           (grade 1 ↔ grade 3)
  H |ψ₂⟩ → |ψ₀⟩ ⊕ |ψ₂⟩ ⊕ |ψ₄⟩   (grade 2 ↔ grades 0, 4)
```

The Hamiltonian matrix in the grade basis is BANDED.
The resolvent of a banded matrix has a continued fraction expansion.
The mass gap is the first pole of this continued fraction.
-/
