# ADR-003: Prose-Proof Coherence Crisis and Paper Restructuring

## Status

Accepted (2026-03-12)

## Context

### The Wilson Correspondence

On 2026-03-12, Robert A. Wilson (Queen Mary University of London, world authority
on E₈ and finite simple groups) withdrew his consideration of arXiv endorsement
with this statement:

> "I think I now understand why I can't understand your papers. The arXiv will
> certainly reject AI-generated papers, and I will certainly not endorse any
> such thing."

This was not a rejection of the mathematics. Wilson had previously:
- Independently confirmed our algebraic necessity finding (D₈ vs Z₄)
- Expressed interest in the SU(9)/Z₃ three-generation paper
- Provided substantive feedback on massive chirality (compact gauge group =
  intrinsically massless)

His withdrawal was about **prose quality and coherence**, not mathematical content.

### The Diagnosis

Wilson identified two problems:
1. **Prose-proof incoherence** (primary): The connecting narrative asserts things
   the theorems don't prove. Logic chains have gaps that AI prose papers over.
2. **AI voice** (symptom): Downstream of #1. Inflated language, self-congratulatory
   framing, and confidence that outstrips the evidence.

### The Audit

We built a `paper-integrity-auditor` agent and ran it on all four papers in
parallel. The agent maps every prose claim to its supporting Lean theorem and
classifies each as: ACCURATE / OVERCLAIMED / TAUTOLOGICAL / SCOPE BLUR /
CHAIN GAP / UNSUPPORTED / INFLATED / AI TELLTALE.

### What the Audit Found

**The central pathology across all four papers:**

Arithmetic tautologies dressed up as structural proofs.

The prose takes `(45 : ℕ) + 6 + 40 = 91 := by norm_num` and calls it
"machine-verified algebraic decomposition of so(14)." A reviewer who reads
the Lean files sees `norm_num`, `native_decide`, and `rfl` everywhere and
concludes — correctly — that the papers are overclaiming.

| Paper | Target | ACCURATE | OVERCLAIMED | TAUTOLOGICAL | SCOPE BLUR | CHAIN GAP | AI TELLTALE | Severity |
|-------|--------|----------|-------------|--------------|------------|-----------|-------------|----------|
| 1     | CICM   | 26       | 6           | 5*           | 2          | 2         | 6           | Medium   |
| 2     | AACA   | 35+      | 4           | 5            | 2          | 0         | 2           | Low      |
| 3     | PRD    | 8        | 7           | 5            | 3          | 2         | 5           | Critical |
| 4     | LMP    | 26       | 11          | 2            | 4          | 0         | 4           | High     |

*Paper 1's tautologies are in referenced files, not directly cited in the body.

**Worst individual findings:**
- `anomaly_checklist : (6 : ℕ) = 6 := rfl` presented as "all 6 anomaly conditions
  machine-verified" (Paper 3)
- `(3 : ℕ) = 3 := rfl` presented as "the number 3 arises from SU(3)_family" (Paper 4)
- `three_generation_theorem` containing arithmetic like `80 + 84 + 84 = 248` presented
  as "machine-verified resolution of the three-generation problem" (Papers 1, 4)
- "Algebraic hierarchy from Z₄ through Clifford algebras to spacetime" with no
  morphisms connecting the independently-defined algebras (Paper 1)

### What Actually IS Real

Twelve genuinely algebraic results survive honest reframing:

1. `algebraic_necessity_general` — over ANY field, Dollard's 3 axioms force h = -1
2. A4 Cartan matrix — 48 theorems verifying su(5) root system. First machine-verified
   Lie algebra identification for a GUT subalgebra.
3. `jacobi` for so(10) — full 45-component Jacobi identity
4. `centralizer_closed` — su(5) is a Lie subalgebra of so(10) via centralizer
5. `gravity_gauge_commute` — [so(4), so(10)] = 0 in so(14)
6. `killing_form_negative` — Killing form of so(3) is negative definite
7. `charge_preserves_vev` — Q = T₃ + Y/2 annihilates the Higgs VEV
8. `grade2_times_grade2_selection` — bivector product grade selection in Cl(3,0)
9. Four LieRing/LieAlgebra mathlib instances (so(1,3), sl(3), sl(5), so(10))
10. `no_so_gives_three_families` — 2^k ≠ 3 for all k (genuine ∀ statement)
11. `odd_nine_all_chiral` — all Λ^k(C⁹) for 0 < k < 9 are non-self-conjugate
12. Root eigenvalue completeness for su(3) — all 8 eigenvalues of ad_{H1}, ad_{H2}

These are real contributions. Nobody has machine-verified a Lie algebra identification,
a GUT subalgebra closure, or gravity-gauge commutation in any theorem prover before.

The ~50 additional arithmetic consistency checks (dimensions, sums, binomial
coefficients) are useful bookkeeping but should never have been called "proofs"
of algebraic structure or physics.

## Decision

### The Lesson

**Arithmetic alone isn't good enough.**

A theorem prover that verifies `45 + 6 + 40 = 91` has not verified that so(14)
decomposes into so(10) ⊕ so(4) ⊕ mixed. The dimension check is necessary but
not sufficient. The actual decomposition requires proving that generators with
indices 1-10 form a Lie subalgebra, generators with indices 11-14 form another,
and the two commute — which IS proved for [so(10), so(4)] = 0, but is NOT what
the dimension arithmetic proves.

We confused the scaffolding (dimensional consistency) with the building (algebraic
structure). The papers presented both as if they were the same thing.

### The Fix

Restructure all four papers following these principles:

1. **Three tiers of verification.** Every [MV] claim must specify:
   - **[MV-structural]**: Algebraic identity proved (Jacobi, Cartan matrix, closure)
   - **[MV-arithmetic]**: Dimensional consistency check (norm_num, native_decide)
   - **[MV-definitional]**: Tautological (rfl, or proves a definition equals itself)

2. **Elevate the genuine results.** The 12 real algebraic results deserve prominence.
   They are novel. They are substantive. They should be the focus.

3. **Demote the arithmetic.** Dimensional checks become "consistency checks" in a
   summary table, not individual theorem highlights.

4. **Kill all AI telltale language.** Every identified instance removed.

5. **Match abstract/conclusion claims to actual Lean content.** No scope creep.

6. **Own the gap honestly.** State what dimensional arithmetic proves and what it
   doesn't. A paper that says "we verified the arithmetic skeleton; the algebraic
   structure is partially verified (subalgebra closure, Jacobi) and partially
   cited from the literature" is honest and publishable.

### Priority Order

1. Paper 2 (AACA) — smallest delta, already submitted, demonstrates we heard feedback
2. Paper 1 (CICM) — already submitted, conclusion needs scoping back
3. Paper 4 (LMP) — needs significant rewrite, not yet submitted
4. Paper 3 (PRD) — most work needed, not yet submitted

## Consequences

### Positive
- Papers become honest and defensible
- Genuine contributions get proper emphasis instead of drowning in tautologies
- Methodology becomes credible for future ITP work on physics
- If Wilson (or any reviewer) reads the Lean files, claims match what they find

### Negative
- Papers shrink in apparent scope
- "First formally verified GUT" claim must be softened to "first arithmetic
  skeleton of a GUT checked by a theorem prover"
- Submitted papers may need errata or withdrawal if reviews come back negative

### What We Learned

The journey from ADR-001 (honest reframing of inflated documentation) through
ADR-002 (candidate theory construction with gates) to ADR-003 (prose-proof
coherence crisis) follows a pattern: each time we found a new layer of inflation
and stripped it away.

- **ADR-001**: "EXTRAORDINARY SUCCESS" for basic arithmetic → honest methodology framing
- **ADR-002**: candidate physics with gate controls → honest Track D
- **ADR-003**: arithmetic presented as algebraic proof → honest three-tier classification

The lesson is recursive: honesty requires ongoing audit, not a one-time fix.
The AI-assisted writing process systematically inflates because the AI has no
ground-truth access to what the Lean proofs actually prove — it generates
confident prose that sounds right but exceeds the evidence. Human review of
AI-generated academic prose must specifically check that every claim maps to
a specific theorem, and that the prose does not assert more than the theorem
statement contains.

## Timeline

| Date | Event |
|------|-------|
| 2026-02-XX | ADR-001: Honest reframing of original project |
| 2026-03-XX | ADR-002: Candidate theory construction with gates |
| 2026-03-07 | Paper 1 submitted to CICM 2026 |
| 2026-03-XX | Paper 2 submitted to AACA |
| 2026-03-12 | Wilson Email 1: substantive feedback, D₈, SU(9) interest |
| 2026-03-12 | Wilson Email 2: "I can't understand your papers" — withdrawal |
| 2026-03-12 | Built paper-integrity-auditor agent |
| 2026-03-12 | Ran parallel audit on all four papers |
| 2026-03-12 | ADR-003: This decision — prose-proof coherence crisis |
| 2026-03-12 | Begin paper restructuring (Paper 2 first) |
