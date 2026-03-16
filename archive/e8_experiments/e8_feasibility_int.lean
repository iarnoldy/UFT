/-
E₈ Feasibility — Mitigation A: Use ℤ instead of ℚ
===================================================

Integer arithmetic avoids GCD normalization overhead.
E₈ Chevalley basis structure constants are integers anyway.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

abbrev ZMat248 := Matrix (Fin 248) (Fin 248) ℤ

def E01z : ZMat248 := Matrix.of fun i j => match i, j with
    | 0, 1 => 1
    | 1, 0 => -1
    | _, _ => 0

def E02z : ZMat248 := Matrix.of fun i j => match i, j with
    | 0, 2 => 1
    | 2, 0 => -1
    | _, _ => 0

def neg_E12z : ZMat248 := Matrix.of fun i j => match i, j with
    | 1, 2 => -1
    | 2, 1 => 1
    | _, _ => 0

/-- Feasibility test over ℤ. -/
theorem e8_feasibility_bracket_int :
    E01z * E02z - E02z * E01z = neg_E12z := by
  native_decide
