/-
E₈ Feasibility — Scaling test: 64×64, 128×128 matrices
========================================================

Find where the scaling wall is. If 128×128 is fast but 248×248 is slow,
we know the bottleneck is matrix size, not overhead.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

-- 64×64 test
abbrev ZMat64 := Matrix (Fin 64) (Fin 64) ℤ

def E01_64 : ZMat64 := Matrix.of fun i j => match i, j with
    | 0, 1 => 1 | 1, 0 => -1 | _, _ => 0
def E02_64 : ZMat64 := Matrix.of fun i j => match i, j with
    | 0, 2 => 1 | 2, 0 => -1 | _, _ => 0
def neg_E12_64 : ZMat64 := Matrix.of fun i j => match i, j with
    | 1, 2 => -1 | 2, 1 => 1 | _, _ => 0

theorem bracket_64 : E01_64 * E02_64 - E02_64 * E01_64 = neg_E12_64 := by
  native_decide

-- 128×128 test
abbrev ZMat128 := Matrix (Fin 128) (Fin 128) ℤ

def E01_128 : ZMat128 := Matrix.of fun i j => match i, j with
    | 0, 1 => 1 | 1, 0 => -1 | _, _ => 0
def E02_128 : ZMat128 := Matrix.of fun i j => match i, j with
    | 0, 2 => 1 | 2, 0 => -1 | _, _ => 0
def neg_E12_128 : ZMat128 := Matrix.of fun i j => match i, j with
    | 1, 2 => -1 | 2, 1 => 1 | _, _ => 0

theorem bracket_128 : E01_128 * E02_128 - E02_128 * E01_128 = neg_E12_128 := by
  native_decide
