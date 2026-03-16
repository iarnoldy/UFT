/-
SO(16) is a Lie subalgebra of E₈ — closure verification
=========================================================

Verifies that for every pair (i,j) of SO(16) basis elements,
the E₈ bracket [B_i, B_j] contains only SO(16) basis elements.
120 SO(16) generators inside 248 E₈ generators.

SO(16) = D8 root subsystem: integer-coordinate E₈ roots.
Spinor complement: half-integer E₈ roots (128_s representation).
-/

import clifford.e8_sparse_defs

set_option maxHeartbeats 4000000

open E8Sparse

/-- SO(16) basis element indices in E₈ (120 out of 248). -/
def isSO16 (n : Nat) : Bool :=
  match n with
  | 0 => true
  | 1 => true
  | 2 => true
  | 3 => true
  | 4 => true
  | 5 => true
  | 6 => true
  | 7 => true
  | 8 => true
  | 9 => true
  | 10 => true
  | 11 => true
  | 12 => true
  | 13 => true
  | 14 => true
  | 16 => true
  | 17 => true
  | 18 => true
  | 19 => true
  | 20 => true
  | 21 => true
  | 23 => true
  | 24 => true
  | 25 => true
  | 26 => true
  | 27 => true
  | 28 => true
  | 30 => true
  | 31 => true
  | 32 => true
  | 33 => true
  | 34 => true
  | 37 => true
  | 38 => true
  | 39 => true
  | 40 => true
  | 41 => true
  | 44 => true
  | 45 => true
  | 46 => true
  | 47 => true
  | 51 => true
  | 52 => true
  | 53 => true
  | 58 => true
  | 59 => true
  | 64 => true
  | 65 => true
  | 70 => true
  | 76 => true
  | 107 => true
  | 110 => true
  | 113 => true
  | 115 => true
  | 117 => true
  | 119 => true
  | 120 => true
  | 121 => true
  | 122 => true
  | 123 => true
  | 124 => true
  | 125 => true
  | 126 => true
  | 127 => true
  | 128 => true
  | 129 => true
  | 130 => true
  | 131 => true
  | 132 => true
  | 133 => true
  | 134 => true
  | 136 => true
  | 137 => true
  | 138 => true
  | 139 => true
  | 140 => true
  | 141 => true
  | 143 => true
  | 144 => true
  | 145 => true
  | 146 => true
  | 147 => true
  | 148 => true
  | 150 => true
  | 151 => true
  | 152 => true
  | 153 => true
  | 154 => true
  | 157 => true
  | 158 => true
  | 159 => true
  | 160 => true
  | 161 => true
  | 164 => true
  | 165 => true
  | 166 => true
  | 167 => true
  | 171 => true
  | 172 => true
  | 173 => true
  | 178 => true
  | 179 => true
  | 184 => true
  | 185 => true
  | 190 => true
  | 196 => true
  | 227 => true
  | 230 => true
  | 233 => true
  | 235 => true
  | 237 => true
  | 239 => true
  | 240 => true
  | 241 => true
  | 242 => true
  | 243 => true
  | 244 => true
  | 245 => true
  | 246 => true
  | 247 => true
  | _ => false

/-- Every term in [B_i, B_j] for SO(16) elements is an SO(16) element. -/
def so16ClosedCheck (i j : Nat) : Bool :=
  (bkt i j).all fun (k, _) => isSO16 k

/-- SO(16) is closed under the E₈ bracket. -/
theorem so16_subalgebra_e8 : ∀ (i j : Fin 248),
    isSO16 i.val = true → isSO16 j.val = true →
    (bkt i.val j.val).all (fun (k, _) => isSO16 k) = true := by
  native_decide
