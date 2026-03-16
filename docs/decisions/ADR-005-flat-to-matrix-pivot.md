# ADR-005: Pivot from Flat Generator Types to Mathlib Matrix Types

## Status

Accepted (2026-03-14)

## Context

### The Flat Approach (SO(10) through SO(16))

The project's original approach to Lie algebra construction uses "flat" structures:
explicit `@[ext] structure` types with one ℝ field per generator, manually defined
brackets, and kernel-verified `LieRing`/`LieAlgebra ℝ` instances. This pattern was
established with SO(10) (45 fields) and successfully extended to SO(14) (91 fields).

The flat approach was the only pattern available when SO(16) construction began. It had
been proven to work at scale, producing correct results for SO(10) and SO(14). There was
no empirical reason to believe 120 fields would hit a qualitatively different wall.

### The .olean Scaling Wall

SO(16) flat structure (120 fields) compiled successfully — Lean's kernel verified all
120 generators satisfy every Lie algebra axiom. **The mathematics is correct.** However,
the serialized .olean file grew to 2.2 GB, exceeding the 32-bit `stat` limit on the
filesystem. Downstream files fail with `failed to stat file: value too large`.

.olean size scales approximately O(N⁴) with the number of generators:
- SO(10), 45 generators: manageable .olean
- SO(14), 91 generators: large but usable .olean
- SO(16), 120 generators: 2.2 GB .olean, exceeds 32-bit file stat
- E₈, 248 generators: would be catastrophically larger — impossible via flat

### Why the Flat Route Was Taken First

1. **Proven pattern**: SO(10) and SO(14) both succeeded with flat structures.
2. **No scaling data**: .olean size growth was not measured until SO(16) hit the wall.
3. **Kernel verification value**: The flat approach produces the strongest form of
   verification — Lean's kernel checks every axiom from scratch, independent of mathlib.
4. **No known alternative**: The matrix approach (using mathlib's `so n R`) was not
   discovered until after SO(16) flat compilation revealed the need.

The flat route was not a mistake. It was a rational application of the proven pattern
to the next scale point. The scaling wall was an empirical discovery.

### What the Flat SO(16) Proved

The flat `so16_grand.lean` compilation remains a valid mathematical result:
- Lean's kernel confirmed that the 120-generator algebra satisfies all Lie algebra
  axioms (Jacobi identity, bilinearity, antisymmetry, Leibniz rule).
- This is an **independent verification** — it does not depend on any mathlib theorem
  about orthogonal Lie algebras.
- The file can still be compiled standalone; it just cannot be imported downstream.

### The Matrix Alternative

Mathlib already defines `LieAlgebra.Orthogonal.so n R` as a `LieSubalgebra` of
antisymmetric n×n matrices. This provides `LieRing` and `LieAlgebra R` instances
for free — inherited from the matrix ring and the `LieSubalgebra` construction.
The .olean for SO(16) via matrices is 335 KB (6,400× smaller than flat).

## Decision

1. **Adopt mathlib's matrix Lie algebra types** as the primary representation for
   so(n) at n ≥ 16. The flat approach remains viable for n ≤ 14.

2. **Keep the flat SO(16) file** (`so16_grand.lean`) as an independent verification
   artifact. It compiles, it's correct, and it serves as documentation of the
   scaling wall.

3. **Build all new LieHoms to/from SO(16)** using the matrix type `SO16M`.

4. **Accept the type bridge gap**: The flat types (SO10, SO14) and matrix types
   (SO14M, SO16M) are mathematically isomorphic but different Lean types. No
   `LieEquiv` bridges them yet. This gap is **honestly disclosed** in Paper 3.

5. **Use the matrix approach for E₈** (248×248 adjoint matrices over ℤ, verified
   by `native_decide`). The flat approach is mathematically impossible at this scale.

## Consequences

### Positive
- SO(16) LieHom (SO14M → SO16Block) now compiles and is usable (.olean: 335 KB)
- E₈ construction becomes feasible via 248×248 matrices (Phase 0 feasibility passed)
- Mathlib provides free instances — no manual Jacobi proofs needed
- Future so(n) constructions are trivial via `so (Fin n) R`

### Negative
- **Type bridge gap**: `SO14` (flat) ≠ `SO14M` (matrix). The four certified LieHoms
  do not compose into a single chain in Lean. Building the bridge requires a
  `LieEquiv SO14 SO14M` or `LieHom SO14 SO14M` (estimated effort: 4,095 bracket
  pairs via native_decide).
- **Weaker verification claim**: Matrix types inherit correctness from mathlib.
  The flat approach proves correctness from scratch. A reviewer could ask: "how do
  you know mathlib's `so n R` is correct?" (Answer: mathlib is itself machine-verified,
  but the chain is longer.)
- **Two representations in one paper**: Paper 3 must explain why some morphisms use
  flat types and others use matrix types.

### Neutral
- The flat SO(16) file remains in the repository as a compilation artifact.
  It can serve as a reference point for the scaling wall, as an independent
  mathematical verification, and as a potential future asset if 64-bit file stat
  support is added to the Lean build system.
- The flat SO(10) and SO(14) files remain the canonical types for all existing
  LieHoms (SU5C→SO10, SO10→SO14, SO4→SO14).
- The matrix approach is strictly necessary for E₈ and any larger algebras.
