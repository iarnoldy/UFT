/-
E₈ Feasibility — Multi-pair scaling test
==========================================

Tests whether native_decide scales linearly with number of pairs
for 248×248 integer matrices. Uses 3 basis pairs to compare against
single-pair timing.

If 3 pairs ≈ 3× single pair → linear scaling (predictable)
If 3 pairs ≈ 1× single pair → overhead-dominated (good news)
If 3 pairs >> 3× single pair → super-linear scaling (bad news)
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

abbrev ZMat248m := Matrix (Fin 248) (Fin 248) ℤ

-- Basis elements of so(248)
def basisM (a b : Fin 248) : ZMat248m := Matrix.of fun i j =>
  if i = a ∧ j = b then 1
  else if i = b ∧ j = a then -1
  else 0

-- Expected bracket results
-- [E_{01}, E_{02}] = -E_{12}
-- [E_{01}, E_{03}] = -E_{13}
-- [E_{02}, E_{03}] = -E_{23}

/-- Three bracket pairs verified simultaneously. -/
theorem e8_multi_bracket :
    (basisM 0 1 * basisM 0 2 - basisM 0 2 * basisM 0 1 = -(basisM 1 2)) ∧
    (basisM 0 1 * basisM 0 3 - basisM 0 3 * basisM 0 1 = -(basisM 1 3)) ∧
    (basisM 0 2 * basisM 0 3 - basisM 0 3 * basisM 0 2 = -(basisM 2 3)) := by
  native_decide
