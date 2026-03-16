/-
Scale test: so(5) has 10 generators. Fin 10⁴ = 10,000 evaluations.
If this takes < 1 second, E₈ (248⁴ = 3.8B) takes < 380,000 seconds.
If this takes < 0.01 seconds, E₈ takes < 3,800 seconds ≈ 1 hour.
-/

import Mathlib.Tactic

/-- so(5) structure constants: [L_{ij}, L_{kl}] = δ_{jk}L_{il} - δ_{ik}L_{jl} - δ_{jl}L_{ik} + δ_{il}L_{jk}
    10 generators: L_{12}, L_{13}, L_{14}, L_{15}, L_{23}, L_{24}, L_{25}, L_{34}, L_{35}, L_{45}
    Indexed 0-9 in this order. -/
def so5_f (a b c : Fin 10) : Int :=
  -- Precomputed from so(5) bracket relations
  match a.val, b.val, c.val with
  -- [L12, L13] = L23 (indices 0,1 -> 4)
  | 0, 1, 4 => 1 | 1, 0, 4 => -1
  -- [L12, L14] = L24 (indices 0,2 -> 5)
  | 0, 2, 5 => 1 | 2, 0, 5 => -1
  -- [L12, L15] = L25 (indices 0,3 -> 6)
  | 0, 3, 6 => 1 | 3, 0, 6 => -1
  -- [L12, L23] = -L13 (indices 0,4 -> 1)
  | 0, 4, 1 => -1 | 4, 0, 1 => 1
  -- [L12, L24] = -L14 (indices 0,5 -> 2)
  | 0, 5, 2 => -1 | 5, 0, 2 => 1
  -- [L12, L25] = -L15 (indices 0,6 -> 3)
  | 0, 6, 3 => -1 | 6, 0, 3 => 1
  -- [L13, L14] = L34 (indices 1,2 -> 7)
  | 1, 2, 7 => 1 | 2, 1, 7 => -1
  -- [L13, L15] = L35 (indices 1,3 -> 8)
  | 1, 3, 8 => 1 | 3, 1, 8 => -1
  -- [L13, L23] = L12 (indices 1,4 -> 0)
  | 1, 4, 0 => 1 | 4, 1, 0 => -1
  -- [L13, L34] = -L14 (indices 1,7 -> 2)
  | 1, 7, 2 => -1 | 7, 1, 2 => 1
  -- [L13, L35] = -L15 (indices 1,8 -> 3)
  | 1, 8, 3 => -1 | 8, 1, 3 => 1
  -- [L14, L15] = L45 (indices 2,3 -> 9)
  | 2, 3, 9 => 1 | 3, 2, 9 => -1
  -- [L14, L24] = L12 (indices 2,5 -> 0)
  | 2, 5, 0 => 1 | 5, 2, 0 => -1
  -- [L14, L34] = L13 (indices 2,7 -> 1)
  | 2, 7, 1 => 1 | 7, 2, 1 => -1
  -- [L14, L45] = -L15 (indices 2,9 -> 3)
  | 2, 9, 3 => -1 | 9, 2, 3 => 1
  -- [L15, L25] = L12 (indices 3,6 -> 0)
  | 3, 6, 0 => 1 | 6, 3, 0 => -1
  -- [L15, L35] = L13 (indices 3,8 -> 1)
  | 3, 8, 1 => 1 | 8, 3, 1 => -1
  -- [L15, L45] = L14 (indices 3,9 -> 2)
  | 3, 9, 2 => 1 | 9, 3, 2 => -1
  -- [L23, L24] = L34 (indices 4,5 -> 7)
  | 4, 5, 7 => 1 | 5, 4, 7 => -1
  -- [L23, L25] = L35 (indices 4,6 -> 8)
  | 4, 6, 8 => 1 | 6, 4, 8 => -1
  -- [L23, L34] = -L24 (indices 4,7 -> 5)
  | 4, 7, 5 => -1 | 7, 4, 5 => 1
  -- [L23, L35] = -L25 (indices 4,8 -> 6)
  | 4, 8, 6 => -1 | 8, 4, 6 => 1
  -- [L24, L25] = L45 (indices 5,6 -> 9)
  | 5, 6, 9 => 1 | 6, 5, 9 => -1
  -- [L24, L34] = L23 (indices 5,7 -> 4)
  | 5, 7, 4 => 1 | 7, 5, 4 => -1
  -- [L24, L45] = -L25 (indices 5,9 -> 6)
  | 5, 9, 6 => -1 | 9, 5, 6 => 1
  -- [L25, L35] = L23 (indices 6,8 -> 4)
  | 6, 8, 4 => 1 | 8, 6, 4 => -1
  -- [L25, L45] = L24 (indices 6,9 -> 5)
  | 6, 9, 5 => 1 | 9, 6, 5 => -1
  -- [L34, L35] = L45 (indices 7,8 -> 9)
  | 7, 8, 9 => 1 | 8, 7, 9 => -1
  -- [L34, L45] = -L35 (indices 7,9 -> 8)
  | 7, 9, 8 => -1 | 9, 7, 8 => 1
  -- [L35, L45] = L34 (indices 8,9 -> 7)
  | 8, 9, 7 => 1 | 9, 8, 7 => -1
  | _, _, _ => 0

set_option maxHeartbeats 400000

/-- Jacobi identity for so(5): Fin 10⁴ = 10,000 evaluations. -/
theorem so5_jacobi : ∀ (i j k l : Fin 10),
    (Finset.univ.sum fun m => so5_f i j m * so5_f m k l) +
    (Finset.univ.sum fun m => so5_f j k m * so5_f m i l) +
    (Finset.univ.sum fun m => so5_f k i m * so5_f m j l) = 0 := by
  native_decide
