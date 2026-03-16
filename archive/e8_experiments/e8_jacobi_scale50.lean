/-
Scale test 3: 50-dim with ~50 match patterns (similar to E₈'s pattern density).
Fin 50⁴ = 6,250,000 evaluations.
-/

import Mathlib.Tactic

/-- 50-dim bracket with ~50 nonzero triple patterns (comparable to E₈ density). -/
def test50_f (i j k : Fin 50) : Int :=
  match i.val, j.val, k.val with
  | 0, 1, 2 => 1 | 1, 0, 2 => -1
  | 0, 2, 1 => -1 | 2, 0, 1 => 1
  | 1, 2, 0 => 1 | 2, 1, 0 => -1
  | 3, 4, 5 => 1 | 4, 3, 5 => -1
  | 3, 5, 4 => -1 | 5, 3, 4 => 1
  | 4, 5, 3 => 1 | 5, 4, 3 => -1
  | 6, 7, 8 => 1 | 7, 6, 8 => -1
  | 6, 8, 7 => -1 | 8, 6, 7 => 1
  | 7, 8, 6 => 1 | 8, 7, 6 => -1
  | 9, 10, 11 => 1 | 10, 9, 11 => -1
  | 9, 11, 10 => -1 | 11, 9, 10 => 1
  | 10, 11, 9 => 1 | 11, 10, 9 => -1
  | 12, 13, 14 => 2 | 13, 12, 14 => -2
  | 12, 14, 13 => -1 | 14, 12, 13 => 1
  | 13, 14, 12 => 1 | 14, 13, 12 => -1
  | 15, 16, 17 => 1 | 16, 15, 17 => -1
  | 15, 17, 16 => -1 | 17, 15, 16 => 1
  | 16, 17, 15 => 1 | 17, 16, 15 => -1
  | 18, 19, 20 => 1 | 19, 18, 20 => -1
  | 18, 20, 19 => -1 | 20, 18, 19 => 1
  | 19, 20, 18 => 1 | 20, 19, 18 => -1
  | 21, 22, 23 => 1 | 22, 21, 23 => -1
  | 21, 23, 22 => -1 | 23, 21, 22 => 1
  | 22, 23, 21 => 1 | 23, 22, 21 => -1
  | _, _, _ => 0

set_option maxHeartbeats 4000000

/-- Jacobi for 50-dim: 6.25M evaluations. -/
theorem test50_jacobi : ∀ (i j k l : Fin 50),
    (Finset.univ.sum fun m => test50_f i j m * test50_f m k l) +
    (Finset.univ.sum fun m => test50_f j k m * test50_f m i l) +
    (Finset.univ.sum fun m => test50_f k i m * test50_f m j l) = 0 := by
  native_decide
