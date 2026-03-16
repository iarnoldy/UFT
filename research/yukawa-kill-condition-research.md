# SU(9) Yukawa Couplings and the Three-Generation Kill-Condition

> Research for Milestone 8 (Phenomenology Kill-Condition)
> Date: 2026-03-16
> Full notebook: ~/research/su9-yukawa-kill-condition-20260316/

## Research Question

In an E8 grand unified theory with three generations arising from the SU(9)/Z3 decomposition (248 = 80 + 84 + 84*), what constraints does the SU(9) representation theory impose on Yukawa coupling matrices? Can this framework produce realistic CKM and PMNS mixing matrices?

---

## 1. SU(9) Clebsch-Gordan Coefficients for 84 x 84 x 80

### 1.1 The Trilinear Coupling Structure

The Yukawa coupling in the SU(9) framework comes from the E8 adjoint self-coupling. Under E8 -> SU(9)/Z3, the 248-dimensional adjoint decomposes as:

    248 = 80 + 84 + 84*

where 80 = adj(SU(9)), 84 = Lambda^3(C^9), and 84* = Lambda^6(C^9).

The E8 Lie bracket decomposes under SU(9) as:

    [80, 80] -> 80      (SU(9) gauge self-interaction)
    [80, 84] -> 84      (gauge coupling to matter)
    [80, 84*] -> 84*    (gauge coupling to anti-matter)
    [84, 84*] -> 80     (Yukawa type 1: matter x anti-matter -> Higgs)
    [84, 84] -> 84*     (Yukawa type 2: matter x matter -> anti-matter, via epsilon tensor)

### 1.2 Uniqueness of the Coupling

**Result:** The SU(9)-invariant trilinear coupling 84 x 84* x 80 is UNIQUE up to overall normalization.

**Proof sketch:** By Schur's lemma, the number of independent SU(9)-invariant couplings R x R* -> adj(SU(9)) equals the multiplicity of the adjoint in the tensor product R x R*. For any irreducible representation R of SU(N), the decomposition R x R* always contains the adjoint exactly once (and the trivial representation exactly once). Since 84 = Lambda^3(C^9) is irreducible under SU(9), the coupling is unique.

**Implication:** At leading order, the Yukawa coupling structure is entirely determined by group theory. The only freedom is the overall coupling constant.

### 1.3 Decomposition Under SU(5) x SU(4)

Under SU(9) -> SU(5) x SU(4) x U(1), the 84 decomposes as [MV]:

    84 = (10,1) + (10,4) + (5,6) + (1,4-bar)

with dimensions 10 + 40 + 30 + 4 = 84.

Further breaking SU(4) -> SU(3)_family x U(1):

    84 = (10,1) + (10,3) + (10,1) + (5,3-bar) + (5,3) + (1,3-bar) + (1,1)

with dimensions 10 + 30 + 10 + 15 + 15 + 3 + 1 = 84.

The Yukawa coupling 84 x 84* x 80 decomposes into multiple SU(5) x SU(3)_family components. The KEY question is: what are the RELATIVE Clebsch-Gordan coefficients between different SU(5) sectors?

Specifically, the Yukawa matrix for the (10,3) sector and the (5-bar,3) sector may have different CG prefactors. If so, this provides a NON-TRIVIAL prediction for the GUT-scale ratio m_d/m_e per generation, beyond the standard SU(5) Georgi-Jarlskog factor.

### 1.4 What Needs to Be Computed

The SU(9) CG coefficient computation requires:
1. The tensor product 84 x 84* decomposed into SU(9) irreps
2. The projection onto the adjoint 80 component
3. This projection further decomposed under SU(5) x SU(4)
4. The specific CG coefficients for the (10,3) x (10-bar,3-bar) -> (24,1) and (5,3-bar) x (5-bar,3) -> (24,1) contractions

**This computation has NOT been performed in the literature.** No paper was found that explicitly computes SU(9) Yukawa CG coefficients.

---

## 2. Family Symmetry and Yukawa Textures

### 2.1 Literature Survey: SU(3)_family Models

The SU(3)_family symmetry has been extensively studied in the flavor physics literature:

**Key authors and results:**
- **Froggatt-Nielsen (1979):** Hierarchical Yukawa from abelian U(1) symmetry + flavon VEV. The small parameter epsilon = v/M generates mass hierarchy as powers: m_1 : m_2 : m_3 ~ epsilon^4 : epsilon^2 : 1. [Nucl. Phys. B 147 (1979) 277]
- **Ma-Rajasekaran (2001):** A4 discrete symmetry (subgroup of SU(3)) for tri-bimaximal neutrino mixing. [Phys. Rev. D 64 (2001) 113012]
- **King (2003-present):** SU(3)_family -> A4 or S4 for lepton mixing. Extensive model building. [arXiv:1301.1340]
- **Altarelli-Feruglio (2005-2010):** A4 models for neutrino mixing. Review in Rev. Mod. Phys. 82 (2010) 2701. [arXiv:1002.0211]
- **Barbieri-Hall (1995):** U(2) symmetry for first two generations. Predictive texture. [arXiv:hep-ph/9512388]
- **Ross et al. (1997):** Yukawa textures from U(1)_X family symmetry combined with Pati-Salam unification. chi^2/dof = 0.39/3. [arXiv:hep-ph/9703361]
- **Ramond (1979/1998):** Family group problem. Reviews SU(5), SO(10), E6 family enlargement. Sketches SU(8) unification with family. [arXiv:hep-ph/9809459]

### 2.2 What SU(3)_family Predicts for Yukawa Textures

**Unbroken SU(3)_family:**
The SU(3)-invariant Yukawa coupling gives M_{ij} = y * v * delta_{ij}. All three generations have the SAME mass. CKM = PMNS = identity. This is the WRONG starting point for the "democratic mass matrix" -- the democratic matrix (all entries equal) gives eigenvalues (3m, 0, 0) and trimaximal mixing, but it is NOT the SU(3)-symmetric limit.

**Democratic mass matrix:**
The democratic texture M_{ij} = m * J (where J has all entries = 1/3) is NOT SU(3)-invariant. It is the outer product of the SU(3)-invariant vector (1,1,1)/sqrt(3) with itself: M = m * |v><v|. This is a RANK-1 matrix with eigenvalues (m, 0, 0). Its diagonalization requires the "trimaximal" rotation, which has mixing angles similar to those in the PMNS matrix (theta_12 ~ 35.3 deg, theta_23 ~ 45 deg, theta_13 = 0).

**SU(3) breaking patterns:**
- SU(3) -> SU(2) x U(1): one generation distinguished. Gives hierarchy m_3 >> m_2, m_1.
- SU(3) -> U(1) x U(1): all three generations distinguished. Full hierarchy m_3 >> m_2 >> m_1.
- SU(3) -> A4/S4/Delta(27): discrete subgroups. Different mixing patterns.
- SU(3) -> nothing: generic breaking. Most parameters.

### 2.3 The Critical Question: CKM (Small) vs PMNS (Large) from the Same SU(3)

**Can a SINGLE SU(3)_family produce both hierarchical CKM and large-angle PMNS?**

**Answer: YES, but only with additional structure.**

The standard mechanism:
1. The up-type quark mass matrix M_u is nearly diagonal (hierarchical): m_t >> m_c >> m_u
2. The down-type quark mass matrix M_d is also nearly diagonal: m_b >> m_s >> m_d
3. Since both are nearly diagonal, CKM = V_u^dag V_d is close to identity (small mixing).
4. The charged lepton mass matrix M_e is also hierarchical (like M_d in SU(5)).
5. The neutrino mass matrix M_nu is DEMOCRATIC or ANARCHICAL (from the seesaw mechanism).
6. Since M_e is hierarchical but M_nu is democratic, PMNS = V_e^dag V_nu has large mixing.

The key insight: the difference between CKM (small) and PMNS (large) comes from the SEESAW MECHANISM acting on neutrinos, NOT from different Yukawa structures. The charged fermion Yukawa matrices can all be hierarchical (from SU(3)_family breaking), while the neutrino mass matrix gets a democratic contribution from the seesaw.

**Implication for SU(9):** The SU(9) framework provides hierarchical Yukawa matrices for charged fermions (from perturbative SU(3)_family breaking around the delta_{ij} starting point). The PMNS large mixing must come from the seesaw sector, which is NOT directly constrained by the SU(9) Yukawa structure.

---

## 3. Prior Work on E8 Yukawa Couplings

### 3.1 Bars and Gunaydin (1980)
**Paper:** "Grand Unification with the Exceptional Group E8" PRL 45 (1980) 859
**Content:** Proposed E8 as a unified gauge group. Identified 3 + 3-bar families of SU(5) within E8. Predicted conjugate families below 1 TeV (not observed).
**Yukawa computation:** Did NOT compute Yukawa coupling matrices.
**Relevance:** Foundational paper for E8 GUTs but no Yukawa content.

### 3.2 Ramond (1979/1998)
**Paper:** "The Family Group in Grand Unified Theories" [arXiv:hep-ph/9809459]
**Content:** Reviews family problem. Discusses SU(5), SO(10), E6 as family enlargement groups. Sketches SU(8) (not SU(9)) unification with SU(5) family.
**Yukawa computation:** General discussion of Yukawa structure in family GUTs. No specific SU(9) computation.
**Relevance:** Closest approach to the SU(9) question but uses SU(8) instead.

### 3.3 Lisi (2007)
**Paper:** "An Exceptionally Simple Theory of Everything" [arXiv:0711.0770]
**Content:** Proposed E8 unification including gravity. Used the noncompact form E8(-24).
**Yukawa computation:** Did NOT compute Yukawa couplings. Acknowledged mass/generation problem unresolved.
**Chirality problem:** Distler-Garibaldi showed mirror fermions are unavoidable in Lisi's embedding.
**Relevance:** Same E8 algebra but different physical interpretation. No Yukawa content.

### 3.4 Wilson (2025)
**Claimed paper:** arXiv:2507.16517 -- alleged to derive mixing angles from mass ratios.
**Status:** This arXiv ID does not correspond to a published or accessible paper as of 2026-03-16. The reference cannot be verified.
**Relevance:** Cannot be assessed.

### 3.5 Heterotic String Models
**E8 x E8 heterotic string** models use the decomposition E8 -> E6 x SU(3)_family (different from our SU(9) decomposition). In these models, Yukawa couplings arise from string worldsheet instantons and are in principle computable but depend on the compactification geometry. The SU(3)_family in heterotic models plays the same role as in our framework, but the UV completion is different (string theory vs point-particle GUT).

### 3.6 Literature Gap Assessment

**No paper was found that explicitly computes Yukawa coupling matrices from the SU(9)/Z3 decomposition of E8.**

Possible explanations:
1. **The chirality problem** (Distler-Garibaldi) has discouraged E8 Yukawa computations.
2. **The computation reduces to standard SU(3)_family + SU(5) GUT** analysis, which has been extensively done.
3. **The SU(9) embedding provides no additional information** beyond the standard framework.

Assessment: Explanation (2) is most likely. The SU(9) framework provides a UV completion for SU(3)_family models, but the low-energy Yukawa predictions depend on the flavon sector.

---

## 4. The CKM vs PMNS Puzzle

### 4.1 Measured Values

**CKM matrix** (Wolfenstein parameterization):
- lambda = 0.22500 +/- 0.00067 (Cabibbo angle sin(theta_C) ~ 0.22)
- A = 0.826 +/- 0.015
- rho-bar = 0.159 +/- 0.010
- eta-bar = 0.348 +/- 0.010

**PMNS matrix** (PDG 2024):
- theta_12 = 33.41 +/- 0.75 deg (solar angle)
- theta_23 = 49.1 +/- 1.0 deg (atmospheric angle, close to maximal)
- theta_13 = 8.54 +/- 0.12 deg (reactor angle)
- delta_CP = 194 +/- 25 deg

### 4.2 How Standard GUTs Explain the Difference

In SU(5) or SO(10) GUTs:
- **Quark sector:** M_u and M_d are both hierarchical. M_d ~ M_e^T (from 5_H Higgs) or M_d ~ -3 M_e^T (from 45_H, Georgi-Jarlskog). CKM is small because both mass matrices are nearly diagonal.
- **Lepton sector:** Charged lepton masses are hierarchical (related to M_d). Neutrino masses come from the seesaw: m_nu = -m_D M_R^{-1} m_D^T. If M_R has a specific structure (e.g., from SO(10) 126 Higgs), m_nu can be democratic or anarchical, giving large PMNS mixing.

### 4.3 What SU(9) Adds

The SU(9) framework provides:
1. **Three generations from SU(3)_family**: the number 3 is explained algebraically.
2. **SU(5) GUT structure**: quark-lepton unification within each generation.
3. **SU(9) CG coefficients**: potentially non-trivial ratios between sectors.
4. **E8 coupling normalization**: one overall Yukawa constant from E8 structure.

The SU(9) framework does NOT provide:
1. The flavon sector (must be specified by hand).
2. The right-handed neutrino mass matrix (must be specified by hand).
3. The symmetry-breaking pattern for SU(3)_family (multiple options).
4. Higher-dimensional operator coefficients.

### 4.4 Does SU(9) Provide Enough Higgs Freedom?

The 80-dimensional adjoint of SU(9) contains, under SU(5) x SU(3):

    80 = (24,1) + (1,8) + (1,1) + (5,3-bar) + (5-bar,3)

The Higgs fields that give fermion masses must come from the 80 (or from additional representations). The (24,1) component can give masses in the SU(5) sector. The (1,8) component is the SU(3)_family adjoint -- its VEV breaks SU(3)_family.

A Higgs in the (5,3-bar) of the 80 would give a BIFUNDAMENTAL Yukawa coupling, connecting the GUT and family sectors. This is analogous to the standard GUT Higgs but with family structure.

**Conclusion:** The SU(9) framework has enough Higgs freedom to accommodate both CKM and PMNS, but the specific outcome depends on which components of the 80 acquire VEVs and in what pattern.

---

## 5. Kill-Condition Analysis

### 5.1 Parameter Counting

**Observables (flavor sector):** 22 parameters
- 6 quark masses
- 3 charged lepton masses
- 3 neutrino masses
- 4 CKM parameters (3 angles + 1 phase)
- 6 PMNS parameters (3 angles + 1 Dirac phase + 2 Majorana phases)

**Model parameters (minimal SU(3)_family model):**

| Source | Parameters | Count |
|--------|-----------|-------|
| Overall Yukawa coupling | 1 real | 1 |
| SU(3)_family breaking VEV (3) | 2 complex ratios | 4 |
| SU(3)_family breaking VEV (3-bar) | 2 complex ratios | 4 |
| Up-type Yukawa coefficient | 1 complex | 2 |
| Down-type Yukawa coefficient | 1 complex | 2 |
| Lepton Yukawa coefficient | 1 complex | 2 |
| Seesaw parameters (M_R) | 3x3 symmetric matrix | 6 |
| **Total** | | **~21** |

### 5.2 Assessment

With ~21 parameters and 22 observables, the model has approximately 1 prediction in its minimal form. This is MARGINAL -- the model is barely predictive.

However, the SU(9) CG coefficients may impose ADDITIONAL constraints (reducing effective parameters by 1-3), which would increase predictivity to 2-4 predictions. This is the crucial unknown.

### 5.3 Kill-Condition Reformulation

The original kill condition (M8.4): "Yukawa texture is immediately inconsistent with measured CKM matrix elements."

**Revised kill condition:** The SU(9) CG coefficients, computed for the 84 x 84* x 80 coupling decomposed under SU(5) x SU(3)_family, impose specific RATIOS between quark and lepton Yukawa couplings. If these ratios are inconsistent with the measured GUT-scale mass ratios (specifically m_b/m_tau, m_s/m_mu, m_d/m_e extrapolated to M_GUT), the model is falsified.

**Falsification criterion:** If the SU(9) CG ratio for m_b/m_tau differs from the measured GUT-scale value (approximately 0.9-1.1 in the MSSM, or 1.5-2.5 in the SM) by more than a factor of 3, the model is FALSIFIED.

**Survival criterion:** If the CG ratio is within a factor of 3 of the measured value, the model SURVIVES and proceeds to detailed fitting.

### 5.4 Expected Outcome

Based on the analysis, the most likely outcome is:

**The SU(9) CG ratio for m_b/m_tau is exactly the SAME as the standard SU(5) GUT prediction** (either 1 from 5_H or 1/3 from 45_H), because the SU(9) embedding factorizes into SU(5) x SU(4) components, and the SU(4) part acts only on the family index.

If this is the case:
- The model SURVIVES the kill condition (CG ratio is consistent).
- But the model makes NO additional prediction beyond standard SU(5).
- The SU(9) framework reduces to SU(5) + SU(3)_family at the Yukawa level.
- The value added by SU(9) is purely at the UV level (explaining WHY three generations), not at the phenomenological level.

---

## 6. Computational Pathway

### 6.1 Tools

| Tool | Capability | Use Case |
|------|-----------|----------|
| **SageMath** | Branching rules, CG coefficients, Weyl characters | Primary computation tool |
| **LiE** | Fast tensor product decomposition, branching | Cross-check |
| **Susyno** | SUSY GUT model building (Mathematica) | If Mathematica is available |
| **Python/SymPy** | Symbolic mass matrix manipulation | Yukawa texture fitting |
| **Lean 4** | Machine verification of results | Final formalization |

### 6.2 SageMath Computation Plan

```python
# Step 1: Define representations
sage: A8 = WeylCharacterRing("A8", style="coroots")  # SU(9)
sage: A4 = WeylCharacterRing("A4", style="coroots")  # SU(5)
sage: A3 = WeylCharacterRing("A3", style="coroots")  # SU(4)

# Step 2: Define the 84 = Lambda^3(C^9)
sage: rep84 = A8(0,0,1,0,0,0,0,0)  # third fundamental weight of A8

# Step 3: Branch 84 under SU(5) x SU(4) x U(1)
# (need to specify the branching rule for A8 -> A4 x A3 x T1)

# Step 4: Compute tensor product 84 x 84*
sage: rep84_star = A8(0,0,0,0,0,1,0,0)  # conjugate
sage: product = rep84 * rep84_star  # tensor product decomposition

# Step 5: Extract the adjoint (80) component
# Look for A8(1,0,0,0,0,0,0,1) in the decomposition

# Step 6: Compute CG coefficients for the restricted coupling
# This requires the branching_rule function
```

### 6.3 Precision Requirements

The GUT-scale mass ratios are known to approximately 10-20% precision (from RG evolution). The SU(9) CG coefficients are exact rational numbers. Therefore, any factor-of-2 or larger discrepancy between the CG prediction and the measured ratio would constitute a clear falsification.

### 6.4 What We Need to Compute (Explicit List)

| # | Computation | Tool | Expected Effort | Kill Potential |
|---|------------|------|-----------------|----------------|
| 1 | 84 x 84* tensor product under SU(9) | SageMath | 1 hour | LOW |
| 2 | Verify adj appears once in 84 x 84* | SageMath | 30 min | NONE (theory guarantees it) |
| 3 | CG coefficients for 84 x 84* -> 80, decomposed under SU(5) x SU(4) | SageMath | 1-2 days | HIGH |
| 4 | Ratio of (10,3) vs (5-bar,3) CG coefficients | SageMath | 1 day | HIGH |
| 5 | Compare ratio to GUT-scale m_b/m_tau | Python | 1 hour | HIGH (if ratio is off) |
| 6 | Construct minimal flavon model | Python/SymPy | 3-5 days | MEDIUM |
| 7 | Fit to CKM + masses | Python | 2-3 days | MEDIUM |
| 8 | Predict PMNS (if quark fit works) | Python | 1-2 days | HIGH |
| 9 | Formalize key results in Lean 4 | Lean | 3-5 days | NONE |

**Total estimated effort: 2-3 weeks for complete analysis.**

---

## 7. Summary and Recommendations

### 7.1 Key Findings

1. **The SU(9) Yukawa coupling is unique at leading order** (Schur's lemma). This is established mathematics.

2. **The SU(3)-symmetric limit gives degenerate (not democratic) masses.** All three generations have equal mass; CKM = PMNS = identity. This corrects a common misconception.

3. **No one has computed SU(9) Yukawa CG coefficients.** The literature gap is significant. The most likely explanation is that the computation reduces to standard SU(5) + SU(3)_family, which has been extensively studied.

4. **The model is NOT immediately falsified.** Nothing in the SU(9) structure prevents realistic CKM or PMNS mixing. The kill condition cannot be evaluated without computing the CG coefficients.

5. **The model is UNDER-CONSTRAINED without specifying the flavon sector.** With a minimal flavon sector, the model has approximately 21 parameters for 22 observables -- barely predictive.

6. **The key computation is the CG ratio between quark and lepton sectors.** This ratio determines whether SU(9) adds information beyond generic SU(5) + SU(3)_family models.

### 7.2 Recommendation for M8 Kill-Condition

**Proceed to computation (M8.1-M8.3).** The kill condition is NOT triggered by theoretical analysis alone. The CG coefficient computation will determine:

- If CG ratio is inconsistent with data: **KILL. Publish as negative result.**
- If CG ratio equals standard SU(5) prediction: **SURVIVE but no new prediction.** The SU(9) framework adds UV understanding (why 3 generations) but no phenomenological content beyond SU(5) + SU(3)_family.
- If CG ratio is non-trivially different from SU(5) and consistent with data: **SURVIVE with prediction.** This would be a genuine result worth publishing.

### 7.3 Revised Milestone 8 Steps

| Step | Task | Status | Revised? |
|------|------|--------|----------|
| 8.0 | Literature survey + kill-condition analysis | **COMPLETE** (this document) | NEW |
| 8.1 | SU(9) CG coefficients via SageMath | NOT STARTED | SAME |
| 8.2 | CG ratio for (10,3) vs (5-bar,3) sectors | NOT STARTED | SAME |
| 8.3 | Compare CG ratio to GUT-scale m_b/m_tau | NOT STARTED | CLARIFIED |
| 8.4 | Kill condition: CG ratio inconsistent by >3x | NOT STARTED | REFORMULATED |
| 8.5 | If survives: minimal flavon model construction | NOT STARTED | SAME |
| 8.6 | If survives: fit to CKM + quark masses | NOT STARTED | SAME |
| 8.7 | If survives: predict PMNS | NOT STARTED | SAME |
| 8.8 | Paper 5 (if predictions survive) | NOT STARTED | SAME |

---

## Key Papers

| Paper | arXiv | Relevance |
|-------|-------|-----------|
| Bars & Gunaydin, "Grand Unification with E8" | PRL 45 (1980) 859 | Original E8 GUT |
| Slansky, "Group Theory for Unified Model Building" | Phys. Rep. 79 (1981) | E8 branching tables |
| Ramond, "The Family Group in GUTs" | hep-ph/9809459 | Family problem review |
| Altarelli & Feruglio, "Discrete Flavor Symmetries" | 1002.0211 | A4/S4 for PMNS |
| King & Luhn, "Neutrino Mass and Mixing with Discrete Symmetry" | 1301.1340 | SU(3)->discrete review |
| Barbieri, Hall et al, "U(2) Flavor Symmetry Predictions" | hep-ph/9512388 | U(2) Yukawa texture |
| Ross et al, "Yukawa Textures from Family Symmetry" | hep-ph/9703361 | Family+GUT textures |
| Froggatt & Nielsen, "Hierarchy of Quark Masses" | Nucl. Phys. B 147 (1979) | FN mechanism |
| Distler & Garibaldi, "No Theory of Everything in E8" | arXiv:0905.2658 | E8 chirality problem |
| Georgi & Jarlskog, "Mass Relations for Fermions" | Phys. Lett. B 86 (1979) | m_d/m_e GUT relation |
| Koca et al, "SU(9) decomposition of E8" | J. Math. Phys. (1989) | SU(9) branching details |

---

## Claim Tags

- [MV] All dimensional identities (84 = 10+40+30+4, etc.): machine-verified in Lean 4
- [SP] Schur's lemma, uniqueness of trilinear: standard mathematics
- [SP] Georgi-Jarlskog m_d/m_e relation: standard physics
- [SP] Seesaw mechanism for neutrino masses: standard physics
- [CO] Parameter counting (~21 parameters): computed estimate
- [CP] SU(9) CG ratio prediction: candidate physics, requires computation
- [OP] Whether SU(9) adds non-trivial Yukawa constraints beyond SU(5)+SU(3): open problem
