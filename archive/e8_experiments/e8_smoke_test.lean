/-
E₈ Smoke Test — verify import chain works before 26-hour build.
2 theorems only. Delete after verification.
-/

import clifford.e8_defs

set_option maxHeartbeats 800000

open E8

/-- [H_1, H_2] = 0 (Cartan elements commute). -/
theorem e8_smoke_1 :
    ad0 * ad1 - ad1 * ad0 = (0 : Mat) := by
  native_decide

/-- [E_1, E_2] = E_9 (first positive bracket). -/
theorem e8_smoke_2 :
    ad8 * ad9 - ad9 * ad8 = ad16 := by
  native_decide
