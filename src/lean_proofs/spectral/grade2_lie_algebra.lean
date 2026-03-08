/-
UFT Formal Verification - Grade-2 Lie Algebra from Clifford Algebra
====================================================================

SPECTRAL THEORY FOUNDATION 1:
  Grade-2 elements of Cl(n,0) form the Lie algebra so(n) under commutator.

This file proves it concretely for Cl(3,0) → so(3):
  - Bivectors {e12, e13, e23} span a 3D subspace
  - The commutator [A,B] = AB - BA of pure bivectors is a pure bivector
  - The structure constants match so(3) exactly
  - The Jacobi identity holds
  - The Casimir C₂ = e12² + e13² + e23² = -3 · 1 in Cl(3,0)
  - The Casimir is nonzero (algebraic root of the spectral gap)

In the mass gap context:
  - The gauge group SO(n) arises from the Clifford algebra Cl(n,0)
  - The Casimir eigenvalue bounds representation energies from below
  - For so(14), C₂(fundamental) = 13/2, giving the conjectured spectral gap
  - This file establishes the foundation: so(n) FROM Cl(n,0)

Combined with lie_bridge.lean (which proves Cl(1,3) → so(1,3)):
  - lie_bridge.lean: signature (1,3) → Lorentz algebra (non-compact)
  - THIS FILE: signature (3,0) → rotation algebra (compact)
  - Compactness is REQUIRED for mass gap (all reps finite-dimensional)

References:
  - Lounesto, "Clifford Algebras and Spinors" (2001), Ch. 3
  - Gallier & Quaintance, "Differential Geometry and Lie Groups" (2020), Ch. 19
-/

import clifford.cl30

namespace Cl30

/-! ## Part 1: Pure Bivectors

A "pure bivector" in Cl(3,0) has only b12, b13, b23 components.
All other components (scalar, vectors, pseudoscalar) are zero.

In the mass gap context, the gauge field A_μ takes values in the
Lie algebra of the gauge group. For so(n), these are the bivectors
of Cl(n,0). The entire dynamics is built from these grade-2 elements. -/

/-- Predicate: an element of Cl(3,0) is a pure bivector. -/
def isPureBivector (x : Cl30) : Prop :=
  x.s = 0 ∧ x.v1 = 0 ∧ x.v2 = 0 ∧ x.v3 = 0 ∧ x.ps = 0

/-- Constructor: make a pure bivector from three components.
    The three components correspond to the three generators of so(3):
      a ↔ e12 (rotation in 12-plane)
      b ↔ e13 (rotation in 13-plane)
      c ↔ e23 (rotation in 23-plane) -/
def mkBivector (a b c : ℝ) : Cl30 :=
  ⟨0, 0, 0, 0, a, b, c, 0⟩

theorem mkBivector_isPureBivector (a b c : ℝ) :
    isPureBivector (mkBivector a b c) := by
  exact ⟨rfl, rfl, rfl, rfl, rfl⟩

/-- Any pure bivector can be expressed as mkBivector. -/
theorem isPureBivector_eq_mkBivector (x : Cl30) (h : isPureBivector x) :
    x = mkBivector x.b12 x.b13 x.b23 := by
  obtain ⟨hs, hv1, hv2, hv3, hps⟩ := h
  ext <;> simp [mkBivector, hs, hv1, hv2, hv3, hps]

/-- The basis bivectors are pure bivectors. -/
theorem e12_isPureBivector : isPureBivector e12 :=
  ⟨rfl, rfl, rfl, rfl, rfl⟩

theorem e13_isPureBivector : isPureBivector e13 :=
  ⟨rfl, rfl, rfl, rfl, rfl⟩

theorem e23_isPureBivector : isPureBivector e23 :=
  ⟨rfl, rfl, rfl, rfl, rfl⟩

/-! ## Part 2: The Commutator

The Lie bracket [A, B] = AB - BA in the Clifford algebra.
For any associative algebra, this satisfies:
  - Antisymmetry: [A, B] = -[B, A]
  - Jacobi identity: [A, [B, C]] + cyclic = 0

We define it and prove closure on bivectors. -/

/-- The commutator [A, B] = A*B - B*A in Cl(3,0). -/
def comm (A B : Cl30) : Cl30 := A * B + -(B * A)

/-- CLOSURE: The commutator of two pure bivectors is a pure bivector.

    This is the KEY structural result: grade-2 elements form a
    Lie SUBALGEBRA of Cl(3,0). They are closed under the Lie bracket.

    Algebraically: [grade 2, grade 2] ⊆ grade 2.

    This is the algebraic foundation of gauge theory. The gauge field
    lives in grade 2, and the field strength F = dA + [A,A] stays
    in grade 2 because of this closure. -/
theorem comm_pure_bivector (A B : Cl30)
    (hA : isPureBivector A) (hB : isPureBivector B) :
    isPureBivector (comm A B) := by
  obtain ⟨hAs, hAv1, hAv2, hAv3, hAps⟩ := hA
  obtain ⟨hBs, hBv1, hBv2, hBv3, hBps⟩ := hB
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
  simp only [comm, mul_def, add_def, neg_def, mul, add, neg,
    hAs, hAv1, hAv2, hAv3, hAps, hBs, hBv1, hBv2, hBv3, hBps] <;> ring

/-! ## Part 3: Structure Constants of so(3)

The commutator algebra of bivectors in Cl(3,0) has structure constants:
  [e12, e13] = -2·e23
  [e12, e23] =  2·e13
  [e13, e23] = -2·e12

With the rescaling L₁ = (1/2)e23, L₂ = (1/2)e13, L₃ = (1/2)e12,
these become [Lᵢ, Lⱼ] = εᵢⱼₖ Lₖ — exactly the structure constants
of so(3). The factor of 2 is the standard convention difference between
the Clifford commutator AB-BA and the Lie bracket (AB-BA)/2. -/

/-- Scalar multiplication for Cl(3,0). -/
def smul (r : ℝ) (x : Cl30) : Cl30 :=
  ⟨r*x.s, r*x.v1, r*x.v2, r*x.v3, r*x.b12, r*x.b13, r*x.b23, r*x.ps⟩

/-- [e12, e13] = -2·e23.
    In physics: rotating first in the 12-plane then the 13-plane,
    minus the reverse, gives rotation in the 23-plane. -/
theorem comm_e12_e13 : comm e12 e13 = smul (-2) e23 := by
  ext <;> simp [comm, e12, e13, e23, mul, add, neg, smul] <;> norm_num

/-- [e12, e23] = 2·e13. -/
theorem comm_e12_e23 : comm e12 e23 = smul 2 e13 := by
  ext <;> simp [comm, e12, e23, e13, mul, add, neg, smul] <;> norm_num

/-- [e13, e23] = -2·e12. -/
theorem comm_e13_e23 : comm e13 e23 = smul (-2) e12 := by
  ext <;> simp [comm, e13, e23, e12, mul, add, neg, smul] <;> norm_num

/-- The commutator of any bivector with itself is zero.
    [A, A] = AA - AA = 0. -/
theorem comm_self (A : Cl30) : comm A A = zero := by
  ext <;> simp [comm, mul_def, add_def, neg_def, mul, add, neg, zero] <;> ring

/-- Antisymmetry: [A, B] = -[B, A].
    Fundamental property of the Lie bracket. -/
theorem comm_antisymm (A B : Cl30) : comm A B = -(comm B A) := by
  ext <;> simp [comm, mul_def, add_def, neg_def, mul, add, neg] <;> ring

/-! ## Part 4: The Jacobi Identity

For all A, B, C in Cl(3,0):
  [A, [B, C]] + [B, [C, A]] + [C, [A, B]] = 0

This holds in ANY associative algebra under the commutator bracket.
The proof expands to 12 triple products which cancel pairwise by
associativity: ABC - ACB - BCA + CBA + BCA - BAC - CAB + ACB
+ CAB - CBA - ABC + BAC = 0.

Combined with closure (comm_pure_bivector), this proves:
  (bivectors of Cl(3,0), [·,·]) IS a Lie algebra = so(3). -/

set_option maxHeartbeats 1600000 in
/-- THE JACOBI IDENTITY for the Cl(3,0) commutator.

    [A, [B, C]] + [B, [C, A]] + [C, [A, B]] = 0

    This is the identity that makes (grade-2 elements, commutator)
    a Lie algebra. Combined with closure, this establishes:
      so(3) ≅ (bivectors of Cl(3,0), [·,·]) -/
theorem jacobi (A B C : Cl30) :
    comm A (comm B C) + comm B (comm C A) + comm C (comm A B)
    = zero := by
  ext <;> simp [comm, mul_def, add_def, neg_def, mul, add, neg, zero] <;> ring

/-! ## Part 5: Casimir Operator

The quadratic Casimir of so(3) measures the "total angular momentum."
In the Clifford algebra, it is the sum of squares of all generators:
  C₂ = e12² + e13² + e23²

Since each bivector squares to -1 in Cl(3,0), we get C₂ = -3·1.
The minus sign is a Clifford algebra convention; in REPRESENTATIONS,
the Casimir acts as a POSITIVE scalar:
  C₂|j⟩ = j(j+1)|j⟩  (with appropriate normalization)

The key point for the mass gap: C₂ > 0 for all NONTRIVIAL representations.
C₂ = 0 only for the trivial (1-dimensional) representation. This means
any state carrying gauge charge MUST have nonzero energy. -/

/-- The sum of squares of all bivector basis elements.
    Proportional to the Casimir operator of so(3). -/
def bivector_sum_of_squares : Cl30 := e12 * e12 + e13 * e13 + e23 * e23

/-- The bivector sum of squares equals -3·1.
    e12² + e13² + e23² = -3  (in the Clifford algebra)

    Each eij² = -1, so three of them sum to -3.
    In representation theory, this becomes +C₂ > 0 for nontrivial reps. -/
theorem bivector_sum_of_squares_val :
    bivector_sum_of_squares = smul (-3) (1 : Cl30) := by
  ext <;> simp [bivector_sum_of_squares, e12, e13, e23, mul, add, one, smul] <;> norm_num

/-- THE CASIMIR IS NONZERO.

    This is the algebraic root of the spectral gap.

    In representation theory:
      C₂ = 0  only for the trivial (1D) representation
      C₂ > 0  for ALL nontrivial representations

    For so(n) with standard normalization Tr(TₐTᵦ) = (1/2)δₐᵦ:
      C₂(fundamental of so(n)) = (n-1)/2
      C₂(fundamental of so(3))  = 1
      C₂(fundamental of so(14)) = 13/2

    The minimum nonzero Casimir eigenvalue provides a LOWER BOUND
    on the energy of any state in a nontrivial representation —
    the algebraic precursor to the mass gap. -/
theorem casimir_nonzero :
    bivector_sum_of_squares ≠ (0 : Cl30) := by
  intro h
  have := congr_arg Cl30.s h
  simp [bivector_sum_of_squares, e12, e13, e23, mul, add, zero] at this
  norm_num at this

/-- The Casimir is a SCALAR (central element) — it commutes with all bivectors.
    This is verified by showing its commutator with each generator vanishes.
    A central element acts as a scalar on each irreducible representation. -/
theorem casimir_commutes_e12 :
    comm bivector_sum_of_squares e12 = zero := by
  ext <;> simp [comm, bivector_sum_of_squares, e12, e13, e23,
    mul, add, neg, zero]

theorem casimir_commutes_e13 :
    comm bivector_sum_of_squares e13 = zero := by
  ext <;> simp [comm, bivector_sum_of_squares, e12, e13, e23,
    mul, add, neg, zero]

theorem casimir_commutes_e23 :
    comm bivector_sum_of_squares e23 = zero := by
  ext <;> simp [comm, bivector_sum_of_squares, e12, e13, e23,
    mul, add, neg, zero]

/-! ## Part 6: Grade Selection Rules

When a grade-2 element acts on a general Cl(3,0) element by commutator,
it preserves a grading structure:

  [grade 2, grade 0] = 0           (scalars commute with everything)
  [grade 2, grade 1] ⊆ grade 1    (rotations rotate vectors)
  [grade 2, grade 2] ⊆ grade 2    (closure, proved above)
  [grade 2, grade 3] = 0           (pseudoscalar is central in odd dim)

Note: in Cl(3,0), n=3 is odd, so the pseudoscalar e123 is central.
In even dimensions (e.g., Cl(14,0) for the mass gap), the pseudoscalar
does NOT commute with everything, and the selection rules differ. -/

/-- [grade 2, grade 0] = 0: a bivector commutes with any scalar multiple.
    Scalars are the "vacuum" — they carry no gauge charge. -/
theorem comm_bivector_scalar (B : Cl30) (hB : isPureBivector B) (r : ℝ) :
    comm B (smul r 1) = zero := by
  obtain ⟨hBs, hBv1, hBv2, hBv3, hBps⟩ := hB
  ext <;> simp [comm, smul, mul_def, add_def, neg_def, mul, add, neg, one, zero,
    hBs, hBv1, hBv2, hBv3, hBps] <;> ring

/-- [grade 2, grade 1] ⊆ grade 1: commutator of bivector with vector is a vector.
    This is "rotations rotate vectors" — the fundamental representation of so(3).

    For the mass gap: this shows gauge fields ACT ON matter fields.
    The action stays within the matter field's grade. -/
theorem comm_bivector_vector_is_vector (B V : Cl30)
    (hB : isPureBivector B)
    (hV : V.s = 0 ∧ V.b12 = 0 ∧ V.b13 = 0 ∧ V.b23 = 0 ∧ V.ps = 0) :
    let W := comm B V
    W.s = 0 ∧ W.b12 = 0 ∧ W.b13 = 0 ∧ W.b23 = 0 ∧ W.ps = 0 := by
  obtain ⟨hBs, hBv1, hBv2, hBv3, hBps⟩ := hB
  obtain ⟨hVs, hVb12, hVb13, hVb23, hVps⟩ := hV
  simp only
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
  simp only [comm, mul_def, add_def, neg_def, mul, add, neg,
    hBs, hBv1, hBv2, hBv3, hBps, hVs, hVb12, hVb13, hVb23, hVps] <;> ring

/-- [grade 2, grade 3] = 0 in Cl(3,0): bivectors commute with the pseudoscalar.
    This is specific to ODD dimension (n=3): e123 is central.
    In Cl(14,0) (even n), this does NOT hold. -/
theorem comm_bivector_pseudoscalar (B : Cl30) (hB : isPureBivector B) :
    comm B e123 = zero := by
  obtain ⟨hBs, hBv1, hBv2, hBv3, hBps⟩ := hB
  ext <;> simp [comm, e123, mul_def, add_def, neg_def, mul, add, neg, zero,
    hBs, hBv1, hBv2, hBv3, hBps] <;> ring

/-! ## Part 7: Dimension Count

so(n) has dimension n(n-1)/2.
For so(3): dim = 3·2/2 = 3. Our bivector space has 3 generators: e12, e13, e23. ✓
For so(14): dim = 14·13/2 = 91. The Cl(14,0) bivector space has C(14,2) = 91 generators. ✓

This is not a coincidence — it is the DEFINITION of so(n) in terms of
antisymmetric matrices (or equivalently, grade-2 Clifford elements). -/

/-- The three basis bivectors span the full bivector space.
    Any pure bivector is a linear combination of e12, e13, e23.
    This gives dim(so(3)) = 3 = 3·2/2. -/
theorem bivector_span (x : Cl30) (h : isPureBivector x) :
    x = Cl30.add (Cl30.add (smul x.b12 e12) (smul x.b13 e13)) (smul x.b23 e23) := by
  obtain ⟨hs, hv1, hv2, hv3, hps⟩ := h
  ext <;> simp [smul, e12, e13, e23, add, hs, hv1, hv2, hv3, hps]

end Cl30

/-!
## Summary: Grade-2 Elements of Cl(3,0) Form so(3)

### Theorems proved (0 sorry):

1. **Closure** (`comm_pure_bivector`):
   [grade 2, grade 2] ⊆ grade 2

2. **Structure constants**:
   [e12,e13] = -2e23,  [e12,e23] = 2e13,  [e13,e23] = -2e12
   Matches so(3) with Lᵢ = (1/2)eⱼₖ

3. **Jacobi identity** (`jacobi`):
   [A,[B,C]] + [B,[C,A]] + [C,[A,B]] = 0

4. **Casimir** (`bivector_sum_of_squares_val`):
   C₂ = e12² + e13² + e23² = -3·1

5. **Nonzero Casimir** (`casimir_nonzero`):
   C₂ ≠ 0, the algebraic root of the spectral gap

6. **Casimir centrality** (`casimir_commutes_*`):
   [C₂, eᵢⱼ] = 0 for all generators

7. **Grade selection rules**:
   [grade 2, grade k] ⊆ grade k for k = 0, 1, 2, 3

### The mass gap connection:

The gauge algebra so(n) emerges FROM the Clifford algebra Cl(n,0)
via the grade-2 commutator closure. The Casimir eigenvalue is
determined by algebraic structure alone. For ANY compact non-abelian
gauge group, C₂(fund) > 0, providing a LOWER BOUND on energies
in nontrivial representations.

The mass gap is the statement that this algebraic lower bound
survives quantization — that the quantum Hamiltonian inherits
the spectral gap from the classical Casimir structure.

### Connection to the hierarchy:

  Cl(3,0) → so(3)     [THIS FILE: 3 generators, compact]
  Cl(1,3) → so(1,3)   [lie_bridge.lean: 6 generators, non-compact]
  Cl(14,0) → so(14)   [GOAL: 91 generators, compact]

### Next: `casimir_eigenvalues.lean`

Compute C₂ eigenvalues for representations of so(n).
Key result: C₂(fundamental of so(n)) = (n-1)/2.
For so(14): C₂(fund) = 13/2 = the conjectured spectral gap lower bound.
-/
