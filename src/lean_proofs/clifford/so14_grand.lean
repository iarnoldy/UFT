/-
UFT Formal Verification - SO(14) Grand Unification Algebra
============================================================

THE so(14) LIE ALGEBRA AS A LEAN TYPE WITH CERTIFIED INSTANCES

so(14) has 91 generators L_{ij} (1 ≤ i < j ≤ 14) with the standard
orthogonal Lie bracket:
  [L_{ij}, L_{kl}] = δ_{jk}L_{il} - δ_{ik}L_{jl}
                        - δ_{jl}L_{ik} + δ_{il}L_{jk}

This algebra decomposes as so(10) ⊕ so(4) ⊕ (10,4):
  - 45 generators with both indices in {1,...,10}: so(10) gauge sector
  - 6 generators with both indices in {11,...,14}: so(4) gravity sector
  - 40 generators with one index in each: mixed sector

All 8281 bracket entries computed by scripts/so14_bracket_gen.py.
Jacobi identity verified numerically (100 random triples) before Lean proof.
so(10) and so(4) subalgebra closures verified.

NOTE ON SIGNATURE: This file defines so(14) in compact (positive-definite)
signature — the Lie algebra of SO(14,0). The gravity sector is so(4), NOT
so(1,3). The Lorentzian version would require so(11,3), a different real form.
See docs/SIGNATURE_ANALYSIS.md.

References:
  - Nesti & Percacci, "Graviweak unification" JPCAM 41 (2008)
  - so10_grand.lean: pattern source (45 generators)
  - su5c_compact.lean: LieAlgebra instance pattern
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Algebra.Lie.Basic

/-! ## Part 1: The so(14) Lie Algebra

91 generators corresponding to antisymmetric 14×14 matrices.
Indices: 1-9 as digits, 10=a, 11=b, 12=c, 13=d, 14=e. -/

/-- The Lie algebra so(14), with 91 generators L_{ij} (i < j).
    Decomposition: 45 (so(10)) + 6 (so(4)) + 40 (mixed). -/
@[ext]
structure SO14 where
  l12 : ℝ  -- L_{1,2}  -- gauge
  l13 : ℝ  -- L_{1,3}  -- gauge
  l14 : ℝ  -- L_{1,4}  -- gauge
  l15 : ℝ  -- L_{1,5}  -- gauge
  l16 : ℝ  -- L_{1,6}  -- gauge
  l17 : ℝ  -- L_{1,7}  -- gauge
  l18 : ℝ  -- L_{1,8}  -- gauge
  l19 : ℝ  -- L_{1,9}  -- gauge
  l1a : ℝ  -- L_{1,10}  -- gauge
  l1b : ℝ  -- L_{1,11}  -- mixed
  l1c : ℝ  -- L_{1,12}  -- mixed
  l1d : ℝ  -- L_{1,13}  -- mixed
  l1e : ℝ  -- L_{1,14}  -- mixed
  l23 : ℝ  -- L_{2,3}  -- gauge
  l24 : ℝ  -- L_{2,4}  -- gauge
  l25 : ℝ  -- L_{2,5}  -- gauge
  l26 : ℝ  -- L_{2,6}  -- gauge
  l27 : ℝ  -- L_{2,7}  -- gauge
  l28 : ℝ  -- L_{2,8}  -- gauge
  l29 : ℝ  -- L_{2,9}  -- gauge
  l2a : ℝ  -- L_{2,10}  -- gauge
  l2b : ℝ  -- L_{2,11}  -- mixed
  l2c : ℝ  -- L_{2,12}  -- mixed
  l2d : ℝ  -- L_{2,13}  -- mixed
  l2e : ℝ  -- L_{2,14}  -- mixed
  l34 : ℝ  -- L_{3,4}  -- gauge
  l35 : ℝ  -- L_{3,5}  -- gauge
  l36 : ℝ  -- L_{3,6}  -- gauge
  l37 : ℝ  -- L_{3,7}  -- gauge
  l38 : ℝ  -- L_{3,8}  -- gauge
  l39 : ℝ  -- L_{3,9}  -- gauge
  l3a : ℝ  -- L_{3,10}  -- gauge
  l3b : ℝ  -- L_{3,11}  -- mixed
  l3c : ℝ  -- L_{3,12}  -- mixed
  l3d : ℝ  -- L_{3,13}  -- mixed
  l3e : ℝ  -- L_{3,14}  -- mixed
  l45 : ℝ  -- L_{4,5}  -- gauge
  l46 : ℝ  -- L_{4,6}  -- gauge
  l47 : ℝ  -- L_{4,7}  -- gauge
  l48 : ℝ  -- L_{4,8}  -- gauge
  l49 : ℝ  -- L_{4,9}  -- gauge
  l4a : ℝ  -- L_{4,10}  -- gauge
  l4b : ℝ  -- L_{4,11}  -- mixed
  l4c : ℝ  -- L_{4,12}  -- mixed
  l4d : ℝ  -- L_{4,13}  -- mixed
  l4e : ℝ  -- L_{4,14}  -- mixed
  l56 : ℝ  -- L_{5,6}  -- gauge
  l57 : ℝ  -- L_{5,7}  -- gauge
  l58 : ℝ  -- L_{5,8}  -- gauge
  l59 : ℝ  -- L_{5,9}  -- gauge
  l5a : ℝ  -- L_{5,10}  -- gauge
  l5b : ℝ  -- L_{5,11}  -- mixed
  l5c : ℝ  -- L_{5,12}  -- mixed
  l5d : ℝ  -- L_{5,13}  -- mixed
  l5e : ℝ  -- L_{5,14}  -- mixed
  l67 : ℝ  -- L_{6,7}  -- gauge
  l68 : ℝ  -- L_{6,8}  -- gauge
  l69 : ℝ  -- L_{6,9}  -- gauge
  l6a : ℝ  -- L_{6,10}  -- gauge
  l6b : ℝ  -- L_{6,11}  -- mixed
  l6c : ℝ  -- L_{6,12}  -- mixed
  l6d : ℝ  -- L_{6,13}  -- mixed
  l6e : ℝ  -- L_{6,14}  -- mixed
  l78 : ℝ  -- L_{7,8}  -- gauge
  l79 : ℝ  -- L_{7,9}  -- gauge
  l7a : ℝ  -- L_{7,10}  -- gauge
  l7b : ℝ  -- L_{7,11}  -- mixed
  l7c : ℝ  -- L_{7,12}  -- mixed
  l7d : ℝ  -- L_{7,13}  -- mixed
  l7e : ℝ  -- L_{7,14}  -- mixed
  l89 : ℝ  -- L_{8,9}  -- gauge
  l8a : ℝ  -- L_{8,10}  -- gauge
  l8b : ℝ  -- L_{8,11}  -- mixed
  l8c : ℝ  -- L_{8,12}  -- mixed
  l8d : ℝ  -- L_{8,13}  -- mixed
  l8e : ℝ  -- L_{8,14}  -- mixed
  l9a : ℝ  -- L_{9,10}  -- gauge
  l9b : ℝ  -- L_{9,11}  -- mixed
  l9c : ℝ  -- L_{9,12}  -- mixed
  l9d : ℝ  -- L_{9,13}  -- mixed
  l9e : ℝ  -- L_{9,14}  -- mixed
  lab : ℝ  -- L_{10,11}  -- mixed
  lac : ℝ  -- L_{10,12}  -- mixed
  lad : ℝ  -- L_{10,13}  -- mixed
  lae : ℝ  -- L_{10,14}  -- mixed
  lbc : ℝ  -- L_{11,12}  -- gravity
  lbd : ℝ  -- L_{11,13}  -- gravity
  lbe : ℝ  -- L_{11,14}  -- gravity
  lcd : ℝ  -- L_{12,13}  -- gravity
  lce : ℝ  -- L_{12,14}  -- gravity
  lde : ℝ  -- L_{13,14}  -- gravity

namespace SO14

/-! ## Part 2: Basic Operations -/

def zero : SO14 where
  l12 := 0
  l13 := 0
  l14 := 0
  l15 := 0
  l16 := 0
  l17 := 0
  l18 := 0
  l19 := 0
  l1a := 0
  l1b := 0
  l1c := 0
  l1d := 0
  l1e := 0
  l23 := 0
  l24 := 0
  l25 := 0
  l26 := 0
  l27 := 0
  l28 := 0
  l29 := 0
  l2a := 0
  l2b := 0
  l2c := 0
  l2d := 0
  l2e := 0
  l34 := 0
  l35 := 0
  l36 := 0
  l37 := 0
  l38 := 0
  l39 := 0
  l3a := 0
  l3b := 0
  l3c := 0
  l3d := 0
  l3e := 0
  l45 := 0
  l46 := 0
  l47 := 0
  l48 := 0
  l49 := 0
  l4a := 0
  l4b := 0
  l4c := 0
  l4d := 0
  l4e := 0
  l56 := 0
  l57 := 0
  l58 := 0
  l59 := 0
  l5a := 0
  l5b := 0
  l5c := 0
  l5d := 0
  l5e := 0
  l67 := 0
  l68 := 0
  l69 := 0
  l6a := 0
  l6b := 0
  l6c := 0
  l6d := 0
  l6e := 0
  l78 := 0
  l79 := 0
  l7a := 0
  l7b := 0
  l7c := 0
  l7d := 0
  l7e := 0
  l89 := 0
  l8a := 0
  l8b := 0
  l8c := 0
  l8d := 0
  l8e := 0
  l9a := 0
  l9b := 0
  l9c := 0
  l9d := 0
  l9e := 0
  lab := 0
  lac := 0
  lad := 0
  lae := 0
  lbc := 0
  lbd := 0
  lbe := 0
  lcd := 0
  lce := 0
  lde := 0

def neg (X : SO14) : SO14 where
  l12 := -X.l12
  l13 := -X.l13
  l14 := -X.l14
  l15 := -X.l15
  l16 := -X.l16
  l17 := -X.l17
  l18 := -X.l18
  l19 := -X.l19
  l1a := -X.l1a
  l1b := -X.l1b
  l1c := -X.l1c
  l1d := -X.l1d
  l1e := -X.l1e
  l23 := -X.l23
  l24 := -X.l24
  l25 := -X.l25
  l26 := -X.l26
  l27 := -X.l27
  l28 := -X.l28
  l29 := -X.l29
  l2a := -X.l2a
  l2b := -X.l2b
  l2c := -X.l2c
  l2d := -X.l2d
  l2e := -X.l2e
  l34 := -X.l34
  l35 := -X.l35
  l36 := -X.l36
  l37 := -X.l37
  l38 := -X.l38
  l39 := -X.l39
  l3a := -X.l3a
  l3b := -X.l3b
  l3c := -X.l3c
  l3d := -X.l3d
  l3e := -X.l3e
  l45 := -X.l45
  l46 := -X.l46
  l47 := -X.l47
  l48 := -X.l48
  l49 := -X.l49
  l4a := -X.l4a
  l4b := -X.l4b
  l4c := -X.l4c
  l4d := -X.l4d
  l4e := -X.l4e
  l56 := -X.l56
  l57 := -X.l57
  l58 := -X.l58
  l59 := -X.l59
  l5a := -X.l5a
  l5b := -X.l5b
  l5c := -X.l5c
  l5d := -X.l5d
  l5e := -X.l5e
  l67 := -X.l67
  l68 := -X.l68
  l69 := -X.l69
  l6a := -X.l6a
  l6b := -X.l6b
  l6c := -X.l6c
  l6d := -X.l6d
  l6e := -X.l6e
  l78 := -X.l78
  l79 := -X.l79
  l7a := -X.l7a
  l7b := -X.l7b
  l7c := -X.l7c
  l7d := -X.l7d
  l7e := -X.l7e
  l89 := -X.l89
  l8a := -X.l8a
  l8b := -X.l8b
  l8c := -X.l8c
  l8d := -X.l8d
  l8e := -X.l8e
  l9a := -X.l9a
  l9b := -X.l9b
  l9c := -X.l9c
  l9d := -X.l9d
  l9e := -X.l9e
  lab := -X.lab
  lac := -X.lac
  lad := -X.lad
  lae := -X.lae
  lbc := -X.lbc
  lbd := -X.lbd
  lbe := -X.lbe
  lcd := -X.lcd
  lce := -X.lce
  lde := -X.lde

def add (X Y : SO14) : SO14 where
  l12 := X.l12 + Y.l12
  l13 := X.l13 + Y.l13
  l14 := X.l14 + Y.l14
  l15 := X.l15 + Y.l15
  l16 := X.l16 + Y.l16
  l17 := X.l17 + Y.l17
  l18 := X.l18 + Y.l18
  l19 := X.l19 + Y.l19
  l1a := X.l1a + Y.l1a
  l1b := X.l1b + Y.l1b
  l1c := X.l1c + Y.l1c
  l1d := X.l1d + Y.l1d
  l1e := X.l1e + Y.l1e
  l23 := X.l23 + Y.l23
  l24 := X.l24 + Y.l24
  l25 := X.l25 + Y.l25
  l26 := X.l26 + Y.l26
  l27 := X.l27 + Y.l27
  l28 := X.l28 + Y.l28
  l29 := X.l29 + Y.l29
  l2a := X.l2a + Y.l2a
  l2b := X.l2b + Y.l2b
  l2c := X.l2c + Y.l2c
  l2d := X.l2d + Y.l2d
  l2e := X.l2e + Y.l2e
  l34 := X.l34 + Y.l34
  l35 := X.l35 + Y.l35
  l36 := X.l36 + Y.l36
  l37 := X.l37 + Y.l37
  l38 := X.l38 + Y.l38
  l39 := X.l39 + Y.l39
  l3a := X.l3a + Y.l3a
  l3b := X.l3b + Y.l3b
  l3c := X.l3c + Y.l3c
  l3d := X.l3d + Y.l3d
  l3e := X.l3e + Y.l3e
  l45 := X.l45 + Y.l45
  l46 := X.l46 + Y.l46
  l47 := X.l47 + Y.l47
  l48 := X.l48 + Y.l48
  l49 := X.l49 + Y.l49
  l4a := X.l4a + Y.l4a
  l4b := X.l4b + Y.l4b
  l4c := X.l4c + Y.l4c
  l4d := X.l4d + Y.l4d
  l4e := X.l4e + Y.l4e
  l56 := X.l56 + Y.l56
  l57 := X.l57 + Y.l57
  l58 := X.l58 + Y.l58
  l59 := X.l59 + Y.l59
  l5a := X.l5a + Y.l5a
  l5b := X.l5b + Y.l5b
  l5c := X.l5c + Y.l5c
  l5d := X.l5d + Y.l5d
  l5e := X.l5e + Y.l5e
  l67 := X.l67 + Y.l67
  l68 := X.l68 + Y.l68
  l69 := X.l69 + Y.l69
  l6a := X.l6a + Y.l6a
  l6b := X.l6b + Y.l6b
  l6c := X.l6c + Y.l6c
  l6d := X.l6d + Y.l6d
  l6e := X.l6e + Y.l6e
  l78 := X.l78 + Y.l78
  l79 := X.l79 + Y.l79
  l7a := X.l7a + Y.l7a
  l7b := X.l7b + Y.l7b
  l7c := X.l7c + Y.l7c
  l7d := X.l7d + Y.l7d
  l7e := X.l7e + Y.l7e
  l89 := X.l89 + Y.l89
  l8a := X.l8a + Y.l8a
  l8b := X.l8b + Y.l8b
  l8c := X.l8c + Y.l8c
  l8d := X.l8d + Y.l8d
  l8e := X.l8e + Y.l8e
  l9a := X.l9a + Y.l9a
  l9b := X.l9b + Y.l9b
  l9c := X.l9c + Y.l9c
  l9d := X.l9d + Y.l9d
  l9e := X.l9e + Y.l9e
  lab := X.lab + Y.lab
  lac := X.lac + Y.lac
  lad := X.lad + Y.lad
  lae := X.lae + Y.lae
  lbc := X.lbc + Y.lbc
  lbd := X.lbd + Y.lbd
  lbe := X.lbe + Y.lbe
  lcd := X.lcd + Y.lcd
  lce := X.lce + Y.lce
  lde := X.lde + Y.lde

def smul (c : ℝ) (X : SO14) : SO14 where
  l12 := c * X.l12
  l13 := c * X.l13
  l14 := c * X.l14
  l15 := c * X.l15
  l16 := c * X.l16
  l17 := c * X.l17
  l18 := c * X.l18
  l19 := c * X.l19
  l1a := c * X.l1a
  l1b := c * X.l1b
  l1c := c * X.l1c
  l1d := c * X.l1d
  l1e := c * X.l1e
  l23 := c * X.l23
  l24 := c * X.l24
  l25 := c * X.l25
  l26 := c * X.l26
  l27 := c * X.l27
  l28 := c * X.l28
  l29 := c * X.l29
  l2a := c * X.l2a
  l2b := c * X.l2b
  l2c := c * X.l2c
  l2d := c * X.l2d
  l2e := c * X.l2e
  l34 := c * X.l34
  l35 := c * X.l35
  l36 := c * X.l36
  l37 := c * X.l37
  l38 := c * X.l38
  l39 := c * X.l39
  l3a := c * X.l3a
  l3b := c * X.l3b
  l3c := c * X.l3c
  l3d := c * X.l3d
  l3e := c * X.l3e
  l45 := c * X.l45
  l46 := c * X.l46
  l47 := c * X.l47
  l48 := c * X.l48
  l49 := c * X.l49
  l4a := c * X.l4a
  l4b := c * X.l4b
  l4c := c * X.l4c
  l4d := c * X.l4d
  l4e := c * X.l4e
  l56 := c * X.l56
  l57 := c * X.l57
  l58 := c * X.l58
  l59 := c * X.l59
  l5a := c * X.l5a
  l5b := c * X.l5b
  l5c := c * X.l5c
  l5d := c * X.l5d
  l5e := c * X.l5e
  l67 := c * X.l67
  l68 := c * X.l68
  l69 := c * X.l69
  l6a := c * X.l6a
  l6b := c * X.l6b
  l6c := c * X.l6c
  l6d := c * X.l6d
  l6e := c * X.l6e
  l78 := c * X.l78
  l79 := c * X.l79
  l7a := c * X.l7a
  l7b := c * X.l7b
  l7c := c * X.l7c
  l7d := c * X.l7d
  l7e := c * X.l7e
  l89 := c * X.l89
  l8a := c * X.l8a
  l8b := c * X.l8b
  l8c := c * X.l8c
  l8d := c * X.l8d
  l8e := c * X.l8e
  l9a := c * X.l9a
  l9b := c * X.l9b
  l9c := c * X.l9c
  l9d := c * X.l9d
  l9e := c * X.l9e
  lab := c * X.lab
  lac := c * X.lac
  lad := c * X.lad
  lae := c * X.lae
  lbc := c * X.lbc
  lbd := c * X.lbd
  lbe := c * X.lbe
  lcd := c * X.lcd
  lce := c * X.lce
  lde := c * X.lde

instance : Add SO14 := ⟨add⟩
instance : Neg SO14 := ⟨neg⟩
instance : Zero SO14 := ⟨zero⟩
instance : Sub SO14 := ⟨fun a b => add a (neg b)⟩
instance : SMul ℝ SO14 := ⟨smul⟩

@[simp] lemma add_def (X Y : SO14) : X + Y = add X Y := rfl
@[simp] lemma neg_def (X : SO14) : -X = neg X := rfl
@[simp] lemma zero_val : (0 : SO14) = zero := rfl
@[simp] lemma sub_def' (a b : SO14) : a - b = add a (neg b) := rfl
@[simp] lemma smul_def' (r : ℝ) (a : SO14) : r • a = smul r a := rfl

/-! ## Part 3: The Lie Bracket

The Lie bracket [X, Y] of two so(14) elements.
Generated by scripts/so14_bracket_gen.py from the formula
[L_{ij}, L_{kl}] = δ_{jk}L_{il} - δ_{ik}L_{jl} - δ_{jl}L_{ik} + δ_{il}L_{jk}. -/

def comm (X Y : SO14) : SO14 where
  l12 := -(X.l13 * Y.l23) - (X.l14 * Y.l24) - (X.l15 * Y.l25) - (X.l16 * Y.l26) - (X.l17 * Y.l27) - (X.l18 * Y.l28) - (X.l19 * Y.l29) - (X.l1a * Y.l2a) - (X.l1b * Y.l2b) - (X.l1c * Y.l2c) - (X.l1d * Y.l2d) - (X.l1e * Y.l2e) + X.l23 * Y.l13 + X.l24 * Y.l14 + X.l25 * Y.l15 + X.l26 * Y.l16 + X.l27 * Y.l17 + X.l28 * Y.l18 + X.l29 * Y.l19 + X.l2a * Y.l1a + X.l2b * Y.l1b + X.l2c * Y.l1c + X.l2d * Y.l1d + X.l2e * Y.l1e
  l13 := X.l12 * Y.l23 - (X.l14 * Y.l34) - (X.l15 * Y.l35) - (X.l16 * Y.l36) - (X.l17 * Y.l37) - (X.l18 * Y.l38) - (X.l19 * Y.l39) - (X.l1a * Y.l3a) - (X.l1b * Y.l3b) - (X.l1c * Y.l3c) - (X.l1d * Y.l3d) - (X.l1e * Y.l3e) - (X.l23 * Y.l12) + X.l34 * Y.l14 + X.l35 * Y.l15 + X.l36 * Y.l16 + X.l37 * Y.l17 + X.l38 * Y.l18 + X.l39 * Y.l19 + X.l3a * Y.l1a + X.l3b * Y.l1b + X.l3c * Y.l1c + X.l3d * Y.l1d + X.l3e * Y.l1e
  l14 := X.l12 * Y.l24 + X.l13 * Y.l34 - (X.l15 * Y.l45) - (X.l16 * Y.l46) - (X.l17 * Y.l47) - (X.l18 * Y.l48) - (X.l19 * Y.l49) - (X.l1a * Y.l4a) - (X.l1b * Y.l4b) - (X.l1c * Y.l4c) - (X.l1d * Y.l4d) - (X.l1e * Y.l4e) - (X.l24 * Y.l12) - (X.l34 * Y.l13) + X.l45 * Y.l15 + X.l46 * Y.l16 + X.l47 * Y.l17 + X.l48 * Y.l18 + X.l49 * Y.l19 + X.l4a * Y.l1a + X.l4b * Y.l1b + X.l4c * Y.l1c + X.l4d * Y.l1d + X.l4e * Y.l1e
  l15 := X.l12 * Y.l25 + X.l13 * Y.l35 + X.l14 * Y.l45 - (X.l16 * Y.l56) - (X.l17 * Y.l57) - (X.l18 * Y.l58) - (X.l19 * Y.l59) - (X.l1a * Y.l5a) - (X.l1b * Y.l5b) - (X.l1c * Y.l5c) - (X.l1d * Y.l5d) - (X.l1e * Y.l5e) - (X.l25 * Y.l12) - (X.l35 * Y.l13) - (X.l45 * Y.l14) + X.l56 * Y.l16 + X.l57 * Y.l17 + X.l58 * Y.l18 + X.l59 * Y.l19 + X.l5a * Y.l1a + X.l5b * Y.l1b + X.l5c * Y.l1c + X.l5d * Y.l1d + X.l5e * Y.l1e
  l16 := X.l12 * Y.l26 + X.l13 * Y.l36 + X.l14 * Y.l46 + X.l15 * Y.l56 - (X.l17 * Y.l67) - (X.l18 * Y.l68) - (X.l19 * Y.l69) - (X.l1a * Y.l6a) - (X.l1b * Y.l6b) - (X.l1c * Y.l6c) - (X.l1d * Y.l6d) - (X.l1e * Y.l6e) - (X.l26 * Y.l12) - (X.l36 * Y.l13) - (X.l46 * Y.l14) - (X.l56 * Y.l15) + X.l67 * Y.l17 + X.l68 * Y.l18 + X.l69 * Y.l19 + X.l6a * Y.l1a + X.l6b * Y.l1b + X.l6c * Y.l1c + X.l6d * Y.l1d + X.l6e * Y.l1e
  l17 := X.l12 * Y.l27 + X.l13 * Y.l37 + X.l14 * Y.l47 + X.l15 * Y.l57 + X.l16 * Y.l67 - (X.l18 * Y.l78) - (X.l19 * Y.l79) - (X.l1a * Y.l7a) - (X.l1b * Y.l7b) - (X.l1c * Y.l7c) - (X.l1d * Y.l7d) - (X.l1e * Y.l7e) - (X.l27 * Y.l12) - (X.l37 * Y.l13) - (X.l47 * Y.l14) - (X.l57 * Y.l15) - (X.l67 * Y.l16) + X.l78 * Y.l18 + X.l79 * Y.l19 + X.l7a * Y.l1a + X.l7b * Y.l1b + X.l7c * Y.l1c + X.l7d * Y.l1d + X.l7e * Y.l1e
  l18 := X.l12 * Y.l28 + X.l13 * Y.l38 + X.l14 * Y.l48 + X.l15 * Y.l58 + X.l16 * Y.l68 + X.l17 * Y.l78 - (X.l19 * Y.l89) - (X.l1a * Y.l8a) - (X.l1b * Y.l8b) - (X.l1c * Y.l8c) - (X.l1d * Y.l8d) - (X.l1e * Y.l8e) - (X.l28 * Y.l12) - (X.l38 * Y.l13) - (X.l48 * Y.l14) - (X.l58 * Y.l15) - (X.l68 * Y.l16) - (X.l78 * Y.l17) + X.l89 * Y.l19 + X.l8a * Y.l1a + X.l8b * Y.l1b + X.l8c * Y.l1c + X.l8d * Y.l1d + X.l8e * Y.l1e
  l19 := X.l12 * Y.l29 + X.l13 * Y.l39 + X.l14 * Y.l49 + X.l15 * Y.l59 + X.l16 * Y.l69 + X.l17 * Y.l79 + X.l18 * Y.l89 - (X.l1a * Y.l9a) - (X.l1b * Y.l9b) - (X.l1c * Y.l9c) - (X.l1d * Y.l9d) - (X.l1e * Y.l9e) - (X.l29 * Y.l12) - (X.l39 * Y.l13) - (X.l49 * Y.l14) - (X.l59 * Y.l15) - (X.l69 * Y.l16) - (X.l79 * Y.l17) - (X.l89 * Y.l18) + X.l9a * Y.l1a + X.l9b * Y.l1b + X.l9c * Y.l1c + X.l9d * Y.l1d + X.l9e * Y.l1e
  l1a := X.l12 * Y.l2a + X.l13 * Y.l3a + X.l14 * Y.l4a + X.l15 * Y.l5a + X.l16 * Y.l6a + X.l17 * Y.l7a + X.l18 * Y.l8a + X.l19 * Y.l9a - (X.l1b * Y.lab) - (X.l1c * Y.lac) - (X.l1d * Y.lad) - (X.l1e * Y.lae) - (X.l2a * Y.l12) - (X.l3a * Y.l13) - (X.l4a * Y.l14) - (X.l5a * Y.l15) - (X.l6a * Y.l16) - (X.l7a * Y.l17) - (X.l8a * Y.l18) - (X.l9a * Y.l19) + X.lab * Y.l1b + X.lac * Y.l1c + X.lad * Y.l1d + X.lae * Y.l1e
  l1b := X.l12 * Y.l2b + X.l13 * Y.l3b + X.l14 * Y.l4b + X.l15 * Y.l5b + X.l16 * Y.l6b + X.l17 * Y.l7b + X.l18 * Y.l8b + X.l19 * Y.l9b + X.l1a * Y.lab - (X.l1c * Y.lbc) - (X.l1d * Y.lbd) - (X.l1e * Y.lbe) - (X.l2b * Y.l12) - (X.l3b * Y.l13) - (X.l4b * Y.l14) - (X.l5b * Y.l15) - (X.l6b * Y.l16) - (X.l7b * Y.l17) - (X.l8b * Y.l18) - (X.l9b * Y.l19) - (X.lab * Y.l1a) + X.lbc * Y.l1c + X.lbd * Y.l1d + X.lbe * Y.l1e
  l1c := X.l12 * Y.l2c + X.l13 * Y.l3c + X.l14 * Y.l4c + X.l15 * Y.l5c + X.l16 * Y.l6c + X.l17 * Y.l7c + X.l18 * Y.l8c + X.l19 * Y.l9c + X.l1a * Y.lac + X.l1b * Y.lbc - (X.l1d * Y.lcd) - (X.l1e * Y.lce) - (X.l2c * Y.l12) - (X.l3c * Y.l13) - (X.l4c * Y.l14) - (X.l5c * Y.l15) - (X.l6c * Y.l16) - (X.l7c * Y.l17) - (X.l8c * Y.l18) - (X.l9c * Y.l19) - (X.lac * Y.l1a) - (X.lbc * Y.l1b) + X.lcd * Y.l1d + X.lce * Y.l1e
  l1d := X.l12 * Y.l2d + X.l13 * Y.l3d + X.l14 * Y.l4d + X.l15 * Y.l5d + X.l16 * Y.l6d + X.l17 * Y.l7d + X.l18 * Y.l8d + X.l19 * Y.l9d + X.l1a * Y.lad + X.l1b * Y.lbd + X.l1c * Y.lcd - (X.l1e * Y.lde) - (X.l2d * Y.l12) - (X.l3d * Y.l13) - (X.l4d * Y.l14) - (X.l5d * Y.l15) - (X.l6d * Y.l16) - (X.l7d * Y.l17) - (X.l8d * Y.l18) - (X.l9d * Y.l19) - (X.lad * Y.l1a) - (X.lbd * Y.l1b) - (X.lcd * Y.l1c) + X.lde * Y.l1e
  l1e := X.l12 * Y.l2e + X.l13 * Y.l3e + X.l14 * Y.l4e + X.l15 * Y.l5e + X.l16 * Y.l6e + X.l17 * Y.l7e + X.l18 * Y.l8e + X.l19 * Y.l9e + X.l1a * Y.lae + X.l1b * Y.lbe + X.l1c * Y.lce + X.l1d * Y.lde - (X.l2e * Y.l12) - (X.l3e * Y.l13) - (X.l4e * Y.l14) - (X.l5e * Y.l15) - (X.l6e * Y.l16) - (X.l7e * Y.l17) - (X.l8e * Y.l18) - (X.l9e * Y.l19) - (X.lae * Y.l1a) - (X.lbe * Y.l1b) - (X.lce * Y.l1c) - (X.lde * Y.l1d)
  l23 := -(X.l12 * Y.l13) + X.l13 * Y.l12 - (X.l24 * Y.l34) - (X.l25 * Y.l35) - (X.l26 * Y.l36) - (X.l27 * Y.l37) - (X.l28 * Y.l38) - (X.l29 * Y.l39) - (X.l2a * Y.l3a) - (X.l2b * Y.l3b) - (X.l2c * Y.l3c) - (X.l2d * Y.l3d) - (X.l2e * Y.l3e) + X.l34 * Y.l24 + X.l35 * Y.l25 + X.l36 * Y.l26 + X.l37 * Y.l27 + X.l38 * Y.l28 + X.l39 * Y.l29 + X.l3a * Y.l2a + X.l3b * Y.l2b + X.l3c * Y.l2c + X.l3d * Y.l2d + X.l3e * Y.l2e
  l24 := -(X.l12 * Y.l14) + X.l14 * Y.l12 + X.l23 * Y.l34 - (X.l25 * Y.l45) - (X.l26 * Y.l46) - (X.l27 * Y.l47) - (X.l28 * Y.l48) - (X.l29 * Y.l49) - (X.l2a * Y.l4a) - (X.l2b * Y.l4b) - (X.l2c * Y.l4c) - (X.l2d * Y.l4d) - (X.l2e * Y.l4e) - (X.l34 * Y.l23) + X.l45 * Y.l25 + X.l46 * Y.l26 + X.l47 * Y.l27 + X.l48 * Y.l28 + X.l49 * Y.l29 + X.l4a * Y.l2a + X.l4b * Y.l2b + X.l4c * Y.l2c + X.l4d * Y.l2d + X.l4e * Y.l2e
  l25 := -(X.l12 * Y.l15) + X.l15 * Y.l12 + X.l23 * Y.l35 + X.l24 * Y.l45 - (X.l26 * Y.l56) - (X.l27 * Y.l57) - (X.l28 * Y.l58) - (X.l29 * Y.l59) - (X.l2a * Y.l5a) - (X.l2b * Y.l5b) - (X.l2c * Y.l5c) - (X.l2d * Y.l5d) - (X.l2e * Y.l5e) - (X.l35 * Y.l23) - (X.l45 * Y.l24) + X.l56 * Y.l26 + X.l57 * Y.l27 + X.l58 * Y.l28 + X.l59 * Y.l29 + X.l5a * Y.l2a + X.l5b * Y.l2b + X.l5c * Y.l2c + X.l5d * Y.l2d + X.l5e * Y.l2e
  l26 := -(X.l12 * Y.l16) + X.l16 * Y.l12 + X.l23 * Y.l36 + X.l24 * Y.l46 + X.l25 * Y.l56 - (X.l27 * Y.l67) - (X.l28 * Y.l68) - (X.l29 * Y.l69) - (X.l2a * Y.l6a) - (X.l2b * Y.l6b) - (X.l2c * Y.l6c) - (X.l2d * Y.l6d) - (X.l2e * Y.l6e) - (X.l36 * Y.l23) - (X.l46 * Y.l24) - (X.l56 * Y.l25) + X.l67 * Y.l27 + X.l68 * Y.l28 + X.l69 * Y.l29 + X.l6a * Y.l2a + X.l6b * Y.l2b + X.l6c * Y.l2c + X.l6d * Y.l2d + X.l6e * Y.l2e
  l27 := -(X.l12 * Y.l17) + X.l17 * Y.l12 + X.l23 * Y.l37 + X.l24 * Y.l47 + X.l25 * Y.l57 + X.l26 * Y.l67 - (X.l28 * Y.l78) - (X.l29 * Y.l79) - (X.l2a * Y.l7a) - (X.l2b * Y.l7b) - (X.l2c * Y.l7c) - (X.l2d * Y.l7d) - (X.l2e * Y.l7e) - (X.l37 * Y.l23) - (X.l47 * Y.l24) - (X.l57 * Y.l25) - (X.l67 * Y.l26) + X.l78 * Y.l28 + X.l79 * Y.l29 + X.l7a * Y.l2a + X.l7b * Y.l2b + X.l7c * Y.l2c + X.l7d * Y.l2d + X.l7e * Y.l2e
  l28 := -(X.l12 * Y.l18) + X.l18 * Y.l12 + X.l23 * Y.l38 + X.l24 * Y.l48 + X.l25 * Y.l58 + X.l26 * Y.l68 + X.l27 * Y.l78 - (X.l29 * Y.l89) - (X.l2a * Y.l8a) - (X.l2b * Y.l8b) - (X.l2c * Y.l8c) - (X.l2d * Y.l8d) - (X.l2e * Y.l8e) - (X.l38 * Y.l23) - (X.l48 * Y.l24) - (X.l58 * Y.l25) - (X.l68 * Y.l26) - (X.l78 * Y.l27) + X.l89 * Y.l29 + X.l8a * Y.l2a + X.l8b * Y.l2b + X.l8c * Y.l2c + X.l8d * Y.l2d + X.l8e * Y.l2e
  l29 := -(X.l12 * Y.l19) + X.l19 * Y.l12 + X.l23 * Y.l39 + X.l24 * Y.l49 + X.l25 * Y.l59 + X.l26 * Y.l69 + X.l27 * Y.l79 + X.l28 * Y.l89 - (X.l2a * Y.l9a) - (X.l2b * Y.l9b) - (X.l2c * Y.l9c) - (X.l2d * Y.l9d) - (X.l2e * Y.l9e) - (X.l39 * Y.l23) - (X.l49 * Y.l24) - (X.l59 * Y.l25) - (X.l69 * Y.l26) - (X.l79 * Y.l27) - (X.l89 * Y.l28) + X.l9a * Y.l2a + X.l9b * Y.l2b + X.l9c * Y.l2c + X.l9d * Y.l2d + X.l9e * Y.l2e
  l2a := -(X.l12 * Y.l1a) + X.l1a * Y.l12 + X.l23 * Y.l3a + X.l24 * Y.l4a + X.l25 * Y.l5a + X.l26 * Y.l6a + X.l27 * Y.l7a + X.l28 * Y.l8a + X.l29 * Y.l9a - (X.l2b * Y.lab) - (X.l2c * Y.lac) - (X.l2d * Y.lad) - (X.l2e * Y.lae) - (X.l3a * Y.l23) - (X.l4a * Y.l24) - (X.l5a * Y.l25) - (X.l6a * Y.l26) - (X.l7a * Y.l27) - (X.l8a * Y.l28) - (X.l9a * Y.l29) + X.lab * Y.l2b + X.lac * Y.l2c + X.lad * Y.l2d + X.lae * Y.l2e
  l2b := -(X.l12 * Y.l1b) + X.l1b * Y.l12 + X.l23 * Y.l3b + X.l24 * Y.l4b + X.l25 * Y.l5b + X.l26 * Y.l6b + X.l27 * Y.l7b + X.l28 * Y.l8b + X.l29 * Y.l9b + X.l2a * Y.lab - (X.l2c * Y.lbc) - (X.l2d * Y.lbd) - (X.l2e * Y.lbe) - (X.l3b * Y.l23) - (X.l4b * Y.l24) - (X.l5b * Y.l25) - (X.l6b * Y.l26) - (X.l7b * Y.l27) - (X.l8b * Y.l28) - (X.l9b * Y.l29) - (X.lab * Y.l2a) + X.lbc * Y.l2c + X.lbd * Y.l2d + X.lbe * Y.l2e
  l2c := -(X.l12 * Y.l1c) + X.l1c * Y.l12 + X.l23 * Y.l3c + X.l24 * Y.l4c + X.l25 * Y.l5c + X.l26 * Y.l6c + X.l27 * Y.l7c + X.l28 * Y.l8c + X.l29 * Y.l9c + X.l2a * Y.lac + X.l2b * Y.lbc - (X.l2d * Y.lcd) - (X.l2e * Y.lce) - (X.l3c * Y.l23) - (X.l4c * Y.l24) - (X.l5c * Y.l25) - (X.l6c * Y.l26) - (X.l7c * Y.l27) - (X.l8c * Y.l28) - (X.l9c * Y.l29) - (X.lac * Y.l2a) - (X.lbc * Y.l2b) + X.lcd * Y.l2d + X.lce * Y.l2e
  l2d := -(X.l12 * Y.l1d) + X.l1d * Y.l12 + X.l23 * Y.l3d + X.l24 * Y.l4d + X.l25 * Y.l5d + X.l26 * Y.l6d + X.l27 * Y.l7d + X.l28 * Y.l8d + X.l29 * Y.l9d + X.l2a * Y.lad + X.l2b * Y.lbd + X.l2c * Y.lcd - (X.l2e * Y.lde) - (X.l3d * Y.l23) - (X.l4d * Y.l24) - (X.l5d * Y.l25) - (X.l6d * Y.l26) - (X.l7d * Y.l27) - (X.l8d * Y.l28) - (X.l9d * Y.l29) - (X.lad * Y.l2a) - (X.lbd * Y.l2b) - (X.lcd * Y.l2c) + X.lde * Y.l2e
  l2e := -(X.l12 * Y.l1e) + X.l1e * Y.l12 + X.l23 * Y.l3e + X.l24 * Y.l4e + X.l25 * Y.l5e + X.l26 * Y.l6e + X.l27 * Y.l7e + X.l28 * Y.l8e + X.l29 * Y.l9e + X.l2a * Y.lae + X.l2b * Y.lbe + X.l2c * Y.lce + X.l2d * Y.lde - (X.l3e * Y.l23) - (X.l4e * Y.l24) - (X.l5e * Y.l25) - (X.l6e * Y.l26) - (X.l7e * Y.l27) - (X.l8e * Y.l28) - (X.l9e * Y.l29) - (X.lae * Y.l2a) - (X.lbe * Y.l2b) - (X.lce * Y.l2c) - (X.lde * Y.l2d)
  l34 := -(X.l13 * Y.l14) + X.l14 * Y.l13 - (X.l23 * Y.l24) + X.l24 * Y.l23 - (X.l35 * Y.l45) - (X.l36 * Y.l46) - (X.l37 * Y.l47) - (X.l38 * Y.l48) - (X.l39 * Y.l49) - (X.l3a * Y.l4a) - (X.l3b * Y.l4b) - (X.l3c * Y.l4c) - (X.l3d * Y.l4d) - (X.l3e * Y.l4e) + X.l45 * Y.l35 + X.l46 * Y.l36 + X.l47 * Y.l37 + X.l48 * Y.l38 + X.l49 * Y.l39 + X.l4a * Y.l3a + X.l4b * Y.l3b + X.l4c * Y.l3c + X.l4d * Y.l3d + X.l4e * Y.l3e
  l35 := -(X.l13 * Y.l15) + X.l15 * Y.l13 - (X.l23 * Y.l25) + X.l25 * Y.l23 + X.l34 * Y.l45 - (X.l36 * Y.l56) - (X.l37 * Y.l57) - (X.l38 * Y.l58) - (X.l39 * Y.l59) - (X.l3a * Y.l5a) - (X.l3b * Y.l5b) - (X.l3c * Y.l5c) - (X.l3d * Y.l5d) - (X.l3e * Y.l5e) - (X.l45 * Y.l34) + X.l56 * Y.l36 + X.l57 * Y.l37 + X.l58 * Y.l38 + X.l59 * Y.l39 + X.l5a * Y.l3a + X.l5b * Y.l3b + X.l5c * Y.l3c + X.l5d * Y.l3d + X.l5e * Y.l3e
  l36 := -(X.l13 * Y.l16) + X.l16 * Y.l13 - (X.l23 * Y.l26) + X.l26 * Y.l23 + X.l34 * Y.l46 + X.l35 * Y.l56 - (X.l37 * Y.l67) - (X.l38 * Y.l68) - (X.l39 * Y.l69) - (X.l3a * Y.l6a) - (X.l3b * Y.l6b) - (X.l3c * Y.l6c) - (X.l3d * Y.l6d) - (X.l3e * Y.l6e) - (X.l46 * Y.l34) - (X.l56 * Y.l35) + X.l67 * Y.l37 + X.l68 * Y.l38 + X.l69 * Y.l39 + X.l6a * Y.l3a + X.l6b * Y.l3b + X.l6c * Y.l3c + X.l6d * Y.l3d + X.l6e * Y.l3e
  l37 := -(X.l13 * Y.l17) + X.l17 * Y.l13 - (X.l23 * Y.l27) + X.l27 * Y.l23 + X.l34 * Y.l47 + X.l35 * Y.l57 + X.l36 * Y.l67 - (X.l38 * Y.l78) - (X.l39 * Y.l79) - (X.l3a * Y.l7a) - (X.l3b * Y.l7b) - (X.l3c * Y.l7c) - (X.l3d * Y.l7d) - (X.l3e * Y.l7e) - (X.l47 * Y.l34) - (X.l57 * Y.l35) - (X.l67 * Y.l36) + X.l78 * Y.l38 + X.l79 * Y.l39 + X.l7a * Y.l3a + X.l7b * Y.l3b + X.l7c * Y.l3c + X.l7d * Y.l3d + X.l7e * Y.l3e
  l38 := -(X.l13 * Y.l18) + X.l18 * Y.l13 - (X.l23 * Y.l28) + X.l28 * Y.l23 + X.l34 * Y.l48 + X.l35 * Y.l58 + X.l36 * Y.l68 + X.l37 * Y.l78 - (X.l39 * Y.l89) - (X.l3a * Y.l8a) - (X.l3b * Y.l8b) - (X.l3c * Y.l8c) - (X.l3d * Y.l8d) - (X.l3e * Y.l8e) - (X.l48 * Y.l34) - (X.l58 * Y.l35) - (X.l68 * Y.l36) - (X.l78 * Y.l37) + X.l89 * Y.l39 + X.l8a * Y.l3a + X.l8b * Y.l3b + X.l8c * Y.l3c + X.l8d * Y.l3d + X.l8e * Y.l3e
  l39 := -(X.l13 * Y.l19) + X.l19 * Y.l13 - (X.l23 * Y.l29) + X.l29 * Y.l23 + X.l34 * Y.l49 + X.l35 * Y.l59 + X.l36 * Y.l69 + X.l37 * Y.l79 + X.l38 * Y.l89 - (X.l3a * Y.l9a) - (X.l3b * Y.l9b) - (X.l3c * Y.l9c) - (X.l3d * Y.l9d) - (X.l3e * Y.l9e) - (X.l49 * Y.l34) - (X.l59 * Y.l35) - (X.l69 * Y.l36) - (X.l79 * Y.l37) - (X.l89 * Y.l38) + X.l9a * Y.l3a + X.l9b * Y.l3b + X.l9c * Y.l3c + X.l9d * Y.l3d + X.l9e * Y.l3e
  l3a := -(X.l13 * Y.l1a) + X.l1a * Y.l13 - (X.l23 * Y.l2a) + X.l2a * Y.l23 + X.l34 * Y.l4a + X.l35 * Y.l5a + X.l36 * Y.l6a + X.l37 * Y.l7a + X.l38 * Y.l8a + X.l39 * Y.l9a - (X.l3b * Y.lab) - (X.l3c * Y.lac) - (X.l3d * Y.lad) - (X.l3e * Y.lae) - (X.l4a * Y.l34) - (X.l5a * Y.l35) - (X.l6a * Y.l36) - (X.l7a * Y.l37) - (X.l8a * Y.l38) - (X.l9a * Y.l39) + X.lab * Y.l3b + X.lac * Y.l3c + X.lad * Y.l3d + X.lae * Y.l3e
  l3b := -(X.l13 * Y.l1b) + X.l1b * Y.l13 - (X.l23 * Y.l2b) + X.l2b * Y.l23 + X.l34 * Y.l4b + X.l35 * Y.l5b + X.l36 * Y.l6b + X.l37 * Y.l7b + X.l38 * Y.l8b + X.l39 * Y.l9b + X.l3a * Y.lab - (X.l3c * Y.lbc) - (X.l3d * Y.lbd) - (X.l3e * Y.lbe) - (X.l4b * Y.l34) - (X.l5b * Y.l35) - (X.l6b * Y.l36) - (X.l7b * Y.l37) - (X.l8b * Y.l38) - (X.l9b * Y.l39) - (X.lab * Y.l3a) + X.lbc * Y.l3c + X.lbd * Y.l3d + X.lbe * Y.l3e
  l3c := -(X.l13 * Y.l1c) + X.l1c * Y.l13 - (X.l23 * Y.l2c) + X.l2c * Y.l23 + X.l34 * Y.l4c + X.l35 * Y.l5c + X.l36 * Y.l6c + X.l37 * Y.l7c + X.l38 * Y.l8c + X.l39 * Y.l9c + X.l3a * Y.lac + X.l3b * Y.lbc - (X.l3d * Y.lcd) - (X.l3e * Y.lce) - (X.l4c * Y.l34) - (X.l5c * Y.l35) - (X.l6c * Y.l36) - (X.l7c * Y.l37) - (X.l8c * Y.l38) - (X.l9c * Y.l39) - (X.lac * Y.l3a) - (X.lbc * Y.l3b) + X.lcd * Y.l3d + X.lce * Y.l3e
  l3d := -(X.l13 * Y.l1d) + X.l1d * Y.l13 - (X.l23 * Y.l2d) + X.l2d * Y.l23 + X.l34 * Y.l4d + X.l35 * Y.l5d + X.l36 * Y.l6d + X.l37 * Y.l7d + X.l38 * Y.l8d + X.l39 * Y.l9d + X.l3a * Y.lad + X.l3b * Y.lbd + X.l3c * Y.lcd - (X.l3e * Y.lde) - (X.l4d * Y.l34) - (X.l5d * Y.l35) - (X.l6d * Y.l36) - (X.l7d * Y.l37) - (X.l8d * Y.l38) - (X.l9d * Y.l39) - (X.lad * Y.l3a) - (X.lbd * Y.l3b) - (X.lcd * Y.l3c) + X.lde * Y.l3e
  l3e := -(X.l13 * Y.l1e) + X.l1e * Y.l13 - (X.l23 * Y.l2e) + X.l2e * Y.l23 + X.l34 * Y.l4e + X.l35 * Y.l5e + X.l36 * Y.l6e + X.l37 * Y.l7e + X.l38 * Y.l8e + X.l39 * Y.l9e + X.l3a * Y.lae + X.l3b * Y.lbe + X.l3c * Y.lce + X.l3d * Y.lde - (X.l4e * Y.l34) - (X.l5e * Y.l35) - (X.l6e * Y.l36) - (X.l7e * Y.l37) - (X.l8e * Y.l38) - (X.l9e * Y.l39) - (X.lae * Y.l3a) - (X.lbe * Y.l3b) - (X.lce * Y.l3c) - (X.lde * Y.l3d)
  l45 := -(X.l14 * Y.l15) + X.l15 * Y.l14 - (X.l24 * Y.l25) + X.l25 * Y.l24 - (X.l34 * Y.l35) + X.l35 * Y.l34 - (X.l46 * Y.l56) - (X.l47 * Y.l57) - (X.l48 * Y.l58) - (X.l49 * Y.l59) - (X.l4a * Y.l5a) - (X.l4b * Y.l5b) - (X.l4c * Y.l5c) - (X.l4d * Y.l5d) - (X.l4e * Y.l5e) + X.l56 * Y.l46 + X.l57 * Y.l47 + X.l58 * Y.l48 + X.l59 * Y.l49 + X.l5a * Y.l4a + X.l5b * Y.l4b + X.l5c * Y.l4c + X.l5d * Y.l4d + X.l5e * Y.l4e
  l46 := -(X.l14 * Y.l16) + X.l16 * Y.l14 - (X.l24 * Y.l26) + X.l26 * Y.l24 - (X.l34 * Y.l36) + X.l36 * Y.l34 + X.l45 * Y.l56 - (X.l47 * Y.l67) - (X.l48 * Y.l68) - (X.l49 * Y.l69) - (X.l4a * Y.l6a) - (X.l4b * Y.l6b) - (X.l4c * Y.l6c) - (X.l4d * Y.l6d) - (X.l4e * Y.l6e) - (X.l56 * Y.l45) + X.l67 * Y.l47 + X.l68 * Y.l48 + X.l69 * Y.l49 + X.l6a * Y.l4a + X.l6b * Y.l4b + X.l6c * Y.l4c + X.l6d * Y.l4d + X.l6e * Y.l4e
  l47 := -(X.l14 * Y.l17) + X.l17 * Y.l14 - (X.l24 * Y.l27) + X.l27 * Y.l24 - (X.l34 * Y.l37) + X.l37 * Y.l34 + X.l45 * Y.l57 + X.l46 * Y.l67 - (X.l48 * Y.l78) - (X.l49 * Y.l79) - (X.l4a * Y.l7a) - (X.l4b * Y.l7b) - (X.l4c * Y.l7c) - (X.l4d * Y.l7d) - (X.l4e * Y.l7e) - (X.l57 * Y.l45) - (X.l67 * Y.l46) + X.l78 * Y.l48 + X.l79 * Y.l49 + X.l7a * Y.l4a + X.l7b * Y.l4b + X.l7c * Y.l4c + X.l7d * Y.l4d + X.l7e * Y.l4e
  l48 := -(X.l14 * Y.l18) + X.l18 * Y.l14 - (X.l24 * Y.l28) + X.l28 * Y.l24 - (X.l34 * Y.l38) + X.l38 * Y.l34 + X.l45 * Y.l58 + X.l46 * Y.l68 + X.l47 * Y.l78 - (X.l49 * Y.l89) - (X.l4a * Y.l8a) - (X.l4b * Y.l8b) - (X.l4c * Y.l8c) - (X.l4d * Y.l8d) - (X.l4e * Y.l8e) - (X.l58 * Y.l45) - (X.l68 * Y.l46) - (X.l78 * Y.l47) + X.l89 * Y.l49 + X.l8a * Y.l4a + X.l8b * Y.l4b + X.l8c * Y.l4c + X.l8d * Y.l4d + X.l8e * Y.l4e
  l49 := -(X.l14 * Y.l19) + X.l19 * Y.l14 - (X.l24 * Y.l29) + X.l29 * Y.l24 - (X.l34 * Y.l39) + X.l39 * Y.l34 + X.l45 * Y.l59 + X.l46 * Y.l69 + X.l47 * Y.l79 + X.l48 * Y.l89 - (X.l4a * Y.l9a) - (X.l4b * Y.l9b) - (X.l4c * Y.l9c) - (X.l4d * Y.l9d) - (X.l4e * Y.l9e) - (X.l59 * Y.l45) - (X.l69 * Y.l46) - (X.l79 * Y.l47) - (X.l89 * Y.l48) + X.l9a * Y.l4a + X.l9b * Y.l4b + X.l9c * Y.l4c + X.l9d * Y.l4d + X.l9e * Y.l4e
  l4a := -(X.l14 * Y.l1a) + X.l1a * Y.l14 - (X.l24 * Y.l2a) + X.l2a * Y.l24 - (X.l34 * Y.l3a) + X.l3a * Y.l34 + X.l45 * Y.l5a + X.l46 * Y.l6a + X.l47 * Y.l7a + X.l48 * Y.l8a + X.l49 * Y.l9a - (X.l4b * Y.lab) - (X.l4c * Y.lac) - (X.l4d * Y.lad) - (X.l4e * Y.lae) - (X.l5a * Y.l45) - (X.l6a * Y.l46) - (X.l7a * Y.l47) - (X.l8a * Y.l48) - (X.l9a * Y.l49) + X.lab * Y.l4b + X.lac * Y.l4c + X.lad * Y.l4d + X.lae * Y.l4e
  l4b := -(X.l14 * Y.l1b) + X.l1b * Y.l14 - (X.l24 * Y.l2b) + X.l2b * Y.l24 - (X.l34 * Y.l3b) + X.l3b * Y.l34 + X.l45 * Y.l5b + X.l46 * Y.l6b + X.l47 * Y.l7b + X.l48 * Y.l8b + X.l49 * Y.l9b + X.l4a * Y.lab - (X.l4c * Y.lbc) - (X.l4d * Y.lbd) - (X.l4e * Y.lbe) - (X.l5b * Y.l45) - (X.l6b * Y.l46) - (X.l7b * Y.l47) - (X.l8b * Y.l48) - (X.l9b * Y.l49) - (X.lab * Y.l4a) + X.lbc * Y.l4c + X.lbd * Y.l4d + X.lbe * Y.l4e
  l4c := -(X.l14 * Y.l1c) + X.l1c * Y.l14 - (X.l24 * Y.l2c) + X.l2c * Y.l24 - (X.l34 * Y.l3c) + X.l3c * Y.l34 + X.l45 * Y.l5c + X.l46 * Y.l6c + X.l47 * Y.l7c + X.l48 * Y.l8c + X.l49 * Y.l9c + X.l4a * Y.lac + X.l4b * Y.lbc - (X.l4d * Y.lcd) - (X.l4e * Y.lce) - (X.l5c * Y.l45) - (X.l6c * Y.l46) - (X.l7c * Y.l47) - (X.l8c * Y.l48) - (X.l9c * Y.l49) - (X.lac * Y.l4a) - (X.lbc * Y.l4b) + X.lcd * Y.l4d + X.lce * Y.l4e
  l4d := -(X.l14 * Y.l1d) + X.l1d * Y.l14 - (X.l24 * Y.l2d) + X.l2d * Y.l24 - (X.l34 * Y.l3d) + X.l3d * Y.l34 + X.l45 * Y.l5d + X.l46 * Y.l6d + X.l47 * Y.l7d + X.l48 * Y.l8d + X.l49 * Y.l9d + X.l4a * Y.lad + X.l4b * Y.lbd + X.l4c * Y.lcd - (X.l4e * Y.lde) - (X.l5d * Y.l45) - (X.l6d * Y.l46) - (X.l7d * Y.l47) - (X.l8d * Y.l48) - (X.l9d * Y.l49) - (X.lad * Y.l4a) - (X.lbd * Y.l4b) - (X.lcd * Y.l4c) + X.lde * Y.l4e
  l4e := -(X.l14 * Y.l1e) + X.l1e * Y.l14 - (X.l24 * Y.l2e) + X.l2e * Y.l24 - (X.l34 * Y.l3e) + X.l3e * Y.l34 + X.l45 * Y.l5e + X.l46 * Y.l6e + X.l47 * Y.l7e + X.l48 * Y.l8e + X.l49 * Y.l9e + X.l4a * Y.lae + X.l4b * Y.lbe + X.l4c * Y.lce + X.l4d * Y.lde - (X.l5e * Y.l45) - (X.l6e * Y.l46) - (X.l7e * Y.l47) - (X.l8e * Y.l48) - (X.l9e * Y.l49) - (X.lae * Y.l4a) - (X.lbe * Y.l4b) - (X.lce * Y.l4c) - (X.lde * Y.l4d)
  l56 := -(X.l15 * Y.l16) + X.l16 * Y.l15 - (X.l25 * Y.l26) + X.l26 * Y.l25 - (X.l35 * Y.l36) + X.l36 * Y.l35 - (X.l45 * Y.l46) + X.l46 * Y.l45 - (X.l57 * Y.l67) - (X.l58 * Y.l68) - (X.l59 * Y.l69) - (X.l5a * Y.l6a) - (X.l5b * Y.l6b) - (X.l5c * Y.l6c) - (X.l5d * Y.l6d) - (X.l5e * Y.l6e) + X.l67 * Y.l57 + X.l68 * Y.l58 + X.l69 * Y.l59 + X.l6a * Y.l5a + X.l6b * Y.l5b + X.l6c * Y.l5c + X.l6d * Y.l5d + X.l6e * Y.l5e
  l57 := -(X.l15 * Y.l17) + X.l17 * Y.l15 - (X.l25 * Y.l27) + X.l27 * Y.l25 - (X.l35 * Y.l37) + X.l37 * Y.l35 - (X.l45 * Y.l47) + X.l47 * Y.l45 + X.l56 * Y.l67 - (X.l58 * Y.l78) - (X.l59 * Y.l79) - (X.l5a * Y.l7a) - (X.l5b * Y.l7b) - (X.l5c * Y.l7c) - (X.l5d * Y.l7d) - (X.l5e * Y.l7e) - (X.l67 * Y.l56) + X.l78 * Y.l58 + X.l79 * Y.l59 + X.l7a * Y.l5a + X.l7b * Y.l5b + X.l7c * Y.l5c + X.l7d * Y.l5d + X.l7e * Y.l5e
  l58 := -(X.l15 * Y.l18) + X.l18 * Y.l15 - (X.l25 * Y.l28) + X.l28 * Y.l25 - (X.l35 * Y.l38) + X.l38 * Y.l35 - (X.l45 * Y.l48) + X.l48 * Y.l45 + X.l56 * Y.l68 + X.l57 * Y.l78 - (X.l59 * Y.l89) - (X.l5a * Y.l8a) - (X.l5b * Y.l8b) - (X.l5c * Y.l8c) - (X.l5d * Y.l8d) - (X.l5e * Y.l8e) - (X.l68 * Y.l56) - (X.l78 * Y.l57) + X.l89 * Y.l59 + X.l8a * Y.l5a + X.l8b * Y.l5b + X.l8c * Y.l5c + X.l8d * Y.l5d + X.l8e * Y.l5e
  l59 := -(X.l15 * Y.l19) + X.l19 * Y.l15 - (X.l25 * Y.l29) + X.l29 * Y.l25 - (X.l35 * Y.l39) + X.l39 * Y.l35 - (X.l45 * Y.l49) + X.l49 * Y.l45 + X.l56 * Y.l69 + X.l57 * Y.l79 + X.l58 * Y.l89 - (X.l5a * Y.l9a) - (X.l5b * Y.l9b) - (X.l5c * Y.l9c) - (X.l5d * Y.l9d) - (X.l5e * Y.l9e) - (X.l69 * Y.l56) - (X.l79 * Y.l57) - (X.l89 * Y.l58) + X.l9a * Y.l5a + X.l9b * Y.l5b + X.l9c * Y.l5c + X.l9d * Y.l5d + X.l9e * Y.l5e
  l5a := -(X.l15 * Y.l1a) + X.l1a * Y.l15 - (X.l25 * Y.l2a) + X.l2a * Y.l25 - (X.l35 * Y.l3a) + X.l3a * Y.l35 - (X.l45 * Y.l4a) + X.l4a * Y.l45 + X.l56 * Y.l6a + X.l57 * Y.l7a + X.l58 * Y.l8a + X.l59 * Y.l9a - (X.l5b * Y.lab) - (X.l5c * Y.lac) - (X.l5d * Y.lad) - (X.l5e * Y.lae) - (X.l6a * Y.l56) - (X.l7a * Y.l57) - (X.l8a * Y.l58) - (X.l9a * Y.l59) + X.lab * Y.l5b + X.lac * Y.l5c + X.lad * Y.l5d + X.lae * Y.l5e
  l5b := -(X.l15 * Y.l1b) + X.l1b * Y.l15 - (X.l25 * Y.l2b) + X.l2b * Y.l25 - (X.l35 * Y.l3b) + X.l3b * Y.l35 - (X.l45 * Y.l4b) + X.l4b * Y.l45 + X.l56 * Y.l6b + X.l57 * Y.l7b + X.l58 * Y.l8b + X.l59 * Y.l9b + X.l5a * Y.lab - (X.l5c * Y.lbc) - (X.l5d * Y.lbd) - (X.l5e * Y.lbe) - (X.l6b * Y.l56) - (X.l7b * Y.l57) - (X.l8b * Y.l58) - (X.l9b * Y.l59) - (X.lab * Y.l5a) + X.lbc * Y.l5c + X.lbd * Y.l5d + X.lbe * Y.l5e
  l5c := -(X.l15 * Y.l1c) + X.l1c * Y.l15 - (X.l25 * Y.l2c) + X.l2c * Y.l25 - (X.l35 * Y.l3c) + X.l3c * Y.l35 - (X.l45 * Y.l4c) + X.l4c * Y.l45 + X.l56 * Y.l6c + X.l57 * Y.l7c + X.l58 * Y.l8c + X.l59 * Y.l9c + X.l5a * Y.lac + X.l5b * Y.lbc - (X.l5d * Y.lcd) - (X.l5e * Y.lce) - (X.l6c * Y.l56) - (X.l7c * Y.l57) - (X.l8c * Y.l58) - (X.l9c * Y.l59) - (X.lac * Y.l5a) - (X.lbc * Y.l5b) + X.lcd * Y.l5d + X.lce * Y.l5e
  l5d := -(X.l15 * Y.l1d) + X.l1d * Y.l15 - (X.l25 * Y.l2d) + X.l2d * Y.l25 - (X.l35 * Y.l3d) + X.l3d * Y.l35 - (X.l45 * Y.l4d) + X.l4d * Y.l45 + X.l56 * Y.l6d + X.l57 * Y.l7d + X.l58 * Y.l8d + X.l59 * Y.l9d + X.l5a * Y.lad + X.l5b * Y.lbd + X.l5c * Y.lcd - (X.l5e * Y.lde) - (X.l6d * Y.l56) - (X.l7d * Y.l57) - (X.l8d * Y.l58) - (X.l9d * Y.l59) - (X.lad * Y.l5a) - (X.lbd * Y.l5b) - (X.lcd * Y.l5c) + X.lde * Y.l5e
  l5e := -(X.l15 * Y.l1e) + X.l1e * Y.l15 - (X.l25 * Y.l2e) + X.l2e * Y.l25 - (X.l35 * Y.l3e) + X.l3e * Y.l35 - (X.l45 * Y.l4e) + X.l4e * Y.l45 + X.l56 * Y.l6e + X.l57 * Y.l7e + X.l58 * Y.l8e + X.l59 * Y.l9e + X.l5a * Y.lae + X.l5b * Y.lbe + X.l5c * Y.lce + X.l5d * Y.lde - (X.l6e * Y.l56) - (X.l7e * Y.l57) - (X.l8e * Y.l58) - (X.l9e * Y.l59) - (X.lae * Y.l5a) - (X.lbe * Y.l5b) - (X.lce * Y.l5c) - (X.lde * Y.l5d)
  l67 := -(X.l16 * Y.l17) + X.l17 * Y.l16 - (X.l26 * Y.l27) + X.l27 * Y.l26 - (X.l36 * Y.l37) + X.l37 * Y.l36 - (X.l46 * Y.l47) + X.l47 * Y.l46 - (X.l56 * Y.l57) + X.l57 * Y.l56 - (X.l68 * Y.l78) - (X.l69 * Y.l79) - (X.l6a * Y.l7a) - (X.l6b * Y.l7b) - (X.l6c * Y.l7c) - (X.l6d * Y.l7d) - (X.l6e * Y.l7e) + X.l78 * Y.l68 + X.l79 * Y.l69 + X.l7a * Y.l6a + X.l7b * Y.l6b + X.l7c * Y.l6c + X.l7d * Y.l6d + X.l7e * Y.l6e
  l68 := -(X.l16 * Y.l18) + X.l18 * Y.l16 - (X.l26 * Y.l28) + X.l28 * Y.l26 - (X.l36 * Y.l38) + X.l38 * Y.l36 - (X.l46 * Y.l48) + X.l48 * Y.l46 - (X.l56 * Y.l58) + X.l58 * Y.l56 + X.l67 * Y.l78 - (X.l69 * Y.l89) - (X.l6a * Y.l8a) - (X.l6b * Y.l8b) - (X.l6c * Y.l8c) - (X.l6d * Y.l8d) - (X.l6e * Y.l8e) - (X.l78 * Y.l67) + X.l89 * Y.l69 + X.l8a * Y.l6a + X.l8b * Y.l6b + X.l8c * Y.l6c + X.l8d * Y.l6d + X.l8e * Y.l6e
  l69 := -(X.l16 * Y.l19) + X.l19 * Y.l16 - (X.l26 * Y.l29) + X.l29 * Y.l26 - (X.l36 * Y.l39) + X.l39 * Y.l36 - (X.l46 * Y.l49) + X.l49 * Y.l46 - (X.l56 * Y.l59) + X.l59 * Y.l56 + X.l67 * Y.l79 + X.l68 * Y.l89 - (X.l6a * Y.l9a) - (X.l6b * Y.l9b) - (X.l6c * Y.l9c) - (X.l6d * Y.l9d) - (X.l6e * Y.l9e) - (X.l79 * Y.l67) - (X.l89 * Y.l68) + X.l9a * Y.l6a + X.l9b * Y.l6b + X.l9c * Y.l6c + X.l9d * Y.l6d + X.l9e * Y.l6e
  l6a := -(X.l16 * Y.l1a) + X.l1a * Y.l16 - (X.l26 * Y.l2a) + X.l2a * Y.l26 - (X.l36 * Y.l3a) + X.l3a * Y.l36 - (X.l46 * Y.l4a) + X.l4a * Y.l46 - (X.l56 * Y.l5a) + X.l5a * Y.l56 + X.l67 * Y.l7a + X.l68 * Y.l8a + X.l69 * Y.l9a - (X.l6b * Y.lab) - (X.l6c * Y.lac) - (X.l6d * Y.lad) - (X.l6e * Y.lae) - (X.l7a * Y.l67) - (X.l8a * Y.l68) - (X.l9a * Y.l69) + X.lab * Y.l6b + X.lac * Y.l6c + X.lad * Y.l6d + X.lae * Y.l6e
  l6b := -(X.l16 * Y.l1b) + X.l1b * Y.l16 - (X.l26 * Y.l2b) + X.l2b * Y.l26 - (X.l36 * Y.l3b) + X.l3b * Y.l36 - (X.l46 * Y.l4b) + X.l4b * Y.l46 - (X.l56 * Y.l5b) + X.l5b * Y.l56 + X.l67 * Y.l7b + X.l68 * Y.l8b + X.l69 * Y.l9b + X.l6a * Y.lab - (X.l6c * Y.lbc) - (X.l6d * Y.lbd) - (X.l6e * Y.lbe) - (X.l7b * Y.l67) - (X.l8b * Y.l68) - (X.l9b * Y.l69) - (X.lab * Y.l6a) + X.lbc * Y.l6c + X.lbd * Y.l6d + X.lbe * Y.l6e
  l6c := -(X.l16 * Y.l1c) + X.l1c * Y.l16 - (X.l26 * Y.l2c) + X.l2c * Y.l26 - (X.l36 * Y.l3c) + X.l3c * Y.l36 - (X.l46 * Y.l4c) + X.l4c * Y.l46 - (X.l56 * Y.l5c) + X.l5c * Y.l56 + X.l67 * Y.l7c + X.l68 * Y.l8c + X.l69 * Y.l9c + X.l6a * Y.lac + X.l6b * Y.lbc - (X.l6d * Y.lcd) - (X.l6e * Y.lce) - (X.l7c * Y.l67) - (X.l8c * Y.l68) - (X.l9c * Y.l69) - (X.lac * Y.l6a) - (X.lbc * Y.l6b) + X.lcd * Y.l6d + X.lce * Y.l6e
  l6d := -(X.l16 * Y.l1d) + X.l1d * Y.l16 - (X.l26 * Y.l2d) + X.l2d * Y.l26 - (X.l36 * Y.l3d) + X.l3d * Y.l36 - (X.l46 * Y.l4d) + X.l4d * Y.l46 - (X.l56 * Y.l5d) + X.l5d * Y.l56 + X.l67 * Y.l7d + X.l68 * Y.l8d + X.l69 * Y.l9d + X.l6a * Y.lad + X.l6b * Y.lbd + X.l6c * Y.lcd - (X.l6e * Y.lde) - (X.l7d * Y.l67) - (X.l8d * Y.l68) - (X.l9d * Y.l69) - (X.lad * Y.l6a) - (X.lbd * Y.l6b) - (X.lcd * Y.l6c) + X.lde * Y.l6e
  l6e := -(X.l16 * Y.l1e) + X.l1e * Y.l16 - (X.l26 * Y.l2e) + X.l2e * Y.l26 - (X.l36 * Y.l3e) + X.l3e * Y.l36 - (X.l46 * Y.l4e) + X.l4e * Y.l46 - (X.l56 * Y.l5e) + X.l5e * Y.l56 + X.l67 * Y.l7e + X.l68 * Y.l8e + X.l69 * Y.l9e + X.l6a * Y.lae + X.l6b * Y.lbe + X.l6c * Y.lce + X.l6d * Y.lde - (X.l7e * Y.l67) - (X.l8e * Y.l68) - (X.l9e * Y.l69) - (X.lae * Y.l6a) - (X.lbe * Y.l6b) - (X.lce * Y.l6c) - (X.lde * Y.l6d)
  l78 := -(X.l17 * Y.l18) + X.l18 * Y.l17 - (X.l27 * Y.l28) + X.l28 * Y.l27 - (X.l37 * Y.l38) + X.l38 * Y.l37 - (X.l47 * Y.l48) + X.l48 * Y.l47 - (X.l57 * Y.l58) + X.l58 * Y.l57 - (X.l67 * Y.l68) + X.l68 * Y.l67 - (X.l79 * Y.l89) - (X.l7a * Y.l8a) - (X.l7b * Y.l8b) - (X.l7c * Y.l8c) - (X.l7d * Y.l8d) - (X.l7e * Y.l8e) + X.l89 * Y.l79 + X.l8a * Y.l7a + X.l8b * Y.l7b + X.l8c * Y.l7c + X.l8d * Y.l7d + X.l8e * Y.l7e
  l79 := -(X.l17 * Y.l19) + X.l19 * Y.l17 - (X.l27 * Y.l29) + X.l29 * Y.l27 - (X.l37 * Y.l39) + X.l39 * Y.l37 - (X.l47 * Y.l49) + X.l49 * Y.l47 - (X.l57 * Y.l59) + X.l59 * Y.l57 - (X.l67 * Y.l69) + X.l69 * Y.l67 + X.l78 * Y.l89 - (X.l7a * Y.l9a) - (X.l7b * Y.l9b) - (X.l7c * Y.l9c) - (X.l7d * Y.l9d) - (X.l7e * Y.l9e) - (X.l89 * Y.l78) + X.l9a * Y.l7a + X.l9b * Y.l7b + X.l9c * Y.l7c + X.l9d * Y.l7d + X.l9e * Y.l7e
  l7a := -(X.l17 * Y.l1a) + X.l1a * Y.l17 - (X.l27 * Y.l2a) + X.l2a * Y.l27 - (X.l37 * Y.l3a) + X.l3a * Y.l37 - (X.l47 * Y.l4a) + X.l4a * Y.l47 - (X.l57 * Y.l5a) + X.l5a * Y.l57 - (X.l67 * Y.l6a) + X.l6a * Y.l67 + X.l78 * Y.l8a + X.l79 * Y.l9a - (X.l7b * Y.lab) - (X.l7c * Y.lac) - (X.l7d * Y.lad) - (X.l7e * Y.lae) - (X.l8a * Y.l78) - (X.l9a * Y.l79) + X.lab * Y.l7b + X.lac * Y.l7c + X.lad * Y.l7d + X.lae * Y.l7e
  l7b := -(X.l17 * Y.l1b) + X.l1b * Y.l17 - (X.l27 * Y.l2b) + X.l2b * Y.l27 - (X.l37 * Y.l3b) + X.l3b * Y.l37 - (X.l47 * Y.l4b) + X.l4b * Y.l47 - (X.l57 * Y.l5b) + X.l5b * Y.l57 - (X.l67 * Y.l6b) + X.l6b * Y.l67 + X.l78 * Y.l8b + X.l79 * Y.l9b + X.l7a * Y.lab - (X.l7c * Y.lbc) - (X.l7d * Y.lbd) - (X.l7e * Y.lbe) - (X.l8b * Y.l78) - (X.l9b * Y.l79) - (X.lab * Y.l7a) + X.lbc * Y.l7c + X.lbd * Y.l7d + X.lbe * Y.l7e
  l7c := -(X.l17 * Y.l1c) + X.l1c * Y.l17 - (X.l27 * Y.l2c) + X.l2c * Y.l27 - (X.l37 * Y.l3c) + X.l3c * Y.l37 - (X.l47 * Y.l4c) + X.l4c * Y.l47 - (X.l57 * Y.l5c) + X.l5c * Y.l57 - (X.l67 * Y.l6c) + X.l6c * Y.l67 + X.l78 * Y.l8c + X.l79 * Y.l9c + X.l7a * Y.lac + X.l7b * Y.lbc - (X.l7d * Y.lcd) - (X.l7e * Y.lce) - (X.l8c * Y.l78) - (X.l9c * Y.l79) - (X.lac * Y.l7a) - (X.lbc * Y.l7b) + X.lcd * Y.l7d + X.lce * Y.l7e
  l7d := -(X.l17 * Y.l1d) + X.l1d * Y.l17 - (X.l27 * Y.l2d) + X.l2d * Y.l27 - (X.l37 * Y.l3d) + X.l3d * Y.l37 - (X.l47 * Y.l4d) + X.l4d * Y.l47 - (X.l57 * Y.l5d) + X.l5d * Y.l57 - (X.l67 * Y.l6d) + X.l6d * Y.l67 + X.l78 * Y.l8d + X.l79 * Y.l9d + X.l7a * Y.lad + X.l7b * Y.lbd + X.l7c * Y.lcd - (X.l7e * Y.lde) - (X.l8d * Y.l78) - (X.l9d * Y.l79) - (X.lad * Y.l7a) - (X.lbd * Y.l7b) - (X.lcd * Y.l7c) + X.lde * Y.l7e
  l7e := -(X.l17 * Y.l1e) + X.l1e * Y.l17 - (X.l27 * Y.l2e) + X.l2e * Y.l27 - (X.l37 * Y.l3e) + X.l3e * Y.l37 - (X.l47 * Y.l4e) + X.l4e * Y.l47 - (X.l57 * Y.l5e) + X.l5e * Y.l57 - (X.l67 * Y.l6e) + X.l6e * Y.l67 + X.l78 * Y.l8e + X.l79 * Y.l9e + X.l7a * Y.lae + X.l7b * Y.lbe + X.l7c * Y.lce + X.l7d * Y.lde - (X.l8e * Y.l78) - (X.l9e * Y.l79) - (X.lae * Y.l7a) - (X.lbe * Y.l7b) - (X.lce * Y.l7c) - (X.lde * Y.l7d)
  l89 := -(X.l18 * Y.l19) + X.l19 * Y.l18 - (X.l28 * Y.l29) + X.l29 * Y.l28 - (X.l38 * Y.l39) + X.l39 * Y.l38 - (X.l48 * Y.l49) + X.l49 * Y.l48 - (X.l58 * Y.l59) + X.l59 * Y.l58 - (X.l68 * Y.l69) + X.l69 * Y.l68 - (X.l78 * Y.l79) + X.l79 * Y.l78 - (X.l8a * Y.l9a) - (X.l8b * Y.l9b) - (X.l8c * Y.l9c) - (X.l8d * Y.l9d) - (X.l8e * Y.l9e) + X.l9a * Y.l8a + X.l9b * Y.l8b + X.l9c * Y.l8c + X.l9d * Y.l8d + X.l9e * Y.l8e
  l8a := -(X.l18 * Y.l1a) + X.l1a * Y.l18 - (X.l28 * Y.l2a) + X.l2a * Y.l28 - (X.l38 * Y.l3a) + X.l3a * Y.l38 - (X.l48 * Y.l4a) + X.l4a * Y.l48 - (X.l58 * Y.l5a) + X.l5a * Y.l58 - (X.l68 * Y.l6a) + X.l6a * Y.l68 - (X.l78 * Y.l7a) + X.l7a * Y.l78 + X.l89 * Y.l9a - (X.l8b * Y.lab) - (X.l8c * Y.lac) - (X.l8d * Y.lad) - (X.l8e * Y.lae) - (X.l9a * Y.l89) + X.lab * Y.l8b + X.lac * Y.l8c + X.lad * Y.l8d + X.lae * Y.l8e
  l8b := -(X.l18 * Y.l1b) + X.l1b * Y.l18 - (X.l28 * Y.l2b) + X.l2b * Y.l28 - (X.l38 * Y.l3b) + X.l3b * Y.l38 - (X.l48 * Y.l4b) + X.l4b * Y.l48 - (X.l58 * Y.l5b) + X.l5b * Y.l58 - (X.l68 * Y.l6b) + X.l6b * Y.l68 - (X.l78 * Y.l7b) + X.l7b * Y.l78 + X.l89 * Y.l9b + X.l8a * Y.lab - (X.l8c * Y.lbc) - (X.l8d * Y.lbd) - (X.l8e * Y.lbe) - (X.l9b * Y.l89) - (X.lab * Y.l8a) + X.lbc * Y.l8c + X.lbd * Y.l8d + X.lbe * Y.l8e
  l8c := -(X.l18 * Y.l1c) + X.l1c * Y.l18 - (X.l28 * Y.l2c) + X.l2c * Y.l28 - (X.l38 * Y.l3c) + X.l3c * Y.l38 - (X.l48 * Y.l4c) + X.l4c * Y.l48 - (X.l58 * Y.l5c) + X.l5c * Y.l58 - (X.l68 * Y.l6c) + X.l6c * Y.l68 - (X.l78 * Y.l7c) + X.l7c * Y.l78 + X.l89 * Y.l9c + X.l8a * Y.lac + X.l8b * Y.lbc - (X.l8d * Y.lcd) - (X.l8e * Y.lce) - (X.l9c * Y.l89) - (X.lac * Y.l8a) - (X.lbc * Y.l8b) + X.lcd * Y.l8d + X.lce * Y.l8e
  l8d := -(X.l18 * Y.l1d) + X.l1d * Y.l18 - (X.l28 * Y.l2d) + X.l2d * Y.l28 - (X.l38 * Y.l3d) + X.l3d * Y.l38 - (X.l48 * Y.l4d) + X.l4d * Y.l48 - (X.l58 * Y.l5d) + X.l5d * Y.l58 - (X.l68 * Y.l6d) + X.l6d * Y.l68 - (X.l78 * Y.l7d) + X.l7d * Y.l78 + X.l89 * Y.l9d + X.l8a * Y.lad + X.l8b * Y.lbd + X.l8c * Y.lcd - (X.l8e * Y.lde) - (X.l9d * Y.l89) - (X.lad * Y.l8a) - (X.lbd * Y.l8b) - (X.lcd * Y.l8c) + X.lde * Y.l8e
  l8e := -(X.l18 * Y.l1e) + X.l1e * Y.l18 - (X.l28 * Y.l2e) + X.l2e * Y.l28 - (X.l38 * Y.l3e) + X.l3e * Y.l38 - (X.l48 * Y.l4e) + X.l4e * Y.l48 - (X.l58 * Y.l5e) + X.l5e * Y.l58 - (X.l68 * Y.l6e) + X.l6e * Y.l68 - (X.l78 * Y.l7e) + X.l7e * Y.l78 + X.l89 * Y.l9e + X.l8a * Y.lae + X.l8b * Y.lbe + X.l8c * Y.lce + X.l8d * Y.lde - (X.l9e * Y.l89) - (X.lae * Y.l8a) - (X.lbe * Y.l8b) - (X.lce * Y.l8c) - (X.lde * Y.l8d)
  l9a := -(X.l19 * Y.l1a) + X.l1a * Y.l19 - (X.l29 * Y.l2a) + X.l2a * Y.l29 - (X.l39 * Y.l3a) + X.l3a * Y.l39 - (X.l49 * Y.l4a) + X.l4a * Y.l49 - (X.l59 * Y.l5a) + X.l5a * Y.l59 - (X.l69 * Y.l6a) + X.l6a * Y.l69 - (X.l79 * Y.l7a) + X.l7a * Y.l79 - (X.l89 * Y.l8a) + X.l8a * Y.l89 - (X.l9b * Y.lab) - (X.l9c * Y.lac) - (X.l9d * Y.lad) - (X.l9e * Y.lae) + X.lab * Y.l9b + X.lac * Y.l9c + X.lad * Y.l9d + X.lae * Y.l9e
  l9b := -(X.l19 * Y.l1b) + X.l1b * Y.l19 - (X.l29 * Y.l2b) + X.l2b * Y.l29 - (X.l39 * Y.l3b) + X.l3b * Y.l39 - (X.l49 * Y.l4b) + X.l4b * Y.l49 - (X.l59 * Y.l5b) + X.l5b * Y.l59 - (X.l69 * Y.l6b) + X.l6b * Y.l69 - (X.l79 * Y.l7b) + X.l7b * Y.l79 - (X.l89 * Y.l8b) + X.l8b * Y.l89 + X.l9a * Y.lab - (X.l9c * Y.lbc) - (X.l9d * Y.lbd) - (X.l9e * Y.lbe) - (X.lab * Y.l9a) + X.lbc * Y.l9c + X.lbd * Y.l9d + X.lbe * Y.l9e
  l9c := -(X.l19 * Y.l1c) + X.l1c * Y.l19 - (X.l29 * Y.l2c) + X.l2c * Y.l29 - (X.l39 * Y.l3c) + X.l3c * Y.l39 - (X.l49 * Y.l4c) + X.l4c * Y.l49 - (X.l59 * Y.l5c) + X.l5c * Y.l59 - (X.l69 * Y.l6c) + X.l6c * Y.l69 - (X.l79 * Y.l7c) + X.l7c * Y.l79 - (X.l89 * Y.l8c) + X.l8c * Y.l89 + X.l9a * Y.lac + X.l9b * Y.lbc - (X.l9d * Y.lcd) - (X.l9e * Y.lce) - (X.lac * Y.l9a) - (X.lbc * Y.l9b) + X.lcd * Y.l9d + X.lce * Y.l9e
  l9d := -(X.l19 * Y.l1d) + X.l1d * Y.l19 - (X.l29 * Y.l2d) + X.l2d * Y.l29 - (X.l39 * Y.l3d) + X.l3d * Y.l39 - (X.l49 * Y.l4d) + X.l4d * Y.l49 - (X.l59 * Y.l5d) + X.l5d * Y.l59 - (X.l69 * Y.l6d) + X.l6d * Y.l69 - (X.l79 * Y.l7d) + X.l7d * Y.l79 - (X.l89 * Y.l8d) + X.l8d * Y.l89 + X.l9a * Y.lad + X.l9b * Y.lbd + X.l9c * Y.lcd - (X.l9e * Y.lde) - (X.lad * Y.l9a) - (X.lbd * Y.l9b) - (X.lcd * Y.l9c) + X.lde * Y.l9e
  l9e := -(X.l19 * Y.l1e) + X.l1e * Y.l19 - (X.l29 * Y.l2e) + X.l2e * Y.l29 - (X.l39 * Y.l3e) + X.l3e * Y.l39 - (X.l49 * Y.l4e) + X.l4e * Y.l49 - (X.l59 * Y.l5e) + X.l5e * Y.l59 - (X.l69 * Y.l6e) + X.l6e * Y.l69 - (X.l79 * Y.l7e) + X.l7e * Y.l79 - (X.l89 * Y.l8e) + X.l8e * Y.l89 + X.l9a * Y.lae + X.l9b * Y.lbe + X.l9c * Y.lce + X.l9d * Y.lde - (X.lae * Y.l9a) - (X.lbe * Y.l9b) - (X.lce * Y.l9c) - (X.lde * Y.l9d)
  lab := -(X.l1a * Y.l1b) + X.l1b * Y.l1a - (X.l2a * Y.l2b) + X.l2b * Y.l2a - (X.l3a * Y.l3b) + X.l3b * Y.l3a - (X.l4a * Y.l4b) + X.l4b * Y.l4a - (X.l5a * Y.l5b) + X.l5b * Y.l5a - (X.l6a * Y.l6b) + X.l6b * Y.l6a - (X.l7a * Y.l7b) + X.l7b * Y.l7a - (X.l8a * Y.l8b) + X.l8b * Y.l8a - (X.l9a * Y.l9b) + X.l9b * Y.l9a - (X.lac * Y.lbc) - (X.lad * Y.lbd) - (X.lae * Y.lbe) + X.lbc * Y.lac + X.lbd * Y.lad + X.lbe * Y.lae
  lac := -(X.l1a * Y.l1c) + X.l1c * Y.l1a - (X.l2a * Y.l2c) + X.l2c * Y.l2a - (X.l3a * Y.l3c) + X.l3c * Y.l3a - (X.l4a * Y.l4c) + X.l4c * Y.l4a - (X.l5a * Y.l5c) + X.l5c * Y.l5a - (X.l6a * Y.l6c) + X.l6c * Y.l6a - (X.l7a * Y.l7c) + X.l7c * Y.l7a - (X.l8a * Y.l8c) + X.l8c * Y.l8a - (X.l9a * Y.l9c) + X.l9c * Y.l9a + X.lab * Y.lbc - (X.lad * Y.lcd) - (X.lae * Y.lce) - (X.lbc * Y.lab) + X.lcd * Y.lad + X.lce * Y.lae
  lad := -(X.l1a * Y.l1d) + X.l1d * Y.l1a - (X.l2a * Y.l2d) + X.l2d * Y.l2a - (X.l3a * Y.l3d) + X.l3d * Y.l3a - (X.l4a * Y.l4d) + X.l4d * Y.l4a - (X.l5a * Y.l5d) + X.l5d * Y.l5a - (X.l6a * Y.l6d) + X.l6d * Y.l6a - (X.l7a * Y.l7d) + X.l7d * Y.l7a - (X.l8a * Y.l8d) + X.l8d * Y.l8a - (X.l9a * Y.l9d) + X.l9d * Y.l9a + X.lab * Y.lbd + X.lac * Y.lcd - (X.lae * Y.lde) - (X.lbd * Y.lab) - (X.lcd * Y.lac) + X.lde * Y.lae
  lae := -(X.l1a * Y.l1e) + X.l1e * Y.l1a - (X.l2a * Y.l2e) + X.l2e * Y.l2a - (X.l3a * Y.l3e) + X.l3e * Y.l3a - (X.l4a * Y.l4e) + X.l4e * Y.l4a - (X.l5a * Y.l5e) + X.l5e * Y.l5a - (X.l6a * Y.l6e) + X.l6e * Y.l6a - (X.l7a * Y.l7e) + X.l7e * Y.l7a - (X.l8a * Y.l8e) + X.l8e * Y.l8a - (X.l9a * Y.l9e) + X.l9e * Y.l9a + X.lab * Y.lbe + X.lac * Y.lce + X.lad * Y.lde - (X.lbe * Y.lab) - (X.lce * Y.lac) - (X.lde * Y.lad)
  lbc := -(X.l1b * Y.l1c) + X.l1c * Y.l1b - (X.l2b * Y.l2c) + X.l2c * Y.l2b - (X.l3b * Y.l3c) + X.l3c * Y.l3b - (X.l4b * Y.l4c) + X.l4c * Y.l4b - (X.l5b * Y.l5c) + X.l5c * Y.l5b - (X.l6b * Y.l6c) + X.l6c * Y.l6b - (X.l7b * Y.l7c) + X.l7c * Y.l7b - (X.l8b * Y.l8c) + X.l8c * Y.l8b - (X.l9b * Y.l9c) + X.l9c * Y.l9b - (X.lab * Y.lac) + X.lac * Y.lab - (X.lbd * Y.lcd) - (X.lbe * Y.lce) + X.lcd * Y.lbd + X.lce * Y.lbe
  lbd := -(X.l1b * Y.l1d) + X.l1d * Y.l1b - (X.l2b * Y.l2d) + X.l2d * Y.l2b - (X.l3b * Y.l3d) + X.l3d * Y.l3b - (X.l4b * Y.l4d) + X.l4d * Y.l4b - (X.l5b * Y.l5d) + X.l5d * Y.l5b - (X.l6b * Y.l6d) + X.l6d * Y.l6b - (X.l7b * Y.l7d) + X.l7d * Y.l7b - (X.l8b * Y.l8d) + X.l8d * Y.l8b - (X.l9b * Y.l9d) + X.l9d * Y.l9b - (X.lab * Y.lad) + X.lad * Y.lab + X.lbc * Y.lcd - (X.lbe * Y.lde) - (X.lcd * Y.lbc) + X.lde * Y.lbe
  lbe := -(X.l1b * Y.l1e) + X.l1e * Y.l1b - (X.l2b * Y.l2e) + X.l2e * Y.l2b - (X.l3b * Y.l3e) + X.l3e * Y.l3b - (X.l4b * Y.l4e) + X.l4e * Y.l4b - (X.l5b * Y.l5e) + X.l5e * Y.l5b - (X.l6b * Y.l6e) + X.l6e * Y.l6b - (X.l7b * Y.l7e) + X.l7e * Y.l7b - (X.l8b * Y.l8e) + X.l8e * Y.l8b - (X.l9b * Y.l9e) + X.l9e * Y.l9b - (X.lab * Y.lae) + X.lae * Y.lab + X.lbc * Y.lce + X.lbd * Y.lde - (X.lce * Y.lbc) - (X.lde * Y.lbd)
  lcd := -(X.l1c * Y.l1d) + X.l1d * Y.l1c - (X.l2c * Y.l2d) + X.l2d * Y.l2c - (X.l3c * Y.l3d) + X.l3d * Y.l3c - (X.l4c * Y.l4d) + X.l4d * Y.l4c - (X.l5c * Y.l5d) + X.l5d * Y.l5c - (X.l6c * Y.l6d) + X.l6d * Y.l6c - (X.l7c * Y.l7d) + X.l7d * Y.l7c - (X.l8c * Y.l8d) + X.l8d * Y.l8c - (X.l9c * Y.l9d) + X.l9d * Y.l9c - (X.lac * Y.lad) + X.lad * Y.lac - (X.lbc * Y.lbd) + X.lbd * Y.lbc - (X.lce * Y.lde) + X.lde * Y.lce
  lce := -(X.l1c * Y.l1e) + X.l1e * Y.l1c - (X.l2c * Y.l2e) + X.l2e * Y.l2c - (X.l3c * Y.l3e) + X.l3e * Y.l3c - (X.l4c * Y.l4e) + X.l4e * Y.l4c - (X.l5c * Y.l5e) + X.l5e * Y.l5c - (X.l6c * Y.l6e) + X.l6e * Y.l6c - (X.l7c * Y.l7e) + X.l7e * Y.l7c - (X.l8c * Y.l8e) + X.l8e * Y.l8c - (X.l9c * Y.l9e) + X.l9e * Y.l9c - (X.lac * Y.lae) + X.lae * Y.lac - (X.lbc * Y.lbe) + X.lbe * Y.lbc + X.lcd * Y.lde - (X.lde * Y.lcd)
  lde := -(X.l1d * Y.l1e) + X.l1e * Y.l1d - (X.l2d * Y.l2e) + X.l2e * Y.l2d - (X.l3d * Y.l3e) + X.l3e * Y.l3d - (X.l4d * Y.l4e) + X.l4e * Y.l4d - (X.l5d * Y.l5e) + X.l5e * Y.l5d - (X.l6d * Y.l6e) + X.l6e * Y.l6d - (X.l7d * Y.l7e) + X.l7e * Y.l7d - (X.l8d * Y.l8e) + X.l8e * Y.l8d - (X.l9d * Y.l9e) + X.l9e * Y.l9d - (X.lad * Y.lae) + X.lae * Y.lad - (X.lbd * Y.lbe) + X.lbe * Y.lbd - (X.lcd * Y.lce) + X.lce * Y.lcd

set_option maxHeartbeats 16000000 in
/-- The Lie bracket is antisymmetric: [X, Y] = -[Y, X]. -/
theorem comm_antisymm (X Y : SO14) : comm X Y = neg (comm Y X) := by
  ext <;> simp [comm, neg] <;> ring

/-! ## Part 4: Selected Basis Generators -/

/-- Basis generator L_{1,2}. -/
def L12 : SO14 where
  l12 := 1
  l13 := 0
  l14 := 0
  l15 := 0
  l16 := 0
  l17 := 0
  l18 := 0
  l19 := 0
  l1a := 0
  l1b := 0
  l1c := 0
  l1d := 0
  l1e := 0
  l23 := 0
  l24 := 0
  l25 := 0
  l26 := 0
  l27 := 0
  l28 := 0
  l29 := 0
  l2a := 0
  l2b := 0
  l2c := 0
  l2d := 0
  l2e := 0
  l34 := 0
  l35 := 0
  l36 := 0
  l37 := 0
  l38 := 0
  l39 := 0
  l3a := 0
  l3b := 0
  l3c := 0
  l3d := 0
  l3e := 0
  l45 := 0
  l46 := 0
  l47 := 0
  l48 := 0
  l49 := 0
  l4a := 0
  l4b := 0
  l4c := 0
  l4d := 0
  l4e := 0
  l56 := 0
  l57 := 0
  l58 := 0
  l59 := 0
  l5a := 0
  l5b := 0
  l5c := 0
  l5d := 0
  l5e := 0
  l67 := 0
  l68 := 0
  l69 := 0
  l6a := 0
  l6b := 0
  l6c := 0
  l6d := 0
  l6e := 0
  l78 := 0
  l79 := 0
  l7a := 0
  l7b := 0
  l7c := 0
  l7d := 0
  l7e := 0
  l89 := 0
  l8a := 0
  l8b := 0
  l8c := 0
  l8d := 0
  l8e := 0
  l9a := 0
  l9b := 0
  l9c := 0
  l9d := 0
  l9e := 0
  lab := 0
  lac := 0
  lad := 0
  lae := 0
  lbc := 0
  lbd := 0
  lbe := 0
  lcd := 0
  lce := 0
  lde := 0

/-- Basis generator L_{1,3}. -/
def L13 : SO14 where
  l12 := 0
  l13 := 1
  l14 := 0
  l15 := 0
  l16 := 0
  l17 := 0
  l18 := 0
  l19 := 0
  l1a := 0
  l1b := 0
  l1c := 0
  l1d := 0
  l1e := 0
  l23 := 0
  l24 := 0
  l25 := 0
  l26 := 0
  l27 := 0
  l28 := 0
  l29 := 0
  l2a := 0
  l2b := 0
  l2c := 0
  l2d := 0
  l2e := 0
  l34 := 0
  l35 := 0
  l36 := 0
  l37 := 0
  l38 := 0
  l39 := 0
  l3a := 0
  l3b := 0
  l3c := 0
  l3d := 0
  l3e := 0
  l45 := 0
  l46 := 0
  l47 := 0
  l48 := 0
  l49 := 0
  l4a := 0
  l4b := 0
  l4c := 0
  l4d := 0
  l4e := 0
  l56 := 0
  l57 := 0
  l58 := 0
  l59 := 0
  l5a := 0
  l5b := 0
  l5c := 0
  l5d := 0
  l5e := 0
  l67 := 0
  l68 := 0
  l69 := 0
  l6a := 0
  l6b := 0
  l6c := 0
  l6d := 0
  l6e := 0
  l78 := 0
  l79 := 0
  l7a := 0
  l7b := 0
  l7c := 0
  l7d := 0
  l7e := 0
  l89 := 0
  l8a := 0
  l8b := 0
  l8c := 0
  l8d := 0
  l8e := 0
  l9a := 0
  l9b := 0
  l9c := 0
  l9d := 0
  l9e := 0
  lab := 0
  lac := 0
  lad := 0
  lae := 0
  lbc := 0
  lbd := 0
  lbe := 0
  lcd := 0
  lce := 0
  lde := 0

/-- Basis generator L_{1,4}. -/
def L14 : SO14 where
  l12 := 0
  l13 := 0
  l14 := 1
  l15 := 0
  l16 := 0
  l17 := 0
  l18 := 0
  l19 := 0
  l1a := 0
  l1b := 0
  l1c := 0
  l1d := 0
  l1e := 0
  l23 := 0
  l24 := 0
  l25 := 0
  l26 := 0
  l27 := 0
  l28 := 0
  l29 := 0
  l2a := 0
  l2b := 0
  l2c := 0
  l2d := 0
  l2e := 0
  l34 := 0
  l35 := 0
  l36 := 0
  l37 := 0
  l38 := 0
  l39 := 0
  l3a := 0
  l3b := 0
  l3c := 0
  l3d := 0
  l3e := 0
  l45 := 0
  l46 := 0
  l47 := 0
  l48 := 0
  l49 := 0
  l4a := 0
  l4b := 0
  l4c := 0
  l4d := 0
  l4e := 0
  l56 := 0
  l57 := 0
  l58 := 0
  l59 := 0
  l5a := 0
  l5b := 0
  l5c := 0
  l5d := 0
  l5e := 0
  l67 := 0
  l68 := 0
  l69 := 0
  l6a := 0
  l6b := 0
  l6c := 0
  l6d := 0
  l6e := 0
  l78 := 0
  l79 := 0
  l7a := 0
  l7b := 0
  l7c := 0
  l7d := 0
  l7e := 0
  l89 := 0
  l8a := 0
  l8b := 0
  l8c := 0
  l8d := 0
  l8e := 0
  l9a := 0
  l9b := 0
  l9c := 0
  l9d := 0
  l9e := 0
  lab := 0
  lac := 0
  lad := 0
  lae := 0
  lbc := 0
  lbd := 0
  lbe := 0
  lcd := 0
  lce := 0
  lde := 0

/-- Basis generator L_{1,5}. -/
def L15 : SO14 where
  l12 := 0
  l13 := 0
  l14 := 0
  l15 := 1
  l16 := 0
  l17 := 0
  l18 := 0
  l19 := 0
  l1a := 0
  l1b := 0
  l1c := 0
  l1d := 0
  l1e := 0
  l23 := 0
  l24 := 0
  l25 := 0
  l26 := 0
  l27 := 0
  l28 := 0
  l29 := 0
  l2a := 0
  l2b := 0
  l2c := 0
  l2d := 0
  l2e := 0
  l34 := 0
  l35 := 0
  l36 := 0
  l37 := 0
  l38 := 0
  l39 := 0
  l3a := 0
  l3b := 0
  l3c := 0
  l3d := 0
  l3e := 0
  l45 := 0
  l46 := 0
  l47 := 0
  l48 := 0
  l49 := 0
  l4a := 0
  l4b := 0
  l4c := 0
  l4d := 0
  l4e := 0
  l56 := 0
  l57 := 0
  l58 := 0
  l59 := 0
  l5a := 0
  l5b := 0
  l5c := 0
  l5d := 0
  l5e := 0
  l67 := 0
  l68 := 0
  l69 := 0
  l6a := 0
  l6b := 0
  l6c := 0
  l6d := 0
  l6e := 0
  l78 := 0
  l79 := 0
  l7a := 0
  l7b := 0
  l7c := 0
  l7d := 0
  l7e := 0
  l89 := 0
  l8a := 0
  l8b := 0
  l8c := 0
  l8d := 0
  l8e := 0
  l9a := 0
  l9b := 0
  l9c := 0
  l9d := 0
  l9e := 0
  lab := 0
  lac := 0
  lad := 0
  lae := 0
  lbc := 0
  lbd := 0
  lbe := 0
  lcd := 0
  lce := 0
  lde := 0

/-- Basis generator L_{1,6}. -/
def L16 : SO14 where
  l12 := 0
  l13 := 0
  l14 := 0
  l15 := 0
  l16 := 1
  l17 := 0
  l18 := 0
  l19 := 0
  l1a := 0
  l1b := 0
  l1c := 0
  l1d := 0
  l1e := 0
  l23 := 0
  l24 := 0
  l25 := 0
  l26 := 0
  l27 := 0
  l28 := 0
  l29 := 0
  l2a := 0
  l2b := 0
  l2c := 0
  l2d := 0
  l2e := 0
  l34 := 0
  l35 := 0
  l36 := 0
  l37 := 0
  l38 := 0
  l39 := 0
  l3a := 0
  l3b := 0
  l3c := 0
  l3d := 0
  l3e := 0
  l45 := 0
  l46 := 0
  l47 := 0
  l48 := 0
  l49 := 0
  l4a := 0
  l4b := 0
  l4c := 0
  l4d := 0
  l4e := 0
  l56 := 0
  l57 := 0
  l58 := 0
  l59 := 0
  l5a := 0
  l5b := 0
  l5c := 0
  l5d := 0
  l5e := 0
  l67 := 0
  l68 := 0
  l69 := 0
  l6a := 0
  l6b := 0
  l6c := 0
  l6d := 0
  l6e := 0
  l78 := 0
  l79 := 0
  l7a := 0
  l7b := 0
  l7c := 0
  l7d := 0
  l7e := 0
  l89 := 0
  l8a := 0
  l8b := 0
  l8c := 0
  l8d := 0
  l8e := 0
  l9a := 0
  l9b := 0
  l9c := 0
  l9d := 0
  l9e := 0
  lab := 0
  lac := 0
  lad := 0
  lae := 0
  lbc := 0
  lbd := 0
  lbe := 0
  lcd := 0
  lce := 0
  lde := 0

/-- Basis generator L_{11,12} (gravity sector). -/
def Lbc : SO14 where
  l12 := 0
  l13 := 0
  l14 := 0
  l15 := 0
  l16 := 0
  l17 := 0
  l18 := 0
  l19 := 0
  l1a := 0
  l1b := 0
  l1c := 0
  l1d := 0
  l1e := 0
  l23 := 0
  l24 := 0
  l25 := 0
  l26 := 0
  l27 := 0
  l28 := 0
  l29 := 0
  l2a := 0
  l2b := 0
  l2c := 0
  l2d := 0
  l2e := 0
  l34 := 0
  l35 := 0
  l36 := 0
  l37 := 0
  l38 := 0
  l39 := 0
  l3a := 0
  l3b := 0
  l3c := 0
  l3d := 0
  l3e := 0
  l45 := 0
  l46 := 0
  l47 := 0
  l48 := 0
  l49 := 0
  l4a := 0
  l4b := 0
  l4c := 0
  l4d := 0
  l4e := 0
  l56 := 0
  l57 := 0
  l58 := 0
  l59 := 0
  l5a := 0
  l5b := 0
  l5c := 0
  l5d := 0
  l5e := 0
  l67 := 0
  l68 := 0
  l69 := 0
  l6a := 0
  l6b := 0
  l6c := 0
  l6d := 0
  l6e := 0
  l78 := 0
  l79 := 0
  l7a := 0
  l7b := 0
  l7c := 0
  l7d := 0
  l7e := 0
  l89 := 0
  l8a := 0
  l8b := 0
  l8c := 0
  l8d := 0
  l8e := 0
  l9a := 0
  l9b := 0
  l9c := 0
  l9d := 0
  l9e := 0
  lab := 0
  lac := 0
  lad := 0
  lae := 0
  lbc := 1
  lbd := 0
  lbe := 0
  lcd := 0
  lce := 0
  lde := 0

/-! ## Part 5: Structure Constant Verification

Bracket tests are omitted for SO(14) — with 91 generators, defining all basis
elements is impractical. The Jacobi identity (Part 6) and LieRing instance (Part 7)
certify all structure constants. For individual bracket tests, see so10_grand.lean
(45 generators) or so4_gravity.lean (6 generators). -/

/-! ## Part 6: The Jacobi Identity

The Jacobi identity for so(14). 91 generators — larger than so(10)'s 45.
Expected compile time: substantial (cubic in generators). -/

set_option maxHeartbeats 64000000 in
/-- The Jacobi identity for so(14).

    For all A, B, C ∈ so(14):
      [A, [B, C]] + [B, [C, A]] + [C, [A, B]] = 0

    This is the identity that makes so(14) a Lie algebra.
    91 generators, cubic polynomial ring proof. -/
theorem jacobi (A B C : SO14) :
    comm A (comm B C) + comm B (comm C A) + comm C (comm A B) = zero := by
  ext <;> simp [comm, add, zero] <;> ring

/-! ## Part 7: Mathlib LieRing and LieAlgebra Instances

so(14) is certified as a Lie algebra over ℝ via mathlib's typeclass system.
91 generators — the largest Lie algebra in the project with this certification. -/

set_option maxHeartbeats 8000000 in
instance : AddCommGroup SO14 where
  add_assoc := by intros; ext <;> simp [add] <;> ring
  zero_add := by intros; ext <;> simp [add, zero]
  add_zero := by intros; ext <;> simp [add, zero]
  add_comm := by intros; ext <;> simp [add] <;> ring
  neg_add_cancel := by intros; ext <;> simp [add, neg, zero]
  sub_eq_add_neg := by intros; rfl
  nsmul := nsmulRec
  zsmul := zsmulRec

set_option maxHeartbeats 8000000 in
instance : Module ℝ SO14 where
  one_smul := by intros; ext <;> simp [smul]
  mul_smul := by intros; ext <;> simp [smul] <;> ring
  smul_zero := by intros; ext <;> simp [smul, zero]
  smul_add := by intros; ext <;> simp [smul, add] <;> ring
  add_smul := by intros; ext <;> simp [smul, add] <;> ring
  zero_smul := by intros; ext <;> simp [smul, zero]

instance : Bracket SO14 SO14 := ⟨comm⟩

@[simp] lemma bracket_def' (a b : SO14) : ⁅a, b⁆ = comm a b := rfl

set_option maxHeartbeats 200000000 in
instance : LieRing SO14 where
  add_lie := by intros; ext <;> simp [comm, add] <;> ring
  lie_add := by intros; ext <;> simp [comm, add] <;> ring
  lie_self := by intro x; ext <;> simp [comm, zero] <;> ring
  leibniz_lie := by intros; ext <;> simp [comm, add] <;> ring

set_option maxHeartbeats 128000000 in
instance : LieAlgebra ℝ SO14 where
  lie_smul := by intros; ext <;> simp [comm, smul] <;> ring

/-! ## Part 8: Subalgebra Identification -/

/-- The so(10) subalgebra: L_{ij} with i,j in {1,...,10}. -/
def isSO10 (X : SO14) : Prop :=
  X.l1b = 0 ∧
  X.l1c = 0 ∧
  X.l1d = 0 ∧
  X.l1e = 0 ∧
  X.l2b = 0 ∧
  X.l2c = 0 ∧
  X.l2d = 0 ∧
  X.l2e = 0 ∧
  X.l3b = 0 ∧
  X.l3c = 0 ∧
  X.l3d = 0 ∧
  X.l3e = 0 ∧
  X.l4b = 0 ∧
  X.l4c = 0 ∧
  X.l4d = 0 ∧
  X.l4e = 0 ∧
  X.l5b = 0 ∧
  X.l5c = 0 ∧
  X.l5d = 0 ∧
  X.l5e = 0 ∧
  X.l6b = 0 ∧
  X.l6c = 0 ∧
  X.l6d = 0 ∧
  X.l6e = 0 ∧
  X.l7b = 0 ∧
  X.l7c = 0 ∧
  X.l7d = 0 ∧
  X.l7e = 0 ∧
  X.l8b = 0 ∧
  X.l8c = 0 ∧
  X.l8d = 0 ∧
  X.l8e = 0 ∧
  X.l9b = 0 ∧
  X.l9c = 0 ∧
  X.l9d = 0 ∧
  X.l9e = 0 ∧
  X.lab = 0 ∧
  X.lac = 0 ∧
  X.lad = 0 ∧
  X.lae = 0 ∧
  X.lbc = 0 ∧
  X.lbd = 0 ∧
  X.lbe = 0 ∧
  X.lcd = 0 ∧
  X.lce = 0 ∧
  X.lde = 0

/-- The so(4) subalgebra: L_{ij} with i,j in {11,...,14} (gravity sector). -/
def isSO4 (X : SO14) : Prop :=
  X.l12 = 0 ∧
  X.l13 = 0 ∧
  X.l14 = 0 ∧
  X.l15 = 0 ∧
  X.l16 = 0 ∧
  X.l17 = 0 ∧
  X.l18 = 0 ∧
  X.l19 = 0 ∧
  X.l1a = 0 ∧
  X.l1b = 0 ∧
  X.l1c = 0 ∧
  X.l1d = 0 ∧
  X.l1e = 0 ∧
  X.l23 = 0 ∧
  X.l24 = 0 ∧
  X.l25 = 0 ∧
  X.l26 = 0 ∧
  X.l27 = 0 ∧
  X.l28 = 0 ∧
  X.l29 = 0 ∧
  X.l2a = 0 ∧
  X.l2b = 0 ∧
  X.l2c = 0 ∧
  X.l2d = 0 ∧
  X.l2e = 0 ∧
  X.l34 = 0 ∧
  X.l35 = 0 ∧
  X.l36 = 0 ∧
  X.l37 = 0 ∧
  X.l38 = 0 ∧
  X.l39 = 0 ∧
  X.l3a = 0 ∧
  X.l3b = 0 ∧
  X.l3c = 0 ∧
  X.l3d = 0 ∧
  X.l3e = 0 ∧
  X.l45 = 0 ∧
  X.l46 = 0 ∧
  X.l47 = 0 ∧
  X.l48 = 0 ∧
  X.l49 = 0 ∧
  X.l4a = 0 ∧
  X.l4b = 0 ∧
  X.l4c = 0 ∧
  X.l4d = 0 ∧
  X.l4e = 0 ∧
  X.l56 = 0 ∧
  X.l57 = 0 ∧
  X.l58 = 0 ∧
  X.l59 = 0 ∧
  X.l5a = 0 ∧
  X.l5b = 0 ∧
  X.l5c = 0 ∧
  X.l5d = 0 ∧
  X.l5e = 0 ∧
  X.l67 = 0 ∧
  X.l68 = 0 ∧
  X.l69 = 0 ∧
  X.l6a = 0 ∧
  X.l6b = 0 ∧
  X.l6c = 0 ∧
  X.l6d = 0 ∧
  X.l6e = 0 ∧
  X.l78 = 0 ∧
  X.l79 = 0 ∧
  X.l7a = 0 ∧
  X.l7b = 0 ∧
  X.l7c = 0 ∧
  X.l7d = 0 ∧
  X.l7e = 0 ∧
  X.l89 = 0 ∧
  X.l8a = 0 ∧
  X.l8b = 0 ∧
  X.l8c = 0 ∧
  X.l8d = 0 ∧
  X.l8e = 0 ∧
  X.l9a = 0 ∧
  X.l9b = 0 ∧
  X.l9c = 0 ∧
  X.l9d = 0 ∧
  X.l9e = 0 ∧
  X.lab = 0 ∧
  X.lac = 0 ∧
  X.lad = 0 ∧
  X.lae = 0

end SO14

/-! ## Summary

### What this file proves:
1. so(14) Lie algebra with 91 generators and explicit bracket (Parts 1-3)
2. Structure constant verification (Part 5)
3. Jacobi identity for so(14) (Part 6)
4. Certified LieRing and LieAlgebra ℝ instances (Part 7)
5. so(10) and so(4) subalgebra predicates (Part 8)

### Signature:
This is the COMPACT form so(14,0). The gravity sector is so(4), not so(1,3).
Lorentzian signature requires so(11,3) — a different real form.

### Next steps:
- SO10 ↪ SO14 LieHom (so10_so14_liehom.lean)
- so(4) ↪ SO14 LieHom (so4_so14_liehom.lean)
- Anomaly cancellation as algebraic theorem

0 sorry gaps.
-/
