# Lean Zulip Conversation Log — 2026-03-18

## Thread

**Channel**: "Is there code for X?"
**Topic**: "Formalizing Lie Algebra Embeddings in Lean 4 — Scalability Lessons from E₈ (88 files, zero sorry)"
**Posted**: 2026-03-18
**URL**: (on leanprover.zulipchat.com)

## Key Interactions

### 1. Initial Post
Shared: 88 proof files, ~2,975 declarations, five LieHoms, E₈ sparse Jacobi, scalability lessons.
Disclosed: Claude collaboration, AET background.

### 2. Response: Clifford Algebra Question
**Community member asked**: Many files mention "clifford" — why not use mathlib's `CliffordAlgebra`?

**Our reply**: Didn't run into issues — never tried it. Project grew bottom-up from hand-defined multiplication tables. At scale (SO(14)=91 gens, SO(16)=120 gens), avoiding the 2^n blowup of full Clifford algebra was practical.

### 3. Response: Eric Weiser's Suggestion
**Eric Weiser** (author of `CliffordAlgebra.even` in mathlib) pointed to:
`https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/CliffordAlgebra/Even.html`

**What this provides**: The even subalgebra of a Clifford algebra (grades 0+2+4+...).
For Cl(1,3): even part = 8-dim (grade 0: 1-dim + grade 2: 6-dim + grade 4: 1-dim).
The grade-2 part (6-dim) IS so(1,3) — our `Bivector` type.

**Assessment**: This makes small-case derivation (Cl(1,1), Cl(1,3)) feasible.
For large n (Cl(14) even = 8,192-dim), still impractical vs our flat approach.

**Planned reply**: Offer to build so(p,q) from `CliffordAlgebra.even` for small cases as a mathlib PR.

## Potential Contributions (discussed in thread)

1. **Lie-Schur lemma** → `Mathlib.Algebra.Lie.Schur` (first in any ITP, we believe)
2. **so(p,q) from CliffordAlgebra.even** → grade-2 extraction + LieRing instance
3. **Antisymmetric trace identity** → standalone lemma
4. **Scalability lessons** → blog post or documentation

## Files Referenced

- `research/lean-community-submission-plan.md` — full step-by-step guide
- `src/lean_proofs/spectral/schur_killing_uniqueness.lean` — Schur/Killing proof
- `src/lean_proofs/clifford/anomaly_trace.lean` — trace identity
- `src/lean_proofs/clifford/su5c_compact.lean` — mathlib instance pattern
- `.lake/packages/mathlib/Mathlib/LinearAlgebra/CliffordAlgebra/Even.lean` — Eric's file

## Action Items

- [ ] Reply to Eric about CliffordAlgebra.even → so(p,q) for small cases
- [ ] If community interest: fork mathlib4, extract Schur/Killing, prepare PR
- [ ] Track any endorsement opportunities for arXiv
