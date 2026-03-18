# Round 2: ARCHAEOLOGY -- Geometric Mixing Angles from E8

**Agent:** Polymathic Researcher
**Date:** 2026-03-17
**Investigation:** e8-mixing-angles (Real Run)
**Status:** Complete

---

## 0. Scope

This round investigates exactly the two questions identified by Round 1 (VISION):

1. **SU(9) CG Factorization** -- do the Clebsch-Gordan coefficients of the
   SU(9) Yukawa coupling (84 x 84* -> 80) factorize under SU(5) x SU(4)?
2. **Wilson's Group Algebra -- Mathematical Status** -- what is the
   peer-reviewed, independently-verified status of Wilson's mixing angle
   program?

No other topics are investigated. Discrete flavor models (A4, S4, etc.) are
excluded per Round 1 directive (97% closed).

---

## Question 1: SU(9) CG Factorization

### 1.1 The Racah Factorization Lemma (Key Mathematical Framework)

The central mathematical tool is the **Racah factorization lemma**, which
governs how Clebsch-Gordan coefficients of a group G decompose when
restricted to a subgroup H.

**Statement (general form).** For a group chain G ⊃ H, the CG coefficients
of G decompose as:

    CG(G; alpha, beta -> gamma) = sum_delta ISF(G/H; alpha, beta, gamma, delta) * CG(H; alpha_H, beta_H -> gamma_H)

where:
- CG(G) are the Clebsch-Gordan coefficients of G
- CG(H) are the Clebsch-Gordan coefficients of the subgroup H
- ISF(G/H) are the **isoscalar factors** -- the part that does NOT
  factorize into pure subgroup CG coefficients
- delta is a **multiplicity label** that runs over repeated occurrences
  of the same H-irrep in the branching

**The critical point:** The CG coefficients of G do NOT in general
factorize as a simple product CG(H1) x CG(H2) when H = H1 x H2 is a
product subgroup. The isoscalar factors carry the non-factorizable part.
The question "does the coupling factorize?" is precisely the question
"are the isoscalar factors trivial (all equal to 1 or proportional to
delta functions)?"

### 1.2 The Chen Theorem (1981) -- A Structural Surprise

**Paper:** Jin-Quan Chen, "SU(mn) ⊇ SU(m) x SU(n) isoscalar factors and
S(f1+f2) ⊇ S(f1) x S(f2) isoscalar factors," J. Math. Phys. 22, 1-6 (1981).
DOI: 10.1063/1.524735

**Main theorem.** For the subgroup chain SU(mn) ⊃ SU(m) x SU(n):

1. The SU(mn) ⊃ SU(m) x SU(n) isoscalar factors are EQUAL to the
   corresponding S(f1+f2) ⊃ S(f1) x S(f2) isoscalar factors of the
   symmetric (permutation) group.

2. These isoscalar factors are **independent of m and n**. They depend
   only on the Young diagram labels (partition shapes), not on the
   specific values of m and n in SU(mn).

**What this means for our problem (SU(9) ⊃ SU(5) x SU(4)):**

The isoscalar factors for SU(9) ⊃ SU(5) x SU(4) are identical to
those for SU(mn) ⊃ SU(m) x SU(n) for ANY m >= 5 and n >= 4 (provided
the representations exist). They are determined entirely by the
symmetric group S(f1+f2) ⊃ S(f1) x S(f2).

This is a powerful structural constraint, but it does NOT answer our
specific question. The theorem tells us that the isoscalar factors are
universal (independent of m, n), but it does NOT tell us whether they
are trivial (equal to 1) or non-trivial for the specific representations
in our coupling 84 x 84* -> 80.

### 1.3 The Outer Multiplicity Problem

**Paper:** J.P. Draayer et al., "Complementary group resolution of the
SU(n) outer multiplicity problem," multiple publications (1990s-2000s).
Repository: LSU Physics.

The **outer multiplicity problem** is precisely the question of when
the tensor product decomposition SU(n) x SU(n) -> SU(n) has
multiplicities > 1 (i.e., when the same irrep appears more than once
in the decomposition). When multiplicities exceed 1, the isoscalar
factors are non-trivial matrices, not scalars.

**Key result:** The decomposition SU(n) x SU(n) -> SU(n) is **NOT
multiplicity-free** in general. Multiple occurrences of irreps require
additional labels (from a complementary group U(2n-2)) to distinguish
them.

**For our specific case:** We need to check whether the coupling
84 x 84* -> 80 in SU(9) has outer multiplicity. The M8.1 computation
already established that the adjoint 80 appears with **multiplicity 1**
in the decomposition 84 x 84* = 5760 + 1215 + 80 + 1. This means:

- **There is no outer multiplicity problem for this specific coupling.**
- By Schur's lemma, the intertwining map 84 x 84* -> 80 is unique
  up to an overall scalar.
- The CG coefficients for this coupling are unique (no free phases
  or multiplicity labels).

### 1.4 What M8.1 Already Established

The experiment `src/experiments/su9_yukawa_cg.py` (results in
`src/experiments/results/su9_cg_coefficients.json`) established:

**Branching 84 under SU(5) x SU(4):**
- (10, 1): dim 10
- (10, 4): dim 40
- (5, 6): dim 30
- (1, 4-bar): dim 4
- Total: 84. Check.

**Branching 80 (adjoint) under SU(5) x SU(4):**
- (24, 1): SU(5) adjoint, dim 24
- (1, 15): SU(4) adjoint, dim 15
- (5, 4-bar): bifundamental, dim 20
- (5-bar, 4): conjugate bifundamental, dim 20
- (1, 1): relative U(1), dim 1
- Total: 80. Check.

**Factorization channels for 84 x 84* -> 80:**
- Channel 1 (diagonal): (10,4) x (10-bar,4-bar) -> (1,1).
  SU(5): 10 x 10-bar -> 1. SU(4): 4 x 4-bar -> 1. **Factorizes.**
- Channel 2 (cross): (10,4) x (5-bar,6) -> (5-bar,4).
  Needs explicit CG. **Status: depends on CG details.**
- Channel 3 (cross): (5,6) x (10-bar,4-bar) -> (5,4-bar).
  Needs explicit CG. **Status: depends on CG details.**

**M8.1 conclusion:** "Outcome C (underdetermined survival): the framework
has free parameters and makes no unique prediction."

### 1.5 The Precise Mathematical Question (Sharpened)

The question from Round 1 was: "Do the SU(9) CG coefficients factorize
as CG(SU(5)) x CG(SU(4))?"

After archaeology, this question decomposes into three sub-questions:

**(A) Does the overall 84 x 84* -> 80 coupling factorize?**

YES, trivially. The adjoint appears with multiplicity 1 (M8.1 result).
By Schur's lemma, the coupling is unique up to a scalar. There is nothing
to "not factorize" at the level of the full SU(9) coupling.

**(B) When we decompose under SU(5) x SU(4), do different SU(5) sectors
contribute with different relative weights?**

This is the actual question. The coupling 84 x 84* -> 80, when
restricted to SU(5) x SU(4), branches into multiple channels. The
RELATIVE coupling strengths between channels (e.g., the ratio of the
(10,4) x (10-bar,4-bar) -> (24,1) channel to the (5,6) x (5-bar,6) ->
(24,1) channel) are fixed by the isoscalar factors.

By Chen's theorem, these isoscalar factors are determined by the
symmetric group and are universal. They are NOT in general equal to 1.

**(C) Do the non-trivial isoscalar factors produce a non-trivial
Yukawa texture in generation space?**

This requires understanding what "generation space" means in terms of
the SU(4) representations. The SU(4) contains the family SU(3) as a
subgroup (SU(4) ⊃ SU(3) x U(1)). The generation structure lives in
the SU(3) factor. The question becomes: do the SU(4) representations
{1, 4, 6, 4-bar} decompose under SU(3) in a way that couples
differently to different generations?

Under SU(4) ⊃ SU(3) x U(1):
- 4 = 3 + 1 (three generations + one singlet)
- 6 = 3 + 3-bar (three + three-bar)
- 15 = 8 + 3 + 3-bar + 1

The three generations sit in the **3** of SU(3) inside SU(4).
The coupling of 4 x 4-bar -> 1 in SU(4) is just the trace, which is
democratic (treats all generations equally). The coupling of 4 x 6 -> 4
involves a nontrivial CG coefficient of SU(4).

**Verdict on Question (C):** The democratic coupling (identity in
generation space) occurs in the diagonal channels. The cross channels
DO involve non-trivial SU(4) CG coefficients that mix the 3 of SU(3)
with the extra singlet from SU(4) ⊃ SU(3) x U(1). However, this
mixing is between generations and a U(1) direction -- it does NOT
produce off-diagonal entries in the 3x3 generation Yukawa matrix.
It produces a RANK structure (one coupling to the U(1) direction is
different), which after SU(3)-breaking gives a mass hierarchy but
NOT mixing angles.

### 1.6 Kill Condition KC-M5 Assessment

**KC-M5: SU(9) CG coefficients factorize completely under SU(5) x SU(4).**

**Verdict: KC-M5 FIRES with a nuanced conclusion.**

The factorization is not complete in the naive sense -- the isoscalar
factors are non-trivial (Chen's theorem says they are given by symmetric
group ISFs, which are not all 1). However, the non-trivial part does
NOT produce generation mixing. It produces:

1. **Different coupling strengths for different SU(5) sectors** (10 vs
   5-bar vs 1), which gives Yukawa hierarchy (mass ratios) but not
   mixing angles.
2. **A rank structure in the SU(4) sector** (the U(1) in SU(4) ⊃ SU(3)
   x U(1) couples differently), which distinguishes the "fourth family
   direction" from the three generations but does NOT mix generations
   with each other.

**In terms of 3x3 generation mixing: the coupling IS proportional to
the identity matrix in generation space.** The SU(3) symmetry within
SU(4) forces all three generations to couple identically. The non-trivial
isoscalar factors act on the SU(5) sector labels and the U(1) direction,
not on the generation indices.

**KC-M5 fires FATAL for generation mixing from CG coefficients alone.**
The SU(9) Yukawa coupling 84 x 84* -> 80, decomposed under SU(5) x SU(4),
produces a Yukawa matrix that is proportional to delta_{ij} in generation
space (i,j = 1,2,3). Generation mixing requires SU(3)_family breaking,
which is a dynamical (flavon) effect, not a kinematical (CG coefficient)
effect.

### 1.7 What Survives After KC-M5

The E8 representation theory still provides:
- **The existence of three generations** (from Z3 eigenspaces in 248)
- **The particle content per generation** (from SU(5) x SU(4) branching)
- **The Yukawa coupling structure** (84 x 84* -> 80, unique by Schur)
- **Mass hierarchy possibility** (different SU(5) sectors have different
  coupling strengths, via non-trivial isoscalar factors)

What it does NOT provide:
- **Generation mixing angles** (the 3x3 matrix is proportional to identity)
- **CP-violating phases** (requires complex flavon VEVs)
- **Mass values** (requires dynamical symmetry breaking)

### 1.8 Literature for Question 1

| Reference | Year | Relevance | What it says |
|-----------|------|-----------|--------------|
| Chen, J. Math. Phys. 22, 1 (1981) | 1981 | CRITICAL | SU(mn) ⊃ SU(m) x SU(n) ISFs = permutation group ISFs, independent of m,n |
| Slansky, Phys. Rep. 79, 1 (1981) | 1981 | HIGH | Tables of branching rules for GUT groups. Does NOT tabulate SU(9) explicitly; covers up to SU(8) and E-series |
| De Swart, Rev. Mod. Phys. 35, 916 (1963) | 1963 | FOUNDATIONAL | SU(3) isoscalar factors: defined the concept, computed tables |
| Alex et al., J. Math. Phys. 52, 023507 (2011) | 2011 | MEDIUM | Algorithm for SU(N) CG coefficients via Gelfand-Tsetlin patterns. Could compute SU(9) CG numerically |
| Draayer et al., LSU (1990s) | 1990s | MEDIUM | Outer multiplicity problem: resolved by complementary group U(2n-2). Confirms non-multiplicity-free decompositions exist |
| Berenstein-Zelevinsky, J. Alg. Comb. (1992) | 1992 | LOW | Triple multiplicities for sl(r+1) in exterior algebra of adjoint. Relevant to Lambda^k decomposition |

**Papers NOT found:**
- No paper computing SU(9) CG coefficients explicitly for 84 x 84* -> 80
- No paper on SU(9) ⊃ SU(5) x SU(4) isoscalar factors for exterior powers
- No paper addressing whether E8 Yukawa CG produces generation mixing

This computation appears to be novel. The M8.1 experiment was the first
to address it directly.

---

## Question 2: Wilson's Group Algebra -- Mathematical Status

### 2.1 Publication and Citation Record

**Robert Arnott Wilson** -- Professor of Group Theory, Queen Mary University
of London. Author of the ATLAS of Finite Groups. World-class finite group
theorist; not a physicist by training.

**Publication status of physics papers:**

| Paper | arXiv | Year | Venue | Status | Citations |
|-------|-------|------|-------|--------|-----------|
| Octions (with Manogue, Dray) | 2204.05310 | 2022 | J. Math. Phys. 63, 081703 | PUBLISHED | ~10-15 |
| Chirality in E8 | 2210.06029 | 2022 | physics.gen-ph | PREPRINT ONLY | Few |
| Tetrions | 2301.11727 | 2023 | physics.gen-ph | PREPRINT ONLY | Few |
| Group-theorist's perspective | 2009.14613 | 2020 | physics.gen-ph | PREPRINT ONLY | ~5 |
| Finite symmetry groups | 2102.02817 | 2021 | physics.gen-ph | PREPRINT ONLY | 11 (INSPIRE) |
| Uniqueness of E8 model | 2407.18279 | 2024 | physics.gen-ph | PREPRINT ONLY | Few |
| Embeddings of SM in E8 | 2507.16517 | 2025 | physics.gen-ph | PREPRINT ONLY | ~0 (recent) |

**Key observation:** Only ONE of Wilson's physics papers is published in
a peer-reviewed journal (the co-authored Octions paper in J. Math. Phys.).
All solo physics papers are on physics.gen-ph, the arXiv category with the
lowest scrutiny. The mixing angle calculations appear only in the unpublished
preprints.

**Total citations across all physics papers: approximately 20-30.**
No citations from mainstream particle physics groups. No responses,
corrections, or criticisms in the published literature.

### 2.2 Independent Reproduction of Wilson's Formulas

I have independently computed all of Wilson's mixing angle predictions
using PDG 2024 values. Results:

**Mass equation: m_e + m_mu + m_tau + 3*m_p = 5*m_n**

| Quantity | Value (MeV) |
|----------|-------------|
| LHS = m_e + m_mu + m_tau + 3*m_p | 4697.8456 |
| RHS = 5*m_n | 4697.8271 |
| Difference | 0.0185 MeV = 18.5 keV |
| Relative precision | 3.95 ppm |
| As tau prediction | 0.15 sigma |

For comparison, the Koide formula predicts m_tau with 61.4 ppm precision
(0.91 sigma). Wilson's mass equation is **6x more precise than Koide.**

**Mixing angle formulas (all independently verified):**

| Parameter | Wilson formula | Wilson value | Experimental | Deviation |
|-----------|--------------|-------------|-------------|-----------|
| sin^2(theta_W) | 1/2 - 1/sqrt(13) | 0.22265 | 0.22290 +/- 0.00030 | 0.83 sigma |
| theta_12 (PMNS) | cos(60-t)/cos(t) = (m_tau-m_e)/(m_tau-m_mu) | 33.024 deg | 33.41 +/- 0.75 | 0.51 sigma |
| delta_CP (CKM) | arctan((m_n-m_p)/m_e) | 68.44 deg | 68.8 +/- 4.5 | 0.08 sigma |
| theta_23 (CKM, V_cb) | arccos((m_p+m_e)/m_n) | 2.338 deg | 2.38 +/- 0.06 | 0.70 sigma |
| theta_C (Cabibbo) | theta_12 - 20 | 13.02 deg | 13.04 +/- 0.05 | 0.40 sigma |
| theta_23 (PMNS) | 50 - 0.815 (complex) | 49.19 deg | 49.1 +/- 1.0 | 0.09 sigma |
| theta_13 (PMNS) | 10 - 1.482 (complex) | 8.518 deg | 8.54 +/- 0.10 | 0.22 sigma |

**All predictions verified numerically. The formulas are reproducible.**

### 2.3 Is the Mass Equation Known?

**The specific equation m_e + m_mu + m_tau + 3*m_p = 5*m_n is NOT known
in the standard literature.** It is not a consequence of any standard
conservation law, symmetry, or known mass relation.

The Koide formula (1981) relates charged lepton masses via
Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = 2/3.
Wilson's equation is structurally different: it mixes leptons and baryons,
involves integer coefficients (1, 1, 1, 3, 5), and is more precise.

**No one other than Wilson has published this relation.** I found no
citations, discussions, or independent discoveries of this equation in
the literature. Wilson discusses it on his blog ("Hidden Assumptions,"
February 2024) and in arXiv:2507.16517.

Wilson claims 4 ppm accuracy. My independent computation confirms
3.95 ppm (consistent within rounding of input masses).

### 2.4 Is theta_12 Known as a Mass-Ratio Formula?

Wilson's theta_12 formula can be written as:

    cos(60 - theta) / cos(theta) = (m_tau - m_e) / (m_tau - m_mu)

This is equivalent to the geometric statement: "project the mass vector
(m_e, m_mu, m_tau) onto the plane perpendicular to (1,1,1) in mass space,
and measure the angle between the projection and the mu-tau edge of the
equilateral triangle formed by the three generation vertices."

**This specific parametrization is NOT known in the standard flavor physics
literature.** The standard approaches to relating theta_12 to mass ratios
involve neutrino masses (not charged lepton masses), because theta_12 is
a PMNS parameter that depends on both the charged lepton and neutrino
mass matrices.

Wilson's formula uses ONLY charged lepton masses to predict a PMNS mixing
angle. This is unusual because standard diagonalization of the PMNS matrix
requires both the charged lepton and neutrino mass matrices. Wilson's
implicit assumption is that the neutrino mass matrix is democratic (proportional
to identity in generation space), so the PMNS mixing comes entirely from
the charged lepton sector.

The closest known parametrization is the **tri-bimaximal mixing** (TBM)
pattern, which gives theta_12 = arcsin(1/sqrt(3)) = 35.26 deg. This is a
discrete symmetry prediction (A4 or S4 group) with zero mass-ratio input.
Wilson's value (33.02 deg) is closer to experiment than TBM.

### 2.5 The CKM CP Phase Formula

Wilson's formula: delta_CP(CKM) = arctan((m_n - m_p) / m_e) = 68.44 deg.

This involves the neutron-proton mass difference (1.2933 MeV), which is a
quantity determined by QCD + QED effects. The experimental CKM CP phase is
68.8 +/- 4.5 deg. The agreement (0.08 sigma) is striking.

**This formula is NOT known in the standard literature.** The CKM CP phase
is normally parametrized via the Wolfenstein parameters (eta, rho) with no
simple mass-ratio expression. Wilson's formula connects the CKM phase to
the nucleon mass splitting, which is a quantity from an entirely different
sector of physics (strong interactions vs. weak mixing).

**No one has independently noted or reproduced this connection.**

### 2.6 Has Anyone Reproduced Wilson's Calculations?

**No.** A thorough search found:
- Zero published responses to Wilson's mixing angle papers
- Zero citations that attempt to reproduce his calculations
- Zero discussions in mainstream physics journals
- A few Physics Forums threads mentioning his work, with skeptical reception
- Wilson's own blog "Hidden Assumptions" as the primary discussion venue

The physics community has effectively ignored Wilson's mixing angle work.
This is likely because:
1. The papers are on physics.gen-ph (low visibility)
2. Wilson is a mathematician, not a physicist (credibility gap)
3. The approach (mass ratios -> angles) looks like numerology without a
   theoretical derivation
4. The 20-degree Cabibbo subtraction is explicitly conjectural

### 2.7 The Critical Assessment

**What Wilson gets right:**
- The mass equation m_e + m_mu + m_tau + 3*m_p = 5*m_n (3.95 ppm, 0.15 sigma)
- The CKM CP phase arctan((m_n-m_p)/m_e) = 68.44 deg (0.08 sigma)
- The PMNS theta_12 from mass-plane geometry = 33.02 deg (0.51 sigma)
- The CKM V_cb = arccos((m_p+m_e)/m_n) = 2.338 deg (0.70 sigma)
- The Weinberg angle sin^2(theta_W) = 1/2 - 1/sqrt(13) = 0.22265 (0.83 sigma)

**What Wilson acknowledges he cannot compute:**
- CKM V_ub angle (admits his derivation gives 4 sigma discrepancy)
- The down-bottom quark mixing

**What Wilson does NOT address honestly:**
- Whether any of these were predictions or post-hoc fits (critical gap)
- Why charged lepton masses should determine PMNS angles (neutrino masses
  are needed in the standard formalism)
- Why nucleon masses should determine CKM parameters (nucleon masses are
  composite; quark masses are the fundamental parameters)
- The 20-degree Cabibbo subtraction has no derivation ("conjectural" in
  his own words)

**The deepest issue:** Wilson's formulas use COMPOSITE particle masses
(proton, neutron) to predict FUNDAMENTAL parameters (mixing angles).
In the Standard Model, the proton and neutron masses are emergent from
QCD dynamics, not fundamental inputs. Using them as inputs for mixing
angles reverses the standard hierarchy of explanation. Wilson argues
this is because the "fundamental" distinction between composite and
elementary is model-dependent, but this is not a standard physics
argument.

### 2.8 Kill Condition KC-M6 Assessment

**KC-M6: Wilson's mass equation m_e + m_mu + m_tau + 3*m_p = 5*m_n
is a coincidence.**

**Verdict: KC-M6 is INCONCLUSIVE. The evidence is ambiguous.**

Arguments FOR coincidence:
- The equation mixes fundamental (lepton masses) with composite (baryon
  masses) quantities
- The integer coefficients (1,1,1,3,5) have no known derivation
- No one has derived this from any Lagrangian or symmetry principle
- The dimensional analysis does not constrain it (both sides are just
  sums of masses)
- With 5 measured quantities and 2 free coefficients (3 and 5), you
  have 3 constraints -- getting one relation correct is not surprising

Arguments AGAINST coincidence:
- 3.95 ppm is remarkably precise for a "random" numerical coincidence
- Wilson's equation is 6x more precise than the Koide formula
- The coefficients (1,1,1,3,5) are simple integers, not contrived
- The equation connects leptons and baryons, which is what GUT theories
  are supposed to do
- As a tau mass prediction, it is the most precise extant prediction
  (0.15 sigma)

**A simple counting argument:** There are roughly 20 "fundamental"
masses in the Standard Model (6 quarks, 6 leptons, W, Z, H, plus
proton and neutron as composite reference). The number of possible
linear relations sum_i a_i m_i = 0 with small integer coefficients
|a_i| <= 5, using 5-6 of these masses, is in the thousands. Finding
one that holds to 4 ppm is not by itself remarkable -- it could be
a look-elsewhere effect.

HOWEVER: Wilson does not just have one relation. He has a SYSTEM of
relations (mass equation + 6-7 angle formulas) that use the SAME 5
masses (m_e, m_mu, m_tau, m_p, m_n) to predict ~8 independent quantities.
If these were all independent coincidences, the joint probability is
much lower. Whether the system is genuinely impressive or whether the
angle formulas are post-hoc fits that exploit the degrees of freedom
in trigonometric functions of mass ratios -- this is the open question.

**Status: Wilson's program is neither confirmed nor debunked. It is
UNENGAGED by the physics community.**

---

## Summary Table

| Question | Answer | Confidence | Evidence |
|----------|--------|------------|----------|
| Do SU(9) CG coefficients factorize under SU(5) x SU(4)? | The coupling is unique by Schur's lemma (mult. 1). Isoscalar factors are non-trivial but act on SU(5) sector labels, not generation indices. Generation mixing matrix is proportional to identity. | 90% | Chen (1981), Schur's lemma, M8.1 data |
| Does KC-M5 fire? | YES, FATAL for generation mixing from CG alone | 85% | Schur + SU(3) symmetry within SU(4) forces delta_{ij} |
| Is Wilson's mass equation known? | No. Novel to Wilson. | 95% | Literature search: zero prior instances |
| Is Wilson's theta_12 formula known? | No. Novel to Wilson. | 95% | Literature search: no standard equivalent |
| Is Wilson's CP phase formula known? | No. Novel to Wilson. | 95% | Literature search: no standard equivalent |
| Has anyone reproduced Wilson? | No. Zero independent reproductions. | 99% | INSPIRE: 11 citations total, none reproduce |
| Is Wilson's program published? | ONE co-authored paper in J. Math. Phys. Solo work: all preprints on gen-ph. | 99% | INSPIRE data |
| Is Wilson's mass equation coincidence? | INCONCLUSIVE. 3.95 ppm is impressive but not proof. | 50/50 | Independent computation confirms precision |

---

## KC-M5 Analysis: What Does This Mean for the Investigation?

**KC-M5 fires FATAL for the specific mechanism tested:** SU(9) CG
coefficients do not produce generation mixing. The 3x3 Yukawa matrix
in generation space is proportional to the identity when the coupling
is computed from SU(9) representation theory alone.

**This confirms the Round 1 prediction at 65% confidence. The actual
confidence is now 85-90%.**

**What remains after KC-M5:**

1. **E8 determines the STAGE (particle content, gauge group, generation
   number) but NOT the SCRIPT (mixing angles, masses).** The mixing
   angles are dynamical, determined by symmetry-breaking VEVs, not by
   kinematical CG coefficients.

2. **Wilson's mass-ratio approach is the only surviving candidate for
   connecting masses to mixing angles**, but it uses mass ratios as
   inputs (not as E8 invariants). The E8 connection is organizational
   (justifying the existence of three generations and specific fermion
   types), not computational (determining the mixing angles).

3. **The maximum achievable from E8 representation theory alone is:**
   - Existence of three generations [MV, verified in Lean]
   - Anomaly cancellation per generation [MV, verified in Lean]
   - Yukawa coupling existence and uniqueness (84 x 84* -> 80, mult 1)
   - Particle content per generation (SU(5) representations)
   - Mass hierarchy PATTERN (different SU(5) sectors couple differently)

   But NOT:
   - Mixing angle values
   - Mass values
   - CP-violating phases
   - Mass hierarchy magnitudes

---

## Recommendations for Round 3

1. **The "geometric mixing from E8" program is dead.** KC-M5 has fired.
   The CG coefficients produce an identity matrix in generation space.
   No further investigation of this line is warranted.

2. **Wilson's mass-ratio program is alive but unengaged.** The Round 3
   investigator should determine: is Wilson's approach DERIVABLE from
   a theoretical framework, or is it empirical pattern-matching? The
   key question is whether the mass equation and angle formulas have a
   common origin in some algebraic structure.

3. **The honest conclusion for Paper 3/4 is:** "E8 representation theory
   constrains particle content and generation number but does not
   determine mixing angles. Mixing requires dynamical input beyond the
   Lie algebra structure."

---

## Files Referenced

- `research/council/e8-mixing-angles/01-vision.md`
- `src/experiments/results/su9_cg_coefficients.json`
- `research/wilson-three-generation-comparison.md`
- Chen, J. Math. Phys. 22, 1-6 (1981), DOI: 10.1063/1.524735
- Slansky, Phys. Rep. 79, 1-128 (1981)
- De Swart, Rev. Mod. Phys. 35, 916 (1963)
- Alex et al., J. Math. Phys. 52, 023507 (2011), arXiv:1009.0437
- Draayer et al., LSU Physics (1990s)
- Wilson, arXiv:2102.02817 (gen-ph, 2021)
- Wilson, arXiv:2407.18279 (gen-ph, 2024)
- Wilson, arXiv:2507.16517 (gen-ph, 2025)
- Manogue, Dray, Wilson, J. Math. Phys. 63, 081703 (2022)
- PDG 2024: https://pdg.lbl.gov/2024/

---

## Confidence Calibration

| Claim | Confidence | Change from Round 1 |
|-------|-----------|-------------------|
| Zero-parameter geometric mixing from E8 is impossible | 95% | Was 85%, strengthened by KC-M5 |
| SU(9) CG coefficients factorize (give identity in gen. space) | 88% | Was 65% (KC-M5 prediction), now nearly confirmed |
| Wilson's theta_12 is a mass-ratio function, not E8 invariant | 97% | Was 95%, confirmed by reproduction |
| Wilson's mass equation precision is genuine (3.95 ppm) | 99% | Was 90%, independently verified |
| Wilson's mass equation is a coincidence | 50% | Was untested, now inconclusive |
| Wilson's program is not peer-reviewed | 99% | Confirmed by publication record |
| No independent reproduction of Wilson exists | 99% | Confirmed by citation search |
| E8 constrains particle content but not mixing angles | 92% | New assessment post-KC-M5 |
| This investigation will close with negative result | 85% | Was 60%, raised by KC-M5 |
