# PR: Bivector Lie subalgebra of Clifford algebras

## Title
feat(LinearAlgebra/CliffordAlgebra): bivector Lie subalgebra

## Body

### Summary

We define the submodule of bivectors in a Clifford algebra (spanned by
products `ι(m₁) * ι(m₂)`) and show it forms a `LieSubalgebra` under
the commutator bracket. This gives the standard construction of the
orthogonal Lie algebra so(Q) from Cl(Q).

### Main definitions

* `CliffordAlgebra.bivector` -- the `Submodule R (CliffordAlgebra Q)`
  spanned by products `ι Q m₁ * ι Q m₂`
* `CliffordAlgebra.bivectorLieSubalgebra` -- the `LieSubalgebra` of
  bivectors under the commutator bracket

### Main results

* `CliffordAlgebra.ι_mul_ι_comm'` -- subtraction form of the Clifford
  anticommutation: `ι Q b * ι Q a = polar(a,b) - ι Q a * ι Q b`
* `CliffordAlgebra.lie_ι_mul_ι` -- explicit commutator formula for
  bivector generators as a linear combination of bivectors
* `CliffordAlgebra.lie_mem_bivector` -- the bivector submodule is
  closed under the Lie bracket
* `CliffordAlgebra.bivector_le_evenOdd_zero` -- bivectors lie in
  the even part of the Clifford algebra

### Dependencies

None -- uses only existing `CliffordAlgebra.Grading`,
`Lie.OfAssociative`, and `Tactic.NoncommRing`.

### Implementation notes

The `LieModule R (CliffordAlgebra Q) (CliffordAlgebra Q)` instance
does not synthesize automatically (exceeds default heartbeat limit),
so we provide it explicitly via `lieAlgebraSelfModule`. This is a
known issue with deep instance chains in the Clifford algebra
typeclass hierarchy.

The commutator formula `lie_ι_mul_ι` uses `noncomm_ring` for
associativity/distribution steps and `Algebra.commutes` to commute
`algebraMap` scalars past algebra elements.

The formula produces `ι Q c * ι Q b` and `ι Q c * ι Q a` (not
`ι Q b * ι Q c` and `ι Q a * ι Q c`) because swapping would
introduce scalar-scalar cross-terms that do not cancel.

### AI disclosure

This code was generated and proven entirely by AI (Claude, Anthropic)
under the direction of the submitter, who is not a Lean programmer.
The submitter understands the mathematical content (bivectors form a
Lie subalgebra of the Clifford algebra) but cannot independently
vouch for every line of Lean syntax. The code compiles with zero
sorry against current mathlib. Extra review scrutiny is welcomed.
The mathematical result is classical; see Doran & Lasenby,
*Geometric Algebra for Physicists* (Cambridge, 2003), Chapter 3.

### Status

All proofs complete. Zero sorry. Compiles cleanly with current
mathlib (no warnings).

---

## QA Checklist

- [x] Copyright header (Apache 2.0, Authors)
- [x] Module docstring (title, summary, Main definitions, Main results, Tags)
- [x] All defs have docstrings
- [x] LaTeX in docstrings, not unicode
- [x] Maximum generality: `CommRing R`, `AddCommGroup M`, `Module R M`
- [x] `Type*` not `Type _`
- [x] Line length <= 100 characters (verified: 0 violations)
- [x] 4-space continuation indent
- [x] 2-space proof indent
- [x] `by` at end of line, never standalone
- [x] No blank lines between structure/instance fields
- [x] Declarations flush-left
- [x] Namespace content not indented
- [x] Focus dots properly placed
- [x] `fun` not `lambda`
- [x] No `$` usage
- [x] Scoped `section`/`variable` usage
- [x] UpperCamelCase file name: `Bivector.lean`
- [x] dot-notation friendly naming
- [x] Zero sorry -- all proofs complete
- [x] `Submodule.span_induction₂` uses modern `induction ... using` syntax
- [x] Uses existing mathlib API (`ι_mul_ι_comm`, `ι_mul_ι_add_swap`, `ι_mul_ι_mem_evenOdd_zero`)
- [x] Clean compilation (zero warnings)
- [x] Minimal imports (3, no transitive redundancy)
- [x] Private helper lemmas for proof scaffolding
- [x] `@[simp]` on membership characterization lemmas
