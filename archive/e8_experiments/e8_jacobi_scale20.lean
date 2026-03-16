/-
Scale test 2: Fake 20-dim algebra with sparse brackets.
Fin 20⁴ = 160,000 evaluations. Tests scaling behavior.
-/

import Mathlib.Tactic

/-- Sparse bracket function: only 6 nonzero pairs out of 190.
    Similar sparsity ratio to E₈ (7,752/30,628 ≈ 25%). -/
def test20_f (i j k : Fin 20) : Int :=
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
  | 12, 13, 14 => 1 | 13, 12, 14 => -1
  | 12, 14, 13 => -1 | 14, 12, 13 => 1
  | 13, 14, 12 => 1 | 14, 13, 12 => -1
  | 15, 16, 17 => 1 | 16, 15, 17 => -1
  | 15, 17, 16 => -1 | 17, 15, 16 => 1
  | 16, 17, 15 => 1 | 17, 16, 15 => -1
  | _, _, _ => 0

set_option maxHeartbeats 800000

/-- Jacobi for 20-dim algebra: 160,000 evaluations. -/
theorem test20_jacobi : ∀ (i j k l : Fin 20),
    (Finset.univ.sum fun m => test20_f i j m * test20_f m k l) +
    (Finset.univ.sum fun m => test20_f j k m * test20_f m i l) +
    (Finset.univ.sum fun m => test20_f k i m * test20_f m j l) = 0 := by
  native_decide
