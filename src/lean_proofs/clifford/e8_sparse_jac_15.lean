/-
E₈ Jacobi Verification — Chunk 15 (i = 240..247)
-/

import clifford.e8_sparse_defs

set_option maxHeartbeats 16000000

open E8Sparse

theorem e8_jacobi_240 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨240, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_241 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨241, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_242 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨242, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_243 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨243, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_244 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨244, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_245 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨245, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_246 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨246, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_247 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨247, by omega⟩ j k l = 0 := by
  native_decide
