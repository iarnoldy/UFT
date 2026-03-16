/-
UFT Formal Verification - SO(16) via Mathlib Matrix Lie Algebra
================================================================

THE so(16) LIE ALGEBRA AS A MATHLIB LieSubalgebra OF MATRICES

This file defines so(16) using mathlib's `LieAlgebra.Orthogonal.so` construction:
  so(16) = {A in Mat(16,R) | A^T = -A}

This is a `LieSubalgebra R (Matrix (Fin 16) (Fin 16) R)`, which automatically
inherits `LieRing` and `LieAlgebra R` instances from mathlib's infrastructure.

MOTIVATION: The flat 120-field SO16 type (so16_grand.lean) compiles but produces
a 2.2 GB .olean file, exceeding 32-bit file stat limits. This matrix approach
uses mathlib's existing types, avoiding the .olean explosion entirely.

KEY ADVANTAGES OVER FLAT APPROACH:
  - No manual bracket definition (120*120 = 14,400 terms)
  - No manual Jacobi proof (follows from associativity of matrix multiplication)
  - No manual LieRing/LieAlgebra instances (inherited from LieSubalgebra)
  - Small .olean file (uses mathlib's matrix types)

The bracket is the matrix commutator: [A, B] = A * B - B * A.
This is provably equivalent to the structure constants formula:
  [L_{ij}, L_{kl}] = d_{jk}L_{il} - d_{ik}L_{jl} - d_{jl}L_{ik} + d_{il}L_{jk}

WHAT THIS FILE PROVES:
  1. so(16) as a LieSubalgebra of matrices (via mathlib)
  2. Membership criterion: A in so(16) iff A^T = -A
  3. Free LieRing and LieAlgebra R instances (inherited)
  4. Standard basis element constructor (E_{ij} - E_{ji})
  5. so(14) embeds into so(16) via block inclusion (using fromBlocks)
  6. Lie equivalence between Fin 14 + Fin 2 and Fin 16 index types

References:
  - Mathlib.Algebra.Lie.Classical: `LieAlgebra.Orthogonal.so`
  - Mathlib.Algebra.Lie.SkewAdjoint: bracket closure for skew-adjoint matrices
  - so16_grand.lean: the flat version (120 fields, 2.2 GB .olean)
-/

import Mathlib.Algebra.Lie.Classical
import Mathlib.Data.Real.Basic

/-! ## Part 1: The so(16) Lie Algebra as a Matrix LieSubalgebra

Mathlib already defines:
  `LieAlgebra.Orthogonal.so (Fin 16) R : LieSubalgebra R (Matrix (Fin 16) (Fin 16) R)`

We give it a convenient abbreviation. -/

open scoped Matrix
open LieAlgebra.Orthogonal

/-- The Lie algebra so(16), defined as the subalgebra of 16x16 skew-symmetric real matrices.
    This is `{A : Matrix (Fin 16) (Fin 16) R | A^T = -A}`.
    Dimension = 16 * 15 / 2 = 120 generators. -/
abbrev SO16M := LieAlgebra.Orthogonal.so (Fin 16) ℝ

-- The LieRing and LieAlgebra instances are automatic.
-- These #check commands verify they exist:
#check (inferInstance : LieRing SO16M)
#check (inferInstance : LieAlgebra ℝ SO16M)

/-! ## Part 2: Membership and Bracket

The membership criterion is: A in so(16) iff A^T = -A.
The bracket is the matrix commutator: [A, B] = A * B - B * A. -/

/-- An element of SO16M is a matrix A with A^T = -A. -/
theorem SO16M_mem (A : Matrix (Fin 16) (Fin 16) ℝ) :
    A ∈ SO16M ↔ Aᵀ = -A :=
  LieAlgebra.Orthogonal.mem_so _ _ A

/-- The Lie bracket in SO16M is the matrix commutator. -/
theorem SO16M_bracket_val (A B : SO16M) :
    (⁅A, B⁆ : SO16M).val = A.val * B.val - B.val * A.val := by
  rfl

/-! ## Part 3: Standard Basis Elements

The standard basis for so(n) consists of matrices E_{ij} - E_{ji}
for i < j, where E_{ij} is the matrix with 1 at position (i,j) and 0 elsewhere.
These correspond to the generators L_{ij} in the flat representation. -/

/-- The antisymmetric basis element E_{ij} - E_{ji}.
    This is the matrix-representation analog of the generator L_{ij}.
    Uses `Matrix.single` (the matrix with one nonzero entry). -/
def soGenerator (i j : Fin 16) : Matrix (Fin 16) (Fin 16) ℝ :=
  Matrix.single i j 1 - Matrix.single j i 1

/-- The antisymmetric basis element is indeed skew-symmetric. -/
theorem soGenerator_skew (i j : Fin 16) :
    (soGenerator i j)ᵀ = -(soGenerator i j) := by
  unfold soGenerator
  rw [Matrix.transpose_sub, Matrix.transpose_single, Matrix.transpose_single]
  abel

/-- The antisymmetric basis element is in so(16). -/
theorem soGenerator_mem (i j : Fin 16) :
    soGenerator i j ∈ SO16M := by
  rw [SO16M_mem]
  exact soGenerator_skew i j

/-- Lift the generator to an element of SO16M. -/
def soGeneratorM (i j : Fin 16) : SO16M :=
  ⟨soGenerator i j, soGenerator_mem i j⟩

/-! ## Part 4: The Inclusion SO16M into Matrices

The inclusion map is automatic via `LieSubalgebra.incl`. -/

/-- The inclusion SO16M into Matrix (Fin 16) (Fin 16) R as a LieHom.
    This is the canonical embedding of the subalgebra into the ambient algebra. -/
def SO16M_incl : SO16M →ₗ⁅ℝ⁆ Matrix (Fin 16) (Fin 16) ℝ :=
  SO16M.incl

/-! ## Part 5: so(14) inside so(16) via block embedding

We use `Fin 14 + Fin 2` as the index type for the block decomposition.
`Matrix.fromBlocks` gives clean algebraic structure:
  `(fromBlocks A 0 0 0)^T = fromBlocks A^T 0 0 0`
  `-(fromBlocks A 0 0 0) = fromBlocks (-A) 0 0 0`

Then `Matrix.reindexLieEquiv` connects `Fin 14 + Fin 2` to `Fin 16`. -/

/-- so(16) indexed by Fin 14 + Fin 2 (equivalent to Fin 16, better for blocks). -/
abbrev SO16Block := LieAlgebra.Orthogonal.so (Fin 14 ⊕ Fin 2) ℝ

/-- so(14) as a matrix LieSubalgebra. -/
abbrev SO14M := LieAlgebra.Orthogonal.so (Fin 14) ℝ

-- Free instances for all matrix-based types
#check (inferInstance : LieRing SO16Block)
#check (inferInstance : LieAlgebra ℝ SO16Block)
#check (inferInstance : LieRing SO14M)
#check (inferInstance : LieAlgebra ℝ SO14M)

/-- Block-embed a 14x14 matrix into a (14+2)x(14+2) matrix: upper-left block. -/
def blockEmbed (A : Matrix (Fin 14) (Fin 14) ℝ) :
    Matrix (Fin 14 ⊕ Fin 2) (Fin 14 ⊕ Fin 2) ℝ :=
  Matrix.fromBlocks A 0 0 0

/-- Block embedding preserves skew-symmetry. -/
theorem blockEmbed_skew {A : Matrix (Fin 14) (Fin 14) ℝ} (hA : Aᵀ = -A) :
    (blockEmbed A)ᵀ = -(blockEmbed A) := by
  simp only [blockEmbed, Matrix.fromBlocks_transpose, Matrix.fromBlocks_neg,
    Matrix.transpose_zero, neg_zero, hA]

/-- Block embedding maps so(14) elements into so(16). -/
theorem blockEmbed_mem_so16block {A : Matrix (Fin 14) (Fin 14) ℝ}
    (hA : A ∈ SO14M) :
    blockEmbed A ∈ SO16Block := by
  rw [LieAlgebra.Orthogonal.mem_so _ _]
  exact blockEmbed_skew ((LieAlgebra.Orthogonal.mem_so _ _ A).mp hA)

/-- The Lie equivalence between so(16) indexed by Fin 14 + Fin 2 and Fin 16.
    This uses mathlib's `Matrix.reindexLieEquiv` with the canonical
    `finSumFinEquiv : Fin 14 + Fin 2 ≃ Fin 16`. -/
noncomputable def so16_reindex :
    Matrix (Fin 14 ⊕ Fin 2) (Fin 14 ⊕ Fin 2) ℝ ≃ₗ⁅ℝ⁆ Matrix (Fin 16) (Fin 16) ℝ :=
  Matrix.reindexLieEquiv finSumFinEquiv

/-! ## Part 6: Dimension Statement

The dimension of so(n) is n(n-1)/2. For n=16, this is 120.
We state this; a full proof would require constructing a basis. -/

/-- The expected dimension of so(16) is 120 = 16 * 15 / 2. -/
theorem so16_expected_dim : 16 * (16 - 1) / 2 = 120 := by norm_num

/-- The expected dimension of so(14) is 91 = 14 * 13 / 2. -/
theorem so14_expected_dim : 14 * (14 - 1) / 2 = 91 := by norm_num

/-! ## Part 7: so(14) →ₗ⁅ℝ⁆ so(16) as a Certified LieHom (Matrix World)

The block-diagonal embedding SO14M → SO16Block sends a 14×14 antisymmetric matrix
to a (14+2)×(14+2) antisymmetric matrix with zeros in the last 2 rows/columns.

The bracket preservation is immediate from `fromBlocks_multiply`:
  [blockEmbed A, blockEmbed B] = blockEmbed(AB) - blockEmbed(BA)
                                = blockEmbed(AB - BA)
                                = blockEmbed([A, B])

Combined with `so16_reindex`, this gives SO14M →ₗ⁅ℝ⁆ SO16M via composition. -/

/-- The block embedding as a function from SO14M to SO16Block (subtype-level). -/
def so14m_to_so16block (A : SO14M) : SO16Block :=
  ⟨blockEmbed A.val, blockEmbed_mem_so16block A.property⟩

/-- Block embedding preserves addition. -/
theorem so14m_to_so16block_add (A B : SO14M) :
    so14m_to_so16block (A + B) = so14m_to_so16block A + so14m_to_so16block B := by
  apply Subtype.ext
  show blockEmbed (↑(A + B)) = ↑(so14m_to_so16block A + so14m_to_so16block B)
  rw [AddMemClass.coe_add, AddMemClass.coe_add]
  simp only [so14m_to_so16block, blockEmbed, Matrix.fromBlocks_add, add_zero]

/-- Block embedding preserves scalar multiplication. -/
theorem so14m_to_so16block_smul (r : ℝ) (A : SO14M) :
    so14m_to_so16block (r • A) = r • so14m_to_so16block A := by
  apply Subtype.ext
  show blockEmbed (↑(r • A)) = ↑(r • so14m_to_so16block A)
  rw [SetLike.val_smul, SetLike.val_smul]
  simp only [so14m_to_so16block, blockEmbed, Matrix.fromBlocks_smul, smul_zero]

/-- Block embedding preserves the Lie bracket.
    This is the key theorem: the matrix commutator of block-embedded matrices
    equals the block embedding of the matrix commutator. -/
theorem so14m_to_so16block_lie (A B : SO14M) :
    so14m_to_so16block ⁅A, B⁆ = ⁅so14m_to_so16block A, so14m_to_so16block B⁆ := by
  apply Subtype.ext
  show blockEmbed (↑⁅A, B⁆) = ↑⁅so14m_to_so16block A, so14m_to_so16block B⁆
  rw [LieSubalgebra.coe_bracket, LieSubalgebra.coe_bracket]
  simp only [LieRing.of_associative_ring_bracket, so14m_to_so16block, blockEmbed]
  rw [sub_eq_add_neg, sub_eq_add_neg]
  simp only [Matrix.fromBlocks_multiply, Matrix.fromBlocks_neg, Matrix.fromBlocks_add]
  congr 1 <;> simp [mul_zero, zero_mul, add_zero, neg_zero]

/-- The certified Lie algebra homomorphism SO14M →ₗ⁅ℝ⁆ SO16Block.
    so(14) embeds into so(16) via block-diagonal inclusion. -/
def so14m_embed_block : SO14M →ₗ⁅ℝ⁆ SO16Block :=
  { toLinearMap := {
      toFun := so14m_to_so16block
      map_add' := so14m_to_so16block_add
      map_smul' := so14m_to_so16block_smul
    }
    map_lie' := fun {x} {y} => so14m_to_so16block_lie x y }

/-! ## Summary

### What this file provides:
1. `SO16M` : so(16) as a `LieSubalgebra R (Matrix (Fin 16) (Fin 16) R)` [Part 1]
2. Free `LieRing` and `LieAlgebra R` instances (no manual proofs!) [Part 1]
3. Membership: `A in SO16M iff A^T = -A` [Part 2]
4. Bracket: `[A, B].val = A.val * B.val - B.val * A.val` [Part 2]
5. Standard basis generators `soGeneratorM i j` [Part 3]
6. Canonical inclusion `SO16M.incl : SO16M -> Matrix (Fin 16) (Fin 16) R` [Part 4]
7. Block embedding `blockEmbed` via `fromBlocks` preserving skew-symmetry [Part 5]
8. `so16_reindex`: Lie equivalence between Fin 14 + Fin 2 and Fin 16 indexing [Part 5]
9. Dimension arithmetic: 16*15/2 = 120 [Part 6]

### What this enables:
- **Replace so16_grand.lean**: Same algebra, vastly smaller .olean
- **SO14 -> SO16M**: Via block embedding (bridge from flat SO14 or matrix SO14)
- **E_8 construction**: so(16) subalgebra of E_8 uses this matrix type
- **Indefinite forms**: `so' p q R` gives so(p,q) for Lorentzian signature

### Relationship to existing files:
- `so16_grand.lean`: The flat 120-field version (2.2 GB .olean, broken downstream)
- `so14_so16_liehom.lean`: Depends on so16_grand.lean (currently broken)
- `so14_grand.lean`: The flat SO14 type (works, 91 fields)

The next step is to build the LieHom `SO14 -> SO16M` that bridges the flat
SO14 type to the matrix SO16 type, replacing the broken flat-to-flat morphism.

0 sorry gaps.
-/
