import Lake
open Lake DSL

package «dollard-formal-verification» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4"

@[default_target]
lean_lib «DollardFormalVerification» where
  srcDir := "src/lean_proofs"
  roots := #[`foundations.basic_operators, `foundations.algebraic_necessity, `telegraph.telegraph_equation, `polyphase.polyphase_formula, `clifford.cl11, `clifford.cl30, `clifford.cl31_maxwell, `clifford.gauge_gravity, `clifford.dirac, `clifford.su3_color, `clifford.su5_grand, `clifford.unification, `clifford.georgi_glashow, `lagrangian.circuit_action]
