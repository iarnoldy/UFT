/-
E₈ Jacobi Verification — Chunk 00 (i = 0..15)
-/

import clifford.e8_sparse_defs

set_option maxHeartbeats 16000000

open E8Sparse

theorem e8_jacobi_000 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨0, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_001 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨1, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_002 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨2, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_003 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨3, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_004 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨4, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_005 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨5, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_006 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨6, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_007 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨7, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_008 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨8, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_009 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨9, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_010 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨10, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_011 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨11, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_012 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨12, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_013 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨13, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_014 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨14, by omega⟩ j k l = 0 := by
  native_decide

theorem e8_jacobi_015 : ∀ (j k l : Fin 248),
    jacobiCheck ⟨15, by omega⟩ j k l = 0 := by
  native_decide
