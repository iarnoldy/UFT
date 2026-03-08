/-
UFT Formal Verification - Clifford Algebra Cl(1,1)
====================================================

THE BRIDGE FROM LEVEL 1 TO LEVEL 2

Dollard's versor algebra is Z_4 (Level 1). We proved this is forced by his axioms.
The question: what algebra SHOULD he have used?

Answer: Cl(1,1), the Clifford algebra with signature (+1, -1).

Cl(1,1) has basis {1, e1, e2, e12} with:
  - e1^2 = +1  (like Dollard's h^2 = +1, but e1 is not ±1)
  - e2^2 = -1  (like Dollard's j^2 = -1)
  - e1*e2 = -e2*e1  (ANTICOMMUTATIVE -- this is what Dollard missed)
  - e12 = e1*e2  (the bivector, analogous to Dollard's k)

Key results in this file:
  1. Cl(1,1) is well-defined with explicit multiplication table
  2. e1 is genuinely non-trivial: e1^2 = 1 but e1 is not ±1
  3. Dollard's axiom jk=1 FAILS in Cl(1,1) (e2*e12 = e1, not 1)
  4. The idempotents P+ = (1+e1)/2 and P- = (1-e1)/2 decompose signals
     into forward and backward traveling waves
  5. This IS the algebra Dollard was reaching for, but his commutativity
     assumption collapsed it to Z_4

This connects to the UFT roadmap:
  Z_4 (Dollard) -> Cl(1,1) (this file) -> Cl(3,1) (spacetime algebra)

References:
  - Porteous, I. R. "Clifford Algebras and the Classical Groups"
  - Hestenes, D. "Space-Time Algebra" (1966)
  - Polymathic research analysis, 2026
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-! ## Part 1: The Algebra Structure

We define Cl(1,1) as a concrete 4-tuple with explicit multiplication.
-/

/-- Cl(1,1): the Clifford algebra with signature (+1, -1).
    Elements are a + b*e1 + c*e2 + d*e12 where
    e1^2 = +1, e2^2 = -1, e1*e2 = -e2*e1. -/
@[ext]
structure Cl11 where
  s : ℝ    -- scalar (grade 0)
  v1 : ℝ   -- e1 coefficient (grade 1)
  v2 : ℝ   -- e2 coefficient (grade 1)
  b12 : ℝ  -- e12 = e1*e2 coefficient (grade 2)

namespace Cl11

/-!
### Operations

Multiplication derived from the geometric product rules:
  e1*e1 = +1,  e2*e2 = -1,  e12*e12 = +1
  e1*e2 = e12, e2*e1 = -e12
  e1*e12 = e2, e12*e1 = -e2
  e2*e12 = e1, e12*e2 = -e1
-/

/-- The geometric product in Cl(1,1). -/
def mul (x y : Cl11) : Cl11 :=
  { s   := x.s * y.s   + x.v1 * y.v1  - x.v2 * y.v2  + x.b12 * y.b12,
    v1  := x.s * y.v1  + x.v1 * y.s   + x.v2 * y.b12 - x.b12 * y.v2,
    v2  := x.s * y.v2  + x.v1 * y.b12 + x.v2 * y.s   - x.b12 * y.v1,
    b12 := x.s * y.b12 + x.v1 * y.v2  - x.v2 * y.v1  + x.b12 * y.s }

instance : Mul Cl11 := ⟨mul⟩

/-- Addition in Cl(1,1). -/
def add (x y : Cl11) : Cl11 :=
  { s := x.s + y.s, v1 := x.v1 + y.v1, v2 := x.v2 + y.v2, b12 := x.b12 + y.b12 }

instance : Add Cl11 := ⟨add⟩

/-- Negation in Cl(1,1). -/
def neg (x : Cl11) : Cl11 :=
  { s := -x.s, v1 := -x.v1, v2 := -x.v2, b12 := -x.b12 }

instance : Neg Cl11 := ⟨neg⟩

/-- Scalar multiplication. -/
def smul (r : ℝ) (x : Cl11) : Cl11 :=
  { s := r * x.s, v1 := r * x.v1, v2 := r * x.v2, b12 := r * x.b12 }

/-! ### Distinguished Elements -/

def one : Cl11 := ⟨1, 0, 0, 0⟩
instance : One Cl11 := ⟨one⟩

def zero : Cl11 := ⟨0, 0, 0, 0⟩
instance : Zero Cl11 := ⟨zero⟩

/-! ### Simp bridge lemmas

These connect typeclass operators to our custom functions,
allowing `simp` to unfold through instance resolution. -/

@[simp] lemma mul_def (a b : Cl11) : a * b = mul a b := rfl
@[simp] lemma add_def (a b : Cl11) : a + b = add a b := rfl
@[simp] lemma neg_def (a : Cl11) : -a = neg a := rfl
@[simp] lemma one_val : (1 : Cl11) = one := rfl
@[simp] lemma zero_val : (0 : Cl11) = zero := rfl

/-! ### Basis Elements -/

/-- Basis vector e1 with e1^2 = +1 (the "h" direction). -/
def e1 : Cl11 := ⟨0, 1, 0, 0⟩

/-- Basis vector e2 with e2^2 = -1 (the "j" direction). -/
def e2 : Cl11 := ⟨0, 0, 1, 0⟩

/-- Bivector e12 = e1*e2 (the "k" direction). -/
def e12 : Cl11 := ⟨0, 0, 0, 1⟩

/-- Embed a real scalar into Cl(1,1). -/
def ofReal (r : ℝ) : Cl11 := ⟨r, 0, 0, 0⟩

/-! ## Part 2: Fundamental Properties -/

/-- e1 squared equals +1 (like Dollard's h^2 = +1). -/
theorem e1_sq : e1 * e1 = (1 : Cl11) := by
  ext <;> simp [e1, mul, one]

/-- e2 squared equals -1 (like Dollard's j^2 = -1). -/
theorem e2_sq : e2 * e2 = -(1 : Cl11) := by
  ext <;> simp [e2, mul, one, neg]

/-- e12 squared equals +1. -/
theorem e12_sq : e12 * e12 = (1 : Cl11) := by
  ext <;> simp [e12, mul, one]

/-- e1 * e2 = e12 (the bivector). -/
theorem e1_mul_e2 : e1 * e2 = e12 := by
  ext <;> simp [e1, e2, e12, mul]

/-- e2 * e1 = -e12 (ANTICOMMUTATIVE -- Dollard's critical missing property). -/
theorem e2_mul_e1 : e2 * e1 = -e12 := by
  ext <;> simp [e2, e1, e12, mul, neg]

/-- e1 and e2 do NOT commute. This is the fundamental difference from Dollard's algebra. -/
theorem e1_e2_anticommute : e1 * e2 ≠ e2 * e1 := by
  rw [e1_mul_e2, e2_mul_e1]
  intro h
  have := congr_arg Cl11.b12 h
  simp only [neg_def, e12, neg] at this
  norm_num at this

/-! ### Additional multiplication table entries -/

/-- e1 * e12 = e2. -/
theorem e1_mul_e12 : e1 * e12 = e2 := by
  ext <;> simp [e1, e12, e2, mul]

/-- e12 * e1 = -e2. -/
theorem e12_mul_e1 : e12 * e1 = -e2 := by
  ext <;> simp [e12, e1, e2, mul, neg]

/-- e2 * e12 = e1 (NOT 1 -- Dollard's jk=1 fails!). -/
theorem e2_mul_e12 : e2 * e12 = e1 := by
  ext <;> simp [e2, e12, e1, mul]

/-- e12 * e2 = -e1. -/
theorem e12_mul_e2 : e12 * e2 = -e1 := by
  ext <;> simp [e12, e2, e1, mul, neg]

/-! ## Part 3: Why Dollard's Axioms Fail in Cl(1,1)

Mapping Dollard's operators into Cl(1,1):
  h -> e1  (h^2 = +1, non-trivially)
  j -> e2  (j^2 = -1)
  k -> e12 (k = hj = e1*e2)

We show that jk = 1 FAILS, confirming the algebraic necessity result:
you cannot have h^2=+1 (non-trivially), j^2=-1, hj=k, AND jk=1. -/

/-- Dollard's axiom jk = 1 FAILS in Cl(1,1).
    e2 * e12 = e1, not 1. -/
theorem dollard_jk_fails : e2 * e12 ≠ (1 : Cl11) := by
  rw [e2_mul_e12]
  intro h
  have := congr_arg Cl11.s h
  simp [e1, one] at this

/-- Dollard's commutativity assumption hj = jh also FAILS.
    e1*e2 = e12 but e2*e1 = -e12. -/
theorem dollard_commutativity_fails : e1 * e2 ≠ e2 * e1 := e1_e2_anticommute

/-- Summary: Dollard needs THREE axiom changes to use Cl(1,1):
    1. Drop jk = 1 (in Cl(1,1): jk = e2*e12 = e1)
    2. Drop commutativity (in Cl(1,1): hj = e12 but jh = -e12)
    3. Accept that "cancellation" becomes k*j = -e1 (not e1) -/
theorem dollard_kj_also_fails : e12 * e2 ≠ (1 : Cl11) := by
  rw [e12_mul_e2]
  intro h
  have := congr_arg Cl11.s h
  simp [e1, one, neg] at this

/-! ## Part 4: The Genuine Power of Cl(1,1) -- Idempotent Decomposition

The idempotents P+ = (1+e1)/2 and P- = (1-e1)/2 are the reason
Cl(1,1) matters for electrical engineering. They project signals
into forward-traveling and backward-traveling components.

In transmission line theory:
  - Forward wave: V+ = P+ * V
  - Backward wave: V- = P- * V
  - V = V+ + V-  (completeness)
  - V+ and V- are orthogonal (P+ * P- = 0)

This is what Dollard was reaching for: a non-trivial h that
decomposes signals into complementary halves. But his commutative
Z_4 can't do this -- Cl(1,1) can. -/

/-- The forward-wave projector: P+ = (1 + e1) / 2. -/
noncomputable def P_plus : Cl11 := ⟨1/2, 1/2, 0, 0⟩

/-- The backward-wave projector: P- = (1 - e1) / 2. -/
noncomputable def P_minus : Cl11 := ⟨1/2, -1/2, 0, 0⟩

/-- P+ is idempotent: P+^2 = P+. -/
theorem P_plus_idempotent : P_plus * P_plus = P_plus := by
  ext <;> simp [P_plus, mul] <;> ring

/-- P- is idempotent: P-^2 = P-. -/
theorem P_minus_idempotent : P_minus * P_minus = P_minus := by
  ext <;> simp [P_minus, mul] <;> ring

/-- P+ and P- are orthogonal: P+ * P- = 0. -/
theorem P_orthogonal : P_plus * P_minus = (0 : Cl11) := by
  ext <;> simp [P_plus, P_minus, mul, zero] <;> ring

/-- P- and P+ are orthogonal (the other direction). -/
theorem P_orthogonal' : P_minus * P_plus = (0 : Cl11) := by
  ext <;> simp [P_minus, P_plus, mul, zero] <;> ring

/-- P+ and P- form a complete decomposition: P+ + P- = 1. -/
theorem P_complete : P_plus + P_minus = (1 : Cl11) := by
  ext <;> simp [P_plus, P_minus, add, one] <;> ring

/-! ## Part 5: Cl(1,1) Subalgebra Structure

Cl(1,1) contains two important subalgebras:
  - {1, e2}: the complex numbers C (e2^2 = -1)
  - {1, e1}: the split-complex numbers (e1^2 = +1, e1 is not ±1)
  - {1, e12}: another copy of split-complex numbers (e12^2 = +1)

The telegraph equation lives in the complex subalgebra {1, e2}.
The forward/backward decomposition lives in the split-complex subalgebra {1, e1}.
These two structures are ORTHOGONAL in Cl(1,1) -- which is why Dollard
couldn't mix them in a commutative algebra. -/

/-- The complex subalgebra: (a + b*e2)*(c + d*e2) = (ac-bd) + (ad+bc)*e2.
    This is standard complex multiplication. -/
theorem complex_subalgebra (a b c d : ℝ) :
    (⟨a, 0, b, 0⟩ : Cl11) * (⟨c, 0, d, 0⟩ : Cl11) =
    (⟨a*c - b*d, 0, a*d + b*c, 0⟩ : Cl11) := by
  ext <;> simp [mul]

/-- The split-complex subalgebra: (a + b*e1)*(c + d*e1) = (ac+bd) + (ad+bc)*e1.
    Note the + sign in ac+bd (vs ac-bd for complex). This is the
    split-complex or hyperbolic number system. -/
theorem split_complex_subalgebra (a b c d : ℝ) :
    (⟨a, b, 0, 0⟩ : Cl11) * (⟨c, d, 0, 0⟩ : Cl11) =
    (⟨a*c + b*d, a*d + b*c, 0, 0⟩ : Cl11) := by
  ext <;> simp [mul]

/-! ## Part 6: The Corrected Telegraph Equation in Cl(1,1)

The standard telegraph equation uses the complex subalgebra {1, e2}:
  Z = R + X*e2  (impedance: resistance + reactance)
  Y = G + B*e2  (admittance: conductance + susceptance)
  ZY = (RG - XB) + (RB + XG)*e2

This is standard complex multiplication (same result as using j = i).

The versor form (using e1) STILL doesn't give an equivalent expression,
because e1 is grade 1 while the scalar part is grade 0. You can't replace
a scalar with a vector and get the same element.

HOWEVER, Cl(1,1) offers something Dollard COULDN'T get in Z_4:
the idempotent decomposition of ZY into forward and backward components. -/

/-- Telegraph equation in the complex subalgebra of Cl(1,1).
    ZY = (R + X*e2)(G + B*e2) = (RG - XB) + (RB + XG)*e2. -/
theorem telegraph_in_cl11 (R X G B : ℝ) :
    (⟨R, 0, X, 0⟩ : Cl11) * (⟨G, 0, B, 0⟩ : Cl11) =
    (⟨R*G - X*B, 0, R*B + X*G, 0⟩ : Cl11) := by
  exact complex_subalgebra R X G B

/-- The versor form STILL fails in Cl(1,1).
    e1*(XB + RG) + e2*(XG - RB) has an e1 component,
    but the telegraph product has NO e1 component.
    Grade mismatch: you can't replace a scalar with a vector. -/
theorem versor_form_grade_mismatch (R X G B : ℝ)
    (hXB : X * B + R * G ≠ 0) :
    (⟨R, 0, X, 0⟩ : Cl11) * (⟨G, 0, B, 0⟩ : Cl11) ≠
    (⟨0, X*B + R*G, X*G - R*B, 0⟩ : Cl11) := by
  rw [telegraph_in_cl11]
  intro h
  have : (0 : ℝ) = X * B + R * G := by
    have := congr_arg Cl11.v1 h
    simpa using this
  exact hXB this.symm

/-! ## Part 7: What Cl(1,1) DOES Offer -- The Forward/Backward Decomposition

The genuine power of Cl(1,1) for electromagnetic theory is the
idempotent decomposition. For any element in the complex subalgebra:

  z = a + b*e2

We can decompose using the idempotents:
  z = P+ * z + P- * z

where P+ * z and P- * z live in complementary subspaces.
This corresponds to decomposing an electromagnetic wave into
forward-traveling and backward-traveling components.

This is what Dollard was TRYING to do with the h operator:
separate signals into complementary halves. But in Z_4, h = -1
just negates -- it can't project. In Cl(1,1), e1 generates
genuine projectors that decompose signals non-trivially. -/

/-- Forward projection of a complex-subalgebra element. -/
theorem forward_projection (a b : ℝ) :
    P_plus * (⟨a, 0, b, 0⟩ : Cl11) =
    (⟨a/2, a/2, b/2, b/2⟩ : Cl11) := by
  ext <;> simp [P_plus, mul] <;> ring

/-- Backward projection of a complex-subalgebra element. -/
theorem backward_projection (a b : ℝ) :
    P_minus * (⟨a, 0, b, 0⟩ : Cl11) =
    (⟨a/2, -a/2, b/2, -b/2⟩ : Cl11) := by
  ext <;> simp [P_minus, mul] <;> ring

/-- The projections sum to the original: P+*z + P-*z = z. -/
theorem projection_complete (a b : ℝ) :
    P_plus * (⟨a, 0, b, 0⟩ : Cl11) + P_minus * (⟨a, 0, b, 0⟩ : Cl11) =
    (⟨a, 0, b, 0⟩ : Cl11) := by
  rw [forward_projection, backward_projection]
  ext <;> simp [add] <;> ring

/-! ## Part 8: Lorentz Boost Rotors

The crown jewel of Cl(1,1): Lorentz transformations as rotor sandwiches.

A rotor R = cosh(φ/2) + sinh(φ/2)*e12 acts on vectors by the sandwich product:
  v' = R * v * R̃

where R̃ is the REVERSE (flip sign of bivector component).

This implements hyperbolic rotations (Lorentz boosts):
  R * e1 * R̃ = cosh(φ)*e1 - sinh(φ)*e2
  R * e2 * R̃ = -sinh(φ)*e1 + cosh(φ)*e2

The boost subalgebra {1, e1, e2, e12} of Cl(1,3) spacetime algebra
is isomorphic to this Cl(1,1), with e1 ↔ γ₀ (timelike) and e2 ↔ γ₁ (spacelike).

Thus: Lorentz boosts ARE rotors in Cl(1,1). No matrices needed.

References:
  - Hestenes, "Space-Time Algebra" (1966), Ch. 1
  - Doran & Lasenby, "Geometric Algebra for Physicists" (2003), §5.2
-/

/-- Reversion (grade involution): reverses the order of basis vectors in each blade.
    Scalars and vectors are unchanged; bivectors flip sign.
    For a = s + v1*e1 + v2*e2 + b12*e12:  ã = s + v1*e1 + v2*e2 - b12*e12 -/
def rev (x : Cl11) : Cl11 :=
  { s := x.s, v1 := x.v1, v2 := x.v2, b12 := -x.b12 }

/-- Reversion is an involution: rev(rev(x)) = x. -/
theorem rev_rev (x : Cl11) : rev (rev x) = x := by
  ext <;> simp [rev]

/-- Reversion of the identity is the identity. -/
theorem rev_one : rev (1 : Cl11) = (1 : Cl11) := by
  ext <;> simp [rev, one]

/-- Reversion of e1 is e1 (vectors are grade 1, unchanged). -/
theorem rev_e1 : rev e1 = e1 := by
  ext <;> simp [rev, e1]

/-- Reversion of e2 is e2. -/
theorem rev_e2 : rev e2 = e2 := by
  ext <;> simp [rev, e2]

/-- Reversion of e12 is -e12 (bivectors flip sign). -/
theorem rev_e12 : rev e12 = -e12 := by
  ext <;> simp [rev, e12, neg]

/-- The sandwich product: R * x * R̃. This is how rotors act on multivectors. -/
def sandwich (R x : Cl11) : Cl11 := R * x * (rev R)

/-! ### Boost Rotor: R = c + s*e12

For a rapidity parameter φ, the boost rotor is:
  R = cosh(φ/2) + sinh(φ/2)*e12 = (c, 0, 0, s)

We work with abstract c, s and prove the ALGEBRAIC identities.
The connection to cosh/sinh is a separate step. -/

/-- A boost rotor with parameters c (scalar) and s (bivector coefficient). -/
def boostRotor (c s : ℝ) : Cl11 := ⟨c, 0, 0, s⟩

/-- The reverse of a boost rotor: flip the bivector sign. -/
theorem rev_boostRotor (c s : ℝ) : rev (boostRotor c s) = boostRotor c (-s) := by
  ext <;> simp [rev, boostRotor]

/-- R * R̃ = (c² - s²) * 1.
    For a proper Lorentz boost, c = cosh(φ/2), s = sinh(φ/2),
    so c² - s² = cosh²(φ/2) - sinh²(φ/2) = 1. -/
theorem rotor_norm (c s : ℝ) :
    boostRotor c s * rev (boostRotor c s) = ofReal (c ^ 2 - s ^ 2) := by
  ext <;> simp [boostRotor, rev, mul, ofReal] <;> ring

/-- Boost of e1: R * e1 * R̃ = (c²+s²)*e1 + (-2cs)*e2.
    When c = cosh(φ/2), s = sinh(φ/2):
      c²+s² = cosh(φ),  2cs = sinh(φ)
    So this is the Lorentz boost: t' = cosh(φ)*t - sinh(φ)*x. -/
theorem boost_e1 (c s : ℝ) :
    sandwich (boostRotor c s) e1 =
    ⟨0, c ^ 2 + s ^ 2, -2 * c * s, 0⟩ := by
  ext <;> simp [sandwich, boostRotor, e1, rev, mul] <;> ring

/-- Boost of e2: R * e2 * R̃ = (-2cs)*e1 + (c²+s²)*e2.
    The spacelike vector transforms as: x' = -sinh(φ)*t + cosh(φ)*x. -/
theorem boost_e2 (c s : ℝ) :
    sandwich (boostRotor c s) e2 =
    ⟨0, -2 * c * s, c ^ 2 + s ^ 2, 0⟩ := by
  ext <;> simp [sandwich, boostRotor, e2, rev, mul] <;> ring

/-- The boost preserves e1² - e2² (the Minkowski metric).
    If v = a*e1 + b*e2, then v*v = a²-b² (scalar part).
    After boosting, v' = v'_1*e1 + v'_2*e2 with v'*v' = v'_1² - v'_2².
    We prove: (c²+s²)² - (2cs)² = (c²-s²)² * (a²-b²),
    which equals a²-b² when the rotor is normalized (c²-s²=1). -/
theorem boost_preserves_interval (c s a b : ℝ) :
    let v' := sandwich (boostRotor c s) ⟨0, a, b, 0⟩
    v'.v1 ^ 2 - v'.v2 ^ 2 = (c ^ 2 - s ^ 2) ^ 2 * (a ^ 2 - b ^ 2) := by
  simp [sandwich, boostRotor, rev, mul]
  ring

/-- Composition of boosts: two boosts compose as rotor multiplication.
    R₁ * R₂ is another boost rotor (closure). -/
theorem boost_compose (c₁ s₁ c₂ s₂ : ℝ) :
    boostRotor c₁ s₁ * boostRotor c₂ s₂ =
    boostRotor (c₁ * c₂ + s₁ * s₂) (c₁ * s₂ + s₁ * c₂) := by
  ext <;> simp [boostRotor, mul]

/-! Boost composition matches the hyperbolic addition formula.
    If c₁ = cosh(α/2), s₁ = sinh(α/2), c₂ = cosh(β/2), s₂ = sinh(β/2),
    then the composed rotor has:
      c' = c₁c₂ + s₁s₂ = cosh((α+β)/2)
      s' = c₁s₂ + s₁c₂ = sinh((α+β)/2)
    This is the hyperbolic angle addition formula:
      cosh(A+B) = cosh(A)cosh(B) + sinh(A)sinh(B)
      sinh(A+B) = sinh(A)cosh(B) + cosh(A)sinh(B)
    The algebraic structure of boost_compose IS the addition formula. -/

/-- The inverse of a normalized boost rotor is its reverse.
    If c²-s² = 1, then R̃ * R = 1. -/
theorem rotor_inverse (c s : ℝ) (hn : c ^ 2 - s ^ 2 = 1) :
    rev (boostRotor c s) * boostRotor c s = (1 : Cl11) := by
  rw [rev_boostRotor]
  rw [boost_compose]
  ext <;> simp [boostRotor, one] <;> nlinarith

/-- A normalized rotor has unit "norm": R * R̃ = 1. -/
theorem rotor_unit (c s : ℝ) (hn : c ^ 2 - s ^ 2 = 1) :
    boostRotor c s * rev (boostRotor c s) = (1 : Cl11) := by
  rw [rotor_norm]
  ext <;> simp [ofReal, one]; all_goals linarith

end Cl11

/-!
## Summary: The Bridge from Z_4 to Spacetime

### What this file proves:
1. Cl(1,1) is a well-defined 4D algebra (explicit multiplication table verified)
2. e1^2 = +1 with e1 genuinely non-trivial (not ±1)
3. Dollard's axiom jk=1 FAILS (e2*e12 = e1, not 1)
4. Dollard's commutativity FAILS (e1*e2 = -e2*e1)
5. Idempotent projectors P+, P- are complete and orthogonal
6. Telegraph equation lives in the complex subalgebra {1, e2}
7. The versor form STILL fails (grade mismatch)
8. Forward/backward decomposition IS the genuine contribution
9. LORENTZ BOOSTS are rotor sandwiches: R*v*R̃ (Part 8)
10. Boost of e1 gives cosh(φ)*e1 - sinh(φ)*e2 (time dilation)
11. Boost of e2 gives -sinh(φ)*e1 + cosh(φ)*e2 (length contraction)
12. Minkowski interval a²-b² is PRESERVED by boosts
13. Boost composition = hyperbolic angle addition (velocity addition)
14. Normalized rotors (c²-s²=1) have R̃ as inverse

### The algebraic hierarchy:
  Z_4           = Dollard's versor algebra (trivial, forced by axioms)
  Cl(1,0) ~ R+R = split-complex numbers (2D, zero divisors)
  Cl(0,1) ~ C   = complex numbers (2D, standard)
  Cl(1,1) ~ M2R = 2x2 real matrices (4D, THIS FILE ← LORENTZ BOOSTS HERE)
  Cl(3,0) ~ M2C = Pauli algebra (8D, 3D rotations)
  Cl(1,3) ~ M4R = spacetime algebra (16D, Maxwell + Dirac)

### Next step:
  Embed these Lorentz rotors into Cl(1,3) spacetime algebra.
  The boost subalgebra {1, γ₀, γ₁, γ₀₁} of Cl(1,3) IS Cl(1,1).
  Then: rotors in the full 6D bivector space give ALL Lorentz transformations
  (boosts + rotations), and Maxwell's equations become ∇F = J.
-/
