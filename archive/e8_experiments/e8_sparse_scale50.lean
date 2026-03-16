/-
Sparse Jacobi scale test: 50-dim algebra.
Dense array: 16.7 min. Flat match: 37.5 min.
Sparse should be MUCH faster since only 6 independent so(3) subalgebras.
-/

import Mathlib.Tactic

set_option maxHeartbeats 4000000

-- 6 independent so(3) subalgebras in a 50-dim space
-- Each so(3) has 3 nonzero bracket pairs (6 with antisymmetry)
private def test50_brackets : List (Nat × Nat × List (Nat × Int)) :=
  [-- so(3) in 0,1,2
   (0, 1, [(2, 1)]), (0, 2, [(1, -1)]), (1, 2, [(0, 1)]),
   -- so(3) in 3,4,5
   (3, 4, [(5, 1)]), (3, 5, [(4, -1)]), (4, 5, [(3, 1)]),
   -- so(3) in 6,7,8
   (6, 7, [(8, 1)]), (6, 8, [(7, -1)]), (7, 8, [(6, 1)]),
   -- so(3) in 9,10,11
   (9, 10, [(11, 1)]), (9, 11, [(10, -1)]), (10, 11, [(9, 1)]),
   -- so(3) in 12,13,14 (coeff 2 on first)
   (12, 13, [(14, 2)]), (12, 14, [(13, -1)]), (13, 14, [(12, 1)]),
   -- so(3) in 15,16,17
   (15, 16, [(17, 1)]), (15, 17, [(16, -1)]), (16, 17, [(15, 1)])]

private def test50_table : Array (List (Nat × Int)) :=
  let n := 50
  let base := (List.replicate (n * n) ([] : List (Nat × Int))).toArray
  let t := test50_brackets.foldl (fun acc (i, j, terms) =>
    acc.set! (i * n + j) terms) base
  test50_brackets.foldl (fun acc (i, j, terms) =>
    acc.set! (j * n + i) (terms.map fun (k, c) => (k, -c))) t

private def t50_bkt (i j : Nat) : List (Nat × Int) :=
  test50_table.getD (i * 50 + j) []

private def t50_jacobi_term (bkt : List (Nat × Int)) (k l : Nat) : Int :=
  bkt.foldl (fun acc (m, c_m) =>
    let f_mkl := (t50_bkt m k).foldl
      (fun a (idx, c) => if idx == l then a + c else a) 0
    acc + c_m * f_mkl) 0

def t50_sparse (i j k l : Fin 50) : Int :=
  t50_jacobi_term (t50_bkt i.val j.val) k.val l.val +
  t50_jacobi_term (t50_bkt j.val k.val) i.val l.val +
  t50_jacobi_term (t50_bkt k.val i.val) j.val l.val

/-- Sparse Jacobi for 50-dim. Dense array took 16.7 min. How fast is sparse? -/
theorem t50_sparse_jacobi : ∀ (i j k l : Fin 50),
    t50_sparse i j k l = 0 := by
  native_decide
