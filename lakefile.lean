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
  roots := #[`foundations.basic_operators, `foundations.algebraic_necessity, `telegraph.telegraph_equation, `polyphase.polyphase_formula, `clifford.cl11, `clifford.cl30, `clifford.cl31_maxwell, `clifford.gauge_gravity, `clifford.dirac, `clifford.su3_color, `clifford.su3_cartan_weyl, `clifford.su5_grand, `clifford.unification, `clifford.georgi_glashow, `clifford.lie_bridge, `clifford.so10_grand, `clifford.unification_gravity, `clifford.spinor_matter, `clifford.su5_so10_embedding, `clifford.grand_unified_field, `clifford.symmetry_breaking, `dynamics.yang_mills_energy, `dynamics.covariant_derivative, `dynamics.rg_running, `dynamics.bianchi_identity, `dynamics.yang_mills_equation, `dynamics.yukawa_couplings, `clifford.so14_unification, `clifford.so14_anomalies, `quantum.hilbert_space, `quantum.mass_gap, `lagrangian.circuit_action, `spectral.grade2_lie_algebra, `spectral.casimir_eigenvalues, `spectral.casimir_spectral_gap, `spectral.block_tridiagonal]
