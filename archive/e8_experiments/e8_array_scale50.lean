/-
Scale test: Array-based Fin 50 Jacobi.
Flat match took 37.5 minutes. Array should be faster if match-scanning is the bottleneck.
-/

import Mathlib.Tactic

set_option maxHeartbeats 4000000

-- Same 6 independent so(3) subalgebras as the match test, keys = i*2500+j*50+k
private def test50_data : List (Nat × Int) :=
  -- so(3) in indices 0,1,2
  [(0*2500+1*50+2, 1), (1*2500+0*50+2, -1), (0*2500+2*50+1, -1),
   (2*2500+0*50+1, 1), (1*2500+2*50+0, 1), (2*2500+1*50+0, -1),
  -- so(3) in indices 3,4,5
   (3*2500+4*50+5, 1), (4*2500+3*50+5, -1), (3*2500+5*50+4, -1),
   (5*2500+3*50+4, 1), (4*2500+5*50+3, 1), (5*2500+4*50+3, -1),
  -- so(3) in indices 6,7,8
   (6*2500+7*50+8, 1), (7*2500+6*50+8, -1), (6*2500+8*50+7, -1),
   (8*2500+6*50+7, 1), (7*2500+8*50+6, 1), (8*2500+7*50+6, -1),
  -- so(3) in indices 9,10,11
   (9*2500+10*50+11, 1), (10*2500+9*50+11, -1), (9*2500+11*50+10, -1),
   (11*2500+9*50+10, 1), (10*2500+11*50+9, 1), (11*2500+10*50+9, -1),
  -- so(3) in indices 12,13,14 (coefficient 2 on first bracket for variety)
   (12*2500+13*50+14, 2), (13*2500+12*50+14, -2), (12*2500+14*50+13, -1),
   (14*2500+12*50+13, 1), (13*2500+14*50+12, 1), (14*2500+13*50+12, -1),
  -- so(3) in indices 15,16,17
   (15*2500+16*50+17, 1), (16*2500+15*50+17, -1), (15*2500+17*50+16, -1),
   (17*2500+15*50+16, 1), (16*2500+17*50+15, 1), (17*2500+16*50+15, -1)]

private def test50_table : Array Int :=
  let base := (List.replicate 125000 (0 : Int)).toArray
  test50_data.foldl (fun acc (k, v) => acc.set! k v) base

def test50_arr (i j k : Fin 50) : Int :=
  test50_table.getD (i.val * 2500 + j.val * 50 + k.val) 0

/-- Jacobi for 50-dim via ARRAY lookup. Compare to 37.5min with flat match. -/
theorem test50_jacobi_arr : ∀ (i j k l : Fin 50),
    (Finset.univ.sum fun m => test50_arr i j m * test50_arr m k l) +
    (Finset.univ.sum fun m => test50_arr j k m * test50_arr m i l) +
    (Finset.univ.sum fun m => test50_arr k i m * test50_arr m j l) = 0 := by
  native_decide
