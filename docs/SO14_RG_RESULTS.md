# SO(14) Renormalization Group Results

**Date**: 2026-03-09
**Status**: Phase 1 Complete -- Both kill conditions PASS (GREEN)
**Script**: `src/experiments/so14_rg_unification_v2.py`
**Data**: `src/experiments/results/so14_rg_unification_v2_results.json`

## Executive Summary

The SO(14) candidate theory passes both pre-registered kill conditions for coupling
unification and proton decay. The theory is viable with the same caveats as any
non-supersymmetric GUT. The SO(14) breaking chain introduces no new fatal problems
beyond those already present in SO(10).

## 1. Beta Function Table

| Scale | Gauge Group | Beta Coefficient | Asymptotically Free? |
|-------|-------------|-----------------|---------------------|
| M_Z to M_4 | SU(3) | b_3 = -7.0 | YES |
| M_Z to M_4 | SU(2) | b_2 = -19/6 = -3.167 | YES |
| M_Z to M_4 | U(1)_Y | b_1 = 123/50 = 2.46 (GUT norm.) | NO |
| M_4 to M_3 | SU(5) | b_SU5 = -40/3 = -13.33 | YES |
| M_3 to M_1 | SO(10) | b_SO10 = -38.0 | YES |
| M_3 to M_1 | SU(2)_a | b_SU2a = 29/3 = 9.67 | NO |
| > M_1 | SO(14) | b_SO14 = -208/3 = -69.33 | YES |

### Field Content at Each Scale

**SM (M_Z to M_4)**: Standard Model with right-handed neutrino. SM betas
are machine-verified in `rg_running.lean` [MV].

**SU(5) x U(1)_chi (M_4 to M_3)**:
- 3 generations of (10 + 5bar + 1) Weyl fermions
- Adjoint Higgs Sigma' (24 real), fundamental Higgs H_5 (5 complex = 10 real)
- C_2(SU(5)) = 5, T_f = 6, scalar = (1/6)*5 + (1/3)*(1/2) = 1.0

**SO(10) x SO(4) (M_3 to M_1)**:
- 3 generations of [(16, (2,1)) + (16bar, (1,2))] under SO(10) x SU(2)_a x SU(2)_b
- SO(10) adjoint Higgs Sigma (45 real), remnant (54,1) scalars from 104
- C_2(SO(10)) = 16, T_f(SO(10)) = 24, scalar = (1/6)*(12+16) = 14/3

**SO(14) (above M_1)**:
- 3 x 64 semi-spinor Weyl fermions
- Symmetric traceless Higgs S (104 real)
- C_2(SO(14)) = 24, T_f = 24, scalar = (1/6)*16 = 8/3
- Asymptotically free: b_SO14 = -208/3 < 0 [CO]

### Dynkin Indices Used

| Group | Representation | Dimension | T(R) |
|-------|---------------|-----------|------|
| SO(14) | vector 14 | 14 | 1 |
| SO(14) | adjoint 91 | 91 | 24 |
| SO(14) | spinor 64 | 64 | 8 |
| SO(14) | sym.traceless 104 | 104 | 16 |
| SO(10) | vector 10 | 10 | 1 |
| SO(10) | adjoint 45 | 45 | 16 |
| SO(10) | spinor 16 | 16 | 2 |
| SO(10) | sym.traceless 54 | 54 | 12 |
| SU(5) | fundamental 5 | 5 | 1/2 |
| SU(5) | adjoint 24 | 24 | 5 |
| SU(5) | antisymmetric 10 | 10 | 3/2 |
| SU(2) | fundamental 2 | 2 | 1/2 |
| SU(2) | adjoint 3 | 3 | 2 |

Convention: T(fund SO(N)) = 1, T(fund SU(N)) = 1/2.

## 2. Best-Fit Unification Parameters

### Desert Hypothesis (single scale)

| Parameter | Value |
|-----------|-------|
| M_GUT | 10^16.98 GeV |
| alpha_GUT^{-1} | 47.03 |
| alpha_1^{-1} at M_GUT | 45.46 |
| Absolute miss | 1.57 |
| Relative miss | 3.3% |

### Multi-Scale Approach B (free M_4, M_3, M_1)

| Parameter | Value |
|-----------|-------|
| M_4 (SU(5) breaking) | 10^16.50 GeV |
| M_3 (SO(10) breaking) | 10^17.00 GeV |
| M_1 (SO(14) breaking) | 10^19.00 GeV |
| Spread at M_1 | 0.67 |
| Quality (spread/avg) | 0.88% |

### Multi-Scale Approach C (M_4 fixed at 2-3 crossing)

| Parameter | Value |
|-----------|-------|
| M_4 = M_3 | 10^16.98 GeV |
| M_1 | 10^19.50 GeV |
| a_SU5^{-1}(M_3) | 47.03 |
| a_chi^{-1}(M_3) | 45.46 |
| Gap at M_1 | 1.57 |
| Quality | 1.93% |

**Key finding**: The gap between alpha_1 and alpha_{2,3} is preserved
through the multi-scale chain. The SO(10) and SO(14) betas are LARGE
and negative, which pushes the unified coupling to large alpha^{-1}
(weak coupling) at M_1, but the absolute gap of ~1.57 stays fixed
because both lines evolve with the same SO(10) beta above M_3.

## 3. Proton Lifetime Prediction

| Quantity | Desert | Multi-scale C |
|----------|--------|---------------|
| M_X (X boson mass) | 10^16.98 GeV | 10^16.98 GeV |
| alpha_GUT | 1/47.03 | 1/47.03 |
| tau_p (dimensional) | 10^39.7 years | 10^39.7 years |
| tau_p (with A_R = 2.5) | 10^38.9 years | 10^38.9 years |
| Super-K bound | 10^34.4 years | 10^34.4 years |
| Safety factor | 3.5 x 10^4 | 3.5 x 10^4 |

The proton lifetime is safe by 4-5 orders of magnitude above the
experimental bound. This is because M_GUT ~ 10^17 GeV is high
(tau_p ~ M_X^4), and alpha_GUT ~ 1/47 is small.

Note: The proton lifetime depends on M_4 (the SU(5) breaking scale),
not on M_1 or M_3. The X and Y leptoquark bosons that mediate proton
decay get their mass at M_4.

## 4. Coupling Unification Plot

The plot is saved at:
`src/experiments/results/so14_rg_unification_v2.png`

**Left panel**: SM desert running. Three couplings converge but do not
exactly meet. The spread at the 2-3 crossing is 1.57 units of alpha^{-1}
(3.3% relative miss). This is the well-known non-SUSY GUT triangle.

**Right panel**: Multi-scale SO(14) breaking chain. Shows SM couplings
merging into SU(5) at M_4, then SU(5) + U(1)_chi evolving to M_3,
SO(10) from M_3 to M_1, and SO(14) above M_1. Vertical dashed lines
mark the breaking scales.

## 5. Kill Condition Verdicts

### KC-FATAL-5: Proton Decay

**Status: GREEN (PASS)**

tau_p = 10^38.9 years >> 10^34.4 years (Super-K bound)

Safety factor: 3.5 x 10^4. Even with substantial model-dependent corrections
(nuclear matrix elements, running masses), the proton lifetime remains safely
above the experimental bound.

### KC-FATAL-6: Coupling Unification

**Status: GREEN (PASS)**

Best miss: 0.88% (Approach B) to 3.3% (desert). All well below the 20%
threshold for kill condition firing.

The ~3.3% miss is the standard non-SUSY GUT result. It is NOT specific to
SO(14) and can be closed by:
- Threshold corrections from the rich Higgs sector (104 + 45 + 24 + 5)
- Two-loop corrections
- Split multiplet spectra
- SUSY at an intermediate scale

## 6. Comparison with SO(10)

| Feature | SO(10) | SO(14) |
|---------|--------|--------|
| Desert miss | 3.3% | 3.3% (identical) |
| Multi-scale miss (best) | N/A | 0.88% |
| Proton lifetime | 10^39.7 yr | 10^39.7 yr (identical) |
| Asymptotic freedom | YES | YES |
| Additional scales | 0 | 1 (M_1) |
| Additional gauge bosons | 0 | 46 (6 gravity + 40 mixed) |
| SO(4) sector | absent | present (SU(2)_a x SU(2)_b) |

**Key differences**:

1. SO(14) introduces one additional breaking scale M_1 above the SO(10) scale.
   This does NOT improve coupling unification because the (10,4) mixed bosons
   contribute equally to all three SM beta functions.

2. The SO(4) = SU(2)_a x SU(2)_b sector is entirely decoupled from the SM
   coupling evolution (SM singlets). Its beta coefficient b_SU2a = 29/3 > 0
   means the SU(2) factors are NOT asymptotically free in the SO(10) x SO(4) regime.

3. The proton lifetime is identical because it depends only on M_4 and alpha_GUT,
   both of which are determined by the SM couplings at M_Z and the SM betas.

4. The multi-scale freedom (Approach B) allows a modest improvement from 3.3% to
   0.88%, but this comes from tracking three couplings with different betas through
   intermediate matching conditions, not from any SO(14)-specific physics.

**Bottom line**: SO(14) does not make coupling unification BETTER or WORSE than
SO(10). The physics is dominated by the SM desert regime (M_Z to M_4), where the
betas are identical. The SO(14)-specific physics (SO(4) sector, mixed bosons)
lives above M_GUT and is irrelevant for the coupling evolution.

## 7. Technical Notes

### Beta Function Formula

```
b_i = -(11/3)*C_2(G_i) + (2/3)*sum_f T(R_f) + (1/3)*sum_cs T(R_cs) + (1/6)*sum_rs T(R_rs)
```

where:
- sum_f runs over Weyl fermions
- sum_cs runs over complex scalars
- sum_rs runs over real scalars
All Dynkin indices use the convention T(fund SO(N)) = 1, T(fund SU(N)) = 1/2.

### GUT Normalization

The U(1)_Y coupling is normalized as:
```
alpha_1^{GUT} = (5/3) * alpha_Y
```
so that alpha_1 = alpha_2 = alpha_3 at exact SU(5) unification.
This gives b_1^{GUT} = (3/5) * b_1^Y = (3/5)(41/10) = 123/50.

Machine-verified: `beta1_gut_normalized` in `rg_running.lean` [MV].

### Evolution Formula

```
alpha_i^{-1}(mu) = alpha_i^{-1}(mu_0) - b_i/(2*pi) * ln(mu/mu_0)
```

### Proton Decay Formula

```
tau_p ~ M_X^4 / (alpha_GUT^2 * m_p^5) [natural units]
```

Convert to years: multiply by hbar / (seconds_per_year).

With renormalization enhancement: tau_p -> tau_p / A_R^2, where A_R ~ 2.5.

### Claim Tags

- [MV] Machine-verified: SM beta coefficients (`rg_running.lean`), SO(14) dimension
  and decomposition (`so14_unification.lean`), breaking chain Higgs reps
  (`so14_breaking_chain.lean`), anomaly freedom (`so14_anomalies.lean`)
- [CO] Computed: All beta functions, RG running, proton decay (this script)
- [SP] Standard physics: SM couplings at M_Z, proton mass, Super-K bound
- [CP] Candidate physics: SO(14) as unified group, 3 x 64 matter content

## 8. Open Questions

1. **Threshold corrections**: The rich Higgs sector (104 + 45 + 24 + 5 = 178
   scalar components) provides many parameters for threshold corrections. A
   dedicated computation could determine whether these naturally close the 1.57
   unit gap without fine-tuning.

2. **Two-loop corrections**: The 2-loop beta coefficients for SO(14) have not been
   computed. These could shift the unification scale and quality.

3. **Proton decay channels**: The SO(14) theory has additional gauge bosons beyond
   the SU(5) X and Y bosons. The (10,4) mixed bosons mediate new processes that
   could enhance proton decay. However, these are at M_1 >> M_4, so their
   contribution is suppressed by (M_4/M_1)^4.

4. **Gravitational corrections**: At M_1 ~ 10^19 GeV (near M_Planck), gravitational
   loop corrections to the gauge couplings become relevant. These are model-dependent
   but could affect the unification quality.
