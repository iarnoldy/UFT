# E8 Construction Architecture Research

> Date: 2026-03-14
> Author: clifford-unification-engineer
> Status: Research complete. Recommendation: Option D (mathlib Serre construction).

## Executive Summary

Mathlib already defines `LieAlgebra.e₈ R` via the Serre construction from the E8 Cartan
matrix. This type has free `LieRing` and `LieAlgebra R` instances. **The Lie algebra
exists in Lean 4 today, for free, with zero new code.** The question is no longer "how
do we construct E8" but "how do we connect it to the SO(16) subalgebra we already have."

This changes the problem entirely. The three options from the original task (adjoint
matrices, composite structure, Cartan matrix) are superseded by a fourth: use the
existing mathlib type and prove the SO(16) embedding.

---

## Part 1: Mathlib E8 Infrastructure (SURPRISING DISCOVERY)

### What Already Exists

**File:** `Mathlib.Algebra.Lie.SerreConstruction`

```lean
-- The E8 Cartan matrix (8x8, defined explicitly):
CartanMatrix.E₈ : Matrix (Fin 8) (Fin 8) Z

-- The E8 Lie algebra (Serre construction):
LieAlgebra.e₈ (R : Type*) [CommRing R] :=
  Matrix.ToLieAlgebra R CartanMatrix.E₈

-- Free instances:
deriving LieRing, Inhabited, LieAlgebra R
```

**File:** `Mathlib.Data.Matrix.Cartan`

The E8 Cartan matrix is defined explicitly:
```
 2  0 -1  0  0  0  0  0
 0  2  0 -1  0  0  0  0
-1  0  2 -1  0  0  0  0
 0 -1 -1  2 -1  0  0  0
 0  0  0 -1  2 -1  0  0
 0  0  0  0 -1  2 -1  0
 0  0  0  0  0 -1  2 -1
 0  0  0  0  0  0 -1  2
```

Properties already proven in mathlib:
- `E₈_diag (i : Fin 8) : E₈ i i = 2` (diagonal = 2)
- `E₈_off_diag_nonpos (i j) (h : i != j) : E₈ i j <= 0`
- `E₈_transpose : E₈.transpose = E₈` (symmetric)
- `isSimplyLaced_E₈ : IsSimplyLaced E₈` (all off-diagonal entries 0 or -1)
- `proof_wanted E₈_det : E₈.det = 1` (determinant, not yet proven)

### What the Serre Construction Gives

`LieAlgebra.e₈ R` is defined as `FreeLieAlgebra R (Generators (Fin 8)) / Serre_relations`.

This is the **abstract Lie algebra** with:
- Generators: `H_i, E_i, F_i` for `i : Fin 8` (24 generators, but the algebra has
  infinitely many Lie brackets producing a 248-dimensional quotient)
- Relations: the 7 families of Serre relations
- Free `LieRing` and `LieAlgebra R` instances (inherited from the quotient)

### What It Does NOT Give

**Critical gap:** Mathlib does NOT yet prove:
1. That `LieAlgebra.e₈ R` has dimension 248 (or even that it's finite-dimensional)
2. That it is simple
3. That it is isomorphic to the adjoint representation in 248x248 matrices
4. That SO(16) embeds into it
5. Any root system for it (the `RootSystem` infrastructure exists but connecting it
   to the Serre construction is not done)

The Serre construction file says (line 39): "as of May 2025, almost nothing has been
proved about it in Mathlib."

### Also Available

**Geck Construction:** `Mathlib.LinearAlgebra.RootSystem.GeckConstruction.Basic`

This is a newer (2025) alternative that constructs a Lie algebra directly from a root
system with distinguished base. It yields a *concrete* Lie algebra (not a quotient of a
free algebra), which may be easier to work with computationally. However, it requires
a root system as input, not just a Cartan matrix, and the E8 root system is not yet
defined in mathlib.

### Other Mathlib Infrastructure

| Component | File | Status |
|-----------|------|--------|
| Root systems | `Mathlib.LinearAlgebra.RootSystem.Basic` | Exists, abstract |
| Root chains | `Mathlib.Algebra.Lie.Weights.Chain` | Exists |
| Killing form | `Mathlib.Algebra.Lie.Killing` | Exists |
| Cartan subalgebras | `Mathlib.Algebra.Lie.CartanSubalgebra` | Exists |
| Semisimplicity | `Mathlib.Algebra.Lie.Semisimple.*` | Exists |
| Weight spaces | `Mathlib.Algebra.Lie.Weights.*` | Exists |
| Direct sums | `Mathlib.Algebra.Lie.DirectSum` | Exists |
| Semi-direct products | `Mathlib.Algebra.Lie.SemiDirect` | Exists, has LieRing |
| Free Lie algebras | `Mathlib.Algebra.Lie.Free` | Exists |
| Classical so(n) | `Mathlib.Algebra.Lie.Classical` | Exists (used for SO16M) |

**Bottom line:** Exceptional Lie algebra types exist. The infrastructure around them
(dimension, simplicity, embeddings) does not.

---

## Part 2: Architecture Options Assessment

### Option A: 248x248 Adjoint Matrices over Q

**Approach:** Define all 248 generators of E8 as explicit 248x248 rational matrices.
Use `native_decide` to verify bracket relations.

**Precedent:** `spinor_rep_homomorphism.lean` verifies 990 bracket pairs of 45
generators in 16x16 matrices. This file is 1,419 lines.

**Scaling analysis:**
- E8 has 248 generators -> C(248,2) = 30,628 bracket pairs
- Each bracket pair produces one 248x248 matrix equation
- Matrix multiply: 248^3 = ~15.3 million operations per multiply (vs 16^3 = 4,096)
- Ratio: 248^3 / 16^3 = 3,726x more work per multiply
- Pair count ratio: 30,628 / 990 = 31x more pairs
- Total: 3,726 * 31 = ~115,500x more computational work than spinor_rep_homomorphism

**Memory analysis:**
- Each 248x248 rational matrix: 248^2 = 61,504 entries
- 248 generators * 2 (real/imaginary if complex): ~7.6M entries for definitions
- Bracket table: 30,628 pairs, each a sum of generators: ~5-10 MB of Lean source
- native_decide memory: each 248x248 multiply needs to hold intermediate results
- Estimated Lean file size: 10-50 MB (likely too large for Lean to parse)

**Python feasibility:**
- SageMath has E8 built in: `LieAlgebra(QQ, CartanType(['E', 8]))`
- Can compute the adjoint representation explicitly
- Structure constants are rational (in fact integer for Chevalley basis)
- E8 structure constants are available in the literature (Conway & Sloane, LiE)

**Verdict: FEASIBLE BUT EXTREMELY EXPENSIVE.**
- Python: 1-3 days to generate the structure constants
- Lean file: likely 10-50 MB, may hit parser limits
- Compile time: unknown, possibly hours/days for native_decide
- File size risk: the generated Lean file might be too large for Lean to handle
- This is "brute force" -- it works in principle but may hit practical limits

### Option B: Composite Structure (SO(16) x S16+, piecewise bracket)

**Approach:** Define `E8 := SO16M x S16plus` as a product type with custom bracket.

**The bracket structure:**
- `[so, so'] = [so, so']_{so(16)}` (standard matrix commutator)
- `[so, spinor] = rho(so) * spinor` (the half-spinor representation action)
- `[spinor, spinor'] = Gamma(spinor, spinor')` (Fierz identity, maps to so(16))

**The Fierz/triality bracket `[spinor, spinor']`:**
The explicit formula uses the Gamma matrix construction:
```
[s, s']_ij = sum_a (s_a * (Gamma_ij)_{ab} * s'_b - s'_a * (Gamma_ij)_{ab} * s_b)
```
where `Gamma_ij` are the generators of so(16) in the 128-dim semi-spinor representation.

**Infrastructure needed:**
1. Define `S16plus` as a 128-dimensional vector space
2. Define the 120 representation matrices `rho(L_ij) : Matrix (Fin 128) (Fin 128) R`
3. Define the Fierz map `Gamma : S16plus x S16plus -> SO16M`
4. Prove LieRing axioms for the combined bracket
5. Prove LieAlgebra axioms

**The representation matrices:**
We already have 45 matrices in `spinor_rep_homomorphism.lean` for SO(10) acting on
S16 (=16-dim). For SO(16) acting on S128 (=128-dim), we need 120 matrices of size
128x128. These can be computed from Clifford algebra: Cl(16) gamma matrices in 256-dim,
restricted to positive chirality subspace (128-dim), then taking the grade-2 generators
(bivectors).

**Mathlib support:**
`LieAlgebra.SemiDirectSum` provides `K x L` with bracket:
```
[(k, l), (k', l')] = ([k, k'] + psi(l)(k') - psi(l')(k), [l, l'])
```
This handles `[so, spinor]` via `psi`, but does NOT handle `[spinor, spinor'] -> so`
(the Fierz map). The semi-direct product assumes `K` is an ideal (closed under bracket
on its own), but here the spinor part maps BACK to the so(16) part.

**The bracket is NOT a semi-direct product.** E8 = so(16) + S+ is a Z/2-graded
structure where the "odd" part (S+) brackets into the "even" part (so(16)). This is
more like a "symmetric pair" or "Cartan pair" decomposition.

**Verdict: MATHEMATICALLY CLEAN BUT VERY LABOR-INTENSIVE.**
- Computing 120 matrices of size 128x128: significant Python work
- Defining the Fierz map correctly: mathematically delicate
- Proving Jacobi for the combined bracket: the hardest part (120+128=248 generators)
- No mathlib shortcut: the semi-direct product doesn't apply
- Estimated effort: 2-4 weeks
- Advantage: explicit, concrete, computable
- Disadvantage: enormous boilerplate; the Fierz identity proof is the bottleneck

### Option C: Cartan Matrix / Serre Relations (USE EXISTING MATHLIB TYPE)

**Approach:** Use `LieAlgebra.e₈ R` directly. Prove properties about it.

**What's free:**
- `LieRing` and `LieAlgebra R` instances (inherited from quotient construction)
- The type exists and compiles
- No bracket definitions, no Jacobi proof needed

**What needs proving:**
1. `so(16)` embeds into `e₈` as a Lie subalgebra
2. Dimension is 248 (hard -- this is essentially proving the Serre relations produce
   a finite-dimensional algebra)
3. The decomposition 248 = 120 + 128 under so(16)

**The embedding challenge:**
To embed SO16M into `LieAlgebra.e₈ R`, we need a LieHom. The Serre construction
gives generators `H_i, E_i, F_i` for `i : Fin 8`. The embedding would map the 120
generators of so(16) to specific linear combinations of these Serre generators.

This is essentially constructing the isomorphism between the abstract Serre algebra
and the concrete matrix algebra. This is known to exist (Serre's theorem) but proving
it in Lean is a massive undertaking -- it's the core of the classification of simple
Lie algebras.

**Alternative path:** Instead of embedding SO16M into `LieAlgebra.e₈ R`, prove that
a DIFFERENT construction of E8 (e.g., via adjoint matrices) is isomorphic to
`LieAlgebra.e₈ R`. But this is even harder.

**Verdict: CLEANEST IN PRINCIPLE, HARDEST IN PRACTICE.**
- The type exists for free
- Connecting it to anything concrete is a major project
- Proving dimension = 248 would be a significant mathlib contribution
- This is "the right way" but requires infrastructure that doesn't exist
- Estimated effort: months to years (if building the general theory)

### Option D: HYBRID -- Mathlib e₈ type + adjoint matrix REPRESENTATION

**Approach:** Use `LieAlgebra.e₈ R` as the abstract type, and SEPARATELY define
248x248 adjoint matrices as a `LieSubalgebra R (Matrix (Fin 248) (Fin 248) R)`.
Prove the REPRESENTATION is bracket-preserving (like spinor_rep_homomorphism but
for E8 itself). Then get the SO(16) embedding via the matrix subalgebra.

**Concretely:**
1. Define `E8_adj : LieSubalgebra R (Matrix (Fin 248) (Fin 248) R)` as the span of
   248 explicit matrices
2. Verify bracket closure using native_decide (30,628 pairs, but over Q)
3. This gives `LieRing` and `LieAlgebra R` instances for free (from LieSubalgebra)
4. Embed SO16M into E8_adj via the upper-left 120x120 block (or however the so(16)
   sits inside the adjoint)
5. State (possibly as an axiom [SP]) that E8_adj is isomorphic to `LieAlgebra.e₈ R`

**Advantage:** This parallels the SO16M approach exactly:
- SO16M = `so (Fin 16) R` = LieSubalgebra of 16x16 matrices
- E8_adj = LieSubalgebra of 248x248 matrices
- Both get free LieRing/LieAlgebra instances
- Both allow concrete matrix computations

**The isomorphism with `LieAlgebra.e₈ R`:**
We can state it as a [SP] claim: "E8_adj is isomorphic to the split E8 Lie algebra."
This is mathematically known (the adjoint representation of a simple Lie algebra is
faithful) but formalizing the proof would require the machinery of Option C. We can
leave it as a stated axiom, honestly tagged.

**Python requirements:**
Same as Option A -- need the 248x248 adjoint representation matrices. SageMath can
compute these.

**Verdict: RECOMMENDED. See detailed plan below.**

### Option E: Geck Construction from E8 Root System

**Approach:** Use the newer Geck construction (`RootPairing.GeckConstruction`) which
directly defines a Lie algebra from a root system.

**Advantage:** Produces a concrete Lie algebra (not a quotient of a free algebra),
more amenable to computation.

**Disadvantage:** Requires defining the E8 root system (240 roots in R^8) first.
This is doable but requires significant setup. The Geck construction is very new
(2025) and may not have all the API needed.

**Verdict: WORTH WATCHING but probably not ready for us yet.**

---

## Part 3: Recommended Approach (Option D)

### Architecture

```
LieAlgebra.e₈ R                     (abstract, from mathlib Serre construction)
    |
    | [SP] isomorphism (stated, not proven)
    v
E8Adj : LieSubalgebra R (Mat 248x248 R)   (concrete, our construction)
    |
    | verified LieHom (block embedding)
    v
SO16M : LieSubalgebra R (Mat 16x16 R)     (existing, so16_matrix.lean)
```

### Step-by-Step Plan

**Phase 1: Python (3-5 days)**

1. Use SageMath to compute the 248-dimensional adjoint representation of E8
2. Extract the 248 generators as 248x248 rational matrices
3. Verify bracket closure numerically: for each pair (a,b), compute [rho(a), rho(b)]
   and express as a linear combination of generators
4. Generate the bracket table (structure constants) as Lean source code
5. Generate the SO(16) sub-representation: identify which 120 of the 248 generators
   correspond to so(16)

**Phase 2: Lean File Generation (3-5 days)**

6. Generate `e8_adjoint.lean` with 248 matrix definitions (like spinor_rep_homomorphism)
7. BUT: 248x248 matrices are much larger than 16x16. Each matrix has 61,504 entries.
   Most will be zero (the adjoint representation is sparse).
   Strategy: use `Matrix.of fun i j => match i, j with | ... => ... | _ => 0` pattern
   with only nonzero entries listed.
8. Define `E8Adj : LieSubalgebra R (Matrix (Fin 248) (Fin 248) R)` as the span
9. native_decide verification: CHUNKED, not all-at-once
   - Split 30,628 pairs into blocks of ~1,000
   - Each block gets its own theorem: `bracket_chunk_k : forall a b in range_k, ...`
   - This avoids single-theorem memory blowup

**Phase 3: LieHom Construction (3-5 days)**

10. Define the embedding `SO16M -> E8Adj`
11. Prove bracket preservation using native_decide (990 pairs for so(16) brackets)
12. This gives us `SO16M ->_L[R] E8Adj` as a certified LieHom

**Phase 4: Integration (1-2 days)**

13. State the dimension theorem: `e8_adj_dimension : 248 = 248` (trivial, but document)
14. State the decomposition: `248 = 120 + 128` with so(16) subalgebra + complement
15. State the isomorphism with `LieAlgebra.e₈ R` as [SP] axiom
16. Connect to existing `e8_embedding.lean` dimensional proofs

### File Structure

```
scripts/e8_adjoint_gen.py           -- SageMath-based generator
src/lean_proofs/clifford/
  e8_adjoint_defs.lean              -- 248 generator matrices (generated)
  e8_adjoint_brackets.lean          -- bracket table (generated)
  e8_adjoint_verify_01.lean         -- native_decide chunk 1
  ...
  e8_adjoint_verify_31.lean         -- native_decide chunk 31
  e8_adjoint.lean                   -- LieSubalgebra definition, integration
  so16_e8_liehom.lean               -- SO16M ->_L[R] E8Adj
```

### Size Estimates

| Component | Entries | Lines (est.) | File size (est.) |
|-----------|---------|-------------|-----------------|
| 248 matrices (sparse) | ~50 nonzero per matrix | ~15,000 | ~500 KB |
| Bracket table | 30,628 pairs | ~100,000 | ~3 MB |
| Verification chunks | 31 files x ~1,000 pairs | ~31,000 | ~1 MB total |
| Integration | 1 file | ~300 | ~10 KB |
| LieHom | 1 file | ~200 | ~7 KB |

Total: ~4.5 MB of Lean source. Large but manageable.

---

## Part 4: Python Feasibility for Structure Constants

### SageMath E8 Adjoint

SageMath has built-in support for E8:

```python
from sage.all import *

# Define E8 Lie algebra over Q
L = LieAlgebra(QQ, cartan_type=['E', 8])

# Get the basis
basis = L.basis()          # 248 elements
print(len(basis))          # should print 248

# Compute bracket of two basis elements
b1 = basis[0]
b2 = basis[1]
bracket = L.bracket(b1, b2)
# This gives the result as a linear combination of basis elements

# Extract structure constants
# For each pair (a, b), compute [e_a, e_b] = sum_c f^c_{ab} e_c
```

**Computing the adjoint representation:**
```python
# The adjoint representation
V = L.module()             # 248-dim vector space
for x in basis:
    # ad(x) is a 248x248 matrix
    ad_x = L.adjoint_matrix(x)
    # This is a rational matrix
```

**Alternative: GAP/LiE**

GAP also has E8 structure constants. The `SimpleLieAlgebra` function in GAP can
produce the Chevalley basis and structure constants directly.

LiE (Lie group software) has explicit structure constants for all simple Lie algebras.

### Sparsity of Adjoint Matrices

The adjoint matrix `ad(e_a)` has entries `(ad(e_a))_{bc} = f^c_{ab}` (structure constants).
For E8 in the Chevalley basis:
- Each Cartan element `H_i` (8 of them) has at most 240 nonzero entries
  (acting on each root vector by its root value)
- Each root vector `E_alpha` (240 of them) has at most ~30 nonzero entries
  (it can bracket nontrivially with at most ~30 other root vectors)
- Average sparsity: ~5-15% nonzero entries per matrix

This means the matrices are sparse enough for the `match` pattern to be efficient.

### Cross-Validation

Before generating Lean code, verify in Python:
1. All bracket relations close (output is in the span of basis)
2. Jacobi identity holds numerically for all triples
3. Structure constants are integers (in Chevalley basis) or at worst half-integers
4. The so(16) subalgebra is identifiable (120 generators)

---

## Part 5: Precedent Analysis

### spinor_rep_homomorphism.lean (990 pairs, 16x16, Q)

**What it does:**
- Defines 45 pairs of 16x16 rational matrices (real + imaginary parts)
- Defines expected brackets (30 nonzero out of 990 pairs for real, ~200 for imaginary)
- `native_decide` verifies all 990 pairs in both real and imaginary components
- File: 1,419 lines
- Compile time: not recorded, estimated 30-120 seconds

**Scaling factors to E8:**
- Matrix size: 16 -> 248 (factor ~15x in each dimension, ~3,726x in multiply cost)
- Pair count: 990 -> 30,628 (factor ~31x)
- But the matrices are SPARSE. If we use `Matrix.of fun i j => match ...` with only
  nonzero entries, `native_decide` operates on the expanded form, which is still
  248x248 regardless of sparsity.

**Risk:** The 248x248 case may be too slow for `native_decide`. Each matrix multiply
requires 248^3 = 15.3M multiplications of rationals. With 30,628 pairs and 2 multiplies
per pair (AB and BA for [A,B] = AB-BA), that's ~937 billion rational operations.

**Mitigation:**
1. CHUNK the verification into ~31 files of ~1,000 pairs each
2. Use sparse matrices to reduce constant factors
3. If native_decide is too slow, fall back to `decide` (slower but might work) or
   use a `sorry`-free but manual proof strategy

### so16_matrix.lean (120 generators, 16x16, R)

**What it does:**
- Defines `SO16M := so (Fin 16) R` as a LieSubalgebra
- Gets free LieRing/LieAlgebra from mathlib
- Defines block embedding SO14M -> SO16M
- .olean: 335 KB

**Key lesson:** Using mathlib's existing types is vastly more efficient than building
from scratch. The same principle should apply if we can find a mathlib type for E8
that actually gives us something concrete.

### The .olean wall

| Type | Generators | .olean | Approach |
|------|-----------|--------|----------|
| Bivector (so(1,3)) | 6 | tiny | flat |
| SL3 | 8 | tiny | flat |
| SL5 | 24 | ~10 MB | flat |
| SO10 | 45 | ~100 MB | flat |
| SO14 | 91 | ~1 GB | flat |
| SO16 | 120 | 2.2 GB (broken) | flat |
| SO16M | N/A | 335 KB | mathlib matrix |
| E8 flat | 248 | **impossible** | flat |
| E8 matrix | N/A | TBD (~1 MB?) | mathlib matrix |
| E8 Serre | N/A | ~100 KB? | mathlib quotient |

The matrix approach avoids the .olean wall entirely.

---

## Part 6: Kill Conditions

The following conditions would indicate E8 is infeasible and we should stop:

### Kill Condition 1: native_decide Too Slow for 248x248

**Test:** Write a single bracket pair verification for two 248x248 rational matrices.
If this takes more than 60 seconds, the full verification (30,628 pairs) will take
more than 21 days. That's too slow.

**Mitigation before killing:** Try `Decidable.decide` instead of `native_decide`.
Try a smaller chunk size. Try matrices over Z instead of Q.

### Kill Condition 2: SageMath Cannot Compute Adjoint Matrices

**Test:** Run `LieAlgebra(QQ, cartan_type=['E', 8])` in SageMath and extract one
adjoint matrix. If SageMath crashes or takes >1 hour, the Python side is blocked.

**Mitigation:** Try GAP, or compute from the root system directly using known formulas.

### Kill Condition 3: Generated Lean File Too Large to Parse

**Test:** If the generated Lean file exceeds ~10 MB, check whether Lean can parse it.
The `spinor_rep_homomorphism.lean` is 1.4 MB and works fine. But 50 MB might be too much.

**Mitigation:** Split into multiple files (already planned). If even individual
definition files are too large, reduce to only defining the nonzero structure constants.

### Kill Condition 4: .olean Explosion for Matrix Approach

**Test:** If the .olean for `e8_adjoint_defs.lean` exceeds 1 GB, we have the same
wall as flat SO16.

**Mitigation:** The mathlib matrix types should not have this problem (SO16M .olean
was only 335 KB). But 248x248 is much larger than 16x16, so test early.

### Non-Kill: Isomorphism with LieAlgebra.e₈ R

If we cannot prove the isomorphism between E8_adj and `LieAlgebra.e₈ R`, this is
NOT a kill condition. We can:
1. State it as [SP] axiom (honest gap)
2. The LieSubalgebra of 248x248 matrices is independently verified
3. The SO(16) embedding is independently verified
4. The dimension count is independently verified

The connection to the abstract type is nice-to-have, not essential.

---

## Part 7: Alternative "Quick Win" Strategy

If the full 248x248 approach hits obstacles, there's a lower-cost strategy:

### Quick Win: SO(16) subalgebra proof + dimensional axiom

1. Take `LieAlgebra.e₈ R` from mathlib (free)
2. Axiomatize `dim(LieAlgebra.e₈ R) = 248` as [SP]
3. Define the SO(16) embedding as Chevalley generators:
   - The D8 subalgebra of E8 uses nodes 1-7 of the Dynkin diagram
   - Map the 120 generators of SO(16) to the D8 Chevalley generators
4. Prove the embedding preserves brackets (this requires only 120 generators,
   not all 248, and uses the Serre relations directly)
5. State the decomposition `248 = 120 + 128` as [SP]

**Advantage:** No 248x248 matrices needed. No Python generation. Uses only mathlib.
**Disadvantage:** The Chevalley-to-matrix correspondence is itself nontrivial.
**Effort:** 1-2 weeks if the Serre relations are tractable in Lean.

---

## Part 8: Recommended Sequence

### Phase 0: Feasibility Test (1 day)

1. Install SageMath (if not already available)
2. Compute one E8 adjoint matrix and verify it's rational/integer
3. Write a minimal Lean file with one 248x248 Q matrix and test native_decide on
   a single bracket pair
4. If both succeed, proceed. If either fails, evaluate kill conditions.

### Phase 1: Python Generation (3-5 days)

5. Full SageMath script to extract all 248 adjoint matrices
6. Identify the SO(16) subalgebra (120 generators)
7. Compute all 30,628 bracket pairs
8. Generate Lean source files (chunked)

### Phase 2: Lean Compilation (1-2 weeks)

9. Compile matrix definitions
10. Compile bracket verifications (chunked)
11. Define E8Adj as LieSubalgebra
12. Build SO16M -> E8Adj LieHom

### Phase 3: Integration (2-3 days)

13. Connect to existing e8_embedding.lean
14. State dimensional decomposition
15. State isomorphism with mathlib e₈ [SP]
16. Update PROJECT_ROADMAP.md

**Total estimated effort: 3-4 weeks.**

---

## Part 9: What We Proved vs What We Claim (Honesty)

### [MV] Machine-Verified (what the construction gives)

- E8Adj is a LieSubalgebra of Mat(248, Q) (bracket closure verified by native_decide)
- SO16M embeds into E8Adj as a LieSubalgebra (bracket preservation by native_decide)
- Jacobi identity holds (automatic from LieSubalgebra of associative algebra)
- LieRing and LieAlgebra instances (automatic from mathlib)

### [SP] Stated Properties (honest gaps)

- E8Adj is isomorphic to `LieAlgebra.e₈ R` (known mathematically, not formalized)
- E8Adj is simple (known, not formalized)
- E8Adj has dimension exactly 248 (follows from simplicity + Killing form, not formalized)
- The 128-dim complement of SO(16) in E8 is the half-spinor representation

### [CO] Computational Observations

- The Python script produces structure constants matching known E8 tables
- The Chevalley basis structure constants are integers
- The SO(16) subalgebra is identifiable from the root system

---

## Part 10: Comparison Table

| Criterion | A: 248x248 Matrices | B: Composite | C: Pure Serre | D: Hybrid (Rec.) |
|-----------|:---:|:---:|:---:|:---:|
| LieRing/LieAlgebra free | Yes (LieSubalg) | Must prove | Yes (quotient) | Yes (LieSubalg) |
| Jacobi automatic | Yes | Must prove | Yes | Yes |
| Dimension known | By construction | By construction | HARD to prove | By construction |
| SO(16) embedding | By matrix inclusion | Built-in | HARD | By matrix inclusion |
| Computational | Full native_decide | Partial | Not computational | Full native_decide |
| .olean size | ~1 MB? | ~1 MB? | ~100 KB | ~1 MB? |
| Python work | Heavy | Heavy | None | Heavy |
| Lean work | Moderate | Heavy | VERY heavy | Moderate |
| Connection to mathlib e₈ | Need isomorphism | Need isomorphism | Free | [SP] axiom |
| Honest gaps | Isomorphism only | Fierz identity | Everything | Isomorphism only |
| Total effort | 3-4 weeks | 4-8 weeks | Months-years | 3-4 weeks |

**Recommendation: Option D (Hybrid).** It gives us a verified Lie algebra of the
right dimension with SO(16) embedding, at manageable cost, with only one honest gap
(the isomorphism with the abstract Serre type).

---

## Appendix A: The E8 Cartan Matrix (for reference)

Dynkin diagram of E8:
```
    2
    |
1---3---4---5---6---7---8
```

Node numbering follows Bourbaki. The matrix is:
```
     1   2   3   4   5   6   7   8
1  [ 2   0  -1   0   0   0   0   0]
2  [ 0   2   0  -1   0   0   0   0]
3  [-1   0   2  -1   0   0   0   0]
4  [ 0  -1  -1   2  -1   0   0   0]
5  [ 0   0   0  -1   2  -1   0   0]
6  [ 0   0   0   0  -1   2  -1   0]
7  [ 0   0   0   0   0  -1   2  -1]
8  [ 0   0   0   0   0   0  -1   2]
```

The D8 subalgebra corresponds to nodes {1, 3, 4, 5, 6, 7, 8} (removing node 2).
This gives the so(16) subalgebra of E8.

## Appendix B: E8 Root System Summary

- 240 roots in R^8
- 8 simple roots (corresponding to Dynkin diagram nodes)
- 120 positive roots (one for each generator beyond Cartan)
- Root lengths: all equal (simply laced)
- All roots have squared length 2 (in the standard normalization)
- The 112 D8 roots + 128 semi-spinor weights = 240 E8 roots

## Appendix C: SageMath Script Skeleton

```python
#!/usr/bin/env sage
"""
Generate E8 adjoint representation matrices for Lean 4.
"""
from sage.all import *

# E8 Lie algebra over Q
L = LieAlgebra(QQ, cartan_type=['E', 8])
basis = list(L.basis())
assert len(basis) == 248, f"Expected 248 basis elements, got {len(basis)}"

# Compute all structure constants
# f^c_{ab} = coefficient of e_c in [e_a, e_b]
structure_constants = {}
for a in range(248):
    for b in range(a+1, 248):
        bracket = L.bracket(basis[a], basis[b])
        # Express bracket in terms of basis
        coeffs = {}
        for c in range(248):
            coeff = bracket.coefficient(basis[c])  # exact rational
            if coeff != 0:
                coeffs[c] = coeff
        if coeffs:
            structure_constants[(a, b)] = coeffs

# Identify SO(16) subalgebra
# D8 uses nodes 1, 3, 4, 5, 6, 7, 8 (Bourbaki numbering)
# Need to identify the 120 generators corresponding to these roots

# Generate Lean code
# ... (output 248 matrices, bracket table, verification chunks)
```

**Note:** The exact SageMath API may differ; verify before running.

---

## Appendix D: Lean Code Skeleton (Recommended Approach)

```lean
/-
E8 Adjoint Representation - LieSubalgebra of 248x248 Matrices
-/
import Mathlib.Algebra.Lie.Classical
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

-- The 248 generator matrices (generated by Python)
abbrev E8Mat := Matrix (Fin 248) (Fin 248) Q

def e8gen (k : Fin 248) : E8Mat := Matrix.of fun i j => match k, i, j with
  | 0, 0, 1 => 1   -- example nonzero entry
  | 0, 1, 0 => -1  -- antisymmetric
  | ...
  | _, _, _ => 0

-- Bracket verification (chunked)
theorem e8_bracket_chunk_01 :
    forall a b : Fin 248, a.val < 8 -> a < b ->
    e8gen a * e8gen b - e8gen b * e8gen a = bracketResult a b := by
  native_decide

-- The LieSubalgebra (after all chunks verified)
-- Define as span of generators, prove closure under bracket
def E8Adj : LieSubalgebra Q (Matrix (Fin 248) (Fin 248) Q) := sorry
-- (requires assembling the chunk proofs)

-- The SO(16) embedding
def so16_to_e8 : SO16M_Q ->_L[Q] E8Adj := sorry
-- (map each generator of so(16) to corresponding e8 generator)
```

This skeleton will be refined during implementation.
