# Paper 4 Integrity Audit Report
## "Three Fermion Generations from E₈: A Machine-Verified Impossibility and Resolution"
## Target: Letters in Mathematical Physics

**Audit Date**: 2026-03-12
**Part of**: ADR-003 (Prose-Proof Coherence Crisis)
**Status**: FIXES PENDING

---

## SEVERITY SUMMARY

### ACCURATE: 26 claims
The dimensional arithmetic claims are consistently accurate. The claim tagging
system ([MV]/[CO]/[CP]/[SP]/[OP]) is used and mostly correctly applied within
the Discussion section.

### OVERCLAIMED: 11 claims
1. Abstract: "first machine-verified resolution" — arithmetic is verified, not the resolution
2. Abstract: branching rule cited as [MV] when only dimension check is [MV]
3. Abstract: "no intrinsic mechanism" from arithmetic proving 2^k != 3
4. Abstract: "coexist...connected through SU(7)xU(1)" when theorem proves 49+21+21=91
5. Intro: "universal impossibility" requires [SP] premise
6. Intro: "first machine-verified three-generation resolution"
7. Line 147-149: "immediately implies" physics from arithmetic
8. Line 153-158: orbit-stabilizer claim tagged [MV] when theorem is arithmetic
9. Line 179-182: "definitive" physical consequence
10. Line 436-438: "housing exactly SU(3)+U(1)" from 8+1=9
11. Conclusion: "We have proved...universal impossibility...E₈ resolves"

**Common pattern**: Paper systematically presents dimensional arithmetic as if it
verifies representation-theoretic and physics claims.

### TAUTOLOGICAL: 2 claims
1. Abstract: "dim(fund. SU(3)) = 3" backed by `(3:N) = 3 := rfl`
2. Line 303: same, as part 8 of `e8_three_generation_theorem`

### SCOPE BLUR: 4 claims
1. Abstract: "contain exactly three SM generations" tagged [MV] when SM identification is [CP]
2. Intro: "provides exactly three generations" tagged [MV]
3. Lines 388-392: chirality index 35-21=14 tagged [MV] when root classification is [CO]
4. Conclusion: Definition D tagged [MV] when it depends on [CO] root counting

### AI TELLTALE: 4 instances
1. "miraculous" (line 423, in scare quotes but still signals AI)
2. "crucially" (line 288)
3. Title: "Machine-Verified Impossibility and Resolution" — dramatic framing
4. Systematic arithmetic-as-physics overclaiming pattern itself is an AI telltale

## OVERALL ASSESSMENT

Paper 4 is the **best-written of the four** in terms of honest claim tagging. The
Discussion section correctly uses all five tag types. The chirality boundary
analysis is honest about what is open.

However, the paper suffers from a **systematic overclaim pattern**: dimensional
arithmetic is consistently presented as "proving" or "resolving" physics questions.
A mathematician reading the Lean files sees `norm_num`, `omega`, `native_decide`
everywhere — computer-checked arithmetic, not deep structural results.

**The arithmetic is right, and the methodology is genuinely novel. The paper would
be stronger if it claimed less.**

## RECOMMENDED FIXES

### Critical
1. Add clear introductory statement distinguishing arithmetic from representation theory
2. Tag [SP] and [CP] in abstract explicitly
3. "Resolution" → "dimensional consistency of a known resolution"
4. Consider retitling to not overclaim

### Important
5. Remove "miraculous"
6. Clarify chirality index scope: [CO] root counting vs [MV] arithmetic
7. Fix "The number 3 is not put in by hand" — it literally is `(3:N) = 3 := rfl`
