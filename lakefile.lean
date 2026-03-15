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
  roots := #[`foundations.basic_operators, `foundations.algebraic_necessity, `telegraph.telegraph_equation, `polyphase.polyphase_formula, `clifford.cl11, `clifford.cl30, `clifford.cl31_maxwell, `clifford.gauge_gravity, `clifford.dirac, `clifford.su3_color, `clifford.su3_cartan_weyl, `clifford.su5_grand, `clifford.unification, `clifford.georgi_glashow, `clifford.lie_bridge, `clifford.so10_grand, `clifford.unification_gravity, `clifford.spinor_matter, `clifford.su5_so10_embedding, `clifford.grand_unified_field, `clifford.symmetry_breaking, `dynamics.yang_mills_energy, `dynamics.covariant_derivative, `dynamics.rg_running, `dynamics.bianchi_identity, `dynamics.yang_mills_equation, `dynamics.yukawa_couplings, `clifford.so14_unification, `clifford.so14_anomalies, `quantum.hilbert_space, `quantum.mass_gap, `lagrangian.circuit_action, `spectral.grade2_lie_algebra, `spectral.casimir_eigenvalues, `spectral.casimir_spectral_gap, `spectral.block_tridiagonal, `clifford.so14_breaking_chain, `clifford.spinor_parity_obstruction, `clifford.e8_embedding, `clifford.e8_su9_decomposition, `clifford.e8_generation_mechanism, `clifford.three_generation_theorem, `clifford.e8_chirality_boundary, `clifford.j_anomaly_free_eigenspaces, `clifford.exterior_cube_chirality, `clifford.massive_chirality_definition, `clifford.chirality_factorization, `dynamics.lagrangian_uniqueness, `spectral.schur_killing_uniqueness, `dynamics.differential_forms, `clifford.spinor_rep, `clifford.spinor_rep_full, `dynamics.wedge_product, `dynamics.gauge_connection, `dynamics.bianchi_from_principles, `dynamics.yang_mills_variation, `clifford.spinor_rep_homomorphism, `clifford.su5c_compact, `clifford.su5c_so10_liehom, `clifford.so14_grand, `clifford.so10_so14_liehom, `clifford.so4_gravity, `clifford.so4_so14_liehom, `clifford.anomaly_trace, `clifford.so16_grand, `clifford.so16_matrix, `clifford.e8_defs, `clifford.e8_chunk_00, `clifford.e8_chunk_01, `clifford.e8_chunk_02, `clifford.e8_chunk_03, `clifford.e8_chunk_04, `clifford.e8_chunk_05, `clifford.e8_chunk_06, `clifford.e8_chunk_07, `clifford.e8_chunk_08, `clifford.e8_chunk_09, `clifford.e8_chunk_10, `clifford.e8_chunk_11, `clifford.e8_chunk_12, `clifford.e8_chunk_13, `clifford.e8_chunk_14, `clifford.e8_chunk_15, `clifford.e8_chunk_16, `clifford.e8_chunk_17, `clifford.e8_chunk_18, `clifford.e8_chunk_19, `clifford.e8_chunk_20, `clifford.e8_chunk_21, `clifford.e8_chunk_22, `clifford.e8_chunk_23, `clifford.e8_chunk_24, `clifford.e8_chunk_25, `clifford.e8_chunk_26, `clifford.e8_chunk_27, `clifford.e8_chunk_28, `clifford.e8_chunk_29, `clifford.e8_chunk_30, `clifford.e8_root]
