# ADR-006: SO(14) → SO(16) LieHom Compilation Gap

## Status

Accepted (2026-03-22)

## Context

### The Claimed Fifth LieHom

The project claims "Five certified LieHoms" composing into the chain
SU(5) →ₗ⁅ℝ⁆ SO(10) →ₗ⁅ℝ⁆ SO(14) →ₗ⁅ℝ⁆ SO(16). The file
`so14_so16_liehom.lean` contains the SO(14) → SO(16) embedding with
0 `sorry` in its source. However, this file is **not compiled** by
`lake build` and has not been since March 15, 2026.

### The Compilation Failure

`so14_so16_liehom.lean` imports `so16_grand` (the flat 120-generator
SO(16) type). As documented in ADR-005, the flat SO(16) produces a
2.2 GB `.olean` file that exceeds the 32-bit `stat()` limit. Any file
that imports `so16_grand` fails with:

```
failed to stat file 'so16_grand.olean': value too large
```

The flat `so16_grand.lean` itself compiles (Lean's kernel verifies it),
but the `.olean` it produces cannot be read by downstream importers.

### How the Gap Arose

Git history shows the file was in lakefile roots for exactly one commit
window, then accidentally dropped during a lakefile rewrite:

1. **`97a3fa2` (March 13)**: `so14_so16_liehom.lean` created.
2. **`96fce04` (March 13)**: Added to lakefile roots (67 roots). It was
   the last entry: `..., \`clifford.so14_so16_liehom]`.
3. **`4b1fb7e` (March 15)**: Lakefile rewritten for E₈ dense approach
   (100 roots). The old ending was replaced with E₈ chunk files. The
   `so14_so16_liehom` entry was not carried over.
4. **March 15–present**: Four subsequent lakefile rewrites (85→86→87→
   88→89 roots). `so14_so16_liehom` was never re-added.

The drop was accidental — a casualty of lakefile regeneration during the
E₈ approach transition. It was not a deliberate removal.

### What `so16_matrix.lean` Provides

ADR-005 introduced `so16_matrix.lean`, which defines SO(16) via
mathlib's `LieAlgebra.Orthogonal.so` (335 KB `.olean`). This is the
compiled path for SO(16). However, `so14_so16_liehom.lean` was never
updated to use the matrix type — it still imports the flat type.

## Decision

1. **Downgrade the LieHom claim** in README and CLAUDE.md from "Five
   certified LieHoms" to "Four certified LieHoms + 1 type bridge."
   Note the SO(14) → SO(16) step as a pending rewrite.

2. **Update the hierarchy diagram** to show the SO(14) → SO(16) step
   with the pending marker (`-?-`) rather than the certified marker
   (`==>`).

3. **Keep `so14_so16_liehom.lean`** in the repository as documentation
   of the intended construction. Its source code is correct (no `sorry`),
   but it is not machine-verified until it compiles.

4. **Define the remediation path**: rewrite the file to embed SO(14)
   into the matrix-based SO(16) from `so16_matrix.lean`. This is the
   same pattern used in `so14_to_matrix.lean` (the SO(14) type bridge).

### Remediation Steps (Not Yet Scheduled)

1. Rewrite `so14_so16_liehom.lean` to import `so16_matrix` instead of
   `so16_grand`.
2. Map the 91 flat `SO14` fields to explicit 16×16 antisymmetric
   matrices (block-diagonal embedding in the first 14 indices).
3. Prove bracket preservation using matrix commutator `[A,B] = AB - BA`
   instead of flat structure constant matching.
4. Pattern: follow `so14_to_matrix.lean`, which already maps 91 flat
   SO(14) fields to 14×14 antisymmetric matrices.
5. Add `clifford.so14_so16_liehom` back to lakefile roots.
6. Verify `lake build` passes.

Estimated effort: moderate. The `so14_to_matrix.lean` bridge required
~440 lines and a 4,095-equation bracket proof via `native_decide`. The
SO(14) → SO(16) embedding is structurally simpler (block-diagonal
inclusion), but the matrix dimension increases from 14×14 to 16×16.

## Consequences

### Positive
- README and CLAUDE.md accurately reflect what is machine-verified.
- The compilation gap is documented, not hidden.
- A clear remediation path exists for restoring the fifth LieHom.

### Negative
- The certified chain is currently SU(5) → SO(10) → SO(14) only.
  The SO(14) → SO(16) step and the SO(16) → E₈ step both require
  type bridge work.
- Papers that cite "five LieHoms" need correction.

### Neutral
- The flat `so16_grand.lean` and `so14_so16_liehom.lean` remain in
  the repository. The mathematics is likely correct (source has 0
  `sorry`), but "likely correct source" is not "machine-verified."
- The SO(16) → E₈ connection goes through subalgebra closure
  (`e8_so16_subalgebra.lean`), which IS compiled and verified. Only
  the typed `LieHom` is missing.
