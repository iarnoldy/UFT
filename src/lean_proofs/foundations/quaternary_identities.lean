/-
UFT Formal Verification - Quaternary Expansion Identities
==========================================================

Formalizes the complete identity set for the mod-4 subseries decomposition of e^t.

The four quantities u, v, x, y are defined via their closed forms:
  u(t) = (cosh(t) + cos(t))/2     "storage"
  v(t) = (cosh(t) - cos(t))/2     "return"
  x(t) = (sinh(t) + sin(t))/2     "transfer"
  y(t) = (sinh(t) - sin(t))/2     "dissipation"

Seven identities are proved:
  (1) u - v = cos(t)                [net circular]
  (2) u + v = cosh(t)               [gross circular]
  (3) x - y = sin(t)                [net hyperbolic]
  (4) x + y = sinh(t)               [gross hyperbolic]
  (5) u + x + v + y = exp(t)        [total exponential]
  (6) 4*u*v = sinh(t)^2 + sin(t)^2  [cross-energy]
  (7) 4*x*y = sinh(t)^2 - sin(t)^2  [cross-energy differential]

Tag: [OUR ANALYSIS] — derived from mod-4 subseries, not from Dollard's explicit text.
Dollard provides the quaternary decomposition pattern (eq 67-77, Versor Algebra).
These identities follow from the closed-form definitions.

References:
- Dollard, E. P. "Versor Algebra: As Applied to Polyphase Power Systems" (2015), eq 67-82
- research/dollard-investigation/2026-03-17-quaternary-identity-set.md
-/

import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Tactic

noncomputable section

open Real

-- ============================================================================
-- DEFINITIONS: The four quaternary components
-- ============================================================================

/-- The "storage" component: u(t) = (cosh(t) + cos(t))/2 -/
def quat_u (t : ℝ) : ℝ := (cosh t + cos t) / 2

/-- The "return" component: v(t) = (cosh(t) - cos(t))/2 -/
def quat_v (t : ℝ) : ℝ := (cosh t - cos t) / 2

/-- The "transfer" component: x(t) = (sinh(t) + sin(t))/2 -/
def quat_x (t : ℝ) : ℝ := (sinh t + sin t) / 2

/-- The "dissipation" component: y(t) = (sinh(t) - sin(t))/2 -/
def quat_y (t : ℝ) : ℝ := (sinh t - sin t) / 2

-- ============================================================================
-- IDENTITY 1: u - v = cos(t)  [net circular]
-- ============================================================================

/-- The difference of storage and return gives cosine (net circular oscillation). -/
theorem quaternary_diff_eq_cos (t : ℝ) : quat_u t - quat_v t = cos t := by
  simp [quat_u, quat_v]
  ring

-- ============================================================================
-- IDENTITY 2: u + v = cosh(t)  [gross circular]
-- ============================================================================

/-- The sum of storage and return gives hyperbolic cosine (gross circulation). -/
theorem quaternary_sum_eq_cosh (t : ℝ) : quat_u t + quat_v t = cosh t := by
  simp [quat_u, quat_v]
  ring

-- ============================================================================
-- IDENTITY 3: x - y = sin(t)  [net hyperbolic]
-- ============================================================================

/-- The difference of transfer and dissipation gives sine (net transfer). -/
theorem quaternary_x_diff_eq_sin (t : ℝ) : quat_x t - quat_y t = sin t := by
  simp [quat_x, quat_y]
  ring

-- ============================================================================
-- IDENTITY 4: x + y = sinh(t)  [gross hyperbolic]
-- ============================================================================

/-- The sum of transfer and dissipation gives hyperbolic sine (gross transfer). -/
theorem quaternary_x_sum_eq_sinh (t : ℝ) : quat_x t + quat_y t = sinh t := by
  simp [quat_x, quat_y]
  ring

-- ============================================================================
-- IDENTITY 5: u + x + v + y = exp(t)  [total exponential]
-- ============================================================================

/-- The sum of all four components gives the exponential.
    This uses cosh(t) + sinh(t) = exp(t). -/
theorem quaternary_total_eq_exp (t : ℝ) : quat_u t + quat_x t + quat_v t + quat_y t = exp t := by
  simp [quat_u, quat_x, quat_v, quat_y]
  have h := cosh_add_sinh t
  linarith

-- ============================================================================
-- IDENTITY 6: 4*u*v = sinh(t)^2 + sin(t)^2  [cross-energy]
-- ============================================================================

/-- The cross-energy identity: the product of storage and return components
    equals the total energy in both circular and hyperbolic modes.
    Proof: 4uv = (cosh+cos)(cosh-cos) = cosh²-cos² = sinh²+sin²
    (using cosh²-sinh²=1 and cos²+sin²=1). -/
theorem quaternary_cross_energy (t : ℝ) :
    4 * quat_u t * quat_v t = sinh t ^ 2 + sin t ^ 2 := by
  simp [quat_u, quat_v]
  have h1 : cosh t ^ 2 - sinh t ^ 2 = 1 := cosh_sq_sub_sinh_sq t
  have h2 : sin t ^ 2 + cos t ^ 2 = 1 := sin_sq_add_cos_sq t
  nlinarith [h1, h2]

-- ============================================================================
-- IDENTITY 7: 4*x*y = sinh(t)^2 - sin(t)^2  [cross-energy differential]
-- ============================================================================

/-- The cross-energy differential: the product of transfer and dissipation
    equals the difference between hyperbolic and circular mode energies.
    Proof: 4xy = (sinh+sin)(sinh-sin) = sinh²-sin² -/
theorem quaternary_cross_differential (t : ℝ) :
    4 * quat_x t * quat_y t = sinh t ^ 2 - sin t ^ 2 := by
  simp [quat_x, quat_y]
  ring

-- ============================================================================
-- BONUS: The gross/net conditioning ratio relationship
-- ============================================================================

/-- The gross is always at least as large as the absolute net (triangle inequality).
    This is the mathematical basis for the conditioning diagnostic.
    Proof: |cos t| ≤ 1 ≤ cosh t. -/
theorem gross_geq_abs_net (t : ℝ) : |quat_u t - quat_v t| ≤ quat_u t + quat_v t := by
  rw [quaternary_diff_eq_cos, quaternary_sum_eq_cosh]
  calc |cos t| ≤ 1 := abs_cos_le_one t
    _ ≤ cosh t := one_le_cosh t

/-- cosh(ln(s)) = (s + 1/s)/2 for s > 0. The SWR identity.
    This is already in mathlib as `cosh_log`; we alias it for naming clarity. -/
theorem cosh_log_eq_swr {s : ℝ} (hs : 0 < s) :
    cosh (log s) = (s + s⁻¹) / 2 :=
  cosh_log hs

end
