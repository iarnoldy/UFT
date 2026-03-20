# Mathlib Contribution Reference -- Complete Scraped Documentation

> Scraped 2026-03-19 from leanprover-community.github.io and web searches.
> Source URLs listed per section. This is raw reference material for building
> the definitive mathlib expert agent.

---

## Table of Contents

1. [How to Contribute (index.html)](#1-how-to-contribute)
2. [Style Guide (style.html)](#2-style-guide)
3. [Naming Conventions (naming.html)](#3-naming-conventions)
4. [Documentation Standards (doc.html)](#4-documentation-standards)
5. [Simp Lemma Guide (extras/simp.html)](#5-simp-lemma-guide)
6. [Commit Conventions (commit.html)](#6-commit-conventions)
7. [PR Review Guide (pr-review.html)](#7-pr-review-guide)
8. [Git Guide (git.html)](#8-git-guide)
9. [Linters -- Complete List](#9-linters)
10. [Lie Algebra Typeclass Patterns](#10-lie-algebra-typeclass-patterns)
11. [AI Use Policy](#11-ai-use-policy)
12. [Build Configuration Enforcement](#12-build-configuration)
13. [Web Search Findings](#13-web-search-findings)

---

## 1. How to Contribute

Source: https://leanprover-community.github.io/contribute/index.html

### What to Contribute

Small fixes (e.g., docstring fixes) and single-lemma additions in already-existing theories
are almost always welcome. Longer PRs extending existing theories are also almost always welcome.

For completely new theories, consider:
- Is the material typically taught/studied in a mathematics department?
- Is the topic within the mathematical interests of the mathlib maintainers?
- Mathlib's remit should NOT be thought of as "all of mathematics and related areas."
- Consider creating a standalone repository with mathlib as a dependency (indexed by reservoir).
- Contributors are encouraged to seek out reviewers for their PRs. A PR reviewer does NOT
  have to be a maintainer.

### Style Changes

PRs fixing style violations documented in the style guide are welcome. Other stylistic PRs
without explicit approval by authors of affected files may be closed. Discuss on Zulip first.

### Working on Mathlib

- Use `git` for version control.
- The `master` branch is production. Everything must compile, no `sorry`s.
- Work on branches in your own fork.
- Typical workflow:

```bash
git clone https://github.com/YOUR_USERNAME/mathlib4.git
cd mathlib4
lake exe cache get
git switch -c my_new_branch   # New branch per contribution
# ... make changes ...
git commit -a
lake build                     # Optional local check
lake exe mk_all                # If new files created -- updates Mathlib.lean
git push
git push --set-upstream origin my_new_branch  # If remote not configured
```

### Making a Pull Request

- Introduce yourself on Zulip (https://leanprover.zulipchat.com/).
- Make many small, self-contained PRs. Smaller = better. Especially important for new contributors.
- Title and description follow commit conventions.
- For moves/deletions, include at bottom of commit message (before `---`):

```
Moves:
- Vector.* -> Mathlib.Vector.*
- ...

Deletions:
- Nat.bit1_add_bit1
- ...
```

### Lifecycle of a PR

The review queue (`#queueboard` on Zulip) is controlled by GitHub labels.

**Label commands (anyone can use in PR comments, each on its own line):**
- `awaiting-author` / `-awaiting-author`
- `awaiting-zulip` / `-awaiting-zulip`
- `WIP` / `-WIP`
- `easy` / `-easy`
- `help-wanted` / `-help-wanted`
- `please-adopt` / `-please-adopt`
- Any `t-*` topic label (e.g., `t-topology`)
- `CI`, `IMO`
- Downstream project labels: `brownian`, `carleson`, `CFT`, `FLT`, `infinity-cosmos`,
  `sphere-packing`, `toric`

**Review flow:**
1. PR builds (green checkmark) -> reviewed within a few weeks
2. Reviewer leaves comments, adds `awaiting-author`
3. Author addresses comments, resolves conversations, removes `awaiting-author`
4. Anyone can review. Reviewer approval -> reviewer adds `maintainer-merge`
5. Maintainer gives final approval -> `ready-to-merge` auto-applied
6. `bors` bot processes merge queue

**The `easy` label criteria (ALL must be true):**
- Diff is 25 lines or less
- Does not change existing definitions or theorem statements
- Does not add definitions or new files
- Does not add `simp` lemmas or instances that aren't immediately analogous to existing ones
- Small diff alone does NOT make a PR easy

**Delegated PRs:** Maintainer trusts you to make final changes. Write `bors merge` when ready.

---

## 2. Style Guide

Source: https://leanprover-community.github.io/contribute/style.html

### Variable Conventions

| Variables | Use |
|-----------|-----|
| `u`, `v`, `w` | universes |
| `α`, `β`, `γ` | generic types |
| `a`, `b`, `c` | propositions |
| `x`, `y`, `z` | elements of generic type |
| `h`, `h₁` | assumptions |
| `p`, `q`, `r` | predicates and relations |
| `s`, `t` | lists and sets |
| `m`, `n`, `k` | natural numbers |
| `i`, `j`, `k` | integers |
| `G` | group, `R` ring, `K`/`𝕜` field, `E` vector space |

### Line Length

Lines must not exceed 100 characters.

### Header and Imports

```lean
/- Copyright (c) 2024 Joe Cool. All rights reserved. Released under Apache 2.0
license as described in the file LICENSE. Authors: Joe Cool -/
import Mathlib.Data.Nat.Basic
import Mathlib.Algebra.Group.Defs
```

- Copyright info, author list, description in header
- Imports immediately after header, no blank lines between
- Use "Authors" (plural) even for single author
- No period at end of author line
- Separate authors with commas (no "and" before final author)

### Module Docstrings

```lean
/-! # Foos and bars

In this file we introduce `foo` and `bar`, two main concepts in the theory
of xyzzyology.

## Main results

- `exists_foo`: the main existence theorem of `foo`s.
- `bar_of_foo_of_baz`: a construction of a `bar`, given a `foo` and a `baz`.

## Notation

- `|_|`: The barrification operator, see `bar_of_foo`.

## References

See [Thales600BC] for the original account on Xyzzyology.
-/
```

Requirements:
- Title
- Summary
- Main definitions and theorems section
- Notation section (if applicable)
- References section (if applicable)
- Subsequent lines indented by 2 spaces
- Bibliography entries in `docs/references.bib`

### Structuring Definitions and Theorems

**All declarations flush-left. No indentation for namespace/section contents.**

Single-line:
```lean
open Nat
theorem succ_pos : ∀ n : Nat, 0 < succ n := zero_lt_succ
def square (x : Nat) : Nat := x * x
```

Multi-line theorem (subsequent lines indented 4 spaces, proof indented 2):
```lean
import Mathlib.Data.Nat.Basic

theorem le_induction {P : Nat → Prop} {m}
    (h0 : P m) (h1 : ∀ n, m ≤ n → P n → P (n + 1)) :
    ∀ n, m ≤ n → P n := by
  apply Nat.le.rec
  · exact h0
  · exact h1 _
```

Multi-argument proof terms (each argument indented 2 spaces):
```lean
def decreasingInduction {P : ℕ → Sort*} (h : ∀ n, P (n + 1) → P n) {m n : ℕ}
    (mn : m ≤ n) (hP : P n) : P m :=
  Nat.leRecOn mn (fun {k} ih hsk => ih <| h k hsk) (fun h => h) hP
```

Complex term with Or.elim:
```lean
open Nat

theorem nat_discriminate {B : Prop} {n : Nat} (H1: n = 0 → B)
    (H2 : ∀ m, n = succ m → B) : B :=
  Or.elim (zero_or_succ n)
    (fun H3 : n = zero ↦ H1 H3)
    (fun H3 : n = succ (pred n) ↦ H2 (pred n) H3)
```

Extended List example:
```lean
import Mathlib.Init.Data.List.Lemmas

open List

variable {T : Type}

theorem mem_split {x : T} {l : List T} : x ∈ l → ∃ s t : List T, l = s ++ (x :: t) :=
  List.recOn l
    (fun H : x ∈ [] ↦ False.elim ((mem_nil_iff _).mp H))
    (fun y l ↦
      fun IH : x ∈ l → ∃ s t : List T, l = s ++ (x :: t) ↦
      fun H : x ∈ y :: l ↦
      Or.elim (eq_or_mem_of_mem_cons H)
        (fun H1 : x = y ↦
          Exists.intro [] (Exists.intro l (by rw [H1]; rfl)))
        (fun H1 : x ∈ l ↦
          let ⟨s, (H2 : ∃ t : List T, l = s ++ (x :: t))⟩ := IH H1
          let ⟨t, (H3 : l = s ++ (x :: t))⟩ := H2
          have H4 : y :: l = (y :: s) ++ (x :: t) := by rw [H3]; rfl
          Exists.intro (y :: s) (Exists.intro t H4)))
```

**Key formatting rules:**
- Explicit types on ALL arguments and return types
- Space on both sides of `:`, `:=`, and infix operators
- Place operators before line breaks, not at start of next line
- Indent proof body 2 spaces
- Multi-line theorem statements: subsequent lines indented 4 spaces
- Proof still indented 2 spaces (not 6)
- Don't orphan parentheses; keep with arguments

### Have Statements

```lean
-- Short justification on same line:
example (n k : Nat) (h : n < k) : ... :=
  have h1 : n ≠ k := ne_of_lt h
  ...

-- Longer justification on next line:
example (n k : Nat) (h : n < k) : ... :=
  have h1 : n ≠ k :=
    ne_of_lt h
  ...

-- With tactic mode (by on same line):
example (n k : Nat) (h : n < k) : ... :=
  have h1 : n ≠ k := by apply ne_of_lt; exact h
  ...

example (n k : Nat) (h : n < k) : ... :=
  have h1 : n ≠ k := by
    apply ne_of_lt
    exact h
  ...
```

### Structure/Class Definitions

Fields indented 2 spaces, each with docstring:
```lean
structure PrincipalSeg {α β : Type*} (r : α → α → Prop) (s : β → β → Prop)
    extends r ↪r s where
  /-- The supremum of the principal segment -/
  top : β
  /-- The image of the order embedding is the set of elements `b`
      such that `s b top` -/
  down' : ∀ b, s b top ↔ ∃ a, toRelEmbedding a = b

class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
    DistribMulAction R M where
  /-- Scalar multiplication distributes over addition from the right. -/
  protected add_smul : ∀ (r s : R) (x : M), (r + s) • x = r • x + s • x
  /-- Scalar multiplication by zero gives zero. -/
  protected zero_smul : ∀ x : M, (0 : R) • x = 0
```

### Instances

Use `where` syntax over braces:
```lean
instance instOrderBot : OrderBot ℕ where
  bot := 0
  bot_le := Nat.zero_le

-- With existing instance:
instance instOrderBot : OrderBot ℕ where
  __ := instBot
  bot_le := Nat.zero_le
```

### Hypotheses Left of Colon

**Preferred:**
```lean
example (n : ℝ) (h : 1 < n) : 0 < n := by linarith
example (n : ℕ) : 0 ≤ n := Nat.zero_le n
```

**Not preferred:**
```lean
example (n : ℝ) : 1 < n → 0 < n := fun h ↦ by linarith
example : ∀ (n : ℕ), 0 ≤ n := Nat.zero_le
```

**Exception (pattern matching is valid):**
```lean
lemma zero_le : ∀ n : ℕ, 0 ≤ n
  | 0 => le_rfl
  | n + 1 => add_nonneg (zero_le n) zero_le_one
```

### Binders

Space after binders; explicit types required:
```lean
example : ∀ α : Type, ∀ x : α, ∃ y : α, y = x :=
  fun (α : Type) (x : α) ↦ Exists.intro x rfl
```

### Anonymous Functions

```lean
(· ^ 2)                -- Centered dot for simple functions
fun x ↦ x * x          -- fun with ↦ (preferred)
-- λ x ↦ x * x         -- DISALLOWED in mathlib, use fun
```

### Calculations (calc blocks)

**Style 1** (relations aligned, underscores left-justified):
```lean
theorem reverse_reverse : ∀ (l : List α), reverse (reverse l) = l
  | []     => rfl
  | a :: l => calc
    reverse (reverse (a :: l))
      = reverse (reverse l ++ [a]) := by rw [reverse_cons]
    _ = reverse [a] ++ reverse (reverse l) := reverse_append _ _
    _ = reverse [a] ++ l := by rw [reverse_reverse l]
    _ = a :: l := rfl
```

**Style 2** (all lines interchangeable):
```lean
theorem reverse_reverse : ∀ (l : List α), reverse (reverse l) = l
  | []     => rfl
  | a :: l => calc
      reverse (reverse (a :: l))
    _ = reverse (reverse l ++ [a]) := by rw [reverse_cons]
    _ = reverse [a] ++ reverse (reverse l) := reverse_append _ _
    _ = reverse [a] ++ l := by rw [reverse_reverse l]
    _ = a :: l := rfl
```

Rules:
- `calc` on line prior to start of calculation
- Calculation indented
- Relations aligned across lines
- Underscores left-justified

### Tactic Mode

**`by` at end of preceding line, NEVER on its own line; all tactics indented:**

```lean
theorem continuous_uncurry_of_discreteTopology [DiscreteTopology α]
    {f : α → β → γ}
    (hf : ∀ a, Continuous (f a)) : Continuous (uncurry f) := by
  apply continuous_iff_continuousAt.2
  rintro ⟨a, x⟩
  change map _ _ ≤ _
  rw [nhds_prod_eq, nhds_discrete, Filter.map_pure_prod]
  exact (hf a).continuousAt
```

**Sub-goals with focusing dot:**
```lean
theorem exists_npow_eq_one_of_zpow_eq_one' [Group G] {n : ℤ} (hn : n ≠ 0)
    {x : G} (h : x ^ n = 1) :
    ∃ n : ℕ, 0 < n ∧ x ^ n = 1 := by
  cases n
  · simp only [Int.ofNat_eq_coe] at h
    rw [zpow_ofNat] at h
    refine ⟨_, Nat.pos_of_ne_zero fun n0 ↦ hn ?_, h⟩
    rw [n0]
    rfl
  · rw [zpow_negSucc, inv_eq_one] at h
    refine ⟨_ + 1, Nat.succ_pos _, h⟩
```

**Named subgoals with case:**
```lean
example {p q : Prop} (h₁ : p → q) (h₂ : q → p) : p ↔ q := by
  refine ⟨?imp, ?converse⟩
  case converse => exact h₂
  case imp => exact h₁
```

### Squeezing Simp Calls

**Rule: Do NOT squeeze terminal `simp` calls unless performance is critical.**

Rationale:
- Squeezed simp calls become several lines longer
- Drown useful info in sea of basic simp lemmas
- Refer to many lemmas by name; breaks on lemma renames

Terminal simp = closes goal or only followed by flexible tactics like `ring`,
`field_simp`, `aesop`.

### Whitespace and Delimiters

- **Avoid `$`** (disallowed in mathlib); use `<|` instead
- `<|` parenthesizes to the right
- `|>` parenthesizes to the left
- Avoid semicolons except special cases

```lean
-- Use <| not $:
le_antisymm hxy <| le_of_forall_pos_le_add <| by
    intro ε hε
    have := h ε hε
    linarith
```

### Empty Lines Inside Declarations

Discouraged; linter enforces absence. Use comments instead.

### Normal Forms

Standard form for equivalent statements. Use in both statements and conclusions.

Special case for bottom/top elements:
- Assumptions: use `x ≠ ⊥` (easier to check)
- Conclusions: use `⊥ < x` (more powerful)
- Example with naturals: `⊥ = 0`, so use `x ≠ 0` in assumptions, `0 < x` in conclusions

### Transparency and API Design

Transparency levels:
1. `reducible` - always unfolded
2. `semireducible` (default for `def`) - usually not unfolded in `rw`/`simp`
3. `irreducible` - never unfolded unless explicitly requested

For semireducible definitions:
- Declare instances: `instance : Foo myDef := inferInstanceAs (Foo underlyingTermOfMyDef)`
- Recycle simp API: `@[simp] lemma myDef_bar_eq_bizz (x : X) : myDef.bar = bizz := ...`

Complete seal (type synonym preferred over irreducible):
```lean
structure myDef where
  underlying : underlyingTerm
```

**Red flag:** Use of `erw` or `rfl` after `simp`/`rw` indicates missing API.

### Type Requirements

**All declarations require explicit types on all arguments AND explicit return type:**

```lean
-- BAD:
def BadStatement (n) := ∃ k, n + k = 3

-- GOOD:
def GoodStatement (n : ℕ) : Prop := ∃ k : ℕ, n + k = 3
```

### Deprecation

```lean
-- Renamed declaration (use alias):
@[deprecated (since := "YYYY-MM-DD")]
alias old_name := new_name

-- Deprecated with message:
@[deprecated "This theorem is deprecated in favor of using ... with ..."
    (since := "YYYY-MM-DD")]
theorem example_thm ...

-- With to_additive (both versions need deprecation):
@[to_additive]
theorem Group_bar {G} [Group G] {a : G} : a = a := rfl

@[deprecated (since := "YYYY-MM-DD")]
alias AddGroup_foo := AddGroup_bar

@[to_additive existing, deprecated (since := "YYYY-MM-DD")]
alias Group_foo := Group_bar
```

Exceptions:
- Named instances do NOT require deprecations
- Deprecated declarations can be deleted after 6 months

### Avoid `nonrec`

Avoid `nonrec` for namespace conflicts. Instead, add namespace to conflicting declaration.

### Profiling

Authors should benchmark contributions, especially if touching:
- Significant language components
- Adding new classes, instances, or simp lemmas
- Changing imports
- Creating new definitions

Comment `!bench` on PR for benchmarking infrastructure.

---

## 3. Naming Conventions

Source: https://leanprover-community.github.io/contribute/naming.html

### File Names

Files use `UpperCamelCase`. Rare exceptions for specifically lower-cased objects
(e.g., `lp.lean` for lp spaces) require Zulip discussion.

### Capitalization Rules

1. **Propositions/Proofs**: `snake_case`
2. **Types/Props/Sorts**: `UpperCamelCase` (with rare field exceptions)
3. **Functions**: Named matching their return type
4. **Other Terms**: `lowerCamelCase`
5. **UpperCamelCase in snake_case contexts**: Converted to `lowerCamelCase`
6. **Acronyms**: Written as a unit (e.g., `LE`, `Ne` for symmetry with `Eq`)
7. **Structure fields/inductive constructors**: Follow rules 1-6

### Symbol Dictionary

#### Logic

| Symbol | Shortcut | Name | Notes |
|--------|----------|------|-------|
| `∨` | `\or` | `or` | |
| `∧` | `\and` | `and` | |
| `→` | `\r` | `of`/`imp` | Conclusion stated first |
| `↔` | `\iff` | `iff` | Often omitted with RHS |
| `¬` | `\n` | `not` | |
| `∃` | `\ex` | `exists`/`bex` | `bex` = bounded exists |
| `∀` | `\fo` | `all`/`forall`/`ball` | `ball` = bounded forall |
| `=` | | `eq` | Often omitted |
| `≠` | `\ne` | `ne` | |
| `∘` | `\o` | `comp` | |

#### Set Operations

| Symbol | Shortcut | Name | Notes |
|--------|----------|------|-------|
| `∈` | `\in` | `mem` | |
| `∉` | `\notin` | `notMem` | |
| `∪` | `\cup` | `union` | |
| `∩` | `\cap` | `inter` | |
| `⋃` | `\bigcup` | `iUnion`/`biUnion` | Indexed/bounded indexed |
| `⋂` | `\bigcap` | `iInter`/`biInter` | Indexed/bounded indexed |
| `⋃₀` | `\bigcup\0` | `sUnion` | "set" union |
| `⋂₀` | `\bigcap\0` | `sInter` | "set" intersection |
| `\` | `\\` | `sdiff` | Set difference |
| `ᶜ` | `\^c` | `compl` | Complement |
| `{x \| p x}` | | `setOf` | |
| `{x}` | | `singleton` | |
| `{x, y}` | | `pair` | |

#### Algebra

| Symbol | Shortcut | Name | Notes |
|--------|----------|------|-------|
| `0` | | `zero` | |
| `+` | | `add` | |
| `-` | | `neg`/`sub` | Unary vs. binary |
| `1` | | `one` | |
| `*` | | `mul` | |
| `^` | | `pow` | |
| `/` | | `div` | |
| `•` | `\bu` | `smul` | Scalar multiplication |
| `⁻¹` | `\-1` | `inv` | |
| `⅟` | `\frac1` | `invOf` | |
| `∣` | `\|` | `dvd` | Divisibility |
| `∑` | `\sum` | `sum` | |
| `∏` | `\prod` | `prod` | |

#### Lattices

| Symbol | Shortcut | Name | Notes |
|--------|----------|------|-------|
| `<` | | `lt`/`gt` | |
| `≤` | `\le` | `le`/`ge` | |
| `⊔` | `\sup` | `sup` | Binary operator |
| `⊓` | `\inf` | `inf` | Binary operator |
| `⨆` | `\supr` | `iSup`/`biSup`/`ciSup` | Conditionally complete |
| `⨅` | `\infi` | `iInf`/`biInf`/`ciInf` | Conditionally complete |
| `⊥` | `\bot` | `bot` | |
| `⊤` | `\top` | `top` | |

### Ordering Convention (le and lt)

Use `ge`/`gt` in these cases:
1. Arguments appear in different orders
2. Matching argument order of another relation (`=`, `≠`)
3. Describing the relation with arguments swapped
4. Second argument is "more variable"

### Spelling

Use American English: `factorization`, `Localization`, `FiberBundle` (not British variants).

### Theorem Naming Patterns

**Descriptive names are primary.** Structure: conclusion followed by hypotheses
separated by "of":
- `C_of_A_of_B` for theorem `A → B → C`
- Hypotheses listed in appearance order

**Abbreviations:**
- `pos`, `neg`, `nonpos`, `nonneg` instead of `zero_lt`, `lt_zero`, `le_zero`, `zero_le`

**Variants:**
- "left"/"right" for operation variants: `add_le_add_left`, `le_of_mul_le_mul_right`

**Namespace removal:** When referencing namespaced definitions outside their namespace:
- `continuous_fst` (from `Prod.fst`)
- `map_natCast` (from `Nat.cast`)

### Logical Connective Namespaces

| Connective | Intro/Elim |
|------------|-----------|
| `And` | `.intro`, `.elim`, `.left`, `.right` |
| `Or` | `.inl`, `.inr`, `.intro_left`, `.intro_right`, `.elim` |
| `Iff` | `.intro`, `.elim`, `.mp`, `.mpr` |
| `Not` | `.intro`, `.elim` |
| `Eq` | `.refl`, `.rec`, `.subst`, `.symm`, `.trans` |
| `Exists` | `.intro`, `.elim` |
| `True` | `.intro` |
| `False` | `.elim` |

### Axiomatic Description Names

- `def` (unfolding)
- `refl`, `irrefl`
- `symm`, `trans`, `antisymm`, `asymm`
- `congr`, `comm`, `assoc`
- `left_comm`, `right_comm`
- `mul_left_cancel`, `mul_right_cancel`
- `inj` (injective)

### Structural Lemma Naming

**Extensionality:**
- `.ext` for `(forall x, f x = g x) -> f = g` (use `@[ext]` attribute)
- `.ext_iff` for `f = g <-> forall x, f x = g x`

**Injectivity:**
- `f_injective` for `Function.Injective f`
- `f_inj` for bidirectional: `f x = f y <-> x = y`
- `.inj_iff` for bidirectional variants
- "left"/"right" = the changing argument: `sub_right_inj`

**Induction/Recursion:**

| Motive Target | Value First | Constructions First |
|---------------|-------------|-------------------|
| `Prop` | `T.induction_on` | `T.induction` |
| `Sort u`/`Type u` | `T.recOn` | `T.rec` |

**Predicates as Suffixes:**
- Standard predicates as prefixes: `isClosed_Icc`
- Exceptions (widely used): `_injective`, `_surjective`, `_bijective`, `_monotone`,
  `_antitone`, `_strictMono`, `_strictAnti`

**Prop-valued Classes:**
- Nouns: Begin with `Is` (e.g., `IsTopologicalRing`, `IsNormal`)
- Adjectives: Optional `Is` (e.g., `Normal` or `IsNormal`)

### Function Form Variants

- Unexpanded (pointwise): Uses `mul` (e.g., `Continuous.mul`)
- Expanded (lambda form): Uses `fun_mul` (e.g., `Continuous.fun_mul`)
- Both get `@[fun_prop]` when appropriate

---

## 4. Documentation Standards

Source: https://leanprover-community.github.io/contribute/doc.html

### Header Comment Structure

Every mathlib file must begin with:
1. Copyright information header
2. Import statements (one per line)
3. Module docstring

### Module Docstring Sections (in order)

1. **Title** -- First level header (`# Title`) (mandatory)
2. **Summary** -- Following the title
3. **Main definitions** -- `## Main definitions`
4. **Main statements** -- `## Main statements`
5. **Notation** -- `## Notation` (omit only if no notation introduced)
6. **Implementation notes** -- Design decisions, typeclass choices, simp canonical forms
7. **References** -- Links to textbooks, papers, Wikipedia
8. **Tags** -- Keywords for text search

Headers use atx-style (with hash signs, no underlying dash). Open/close delimiters
`/-!` and `-/` should appear on their own lines.

References must cite entries in `docs/references.bib`.

### Declaration Documentation

**Every definition and major theorem MUST have a doc string.** Doc strings on lemmas
are also encouraged, particularly if the lemma has mathematical content or might be
useful in another file.

Format: `/--` opening and `-/` closing. Subsequent lines in a doc-string should
NOT be indented.

If a doc string is a complete sentence, it should end in a period.

Doc strings should convey the mathematical meaning. They are allowed to lie slightly
about the actual implementation.

Named theorems should be **bold faced** (two asterisks).

### Tactic Documentation

- Start with complete sentence with tactic as subject
- Include all options and forms in bulleted list
- Include "Examples:" section with code blocks

### Linting

```lean
#lint only docBlame                -- Definitions without docstrings
#lint only docBlame docBlameThm    -- Definitions AND theorems/lemmas
#lint                              -- All default linters
#lint docBlameThm                  -- Defaults plus theorem doc check
```

### LaTeX and Markdown

- References to Lean declarations in backticks. Fully-qualified names become links.
- Raw URLs in angle brackets `<...>` for clickability.
- Math: `$ ... $` inline, `$$ ... $$` display mode
- MathJax rendering (same as math.stackexchange.com)

### Sectioning Comments

Use `/-! ... -/` for section documentation. Third-level headers `###` for titles
inside sectioning comments. If more than one line, delimiters on their own lines.

### Language

Documentation in English. Any common spelling acceptable (British, American, Australian).
PRs changing only spelling discouraged unless part of substantive enhancement.

### Citation Format

Add references to `docs/references.bib` first. Normalize using bibtool.

```
See [Boole1854] for the original account.      -- Key in brackets = link
See [Grundlagen der Geometrie][hilbert1999]...  -- Custom text before key
```

Cannot use closing bracket `]` in link text.

---

## 5. Simp Lemma Guide

Source: https://leanprover-community.github.io/extras/simp.html

### Core Functionality

`simp` is a conditional term rewriting system. Repeatedly replaces subterms matching
lemmas of form `A = B` or `A <-> B`. Processes from innermost to outermost.

### Simp Lemma Rules

Lemmas marked `@[simp]` join the simplification database. **Critical: RHS must be
simpler than LHS** (rewriting only proceeds left-to-right).

**Terrible simp lemmas (DO NOT):**
- `1 = a * a⁻¹` (wrong direction)
- `(1 : G) = 1 * 1⁻¹` (infinite loop)

Over 40,000 simp lemmas in mathlib as of February 2026.

### Simp Normal Form

When multiple equivalent formulations exist (e.g., `n ≠ 0`, `0 ≠ n`, `n > 0`),
mathlib designates one canonical form. Example: `0 < n` is preferred for positivity.

`@[simps]` auto-generates projection evaluation lemmas.

### Usage Syntax

```lean
simp                    -- All known simp lemmas
simp [h1, h2]           -- Adds hypotheses or non-simp lemmas
simp [← h]              -- Reverses equality direction
simp [-thm]             -- Excludes specific simp lemma
simp [*]                -- Uses all local hypotheses
simp at h               -- Simplifies hypothesis h
simp [h1] at h2 ⊢       -- Simplifies multiple targets
simp only [...]         -- Uses EXCLUSIVELY listed lemmas
simp [↓h1]              -- Applies before entering subterms
simp [↑h1]              -- Applies after entering subterms
```

### Terminal vs Non-Terminal

**Rule: Every `simp` in final code should completely close a goal.**

Approved non-terminal uses:
1. `simp only [h1, h2, ..., hn]` -- constrained to explicit lemmas, immune to library changes
2. `have h : P := by ...; simp` -- introduces hypothesis where simp closes its goal
3. `suffices : P by simpa` -- pattern with new goal

Replace `simp at ⊢ h; exact h` with `simpa using h`.

### `simpa` Tactic

Finishing tactic that fails if unable to close goals:
```lean
simpa [h1, h2] using e
```
Both type of `e` and goal simplified; success requires both simplify identically.

### `dsimp` Variant

Uses only "definitional" simp lemmas (proven by `rfl` or `Iff.rfl`).

`dsimp only` (empty list) safely simplifies mid-proof: beta reduction, structure
projection reduction, zeta reduction. No external lemmas.

### Configuration Options

| Option | Default | Purpose |
|--------|---------|---------|
| `maxSteps` | 100000 | Maximum rewrite steps |
| `maxDischargeDepth` | 2 | Recursion depth for side conditions |
| `contextual` | false | Use context-dependent simp lemmas |
| `memoize` | true | Cache subterm simplifications |
| `singlePass` | false | Visit each subterm at most once |
| `zeta` | true | Reduce let-bindings |
| `beta` | true | Beta-reduce |
| `iota` | true | Reduce recursors |
| `proj` | true | Reduce projections |
| `decide` | false | Reduce decidable propositions |
| `arith` | false | Simplify arithmetic |
| `autoUnfold` | false | Unfold equation compiler lemmas |
| `dsimp` | true | Switch to dsimp on dependent args |
| `failIfUnchanged` | true | Fail if no simplifications applied |
| `ground` | false | Reduce ground terms |

Example:
```lean
example {x y : ℕ} : x = 0 → y = 0 → x = y := by
  simp (config := { contextual := true })
```

### Trace Options

```lean
set_option trace.Meta.Tactic.simp.rewrite true  -- Shows successful rewrites
set_option trace.Meta.Tactic.simp true           -- Shows all rewrite attempts
set_option trace.Meta.Tactic.simp.discharge true -- Shows side condition solving
```

### Custom Simp Attributes

Using `register_simp_attr`, create custom attributes where tagged lemmas must be
explicitly included: `simp [new_attr]`. Examples: `@[mfld_simps]`, `@[field_simps]`.

### Discharger

```lean
simp (disch := decide) only [Nat.max_eq_left]
```

---

## 6. Commit Conventions

Source: https://leanprover-community.github.io/contribute/commit.html

### Format

```
<type>(<optional-scope>): <subject>

<body>

<footer>

<dependencies>
```

### Types

- **feat** -- feature
- **fix** -- bug fix
- **doc** -- documentation
- **style** -- formatting, missing semicolons, etc.
- **refactor**
- **test** -- adding missing tests
- **chore** -- maintain
- **perf** -- performance improvement
- **ci** -- changes to GitHub workflows, automation

### Scope

Identifies affected module/directory. Omit "Mathlib" prefix.
Examples: `Data/Nat/Basic`, `Algebra/Group/Defs`, `Topology/Constructions`

### Subject Line Rules

1. Use imperative, present tense: "change" not "changed" nor "changes"
2. Do NOT capitalize the first letter
3. No period at the end

### Body

- Imperative, present tense
- Include motivation and contrast with previous behavior

### Footer

- Breaking changes: describe change, justification, migration notes
- Issue references: `Closes #123, #456`

### Dependencies

If PR depends on others: `- [ ] depends on: #XXXX`

---

## 7. PR Review Guide

Source: https://leanprover-community.github.io/contribute/pr-review.html

Everyone is welcome and encouraged to review PRs. Only maintainers can merge.
Follow Contributor Covenant Code of Conduct. Be gentle in feedback.

### Five Core Evaluation Areas

#### 1. Style
- Code formatting: spacing around binary operations, proper line breaks, colon at line end
- Naming: follow mathlib standards (`mul` not `times`, `one` not `1`)
- PR metadata: titles and descriptions must be informative (permanently in git history)

#### 2. Documentation
- **Docstrings for definitions**: `docBlame` linter checks existence; reviewer verifies accuracy
- **Important theorems**: complex theorems need docstrings explaining the statement
- **Proof comments**: intricate proofs need "a sketch in comments interspersed throughout"
- **Usage warnings**: declarations requiring restricted usage must include warnings
- **Literature connections**: code formalizing published math should cite sources in
  `references.bib` and module documentation

#### 3. Location
- **File placement**: use `#find_home` command to verify appropriate file
- **Duplicate detection**: `apply?` and `exact?` help find existing more general results
- **Import management**: scrutinize new imports. Guard against "import creep"
- **File splitting** (three reasons):
  - Exceeding ~1000 lines
  - Multiple loosely-related sections
  - Avoiding import creep from new results

#### 4. Improvements
- **Supporting lemmas**: long proofs = refactoring opportunity
- **Better tactics**: `gcongr` > `mul_le_mul_of_nonneg_left`; `positivity` for verbose proofs
- **Proof restructuring**: e.g., `Algebra.adjoin_le` > `Algebra.adjoin_induction'`
- **Definition quality**: prefer non-dependent types when possible

#### 5. Library Integration
- **Attributes**: verify `@[simp]`, `@[ext]`, `@[gcongr]`, `@[aesop]` applied correctly
- **Future generality**: check for more general literature versions using existing mathlib concepts
- **Design alignment**:
  - New morphisms: bundled types with `FunLike` API
  - New subobjects: bundled subobjects with `SetLike` API
  - Follow existing library notes
- **Universe polymorphism**: use `Type*` not `Type _`
- **Instance safety**: no diamonds, no non-defeq/non-propeq relationships

---

## 8. Git Guide

Source: https://leanprover-community.github.io/contribute/git.html

### One-Time Setup

```bash
# Quick start with GitHub CLI:
gh repo fork leanprover-community/mathlib4 --default-branch-only --clone

# Or manual:
# 1. Fork on GitHub
# 2. Clone:
git clone https://github.com/YOUR_USERNAME/mathlib4.git && cd mathlib4
# 3. Configure remotes (origin = your fork, upstream = official)
# 4. Configure master:
git fetch upstream
git branch --set-upstream-to=upstream/master master
# 5. Configure push behavior:
git config push.default current
git config push.autoSetupRemote true
```

### Daily Workflow

```bash
git switch master && git pull     # Update master
git switch -c my-feature-branch   # New branch
# ... make changes ...
git push                          # Push
```

### Working with Others' PRs

```bash
gh pr checkout 1234               # Recommended
# Or:
git remote add contributor https://github.com/USERNAME/mathlib4.git
git fetch contributor
git checkout contributor/their-branch
```

### Security Warning

Checking out and running someone else's code = running unreviewed code on your computer.

---

## 9. Linters

### Layer 1: Syntax Linters (active during parsing)

Imported in `Mathlib/Init.lean`:

| Linter | What It Checks |
|--------|---------------|
| `linter.style.header` | File headers and copyright notices |
| `linter.style.longLine` | Lines > 100 characters (URLs exempt) |
| `linter.style.longFile` | Files > 1500 lines (configurable, 0 = silent) |
| `linter.style.cdot` | Proper `·` character (not plain `.`); no isolated cdots on own line |
| `linter.style.multiGoal` | Tactics creating multiple goals |
| `linter.hashCommand` | Deprecated `#` commands |
| `linter.oldObtain` | Deprecated `obtain'` syntax |

### Layer 2: Style Linters (Mathlib.Tactic.Linter.Style)

| Linter | What It Checks |
|--------|---------------|
| `setOption` | Flags `set_option` for `pp`, `profiler`, `trace`, `maxHeartbeats` options |
| `missingEnd` | Sections/namespaces must be closed by file end (outer `noncomputable section` exempt) |
| `dollarSyntax` | Flags `$` usage; must use `<\|` instead |
| `lambdaSyntax` | Flags `λ`; must use `fun` |
| `longFile` | Files > 1500 lines default |
| `longLine` | Lines > 100 chars (URLs exempt) |
| `nameCheck` | Flags double underscores in declaration names |
| `openClassical` | Flags unscoped `open Classical` (should be scoped to declarations) |
| `show` | Ensures `show` doesn't change the goal (use `change` instead) |

### Layer 3: Environment Linters (post-elaboration, via `lake exe runLinter`)

| Linter | What It Checks |
|--------|---------------|
| `docBlame` | Missing documentation strings |
| `unusedDecidableInType` | Unused `Decidable` instances |
| `unusedFintypeInType` | Unused `Fintype` instances |
| `structureInType` | Structure should be in `Prop` |
| `deprecatedNoSince` | `@[deprecated]` tags without `since` dates |
| `dupNamespace` | Same namespace repeated consecutively (e.g., `Nat.Nat.foo`) |

### Layer 4: Text-Based Linters (regex, via `lake exe lint-style`)

| Error Code | What It Checks |
|------------|---------------|
| `ERR_WIN` | Windows line endings (`\r\n`) |
| `ERR_TWS` | Trailing whitespace |
| `ERR_MOD` | Module names match file paths |
| `ERR_COP` | Copyright headers |
| `ERR_IMP` | Import ordering |

### Exception Files

- `scripts/nolints.json` -- Environment linter exceptions (auto-updated weekly)
- `scripts/nolints-style.txt` -- Text linter exceptions (manual)
- `scripts/noshake.json` -- Unused import exceptions (categories: `ignoreImport`, `ignoreAll`, `ignore`)

### Linter Commands

```lean
#lint                              -- All default linters
#lint*                             -- Omit slow tests
#lint-                             -- Silent mode
#lint+                             -- Verbose mode
#lint only docBlame                -- Only specific linters
#lint docBlameThm                  -- Defaults plus additional
#list_linters                      -- Print all available linters
```

Suppress per-declaration: `@[nolint doc_blame unused_arguments]`

---

## 10. Lie Algebra Typeclass Patterns

Source: mathlib4_docs, arXiv:2112.04570, arXiv:2505.19975v1

### Core Hierarchy

**LieRing L**: extends `AddCommGroup L` and `Bracket L L`
- Additivity in both arguments: `⁅x + y, z⁆ = ⁅x, z⁆ + ⁅y, z⁆`
- Diagonal vanishing: `⁅x, x⁆ = 0`
- Leibniz/Jacobi: `⁅x, ⁅y, z⁆⁆ = ⁅⁅x, y⁆, z⁆ + ⁅y, ⁅x, z⁆⁆`

**LieAlgebra R L**: extends `Module R L`
- Scalar compatibility: `⁅x, t • y⁆ = t • ⁅x, y⁆`
- First-argument compatibility follows from natural self-action

**LieRingModule L M**: additive action of Lie ring on additive group

**LieModule R L M**: scalar multiplication compatibility in both bracket arguments

**IsLieTower**: Leibniz rule for relative bracket actions

### Morphisms

- **LieHom** (`L₁ →ₗ⁅R⁆ L₂`): linear map preserving brackets
- **LieEquiv** (`L₁ ≃ₗ⁅R⁆ L₂`): linear equivalence + bracket preservation
- **LieModuleHom / LieModuleEquiv**: module-level morphisms

### Design Notes (from mathlib and recent papers)

**Unbundling**: Lie algebras partially unbundled (like modules).

**Concrete instantiation strategy**: Model on `Fin n → K` (more practical/scalable than
iterated products). Use type synonyms to avoid instance inference conflicts:

```lean
def Affine := Fin 2 → K
instance : LieRing (Affine K) := {
  bracket := fun l r ↦ ![0, l 0 * r 1 - r 0 * l 1]
  ...
}
```

**Parametric families**: Use 2-parameter family to handle infinite families uniformly:
```lean
def Family (_ _ : K) := Fin 3 → K
instance (α β : K) : LieRing (Family K α β) := {...}
```

**Classification results**: Return `Nonempty (L ≃ₗ⁅K⁆ Representative)` not explicit
`LieEquiv` terms. Proof irrelevance means Lean doesn't retain specific isomorphism data.

**Key supporting structures**:
- `LieSubalgebra K L` and `LieIdeal K L`: bundled structures (predicates on carrier sets)
- `IsSolvable L`: proposition typeclass

### Oliver Nash's Contributions

- "Formalising Lie algebras" (CPP 2022) -- arXiv:2112.04570
  - Constructed classical and exceptional Lie algebras
  - Enabled stating classification theorem for finite-dim semisimple Lie algebras
  - Demonstrated "the unity of Mathlib" by leveraging several library branches
- "Engel's theorem in Mathlib" (JAR 2023) -- arXiv:2304.10424
  - Formalized Engel's theorem and application to root space theory

### Recent Work: Low-Dimensional Solvable Classification (2025)

From arXiv:2505.19975v1:
- Used `Fin n → K` over iterated products (more practical/scalable)
- Created `mkAbelian` constructor for trivial brackets (avoids conflicts)
- Standard `module` tactic can't handle `⁅x, y⁆` atoms -- developed `simplify_lie`
- Mathlib later developed Lyndon-word based alternative
- Lean 4 + mathlib4 v4.19.0
- Repository: https://github.com/LieLean/LowDimSolvClassification

---

## 11. AI Use Policy

Source: https://leanprover-community.github.io/contribute/index.html (March 2026 version)

> "Using artificial intelligence tools to generate code is becoming more and more common.
> While this can be practical, their use also poses ethical, ecological, legal and social
> concerns. We recognise that there are strong differences in opinion on this topic, and
> do not enforce a strict ban."

**Requirements:**
1. If you use AI (Copilot, ChatGPT, Codex, Claude, Gemini, etc.), explain in PR description:
   which tool(s) and how you used them.
2. You MUST vouch for and understand ALL code submitted. If you don't, the PR may have
   negative value.
3. Be particularly careful with AI for new code: "mathlib intentionally has very high
   standards (on generality, integration with the remaining library and maintainability,
   including code style). **As of March 2026, AI-written code fails to meet that bar by
   a large margin.**"
4. Getting code to mathlib's standards requires understanding and writing Lean code by hand.
5. "If you just want to help and not put in the learning effort, making a PR to mathlib
   is counterproductive: the effort required from the mathlib maintainers is larger than
   the benefit."

---

## 12. Build Configuration

Source: DeepWiki mathlib4, lakefile.lean

### Required Lean Options (mathlibLeanOptions)

```lean
pp.unicode.fun := true          -- Pretty-print ↦ notation
autoImplicit := false           -- Reject implicit arguments
maxSynthPendingDepth := 3       -- Type class search depth
```

`autoImplicit := false` is enforced globally. 317 files were migrated when this became
default. Files that need it must explicitly `set_option autoImplicit true`.

### Linter Configuration (mathlibOnlyLinters)

Prefixed with `weak` designation, includes:
- `linter.mathlibStandardSet`
- `linter.style.header`
- `linter.checkInitImports`
- `linter.allScriptsDocumented`
- `linter.pythonStyle`
- `linter.style.longFile` (limit 1500)

### CI Pipeline

1. Dependency validation
2. Cache fetching (Azure/Cloudflare)
3. Build compilation with linter enforcement
4. Test execution (MathlibTest/)
5. Linter execution (all three layers)
6. Cache upload (Azure Blob Storage)

**Sandbox isolation**: untrusted PR code runs in `landrun` sandboxes with:
- Read-only filesystem access (`--rox /usr`)
- Read-write only to `.lake/`
- Network isolation

### Benchmarking

Comment `!bench` on a PR to trigger benchmarking infrastructure.

---

## 13. Web Search Findings

### Mathlib Initiative (2025-2026)

- Deliverable: review response times under one week for 90% of review cycles by
  September 2026
- Strategy: professional editorial team of research mathematicians to process review queue
- Working within existing maintainer structure
- As of September 2025: ~2000 open PRs

### Common PR Issues for New Contributors

1. **Duplicating existing results** -- use `apply?`, `exact?` to check
2. **Import hierarchy problems** -- adding unnecessary imports to access helper lemmas
3. **Poor/inaccurate documentation** -- `docBlame` checks existence, not quality
4. **Overly large PRs** -- small, self-contained pieces get reviewed faster

### Practical Tips

- Use `#find_home` to verify declaration belongs in appropriate file
- Use `Type*` not `Type _` for universe polymorphism
- New morphisms: bundled type with `FunLike` API
- New subobjects: bundled with `SetLike` API
- Mark with `@[ext]`, `@[simp]`, `@[gcongr]`, `@[aesop]` where appropriate
- Check for instance diamonds
- Partial reviews are welcome -- learn in piecemeal fashion

### Dangerous Instance Linter

The `dangerous_instance` linter (checks for instances generating typeclass problems
with metavariables) has NOT been fully ported to mathlib4 yet (as of 2026). Porting
notes exist for cases where it should be re-enabled.

### Key Community Resources

- Zulip: https://leanprover.zulipchat.com/
  - `#new users` stream for help
  - `#mathlib` channel for contribution discussions
  - `#PR reviews` stream for explicit review requests
- Review queue: https://leanprover-community.github.io/queueboard/
- API docs: https://leanprover-community.github.io/mathlib4_docs
- Declaration search: https://loogle.lean-lang.org/
- Online Lean: https://live.lean-lang.org/
- Reservoir (project index): https://reservoir.lean-lang.org
