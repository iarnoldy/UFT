# Round 4: RIGOR -- Geometric Mixing Angles from E8

**Agent:** Dollard Theorist (Opus, mathematical rigor)
**Date:** 2026-03-17
**Investigation:** e8-mixing-angles (Real Run)
**Status:** Complete

---

## 0. Scope and Method

This round applies PhD-level mathematical rigor to two specific items flagged
by the Devil's Advocate (Round 3):

1. The antisymmetric coupling [84,84] -> 84* and its generation-space structure
2. Wilson's sin^2(theta_W), joint significance, and mass equation

For each, I show explicit computation, state results precisely, and classify
the finding as POSITIVE, NEGATIVE, or NEUTRAL for the investigation hypothesis.

All numerical results are independently computed and cross-checked.

---

## Task 1: The [84,84] -> 84* Antisymmetric Coupling

### 1.1 Setup

The E8 Lie bracket decomposes under the SU(9) subalgebra as:

    [80, 80] -> 80    (gauge self-interaction)
    [80, 84] -> 84    (gauge-matter coupling)
    [84, 84*] -> 80   (symmetric Yukawa -- tested by KC-M5, gives delta_{ij})
    [84, 84] -> 84*   (antisymmetric coupling -- NOT tested by KC-M5)

The representation theory:
- 84 = Lambda^3(C^9), the third exterior power of the fundamental
- 84* = Lambda^6(C^9), the sixth exterior power (dual to Lambda^3 via SU(9) epsilon)
- The map [84, 84] -> 84* is the **wedge product**: psi^{abc} wedge chi^{def} -> Lambda^6

In index notation:

    Y_{a1...a6} = psi_{[a1 a2 a3} chi_{a4 a5 a6]}

where the bracket denotes full antisymmetrization over all 6 indices.

### 1.2 Channel Decomposition Under SU(5) x SU(4)

Under SU(9) -> SU(5) x SU(4), the fundamental C^9 = C^5 + C^4. Each factor
in Lambda^3(C^9) has p indices from C^5 and (3-p) from C^4:

    84 = Lambda^3(C^9):
      p=3: Lambda^3(C^5) x 1       = (10-bar, 1),  dim 10
      p=2: Lambda^2(C^5) x C^4     = (10, 4),      dim 40
      p=1: C^5 x Lambda^2(C^4)     = (5, 6),       dim 30
      p=0: 1 x Lambda^3(C^4)       = (1, 4-bar),   dim 4
    Total: 84. Check.

    84* = Lambda^6(C^9):
      Lambda^2(C^5) x Lambda^4(C^4) = (10, 1),      dim 10
      Lambda^3(C^5) x Lambda^3(C^4) = (10-bar, 4-bar), dim 40
      Lambda^4(C^5) x Lambda^2(C^4) = (5-bar, 6),   dim 30
      Lambda^5(C^5) x Lambda^1(C^4) = (1, 4),       dim 4
    Total: 84. Check.

The wedge product channels Lambda^3 ^ Lambda^3 -> Lambda^6, with p1 SU(5)
indices from factor 1 and p2 from factor 2 (total p1+p2 SU(5) indices in output):

| Factor 1 | Factor 2 | Output | SU(4) structure |
|----------|----------|--------|-----------------|
| (10,4) | (10,4) | (5-bar, 6) | 4 ^ 4 -> Lambda^2(4) = 6 |
| (10,4) | (5,6) | (10-bar, 4-bar) | 4 ^ Lambda^2(4) -> Lambda^3(4) = 4-bar |
| (10,4) | (1,4-bar) | (10, 1) | 4 ^ Lambda^3(4) -> Lambda^4(4) = 1 |
| (5,6) | (5,6) | (10, 1) | Lambda^2(4) ^ Lambda^2(4) -> Lambda^4(4) = 1 |
| (5,6) | (10-bar,1) | (5-bar, 6) | Lambda^2(4) ^ 1 -> Lambda^2(4) = 6 |
| (10,4) | (10-bar,1) | (1, 4) | 4 ^ 1 -> 4 |
| (1,4-bar) | (10-bar,1) | (10-bar, 4-bar) | Lambda^3(4) ^ 1 -> Lambda^3(4) = 4-bar |

### 1.3 Generation Space Analysis

The generation space lives in SU(3)_fam, which is embedded as SU(3) subset SU(4).
Under SU(4) -> SU(3) x U(1):

    4 -> 3_i + 1         (i = 1,2,3 are generations)
    6 = Lambda^2(4) -> 3-bar + 3
    4-bar -> 3-bar + 1
    1 -> 1

**The key channel is (10,4) x (10,4) -> (5-bar, 6).**

The SU(4) contraction: 4_i ^ 4_j -> 6_{ij} = Lambda^2(C^4).

Under SU(3)_fam, when both indices i,j are generation indices (in {1,2,3}):

    3_i ^ 3_j = epsilon_{ijk} * (3-bar)_k

This is the **Levi-Civita tensor** of SU(3). It is completely fixed by group
theory -- no free parameters, no VEV dependence in the coupling itself.

### 1.4 The Effective Mass Matrix

If the 84* field acquires a VEV with a component in the (5-bar, 6) direction,
the effective mass matrix from the antisymmetric coupling is:

    M^{antisym}_{ij} = g * epsilon_{ijk} * phi_k

where phi_k is the SU(3)_fam component of the 84* VEV (a vector in 3-bar).

**Properties verified numerically:**

(a) For any phi_k, this matrix is **antisymmetric**: M_{ij} = -M_{ji}.

(b) For any 3x3 antisymmetric matrix, **det(M) = 0** (odd-dimensional
antisymmetric matrices always have zero determinant).

(c) The eigenvalues are **purely imaginary**: {+i|phi|, -i|phi|, 0} where
|phi| = sqrt(phi_1^2 + phi_2^2 + phi_3^2).

(d) The singular values (physical masses) are {|phi|, |phi|, 0}: one massless
generation and **two degenerate** generations.

**Verification (phi = (0,0,1)):**

    M = | 0   1   0 |     eigenvalues: +i, -i, 0
        | -1  0   0 |     singular values: 1, 1, 0
        | 0   0   0 |

**Verification (phi = (1,1,1)/sqrt(3)):**

    M = | 0      0.577  -0.577 |     eigenvalues: +i, -i, 0
        | -0.577 0       0.577 |     singular values: 1, 1, 0
        | 0.577  -0.577  0     |

### 1.5 Combined Texture: Symmetric + Antisymmetric

The full Yukawa matrix from E8 has two contributions:

    Y_{ij} = y * delta_{ij} + g * epsilon_{ijk} * phi_k
           = y * I + g * A(phi)

where:
- y * I comes from [84, 84*] -> 80 (tested by KC-M5, gives identity)
- g * A(phi) comes from [84, 84] -> 84* (antisymmetric, this section)

**Eigenvalue analysis of Y = yI + gA:**

The matrix A has eigenvalues {+ia, -ia, 0} where a = |phi|. Therefore:

    eigenvalues of Y = {y + iga, y - iga, y}

The **singular values** (physical masses) are:

    m_1 = y,  m_2 = m_3 = sqrt(y^2 + g^2 a^2)

**Two masses are always degenerate.** This is a theorem, not a numerical
accident: it follows from the fact that the eigenvalues of a real
antisymmetric matrix come in conjugate pairs.

**Verification (y=5, g=1, phi=(0,0,1)):**

    Y = | 5   1   0 |     eigenvalues of Y^dag Y: 25, 26, 26
        | -1  5   0 |     masses: 5, sqrt(26)=5.099, sqrt(26)=5.099
        | 0   0   5 |

### 1.6 Consequences for CKM Mixing

For CKM mixing, we need both up-type and down-type Yukawa matrices:

    Y_u = y_u * I + g_u * A(phi_u)
    Y_d = y_d * I + g_d * A(phi_d)

**Case 1: Same VEV direction (phi_u parallel to phi_d).**
Both matrices are diagonalized by the same unitary transformation.
CKM = V_u^dag V_d = I. **Zero mixing.** (Verified numerically.)

**Case 2: Different VEV directions.**
The relative orientation of phi_u and phi_d determines the CKM matrix.
The mixing angles are functions of the angle between phi_u and phi_d,
which is a **dynamical quantity** (VEV alignment), not a geometric invariant.

(Numerical example: phi_u = (0,0,1), phi_d = (0.5, 0.5, 1/sqrt(2)),
y_u=5, g_u=1, y_d=3, g_d=0.5 produces large off-diagonal CKM entries.)

### 1.7 The Two-Fold Degeneracy Problem

The combined texture Y = yI + gA has a fatal phenomenological defect: the
**two-fold mass degeneracy** means it can produce at most 4 distinct masses
for 6 quarks (two degenerate pairs plus two singlets). The observed quark
mass hierarchy has 6 distinct values spanning 5 orders of magnitude:

    m_u/m_t ~ 10^{-5},  m_c/m_t ~ 10^{-2}

The texture Y = yI + gA cannot reproduce this hierarchy without additional
symmetry breaking (more Higgs fields, non-perturbative effects, or
higher-dimensional operators).

### 1.8 Parameter Counting

| Framework | Parameters per sector | Total for quarks | Observables |
|-----------|---------------------|-----------------|-------------|
| Generic Yukawa | 9 (general 3x3 complex) | 18 | 10 |
| SU(3)_fam generic | 6 | 12 | 10 |
| E8 (I + A) texture | 2 (y, g|phi|) | 4 + 2 (orientation) = 6 | 10 |
| Needed for fit | -- | -- | 6 masses + 4 CKM params |

The E8 texture reduces the parameter count from 18 (generic) to 6. But the
2-fold degeneracy means it can only fit 4 distinct masses + some mixing,
falling short of 10 observables. The constraint ratio 6/10 = 0.6 is
misleadingly favorable because the texture is too restrictive in the wrong
way (degeneracy instead of hierarchy).

### 1.9 Verdict on Task 1

**The [84,84] -> 84* coupling produces a non-trivial generation-space structure
via the Levi-Civita tensor epsilon_{ijk}.** The Devil's Advocate was correct
that KC-M5 did not test this channel. However:

(a) The antisymmetric texture has a **mandatory two-fold mass degeneracy**
that is incompatible with the observed quark/lepton mass spectrum.

(b) CKM mixing from this texture requires **different VEV directions for up
and down sectors**, which is a dynamical (not geometric) choice.

(c) The texture does constrain the Yukawa beyond generic SU(3)_fam models
(6 parameters vs 12), but the constraint is of the **wrong type** for
phenomenology.

**Classification: NEUTRAL (leaning NEGATIVE)**

The epsilon coupling exists and is non-trivial, but the two-fold degeneracy
is a structural defect. The antisymmetric coupling alone cannot produce
realistic fermion masses or mixing angles. It strengthens the case that
mixing angles require dynamical input beyond E8 representation theory.

---

## Task 2: Wilson sin^2(theta_W) Calculation

### 2.1 Two Different Wilson Formulas

The previous rounds conflated two different formulas attributed to Wilson:

**Formula A:** sin^2(theta_W) = 3/13 = 0.23076923...

**Formula B:** sin^2(theta_W) = 1/2 - 1/sqrt(13) = 0.22264990...

These are **different numbers** (difference = 0.00812). The Round 3 table
listed sin^2(theta_W) = 3/13 = 0.2308 with a "0.10 sigma" deviation. This
is incorrect. I compute the actual deviations precisely.

### 2.2 Experimental Values (PDG 2024)

The "Weinberg angle" has multiple definitions at different scales and in
different renormalization schemes:

| Scheme | Value | Error |
|--------|-------|-------|
| MS-bar at M_Z | 0.23121 | 0.00004 |
| On-shell (1 - M_W^2/M_Z^2) | 0.22290 | 0.00030 |
| Effective leptonic | 0.23153 | 0.00004 |

### 2.3 Precise Deviations

**For 3/13 = 0.230769:**

| vs Scheme | Deviation |
|-----------|-----------|
| MS-bar at M_Z | (0.23121 - 0.23077) / 0.00004 = **+11.0 sigma** |
| On-shell | (0.22290 - 0.23077) / 0.00030 = **-26.2 sigma** |
| Effective leptonic | (0.23153 - 0.23077) / 0.00004 = **+19.0 sigma** |

**3/13 is a POOR match to experiment in ALL schemes.**

**For 1/2 - 1/sqrt(13) = 0.22265:**

| vs Scheme | Deviation |
|-----------|-----------|
| MS-bar at M_Z | (0.23121 - 0.22265) / 0.00004 = **+214 sigma** |
| On-shell | (0.22290 - 0.22265) / 0.00030 = **+0.83 sigma** |
| Effective leptonic | (0.23153 - 0.22265) / 0.00004 = **+222 sigma** |

**1/2 - 1/sqrt(13) matches the ON-SHELL scheme at 0.83 sigma but fails
catastrophically in the MS-bar scheme.**

### 2.4 The Scheme-Dependence Problem

The discrepancy between Wilson's predictions in different schemes reveals a
fundamental problem: **Wilson does not specify at which scale or in which
scheme his prediction applies.**

In the Standard Model, the running of sin^2(theta_W) from the on-shell
value (0.2229) to the MS-bar value (0.2312) is a shift of +0.0083. This is
a calculable radiative correction. Any prediction must specify which quantity
it predicts.

- If Wilson predicts the **on-shell** value: 1/2 - 1/sqrt(13) works (0.83 sigma)
  but 3/13 fails (26 sigma).
- If Wilson predicts the **MS-bar** value: both formulas fail catastrophically.
- If Wilson predicts a **tree-level GUT** value: then RG running must be applied.

### 2.5 Comparison to Standard GUT Prediction

In SU(5) and all standard GUTs:
- Tree-level at M_GUT: sin^2(theta_W) = 3/8 = 0.375
- After RG running to M_Z: ~0.2312 (matches MS-bar)

The running shifts the value by ~0.144, which is enormous. If Wilson's 3/13
were a GUT-scale prediction, RG running would move it to ~0.227, which is
further from experiment, not closer.

Wilson's formulas appear to be **low-energy** predictions, not GUT-scale
predictions. This means they have no connection to the E8 gauge structure
(which lives at the GUT scale). They are numerological relations at low energy.

### 2.6 The Round 3 Error

The Devil's Advocate Round 3 table listed "sin^2(theta_W) = 3/13 = 0.2308"
with "0.10 sigma" deviation. This is **wrong on multiple levels:**

1. 3/13 = 0.23077, not 0.2308 (rounding error)
2. No experimental value gives a 0.10 sigma deviation from 3/13
3. The Round 1 and Round 2 documents used 1/2 - 1/sqrt(13), not 3/13
4. The 0.83 sigma figure from Round 1 used 1/2 - 1/sqrt(13) vs on-shell

The two formulas (3/13 and 1/2 - 1/sqrt(13)) were conflated across rounds.

### 2.7 Verdict on Task 2

**Classification: NEGATIVE**

- 3/13 is 11-26 sigma from experiment depending on scheme. It is NOT a
  good prediction.
- 1/2 - 1/sqrt(13) is 0.83 sigma from the on-shell value but 214 sigma
  from the MS-bar value. It works in one scheme only, and Wilson does not
  specify which scheme he predicts.
- Neither formula has a mechanism connecting it to E8 geometry. The number
  13 does not arise from any E8 representation dimension or Casimir.
- The comparison to standard GUT (3/8 at GUT scale, runs to 0.231) shows
  that Wilson's approach is fundamentally different and does not incorporate
  radiative corrections.

---

## Task 3: Wilson Joint Significance

### 3.1 Enumeration of Claims

Wilson's system uses 5 input masses: {m_e, m_mu, m_tau, m_p, m_n}.

| # | Prediction | Formula | Wilson value | Experimental | Deviation |
|---|-----------|---------|-------------|-------------|-----------|
| 1 | Mass equation | m_e+m_mu+m_tau+3m_p=5m_n | diff=18.5 keV | -- | 0.15 sigma (as m_tau) |
| 2 | theta_12 (PMNS) | cos(60-t)/cos(t)=(m_tau-m_e)/(m_tau-m_mu) | 33.024 deg | 33.41+/-0.75 | 0.51 sigma |
| 3 | delta_CP (CKM) | arctan((m_n-m_p)/m_e) | 68.44 deg | 68.8+/-4.5 | 0.08 sigma |
| 4 | theta_23 (CKM) | arccos((m_p+m_e)/m_n) | 2.338 deg | 2.38+/-0.06 | 0.70 sigma |
| 5 | Cabibbo | theta_12 - 20 | 13.024 deg | 13.04+/-0.05 | 0.32 sigma |
| 6 | sin^2(theta_W) | 1/2 - 1/sqrt(13) | 0.22265 | 0.22290+/-0.00030 | 0.83 sigma |
| 7 | V_ub (CKM) | Wilson's formula | -- | -- | **4 sigma FAILURE** |

**Note on theta_12:** The formula cos(60-t)/cos(t) = R where R = (m_tau-m_e)/(m_tau-m_mu)
gives tan(t) = (R - 1/2) * 2/sqrt(3), yielding t = 33.024 degrees.
Verified: R = 1776.349/1671.202 = 1.06292, tan(t) = 0.65000, t = 33.024 deg.

### 3.2 Independence Analysis

**Not all predictions are independent.** The genuine degrees of freedom:

(a) **Mass equation** (1 relation among 5 masses): genuinely 1 independent
prediction (equivalent to predicting m_tau from the other 4).

(b) **theta_12**: A function of m_e, m_mu, m_tau. If the mass equation
determines m_tau, then theta_12 becomes a function of m_e, m_mu, m_p, m_n.
This IS independent of the mass equation itself (different functional form).
Count: 1 independent prediction.

(c) **delta_CP (CKM)**: arctan((m_n-m_p)/m_e). Uses masses {m_e, m_p, m_n}.
Independent of the lepton-mass-based predictions. Count: 1.

(d) **theta_23 (CKM)**: arccos((m_p+m_e)/m_n). Uses the **same 3 masses**
as delta_CP. With 3 masses one can form 2 independent dimensionless ratios.
delta_CP and theta_23 use different functions of the same ratios. They are
NOT fully independent -- they share the same information content.
Count: ~0.5 additional.

(e) **Cabibbo angle**: theta_12 - 20 degrees. The "20 degrees" is an **ad hoc
offset** that Wilson calls "purely conjectural" with "no theoretical
justification." This is a **fit with 1 free parameter** (the offset), not a
prediction. Count: 0.

(f) **sin^2(theta_W)**: Uses zero mass inputs. It is an entirely separate
claim, not part of the mass-ratio system. Count: 1 (but see Task 2 -- it
only works in one specific scheme).

(g) **V_ub**: Wilson acknowledges a **4 sigma failure**. This must be counted
as a negative data point.

### 3.3 Honest Count

**Genuinely independent successful predictions: 3.5**
- Mass equation (1)
- theta_12 from lepton masses (1)
- delta_CP from baryon masses (1)
- theta_23 from baryon masses (0.5, not independent of delta_CP)

**Failed predictions: 1** (V_ub at 4 sigma)

**Separate claim (not mass-based): 1** (sin^2 theta_W, scheme-dependent)

### 3.4 Joint Probability

If 3.5 independent predictions each fall within 1 sigma:

    P(all within 1 sigma) = 0.6827^{3.5} = 0.26

This is equivalent to ~1.1 sigma. **Not statistically significant.**

The Round 3 Devil's Advocate claimed "~2 sigma anomaly" based on 8
predictions. This was incorrect for two reasons:
1. Only 3.5 predictions are genuinely independent (not 8)
2. The V_ub failure (4 sigma) was excluded from the joint assessment

**With the V_ub failure included:** The joint probability of getting 3.5
successes at <1 sigma AND one failure at >4 sigma is:

    P = 0.26 * (1 - 0.99994) ~ 0.00002

This looks anomalous in the opposite direction -- the system has an
INCONSISTENCY (some very good, one very bad), which is more characteristic
of post-hoc selection than of a systematic framework.

### 3.5 Pre-Registration Status

**None of Wilson's formulas are pre-registered predictions.** All were
published after the experimental values were known:

- The lepton masses (m_e, m_mu, m_tau) were measured by the 1970s
- The CKM parameters have been measured since the 1980s-2000s
- The PMNS angles were measured 2002-2012
- Wilson's first mixing angle paper appeared in 2021

Wilson had access to all experimental values before constructing his formulas.
The formulas are **post-hoc fits**, not predictions. This is the critical
difference between numerology and physics.

**For comparison:** The Standard Model GUT prediction sin^2(theta_W) = 3/8
(corrected by RG running to ~0.231) was made by Georgi and Glashow in 1974,
**before** the precise experimental measurement (confirmed in the 1990s at
LEP). That was a genuine prediction.

### 3.6 Look-Elsewhere Effect

Wilson uses 5 masses and various trigonometric functions (arctan, arccos,
algebraic combinations). The space of "formulas you can write" with these
ingredients is large:

- Number of distinct dimensionless ratios from 5 masses: C(5,2) = 10
- Number of simple trig functions: ~5 (arctan, arccos, arcsin, algebraic, sqrt)
- Number of candidate formulas: ~50
- Number of measured quantities to match: ~20 (masses, mixing angles, etc.)

With ~50 candidate formulas and ~20 targets, the expected number of <1 sigma
matches **by chance** is 50 * 20 * 0.68 / (number of trials) -- this is hard
to compute precisely, but the point is that post-hoc searching through a
large formula space makes individual successes much less impressive.

### 3.7 Verdict on Task 3

**Classification: NEGATIVE**

- After honest counting: 3.5 independent predictions, not 7-8
- Joint significance: ~1.1 sigma. Not anomalous.
- All predictions are post-hoc (zero pre-registered)
- The V_ub failure (4 sigma) contradicts the "systematic framework" claim
- The look-elsewhere effect from searching over formula space further reduces
  the significance
- The Round 3 claim of "2 sigma anomaly" was based on overcounting

---

## Task 4: Mathematical Status of the Mass Equation

### 4.1 Precise Computation

    m_e + m_mu + m_tau + 3*m_p = 5*m_n

**LHS:**

| Term | Value (MeV) |
|------|-------------|
| m_e | 0.51099895 |
| m_mu | 105.6583755 |
| m_tau | 1776.86 |
| 3*m_p | 2814.81626448 |
| **SUM** | **4697.84564** |

**RHS:**

| Term | Value (MeV) |
|------|-------------|
| 5*m_n | 4697.82710 |

**Difference:**

    LHS - RHS = 0.01854 MeV = 18.54 keV

**Relative precision:** 3.95 ppm

**Error analysis:** The dominant uncertainty is sigma(m_tau) = 0.12 MeV.
All other mass uncertainties are negligible (< 0.01 MeV combined). Therefore:

    sigma(LHS - RHS) ~ sigma(m_tau) = 0.12 MeV
    Significance: 0.0185 / 0.12 = 0.15 sigma

As a prediction of m_tau:

    m_tau(predicted) = 5*m_n - m_e - m_mu - 3*m_p = 1776.8415 MeV
    m_tau(measured) = 1776.86 +/- 0.12 MeV
    Deviation: 0.15 sigma

### 4.2 Comparison to Koide Formula

The Koide formula (1981):

    Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = 2/3

Precision: Q = 0.666661, deviation from 2/3 = 9.2 ppm.

Wilson mass equation precision: 3.95 ppm.

**Wilson's equation is approximately 2x more precise than Koide.**

However, the Koide formula has been studied extensively in the literature
(Koide 1981; Foot 1994; Rivero 2005; many others), has a possible derivation
from a Z3 symmetry acting on a mass matrix, and involves only fundamental
(lepton) masses. Wilson's equation mixes fundamental and composite masses,
which is a deeper problem (Section 4.4).

### 4.3 Algebraic Rewriting

The equation can be rewritten:

    m_e + m_mu + m_tau = 5*m_n - 3*m_p = 2*m_n + 3*(m_n - m_p)

Numerically:
- Lepton sum = 1883.029 MeV
- 2*m_n + 3*(m_n - m_p) = 1879.131 + 3.880 = 1883.011 MeV

Or equivalently:

    sum of charged lepton masses = 2 * (neutron mass) + 3 * (n-p mass splitting)

The n-p mass splitting (1.2933 MeV) is a precisely measured quantity arising
from the interplay of QCD isospin breaking (m_d - m_u contribution ~2.5 MeV)
and electromagnetic effects (~-1.2 MeV). Writing the equation this way does
not illuminate its origin, but it shows that the relation fundamentally
connects the charged lepton mass sum to neutron properties.

### 4.4 The Composite Mass Problem

**This is the deepest objection to the mass equation.**

The proton and neutron masses are ~99% QCD binding energy:
- Current quark masses in proton: m_u + m_u + m_d ~ 9.1 MeV (1% of m_p)
- QCD binding energy: ~929 MeV (99% of m_p)
- Electromagnetic correction: ~-0.8 MeV

The proton mass is determined primarily by Lambda_QCD (the QCD confinement
scale), not by the Higgs Yukawa couplings that set quark masses. The lepton
masses, by contrast, come entirely from the Higgs mechanism.

Wilson's equation connects:
- **Left side:** 3 Yukawa-determined masses (leptons) + 3 x (QCD-determined mass)
- **Right side:** 5 x (QCD-determined mass)

There is **no known theoretical framework** in which a relation between
Yukawa-determined and QCD-determined masses holds at the ppm level. The two
types of mass arise from fundamentally different mechanisms in the Standard
Model.

For such a relation to have a theoretical origin, one would need a framework
in which:
(a) Both lepton masses and Lambda_QCD are determined by a single structure, AND
(b) The relation is protected by a symmetry that holds to ppm accuracy.

E8 unification could in principle satisfy (a) (all couplings derive from the
E8 gauge coupling), but no mechanism for (b) has been identified.

### 4.5 Search for Theoretical Frameworks

**SU(9) trace identities:** The tracelessness condition Tr(T_a) = 0 for SU(9)
generators implies sum rules on representation multiplicities, not on masses.
Masses are eigenvalues of the Yukawa matrix times VEV, which is dynamical.
No SU(9) trace identity produces the Wilson equation.

**E8 trace relations:** The Killing form Tr_{adj}(T_a T_b) = 60 * delta_{ab}
for E8 constrains the sum of squares of all 248 mass eigenvalues, not a linear
relation among 5 specific masses. No E8 identity produces the Wilson equation.

**Koide-type generalizations:** The Koide formula involves only leptons and
uses square roots of masses. It has been generalized to quarks (Rivero 2005)
and to lepton-quark relations (Brannen 2006), but none of these involve
**baryon** masses. Wilson's equation is structurally different from all
known Koide-type relations.

**String theory compactifications:** In heterotic string theory on E8 x E8,
Yukawa couplings and gauge couplings are both determined by the same moduli
(compactification geometry). In principle, this could produce relations between
lepton masses and hadron masses (via quark masses and Lambda_QCD). However:
(a) No specific compactification is known to produce Wilson's equation.
(b) The proton mass depends on Lambda_QCD through dimensional transmutation
(m_p ~ Lambda_QCD * exp(-8pi^2/(b_0 * g^2))), which involves the QCD beta
function coefficient b_0. A ppm-level relation between lepton masses and
exp(-8pi^2/...) would be extraordinary and unprecedented.

**Group-theoretic mass relations:** The only known group-theoretic mass
relations are:
- m_b = m_tau at GUT scale (from SU(5) Yukawa unification, ~20% accuracy)
- m_s / m_mu (Georgi-Jarlskog factor of 3, ~30% accuracy)

These are order-of-magnitude relations, not ppm-level relations. No
group-theoretic framework produces ppm mass relations.

### 4.6 Combinatorial Assessment

With N ~ 20 "fundamental" masses (6 quarks, 6 leptons, W, Z, H, plus proton
and neutron) and small integer coefficients |a_i| <= 5, the number of linear
relations of the form sum_i a_i * m_i = 0 using k masses is roughly:

    N_formulas ~ C(20, k) * 11^k (choices of coefficients -5 to +5)

For k = 5: C(20,5) * 11^5 ~ 15,504 * 161,051 ~ 2.5 * 10^9

The probability that at least one such relation holds at the Q ppm level
is approximately:

    P ~ N_formulas * (Q * 10^{-6}) * (mass_range / typical_mass)

This is a rough estimate but suggests that finding one relation at 4 ppm
among billions of candidates is not improbable. The look-elsewhere effect
is enormous.

**However:** Not all candidate relations are equally "nice." Wilson's
coefficients (1,1,1,3,5) are small and structured (first 3 odd numbers,
sum = 11 = E8 exponent). If we restrict to "nice" coefficients (say,
integers with clear patterns and |a_i| <= 5), the number of candidates
drops by several orders of magnitude, making the 4 ppm precision more
noteworthy.

### 4.7 Verdict on Task 4

**Classification: NEUTRAL**

The mass equation is:
- **Precisely verified:** 3.95 ppm, 0.15 sigma as m_tau prediction.
- **More precise than Koide:** by a factor of ~2.
- **Without theoretical derivation:** No known framework produces it.
- **Mixing fundamental and composite:** Epistemologically problematic.
- **Subject to look-elsewhere effect:** Billions of candidate relations exist.
- **Structurally interesting:** Coefficients (1,1,1,3,5) are "nice."

The honest classification is: **unexplained empirical regularity of uncertain
significance.** It could be a deep relation waiting for explanation, or it
could be a numerical coincidence elevated by post-hoc selection from a large
search space. Without a theoretical framework, it is impossible to distinguish
these possibilities.

---

## Updated Confidence Table

| Claim | R1 | R2 | R3 | R4 (This round) | Basis |
|-------|-----|-----|-----|-----------------|-------|
| Zero-parameter geometric mixing from E8 impossible | 85% | 95% | 96% | **97%** | No mechanism found; antisymmetric coupling has wrong structure |
| Wilson theta_12 is mass-ratio function, not E8 invariant | 95% | 97% | 95% | **97%** | Confirmed formula, confirmed it uses mass inputs |
| Wilson mass equation 3.95 ppm is coincidence | -- | 50% | 35% | **50%** | Restored: Round 3 significance was overcounted |
| Wilson mass equation derivable from algebra | -- | -- | 30% | **15%** | No framework found; composite mass problem is severe |
| SU(9) CG factorize (delta_{ij} in gen. space) | 65% | 88% | 90% | **92%** | Antisymmetric channel adds epsilon_{ijk} but with 2-fold degeneracy |
| Antisymmetric [84,84]->84* gives non-trivial texture | -- | -- | 60% | **90%** | Confirmed: epsilon_{ijk}, but 2-fold degenerate (problematic) |
| E8 constrains Yukawa texture beyond generic SU(5)+SU(3) | -- | -- | 45% | **55%** | Yes: only I+A terms allowed (6 params vs 18). But 2-fold degeneracy. |
| Wilson system statistically anomalous (>2sigma jointly) | -- | -- | 70% | **15%** | Overcounted: 3.5 independent predictions, not 8. Joint P~0.26, ~1.1 sigma. |
| Wilson sin^2(theta_W) = 3/13 matches experiment | -- | -- | -- | **2%** | 11-26 sigma off in all standard schemes |
| Wilson sin^2(theta_W) = 1/2-1/sqrt(13) matches experiment | -- | -- | 80% | **40%** | 0.83 sigma in one scheme, >200 sigma in another; scheme not specified |
| Investigation should close with negative result on H1 | 60% | 85% | 95% | **97%** | Strong form definitively dead by all tests |
| Wilson bridge (H3) is genuine anomaly | -- | -- | 75% | **30%** | Joint significance overcounted; V_ub failure; all post-hoc; scheme problem |

### Key Changes from Round 3

1. **Wilson joint significance downgraded from 70% to 15%.** The "2 sigma
   anomaly" was based on 8 predictions; honest counting gives 3.5, reducing
   joint significance to ~1.1 sigma.

2. **Wilson sin^2(theta_W) split into two claims.** 3/13 is a poor match
   (11 sigma); 1/2-1/sqrt(13) matches one scheme only.

3. **Antisymmetric coupling confirmed but with 2-fold degeneracy.** The
   epsilon_{ijk} structure is real but creates a phenomenological problem,
   not a solution.

4. **Mass equation restored to 50/50.** Without a framework, it cannot be
   distinguished from coincidence. The Round 3 upgrade to 35% was based
   on the now-deflated joint significance argument.

---

## Recommendation for Final Synthesis

### What to Report

1. **Strong form (H1) is DEAD (97%).** E8 root geometry does not determine
   mixing angles. The antisymmetric coupling adds epsilon_{ijk} structure but
   with a 2-fold degeneracy that prevents realistic masses, and CKM mixing
   still requires dynamical VEV alignment.

2. **Medium form (H2) is WEAK but REAL (55%).** E8 constrains the Yukawa
   texture to Y = y*I + g*A (6 parameters vs 18 generic), which is a genuine
   representation-theoretic constraint. But the 2-fold degeneracy is a
   problem, and the constraint does not determine mixing angles.

3. **Weak form (H3/Wilson bridge) is NOT ANOMALOUS (30%).** After honest
   counting of independent predictions (3.5, not 8), including the V_ub
   failure, accounting for post-hoc formula construction, and noting the
   sin^2(theta_W) scheme problem, the Wilson system is ~1.1 sigma
   significant. This is well within noise.

4. **The mass equation is UNEXPLAINED but not ANOMALOUS.** Its 3.95 ppm
   precision is notable but not beyond what combinatorial search can produce.
   It has no theoretical derivation and mixes fundamental and composite masses.

### What NOT to Report

Do not report the "2 sigma joint anomaly" from Round 3. It was based on
incorrect counting (8 predictions instead of 3.5) and did not include the
V_ub failure. The corrected assessment is ~1.1 sigma, which is not anomalous.

Do not report sin^2(theta_W) = 3/13 as matching experiment. It is 11 sigma
off in the MS-bar scheme.

### For Papers 3 and 4

No revision needed. The papers correctly state that mixing angles require
dynamical input beyond E8. The Wilson connection should NOT be mentioned
in the papers (it is neither confirmed nor refuted, it is post-hoc numerology
of marginal significance, and citing it would invite justified criticism).

---

## Files Referenced

- `research/council/e8-mixing-angles/01-vision.md`
- `research/council/e8-mixing-angles/02-archaeology.md`
- `research/council/e8-mixing-angles/03-devils-advocate.md`
- `src/experiments/results/su9_cg_coefficients.json`
- `src/experiments/results/yukawa_texture_analysis.json`
- `src/experiments/results/wilson_pmns_verification.json`
- `research/wilson-three-generation-comparison.md`
- `research/yukawa-kill-condition-research.md`
- Wilson arXiv:2102.02817 (2021)
- Wilson arXiv:2407.18279 (2024)
- Chen, J. Math. Phys. 22, 1-6 (1981)
- PDG 2024: https://pdg.lbl.gov/2024/

---

## Computation Scripts

All numerical results independently computed. Key computations:
- `research/council/e8-mixing-angles/task1_antisym.py` (antisymmetric coupling)
- Inline Python for Tasks 2-4 (verified in conversation, not separately saved)
