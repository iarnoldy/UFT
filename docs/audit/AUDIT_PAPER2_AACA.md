# Paper 2 Integrity Audit Report
## "Character Decomposition from Fortescue to Cartan--Weyl"
## Target: AACA (Advances in Applied Clifford Algebras)

**Audit Date**: 2026-03-12
**Part of**: ADR-003 (Prose-Proof Coherence Crisis)
**Status**: FIXES APPLIED (2026-03-12)

---

## SEVERITY SUMMARY

### ACCURATE: 35+ claims
The vast majority of claims are accurate. The paper is generally well-calibrated,
with honest Limitations and Discussion sections.

### OVERCLAIMED: 4 claims
1. **Abstract line 119-121**: "grade-2 elements of Cl(n,0)" — proved only for Cl(3,0)
2. **Abstract line 131-133**: "We further prove...block-tridiagonal form" — the Hamiltonian conclusion is pen-and-paper, not Lean
3. **Section 9, line 1048-1051**: "All concrete algebraic results...are machine-verified" — the so(14) Casimir table and block-tridiagonal theorem are not
4. **Conclusion line 1287-1291**: "Clifford grade selection rules force operators built from so(n) generators" — proved for Cl(3,0), stated for so(n)

### TAUTOLOGICAL: 5 claims
1. `su3_dimension`: `3^2 - 1 = 8` by norm_num
2. `cartan_weyl_decomposition`: `2 + 6 = 8` by norm_num
3. `fortescue_decomposition`: `2 + 3 + 3 = 8` by norm_num
4. `bracket_count`: `Nat.choose 8 2 = 28` by native_decide
5. `cartan_matrix_determinant`: `2*2 - (-1)*(-1) = 3` by norm_num

Note: These tautologies are LESS harmful in this paper than in others, because the
paper does not over-sell them. They appear alongside the substantive root eigenvalue theorems.

### UNSUPPORTED: 1 claim
1. **Line 714**: "c2(fund) = (n-1)/2 = 13/2, verified in Lean 4" for so(14) — no such Lean proof exists

### SCOPE BLUR: 2 claims
1. **Abstract lines 125-126**: "We prove" the Peter-Weyl generalization — this is a pen-and-paper argument, not Lean
2. **Lines 997-1004**: Theorem 8.2 (block-tridiagonal) presented in theorem environment alongside machine-verified theorems

### AI TELLTALE: 2 instances
1. **Line 892**: "This section contains the most novel algebraic result of the paper"
2. **Line 378**: "This is not merely a restatement. It has a concrete consequence"

## OVERALL ASSESSMENT

Paper 2 is **significantly better** than one would expect from Wilson's critique.
The identity/analogy taxonomy is well-executed. The Limitations section correctly
identifies exactly the gaps this audit found. The prose is restrained. The main
problems are scope creep in the abstract and conclusion.

## FIXES APPLIED (2026-03-12)

1. Abstract: qualified from Cl(n,0)/so(n) to Cl(3,0)/so(3), "We prove" → "We show"
2. Line 378: "This is not merely a restatement" → "The generalization has a concrete consequence"
3. Line 548: Removed `bracket_count` reference, changed to "All 28 independent brackets are verified individually"
4. Line 714: "verified in Lean 4" → "computed by the standard formula"
5. Line 892: Deleted "This section contains the most novel algebraic result of the paper"
6. Section 9: "All concrete algebraic results" → "All concrete computations for Cl(3,0), so(3), and su(3)"
7. Theorem 8.2: Added "(Proved by standard mathematical argument; not machine-verified.)"
8. Conclusion: Qualified from so(n) to Cl(3,0)/so(3) with generalization note
