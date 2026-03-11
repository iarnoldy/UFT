# Chirality in E8: Literature Synthesis

**Date**: 2026-03-11
**Sources**: Two polymathic researcher agents (15+ web searches, 8+ papers fetched each)
**Status**: COMPLETE

## Executive Summary

The D-G theorem (2010) proves no chiral fermions from the E8 adjoint under the standard
massless/complexified definition. Three escape routes exist in the literature; we add a fourth.

## Key Papers Found

### Wilson's Papers (the primary challenger)
1. **arXiv:2210.06029** (Oct 2022) — "Chirality in an E8 model" — DIRECT response to D-G
   - Quaternionic tensor products are "automatically chiral"
   - D-G's complexification "destroys" chirality
   - **Claims chirality REQUIRES exactly 3 generations**

2. **arXiv:2407.18279** (Jul 2024) — "Uniqueness of an E8 model"
   - Type 5 element with centralizer SU(9)/Z3 is "only viable" for 3 generations
   - **"Since Lambda^3(C^9) != Lambda^3(C^9)*, the theory is chiral"**
   - This is OUR mechanism. Wilson endorses it explicitly.

3. **arXiv:2507.16517** (Jul 2025) — "Embeddings of the Standard Model in E8" (THE SYNTHESIS)
   - SM entirely in so(7,3) subalgebra
   - Chain: E8(-24) > Spin(12,4) > Spin(7,3) > su(3,1)
   - "A counterexample to the claimed 'theorem' of Distler and Garibaldi"
   - Computes mixing angles: sin^2(phi/2) ~ 0.22265
   - **Notably AVOIDS the word "chirality"** — relies on structural separation

### Nesti-Percacci / GraviGUT
- **arXiv:0909.4537** (2009) — Chirality from Majorana-Weyl spinor of SO(3,11)
  - Gets ONE chiral family (16 of SO(10)) but not three
  - EVADES D-G because fermions in spinor rep, not adjoint
  - Compatible with E8(-24) via Spin(3,11) subset Spin(12,4) subset E8(-24)

### Alexander-Smolin-Marciano / Graviweak
- **arXiv:1212.5246** (2012) — Chirality from self-dual/anti-self-dual SO(3,1) connection
- **arXiv:2505.17935** (May 2025) — SSB extends the graviweak mechanism

### Singh / Jordan Algebra
- **arXiv:2508.10131** (2025) — Three generations from J3(O_C) eigenvalues
  - Independent route, complementary to E8

## What D-G Actually Proves (Precise Scope)

**What people think**: "No chiral fermions from E8, period."

**What it actually proves**: If you embed SL(2,C) x G inside any real form of E8 and
decompose the adjoint 248 into Weyl spinors of SL(2,C) tensored with representations
of G, then the G-representation is always self-conjugate.

**Gaps**:
1. Assumes fermions in adjoint 248 (Nesti-Percacci puts them in spinor)
2. Assumes complexified chirality definition (Wilson attacks this)
3. Assumes single SL(2,C) embedding (Wilson argues for multiple via triality)
4. Does NOT say Lambda^3(C^9) is non-chiral — Lambda^3(C^9) IS complex

## Our Contribution: Route D (Composite Z3 x Z2 Chirality)

**A8/D8 Overlap Matrix** (computed in e8_chirality_trident.py):
```
Z3 sector              | D8 adj | D7 S+ | D7 S- | Total
Sector 0 (SU(9) adj)   | 56     | 8      | 8      | 72
Sector 1 (84)          | 28     | 35     | 21     | 84
Sector 2 (84-bar)      | 28     | 21     | 35     | 84
Total                   | 112    | 64     | 64     | 240
```

- **84 is chirally ASYMMETRIC**: 35 S+ vs 21 S- (14-root excess)
- **84-bar is conjugate**: 21 S+ vs 35 S- (mirror asymmetry)
- **Total 248 is balanced**: 64 = 64 (D-G satisfied)
- **Physical interpretation**: J separates matter from antimatter (Z3);
  Gamma_14 provides chirality within each sector (Z2). The COMPOSITE
  Z3 x Z2 = Z6 grading is the full chirality structure.

## The Cleanest Argument

Lambda^3(C^9) is a COMPLEX representation of SU(9). It is NOT self-conjugate:
84 != 84-bar (they have different Z3 charges). This satisfies D-G's OWN definition
of chirality at the SU(9) level. The question is whether D-G's framework applies
at this level (they analyze the adjoint decomposition, not the SU(9) decomposition).

Wilson's blog (July 2024) makes this argument explicitly:
"Since [Lambda^3(C^9)] is not the same as the antisymmetric cube of 9*,
the theory is chiral."

Our overlap matrix QUANTIFIES this: the 84's chiral asymmetry is 35:21 = 5:3.

## Wilson's Most Striking Claim

"Chirality of weak interactions can only work with exactly three generations."

If true: chirality and three generations are LOGICALLY EQUIVALENT.
This would explain both "why 3?" AND "why chiral?" simultaneously.
[SP] — speculative, not verified.

## Confidence Calibration

| Claim | Confidence |
|-------|------------|
| D-G theorem mathematically correct within stated assumptions | 95% |
| D-G assumptions narrower than commonly understood | 85% |
| Lambda^3(C^9) != Lambda^3(C^9)* provides chirality | 75% |
| Our overlap matrix is correct (Dynkin coefficient method) | 99% |
| The 35:21 asymmetry has physical chirality meaning | 55% |
| Wilson's quaternionic chirality definition captures physics | 40% |
| Chirality problem solvable within 5 years | 35% |

## Recommended Next Steps

1. **Formalize Lambda^3(C^9) non-self-conjugacy in Lean** — cleanest contribution
2. **Read Wilson 2210.06029 in full** — the chirality paper
3. **Contact Wilson** — he uses our exact mechanism (type 5 / SU(9)/Z3)
4. **For Paper 4**: State Lambda^3(C^9) is complex, cite Wilson's argument,
   note D-G applies at adjoint level not SU(9) level, present overlap matrix

## Bug Found

wilson_e8_type5.py used torus coordinates t5=(1,1,1,1,1,0,0,0) which gives
WRONG Z3 classification (120+64+64 not 80+84+84). Fixed using Dynkin coefficient
of branch node (alpha_2 in Bourbaki E8) mod 3. Dimensional results were correct
from abstract rep theory; root-level classifications were wrong.

## References

See full citation lists in polymathic researcher outputs.
Key: Distler-Garibaldi 0905.2658, Wilson 2210.06029 / 2407.18279 / 2507.16517,
Nesti-Percacci 0909.4537, Alexander-Marciano-Smolin 1212.5246.
