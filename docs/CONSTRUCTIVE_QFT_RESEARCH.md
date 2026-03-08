# Constructive QFT Bridge Research: Polymathic Researcher Report

**Date**: 2026-03-08
**Agent**: polymathic-researcher
**Status**: COMPLETE — five threads investigated with web research

---

## Executive Summary

The mass gap sits at the intersection of five active research programs, none of
which has reached 4D Yang-Mills. The most promising threads are stochastic
quantization (proven in 3D, blocked at 4D by criticality) and the Balaban
constructive program (UV control proven with IR cutoff, continuum limit unfinished).
No one has used Clifford grade structure as a UV regulator. Our Cl(14,0) scaffold
is mathematically interesting but sits in a different category than these programs.
Honest assessment: bridging finite-dimensional Clifford algebra to infinite-dimensional
QFT spectral gaps requires either a fundamentally new idea or a non-obvious connection.

---

## Thread A: Connes' NCG + Spectral Action

**Key people**: Connes, Chamseddine, van Suijlekom, Boyle, Farnsworth

**State of the art**: Spectral action recovers SM + GR at classical level. One-loop
corrections are renormalizable. Random NCG path-integral quantization is in infancy.
No spectral action for SO(10) or SO(14) has been published. The spectral action
does NOT produce a mass gap — it gives the classical action functional only.

**Devastating finding**: Azzurli et al. (2019) showed that Clifford scalar fields
from the finite spectral triple do NOT achieve gauge coupling unification. Out of
twenty mass-hierarchy configurations, zero lead to unification.

**Confidence that NCG produces mass gap**: 5%

---

## Thread B: Algebraic QFT + Split Property

**Key people**: Haag, Kastler, Buchholz, Wichmann, Longo

**CRITICAL CORRECTION**: The implication runs:
  MASS GAP → NUCLEARITY → SPLIT PROPERTY
NOT the reverse. Split property is a CONSEQUENCE of mass gap, not a CAUSE.

The AQFT framework tells you what a theory with a mass gap LOOKS LIKE, but
it does not CONSTRUCT such theories.

**Confidence that AQFT produces mass gap**: 5%

---

## Thread C: Stochastic Quantization (MOST ACTIVE FRONTIER)

**Key people**: Chandra, Chevyrev, Hairer, Shen, Cao, Chatterjee

**This is the most technically active thread (2024-2026).**

Key results:
- 2D: CCHS defined stochastic YM heat flow, gauge-covariant renormalization (IHES 2022)
- 3D with Higgs: Local solutions + unique renormalization counterterms (Inventiones 2024)
- 3D state space: Cao-Chatterjee defined Euclidean YM as random distributional gauge orbits (CMP 2024)
- Chatterjee proved: strong mass gap implies quark confinement (2025)

**The 4D wall**: Regularity structures require subcriticality (d < 4). Yang-Mills
in 4D is CRITICAL (d = 4). The entire framework breaks down. A fundamentally new
idea is needed.

**Critical connection**: In stochastic quantization, the Fokker-Planck generator's
spectral gap IS the mass gap. This is the most direct route.

**Confidence for 3D by 2035**: 50%
**Confidence for 4D with current methods**: 5%

---

## Thread D: Balaban Program

**Key people**: Balaban, Magnen, Rivasseau, Seneor, Dimock, Jaffe

Balaban showed UV control for lattice YM4 via block-spin RG (1980s-90s).
Magnen-Rivasseau-Seneor constructed Schwinger functions for SU(2) YM4 with
IR cutoff (1993). Dimock wrote expository reconstruction (2011-2013).

**Unfinished**: Removing IR cutoff, proving mass gap, verifying OS axioms.
**No one is actively continuing Balaban's exact program as of 2024-2026.**

Several claimed mass gap proofs on arXiv/SSRN (2024-2026) — none accepted by
Clay Institute. Probability any claimed proof is correct: < 2%.

**Confidence Balaban leads to proof by 2035**: 15%

---

## Thread E: Clifford Algebras as UV Regulators

**THIS IS GENUINELY UNEXPLORED TERRITORY.**

**Zero results found for "grade filtration renormalization group".**

What exists:
- Freed-Hopkins classify gapped topological phases using Clifford algebras + K-theory
  (ten-fold way). But this is for FREE systems only.
- Atiyah-Singer connects Dirac spectrum to topological invariants
- Bott periodicity has not been connected to multiscale RG analysis

Arguments FOR potential:
1. Grade filtration gives natural finite-dimensional approximation hierarchy
2. Bott periodicity gives recursive/self-similar structure matching RG self-similarity
3. Freed-Hopkins shows Clifford structure DOES control gapped vs gapless (in free systems)

Arguments AGAINST:
1. UV divergences come from infinite field algebra, not finite structure group
2. Grade filtration is algebraic, UV control requires analytic estimates
3. Freed-Hopkins classification is for free/non-interacting systems

**Confidence this leads to mass gap**: 3-5% directly, 10-15% via non-obvious connection

---

## Scenario Analysis: If Proved by 2035

| Route | Probability |
|-------|------------|
| Stochastic quantization breakthrough for d=4 | 40% |
| Lattice + probability hybrid (Chatterjee-Cao) | 25% |
| Something we haven't thought of | 15% |
| Completed Balaban program | 10% |
| NCG spectral action + new quantization | 5% |
| Clifford algebraic constraint | 3% |
| Remains unproved | ~50% |

---

## Recommended Next Steps

1. **Highest value, lowest risk**: Formalize Freed-Hopkins ten-fold classification in
   Lean 4. Tractable mathematics, publishable regardless of mass gap relevance.

2. **Highest value, moderate risk**: Investigate whether grade filtration defines
   natural lattice approximation for gauge fields. Check if truncation preserves
   gauge covariance. If yes: genuinely new UV regulator.

3. **Track the frontier**: Follow Chevyrev-Shen and Cao-Chatterjee closely.

4. **Speculative paper**: Write modularity bridge paper connecting Clifford grade
   structure to modular nuclearity bounds.

5. **DO NOT claim mass gap relevance for current scaffold.** The algebraic tower
   is honest and verified. Overclaiming damages credibility. Track A (methodology),
   not mass gap.

---

## Sources

### Thread A
- Chamseddine-Connes, The Spectral Action Principle (1996)
- Azzurli et al., Clifford-based spectral action and RG analysis (2019)
- Van Suijlekom, NCG and Particle Physics, 2nd ed. (2024)

### Thread B
- Buchholz-Wichmann, Nuclearity condition
- Marrakchi, Spectral gap characterization of full Type III factors (2016)

### Thread C
- Chandra-Chevyrev-Hairer-Shen, Stochastic quantisation YMH 3D (Inventiones 2024)
- Cao-Chatterjee, State Space for 3D Euclidean YM (CMP 2024)
- Chatterjee, Harvard Millennium Lecture (Oct 2025)

### Thread D
- Jaffe-Witten, Clay problem statement (2000)
- Dimock, The RG According to Balaban I-III (2011-2013)

### Thread E
- Freed-Hopkins, K-theory classification of topological phases
- Gudder, Geometric Algebras and Fermion QFT (2025)
