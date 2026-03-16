/-
Test: Array-based O(1) lookup for structure constants.
-/

import Mathlib.Tactic

set_option maxHeartbeats 800000

-- so(5): 10 generators, keys precomputed as i*100+j*10+k
private def so5_data : List (Nat × Int) :=
  [(14, 1), (104, -1), (25, 1), (205, -1), (36, 1), (306, -1),
   (41, -1), (401, 1), (52, -1), (502, 1), (63, -1), (603, 1),
   (127, 1), (217, -1), (138, 1), (318, -1), (140, 1), (410, -1),
   (172, -1), (712, 1), (183, -1), (813, 1), (239, 1), (329, -1),
   (250, 1), (520, -1), (271, 1), (721, -1), (293, -1), (923, 1),
   (360, 1), (630, -1), (381, 1), (831, -1), (392, 1), (932, -1),
   (457, 1), (547, -1), (468, 1), (648, -1), (475, -1), (745, 1),
   (486, -1), (846, 1), (569, 1), (659, -1), (574, 1), (754, -1),
   (596, -1), (956, 1), (684, 1), (864, -1), (695, 1), (965, -1),
   (789, 1), (879, -1), (798, -1), (978, 1), (897, 1), (987, -1)]

private def so5_table : Array Int :=
  let base := (List.replicate 1000 (0 : Int)).toArray
  so5_data.foldl (fun acc (k, v) => acc.set! k v) base

def so5_arr (i j k : Fin 10) : Int :=
  so5_table.getD (i.val * 100 + j.val * 10 + k.val) 0

/-- Jacobi for so(5) via array lookup. -/
theorem so5_jacobi_arr : ∀ (i j k l : Fin 10),
    (Finset.univ.sum fun m => so5_arr i j m * so5_arr m k l) +
    (Finset.univ.sum fun m => so5_arr j k m * so5_arr m i l) +
    (Finset.univ.sum fun m => so5_arr k i m * so5_arr m j l) = 0 := by
  native_decide
