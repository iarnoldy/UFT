/-
E₈ as a Certified Lie Algebra — All Bracket Relations Verified
===============================================================

This file imports the complete E₈ verification:
  - e8_defs.lean: 248 adjoint matrices (248×248 over ℤ)
  - e8_chunk_00..e8_chunk_30: 30628 bracket theorems

Every bracket relation [B_i, B_j] = Σ_k f^k_{ij} B_k is verified
by Lean's native_decide kernel — not by trust, by computation.

Structure constants from SageMath Chevalley basis (GAP + Chevie).
Cross-verified: SageMath oracle ↔ Python Jacobi (0/2,511,496) ↔ Lean kernel.
-/

import clifford.e8_defs
import clifford.e8_chunk_00
import clifford.e8_chunk_01
import clifford.e8_chunk_02
import clifford.e8_chunk_03
import clifford.e8_chunk_04
import clifford.e8_chunk_05
import clifford.e8_chunk_06
import clifford.e8_chunk_07
import clifford.e8_chunk_08
import clifford.e8_chunk_09
import clifford.e8_chunk_10
import clifford.e8_chunk_11
import clifford.e8_chunk_12
import clifford.e8_chunk_13
import clifford.e8_chunk_14
import clifford.e8_chunk_15
import clifford.e8_chunk_16
import clifford.e8_chunk_17
import clifford.e8_chunk_18
import clifford.e8_chunk_19
import clifford.e8_chunk_20
import clifford.e8_chunk_21
import clifford.e8_chunk_22
import clifford.e8_chunk_23
import clifford.e8_chunk_24
import clifford.e8_chunk_25
import clifford.e8_chunk_26
import clifford.e8_chunk_27
import clifford.e8_chunk_28
import clifford.e8_chunk_29
import clifford.e8_chunk_30
