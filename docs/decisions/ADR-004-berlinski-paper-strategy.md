# ADR-004: Berlinski-Reframed Paper & Proof Strategy

**Status:** Accepted
**Date:** 2026-03-12
**Context:** Wilson withdrew endorsement because papers overclaim. The Berlinski lens clarifies: there's nothing wrong with arithmetic proofs. There's everything wrong with calling them algebraic verification.

## Decision

Submit what's honest. Hold what isn't. Upgrade only where honest labeling isn't enough.

## Immediate: Submit

### Paper 1 (CICM 2026) — Submit now
- Methodology paper. The contribution is the method (Lean 4 for alternative math), not the proofs themselves.
- Honest scope already achieved.

### Paper 2 (AACA) — Tighten and submit
- Mathematically strongest paper. Real algebraic content (Killing form, Lie bracket closure).
- Action: tighten from 18 to ~12 pages, remove padding.

## Hold: Need algebraic proof to justify claims

### Paper 3 (PRD) — Hold
- A dimensional scaffold paper doesn't belong in a physics journal without real algebra.
- Either add genuine algebraic content (subalgebra closure, anomaly cancellation) or change venue.

### Paper 4 (LMP) — Hold
- Same reasoning. Three-generation claims require representation-level proof, not dimension counting.

## Selective Upgrades

Only where the claim requires algebra and relabeling is insufficient:

| Upgrade | Effort | Justification |
|---------|--------|---------------|
| SU(5) → SO(10) `LieAlgebra.Hom` | 1-2 weeks | 24 bracket theorems exist; packaging as morphism is wiring. Paper 1 claims "embedding" — needs the Hom. |
| Anomaly trace vanishing | 2-3 weeks | If any paper claims "anomaly-free," needs a matrix trace theorem. `6 = 6` cannot be relabeled into that. |
| SO(14) subalgebra closure | 2-3 weeks | If Paper 3 claims "subalgebra decomposition," bracket closure is required. Dimension counting is necessary but not sufficient. |

## Deferred (future papers, not current fix)

- SO(14) full 91-generator Jacobi (4-6 weeks)
- Wedge product from mathlib (2-3 weeks) — "axiomatized" label is honest for now
- Maxwell from coordinates (2-3 weeks) — same
- Weight-level branching (3-4 weeks) — Paper 4 can wait
- Non-abelian Bianchi (1-2 weeks) — same

## What stays arithmetic (and that's fine)

These results are correctly classified as arithmetic. They do not need upgrading — they need honest labels:

- Clifford dimensions (2^n) → "dimensional consistency checks"
- Decomposition dimension counts (45 + 6 + 40 = 91) → "arithmetic verification"
- Representation dimensions → call them what they are
- Wightman axioms → definitions, not derivations (cannot be derived)

## Berlinski Test (pre-submission gate)

Before any paper submission: strip every adjective. Remove framing. Look at the naked result. Does the claim match the proof? If yes, submit. If no, fix the claim or fix the proof. Never dress one as the other.

## Verification Protocol

1. `lake build` — zero errors, zero sorry
2. Paper-integrity-auditor on each paper before submission
3. Berlinski test: every [MV] claim checked against actual tactic used
4. Ian reads final prose aloud — if it sounds like AI, rewrite in his voice

## Consequences

- Papers 1 and 2 can proceed to submission immediately after audit/tighten cycle
- Papers 3 and 4 are blocked until either (a) algebraic upgrades land or (b) claims are downscoped to match existing proofs
- All future papers pass the Berlinski test before submission — this is now constitutional (CLAUDE.md mandate #4)
