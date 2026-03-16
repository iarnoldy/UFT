/-
E₈ Antisymmetry — f(i,j,k) = -f(j,i,k)
-/

import clifford.e8_sparse_defs

set_option maxHeartbeats 16000000

open E8Sparse

/-- Structure constant lookup for a specific (i,j,k) triple. -/
def scLookup (i j k : Nat) : Int :=
  (bkt i j).foldl (fun a (idx, c) => if idx == k then a + c else a) 0

/-- E₈ bracket is antisymmetric. -/
theorem e8_antisymm : ∀ (i j k : Fin 248),
    scLookup i.val j.val k.val = -(scLookup j.val i.val k.val) := by
  native_decide
