/-
Sparse Jacobi prototype — so(5) with 10 generators.
Instead of Finset.univ.sum (248 terms), iterate only over nonzero bracket terms (~1 term).
If this is fast, E₈ sparse Jacobi finishes in minutes, not days.
-/

import Mathlib.Tactic

set_option maxHeartbeats 800000

-- Sparse bracket data: for each (i,j), list of (k, coefficient) where [B_i, B_j] = Σ c_k B_k
-- Only upper triangle stored (i < j). Antisymmetry handled in lookup.
-- so(5) has 10 generators, 20 nonzero brackets (10 pairs × 2 for antisymmetry)
private def so5_brackets : List (Nat × Nat × List (Nat × Int)) :=
  [(0, 1, [(4, 1)]),    -- [L12, L13] = L23
   (0, 2, [(5, 1)]),    -- [L12, L14] = L24
   (0, 3, [(6, 1)]),    -- [L12, L15] = L25
   (0, 4, [(1, -1)]),   -- [L12, L23] = -L13
   (0, 5, [(2, -1)]),   -- [L12, L24] = -L14
   (0, 6, [(3, -1)]),   -- [L12, L25] = -L15
   (1, 2, [(7, 1)]),    -- [L13, L14] = L34
   (1, 3, [(8, 1)]),    -- [L13, L15] = L35
   (1, 4, [(0, 1)]),    -- [L13, L23] = L12
   (1, 7, [(2, -1)]),   -- [L13, L34] = -L14
   (1, 8, [(3, -1)]),   -- [L13, L35] = -L15
   (2, 3, [(9, 1)]),    -- [L14, L15] = L45
   (2, 5, [(0, 1)]),    -- [L14, L24] = L12
   (2, 7, [(1, 1)]),    -- [L14, L34] = L13
   (2, 9, [(3, -1)]),   -- [L14, L45] = -L15
   (3, 6, [(0, 1)]),    -- [L15, L25] = L12
   (3, 8, [(1, 1)]),    -- [L15, L35] = L13
   (3, 9, [(2, 1)]),    -- [L15, L45] = L14
   (4, 5, [(7, 1)]),    -- [L23, L24] = L34
   (4, 6, [(8, 1)]),    -- [L23, L25] = L35
   (4, 7, [(5, -1)]),   -- [L23, L34] = -L24
   (4, 8, [(6, -1)]),   -- [L23, L35] = -L25
   (5, 6, [(9, 1)]),    -- [L24, L25] = L45
   (5, 7, [(4, 1)]),    -- [L24, L34] = L23
   (5, 9, [(6, -1)]),   -- [L24, L45] = -L25
   (6, 8, [(4, 1)]),    -- [L25, L35] = L23
   (6, 9, [(5, 1)]),    -- [L25, L45] = L24
   (7, 8, [(9, 1)]),    -- [L34, L35] = L45
   (7, 9, [(8, -1)]),   -- [L34, L45] = -L35
   (8, 9, [(7, 1)])]    -- [L35, L45] = L34

-- Build lookup: flat array indexed by i*10+j, each entry is List (Nat × Int)
private def so5_bkt_table : Array (List (Nat × Int)) :=
  let base := (List.replicate 100 ([] : List (Nat × Int))).toArray
  -- Fill upper triangle
  let t := so5_brackets.foldl (fun acc (i, j, terms) => acc.set! (i * 10 + j) terms) base
  -- Fill lower triangle with negated coefficients
  so5_brackets.foldl (fun acc (i, j, terms) =>
    acc.set! (j * 10 + i) (terms.map fun (k, c) => (k, -c))) t

-- Sparse bracket lookup: returns list of (k, coefficient) for [B_i, B_j]
def so5_bkt (i j : Fin 10) : List (Nat × Int) :=
  so5_bkt_table.getD (i.val * 10 + j.val) []

-- Sparse Jacobi: only iterate over nonzero terms
-- Σ_m f(i,j,m)*f(m,k,l) using sparse bracket lists
private def sparseJacobiTerm (bkt_ij : List (Nat × Int)) (k l : Fin 10) : Int :=
  bkt_ij.foldl (fun acc (m, c_m) =>
    let f_mkl := (so5_bkt_table.getD (m * 10 + k.val) []).foldl
      (fun a (idx, c) => if idx == l.val then a + c else a) 0
    acc + c_m * f_mkl) 0

def so5_jacobi_sparse (i j k l : Fin 10) : Int :=
  sparseJacobiTerm (so5_bkt i j) k l +
  sparseJacobiTerm (so5_bkt j k) i l +
  sparseJacobiTerm (so5_bkt k i) j l

/-- Sparse Jacobi for so(5). Compare timing to dense (15s). -/
theorem so5_sparse_jacobi : ∀ (i j k l : Fin 10),
    so5_jacobi_sparse i j k l = 0 := by
  native_decide
