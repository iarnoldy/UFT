/-
UFT Formal Verification - Telegraph Equation Mathematics
=========================================================

Verifies the algebraic expansion of Heaviside's Telegraph Equation
as presented in Eric Dollard's Four Quadrant Theory.

SIGN CONVENTION (Critical):
  Dollard uses admittance Y = G - jB (negative susceptance convention).
  Standard EE convention uses Y = G + jB.

  With Z = R + jX and Y = G - jB (Dollard):
    ZY = (R + jX)(G - jB) = (RG + XB) + j(XG - RB)

  With Z = R + jX and Y = G + jB (standard):
    ZY = (R + jX)(G + jB) = (RG - XB) + j(RB + XG)

  The signs on XB and RB flip between conventions.
  This file verifies Dollard's claimed expansion under HIS convention.

NOTE ON PROOF TECHNIQUE:
  We use Complex.mk (re, im) notation throughout. This avoids issues
  with the `ring` tactic not knowing Complex.I^2 = -1 (ring treats I
  as an opaque symbol). With Complex.mk, `ext` splits into real/imaginary
  components and `ring` closes purely real arithmetic.

References:
- Dollard, E. P. "Four Quadrant Theory: Advanced Electrical Applications"
- Heaviside, O. "Electromagnetic Theory"
-/

import Mathlib.Data.Complex.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import foundations.basic_operators

-- ============================================================
-- Section 1: Telegraph equation (Dollard's sign convention)
-- ============================================================

-- Z = R + jX (series impedance per unit length)
-- Y = G - jB (shunt admittance per unit length, Dollard convention)
-- We represent Z as Complex.mk R X and Y as Complex.mk G (-B).

/-- Telegraph equation product ZY with Dollard's convention Y = G - jB.
    Equivalent to (R + jX)(G - jB) in standard notation. -/
def telegraph_product (R X G B : ℝ) : ℂ :=
  Complex.mk R X * Complex.mk G (-B)

/-- Core verification: ZY expands to (RG + XB) + j(XG - RB).
    This is Dollard's claimed form and it IS correct under his convention. -/
theorem telegraph_expansion (R X G B : ℝ) :
    telegraph_product R X G B =
    Complex.mk (R * G + X * B) (X * G - R * B) := by
  unfold telegraph_product
  apply Complex.ext <;> simp [Complex.mul_re, Complex.mul_im]; ring

-- For comparison: standard convention Y = G + jB
/-- Telegraph equation product with standard convention Y = G + jB. -/
def telegraph_standard (R X G B : ℝ) : ℂ :=
  Complex.mk R X * Complex.mk G B

/-- Standard convention yields (RG - XB) + j(RB + XG). -/
theorem telegraph_expansion_standard (R X G B : ℝ) :
    telegraph_standard R X G B =
    Complex.mk (R * G - X * B) (R * B + X * G) := by
  unfold telegraph_standard
  apply Complex.ext <;> simp [Complex.mul_re, Complex.mul_im]

-- ============================================================
-- Section 2: Four-factor decomposition
-- ============================================================

def factor_RG (R G : ℝ) : ℝ := R * G
def factor_XB (X B : ℝ) : ℝ := X * B
def factor_XG (X G : ℝ) : ℝ := X * G
def factor_RB (R B : ℝ) : ℝ := R * B

/-- Telegraph equation in terms of named factors. -/
theorem telegraph_four_factors (R X G B : ℝ) :
    telegraph_product R X G B =
    Complex.mk (factor_RG R G + factor_XB X B)
               (factor_XG X G - factor_RB R B) := by
  unfold telegraph_product factor_RG factor_XB factor_XG factor_RB
  apply Complex.ext <;> simp [Complex.mul_re, Complex.mul_im]; ring

/-- All four factors can be simultaneously nonzero. -/
theorem four_factors_nonzero :
    ∃ (R X G B : ℝ), factor_RG R G ≠ 0 ∧ factor_XB X B ≠ 0 ∧
                     factor_XG X G ≠ 0 ∧ factor_RB R B ≠ 0 := by
  exact ⟨1, 1, 1, 1, by norm_num [factor_RG, factor_XB, factor_XG, factor_RB]⟩

/-- The four factors satisfy an algebraic constraint: (RG)(XB) = (XG)(RB).
    They are NOT four free parameters. Dollard's "independence" claim is
    better understood as: four DISTINCT terms appear in the expansion. -/
theorem factor_constraint (R X G B : ℝ) :
    factor_RG R G * factor_XB X B = factor_XG X G * factor_RB R B := by
  unfold factor_RG factor_XB factor_XG factor_RB; ring

-- ============================================================
-- Section 3: Versor form analysis (DISPROOF)
-- ============================================================

-- Dollard claims: ZY = h(XB + RG) + j(XG - RB)
-- With h = -1 (algebraically necessary, see algebraic_necessity.lean):
--   h(XB + RG) = -(XB + RG) ≠ +(XB + RG)
-- The real parts have opposite signs.

/-- What the versor form actually evaluates to when h = -1.
    The real part is NEGATED relative to the telegraph expansion. -/
theorem versor_form_value (R X G B : ℝ) :
    h * (↑(factor_XB X B + factor_RG R G) : ℂ) +
    j * (↑(factor_XG X G - factor_RB R B) : ℂ) =
    Complex.mk (-(factor_XB X B + factor_RG R G))
               (factor_XG X G - factor_RB R B) := by
  simp only [h, j]
  apply Complex.ext <;>
    simp [Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im,
          Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im]

-- Compare the two forms side by side:
--   Telegraph product: Complex.mk +(RG + XB)  (XG - RB)
--   Versor form:       Complex.mk -(XB + RG)  (XG - RB)
--
-- The imaginary parts match. The real parts are NEGATED.
-- These are equal ONLY when RG + XB = 0, i.e., when both
-- dissipation and storage vanish simultaneously — a degenerate case.
--
-- This DISPROOF is robust: it holds regardless of sign convention
-- (Dollard or standard), because h = -1 negates the real part in
-- either convention.

-- ============================================================
-- Section 3b: Versor form repair analysis (Experiment 2)
-- ============================================================
-- Can the versor form be repaired while preserving Dollard's algebra?
-- Answer: NO. The only repair requires h = 1, which contradicts h = -1.
--
-- Analysis: For the versor form c*(XB+RG) + j*(XG-RB) to match the
-- telegraph product (RG+XB) + j*(XG-RB), the coefficient c must
-- equal 1 (compare real parts when RG+XB ≠ 0). But h = -1 ≠ 1.
-- The three possible repairs are:
--   (1) Set c = 1: works mathematically, but c = 1 ≠ h. No versors.
--   (2) Negate the argument: h*(-XB-RG) = XB+RG. Changes Dollard's formula.
--   (3) Drop jk=1 to escape h=-1: yields a DIFFERENT algebra (Cl(1,1)).
-- All three abandon Dollard's system.

/-- h ≠ 1: Dollard's h operator cannot be the identity.
    Combined with versor_form_value, this shows no versor form repair
    exists within Dollard's algebra. -/
theorem h_ne_one : h ≠ (1 : ℂ) := by
  simp [h]; norm_num

/-- Using 1 instead of h makes the "versor form" trivially correct,
    but this is just the telegraph expansion with identity coefficient. -/
theorem versor_repaired_with_one (R X G B : ℝ) :
    (1 : ℂ) * (↑(factor_XB X B + factor_RG R G) : ℂ) +
    j * (↑(factor_XG X G - factor_RB R B) : ℂ) =
    telegraph_product R X G B := by
  unfold telegraph_product factor_XB factor_RG factor_XG factor_RB
  apply Complex.ext <;>
    simp [Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im,
          Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im,
          j] <;> ring

-- ============================================================
-- Section 4: Physical interpretation labels
-- ============================================================

-- Dollard's names for the four factors (physics claims, not math)
def energy_storage (X B : ℝ) : ℝ := factor_XB X B      -- "alternating exchange"
def energy_dissipation (R G : ℝ) : ℝ := factor_RG R G   -- "continuous loss"
def mag_to_diel (X G : ℝ) : ℝ := factor_XG X G         -- "Magnetic -> Dielectric"
def diel_to_mag (R B : ℝ) : ℝ := factor_RB R B         -- "Dielectric -> Magnetic"

/-- Physical labels are just renamed factor functions. -/
theorem physical_labels_are_factors (R X G B : ℝ) :
    telegraph_product R X G B =
    Complex.mk (energy_dissipation R G + energy_storage X B)
               (mag_to_diel X G - diel_to_mag R B) := by
  unfold energy_storage energy_dissipation mag_to_diel diel_to_mag
  exact telegraph_four_factors R X G B

/-
Summary
=======
VERIFIED:
  (1) Algebraic expansion (Dollard convention):
      (R+jX)(G-jB) = (RG+XB) + j(XG-RB)                    [telegraph_expansion]
  (2) Four terms RG, XB, XG, RB appear in the expansion     [telegraph_four_factors]
  (3) Constraint: (RG)(XB) = (XG)(RB)                       [factor_constraint]

DISPROVED:
  (4) Versor form equivalence:
      h(XB+RG) + j(XG-RB) ≠ (RG+XB) + j(XG-RB)
      when h = -1. Real parts differ by sign.                [versor_form_value]
      Robust regardless of sign convention choice.

CORRECTED from original:
  - Sign convention: changed Y = G+jB to Y = G-jB to match Dollard
  - Proof tactic: replaced bare `ring` with `ext/simp/ring` for Complex
  - Removed false `factors_independent_variation` theorem (sorry gap)
  - Added `factor_constraint` showing quadratic relationship
-/
