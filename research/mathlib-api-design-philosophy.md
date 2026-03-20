# Mathlib API Design Philosophy & Style Guide

## Research Summary

Deep research into mathlib's generality requirements, API design patterns, tactic
conventions, documentation standards, and common idioms. Sources: official contributor
docs, actual mathlib source files (`Algebra.Lie.Basic`, `Algebra.Group.Basic`,
`Algebra.Ring.Basic`, `Analysis.InnerProductSpace.Basic`, `Topology.Basic`,
`CategoryTheory.Category.Basic`, `LinearAlgebra.Eigenspace.Basic`), Lean community
blog posts, and naming/style guides.

---

## 1. Generality Requirements

### The Core Principle

Mathlib's documentation states explicitly:

> "Topics are listed in the greatest generality we currently have in mathlib."

This is the defining design philosophy. Every theorem should be stated at the
**weakest sufficient typeclass assumption**. If a result holds for `CommRing R`,
do not state it for `Field K`. If it holds for `Semiring`, do not assume `Ring`.

### When to Use `CommRing R` vs `Field K` vs `ℝ`

**The hierarchy in practice** (from most to least general):

```
Semiring → Ring → CommRing → IsDomain → Field → ℝ / ℂ
```

Rules observed across mathlib:

1. **State at the weakest assumption where the proof works.** If `mul_comm` is
   not needed, use `Ring` not `CommRing`. If division is not needed, use
   `CommRing` not `Field`.

2. **Eigenvalue theory** (`LinearAlgebra.Eigenspace.Basic`): Core definitions
   like `genEigenspace` work over `CommRing R`. Results requiring invertibility
   (spectrum membership, finite-dimensional decomposition) use `Field K` in a
   separate section.

3. **Inner product spaces** (`Analysis.InnerProductSpace.Basic`): Uses `RCLike 𝕜`
   (a typeclass capturing "ℝ-like or ℂ-like") for maximum generality, then
   provides `_real` variants for convenience.

4. **Concrete types (ℝ, ℂ, ℤ)**: Only when the result is intrinsically about
   that type. Never as the primary statement when a general version exists.

5. **Pattern**: General theorem first, then specialized convenience lemmas:
   ```lean
   theorem norm_add_sq [RCLike 𝕜] ...      -- general
   theorem norm_add_sq_real ...              -- convenience for ℝ
   ```

### Universe Polymorphism

**How it works**: Lean 4 types live in universes `Type u`, `Type v`, etc.
Mathlib uses universe polymorphism to ensure results are not trapped at a
single universe level.

**Declaration pattern**:
```lean
universe u v w w₁ w₂

variable {R : Type u} {L : Type v} {M : Type w}
```

**When it is required**:

1. **Always use `Type*`** for simple cases — Lean infers the universe:
   ```lean
   variable {R S : Type*}
   ```

2. **Explicit universe variables** when types must relate across different
   universes (category theory is the canonical example):
   ```lean
   universe v u
   variable {C : Type u} [Category.{v} C]
   ```
   Category theory decouples object universe (`u`) from morphism universe (`v`).
   Convention: list morphism universe first so `u` can be inferred.

3. **The `@[univ_out_params]` attribute** prevents Lean from caching universe
   variables incorrectly — used in `Category` to maintain the object/morphism
   universe distinction.

4. **Rule of thumb**: Use `Type*` unless you have a reason to name universes
   explicitly. Name them when multiple types must coexist at potentially
   different universe levels (e.g., `R : Type u`, `M : Type v` for a module).

### Variable Naming Conventions (Universes and Types)

```
u, v, w        → universes
α, β, γ        → generic types
a, b, c        → propositions
x, y, z        → elements of a generic type
h, h₁          → hypotheses
p, q, r        → predicates and relations
s, t           → lists and sets
m, n, k        → natural numbers
i, j, k        → integers
G              → groups
R              → rings
K, 𝕜           → fields
E              → vector spaces
```

---

## 2. API Design Patterns

### File Organization

Every mathlib file follows this structure:

```lean
/-
Copyright (c) YYYY Author Name. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Author1, Author2
-/
import Mathlib.Foo.Bar
import Mathlib.Baz.Qux

/-!
# Title

Summary of file contents.

## Main definitions

* `Foo` : description
* `Bar` : description

## Main statements

* `foo_bar` : description

## Notation

* `f →ₗ⁅R⁆ g` : Lie algebra morphism

## Implementation notes

Design decisions explained here.

## References

* [Author, *Title*][citationKey]

## Tags

keyword1, keyword2
-/
```

**Key rules**:
- Copyright header uses `/-` (not `/-!`)
- Authors listed with commas, no "and", use "Authors:" (plural) even for one
- Module docstring uses `/-!` delimiters
- Imports immediately follow copyright, no blank lines
- All sections of the docstring are optional except title, but notation and
  implementation notes should be included when relevant

### Transparency and API Boundaries

Three levels of definition transparency:

1. **`abbrev`** (reducible): Always unfolded. Use for true abbreviations.
2. **`def`** (semireducible, default): Not unfolded by `rw`/`simp` unless
   explicitly told. Standard choice.
3. **`irreducible_def`**: Never unfolded. Use only when profiling shows a
   performance need. Prefer structure wrappers instead.

**Sealed API pattern**: When you want a type to be opaque:
```lean
-- Prefer this:
structure MyType where
  val : UnderlyingType

-- Over this:
irreducible_def myDef : ... := ...
```

### Section and Variable Patterns

**Progressive strengthening** — organize from weaker to stronger assumptions:
```lean
section Semigroup
variable [Semigroup α]
-- lemmas needing only associativity

section MulOneClass
variable [MulOneClass M]
-- lemmas needing identity element

section Group
variable [Group G]
-- lemmas needing inverses
```

**Variable declarations are per-section**:
```lean
section
variable {R : Type*} [CommRing R] [LieRing L] [LieAlgebra R L]
variable [AddCommGroup M] [Module R M] [LieRingModule L M]
-- all lemmas in this section inherit these assumptions
end
```

**Namespaces do NOT indent content**:
```lean
namespace MyAlgebra

def foo := ...    -- flush left, not indented

end MyAlgebra
```

### Normal Forms

Mathlib settles on one canonical form and provides simp lemmas to normalize:

- **Nonemptiness**: `s.Nonempty` (not `s ≠ ∅`)
- **Bottom elements**: Assumptions use `x ≠ ⊥`; conclusions use `⊥ < x`
- **Set membership**: `a ∈ s` (not coerced forms)
- **Natural positivity**: `0 < n` (not `n ≥ 1`)

---

## 3. Lean 4 Tactic Style Preferences

### `simp` vs `exact` vs `rfl`

- **`rfl`**: When the goal is definitionally equal. Simplest and fastest.
- **`exact`**: When you know the exact proof term. Preferred for clarity.
- **`simp`**: For normalization and simplification. Rules:
  - Terminal `simp` (closing a goal): leave unsqueezed — do NOT use `simp only`
  - Non-terminal `simp` (mid-proof): use `simp only [lemma1, lemma2, ...]`
    to prevent breakage when new simp lemmas are added
  - `simp` should simplify toward normal forms, not grow expressions

### Term-Mode vs Tactic-Mode

**Mixed freely**. Mathlib has no strong preference — use whichever is clearer:

```lean
-- Term mode for simple proofs
theorem foo : P := bar.trans baz

-- Tactic mode for complex proofs
theorem foo : P := by
  apply bar
  exact baz
```

### Tactic Block Structure

**Indentation**:
```lean
theorem foo : P := by    -- `by` at end of line, never standalone
  tactic1                 -- 2-space indent
  tactic2
```

**Focusing with `·`**:
```lean
theorem foo : P ∧ Q := by
  constructor
  · exact bar     -- dot is NOT indented further
  · exact baz
```

**Semicolons** for short related sequences:
```lean
-- Acceptable for short proofs
theorem foo : P := by split_ifs <;> rfl
```

**One tactic per line** in general. Short proofs can be single-line:
```lean
theorem foo : P := by simp [bar, baz]
```

### When to Use Specific Tactics

**`omega`**: Linear arithmetic over `Nat` and `Int`. Use for goals that are
systems of linear inequalities/equalities over integers. Handles `<`, `≤`,
`+`, `-`, `*` (by constants), `%`, `/` over `Nat`/`Int`. Does NOT handle
multiplication of variables, real arithmetic, or non-linear problems.

**`decide`**: For decidable propositions on finite types. Computes the answer
by exhaustive evaluation. Use for `Fin n` membership, boolean expressions,
small finite checks. Warning: exponential blowup for large types.

**`norm_num`**: Evaluates concrete numerical expressions. Use for goals like
`100 + 200 = 300` or `7 ∣ 49`. Works over `Nat`, `Int`, `Rat`, and numeric
coercions. Does NOT handle symbolic variables.

**`ring`**: Ring equalities with variables. Normalizes polynomial expressions.

**`linarith`**: Linear arithmetic over ordered fields/rings. More general than
`omega` (works over `ℝ`, `ℚ`, etc.) but cannot handle modular arithmetic.

**`field_simp`**: Clears denominators in field expressions. Often followed
by `ring`.

**`ext`**: Applies extensionality lemmas. Use when two objects are equal
iff their components/applications agree.

**`aesop`**: Automated reasoning. Searches for proofs using registered lemmas
and tactics. Good for typeclass-style goals.

---

## 4. Documentation Standards

### Module Docstrings

**Required sections**:
1. Title (first-level `#` header) — **mandatory**
2. Summary — **mandatory**
3. Main definitions — optional if covered in summary
4. Main statements — optional if covered in summary
5. Notation — **required** if any notation is introduced
6. Implementation notes — include for non-obvious design decisions
7. References — cite with `[Author, *Title*][citationKey]`; add entries
   to `docs/references.bib`
8. Tags — keywords for search discovery

### Declaration Docstrings

- **Every `def` and major `theorem`**: docstring required (linter-enforced)
- **Lemmas**: encouraged, especially those with mathematical content
- **Format**: `/-- ... -/` above the declaration, subsequent lines NOT indented
- **Complete sentences** ending with periods
- **Named theorems** in bold: `/-- The **Cauchy-Schwarz inequality**. -/`
- **May "lie slightly"** about implementation to convey mathematical meaning
- **Code references**: backtick-enclosed, fully qualified for auto-linking:
  `` `Finset.card_pos` ``
- **Math notation**: inline `$ ... $`, display `$$ ... $$`

### Section Headers

Use `/-! ... -/` with `###` for section titles within files:
```lean
/-! ### Morphisms -/
```

### Linting

```lean
#lint only docBlame      -- check missing docstrings on defs
#lint only docBlameThm   -- also check theorems/lemmas
#lint                     -- all default linters
```

---

## 5. Common Mathlib Idioms

### `instance` Declarations

**Priority control**:
```lean
instance (priority := 100) DivisionMonoid.toDivInvOneMonoid : ... := ...
```
Lower priority = tried later. Default is 1000. Use lower priority for
instances that should yield to more specific ones.

**Scoped instances**:
```lean
scoped[Subsingleton] attribute [instance] Subsingleton.to_noZeroDivisors
```
Active only when the namespace is opened.

**Instance naming**: Use qualified names to prevent conflicts:
```lean
instance Module.End.instLieRingModule : LieRingModule ...
```

**Diamond avoidance**: Sometimes use `abbrev` instead of `instance`:
```lean
-- "this cannot be a global instance because it would create a diamond when M = A"
abbrev LieRingModule.ofAssociativeModule : LieRingModule A M where ...
attribute [local instance] LieRingModule.ofAssociativeModule
```

### `@[ext]` Lemmas

**Purpose**: Enable the `ext` tactic to decompose equality goals.

**Pattern**: One `ext` lemma per type showing equality follows from
component equality:
```lean
@[ext]
theorem TopologicalSpace.ext :
    (∀ s, IsOpen₁ s ↔ IsOpen₂ s) → t₁ = t₂ := ...

-- For structures, the @[ext] attribute on the structure auto-generates this:
@[ext]
structure SU5C where
  h1 : ℝ
  ...
```

**Companion**: `ext_iff` provides the biconditional version.

### `@[simp]` Lemmas

**Good simp lemmas**:
- RHS simpler than LHS
- Unfold definitions to canonical forms
- Normalize equivalent expressions to one form
- Accompany every new definition

**Bad simp lemmas**:
- LHS simpler than RHS (causes loops)
- Non-terminating rewrite chains
- Overly specialized (won't fire often)

**Common pattern** — projection lemmas for new types:
```lean
@[simp] theorem myType_val (x : MyType) : x.val = ... := rfl
```

**Combined attributes**:
```lean
@[simp, norm_cast] lemma coe_mulLeft (r : R) : ...
```

**`@[simps]`** on definitions auto-generates projection simp lemmas:
```lean
@[simps]
noncomputable def quotKerEquivRange : ... := ...
```

### `theorem` vs `lemma` Conventions

Mathlib's style guide does **not** distinguish between `theorem` and `lemma`.
They are interchangeable in Lean 4. In practice:
- Both are used freely throughout mathlib
- **`lemma`** is slightly more common for routine results
- **`theorem`** is sometimes reserved for named results or main results of a file
- There is no enforced convention — use whichever reads better

### `noncomputable` Usage

Required when a definition uses the axiom of choice or other non-constructive
principles. Common cases:

```lean
-- Classical logic (excluded middle, choice)
noncomputable def quotKerEquivRange : (L ⧸ f.ker) ≃ₗ⁅R⁆ f.range := ...

-- Real number operations that require Cauchy completeness
noncomputable instance : Field ℝ := ...
```

**When to use**:
- Lean will tell you — if you omit it and the definition is non-constructive,
  you get an error
- Mark the specific definition, not the entire file (though
  `noncomputable section` exists for files that are entirely non-constructive)
- In mathlib, many algebraic constructions over ℝ require it

### `section` and `variable` Patterns

**Sections scope variables and instances**:
```lean
section Ring
variable [Ring R]

theorem foo : ... := ...    -- has access to [Ring R]

end Ring
-- [Ring R] no longer in scope
```

**Lean 4 auto-inclusion**: Variables declared with `variable` are only
included in declarations that actually use them. This is a key difference
from Lean 3.

**Pattern for progressive strengthening** (from `Algebra.Group.Basic`):
```lean
variable {α β G M : Type*}

section ite
variable [Pow α β]
end ite

section Semigroup
variable [Semigroup α]
end Semigroup

section Monoid
variable [Monoid M]
end Monoid

section Group
variable [Group G]
end Group
```

---

## 6. Naming Conventions (Detailed)

### Files
- `UpperCamelCase` (e.g., `Basic.lean`, `OfAssociative.lean`)

### Declarations
- **Types, structures, classes**: `UpperCamelCase` (`LieAlgebra`, `CommRing`)
- **Propositions, theorems, lemmas**: `snake_case` (`mul_comm`, `lie_zero`)
- **Functions returning types**: `UpperCamelCase` (matches return type)
- **Other terms**: `lowerCamelCase`
- **Prop-valued classes (nouns)**: Prefix with `Is` (`IsTopologicalRing`)
- **Prop-valued classes (adjectives)**: No prefix (`Normal`, `Continuous`)

### Theorem Name Construction

Names describe the **conclusion**, not the hypotheses:
```
succ_ne_zero      -- conclusion: succ n ≠ 0
mul_zero          -- conclusion: a * 0 = 0
le_iff_lt_or_eq   -- conclusion: a ≤ b ↔ a < b ∨ a = b
```

Hypotheses separated by `of`:
```
C_of_A_of_B       -- A → B → C
```

### Operation Dictionary

```
∨ → or       ∧ → and      → → of/imp    ¬ → not
∃ → exists   ∈ → mem      ∪ → union     ∩ → inter
⋃ → iUnion   \ → sdiff    ᶜ → compl
+ → add      - → neg/sub  * → mul       / → div
• → smul     ^ → pow      ≤ → le        < → lt
```

### Structural Lemma Patterns

```
T.ext          -- extensionality: (∀ x, f x = g x) → f = g
T.ext_iff      -- bidirectional extensionality
f_injective    -- Function.Injective f
f_inj          -- f x = f y ↔ x = y
T.induction_on -- Prop motive, value first
T.induction    -- Prop motive, constructors first
T.recOn        -- Sort u motive, value first
T.rec          -- Sort u motive, constructors first
```

---

## 7. PR Process and Review Criteria

### What Reviewers Look For

1. **Maximum generality**: Is the result stated at its weakest sufficient
   assumptions? Could `Ring` be `Semiring`?
2. **API completeness**: Does the PR provide the basic API lemmas that users
   will need? (simp lemmas, ext lemmas, basic properties)
3. **Integration**: Does the contribution connect with existing mathlib
   infrastructure? (uses existing typeclasses, follows naming patterns)
4. **Style compliance**: Copyright header, documentation, line length ≤ 100,
   proper indentation
5. **No `sorry`**: Must compile cleanly
6. **Performance**: No significant regressions; use `!bench` on PR

### What Makes a Good PR

- **Small and self-contained**: Single lemma additions or focused features
- **Well-documented**: Module docstring, declaration docstrings
- **Follows naming conventions**: Names describe conclusions
- **Maximum generality**: Weakest sufficient assumptions
- **Complete API**: Includes the lemmas users will need downstream
- **Proper commit messages**: `feat(Algebra/Lie): add LieSubalgebra.map`

### Common Rejection Reasons

- Insufficient generality
- Poor integration with existing library
- Missing documentation
- Style violations (line length, indentation, naming)
- AI-generated code that doesn't meet standards
- Content outside mathematical curriculum scope

### PR Title Format

```
<type>(<scope>): <description>

Types: feat, fix, doc, style, refactor, test, chore, perf, ci
Scope: module path without Mathlib prefix (e.g., Algebra/Lie/Basic)
Description: imperative present tense, lowercase, no period
```

---

## 8. Comparison: Our Project vs Mathlib Standards

### What We Do Well
- `@[ext]` on structures (SU5C, SO14, SO16, etc.)
- Explicit field-level comments
- Import of `Mathlib.Algebra.Lie.Basic` for typeclass infrastructure
- Clear section organization with `/-! ## ... -/` headers

### Where We Diverge (Acceptable for a Project, Not for mathlib PR)
- **Copyright headers**: We use descriptive banners instead of Apache 2.0
- **Generality**: We specialize to `ℝ` throughout (appropriate for our physics
  use case, but a mathlib contribution would generalize to `CommRing R`)
- **Module docstrings**: Our format is more narrative; mathlib expects the
  structured Main definitions/statements/notation format
- **Universe polymorphism**: We use no explicit universe variables (fine since
  we only work with `ℝ`)
- **Line length**: Our generated bracket files exceed 100 characters
- **File names**: We use `snake_case` (mathlib uses `UpperCamelCase`)

### If Contributing to Mathlib

For the Killing form uniqueness or E8 formalization, we would need to:
1. Generalize from `ℝ` to `CommRing R` or `Field K` where possible
2. Use mathlib copyright headers
3. Follow the structured module docstring format
4. Ensure line length ≤ 100
5. Rename files to `UpperCamelCase`
6. Add universe polymorphism
7. Provide complete API (simp lemmas, ext lemmas, basic properties)

---

## 9. Key Takeaways for Our Project

1. **For mathlib PRs**: State at maximum generality, follow all conventions
   above. The Killing form uniqueness (`schur_killing_uniqueness.lean`) would
   need to generalize from ℝ to a field of characteristic 0.

2. **For our project**: Current style is fine — we intentionally specialize to
   ℝ because our physics application requires it. The style divergences are
   features, not bugs, for a standalone project.

3. **Simp discipline**: Terminal `simp` unsqueezed, non-terminal `simp only`.
   We should adopt this even in our project.

4. **Documentation**: If preparing mathlib contributions, add structured
   module docstrings with Main definitions/Main statements/Tags sections.

5. **`theorem` vs `lemma`**: No enforced convention in mathlib. Use `theorem`
   for named results, `lemma` for routine lemmas. We can use either.

---

*Compiled 2026-03-18 from official mathlib documentation, source file analysis,
and community blog posts.*
