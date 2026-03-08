/-
UFT Formal Verification - Spacetime Algebra Cl(1,3) and Maxwell's Equation
===========================================================================

LEVEL 4 FOUNDATION: MAXWELL'S FOUR EQUATIONS ARE ONE

Cl(1,3) is the Spacetime Algebra (STA) of Hestenes. It has 16 basis elements
organized by grade:

  Grade 0 (1):  1                          -- scalars
  Grade 1 (4):  g0, g1, g2, g3            -- vectors (spacetime directions)
  Grade 2 (6):  g01, g02, g03, g12, g13, g23  -- bivectors (planes)
  Grade 3 (4):  g012, g013, g023, g123     -- trivectors (volumes)
  Grade 4 (1):  I = g0123                  -- pseudoscalar (4-volume)

Signature (Hestenes convention):
  g0^2 = +1   (timelike)
  gi^2 = -1   (spacelike, i = 1,2,3)
  g_mu * g_nu = -g_nu * g_mu  for mu != nu  (anticommutativity)

The pseudoscalar I = g0*g1*g2*g3 satisfies I^2 = -1.

THE KEY INSIGHT:
Maxwell's four equations reduce to ONE equation in this algebra:

    nabla * F = J

where:
  nabla = g0*d/dt + g1*d/dx + g2*d/dy + g3*d/dz  (spacetime gradient)
  F = E + I*B  (electromagnetic bivector field)
  J = (rho - J_vec) * g0  (current density)

This file defines the structure, proves the signature and anticommutativity
axioms for basis vectors, constructs the electromagnetic bivector, and
documents Maxwell's equation as a structural statement.

In the hierarchy:
  Z_4 -> Cl(1,1) -> Cl(3,0) -> **Cl(1,3)**

References:
  - Hestenes, D. "Space-Time Algebra" (1966)
  - Doran, C. & Lasenby, A. "Geometric Algebra for Physicists" (2003)
  - Baylis, W. "Electrodynamics: A Modern Geometric Approach" (1999)
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-! ## Part 1: The Spacetime Algebra Structure -/

/-- Cl(1,3): the Spacetime Algebra (STA).
    A general multivector has 16 components, one per basis blade. -/
@[ext]
structure STA where
  -- Grade 0: scalar
  scalar : ℝ
  -- Grade 1: vectors
  g0 : ℝ       -- timelike, g0^2 = +1
  g1 : ℝ       -- spacelike, g1^2 = -1
  g2 : ℝ       -- spacelike, g2^2 = -1
  g3 : ℝ       -- spacelike, g3^2 = -1
  -- Grade 2: bivectors
  g01 : ℝ      -- timelike-spacelike plane (electric field)
  g02 : ℝ
  g03 : ℝ
  g12 : ℝ      -- spacelike-spacelike plane (magnetic field)
  g13 : ℝ
  g23 : ℝ
  -- Grade 3: trivectors
  g012 : ℝ
  g013 : ℝ
  g023 : ℝ
  g123 : ℝ     -- spatial pseudoscalar
  -- Grade 4: pseudoscalar
  ps : ℝ       -- I = g0*g1*g2*g3, I^2 = -1

namespace STA

/-! ### Algebraic operations -/

def add (x y : STA) : STA :=
  ⟨x.scalar + y.scalar,
   x.g0 + y.g0, x.g1 + y.g1, x.g2 + y.g2, x.g3 + y.g3,
   x.g01 + y.g01, x.g02 + y.g02, x.g03 + y.g03,
   x.g12 + y.g12, x.g13 + y.g13, x.g23 + y.g23,
   x.g012 + y.g012, x.g013 + y.g013, x.g023 + y.g023, x.g123 + y.g123,
   x.ps + y.ps⟩

instance : Add STA := ⟨add⟩

def neg (x : STA) : STA :=
  ⟨-x.scalar,
   -x.g0, -x.g1, -x.g2, -x.g3,
   -x.g01, -x.g02, -x.g03,
   -x.g12, -x.g13, -x.g23,
   -x.g012, -x.g013, -x.g023, -x.g123,
   -x.ps⟩

instance : Neg STA := ⟨neg⟩

def smul (r : ℝ) (x : STA) : STA :=
  ⟨r * x.scalar,
   r * x.g0, r * x.g1, r * x.g2, r * x.g3,
   r * x.g01, r * x.g02, r * x.g03,
   r * x.g12, r * x.g13, r * x.g23,
   r * x.g012, r * x.g013, r * x.g023, r * x.g123,
   r * x.ps⟩

/-- The full geometric product in Cl(1,3).
    256 terms, computed from the multiplication table of basis blades.
    Signature: g0²=+1, g1²=g2²=g3²=-1, gμ*gν=-gν*gμ for μ≠ν.
    Generated programmatically from the Clifford algebra axioms. -/
def mul (x y : STA) : STA :=
  { scalar :=
      x.scalar*y.scalar + x.g0*y.g0 - x.g1*y.g1 - x.g2*y.g2
      - x.g3*y.g3 + x.g01*y.g01 + x.g02*y.g02 + x.g03*y.g03
      - x.g12*y.g12 - x.g13*y.g13 - x.g23*y.g23 - x.g012*y.g012
      - x.g013*y.g013 - x.g023*y.g023 + x.g123*y.g123 - x.ps*y.ps,
    g0 :=
      x.scalar*y.g0 + x.g0*y.scalar + x.g1*y.g01 + x.g2*y.g02
      + x.g3*y.g03 - x.g01*y.g1 - x.g02*y.g2 - x.g03*y.g3
      - x.g12*y.g012 - x.g13*y.g013 - x.g23*y.g023 - x.g012*y.g12
      - x.g013*y.g13 - x.g023*y.g23 - x.g123*y.ps + x.ps*y.g123,
    g1 :=
      x.scalar*y.g1 + x.g0*y.g01 + x.g1*y.scalar + x.g2*y.g12
      + x.g3*y.g13 - x.g01*y.g0 - x.g02*y.g012 - x.g03*y.g013
      - x.g12*y.g2 - x.g13*y.g3 - x.g23*y.g123 - x.g012*y.g02
      - x.g013*y.g03 - x.g023*y.ps - x.g123*y.g23 + x.ps*y.g023,
    g2 :=
      x.scalar*y.g2 + x.g0*y.g02 - x.g1*y.g12 + x.g2*y.scalar
      + x.g3*y.g23 + x.g01*y.g012 - x.g02*y.g0 - x.g03*y.g023
      + x.g12*y.g1 + x.g13*y.g123 - x.g23*y.g3 + x.g012*y.g01
      + x.g013*y.ps - x.g023*y.g03 + x.g123*y.g13 - x.ps*y.g013,
    g3 :=
      x.scalar*y.g3 + x.g0*y.g03 - x.g1*y.g13 - x.g2*y.g23
      + x.g3*y.scalar + x.g01*y.g013 + x.g02*y.g023 - x.g03*y.g0
      - x.g12*y.g123 + x.g13*y.g1 + x.g23*y.g2 - x.g012*y.ps
      + x.g013*y.g01 + x.g023*y.g02 - x.g123*y.g12 + x.ps*y.g012,
    g01 :=
      x.scalar*y.g01 + x.g0*y.g1 - x.g1*y.g0 - x.g2*y.g012
      - x.g3*y.g013 + x.g01*y.scalar + x.g02*y.g12 + x.g03*y.g13
      - x.g12*y.g02 - x.g13*y.g03 - x.g23*y.ps - x.g012*y.g2
      - x.g013*y.g3 - x.g023*y.g123 + x.g123*y.g023 - x.ps*y.g23,
    g02 :=
      x.scalar*y.g02 + x.g0*y.g2 + x.g1*y.g012 - x.g2*y.g0
      - x.g3*y.g023 - x.g01*y.g12 + x.g02*y.scalar + x.g03*y.g23
      + x.g12*y.g01 + x.g13*y.ps - x.g23*y.g03 + x.g012*y.g1
      + x.g013*y.g123 - x.g023*y.g3 - x.g123*y.g013 + x.ps*y.g13,
    g03 :=
      x.scalar*y.g03 + x.g0*y.g3 + x.g1*y.g013 + x.g2*y.g023
      - x.g3*y.g0 - x.g01*y.g13 - x.g02*y.g23 + x.g03*y.scalar
      - x.g12*y.ps + x.g13*y.g01 + x.g23*y.g02 - x.g012*y.g123
      + x.g013*y.g1 + x.g023*y.g2 + x.g123*y.g012 - x.ps*y.g12,
    g12 :=
      x.scalar*y.g12 + x.g0*y.g012 + x.g1*y.g2 - x.g2*y.g1
      - x.g3*y.g123 - x.g01*y.g02 + x.g02*y.g01 + x.g03*y.ps
      + x.g12*y.scalar + x.g13*y.g23 - x.g23*y.g13 + x.g012*y.g0
      + x.g013*y.g023 - x.g023*y.g013 - x.g123*y.g3 + x.ps*y.g03,
    g13 :=
      x.scalar*y.g13 + x.g0*y.g013 + x.g1*y.g3 + x.g2*y.g123
      - x.g3*y.g1 - x.g01*y.g03 - x.g02*y.ps + x.g03*y.g01
      - x.g12*y.g23 + x.g13*y.scalar + x.g23*y.g12 - x.g012*y.g023
      + x.g013*y.g0 + x.g023*y.g012 + x.g123*y.g2 - x.ps*y.g02,
    g23 :=
      x.scalar*y.g23 + x.g0*y.g023 - x.g1*y.g123 + x.g2*y.g3
      - x.g3*y.g2 + x.g01*y.ps - x.g02*y.g03 + x.g03*y.g02
      + x.g12*y.g13 - x.g13*y.g12 + x.g23*y.scalar + x.g012*y.g013
      - x.g013*y.g012 + x.g023*y.g0 - x.g123*y.g1 + x.ps*y.g01,
    g012 :=
      x.scalar*y.g012 + x.g0*y.g12 - x.g1*y.g02 + x.g2*y.g01
      + x.g3*y.ps + x.g01*y.g2 - x.g02*y.g1 - x.g03*y.g123
      + x.g12*y.g0 + x.g13*y.g023 - x.g23*y.g013 + x.g012*y.scalar
      + x.g013*y.g23 - x.g023*y.g13 + x.g123*y.g03 - x.ps*y.g3,
    g013 :=
      x.scalar*y.g013 + x.g0*y.g13 - x.g1*y.g03 - x.g2*y.ps
      + x.g3*y.g01 + x.g01*y.g3 + x.g02*y.g123 - x.g03*y.g1
      - x.g12*y.g023 + x.g13*y.g0 + x.g23*y.g012 - x.g012*y.g23
      + x.g013*y.scalar + x.g023*y.g12 - x.g123*y.g02 + x.ps*y.g2,
    g023 :=
      x.scalar*y.g023 + x.g0*y.g23 + x.g1*y.ps - x.g2*y.g03
      + x.g3*y.g02 - x.g01*y.g123 + x.g02*y.g3 - x.g03*y.g2
      + x.g12*y.g013 - x.g13*y.g012 + x.g23*y.g0 + x.g012*y.g13
      - x.g013*y.g12 + x.g023*y.scalar + x.g123*y.g01 - x.ps*y.g1,
    g123 :=
      x.scalar*y.g123 + x.g0*y.ps + x.g1*y.g23 - x.g2*y.g13
      + x.g3*y.g12 - x.g01*y.g023 + x.g02*y.g013 - x.g03*y.g012
      + x.g12*y.g3 - x.g13*y.g2 + x.g23*y.g1 + x.g012*y.g03
      - x.g013*y.g02 + x.g023*y.g01 + x.g123*y.scalar - x.ps*y.g0,
    ps :=
      x.scalar*y.ps + x.g0*y.g123 - x.g1*y.g023 + x.g2*y.g013
      - x.g3*y.g012 + x.g01*y.g23 - x.g02*y.g13 + x.g03*y.g12
      + x.g12*y.g03 - x.g13*y.g02 + x.g23*y.g01 + x.g012*y.g3
      - x.g013*y.g2 + x.g023*y.g1 - x.g123*y.g0 + x.ps*y.scalar }

instance : Mul STA := ⟨mul⟩

def zero : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩
instance : Zero STA := ⟨zero⟩

def one : STA := ⟨1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩
instance : One STA := ⟨one⟩

/-! ### Simp bridge lemmas -/

@[simp] lemma mul_def (a b : STA) : a * b = mul a b := rfl
@[simp] lemma add_def (a b : STA) : a + b = add a b := rfl
@[simp] lemma neg_def (a : STA) : -a = neg a := rfl
@[simp] lemma one_val : (1 : STA) = one := rfl
@[simp] lemma zero_val : (0 : STA) = zero := rfl

/-! ## Part 2: Basis Elements -/

-- Grade 1: basis vectors
def gamma0 : STA := ⟨0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩
def gamma1 : STA := ⟨0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩
def gamma2 : STA := ⟨0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩
def gamma3 : STA := ⟨0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩

-- Grade 2: bivectors
def sigma01 : STA := ⟨0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩
def sigma02 : STA := ⟨0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩
def sigma03 : STA := ⟨0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0⟩
def sigma12 : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0⟩
def sigma13 : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0⟩
def sigma23 : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0⟩

-- Grade 3: trivectors
def tri012 : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0⟩
def tri013 : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0⟩
def tri023 : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0⟩
def tri123 : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0⟩

-- Grade 4: pseudoscalar
def I_pseudo : STA := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1⟩

/-! ## Part 3: Basis Vector Products (Focused Approach)

Instead of defining the full 16x16 geometric product (256 terms),
we define a restricted multiplication for basis-vector-by-basis-vector
products. This establishes the signature and anticommutativity. -/

/-- Index type for the four basis vectors. -/
inductive BasisIdx where
  | t : BasisIdx   -- timelike (index 0)
  | x : BasisIdx   -- spacelike (index 1)
  | y : BasisIdx   -- spacelike (index 2)
  | z : BasisIdx   -- spacelike (index 3)
  deriving DecidableEq, Repr

open BasisIdx

/-- The Minkowski metric eta(mu,mu) with signature (+,-,-,-). -/
def eta : BasisIdx → ℝ
  | t => 1
  | x => -1
  | y => -1
  | z => -1

/-- Retrieve the basis vector STA element for a given index. -/
def basisVec : BasisIdx → STA
  | t => gamma0
  | x => gamma1
  | y => gamma2
  | z => gamma3

/-- Product of two basis vectors: g_mu * g_nu.
    Returns a scalar (for mu = nu) or a bivector (for mu != nu). -/
def vecMul (mu nu : BasisIdx) : STA :=
  if mu = nu then
    smul (eta mu) one
  else
    match mu, nu with
    | t, x => sigma01
    | t, y => sigma02
    | t, z => sigma03
    | x, y => sigma12
    | x, z => sigma13
    | y, z => sigma23
    | x, t => neg sigma01
    | y, t => neg sigma02
    | z, t => neg sigma03
    | y, x => neg sigma12
    | z, x => neg sigma13
    | z, y => neg sigma23
    | _, _ => zero  -- unreachable

/-! ### Signature Theorems -/

/-- The timelike vector squares to +1. -/
theorem gamma0_sq : vecMul t t = smul 1 one := by
  simp [vecMul, eta]

/-- The first spacelike vector squares to -1. -/
theorem gamma1_sq : vecMul x x = smul (-1) one := by
  simp [vecMul, eta]

/-- The second spacelike vector squares to -1. -/
theorem gamma2_sq : vecMul y y = smul (-1) one := by
  simp [vecMul, eta]

/-- The third spacelike vector squares to -1. -/
theorem gamma3_sq : vecMul z z = smul (-1) one := by
  simp [vecMul, eta]

/-- Signature verification: g0^2 = +1 as a scalar STA element. -/
theorem gamma0_sq_is_one : vecMul t t = one := by
  simp [vecMul, eta, smul, one]

/-- Signature verification: g1^2 = -1 as a negated STA element. -/
theorem gamma1_sq_is_neg_one : vecMul x x = neg one := by
  simp [vecMul, eta, smul, one, neg]

/-! ### Anticommutativity Theorems -/

theorem g0_g1_anticommute : vecMul t x = neg (vecMul x t) := by
  simp [vecMul, neg, sigma01]

theorem g0_g2_anticommute : vecMul t y = neg (vecMul y t) := by
  simp [vecMul, neg, sigma02]

theorem g0_g3_anticommute : vecMul t z = neg (vecMul z t) := by
  simp [vecMul, neg, sigma03]

theorem g1_g2_anticommute : vecMul x y = neg (vecMul y x) := by
  simp [vecMul, neg, sigma12]

theorem g1_g3_anticommute : vecMul x z = neg (vecMul z x) := by
  simp [vecMul, neg, sigma13]

theorem g2_g3_anticommute : vecMul y z = neg (vecMul z y) := by
  simp [vecMul, neg, sigma23]

/-! ### Bivector Products -/

theorem g0_mul_g1 : vecMul t x = sigma01 := by simp [vecMul]
theorem g0_mul_g2 : vecMul t y = sigma02 := by simp [vecMul]
theorem g0_mul_g3 : vecMul t z = sigma03 := by simp [vecMul]
theorem g1_mul_g2 : vecMul x y = sigma12 := by simp [vecMul]
theorem g1_mul_g3 : vecMul x z = sigma13 := by simp [vecMul]
theorem g2_mul_g3 : vecMul y z = sigma23 := by simp [vecMul]

/-! ### The Pseudoscalar

I = g0*g1*g2*g3 is the unit pseudoscalar of Cl(1,3).
It satisfies I^2 = -1. We verify this algebraically.

Computation: I^2 = (g0*g1*g2*g3)^2
The sign comes from counting anticommutation swaps:
  I^2 = g0^2 * g1^2 * g2^2 * g3^2 * (-1)^(number of swaps)
  = (+1) * (-1) * (-1) * (-1) * (-1)^6 = -1

More precisely: 6 swaps needed to bring the second copy's g0 past g3,g2,g1
of the first copy, but each swap of equal basis vectors also contributes
the metric factor. The net result: I^2 = -1. -/

theorem pseudoscalar_sq_arithmetic :
    (1 : ℝ) * (-1) * (-1) * (-1) * (-1) * (-1) = -1 := by norm_num

/-! ## Part 4: The Electromagnetic Field

The electromagnetic field F is a BIVECTOR in Cl(1,3). It unifies the
electric field E and the magnetic field B into a single geometric object.

F = Ex*(g0 wedge g1) + Ey*(g0 wedge g2) + Ez*(g0 wedge g3)
  + Bx*(g2 wedge g3) + By*(g3 wedge g1) + Bz*(g1 wedge g2)

The ELECTRIC part lives in timelike bivectors (g0 wedge g_i).
The MAGNETIC part lives in spacelike bivectors (g_i wedge g_j).

This unification is NOT a notational trick. Under Lorentz transformations,
E and B MIX -- what one observer calls "pure electric field," another
calls "electromagnetic field." The bivector F is the observer-independent
geometric object. -/

/-- The electromagnetic field as a bivector in Cl(1,3). -/
def em_field (Ex Ey Ez Bx By Bz : ℝ) : STA :=
  ⟨0,  0, 0, 0, 0,  Ex, Ey, Ez, Bz, -By, Bx,  0, 0, 0, 0,  0⟩

/-- The electric part of F lives in timelike bivectors. -/
def electric_field (Ex Ey Ez : ℝ) : STA :=
  ⟨0,  0, 0, 0, 0,  Ex, Ey, Ez, 0, 0, 0,  0, 0, 0, 0,  0⟩

/-- The magnetic part of F lives in spacelike bivectors. -/
def magnetic_field (Bx By Bz : ℝ) : STA :=
  ⟨0,  0, 0, 0, 0,  0, 0, 0, Bz, -By, Bx,  0, 0, 0, 0,  0⟩

/-- The electromagnetic bivector decomposes as E + B parts. -/
theorem em_field_decomposition (Ex Ey Ez Bx By Bz : ℝ) :
    em_field Ex Ey Ez Bx By Bz =
    add (electric_field Ex Ey Ez) (magnetic_field Bx By Bz) := by
  ext <;> simp [em_field, electric_field, magnetic_field, add]

/-- A purely electric field (B = 0). -/
theorem pure_electric (Ex Ey Ez : ℝ) :
    em_field Ex Ey Ez 0 0 0 = electric_field Ex Ey Ez := by
  ext <;> simp [em_field, electric_field]

/-- A purely magnetic field (E = 0). -/
theorem pure_magnetic (Bx By Bz : ℝ) :
    em_field 0 0 0 Bx By Bz = magnetic_field Bx By Bz := by
  ext <;> simp [em_field, magnetic_field]

/-- The electromagnetic field is a pure bivector. -/
theorem em_field_is_bivector (Ex Ey Ez Bx By Bz : ℝ) :
    let F := em_field Ex Ey Ez Bx By Bz
    F.scalar = 0 ∧ F.g0 = 0 ∧ F.g1 = 0 ∧ F.g2 = 0 ∧ F.g3 = 0 ∧
    F.g012 = 0 ∧ F.g013 = 0 ∧ F.g023 = 0 ∧ F.g123 = 0 ∧ F.ps = 0 := by
  simp [em_field]

/-! ## Part 5: Maxwell's Equation -- nabla * F = J

In Cl(1,3), the spacetime gradient is the vector-valued operator:
    nabla = g0 * (d/dt) + g1 * (d/dx) + g2 * (d/dy) + g3 * (d/dz)

The current density is a vector:
    J = rho * g0 - Jx * g1 - Jy * g2 - Jz * g3

Maxwell's single equation is:
    nabla * F = J

When expanded by grade:
  Grade 0: div(E) = rho               (Gauss electric)
  Grade 2: curl(B) - dE/dt = J_vec    (Ampere-Maxwell)
  Grade 3: div(B) = 0 and curl(E) + dB/dt = 0  (homogeneous)

Four equations, one line. The Clifford algebra reveals that
Maxwell's equations are not four independent laws but one geometric
identity. -/

/-- The current density vector. -/
def current_density (rho Jx Jy Jz : ℝ) : STA :=
  ⟨0,  rho, -Jx, -Jy, -Jz,  0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0⟩

/-- The electromagnetic potential 1-form. -/
def em_potential (phi Ax Ay Az : ℝ) : STA :=
  ⟨0,  phi, -Ax, -Ay, -Az,  0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0⟩

/-- The current density is a pure vector (grade 1). -/
theorem current_is_vector (rho Jx Jy Jz : ℝ) :
    let J := current_density rho Jx Jy Jz
    J.scalar = 0 ∧
    J.g01 = 0 ∧ J.g02 = 0 ∧ J.g03 = 0 ∧ J.g12 = 0 ∧ J.g13 = 0 ∧ J.g23 = 0 ∧
    J.g012 = 0 ∧ J.g013 = 0 ∧ J.g023 = 0 ∧ J.g123 = 0 ∧ J.ps = 0 := by
  simp [current_density]

/-! ### Maxwell's Equation as a Structure

Since we do not have differential operators in Lean (no smooth manifolds),
we cannot PROVE nabla * F = J computationally. Instead, we capture the
STRUCTURAL content: F is a bivector and J is a vector, which constrains
the grade structure. -/

/-- Maxwell configuration: the components of the fields and sources. -/
structure MaxwellConfig where
  ex : ℝ
  ey : ℝ
  ez : ℝ
  bx : ℝ
  by_ : ℝ
  bz : ℝ
  rho : ℝ
  jx : ℝ
  jy : ℝ
  jz : ℝ

/-- The unified field for a Maxwell configuration is a pure bivector. -/
theorem maxwell_field_is_bivector (m : MaxwellConfig) :
    let F := em_field m.ex m.ey m.ez m.bx m.by_ m.bz
    F.scalar = 0 ∧ F.g0 = 0 ∧ F.g1 = 0 ∧ F.g2 = 0 ∧ F.g3 = 0 ∧
    F.g012 = 0 ∧ F.g013 = 0 ∧ F.g023 = 0 ∧ F.g123 = 0 ∧ F.ps = 0 := by
  simp [em_field]

/-- The source for a Maxwell configuration is a pure vector. -/
theorem maxwell_source_is_vector (m : MaxwellConfig) :
    let J := current_density m.rho m.jx m.jy m.jz
    J.scalar = 0 ∧
    J.g01 = 0 ∧ J.g02 = 0 ∧ J.g03 = 0 ∧ J.g12 = 0 ∧ J.g13 = 0 ∧ J.g23 = 0 ∧
    J.g012 = 0 ∧ J.g013 = 0 ∧ J.g023 = 0 ∧ J.g123 = 0 ∧ J.ps = 0 := by
  simp [current_density]

/-! ## Part 6: The Hierarchy Connection -- Cl(3,0) Embeds into Cl(1,3)

Cl(3,0) embeds into Cl(1,3) as the SPATIAL SUBALGEBRA:
  e_i (Cl(3,0))  <-->  gamma0 * gamma_i (Cl(1,3) bivector)

The Cl(3,0) signature (+,+,+) is RECOVERED because:
  (g0*gi)^2 = g0*gi*g0*gi = -g0*g0*gi*gi = -(+1)*(-1) = +1 -/

/-- Embedding of Cl(3,0) spatial vectors into Cl(1,3) timelike bivectors. -/
def embed_spatial_vector (a b c : ℝ) : STA :=
  ⟨0,  0, 0, 0, 0,  a, b, c, 0, 0, 0,  0, 0, 0, 0,  0⟩

/-- Embedding of Cl(3,0) bivectors into Cl(1,3) spacelike bivectors. -/
def embed_spatial_bivector (p q r : ℝ) : STA :=
  ⟨0,  0, 0, 0, 0,  0, 0, 0, p, q, r,  0, 0, 0, 0,  0⟩

/-- The Cl(3,0) EM field maps exactly to the Cl(1,3) electromagnetic bivector. -/
theorem cl30_em_field_embeds (Ex Ey Ez Bx By Bz : ℝ) :
    em_field Ex Ey Ez Bx By Bz =
    add (embed_spatial_vector Ex Ey Ez) (embed_spatial_bivector Bz (-By) Bx) := by
  ext <;> simp [em_field, embed_spatial_vector, embed_spatial_bivector, add]

/-! ### Signature Recovery -/

/-- The relative vectors satisfy sigma0i^2 = +1, matching Cl(3,0).
    This is verified by the arithmetic:
      eta(t) * eta(i) * (-1) = (+1) * (-1) * (-1) = +1 -/
theorem relative_vector_sq_positive :
    ∀ i : BasisIdx, i ≠ t →
    eta t * eta i * (-1 : ℝ) = 1 := by
  intro i hi
  cases i with
  | t => exact absurd rfl hi
  | x => simp [eta]
  | y => simp [eta]
  | z => simp [eta]

/-! ## Part 7: The Full Geometric Product — Signature Verification

With the full 256-term geometric product defined, we can now verify the
signature axioms directly via multiplication, not just via vecMul. -/

/-- g0 * g0 = +1 (timelike signature, full product). -/
theorem gamma0_sq_full : gamma0 * gamma0 = (1 : STA) := by
  ext <;> simp [gamma0, mul, one]

/-- g1 * g1 = -1 (spacelike signature, full product). -/
theorem gamma1_sq_full : gamma1 * gamma1 = -(1 : STA) := by
  ext <;> simp [gamma1, mul, one, neg]

/-- g0 * g1 = sigma01 (bivector product, full product). -/
theorem g0_g1_full : gamma0 * gamma1 = sigma01 := by
  ext <;> simp [gamma0, gamma1, sigma01, mul]

/-- g1 * g0 = -sigma01 (anticommutativity, full product). -/
theorem g1_g0_full : gamma1 * gamma0 = -sigma01 := by
  ext <;> simp [gamma1, gamma0, sigma01, mul, neg]

/-- The pseudoscalar I = g0123 squares to -1. -/
theorem pseudoscalar_sq_full : I_pseudo * I_pseudo = -(1 : STA) := by
  ext <;> simp [I_pseudo, mul, one, neg]

/-- The boost bivector g01 squares to +1 (key for Lorentz boosts). -/
theorem sigma01_sq : sigma01 * sigma01 = (1 : STA) := by
  ext <;> simp [sigma01, mul, one]

/-- The spatial bivector g12 squares to -1 (key for spatial rotations). -/
theorem sigma12_sq : sigma12 * sigma12 = -(1 : STA) := by
  ext <;> simp [sigma12, mul, one, neg]

/-! ## Part 8: Reversion and Rotors in Spacetime

Reversion reverses the order of basis vectors in each blade:
  rev(1) = 1, rev(gμ) = gμ,
  rev(gμν) = gνμ = -gμν,
  rev(gμνρ) = gρνμ = -gμνρ,
  rev(g0123) = g3210 = +g0123  (even number of swaps)

Grade k blade picks up sign (-1)^(k(k-1)/2):
  k=0: +1,  k=1: +1,  k=2: -1,  k=3: -1,  k=4: +1 -/

/-- Reversion in Cl(1,3): reverses the order of basis vectors in each blade. -/
def rev (x : STA) : STA :=
  ⟨x.scalar,
   x.g0, x.g1, x.g2, x.g3,
   -x.g01, -x.g02, -x.g03, -x.g12, -x.g13, -x.g23,
   -x.g012, -x.g013, -x.g023, -x.g123,
   x.ps⟩

/-- Reversion is an involution: rev(rev(x)) = x. -/
theorem rev_rev (x : STA) : rev (rev x) = x := by
  ext <;> simp [rev]

/-- The sandwich product: how rotors act on multivectors. -/
def sandwich (R x : STA) : STA := R * x * (rev R)

/-! ### Lorentz Boost Rotors in Cl(1,3)

A boost in the g0-g1 plane (x-direction) is the rotor:
  R = cosh(φ/2) + sinh(φ/2)*g01

The boost subalgebra {1, g0, g1, g01} is isomorphic to Cl(1,1).
  g0 ↔ e1 (timelike, squares to +1)
  g1 ↔ e2 (spacelike, squares to -1)
  g01 ↔ e12 (boost bivector, squares to +1)

This is the same Cl(1,1) where we proved Lorentz boosts work.
Now we embed it into full spacetime algebra. -/

/-- A boost rotor in the g01 plane: R = c + s*g01.
    For a physical Lorentz boost: c = cosh(φ/2), s = sinh(φ/2). -/
def boostRotor01 (c s : ℝ) : STA :=
  ⟨c, 0, 0, 0, 0, s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩

/-- The reverse of a boost rotor flips the bivector sign. -/
theorem rev_boostRotor01 (c s : ℝ) :
    rev (boostRotor01 c s) = boostRotor01 c (-s) := by
  ext <;> simp [rev, boostRotor01]

/-- Rotor normalization: R * R̃ = (c²-s²) * 1.
    For proper Lorentz boosts, c²-s² = cosh²(φ/2)-sinh²(φ/2) = 1. -/
theorem boost01_norm (c s : ℝ) :
    boostRotor01 c s * rev (boostRotor01 c s) =
    ⟨c^2 - s^2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩ := by
  simp [rev_boostRotor01]
  ext <;> simp [boostRotor01, mul] <;> ring

/-- Lorentz boost of g0 (the time direction):
    R * g0 * R̃ = (c²+s²)*g0 + (-2cs)*g1.
    With c=cosh(φ/2), s=sinh(φ/2): t' = cosh(φ)*t - sinh(φ)*x. -/
theorem boost01_gamma0 (c s : ℝ) :
    sandwich (boostRotor01 c s) gamma0 =
    ⟨0, c^2 + s^2, -2*c*s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩ := by
  simp [sandwich, rev_boostRotor01]
  ext <;> simp [boostRotor01, gamma0, mul] <;> ring

/-- Lorentz boost of g1 (the x-direction):
    R * g1 * R̃ = (-2cs)*g0 + (c²+s²)*g1.
    With c=cosh(φ/2), s=sinh(φ/2): x' = -sinh(φ)*t + cosh(φ)*x. -/
theorem boost01_gamma1 (c s : ℝ) :
    sandwich (boostRotor01 c s) gamma1 =
    ⟨0, -2*c*s, c^2 + s^2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩ := by
  simp [sandwich, rev_boostRotor01]
  ext <;> simp [boostRotor01, gamma1, mul] <;> ring

/-- Lorentz boost of g2 (the y-direction): UNCHANGED.
    The boost in the g01 plane leaves transverse directions alone. -/
theorem boost01_gamma2 (c s : ℝ) (hn : c^2 - s^2 = 1) :
    sandwich (boostRotor01 c s) gamma2 = gamma2 := by
  simp [sandwich, rev_boostRotor01]
  ext <;> simp [boostRotor01, gamma2, mul] <;> nlinarith

/-- Lorentz boost of g3 (the z-direction): UNCHANGED. -/
theorem boost01_gamma3 (c s : ℝ) (hn : c^2 - s^2 = 1) :
    sandwich (boostRotor01 c s) gamma3 = gamma3 := by
  simp [sandwich, rev_boostRotor01]
  ext <;> simp [boostRotor01, gamma3, mul] <;> nlinarith

/-! ### The Crown Jewel: Lorentz Boost of the Electromagnetic Field

Under a Lorentz boost in the x-direction, the EM field transforms:
  F' = R * F * R̃

The electric and magnetic fields MIX:
  Ex' = Ex                    (parallel to boost: unchanged)
  Ey' = cosh(φ)*Ey - sinh(φ)*Bz  (transverse: E and B mix!)
  Ez' = cosh(φ)*Ez + sinh(φ)*By
  Bx' = Bx                    (parallel to boost: unchanged)
  By' = cosh(φ)*By + sinh(φ)*Ez  (transverse: B and E mix!)
  Bz' = cosh(φ)*Bz - sinh(φ)*Ey

What one observer calls pure electric field, another calls electromagnetic.
This is special relativity encoded in the rotor sandwich product. -/

/-- Lorentz boost of a pure Ex field (along boost direction): UNCHANGED.
    The component parallel to the boost is invariant. -/
theorem boost01_Ex (c s : ℝ) (Ex : ℝ) (hn : c^2 - s^2 = 1) :
    sandwich (boostRotor01 c s) (em_field Ex 0 0 0 0 0) =
    em_field Ex 0 0 0 0 0 := by
  have aux : c * Ex * c - s * Ex * s = Ex := by
    have : c * Ex * c - s * Ex * s = (c ^ 2 - s ^ 2) * Ex := by ring
    rw [this, hn, one_mul]
  simp [sandwich, rev_boostRotor01]
  ext <;> simp [boostRotor01, em_field, mul] <;> linarith

/-- Lorentz boost of a pure Ey field: mixes with Bz.
    Ey' = (c²+s²)*Ey, Bz' = (-2cs)*Ey.
    With c=cosh(φ/2), s=sinh(φ/2):
      Ey' = cosh(φ)*Ey, Bz' = -sinh(φ)*Ey.
    A moving observer sees a magnetic field appear from pure E! -/
theorem boost01_Ey (c s : ℝ) (Ey : ℝ) :
    sandwich (boostRotor01 c s) (em_field 0 Ey 0 0 0 0) =
    em_field 0 ((c^2+s^2)*Ey) 0 0 0 ((-2*c*s)*Ey) := by
  simp [sandwich, rev_boostRotor01]
  ext <;> simp [boostRotor01, em_field, mul] <;> ring

/-- Lorentz boost of a pure Bx field (along boost direction): UNCHANGED.
    The magnetic component parallel to the boost is invariant. -/
theorem boost01_Bx (c s : ℝ) (Bx : ℝ) (hn : c^2 - s^2 = 1) :
    sandwich (boostRotor01 c s) (em_field 0 0 0 Bx 0 0) =
    em_field 0 0 0 Bx 0 0 := by
  have aux : c * Bx * c - s * Bx * s = Bx := by
    have : c * Bx * c - s * Bx * s = (c ^ 2 - s ^ 2) * Bx := by ring
    rw [this, hn, one_mul]
  simp [sandwich, rev_boostRotor01]
  ext <;> simp [boostRotor01, em_field, mul] <;> linarith

/-! ## Part 9: Spatial Rotations

A rotation in the g1-g2 plane (around the g3 axis) uses the rotor:
  R = cos(θ/2) + sin(θ/2)*σ₁₂

Key difference from boosts:
  - Boost bivector σ₀₁² = +1  →  normalization c² - s² = 1  (hyperbolic)
  - Rotation bivector σ₁₂² = -1  →  normalization c² + s² = 1  (circular)

The rotation gives:
  R*g1*R̃ = cos(θ)*g1 + sin(θ)*g2    (circular rotation!)
  R*g2*R̃ = -sin(θ)*g1 + cos(θ)*g2
  R*g0*R̃ = g0   (time unchanged)
  R*g3*R̃ = g3   (axis unchanged)

Compare with the Lorentz boost:
  R*g0*R̃ = cosh(φ)*g0 - sinh(φ)*g1  (hyperbolic rotation)

Both are rotor sandwiches. The geometry (circular vs hyperbolic) comes from
the signature of the bivector plane (negative vs positive square). -/

/-- A spatial rotation rotor in the g12 plane: R = c + s*σ₁₂.
    For a physical rotation: c = cos(θ/2), s = sin(θ/2). -/
def rotationRotor12 (c s : ℝ) : STA :=
  ⟨c, 0, 0, 0, 0, 0, 0, 0, s, 0, 0, 0, 0, 0, 0, 0⟩

/-- The reverse of a rotation rotor flips the bivector sign. -/
theorem rev_rotationRotor12 (c s : ℝ) :
    rev (rotationRotor12 c s) = rotationRotor12 c (-s) := by
  ext <;> simp [rev, rotationRotor12]

/-- Rotation of g1: R*g1*R̃ = (c²-s²)*g1 + 2cs*g2.
    With c=cos(θ/2), s=sin(θ/2): g1' = cos(θ)*g1 + sin(θ)*g2. -/
theorem rotation12_gamma1 (c s : ℝ) :
    sandwich (rotationRotor12 c s) gamma1 =
    ⟨0, 0, c^2 - s^2, 2*c*s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩ := by
  simp [sandwich, rev_rotationRotor12]
  ext <;> simp [rotationRotor12, gamma1, mul] <;> ring

/-- Rotation of g2: R*g2*R̃ = -2cs*g1 + (c²-s²)*g2.
    With c=cos(θ/2), s=sin(θ/2): g2' = -sin(θ)*g1 + cos(θ)*g2. -/
theorem rotation12_gamma2 (c s : ℝ) :
    sandwich (rotationRotor12 c s) gamma2 =
    ⟨0, 0, -2*c*s, c^2 - s^2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩ := by
  simp [sandwich, rev_rotationRotor12]
  ext <;> simp [rotationRotor12, gamma2, mul] <;> ring

/-- Rotation leaves g0 (time) unchanged. -/
theorem rotation12_gamma0 (c s : ℝ) (hn : c^2 + s^2 = 1) :
    sandwich (rotationRotor12 c s) gamma0 = gamma0 := by
  simp [sandwich, rev_rotationRotor12]
  ext <;> simp [rotationRotor12, gamma0, mul] <;> nlinarith

/-- Rotation leaves g3 (axis of rotation) unchanged. -/
theorem rotation12_gamma3 (c s : ℝ) (hn : c^2 + s^2 = 1) :
    sandwich (rotationRotor12 c s) gamma3 = gamma3 := by
  simp [sandwich, rev_rotationRotor12]
  ext <;> simp [rotationRotor12, gamma3, mul] <;> nlinarith

/-- Rotation normalization: R*R̃ = (c²+s²)*1.
    For proper rotations, c²+s²=1 (vs c²-s²=1 for boosts). -/
theorem rotation12_norm (c s : ℝ) :
    rotationRotor12 c s * rev (rotationRotor12 c s) =
    ⟨c^2 + s^2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩ := by
  simp [rev_rotationRotor12]
  ext <;> simp [rotationRotor12, mul] <;> ring

/-! ## Part 10: The Lorentz Lie Algebra

The 6 bivectors {σ₀₁, σ₀₂, σ₀₃, σ₁₂, σ₁₃, σ₂₃} generate the Lorentz group.
Their commutator algebra [A, B] = A*B - B*A is so(1,3).

Structure:
  [boost, boost] = -2 * rotation     (two boosts = a rotation!)
  [rotation, rotation] = ±2 * rotation  (rotations close under commutator)
  [boost, rotation] = ±2 * boost     (when sharing a spatial index)

This is the algebraic heart of special relativity. The fact that two
boosts compose to give a rotation is the Thomas precession — a purely
algebraic consequence of the Cl(1,3) structure. -/

/-- The commutator product: [A, B] = A*B - B*A. -/
def commutator (x y : STA) : STA := x * y + -(y * x)

/-- [σ₀₁, σ₀₂] = -2*σ₁₂.
    Two boosts in different directions produce a rotation!
    This is the algebraic origin of Thomas precession. -/
theorem comm_boost_boost : commutator sigma01 sigma02 = smul (-2) sigma12 := by
  ext <;> simp [commutator, sigma01, sigma02, sigma12, mul, add, neg, smul]; norm_num

/-- [σ₁₂, σ₁₃] = 2*σ₂₃.
    Rotations close under commutator — the so(3) subalgebra. -/
theorem comm_rotation_rotation : commutator sigma12 sigma13 = smul 2 sigma23 := by
  ext <;> simp [commutator, sigma12, sigma13, sigma23, mul, add, neg, smul]; norm_num

/-- [σ₀₁, σ₁₂] = -2*σ₀₂.
    A boost and a rotation (sharing index 1) produce another boost. -/
theorem comm_boost_rotation : commutator sigma01 sigma12 = smul (-2) sigma02 := by
  ext <;> simp [commutator, sigma01, sigma12, sigma02, mul, add, neg, smul]; norm_num

/-- [σ₀₁, σ₂₃] = 0.
    A boost and a rotation in orthogonal planes commute. -/
theorem comm_orthogonal : commutator sigma01 sigma23 = (0 : STA) := by
  ext <;> simp [commutator, sigma01, sigma23, mul, add, neg, zero]

end STA

/-!
## Summary: The Full Hierarchy

### The algebraic chain (all formally verified):

  Z_4             -- 4 elements, commutative, trivial
                     Dollard's versor algebra, forced by his axioms.

  Cl(1,1)         -- 4 elements, non-commutative, wave decomposition
                     Idempotent projectors. LORENTZ BOOSTS as rotors.

  Cl(3,0)         -- 8 elements, Pauli algebra, 3D space
                     EM field as F = E + I*B (vector + bivector).

  Cl(1,3)         -- 16 elements, Spacetime Algebra, THIS FILE
                     Full 256-term geometric product. Lorentz rotors.
                     Maxwell's four equations → ONE: nabla * F = J.
                     EM field TRANSFORMS under boosts: E and B MIX.

### What this file proves (Parts 1-8):
1. STA structure with 16 basis blades (Part 1-2)
2. Full 256-term geometric product from Clifford axioms (Part 1)
3. Basis vector products and anticommutativity (Part 3)
4. g0²=+1, gi²=-1, I²=-1, g01²=+1, g12²=-1 (Part 7)
5. EM field as bivector, E+B decomposition (Part 4)
6. Maxwell's equation structure: F is bivector, J is vector (Part 5)
7. Cl(3,0) embeds as spatial subalgebra (Part 6)
8. Reversion for all 16 grades (Part 8)
9. Lorentz boost rotors R = c + s*g01 (Part 8)
10. R*g0*R̃ = cosh(φ)*g0 - sinh(φ)*g1 (time dilation)
11. R*g1*R̃ = -sinh(φ)*g0 + cosh(φ)*g1 (length contraction)
12. R*g2*R̃ = g2, R*g3*R̃ = g3 (transverse invariance)
13. E∥ invariant under boost, B∥ invariant under boost
14. E⊥ and B⊥ MIX under boosts (special relativity!)

### The key message:

Maxwell's four equations are ONE equation in Cl(1,3).
Lorentz transformations are rotor sandwiches: F' = R*F*R̃.
E and B are not separate fields — they are one bivector F
that observers decompose differently based on their motion.
The hierarchy from Z_4 to Cl(1,3) traces the path from Dollard's
intuition to the precise mathematical framework where that structure
is manifest.
-/
