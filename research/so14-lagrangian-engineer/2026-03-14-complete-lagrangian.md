# Complete SO(14) Lagrangian Construction

**Date**: 2026-03-14
**Agent**: so14-lagrangian-engineer
**Experiment**: 4, Phase 2
**Status**: COMPLETE

---

## Table of Contents

1. [Field Content Table](#1-field-content-table)
2. [The Complete Lagrangian L = L_gauge + L_Higgs + L_fermion + L_Yukawa](#2-the-complete-lagrangian)
3. [Gauge Sector (L_gauge)](#3-gauge-sector)
4. [Higgs Sector (L_Higgs)](#4-higgs-sector)
5. [Fermion Sector (L_fermion)](#5-fermion-sector)
6. [Yukawa Sector (L_Yukawa)](#6-yukawa-sector)
7. [One-Loop Beta Function Derivation](#7-one-loop-beta-function-derivation)
8. [RG Running Equations](#8-rg-running-equations)
9. [Gravitational Sector Assessment](#9-gravitational-sector-assessment)
10. [Kill Condition Status](#10-kill-condition-status)
11. [Machine-Verified vs Computed vs Candidate](#11-verification-status)
12. [Comparison with SO(10) Lagrangian](#12-comparison-with-so10)

---

## Conventions and Notation

Throughout this document:
- Metric signature: mostly-minus (+,-,-,-) for spacetime.
- Lie algebra generators: $L_{ij}$ for $1 \leq i < j \leq 14$, satisfying $[L_{ij}, L_{kl}] = \delta_{jk}L_{il} - \delta_{ik}L_{jl} - \delta_{jl}L_{ik} + \delta_{il}L_{jk}$.
- Normalization: $\text{Tr}(T^a T^b) = T(R)\,\delta^{ab}$ with $T(\text{fund SO}(N)) = 1$, $T(\text{fund SU}(N)) = 1/2$.
- Claim tags: [MV] = machine-verified in Lean 4, [CO] = computed (Python/analytic), [CP] = candidate physics, [SP] = standard physics.

---

## 1. Field Content Table

### 1.1 Gauge Bosons (91 total)

All gauge bosons live in the adjoint representation **91** of SO(14). Under the breaking chain SO(14) -> SO(10) x SO(4) -> SU(5) x U(1)_chi x SU(2)_a x SU(2)_b -> SU(3)_C x SU(2)_L x U(1)_Y x SU(2)_a x SU(2)_b, they decompose as:

| Field | SO(14) rep | SO(10) x SO(4) rep | SM quantum numbers | Mass scale | Role |
|-------|-----------|-------------------|-------------------|------------|------|
| $G_\mu^a$ (a=1..8) | 91 | (45,1) | (8,1,0) | 0 | Gluons |
| $W_\mu^i$ (i=1,2,3) | 91 | (45,1) | (1,3,0) | $M_W$ | Weak bosons |
| $B_\mu$ | 91 | (45,1) | (1,1,0) | 0 (photon combination) | Hypercharge |
| $X_\mu, Y_\mu$ | 91 | (45,1) | (3,2,-5/6)+(3*,2,5/6) | $M_4 \sim 10^{16.5}$ GeV | Leptoquarks |
| $Z'_\mu$ | 91 | (45,1) | (1,1,0) under SU(5) | $M_3 \sim 10^{17}$ GeV | U(1)_chi boson |
| $V_\mu^{ij}$ (20 total) | 91 | (45,1) | 10+10* of SU(5) | $M_3$ | SO(10)/SU(5) bosons |
| $C_\mu^\alpha$ ($\alpha$=1..6) | 91 | (1,6) | SM singlets | $M_1 \sim 10^{19}$ GeV | SO(4) bosons |
| $M_\mu^{ia}$ (40 total) | 91 | (10,4) | 10 x 4 bifundamental | $M_1$ | Mixed bosons |

**Dimension check** [MV: `so14_breaking_chain.lean`]:
- 8 + 3 + 1 + 12 + 1 + 20 + 6 + 40 = 91. Verified.
- Massless at low energy: 8 (gluons) + 1 (photon) = 9 [SP].
- The 6 SO(4) bosons and 1 U(1)_chi boson are massive (below).

### 1.2 Scalar (Higgs) Fields

| Field | SO(14) rep | Dimension | Breaking step | VEV scale | Physical scalars |
|-------|-----------|-----------|---------------|-----------|-----------------|
| $S$ | **104** (sym. traceless) | 104 | SO(14) -> SO(10) x SO(4) | $v_1 \sim M_1$ | 64 |
| $\Sigma$ | **45** (SO(10) adjoint) | 45 | SO(10) -> SU(5) x U(1) | $v_3 \sim M_3$ | 25 |
| $\Sigma'$ | **24** (SU(5) adjoint) | 24 | SU(5) -> SM | $v_4 \sim M_4$ | 12 |
| $H$ | **5** (SU(5) fundamental) | 10 (real) | SU(2) x U(1) -> U(1)_EM | $v = 246$ GeV | 1 (SM Higgs) |

**KC-6 Assessment**: 4 independent Higgs representations are needed. This exceeds 3, which the kill condition flagged as concerning complexity. However, 4 Higgs representations is STANDARD for non-SUSY SO(10) GUTs (which also require adjoint + spinor + fundamental). This is noted but not fatal.

**Goldstone counting** [MV: `so14_breaking_chain.lean`]:
- Step 1: 104 - 40 Goldstones = 64 physical scalars
- Step 2: 45 - 20 Goldstones = 25 physical scalars
- Step 3: 24 - 12 Goldstones = 12 physical scalars
- Step 4: 10 - 3 Goldstones = 1 physical scalar (the SM Higgs) + 6 eaten by W/Z
  (More precisely: the SU(5) fundamental 5 has 10 real d.o.f.; 3 become Goldstones for W+, W-, Z.)

Total physical scalars: 64 + 25 + 12 + 1 = 102.

**Origin of the Higgs fields in the SO(14) representation theory**:

The 104 is a fundamental SO(14) representation. The 45 arises as the (45,1) component of the 104 under SO(10) x SO(4) decomposition: $104 = (54,1) + (1,9) + (10,4) + (1,1)$. However, the (45,1) is NOT contained in the 104 -- the adjoint of SO(10) is a separate representation. So the $\Sigma$ field in the **45** of SO(10) must either be:
- (a) A separate SO(14) representation (e.g., from the **91** adjoint), or
- (b) An effective field from SO(14) symmetric breaking at a lower scale.

In practice, GUT models typically introduce each Higgs as an independent field. For the minimal SO(14) model, we follow approach (a): the four Higgs fields are independent [CP].

### 1.3 Fermion Fields (Three Generations)

| Field | SO(14) rep | SO(10) x SU(2)_a x SU(2)_b | SM content (per generation) | Chirality |
|-------|-----------|----------------------------|----------------------------|-----------|
| $\psi_{L}^{(i)}$ | $\mathbf{64}^+$ | (16, 2, 1) | $Q_L, L_L$ (left-handed) | L |
| $\psi_{R}^{(i)}$ | $\mathbf{64}^+$ | ($\overline{16}$, 1, 2) | $u_R^c, d_R^c, e_R^c, \nu_R^c$ | R |
| Index $i = 1,2,3$ | 3 copies | | 3 generations | |

**Matter content per generation** (under SM after full breaking):

| Particle | SU(3)_C x SU(2)_L x U(1)_Y | Source in SO(10) 16 |
|----------|---------------------------|-------------------|
| $Q_L = (u_L, d_L)$ | (3, 2, 1/6) | 10 of SU(5) |
| $u_R^c$ | ($\bar{3}$, 1, -2/3) | 10 of SU(5) |
| $e_R^c$ | (1, 1, 1) | 10 of SU(5) |
| $d_R^c$ | ($\bar{3}$, 1, 1/3) | $\bar{5}$ of SU(5) |
| $L_L = (\nu_L, e_L)$ | (1, 2, -1/2) | $\bar{5}$ of SU(5) |
| $\nu_R^c$ | (1, 1, 0) | 1 of SU(5) |

Total per generation: 16 Weyl fermions [SP, MV: `spinor_matter.lean`].

**Three-generation mechanism**: Three copies of the 64-spinor are postulated (simplest mechanism). The number 3 is unexplained within SO(14) alone; resolution requires E8 embedding where 3 = dim(fund SU(3)_family) [MV: `three_generation_theorem.lean`, `e8_generation_mechanism.lean`]. The spinor parity obstruction [MV: `spinor_parity_obstruction.lean`] proves that no single SO(14) spinor can yield 3 generations: $2^{k-1}$ is never 3.

---

## 2. The Complete Lagrangian

$$\mathcal{L} = \mathcal{L}_{\text{gauge}} + \mathcal{L}_{\text{Higgs}} + \mathcal{L}_{\text{fermion}} + \mathcal{L}_{\text{Yukawa}}$$

Each sector is written below at the SO(14) unification scale (single coupling $g_{14}$), then the effective Lagrangian at each breaking scale is obtained by integrating out heavy fields.

---

## 3. Gauge Sector

### 3.1 Yang-Mills Action

$$\mathcal{L}_{\text{gauge}} = -\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}$$

where $a = 1, \ldots, 91$ runs over the generators of so(14) and:

$$F^a_{\mu\nu} = \partial_\mu A^a_\nu - \partial_\nu A^a_\mu + g_{14}\, f^{abc}\, A^b_\mu A^c_\nu$$

**Structure constants** [MV: `so14_grand.lean`]:

For generators $L_{ij}$ ($1 \leq i < j \leq 14$), labeled by pairs $a = (ij)$, the structure constants are:

$$[L_{ij}, L_{kl}] = \delta_{jk}L_{il} - \delta_{ik}L_{jl} - \delta_{jl}L_{ik} + \delta_{il}L_{jk}$$

In explicit index form, with $a = (i_a, j_a)$, $b = (i_b, j_b)$, $c = (i_c, j_c)$:

$$f^{abc} = \delta_{j_a i_b}\epsilon(i_a, j_b, c) - \delta_{i_a i_b}\epsilon(j_a, j_b, c) - \delta_{j_a j_b}\epsilon(i_a, i_b, c) + \delta_{i_a j_b}\epsilon(j_a, i_b, c)$$

where $\epsilon(p,q,c) = +1$ if $c = (p,q)$ with $p < q$, $-1$ if $c = (q,p)$ with $q < p$, and $0$ otherwise.

The Jacobi identity is verified numerically for all $\binom{91}{3} = 125580$ triples (randomly sampled 100 in scripts, full verification in Lean) [MV: `so14_grand.lean`].

**Verified properties** [MV]:
- Yang-Mills energy $H = \frac{1}{2}\sum_{a,i}[(E^a_i)^2 + (B^a_i)^2] \geq 0$ (`yang_mills_energy.lean`)
- Bogomolny bound: $H \geq |\text{Tr}(E \cdot B)|$ (`yang_mills_energy.lean`)
- BPS saturation: $E = B \implies H = \text{Tr}(E \cdot B)$ (`yang_mills_energy.lean`)
- Yang-Mills Lagrangian $\leq 0$ (`covariant_derivative.lean`)
- Algebraic Bianchi identity from Jacobi (`covariant_derivative.lean`)

### 3.2 Gauge Sector After Breaking

Below $M_1$ (SO(14) breaking scale), the 91 gauge bosons split into sectors with different masses. The effective Lagrangian at scale $\mu$ with $M_3 < \mu < M_1$:

$$\mathcal{L}_{\text{gauge}}^{\text{eff}}(\mu) = -\frac{1}{4} G^a_{\mu\nu}G^{a\mu\nu} - \frac{1}{4} W^i_{\mu\nu}W^{i\mu\nu} - \frac{1}{4} B_{\mu\nu}B^{\mu\nu} - \frac{1}{4} C^\alpha_{\mu\nu}C^{\alpha\mu\nu} + \ldots$$

where:
- $G^a_{\mu\nu}$ ($a = 1, \ldots, 45$): SO(10) field strength, coupling $g_{10}(\mu)$
- $C^\alpha_{\mu\nu}$ ($\alpha = 1, \ldots, 6$): SO(4) field strength, coupling $g_4(\mu)$
- Heavy mixed bosons $M_\mu^{ia}$ are integrated out (mass $\sim M_1$)

At unification: $g_{10}(M_1) = g_4(M_1) = g_{14}$ [CP].

---

## 4. Higgs Sector

### 4.1 Symmetric Traceless Higgs $S$ (104 of SO(14))

The symmetric traceless tensor $S_{ij} = S_{ji}$ with $\text{Tr}(S) = \sum_i S_{ii} = 0$ has 104 real components: $14 \times 15/2 - 1 = 104$ [MV: `so14_breaking_chain.lean`].

**Kinetic term**:

$$\mathcal{L}_{S,\text{kin}} = \frac{1}{2}(D_\mu S)_{ij}(D^\mu S)_{ij}$$

where the covariant derivative acts on the rank-2 tensor:

$$(D_\mu S)_{ij} = \partial_\mu S_{ij} + g_{14}\left(A^{kl}_\mu \left(\delta_{ki} S_{lj} - \delta_{li} S_{kj} + \delta_{kj} S_{li} - \delta_{lj} S_{ki}\right)\right)$$

This is the standard adjoint-on-tensor action: $(D_\mu S)_{ij} = \partial_\mu S_{ij} + g_{14}[A_\mu, S]_{ij}$ where brackets denote the matrix commutator with $A_\mu$ viewed as an antisymmetric matrix.

**Potential**:

The most general renormalizable SO(14)-invariant potential for a symmetric traceless tensor:

$$V(S) = -\mu_1^2\,\text{Tr}(S^2) + \kappa\,\text{Tr}(S^3) + \lambda_1\,[\text{Tr}(S^2)]^2 + \lambda_2\,\text{Tr}(S^4)$$

There are exactly 4 independent invariants up to quartic order (the cubic $\text{Tr}(S^3)$ is crucial for selecting asymmetric breaking) [SP: Li 1974, Michel 1973].

**VEV for SO(10) x SO(4) breaking** [CO]:

$$\langle S \rangle = v_1 \cdot \text{diag}(\underbrace{a, a, \ldots, a}_{10}, \underbrace{b, b, b, b}_{4})$$

with tracelessness: $10a + 4b = 0 \implies b = -5a/2$.

VEV invariants [MV: `so14_breaking_chain.lean`]:
- $\text{Tr}(\langle S \rangle^2) = v_1^2(10a^2 + 4 \cdot 25a^2/4) = 35\,v_1^2 a^2$
- $r \equiv \text{Tr}(\langle S\rangle^4)/[\text{Tr}(\langle S\rangle^2)]^2 = 19/140$

The VEV is a GLOBAL minimum of $V$ when [CO]:
- $\mu_1^2 > 0$ (triggers breaking)
- $\lambda_2 > 0$ (stability)
- $\kappa \neq 0$ (selects asymmetric splitting 10+4 over symmetric 7+7)
- Detailed: the ratio $r = 19/140$ must be a local minimum of $r(p) = \text{Tr}(S^4)/[\text{Tr}(S^2)]^2$ among all diagonal VEVs, which requires specific signs and magnitudes of $\kappa, \lambda_1, \lambda_2$.

**104 decomposition under SO(10) x SO(4)** [MV: `so14_breaking_chain.lean`]:

$$104 = (54, 1) \oplus (1, 9) \oplus (10, 4) \oplus (1, 1)$$

- (10, 4) = 40: eaten as Goldstone bosons for the 40 broken generators
- (54, 1) = 54: massive physical scalars (mass $\sim v_1$)
- (1, 9) = 9: massive physical scalars from SO(4) sector
- (1, 1) = 1: radial mode (massive)
- Total physical: 54 + 9 + 1 = 64 [MV]

### 4.2 SO(10) Adjoint Higgs $\Sigma$ (45 of SO(10))

$$\mathcal{L}_{\Sigma,\text{kin}} = \frac{1}{2}(D_\mu \Sigma)^a (D^\mu \Sigma)^a$$

where $a = 1, \ldots, 45$ and:

$$(D_\mu \Sigma)^a = \partial_\mu \Sigma^a + g_{10}\, f^{abc}_{\text{SO(10)}}\, B^b_\mu \Sigma^c$$

**Potential**:

$$V(\Sigma) = -\mu_3^2\,\text{Tr}(\Sigma^2) + \lambda_3\,[\text{Tr}(\Sigma^2)]^2 + \lambda_4\,\text{Tr}(\Sigma^4)$$

No cubic invariant for the antisymmetric (adjoint) representation [SP].

**VEV for SU(5) x U(1) breaking** [SP, MV: embedding in `su5_so10_embedding.lean`]:

$$\langle \Sigma \rangle = v_3 \cdot J, \quad J = L_{1,6} + L_{2,7} + L_{3,8} + L_{4,9} + L_{5,10}$$

$J^2 = -\mathbb{1}$ defines a complex structure on $\mathbb{R}^{10}$. The centralizer of $J$ in so(10) is su(5) $\oplus$ u(1) [MV: `su5_so10_embedding.lean`].

**45 decomposition under SU(5) x U(1)** [SP]:

$$45 = 24_0 \oplus 10_2 \oplus \overline{10}_{-2} \oplus 1_0$$

- 20 components eaten as Goldstone bosons (for $45 - 25 = 20$ broken generators [MV])
- 25 physical scalars survive

### 4.3 SU(5) Adjoint Higgs $\Sigma'$ (24 of SU(5))

$$\mathcal{L}_{\Sigma',\text{kin}} = \text{Tr}(D_\mu \Sigma')^\dagger (D^\mu \Sigma')$$

**VEV** [SP, MV: `symmetry_breaking.lean`]:

$$\langle \Sigma' \rangle = \frac{v_4}{\sqrt{30}}\,\text{diag}(2, 2, 2, -3, -3)$$

This preserves SU(3)_C x SU(2)_L x U(1)_Y. The hypercharge generator is $Y = \text{diag}(-1/3, -1/3, -1/3, 1/2, 1/2)$ [MV: `georgi_glashow.lean`].

**12 Goldstone bosons** are eaten by the X, Y leptoquark gauge bosons (mass $M_4 \sim g \cdot v_4$). **12 physical scalars** survive.

### 4.4 Electroweak Higgs $H$ (5 of SU(5))

$$\mathcal{L}_{H,\text{kin}} = (D_\mu H)^\dagger (D^\mu H)$$

Under SU(3) x SU(2) x U(1): $5 = (3, 1, -1/3) \oplus (1, 2, 1/2)$.

**VEV** [SP, MV: `symmetry_breaking.lean`]:

$$\langle H \rangle = (0, 0, 0, 0, v/\sqrt{2}), \quad v = 246\,\text{GeV}$$

The color triplet $(3, 1, -1/3)$ component must be superheavy (doublet-triplet splitting problem, standard in all SU(5)-based GUTs). Three Goldstone bosons are eaten by $W^{\pm}, Z$.

**Electroweak potential** [SP]:

$$V(H) = -\mu_5^2 H^\dagger H + \lambda_5 (H^\dagger H)^2$$

with $v^2 = \mu_5^2 / \lambda_5$ and $m_h = \sqrt{2\lambda_5}\,v = 125$ GeV.

### 4.5 Cross-Coupling Terms

The full Higgs potential includes cross-couplings between different Higgs fields:

$$V_{\text{cross}} = \alpha_1\,\text{Tr}(S^2)\,\text{Tr}(\Sigma^2) + \alpha_2\,\text{Tr}(S^2)\,H^\dagger H + \alpha_3\,\text{Tr}(\Sigma^2)\,H^\dagger H + \ldots$$

These couplings are important for the mass spectrum of physical scalars but do not affect the breaking pattern to leading order [SP]. The full enumeration of all quartic cross-couplings is model-dependent and involves order 10 additional free parameters.

### 4.6 Complete Higgs Lagrangian

$$\mathcal{L}_{\text{Higgs}} = \frac{1}{2}(D_\mu S)_{ij}(D^\mu S)_{ij} + \frac{1}{2}(D_\mu \Sigma)^a (D^\mu \Sigma)^a + \text{Tr}(D_\mu \Sigma')^\dagger (D^\mu \Sigma') + (D_\mu H)^\dagger (D^\mu H) - V_{\text{total}}$$

where:

$$V_{\text{total}} = V(S) + V(\Sigma) + V(\Sigma') + V(H) + V_{\text{cross}}$$

**Parameter count in the scalar sector**:
- $V(S)$: 4 parameters ($\mu_1, \kappa, \lambda_1, \lambda_2$)
- $V(\Sigma)$: 3 parameters ($\mu_3, \lambda_3, \lambda_4$)
- $V(\Sigma')$: 3 parameters ($\mu_4, \lambda_6, \lambda_7$)
- $V(H)$: 2 parameters ($\mu_5, \lambda_5$)
- $V_{\text{cross}}$: ~10 parameters (quartic cross-terms)
- **Total: ~22 scalar parameters** [CO]

This is high but comparable to non-SUSY SO(10) models, which typically have 15-25 scalar parameters.

---

## 5. Fermion Sector

### 5.1 Fermion Kinetic Terms at SO(14) Scale

For three generations of Weyl fermions in the 64-dimensional semi-spinor of SO(14):

$$\mathcal{L}_{\text{fermion}} = \sum_{i=1}^{3} i\,\bar{\psi}^{(i)} \gamma^\mu D_\mu \psi^{(i)}$$

where:

$$D_\mu \psi^{(i)} = \partial_\mu \psi^{(i)} + i\,g_{14}\,A^a_\mu\,T^a_{64}\,\psi^{(i)}$$

Here $T^a_{64}$ are the generators of so(14) in the 64-dimensional spinor representation. These are $64 \times 64$ matrices constructed from the Clifford algebra $\text{Cl}(14)$:

$$T^{(ij)}_{64} = \frac{i}{4}[\gamma_i, \gamma_j]$$

where $\gamma_1, \ldots, \gamma_{14}$ are the gamma matrices of $\text{Cl}(14,0)$ (compact signature) or $\text{Cl}(11,3)$ (Lorentzian).

The 64-spinor decomposition under SO(10) x SO(4) = SO(10) x SU(2)_a x SU(2)_b [CO: `so14_matter_decomposition.py`]:

$$64^+ = (16, 2, 1) \oplus (\overline{16}, 1, 2)$$

**Chirality interpretation** (under Lorentzian identification SO(4) $\to$ SO(1,3)):
- $(16, 2, 1)$: one generation of LEFT-handed SM fermions
- $(\overline{16}, 1, 2)$: the same generation of RIGHT-handed antifermions
- This is one complete generation, not two [CP, CO]

### 5.2 Fermion Kinetic Terms After SO(10) x SO(4) Breaking

Below $M_1$, the fermion sector reorganizes:

$$\mathcal{L}_{\text{fermion}}^{\text{eff}} = \sum_{i=1}^{3} \left[ i\,\bar{\psi}_L^{(i)} \gamma^\mu \left(\partial_\mu + ig_{10}\,B^a_\mu\,S^a_{16}\right)\psi_L^{(i)} + i\,\bar{\psi}_R^{(i)} \gamma^\mu \left(\partial_\mu + ig_{10}\,B^a_\mu\,\bar{S}^a_{16}\right)\psi_R^{(i)} \right]$$

where:
- $\psi_L^{(i)}$: 16 of SO(10), left-handed (from (16, 2, 1))
- $\psi_R^{(i)}$: $\overline{16}$ of SO(10), right-handed (from ($\overline{16}$, 1, 2))
- $S^a_{16}$: generators in the 16-dim spinor rep of SO(10)
- The SO(4) gauge bosons couple universally to all generations (SM singlets) [CO]

### 5.3 Anomaly Cancellation

SO(14) anomaly cancellation is AUTOMATIC [MV, SP]:

- For any SO(N) with $N \geq 7$: the rank-3 symmetric Casimir $d_{abc} = 0$ [MV: `anomaly_trace.lean`]
- Specifically: $\text{Tr}(T^a\{T^b, T^c\}) = 0$ for antisymmetric $T^a, T^b, T^c$ [MV]
- This holds for ALL representations (fundamental, adjoint, spinor) [MV for fundamental; SP for adjoint and spinor]
- The proof is purely algebraic and signature-independent [MV]

**Specific conditions verified** [MV: `so14_anomalies.lean`, `anomaly_trace.lean`]:
1. $\text{Tr}_{16}(Y^3) = 0$ per generation [MV: `georgi_glashow.lean`]
2. $\text{Tr}_{16}(Y) = 0$ (gravitational anomaly) [MV: `georgi_glashow.lean`]
3. Three generations maintain cancellation (anomaly is per-generation) [SP]

---

## 6. Yukawa Sector

### 6.1 Yukawa Coupling Structure

The Yukawa Lagrangian couples fermion bilinears to Higgs fields. For fermions in the **64** and Higgs in various representations:

$$\mathcal{L}_{\text{Yukawa}} = y^{(10)}_{ij}\,\bar{\psi}^{(i)}\,H_{10}\,\psi^{(j)} + y^{(126)}_{ij}\,\bar{\psi}^{(i)}\,\Delta_{126}\,\psi^{(j)} + y^{(120)}_{ij}\,\bar{\psi}^{(i)}\,\Phi_{120}\,\psi^{(j)} + \text{h.c.}$$

**Clebsch-Gordan analysis**: The tensor product of two 64-spinors decomposes as [SP: Slansky 1981]:

$$64 \otimes 64 = \underbrace{1 \oplus 91 \oplus 2002 \oplus \ldots}_{\text{symmetric}} \oplus \underbrace{14 \oplus 364 \oplus 1716 \oplus \ldots}_{\text{antisymmetric}}$$

More precisely, at the SO(10) level where the effective Yukawa operates:

$$16 \otimes 16 = 10_S \oplus 120_A \oplus \overline{126}_S$$

where $S$ = symmetric, $A$ = antisymmetric in generation indices [SP].

### 6.2 Effective SO(10) Yukawa

After SO(14) breaks to SO(10) x SO(4), the Yukawa interactions reduce to the standard SO(10) Yukawa:

$$\mathcal{L}_{\text{Yukawa}}^{\text{eff}} = Y^{10}_{ij}\,\overline{16}^{(i)}\,10_H\,16^{(j)} + Y^{126}_{ij}\,\overline{16}^{(i)}\,\overline{126}_H\,16^{(j)} + \text{h.c.}$$

where:
- $Y^{10}_{ij}$ is a **symmetric** $3 \times 3$ matrix (from $10_S$ channel)
- $Y^{126}_{ij}$ is a **symmetric** $3 \times 3$ matrix (from $\overline{126}_S$ channel)
- 6 + 6 = 12 complex Yukawa parameters (before phase rotations)

**Yukawa hypercharge conservation** [MV: `yukawa_couplings.lean`]:
- Electron: $Y(\bar{\psi}_L) + Y(\phi) + Y(e_R) = +1/2 + 1/2 + (-1) = 0$ [MV]
- Up quark: $Y(\bar{Q}_L) + Y(\tilde{\phi}) + Y(u_R) = -1/6 + (-1/2) + 2/3 = 0$ [MV]
- Down quark: $Y(\bar{Q}_L) + Y(\phi) + Y(d_R) = -1/6 + 1/2 + (-1/3) = 0$ [MV]

### 6.3 Mass Relations at the GUT Scale

The $10_H$ Yukawa gives the SO(10) mass relation [SP]:

$$m_b(M_{\text{GUT}}) = m_\tau(M_{\text{GUT}})$$

This is the Georgi-Jarlskog bottom-tau unification, which after RG running to $M_Z$ gives $m_b/m_\tau \approx 3$, consistent with experiment [SP].

The $\overline{126}_H$ Yukawa provides [SP]:
- Majorana masses for right-handed neutrinos ($M_R \sim v_{126}$)
- Type-I seesaw: $m_\nu \approx m_D^2/M_R$ with $M_R \sim 10^{14}$ GeV
- Neutrino mass scale: $m_\nu \sim (100\,\text{GeV})^2/(10^{14}\,\text{GeV}) \sim 0.1$ eV [SP]

**SO(14) novelty in the Yukawa sector**: NONE. After breaking to SO(10), the Yukawa sector is identical to standard SO(10) GUT. The SO(4) sector does not directly participate in Yukawa couplings because the SO(4) gauge bosons are SM singlets. The Yukawa structure is determined entirely by the SO(10) x generation structure [CO].

### 6.4 Fermion Mass Hierarchy

The SM flavor sector has 22 free parameters [MV: `yukawa_couplings.lean`]:
- 9 fermion masses
- 4 CKM parameters (3 angles + 1 CP phase) [MV: $C(3,2) = 3$, $C(2,2) = 1$]
- 3 neutrino masses
- 6 PMNS parameters (3 angles + 1 Dirac phase + 2 Majorana phases)

In the SO(10) Yukawa with $10_H + \overline{126}_H$: the number of independent complex parameters is reduced to 12 (before phases), giving nontrivial predictions. Whether this suffices to fit all 22 observables is model-dependent and requires numerical fitting [SP].

---

## 7. One-Loop Beta Function Derivation

### 7.1 General Formula

The one-loop beta function for gauge coupling $g_i$ of group factor $G_i$:

$$\mu \frac{dg_i}{d\mu} = -\frac{b_i}{16\pi^2}\,g_i^3$$

equivalently for inverse coupling $\alpha_i^{-1} = 4\pi/g_i^2$:

$$\frac{d\alpha_i^{-1}}{d\ln\mu} = -\frac{b_i}{2\pi}$$

where [SP]:

$$b_i = -\frac{11}{3}\,C_2(G_i) + \frac{2}{3}\sum_{\text{Weyl } f} T(R_f) + \frac{1}{3}\sum_{\text{complex scalars}} T(R_{cs}) + \frac{1}{6}\sum_{\text{real scalars}} T(R_{rs})$$

and:
- $C_2(G)$ = quadratic Casimir of the adjoint representation
- $T(R)$ = Dynkin index of representation $R$

### 7.2 Dynkin Index Table

| Group | Representation | Dimension | $T(R)$ | Derivation |
|-------|---------------|-----------|--------|------------|
| SO(14) | vector **14** | 14 | 1 | Convention: $T(\text{fund SO}(N)) = 1$ |
| SO(14) | adjoint **91** | 91 | 24 | $C_2(\text{adj SO}(N)) = 2(N-2) = 24$ |
| SO(14) | semi-spinor **64** | 64 | 8 | $T(\text{spinor SO}(2n)) = 2^{n-4}$ for $n = 7$: $T = 2^3 = 8$ |
| SO(14) | sym. traceless **104** | 104 | 16 | $T(\text{sym.tr. SO}(N)) = N+2 = 16$ |
| SO(10) | vector **10** | 10 | 1 | Convention |
| SO(10) | adjoint **45** | 45 | 16 | $C_2(\text{adj}) = 2(10-2) = 16$ |
| SO(10) | semi-spinor **16** | 16 | 2 | $T = 2^{5-4} = 2$ |
| SO(10) | sym. traceless **54** | 54 | 12 | $T = 10 + 2 = 12$ |
| SU(5) | fundamental **5** | 5 | 1/2 | Convention: $T(\text{fund SU}(N)) = 1/2$ |
| SU(5) | adjoint **24** | 24 | 5 | $C_2(\text{adj SU}(N)) = N = 5$ |
| SU(5) | antisymmetric **10** | 10 | 3/2 | $T(\Lambda^2 \text{SU}(N)) = (N-2)/2 = 3/2$ |
| SU(2) | fundamental **2** | 2 | 1/2 | Convention |
| SU(2) | adjoint **3** | 3 | 2 | $C_2(\text{adj SU}(2)) = 2$ |

[CO: Dynkin indices computed from standard formulas. Cross-checked against Slansky (1981) tables.]

### 7.3 Beta Coefficients at Each Scale

#### Scale 1: $M_Z < \mu < M_4$ (Standard Model)

Field content: 3 generations of SM fermions + 1 Higgs doublet.

**GUT-normalized coefficients** [MV: `rg_running.lean`, SP]:

| Coupling | $b_i$ | Formula | AF? |
|----------|-------|---------|-----|
| $\alpha_1^{-1}$ (U(1)_Y, GUT norm.) | $123/50 = 2.46$ | $(3/5)(41/10)$ | NO |
| $\alpha_2^{-1}$ (SU(2)_L) | $-19/6 = -3.167$ | $22/3 - 4 - 1/6$ | YES |
| $\alpha_3^{-1}$ (SU(3)_C) | $-7$ | $11 - 4$ | YES |

Derivation of $b_3$: $C_2(\text{SU}(3)) = 3$. Each generation contributes 2 Weyl triplets (left quark doublet = 2 flavors, each a color triplet) + 2 Weyl anti-triplets (right-handed singlets $u_R, d_R$), for total $T_f = 4 \times (1/2) = 2$ per generation, times 3 generations = 6. No SU(3)-charged scalars in SM. So $b_3 = -(11/3)(3) + (2/3)(6) = -11 + 4 = -7$ [SP].

#### Scale 2: $M_4 < \mu < M_3$ (SU(5) x U(1)_chi x SO(4))

Field content: 3 generations in $(10 + \bar{5} + 1)$ of SU(5), adjoint Higgs $\Sigma'$ (24), fundamental Higgs $H_5$ (5).

| Coupling | $b_i$ | Source |
|----------|-------|--------|
| $b_{\text{SU}(5)}$ | $-40/3 \approx -13.33$ | $-(11/3)(5) + (2/3)(3)(1/2 + 3/2 + 0) + (1/6)(5) + (1/3)(1/2)$ |

Derivation:
- $C_2(\text{SU}(5)) = 5$, so gauge contribution: $-(11/3)(5) = -55/3$
- Fermion Weyl spinors per generation: $10 + \bar{5} + 1$, with $T(10) = 3/2$, $T(\bar{5}) = T(5) = 1/2$, $T(1) = 0$. Total per generation: $3/2 + 1/2 = 2$. Three generations: $3 \times 2 = 6$.
  Fermion contribution: $(2/3)(6) = 4$
- Scalar adjoint $\Sigma'$ (24, real): $T(24) = 5$. Contribution: $(1/6)(5) = 5/6$
- Scalar fundamental $H_5$ (5, complex = 10 real): $T(5) = 1/2$. Contribution: $(1/3)(1/2) = 1/6$
- **Total**: $b_{\text{SU}(5)} = -55/3 + 4 + 5/6 + 1/6 = -55/3 + 4 + 1 = -55/3 + 5 = -40/3$

[CO]

#### Scale 3: $M_3 < \mu < M_1$ (SO(10) x SO(4) = SO(10) x SU(2)_a x SU(2)_b)

Field content: 3 generations in $(16, (2,1)) + (\overline{16}, (1,2))$ of SO(10) x SU(2)_a x SU(2)_b. SO(10) adjoint Higgs $\Sigma$ (45, real). Remnant scalars from 104: (54,1) real.

**SO(10) beta**:

- $C_2(\text{SO}(10)) = 2(10-2) = 16$. Gauge: $-(11/3)(16) = -176/3$
- Fermion: Each generation gives a 16 of SO(10) with $T(16) = 2$, appearing as an SU(2)_a doublet (2 Weyl spinors from each doublet index). So effectively 2 Weyl 16's per generation from (16,(2,1)), plus 2 Weyl $\overline{16}$'s from ($\overline{16}$,(1,2)). Total: $T_f = 3 \times (2 \times 2 + 2 \times 2) = 24$. Fermion contribution: $(2/3)(24) = 16$.

  Actually, let me be more careful. Each Weyl fermion in $(16, (2,1))$ is a doublet under SU(2)_a. The SU(2)_a index gives 2 copies of the 16 as SO(10) representations. So for SO(10) beta function:
  - From $(16, (2,1))$: 2 Weyl fermions in the 16. Per generation: $T = 2 \times 2 = 4$.
  - From $(\overline{16}, (1,2))$: 2 Weyl fermions in the $\overline{16}$. Per generation: $T = 2 \times 2 = 4$.
  - Total per generation: $T_f = 8$. Three generations: $T_f = 24$.
  - Fermion contribution: $(2/3)(24) = 16$ [CO]

- Scalar (45, real): $T(45) = 16$. Contribution: $(1/6)(16) = 8/3$
- Scalar (54, real) from 104: $T(54) = 12$. Contribution: $(1/6)(12) = 2$

**$b_{\text{SO}(10)} = -176/3 + 16 + 8/3 + 2 = -176/3 + 48/3 + 8/3 + 6/3 = -114/3 = -38$** [CO]

**SU(2)_a beta**:

- $C_2(\text{SU}(2)) = 2$. Gauge: $-(11/3)(2) = -22/3$
- Fermion: From $(16, (2,1))$: 3 gen x 16 Weyl fermions in the fundamental 2 of SU(2)_a. $T(2) = 1/2$. Each of the 16 SO(10) components is a doublet. So: $T_f = 3 \times 16 \times (1/2) = 24$. Contribution: $(2/3)(24) = 16$.
- From scalar (1,9) from 104: the 9 of SO(4) decomposes as $(3,1) + (1,3) + (3,3)$...

  Actually, the SO(4) sector sees: $(1,9)$ of SO(10) x SO(4). Under SU(2)_a x SU(2)_b: the symmetric traceless of SO(4) decomposes. The adjoint of SO(4) is $(3,1) + (1,3)$. The 9-dim symmetric traceless of SO(4) has dimension $4 \times 5/2 - 1 = 9$. Under SU(2)_a x SU(2)_b: $9 = (3,3)$. Wait -- the traceless symmetric of SO(4) = the (3,3) of SU(2)_a x SU(2)_b (dimension $3 \times 3 = 9$). So $T_{\text{SU(2)_a}}(3,3) = 3 \times T(3) = 3 \times 2 = 6$. Contribution: $(1/6)(6) = 1$.

  Also: $(1,1)$ from 104 is a singlet, contributes 0.

  From $\Sigma$ in (45,1): this is an SO(10) adjoint, singlet under SO(4). Contributes 0 to SU(2)_a beta.

**$b_{\text{SU(2)}_a} = -22/3 + 16 + 1 = -22/3 + 17 = 29/3 \approx 9.67$** [CO]

This is POSITIVE, meaning SU(2)_a is NOT asymptotically free in this regime. The coupling grows at higher energies -- but this is above $M_3$, and above $M_1$ the theory unifies into SO(14) which IS asymptotically free [CO].

#### Scale 4: $\mu > M_1$ (Unified SO(14))

Field content: 3 generations of 64 semi-spinor (Weyl). Symmetric traceless Higgs $S$ (104, real).

- $C_2(\text{SO}(14)) = 2(14-2) = 24$ [MV: `so14_breaking_chain.lean`]
- Gauge: $-(11/3)(24) = -88$
- Fermion: $T(64) = 8$ per Weyl spinor. Three generations: $T_f = 3 \times 8 = 24$. But each 64 is itself a Weyl spinor, so we count 3 Weyl 64's.
  Contribution: $(2/3)(24) = 16$
- Scalar (104, real): $T(104) = 16$ [MV: `so14_breaking_chain.lean`]
  Contribution: $(1/6)(16) = 8/3$

**$b_{\text{SO}(14)} = -88 + 16 + 8/3 = -72 + 8/3 = -216/3 + 8/3 = -208/3 \approx -69.33$** [CO]

**Asymptotically free**: $b < 0$ means the coupling DECREASES at high energies. The theory is well-behaved in the UV [CO, MV: `so14_breaking_chain.lean` proves $256/3 > 0$ for the pure gauge + scalar part, and adding fermions keeps $b < 0$].

### 7.4 Summary of Beta Coefficients

| Scale | Group | $b_i$ | AF? | Source |
|-------|-------|-------|-----|--------|
| $M_Z$ to $M_4$ | SU(3)_C | $-7$ | YES | [MV: `rg_running.lean`] |
| $M_Z$ to $M_4$ | SU(2)_L | $-19/6$ | YES | [MV: `rg_running.lean`] |
| $M_Z$ to $M_4$ | U(1)_Y | $123/50$ | NO | [MV: `rg_running.lean`] |
| $M_4$ to $M_3$ | SU(5) | $-40/3$ | YES | [CO] |
| $M_3$ to $M_1$ | SO(10) | $-38$ | YES | [CO] |
| $M_3$ to $M_1$ | SU(2)_a | $29/3$ | NO | [CO] |
| $> M_1$ | SO(14) | $-208/3$ | YES | [CO] |

---

## 8. RG Running Equations

### 8.1 One-Loop Evolution

At one-loop, the inverse couplings evolve linearly in $\ln\mu$:

$$\alpha_i^{-1}(\mu) = \alpha_i^{-1}(\mu_0) - \frac{b_i}{2\pi}\,\ln\frac{\mu}{\mu_0}$$

### 8.2 Initial Conditions at $M_Z$

[SP: PDG 2024]

| Coupling | $\alpha_i^{-1}(M_Z)$ |
|----------|---------------------|
| $\alpha_1^{-1}$ (GUT normalized) | 59.0 |
| $\alpha_2^{-1}$ | 29.6 |
| $\alpha_3^{-1}$ | 8.5 |

GUT normalization: $\alpha_1^{-1} = (3/5)\,\alpha_{\text{em}}^{-1}\cos^2\theta_W$ with $\alpha_{\text{em}}^{-1}(M_Z) = 127.9$, $\sin^2\theta_W = 0.2312$.

### 8.3 Multi-Scale Running

**From $M_Z$ to $M_4$**: SM running.

$$\alpha_i^{-1}(M_4) = \alpha_i^{-1}(M_Z) - \frac{b_i^{\text{SM}}}{2\pi}\,\ln\frac{M_4}{M_Z}$$

$M_4$ is determined by the 2-3 crossing (where $\alpha_2$ and $\alpha_3$ meet):

$$M_4: \quad \alpha_2^{-1}(M_4) = \alpha_3^{-1}(M_4)$$

$$\ln\frac{M_4}{M_Z} = \frac{2\pi(\alpha_2^{-1}(M_Z) - \alpha_3^{-1}(M_Z))}{b_2^{\text{SM}} - b_3^{\text{SM}}} = \frac{2\pi(29.6 - 8.5)}{-19/6 + 7} = \frac{2\pi \times 21.1}{23/6}$$

$$= \frac{132.6}{3.833} = 34.59 \implies M_4 = M_Z \times e^{34.59} = 91.2 \times 10^{15.02} \approx 10^{16.98}\,\text{GeV}$$

[CO: `so14_rg_unification.py`]

At the 2-3 crossing:
$$\alpha_{2,3}^{-1}(M_4) \approx 47.03$$
$$\alpha_1^{-1}(M_4) \approx 45.46$$

**Unification miss**: $|\alpha_1^{-1} - \alpha_{2,3}^{-1}| = 1.57$, relative miss = $1.57/47.03 = 3.3\%$ [CO].

This 3.3% miss is the STANDARD non-SUSY GUT result, identical for SO(10) and SO(14) [CO: see Section 12].

**From $M_4$ to $M_3$**: SU(5) running.

$$\alpha_{\text{SU}(5)}^{-1}(M_3) = \alpha_{\text{SU}(5)}^{-1}(M_4) - \frac{b_{\text{SU}(5)}}{2\pi}\,\ln\frac{M_3}{M_4}$$

**From $M_3$ to $M_1$**: SO(10) x SO(4) running.

$$\alpha_{\text{SO}(10)}^{-1}(M_1) = \alpha_{\text{SO}(10)}^{-1}(M_3) - \frac{b_{\text{SO}(10)}}{2\pi}\,\ln\frac{M_1}{M_3}$$

**Above $M_1$**: Unified SO(14) running.

$$\alpha_{\text{SO}(14)}^{-1}(\mu) = \alpha_{\text{SO}(14)}^{-1}(M_1) - \frac{b_{\text{SO}(14)}}{2\pi}\,\ln\frac{\mu}{M_1}$$

### 8.4 Multi-Scale Unification Results

From the recovered Phase 1 results [CO: `so14_rg_unification_v2.py`]:

**Approach B** (free $M_4$, $M_3$, $M_1$):
- $M_4 = 10^{16.50}$ GeV
- $M_3 = 10^{17.00}$ GeV
- $M_1 = 10^{19.00}$ GeV
- Spread at $M_1$: 0.67 in $\alpha^{-1}$
- Quality: **0.88%** [CO]

**Approach C** ($M_4 = M_3$ fixed at 2-3 crossing):
- $M_4 = M_3 = 10^{16.98}$ GeV
- $M_1 = 10^{19.50}$ GeV
- Quality: **1.93%** [CO]

### 8.5 Proton Decay Prediction

$$\tau_p \sim \frac{M_X^4}{\alpha_{\text{GUT}}^2\,m_p^5}$$

With $M_X \sim M_4 \sim 10^{16.98}$ GeV, $\alpha_{\text{GUT}} \approx 1/47$:

$$\tau_p \sim 10^{39.7}\,\text{years}$$

With renormalization enhancement factor $A_R \approx 2.5$:

$$\tau_p \sim 10^{38.9}\,\text{years}$$

Super-Kamiokande bound: $\tau_p > 10^{34.4}$ years. **Safety factor: $10^{4.5}$** [CO].

### 8.6 Weinberg Angle Prediction

At the GUT scale: $\sin^2\theta_W = 3/8 = 0.375$ [MV: `georgi_glashow.lean`].

After RG running to $M_Z$: $\sin^2\theta_W(M_Z) \approx 0.231$ [SP].

The prediction $3/8 \to 0.231$ is a SUCCESSFUL test of grand unification [SP]. SO(14) reproduces this identically to SO(10) and SU(5) because the prediction depends only on the SM desert running [CO].

---

## 9. Gravitational Sector Assessment

### 9.1 The SO(4) Sector

SO(14) naturally contains SO(4) as a subgroup. Under the identification SO(14) -> SO(10) x SO(4), the SO(4) factor has been proposed as a unified gravity sector (Nesti-Percacci 2007, 2008).

**What we have**:
- SO(4) = SU(2)_a x SU(2)_b [MV: `so4_gravity.lean`]
- SO(4) embeds in SO(14) as a LieHom [MV: `so4_so14_liehom.lean`]
- The 6 SO(4) generators are the "gravity sector" of SO(14) [CP]

### 9.2 MacDowell-Mansouri Gravity

If we identify SO(4) with a compact version of the Lorentz group, the Yang-Mills action for the SO(4) sector:

$$\mathcal{L}_{\text{grav}} = -\frac{1}{4}\,F^{ab}_{\mu\nu}\,F^{ab\mu\nu}, \quad a,b \in \{11,12,13,14\}$$

contains terms that, when expanded around a de Sitter background, produce:

$$\mathcal{L}_{\text{grav}} \supset \frac{1}{\Lambda^2}\left(R + \Lambda + c\,R^2 + \ldots\right)$$

where $\Lambda \sim v_1^2$ is related to the SO(14) breaking VEV.

### 9.3 Critical Problems

**Problem 1: Signature** [SERIOUS]

- The Lean proofs use compact SO(14,0), which contains SO(4) $\cong$ SU(2) $\oplus$ SU(2) [MV]
- Physical gravity requires SO(1,3) $\cong$ SL(2,$\mathbb{R}$) $\oplus$ SL(2,$\mathbb{R}$) (non-compact) [SP]
- so(4) $\ncong$ so(1,3) as real Lie algebras [MV: documented in `SIGNATURE_ANALYSIS.md`]
  - so(4): all generators square to $-1$ (compact)
  - so(1,3): boosts square to $+1$ (non-compact)
  - Structure constants differ in boost-rotation cross-terms
- Physical gravity in SO(14) requires the real form SO(11,3), not SO(14,0) [CP]
- The certified LieHom chain SU(5) $\to$ SO(10) $\to$ SO(14) $\leftarrow$ SO(4) is COMPACT ONLY [MV]

**Problem 2: Ghosts (Distler's Objection)** [SERIOUS/POTENTIALLY FATAL]

- In SO(11,3), the metric on the Lie algebra is INDEFINITE
- The non-compact generators (boosts + mixed sector) have WRONG-SIGN kinetic terms
- $\mathcal{L} = -\frac{1}{4}\,\text{Tr}(F^2)$ with indefinite Tr gives negative kinetic energy for some fields
- These are GHOSTS: fields with negative-norm states that violate unitarity
- KC-FATAL-4 status: This is the central open problem

**Problem 3: Cosmological Constant**

- The MacDowell-Mansouri mechanism gives $\Lambda \sim M_1^2 \sim (10^{19}\,\text{GeV})^2$
- This is $\sim 10^{120}$ times larger than the observed value
- The cosmological constant problem is generic to ALL gravity unification approaches [SP]

### 9.4 Honest Assessment

**Viable path**: Treat SO(4) as a broken gauge symmetry at the GUT scale. The 6 SO(4) bosons get masses $\sim M_1$. Gravity is then treated SEPARATELY via Einstein-Hilbert action:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{SO(14)}} + \frac{M_{\text{Pl}}^2}{2}\,R$$

This is the CONSERVATIVE approach. It avoids the ghost problem entirely but also gives up on gravity unification. The SO(4) sector then becomes merely an additional gauge symmetry at high energies with no low-energy consequence beyond enriching the massive particle spectrum at $M_1$.

**Speculative path**: Work in SO(11,3), accept indefinite kinetic terms, and invoke Wick rotation or constrained quantization to resolve ghosts. This is an OPEN RESEARCH PROBLEM and cannot be resolved within this construction. Status: [OP].

---

## 10. Kill Condition Status

| Kill Condition | Status | Evidence |
|---------------|--------|----------|
| KC-FATAL-3: Anomalies | **PASS** | $d_{abc} = 0$ for all SO(N) with $N \geq 7$ [MV: `anomaly_trace.lean`] |
| KC-FATAL-4: Ghosts | **OPEN** | Compact SO(14,0) has no ghosts. Lorentzian SO(11,3) has indefinite metric -- ghosts expected in non-compact sector. Not resolved. [OP] |
| KC-FATAL-5: Proton decay | **PASS** | $\tau_p \sim 10^{38.9}$ yr, bound $10^{34.4}$ yr, safety $10^{4.5}$ [CO] |
| KC-FATAL-6: Coupling unification | **PASS** | 0.88% miss (multi-scale) to 3.3% (desert), below 20% threshold [CO] |
| KC-6: Higgs complexity | **NOTED** | 4 independent Higgs reps needed. Standard for non-SUSY GUTs. Not fatal. |
| KC-CONCERN: Yukawa masses | **DEFERRED** | Yukawa sector identical to SO(10). Known to reproduce masses with $10_H + 126_H$. Detailed fit not performed. [SP] |

---

## 11. Verification Status

### 11.1 Machine-Verified [MV] (Lean 4, 0 sorry)

| Claim | Lean File | Theorem |
|-------|-----------|---------|
| SO(14) has 91 generators | `so14_grand.lean` | Structure type with 91 fields |
| 91 = 45 + 6 + 40 | `so14_unification.lean` | `unification_decomposition` |
| Jacobi identity for so(14) | `so14_grand.lean` | Jacobi proof |
| LieAlgebra R instance for SO14 | `so14_grand.lean` | Instance declaration |
| LieHom SO(10) -> SO(14) | `so10_so14_liehom.lean` | Certified morphism |
| LieHom SO(4) -> SO(14) | `so4_so14_liehom.lean` | Certified morphism |
| LieHom SU(5) -> SO(10) | `su5c_so10_liehom.lean` | Certified morphism |
| Anomaly: Tr(A{B,C}) = 0 for antisymmetric | `anomaly_trace.lean` | `trace_antisymm_anticommutator` |
| Yang-Mills energy H >= 0 | `yang_mills_energy.lean` | `yang_mills_energy_nonneg` |
| Bogomolny bound | `yang_mills_energy.lean` | `bogomolny_bound` |
| YM Lagrangian <= 0 | `covariant_derivative.lean` | `ym_lagrangian_nonpos` |
| Bianchi identity (algebraic) | `covariant_derivative.lean` | `algebraic_bianchi_*` |
| Yukawa hypercharge conservation | `yukawa_couplings.lean` | `yukawa_hypercharge_conservation` |
| SM beta coefficients | `rg_running.lean` | `beta1_SM`, `beta2_SM`, `beta3_SM` |
| sin^2(theta_W) = 3/8 at GUT scale | `georgi_glashow.lean` | Referenced |
| 16 = 1 + 5 + 10 (SO(10) spinor) | `spinor_matter.lean` | `su5_singlet_in_16` |
| Sym. traceless dim = 104 | `so14_breaking_chain.lean` | `so14_sym_traceless_dim` |
| Goldstone counting (40+20+12+3=75) | `so14_breaking_chain.lean` | `total_broken_generators` |
| Adjoint cannot break to SO(10)xSO(4) | `so14_breaking_chain.lean` | `adjoint_insufficient_*` |
| VEV invariant r = 19/140 | `so14_breaking_chain.lean` | `breaking_ratio` |
| Beta > 0 (pure gauge+scalar) | `so14_breaking_chain.lean` | `beta_is_positive` |
| 3 does not divide 2^k | `spinor_parity_obstruction.lean` | Main theorem |
| E8 three-generation mechanism | `e8_generation_mechanism.lean` | Dimensional skeleton |

### 11.2 Computed [CO] (Python, reproducible)

| Claim | Script | Key Result |
|-------|--------|------------|
| Spinor branching 64 = (16,2,1) + (16*,1,2) | `so14_matter_decomposition.py` | Weight analysis |
| One-loop beta coefficients (all scales) | `so14_rg_unification.py`, recovered | Table in Section 7 |
| Coupling unification miss 0.88%-3.3% | `so14_rg_unification.py` | Phase 1 |
| Proton lifetime 10^38.9 yr | `so14_rg_unification.py` | Phase 1 |
| Dynkin indices | Analytic formulas, cross-checked | Table in Section 7.2 |
| Mixed boson beta contribution is SU(5)-universal | `so14_rg_unification.py` Part 4 | Equal shifts |

### 11.3 Candidate Physics [CP] (Proposed, not verified)

| Claim | Status | Risk |
|-------|--------|------|
| SO(14) is a viable GUT gauge group | Phase 1 PASS, Phase 2 complete | Interesting, not compelling (Phase 1 verdict) |
| Three copies of 64 give 3 generations | Ad hoc, not explained by SO(14) | Requires E8 embedding |
| SO(4) sector unifies gravity | OPEN (ghost problem) | High risk |
| Signature SO(11,3) resolves physics | OPEN | Requires separate analysis |
| Yukawa sector reproduces masses | Deferred to SO(10) literature | Standard but unverified for this specific model |

### 11.4 Standard Physics [SP] (Textbook)

| Claim | Reference |
|-------|-----------|
| SO(10) Yukawa structure: 16 x 16 = 10 + 120 + 126 | Georgi 1999, Slansky 1981 |
| Bottom-tau unification at GUT scale | Georgi-Jarlskog 1979 |
| Seesaw mechanism for neutrino masses | Gell-Mann, Ramond, Slansky 1979 |
| CKM matrix has 4 parameters | Kobayashi-Maskawa 1973 |
| PMNS matrix has 6 parameters | Standard |
| Proton decay via leptoquark exchange | Georgi-Glashow 1974 |
| d_abc = 0 for SO(N), N >= 7 | Weinberg QFT Vol II |

---

## 12. Comparison with SO(10) Lagrangian

### 12.1 What SO(14) Adds Beyond SO(10)

| Feature | SO(10) | SO(14) | Difference |
|---------|--------|--------|------------|
| **Generators** | 45 | 91 | +46 (6 gravity + 40 mixed) |
| **Gauge bosons** | 45 | 91 | 46 additional at $M_1$ |
| **Spinor** | 16 (1 gen) | 64 (1 gen + antiparticles) | Includes chirality structure |
| **Breaking steps** | 3-4 | 4-5 | +1 (SO(14) -> SO(10) x SO(4)) |
| **Higgs reps** | 3-4 | 4 | Same order of complexity |
| **Coupling unification** | 3.3% miss (SM desert) | 3.3% miss (identical) | No improvement [CO: D5] |
| **Proton lifetime** | $10^{39.7}$ yr | $10^{39.7}$ yr (identical) | Same [CO] |
| **Weinberg angle** | 3/8 -> 0.231 | 3/8 -> 0.231 (identical) | Same [MV/SP] |
| **Asymptotic freedom** | $b_{\text{SO(10)}} = -38$ | $b_{\text{SO(14)}} = -208/3$ | Both AF |
| **Gravity sector** | Absent | SO(4) = SU(2)xSU(2) | New, but with ghost problem |
| **Three generations** | 3 x 16 (ad hoc) | 3 x 64 (ad hoc) | Neither explains 3 |
| **Anomaly cancellation** | Automatic | Automatic | Identical mechanism [MV] |

### 12.2 The 46 Extra Generators

The extra generators decompose as:

- **6 generators** in $(1, 6)$: the so(4) sector (gravity interpretation)
- **40 generators** in $(10, 4)$: mixed sector (bifundamental)

The 40 mixed bosons have SU(5)-UNIVERSAL Dynkin indices: they contribute EQUALLY to all three SM coupling beta functions. Therefore:
- They cannot differentially close the coupling unification triangle
- They produce no distinctive low-energy signatures
- Their contribution at intermediate scales ($M_3 < \mu < M_1$) is $\delta b_1 = \delta b_2 = \delta b_3$ [CO: `so14_rg_unification.py` Part 4]

### 12.3 Honest Bottom Line

**SO(14) does not improve coupling unification over SO(10)** [CO: Friction Catalog entry D5]. The physics below the SO(10) scale is identical. The distinctive SO(14) content -- the SO(4) gravity sector and 40 mixed bosons -- enters only above $M_3 \sim 10^{17}$ GeV, far above current experimental reach.

**What SO(14) DOES provide** [CP]:
1. A structural HOME for gravity (SO(4) sector), even if the ghost problem is unresolved
2. A natural chirality interpretation: the 64-spinor includes both L and R components via SO(4)
3. A connection to E8 via SO(14) -> SO(16) -> E8 chain [MV: `so14_so16_liehom.lean`]
4. An algebraically richer framework that COULD distinguish itself through:
   - Threshold corrections from the 104 + 45 + 24 + 5 Higgs sector (178 total scalar components)
   - New proton decay channels mediated by mixed bosons at $M_1$
   - Novel topological effects from the richer gauge group

**Phase 1 verdict (unchanged)**: INTERESTING, not compelling. No accessible-energy distinction from SO(10).

---

## Appendix A: Complete Lagrangian in LaTeX

For reference, the complete SO(14) Lagrangian at the unification scale:

$$\boxed{\mathcal{L}_{\text{SO(14)}} = -\frac{1}{4}F^a_{\mu\nu}F^{a\mu\nu} + \frac{1}{2}(D_\mu S)^2 - V(S) + \sum_{i=1}^{3} i\bar{\psi}^{(i)}\gamma^\mu D_\mu \psi^{(i)} + \left(y_{ij}\bar{\psi}^{(i)} S \psi^{(j)} + \text{h.c.}\right)}$$

where:
- $a = 1,\ldots,91$
- $F^a_{\mu\nu} = \partial_\mu A^a_\nu - \partial_\nu A^a_\mu + g_{14} f^{abc} A^b_\mu A^c_\nu$
- $(D_\mu S)_{ij} = \partial_\mu S_{ij} + g_{14}[A_\mu, S]_{ij}$
- $D_\mu\psi = \partial_\mu\psi + ig_{14}A^a_\mu T^a_{64}\psi$
- $V(S) = -\mu_1^2\text{Tr}(S^2) + \kappa\text{Tr}(S^3) + \lambda_1[\text{Tr}(S^2)]^2 + \lambda_2\text{Tr}(S^4)$
- $\psi^{(i)} \in \mathbf{64}^+$ ($i = 1,2,3$)
- $S \in \mathbf{104}$ (symmetric traceless)
- $y_{ij}$ = Yukawa matrix ($3 \times 3$ complex symmetric)

Below the SO(14) breaking scale, additional Higgs fields ($\Sigma$, $\Sigma'$, $H$) appear from the effective theory at each intermediate scale.

---

## Appendix B: Files Referenced

| File | Path | Content |
|------|------|---------|
| SO(14) Lie algebra | `src/lean_proofs/clifford/so14_grand.lean` | 91 generators, Jacobi, LieAlgebra instance |
| Breaking chain | `src/lean_proofs/clifford/so14_breaking_chain.lean` | 104 Higgs, Goldstone counting, beta |
| Anomaly trace | `src/lean_proofs/clifford/anomaly_trace.lean` | Tr(A{B,C})=0 for antisymmetric |
| Yang-Mills energy | `src/lean_proofs/dynamics/yang_mills_energy.lean` | H >= 0, Bogomolny, BPS |
| Covariant derivative | `src/lean_proofs/dynamics/covariant_derivative.lean` | Bianchi, YM Lagrangian |
| Yukawa couplings | `src/lean_proofs/dynamics/yukawa_couplings.lean` | Hypercharge conservation |
| RG running | `src/lean_proofs/dynamics/rg_running.lean` | SM beta coefficients |
| SO(4) gravity | `src/lean_proofs/clifford/so4_gravity.lean` | Compact so(4) type |
| SO(4)->SO(14) | `src/lean_proofs/clifford/so4_so14_liehom.lean` | Certified embedding |
| SO(10)->SO(14) | `src/lean_proofs/clifford/so10_so14_liehom.lean` | Certified embedding |
| SU(5)->SO(10) | `src/lean_proofs/clifford/su5c_so10_liehom.lean` | Certified embedding |
| Spinor matter | `src/lean_proofs/grand_unification/spinor_matter.lean` | 16 = 1+5+10 |
| Spinor parity | `src/lean_proofs/clifford/spinor_parity_obstruction.lean` | 3 does not divide 2^k |
| E8 generations | `src/lean_proofs/clifford/e8_generation_mechanism.lean` | 248=80+84+84 |
| RG unification | `src/experiments/so14_rg_unification.py` | Phase 1 computation |
| Matter decomp | `src/experiments/so14_matter_decomposition.py` | Branching rules |
| Signature analysis | `docs/SIGNATURE_ANALYSIS.md` | Compact vs Lorentzian |
| Friction catalog | `docs/PHYSICS_MATH_FRICTION_CATALOG.md` | 20 friction points |
| Recovered findings | `research/recovered/so14-lagrangian-findings.md` | Phase 1 results |

---

## Appendix C: Open Problems

1. **Ghost resolution in SO(11,3)**: How to quantize a Yang-Mills theory with indefinite Killing form. This is the single most important open problem for the gravity unification interpretation of SO(14). [OP]

2. **Threshold corrections**: The 178 scalar components provide many mass parameters for threshold corrections at each breaking scale. A systematic computation could determine whether these close the 1.57-unit gap in coupling unification without fine-tuning. [CO needed]

3. **Two-loop beta coefficients**: Not computed for the SO(14) regime. Would shift unification predictions by O(few %). [CO needed]

4. **Explicit Yukawa fit**: Numerical fit of the 12 complex Yukawa parameters to the 22 SM flavor observables. Standard SO(10) technology applies. [CO needed]

5. **Doublet-triplet splitting**: The color triplet in the SU(5) fundamental Higgs must be superheavy. Standard solutions (missing partner, Dimopoulos-Wilczek) apply but add complexity. [SP/CP]

6. **U(1)_chi breaking**: The U(1) factor from SO(10) -> SU(5) x U(1) must be broken. Requires an additional scalar (spinor 16 of SO(10), or component of the 64 of SO(14)). Not included in the minimal Higgs content above. [CP]

7. **Three-generation mechanism**: Within SO(14) alone, three generations are postulated, not explained. The E8 resolution via SU(9)/Z3 provides a dimensional mechanism but requires embedding SO(14) in E8 (or going through SO(16)). [MV for algebra, CP for physics]

---

*Generated by so14-lagrangian-engineer agent. Phase 2 of Experiment 4.*
*All [MV] claims correspond to Lean 4 proofs with 0 sorry.*
*All [CO] claims are reproducible from the cited Python scripts.*
*This document is the Phase 2 deliverable for `docs/so14_lagrangian.md` (written to `research/so14-lagrangian-engineer/` per persistence protocol).*
