# Schur's Lemma Formalization in Lean 4/Mathlib: Polymathic Synthesis

## Executive Summary

Mathlib already contains THREE layers of Schur's lemma -- for ring modules, for group
representations, and categorically -- but NONE for Lie algebra modules. The gap between
`LieModule.IsIrreducible` (which exists) and the needed "Killing form is the unique
Ad-invariant bilinear form on a simple Lie algebra" can be bridged via a direct route
through ring-module Schur without touching category theory at all. The eigenvalue
existence theorem over algebraically closed fields (`Module.End.exists_eigenvalue`) is
already in mathlib, but working over the reals requires complexification, which has
partial support. Confidence: the formalization is feasible within mathlib's existing
infrastructure, with 3-5 new lemmas constituting a plausible PR.

---

## 1. What Mathlib Actually Has (Source-Verified)

All findings below are from direct reading of `.lake/packages/mathlib/` source files
in the project, NOT from documentation or memory. Every claim cites the exact file.

### 1.1 Schur's Lemma for Ring Modules (COMPLETE)

**File**: `Mathlib/RingTheory/SimpleModule/Basic.lean`

```
class IsSimpleModule (R M) extends IsSimpleOrder (Submodule R M)
```

**Schur's Lemma (full form)**:
```lean
-- Injective half
theorem LinearMap.injective_or_eq_zero [IsSimpleModule R M] (f : M ->_l[R] N) :
    Function.Injective f | f = 0

-- Surjective half
theorem LinearMap.surjective_or_eq_zero [IsSimpleModule R N] (f : M ->_l[R] N) :
    Function.Surjective f | f = 0

-- Full Schur
theorem LinearMap.bijective_or_eq_zero [IsSimpleModule R M] [IsSimpleModule R N]
    (f : M ->_l[R] N) : Function.Bijective f | f = 0

-- Division ring structure on endomorphisms
noncomputable instance Module.End.instDivisionRing
    [DecidableEq (Module.End R M)] [IsSimpleModule R M] :
    DivisionRing (Module.End R M)
```

**Status**: COMPLETE. This is the classical algebraic Schur's lemma for modules over
any ring. The division ring instance on End(M) is the key structural consequence.

### 1.2 Schur's Lemma for Group Representations (COMPLETE)

**File**: `Mathlib/RepresentationTheory/Irreducible.lean`

```lean
abbrev Representation.IsIrreducible := IsSimpleOrder (Subrepresentation rho)

-- Reduces to ring-module Schur via:
theorem irreducible_iff_isSimpleModule_asModule :
    IsIrreducible rho <-> IsSimpleModule k[G] rho.asModule

-- Full Schur for intertwining maps:
theorem IsIrreducible.bijective_or_eq_zero [IsIrreducible rho] [IsIrreducible sigma]
    (f : IntertwiningMap rho sigma) : Bijective f | f = 0

-- Over algebraically closed fields:
theorem IsSimpleModule.algebraMap_end_bijective_of_isAlgClosed :
    Function.Bijective (algebraMap k (Module.End A V))
-- (from Mathlib/RepresentationTheory/AlgebraRepresentation/Basic.lean)
```

**Status**: COMPLETE. Uses the monoid algebra `k[G]` trick to reduce to `IsSimpleModule`.

### 1.3 Categorical Schur (PARTIAL)

**File**: `Mathlib/CategoryTheory/Simple.lean`

```lean
class Simple (X : C) : Prop where
  mono_isIso_iff_nonzero : forall {Y} (f : Y --> X) [Mono f], IsIso f <-> f != 0
```

This defines simple objects in any category with zero morphisms. Key results:
- `isIso_of_mono_of_nonzero`: nonzero mono to simple is iso
- `isIso_of_epi_of_nonzero`: nonzero epi from simple is iso (in abelian)
- `indecomposable_of_simple`: simple implies indecomposable

**Status**: This is the CATEGORICAL framework. It does NOT have a direct connection to
`LieModule.IsIrreducible` or `IsSimpleModule`. The TODO in SimpleModule/Basic.lean
explicitly says: "Unify with the work on Schur's Lemma in a category theory context."

### 1.4 Lie Algebra Infrastructure

#### 1.4.1 IsSimple for Lie Algebras

**File**: `Mathlib/Algebra/Lie/Semisimple/Defs.lean`

```lean
class LieAlgebra.IsSimple : Prop where
  eq_bot_or_eq_top : forall I : LieIdeal R L, I = bot | I = top
  non_abelian : not (IsLieAbelian L)
```

This is the definition of a simple Lie algebra: only trivial ideals, and non-abelian.

#### 1.4.2 Irreducible Lie Modules

**File**: `Mathlib/Algebra/Lie/Semisimple/Defs.lean`

```lean
abbrev LieModule.IsIrreducible : Prop :=
  IsSimpleOrder (LieSubmodule R L M)
```

This is the definition of an irreducible Lie module: the lattice of Lie submodules
has only bot and top. Note: this is `IsSimpleOrder`, NOT `IsSimpleModule`. These are
DIFFERENT typeclasses operating on DIFFERENT lattices.

**CRITICAL GAP**: `LieSubmodule R L M` != `Submodule R M`. A Lie submodule must be
closed under the Lie action, while a submodule need only be closed under the ring
action. So `LieModule.IsIrreducible` does NOT imply `IsSimpleModule R M` in general --
the Lie submodule lattice is coarser than the submodule lattice.

#### 1.4.3 Lie Module Morphisms

**File**: `Mathlib/Algebra/Lie/Basic.lean` (line 678)

```lean
structure LieModuleHom extends M ->_l[R] N where
  map_lie' : forall {x : L} {m : M}, toFun (lie x m) = lie x (toFun m)

notation M " ->_l[" R "," L "] " N => LieModuleHom R L M N
```

This is the morphism type for Lie modules. A `LieModuleHom` is a linear map that
commutes with the Lie action.

#### 1.4.4 The Killing Form

**File**: `Mathlib/Algebra/Lie/TraceForm.lean`

```lean
noncomputable def LieModule.traceForm : LinearMap.BilinForm R L :=
  ((LinearMap.mul _ _).compl12 phi.toLinearMap phi.toLinearMap).compr2 (trace R M)

-- The Killing form is the trace form for the adjoint representation:
noncomputable def killingForm : LinearMap.BilinForm R L := traceForm R L L
```

Key properties proved:
- `traceForm_isSymm`: the trace form is symmetric
- `traceForm_apply_lie_apply`: Lie-invariance: B([x,y], z) = B(x, [y,z])
- `traceForm_lieInvariant`: the trace form is Lie-invariant

**File**: `Mathlib/Algebra/Lie/Killing.lean`

```lean
class LieAlgebra.IsKilling : Prop where
  killingCompl_top_eq_bot : LieIdeal.killingCompl R L top = bot

-- Key consequences:
lemma ker_killingForm_eq_bot : LinearMap.ker (killingForm R L) = bot
lemma killingForm_nondegenerate : (killingForm R L).Nondegenerate
instance instSemisimple [IsKilling K L] [Module.Finite K L] : IsSemisimple K L
lemma LieIdeal.isCompl_killingCompl [IsKilling K L] (I : LieIdeal K L) :
    IsCompl I I.killingCompl
```

#### 1.4.5 The Adjoint Representation

**File**: `Mathlib/Algebra/Lie/Derivation/AdjointAction.lean`

```lean
def ad : L ->_l[R] LieDerivation R L L
```

**File**: `Mathlib/Algebra/Lie/OfAssociative.lean` (via `LieModule.toEnd`)

The adjoint action `toEnd R L L` gives L the structure of a Lie module over itself.

#### 1.4.6 Invariant Bilinear Forms

**File**: `Mathlib/Algebra/Lie/InvariantForm.lean`

```lean
def LinearMap.BilinForm.lieInvariant : Prop :=
  forall (x : L) (y z : M), Phi (lie x y) z = -Phi y (lie x z)

-- Orthogonal complement as a Lie submodule:
def InvariantForm.orthogonal (hPhi_inv : Phi.lieInvariant L)
    (N : LieSubmodule R L M) : LieSubmodule R L M

-- Main theorem:
theorem isSemisimple_of_nondegenerate : IsSemisimple K L
```

#### 1.4.7 Root Systems and IsSimple

**File**: `Mathlib/Algebra/Lie/Weights/IsSimple.lean`

```lean
instance [IsSimple K L] : (rootSystem H).IsIrreducible
```

This file proves that the root system of a simple Lie algebra is irreducible.
Author: Janos Wolosz (2025). This is RECENT work.

### 1.5 Eigenvalue Existence

**File**: `Mathlib/LinearAlgebra/Eigenspace/Triangularizable.lean`

```lean
-- THE KEY THEOREM:
theorem Module.End.exists_eigenvalue [IsAlgClosed K] [FiniteDimensional K V]
    [Nontrivial V] (f : End K V) :
    exists c : K, f.HasEigenvalue c

-- Generalized eigenspaces span:
theorem iSup_maxGenEigenspace_eq_top [IsAlgClosed K] [FiniteDimensional K V]
    (f : End K V) :
    iSup (mu : K), f.maxGenEigenspace mu = top
```

**Status**: COMPLETE over algebraically closed fields. This is the eigenvalue
existence needed for Route A of Schur's lemma (the "every endomorphism is scalar"
direction).

---

## 2. Gap Analysis

### Gap 1: LieModuleHom Schur's Lemma (CRITICAL)

**What's missing**: There is no theorem stating that a `LieModuleHom` between
irreducible Lie modules is either zero or an isomorphism.

**Why it's hard**: `LieModule.IsIrreducible` is defined as
`IsSimpleOrder (LieSubmodule R L M)`, but Schur's lemma for ring modules uses
`IsSimpleModule R M` which is `IsSimpleOrder (Submodule R M)`. The kernel and image
of a `LieModuleHom` are Lie submodules (not just submodules), so the proof SHOULD
work by the same logic:
- ker f is a Lie submodule of M (source is irreducible) => ker f = bot or top
- im f is a Lie submodule of N (target is irreducible) => im f = bot or top
- If f != 0 then ker f != top so ker f = bot (injective), and im f != bot so im f = top (surjective)

**Required new code** (estimated 20-30 lines):
```lean
theorem LieModuleHom.injective_or_eq_zero
    [LieModule.IsIrreducible R L M] (f : M ->_l[R,L] N) :
    Function.Injective f | f = 0

theorem LieModuleHom.bijective_or_eq_zero
    [LieModule.IsIrreducible R L M] [LieModule.IsIrreducible R L N]
    (f : M ->_l[R,L] N) :
    Function.Bijective f | f = 0
```

**Risk**: LOW. The kernel/image of a LieModuleHom are already known to be
LieSubmodules (this is implicit in the `LieSubmodule` API). The proof mirrors the
ring-module version exactly.

### Gap 2: Adjoint Representation is Irreducible (MEDIUM)

**What's missing**: A theorem that for a simple Lie algebra L, the adjoint
representation (L acting on itself) is irreducible as a Lie module.

**What exists**: `LieAlgebra.IsSimple` says ideals are trivial. Ideals ARE the Lie
submodules of the adjoint representation. So `IsSimple` literally IS the statement
that the adjoint representation is irreducible.

**Formally**: We need
```lean
instance [LieAlgebra.IsSimple R L] : LieModule.IsIrreducible R L L
```

**Risk**: ZERO. CONFIRMED: `LieIdeal` is defined as:
```lean
abbrev LieIdeal := LieSubmodule R L L
```
(Mathlib/Algebra/Lie/Ideal.lean, line 46). They are DEFINITIONALLY EQUAL.
So `IsSimple` (ideals are trivial) IS `IsIrreducible` (Lie submodules of L are
trivial). The instance is literally `inferInstance` or `id`.

### Gap 3: Every Lie Module Endomorphism is Scalar (HARD)

**What's missing**: For an irreducible Lie module M over an algebraically closed
field, every endomorphism in `End_{Lie}(M) = (M ->_l[R,L] M)` is scalar.

**Route A (via eigenvalues)**:
1. A Lie module endomorphism f is in particular a linear map.
2. Over an algebraically closed field, f has an eigenvalue mu
   (`Module.End.exists_eigenvalue` -- EXISTS in mathlib).
3. f - mu*id is a Lie module endomorphism (since scalar maps commute with everything).
4. f - mu*id has nontrivial kernel (the eigenspace).
5. By Gap 1 (Lie Schur), f - mu*id = 0, so f = mu*id.

**Risk**: MEDIUM. Step 2 requires that `f` (viewed as a linear endomorphism) is
over an algebraically closed field. Over R (the reals), this fails. We would need
to complexify.

**Route B (via ring-module Schur)**:
The representation `M ->_l[R,L] M` should reduce to `Module.End (U L) M` where
`U L` is the universal enveloping algebra. Then `IsSimpleModule (U L) M` gives
Schur via the ring-module path.

**Risk**: HIGH. The universal enveloping algebra `U L` exists in mathlib
(`UniversalEnvelopingAlgebra`), but the connection between `LieModule` and
`Module (UniversalEnvelopingAlgebra R L)` may not be fully developed.

### Gap 4: Killing Form Uniqueness on Simple Lie Algebras (THE GOAL)

**What's missing**: The theorem that the Killing form is the unique (up to scale)
Ad-invariant bilinear form on a simple Lie algebra.

**Proof path** (using Gaps 1-3):
1. Let B be any Ad-invariant bilinear form on simple L.
2. The map phi_B : L -> L* defined by phi_B(x) = B(x, -) is a Lie module morphism
   (from the adjoint module to its dual).
3. The Killing form kappa gives phi_kappa : L -> L*.
4. phi_kappa is nondegenerate (proved: `killingForm_nondegenerate`).
5. phi_kappa^{-1} . phi_B : L -> L is a Lie module endomorphism.
6. By Gap 3, this endomorphism is scalar: phi_kappa^{-1} . phi_B = c * id.
7. Therefore B = c * kappa.

**Alternative path** (avoiding eigenvalue problem):
1. For a simple Lie algebra, any invariant bilinear form B has its kernel as an ideal.
2. By simplicity, ker B = 0 or ker B = L.
3. If ker B = L, then B = 0 (B = 0 * kappa).
4. If ker B = 0, then B is nondegenerate.
5. The map kappa^{-1} . B : L -> L is an endomorphism of the adjoint module.
6. Need Schur to conclude it's scalar.

**Risk**: MEDIUM-HIGH. The full path requires Gap 3. The alternative path still
requires the "every endomorphism is scalar" result.

### Gap 5: Real vs Algebraically Closed Field (PRACTICAL)

**The problem**: Our project works over R (real numbers). Schur's lemma in its
strongest form (every endomorphism is scalar) requires algebraically closed fields.
Over R, endomorphisms might not be scalar -- they could be "rotation-like" maps.

**For simple Lie algebras specifically**: The result "Killing form is unique up to
scale" holds over R for simple Lie algebras. The proof uses:
- The complexification L_C = L tensor C is simple (or splits into two simple ideals).
- Apply Schur over C.
- Restrict back to R.

**Mathlib status**: Complexification exists (`TensorProduct.Algebra`), but the specific
Lie algebra complexification API may need work.

**Pragmatic solution**: Work with `[IsAlgClosed K]` throughout and note that the real
case follows by complexification (which can be axiomatized for now).

---

## 3. What Other Proof Assistants Have Done

### 3.1 Coq/Rocq (mathcomp-analysis, math-comp)

Based on my knowledge of the formalization landscape:

- **mathcomp** has extensive finite group representation theory, including Schur's
  lemma for finite groups (Maschke's theorem + character theory). This is in the
  `mathcomp-character` package.
- **Lie algebra Schur**: NOT formalized in Coq/mathcomp as of my knowledge cutoff.
  The mathcomp-analysis project focuses on analysis, not Lie theory.
- **Approach**: mathcomp uses the ssreflect proof style with fintype-based
  representations. Schur's lemma is stated for `mx_irreducible` (irreducible matrix
  representations) of finite groups.

### 3.2 Isabelle/HOL

- **Schur's lemma for groups**: Exists in the Isabelle AFP (Archive of Formal Proofs),
  in the "Group_Representations" entry.
- **Lie algebra Schur**: NOT formalized in Isabelle.
- **Approach**: Uses HOL-Algebra's module theory. The proof is more concrete
  (matrix-based) than mathlib's abstract approach.

### 3.3 Agda

- **HoTT-Agda** has some basic algebra but no representation theory.
- **Schur's lemma**: NOT formalized in Agda.

### 3.4 Summary

NO proof assistant has formalized Schur's lemma specifically for Lie algebra
representations. The closest is mathlib's own ring-module Schur, which is the
foundation our formalization would build on.

**Confidence**: PROBABLE (based on knowledge cutoff, not web search).

---

## 4. Recommended Approach

### Phase 1: LieModuleHom Schur (Estimated: 1-2 hours)

Prove the analogues of `LinearMap.injective_or_eq_zero` and
`LinearMap.bijective_or_eq_zero` for `LieModuleHom`:

```lean
-- In a new file: Mathlib/Algebra/Lie/Module/Schur.lean

theorem LieModuleHom.injective_or_eq_zero
    [LieModule.IsIrreducible R L M] (f : M ->_l[R,L] N) :
    Function.Injective f | f = 0 := by
  -- ker f is a LieSubmodule of M
  -- By irreducibility, ker f = bot or ker f = top
  -- ker f = bot => injective; ker f = top => f = 0
  sorry

theorem LieModuleHom.bijective_or_eq_zero
    [LieModule.IsIrreducible R L M] [LieModule.IsIrreducible R L N]
    (f : M ->_l[R,L] N) :
    Function.Bijective f | f = 0 := by
  sorry
```

**Prerequisites**: CONFIRMED IN MATHLIB (Mathlib/Algebra/Lie/Submodule.lean):
- `LieModuleHom.ker : LieSubmodule R L M` (line 873)
- `LieModuleHom.range : LieSubmodule R L N` (line 904)
- `LieModuleHom.ker_eq_bot : f.ker = bot <-> Function.Injective f` (line 880)
- `LieModuleHom.range_eq_top : f.range = top <-> Function.Surjective f` (line 922)
All four API pieces exist. The proof is LITERALLY four lines.

### Phase 2: IsSimple implies Irreducible Adjoint (Estimated: 5 min)

```lean
instance LieAlgebra.IsSimple.adjoint_isIrreducible
    [LieAlgebra.IsSimple R L] : LieModule.IsIrreducible R L L :=
  -- LieIdeal R L = LieSubmodule R L L (DEFINITIONALLY, via abbrev)
  -- IsSimple says all LieIdeal R L are bot or top
  -- IsIrreducible says all LieSubmodule R L L are bot or top
  -- These are the SAME statement!
  { exists_pair_ne := by exact IsSimple.non_abelian ... -- nontrivial
    eq_bot_or_eq_top := IsSimple.eq_bot_or_eq_top }
```

CONFIRMED: `abbrev LieIdeal := LieSubmodule R L L` (line 46 of Ideal.lean).
This is DEFINITIONALLY the same. The only subtlety is the `Nontrivial` instance
(which follows from `non_abelian`).

### Phase 3: Endomorphisms are Scalar (Estimated: 2-4 hours)

Over an algebraically closed field:
```lean
theorem LieModule.IsIrreducible.endomorphism_eq_smul_id
    [IsAlgClosed K] [FiniteDimensional K M]
    [LieModule.IsIrreducible K L M] (f : M ->_l[K,L] M) :
    exists c : K, f.toLinearMap = c . LinearMap.id := by
  -- f has an eigenvalue mu (exists_eigenvalue)
  -- f - mu * id is a LieModuleHom with nontrivial kernel
  -- By Schur (Phase 1), f - mu * id = 0
  sorry
```

### Phase 4: Killing Form Uniqueness (Estimated: 2-3 hours)

```lean
theorem LieAlgebra.IsSimple.killingForm_unique
    [IsAlgClosed K] [FiniteDimensional K L] [LieAlgebra.IsSimple K L]
    (B : LinearMap.BilinForm K L) (hB : B.lieInvariant L) :
    exists c : K, B = c . killingForm K L := by
  sorry
```

### Phase 5: Axiomatize for Real Case

For our project's immediate needs:
```lean
-- For the lagrangian_uniqueness.lean upgrade:
axiom killing_form_unique_real (L : Type*) [LieRing L] [LieAlgebra R L]
    [LieAlgebra.IsSimple R L] [FiniteDimensional R L]
    (B : LinearMap.BilinForm R L) (hB : B.lieInvariant L) :
    exists c : R, B = c . killingForm R L
```

Tag as [SP] with a note that the full proof is available over algebraically closed
fields and extends to R by complexification.

---

## 5. Risk Assessment

| Component | Risk | Reason |
|-----------|------|--------|
| LieModuleHom Schur | TRIVIAL | ker/range are LieSubmodules (confirmed), 4-line proof |
| IsSimple => Irreducible | TRIVIAL | LieIdeal IS LieSubmodule R L L (abbrev, confirmed) |
| Endomorphism scalar (AlgClosed) | MEDIUM | Needs eigenvalue + careful type coercion |
| Endomorphism scalar (Real) | HIGH | Requires complexification infrastructure |
| Killing uniqueness (AlgClosed) | MEDIUM | Needs dual module as Lie module |
| Killing uniqueness (Real) | HIGH | Depends on complexification |
| Mathlib PR acceptance | MEDIUM | Phase 1-2 very likely; Phase 3-4 need discussion |

---

## 6. The Bridge Problem

**Question**: How to connect `LieModule` to `CategoryTheory.Simple`?

**Answer**: You do NOT need to. The categorical Schur is a distraction for this
application. The direct path is:

```
LieModule.IsIrreducible (Lie submodule lattice)
    |
    v  (ker/im are Lie submodules)
LieModuleHom.bijective_or_eq_zero
    |
    v  (eigenvalue existence over AlgClosed)
Endomorphism is scalar
    |
    v  (applied to kappa^{-1} . B)
Killing form uniqueness
    |
    v  (applied to Tr(F^2))
Yang-Mills Lagrangian uniqueness
```

The categorical bridge WOULD be needed if you wanted to use the categorical Schur
(`CategoryTheory.Simple`) instead of reproving Schur for Lie modules. This would
require:
1. Defining a category of Lie modules (objects: Lie modules, morphisms: LieModuleHom).
2. Showing that `LieModule.IsIrreducible` corresponds to `CategoryTheory.Simple`.
3. Using the categorical Schur.

This is MUCH more work than the direct approach and provides no benefit for our
specific application.

---

## 7. Potential Mathlib Contribution

**What would be welcome**: Phase 1 (LieModuleHom Schur) is a natural addition to
mathlib. It fills an obvious gap and follows the established pattern.

**Style guidelines** (from reading the codebase):
- File would go in `Mathlib/Algebra/Lie/Module/Schur.lean` or similar
- Use the existing `LieModuleHom` notation `M ->_l[R,L] N`
- Follow the injective/surjective/bijective pattern from `SimpleModule/Basic.lean`
- Attribution: this would be new to mathlib

**What might need discussion**: Phase 3-4 (endomorphisms are scalar, Killing
uniqueness) depend on design choices about how Lie algebra representation theory
should be developed in mathlib. The universal enveloping algebra route vs the
direct route is a design decision the mathlib community should make.

---

## 8. Anomaly Register

| Anomaly | Why Anomalous | Potential Significance |
|---------|---------------|----------------------|
| `LieModule.IsIrreducible` uses `IsSimpleOrder` not `IsSimpleModule` | Different lattices! Lie vs ring submodules | Must prove Schur directly, cannot reuse ring-module version |
| No `IsSimple` for Lie modules in the `Simple.lean` sense | Categorical and algebraic notions not unified | The TODO in SimpleModule says to unify -- this is known debt |
| `IsKilling` is NOT standard terminology | Mathlib invented this name | Shows mathlib is still actively developing this area |
| `IsSimple.lean` in Weights directory is from 2025 (Janos Wolosz) | Very recent addition | Root system theory is actively being formalized |
| The RepresentationTheory directory has NO Lie algebra content | All group representations | Lie representation theory is the frontier |

---

## 9. Key Mathlib API Signatures (Reference)

```lean
-- Killing form definition
noncomputable def killingForm (R L : Type*) [...] : LinearMap.BilinForm R L

-- Killing form properties
lemma killingForm_nondegenerate [IsKilling R L] : (killingForm R L).Nondegenerate
lemma traceForm_apply_lie_apply : traceForm R L M (lie x y) z = traceForm R L M x (lie y z)
lemma traceForm_lieInvariant : (traceForm R L M).lieInvariant L

-- Simple Lie algebra
class LieAlgebra.IsSimple : Prop where
  eq_bot_or_eq_top : forall I : LieIdeal R L, I = bot | I = top
  non_abelian : not (IsLieAbelian L)

-- Irreducible Lie module
abbrev LieModule.IsIrreducible := IsSimpleOrder (LieSubmodule R L M)

-- Lie module morphism
structure LieModuleHom extends M ->_l[R] N where
  map_lie' : forall {x : L} {m : M}, toFun (lie x m) = lie x (toFun m)

-- Eigenvalue existence
theorem Module.End.exists_eigenvalue [IsAlgClosed K] [FiniteDimensional K V]
    [Nontrivial V] (f : End K V) : exists c : K, f.HasEigenvalue c

-- Ring-module Schur
theorem LinearMap.bijective_or_eq_zero [IsSimpleModule R M] [IsSimpleModule R N]
    (f : M ->_l[R] N) : Function.Bijective f | f = 0

-- Invariant form
def LinearMap.BilinForm.lieInvariant (L) : Prop :=
  forall (x : L) (y z : M), Phi (lie x y) z = -Phi y (lie x z)
```

---

## 10. Recommended Next Steps

### Immediate (for this project)
1. **Implement Phase 1-2** in a new file `src/lean_proofs/dynamics/schur_lemma.lean`
2. **Axiomatize Killing uniqueness** with honest [SP] tag (as currently done)
3. **Upgrade `lagrangian_uniqueness.lean`** to import Schur results

### Medium-term (mathlib contribution)
4. **Open a mathlib PR** for LieModuleHom Schur (Phase 1-2)
5. **Discuss on Zulip** the design of Lie algebra representation theory

### Long-term
6. **Formalize complexification** for Lie algebras
7. **Full Killing uniqueness** over arbitrary fields of characteristic zero
8. **Category of Lie modules** to unify with categorical Schur

---

## Research Notebook Location
Full phase outputs: `research/schur-lemma-formalization/`

## Phase Completion Record
- Phase 1 (Ingestion): Completed via direct mathlib source reading
- Phase 2 (Deconstruction): Integrated into synthesis
- Phase 3-6: Compressed into synthesis (COMPREHENSIVE mode)
- Phase 7 (Synthesis): This document

## Confidence Calibration

| Claim | Confidence | Basis |
|-------|------------|-------|
| Ring-module Schur exists in mathlib | ESTABLISHED | Read source directly |
| Lie-module Schur does NOT exist | ESTABLISHED | Grep of entire mathlib tree |
| LieModuleHom Schur is straightforward | PROBABLE | Structural similarity to ring case |
| Eigenvalue existence over AlgClosed exists | ESTABLISHED | Read source directly |
| Real case needs complexification | ESTABLISHED | Standard mathematics |
| No other proof assistant has Lie Schur | PROBABLE | Based on knowledge, not web search |
| Mathlib PR would be welcome | PLAUSIBLE | Fills obvious gap, follows patterns |
