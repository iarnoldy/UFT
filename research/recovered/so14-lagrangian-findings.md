# SO(14) Lagrangian & Beta Function Research -- Recovered from Session Transcripts

## Source
Recovered from JSONL session transcripts on 2026-03-14.
Original agents: so14-lagrangian-engineer, so14-phenomenologist, so14-breaking-architect,
clifford-unification-engineer, polymathic-researcher, and related discussions.

Transcripts searched:
- `~/.claude/projects/C--Users-ianar-Documents-CODING-UFT-dollard-formal-verification/*.jsonl`
- `~/.claude/projects/C--Users-ianar-Documents-CODING-UFT/*.jsonl`

Keywords used: lagrangian, beta function, gauge kinetic, Higgs potential, Yukawa coupling,
covariant derivative, field content, running coupling, one-loop, two-loop, asymptotic freedom,
RG equation, Dynkin index, so14-lagrangian-engineer.

---

## 1. SO(14) Agent Architecture (Recovered from session 9c8101a0)

Six dedicated SO(14) physics agents were built (2026-03-09) for the candidate theory:

1. `so14-breaking-architect` -- Symmetry breaking chain SO(14) -> SM
2. `so14-generation-specialist` -- Three-generation problem
3. `so14-signature-analyst` -- Compact vs Lorentzian (Cl(14,0) vs Cl(11,3))
4. **`so14-lagrangian-engineer`** -- Full Lagrangian construction
5. `so14-phenomenologist` -- Experimental predictions (proton decay, coupling unification)
6. `so14-paper-architect` -- Paper 3 writing and integration

Dependency chain: [1,2,3] parallel -> [4] -> [5] -> [6].
The Lagrangian engineer depends on breaking chain, generation, and signature results.

**Status**: The so14-lagrangian-engineer agent was DEFINED but its full Lagrangian
construction (Phase 2 deliverable: `docs/so14_lagrangian.md`) was NOT completed in
the transcripts. Phase 1 (RG/beta functions) was completed instead.

---

## 2. Beta Function Computation -- COMPLETE (Recovered from session 22571151)

### 2.1 One-Loop Beta Function Table

Source: `src/experiments/so14_rg_unification_v2.py`

| Scale | Gauge Group | Beta Coefficient | Asymptotically Free? |
|-------|-------------|-----------------|---------------------|
| M_Z to M_4 | SU(3) | b_3 = -7.0 | YES |
| M_Z to M_4 | SU(2) | b_2 = -19/6 = -3.167 | YES |
| M_Z to M_4 | U(1)_Y | b_1 = 123/50 = 2.46 (GUT norm.) | NO |
| M_4 to M_3 | SU(5) | b_SU5 = -40/3 = -13.33 | YES |
| M_3 to M_1 | SO(10) | b_SO10 = -38.0 | YES |
| M_3 to M_1 | SU(2)_a | b_SU2a = 29/3 = 9.67 | NO |
| > M_1 | SO(14) | b_SO14 = -208/3 = -69.33 | YES |

### 2.2 Beta Function Formula Used

```
b_i = -(11/3)*C_2(G_i) + (2/3)*sum_f T(R_f) + (1/3)*sum_cs T(R_cs) + (1/6)*sum_rs T(R_rs)
```

where:
- sum_f runs over Weyl fermions
- sum_cs runs over complex scalars
- sum_rs runs over real scalars
- Convention: T(fund SO(N)) = 1, T(fund SU(N)) = 1/2

### 2.3 Field Content at Each Scale

**SM (M_Z to M_4)**: Standard Model with right-handed neutrino.
SM betas are machine-verified in `rg_running.lean` [MV].

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

---

## 3. Dynkin Index Table (Recovered from session 22571151)

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

---

## 4. Coupling Unification Results (Recovered from session 22571151)

### 4.1 Desert Hypothesis (single scale)

| Parameter | Value |
|-----------|-------|
| M_GUT | 10^16.98 GeV |
| alpha_GUT^{-1} | 47.03 |
| alpha_1^{-1} at M_GUT | 45.46 |
| Absolute miss | 1.57 |
| Relative miss | 3.3% |

### 4.2 Multi-Scale Approach B (free M_4, M_3, M_1)

| Parameter | Value |
|-----------|-------|
| M_4 (SU(5) breaking) | 10^16.50 GeV |
| M_3 (SO(10) breaking) | 10^17.00 GeV |
| M_1 (SO(14) breaking) | 10^19.00 GeV |
| Spread at M_1 | 0.67 |
| Quality (spread/avg) | 0.88% |

### 4.3 Multi-Scale Approach C (M_4 fixed at 2-3 crossing)

| Parameter | Value |
|-----------|-------|
| M_4 = M_3 | 10^16.98 GeV |
| M_1 | 10^19.50 GeV |
| a_SU5^{-1}(M_3) | 47.03 |
| a_chi^{-1}(M_3) | 45.46 |
| Gap at M_1 | 1.57 |
| Quality | 1.93% |

**Key finding**: The gap between alpha_1 and alpha_{2,3} is preserved through
the multi-scale chain. The SO(10) and SO(14) betas are LARGE and negative, which
pushes the unified coupling to large alpha^{-1} (weak coupling) at M_1, but the
absolute gap of ~1.57 stays fixed because both lines evolve with the same SO(10)
beta above M_3.

**Kill condition verdict**: KC-FATAL-6 (Coupling Unification) = GREEN (PASS).
Best miss: 0.88% (Approach B) to 3.3% (desert). All well below the 20% threshold.

---

## 5. Proton Decay Prediction (Recovered from session 22571151)

| Quantity | Desert | Multi-scale C |
|----------|--------|---------------|
| M_X (X boson mass) | 10^16.98 GeV | 10^16.98 GeV |
| alpha_GUT | 1/47.03 | 1/47.03 |
| tau_p (dimensional) | 10^39.7 years | 10^39.7 years |
| tau_p (with A_R = 2.5) | 10^38.9 years | 10^38.9 years |
| Super-K bound | 10^34.4 years | 10^34.4 years |
| Safety factor | 3.5 x 10^4 | 3.5 x 10^4 |

Proton lifetime safe by 4-5 orders of magnitude. M_GUT ~ 10^17 GeV is high
(tau_p ~ M_X^4), and alpha_GUT ~ 1/47 is small.

Proton lifetime depends on M_4 (SU(5) breaking scale), not on M_1 or M_3.

**Kill condition verdict**: KC-FATAL-5 (Proton Decay) = GREEN (PASS).

Formula: `tau_p ~ M_X^4 / (alpha_GUT^2 * m_p^5)` [natural units]
With renormalization enhancement: `tau_p -> tau_p / A_R^2`, where A_R ~ 2.5.

---

## 6. SO(14) vs SO(10) Comparison (Recovered from session 22571151)

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
   Does NOT improve coupling unification because the (10,4) mixed bosons
   contribute equally to all three SM beta functions.

2. The SO(4) = SU(2)_a x SU(2)_b sector is entirely decoupled from the SM
   coupling evolution (SM singlets). Its beta b_SU2a = 29/3 > 0 means the
   SU(2) factors are NOT asymptotically free in the SO(10) x SO(4) regime.

3. Proton lifetime is identical because it depends only on M_4 and alpha_GUT.

4. Multi-scale freedom allows modest improvement from 3.3% to 0.88%.

**Bottom line**: SO(14) does not make coupling unification BETTER or WORSE than
SO(10). The physics is dominated by the SM desert regime (M_Z to M_4).

---

## 7. Breaking Chain -- CRITICAL CORRECTION (Recovered from sessions e10df509, 9c8101a0)

### The Corrected Breaking Chain

```
SO(14) --[104]--> SO(10) x SO(4) --[45]--> SU(5) x U(1) x SO(4)
  --[24]--> SU(3) x SU(2) x U(1) x SO(4) --[4]--> SU(3) x U(1)_EM x SO(4)
```

**CRITICAL CORRECTION (2026-03-09)**: Step 1 Higgs is the **symmetric traceless
104-dimensional representation**, NOT the adjoint 91.

- Adjoint (91) breaks SO(2n) -> U(n), which is WRONG for the physics.
- Symmetric traceless breaks SO(N) -> SO(n1) x SO(n2), which gives SO(14) -> SO(10) x SO(4).
- Corrected in Lean proofs, verified numerically.

### Higgs Representations

| Step | Higgs rep | Dimension | Breaks to |
|------|-----------|-----------|-----------|
| 1 | Symmetric traceless | 104 | SO(10) x SO(4) |
| 2 | SO(10) adjoint | 45 | SU(5) x U(1) |
| 3 | SU(5) adjoint | 24 | SU(3) x SU(2) x U(1) |
| 4 | SU(2) doublet | 4 | U(1)_EM |

Total scalar components: 177 (104 + 45 + 24 + 4).

---

## 8. Threshold Correction Analysis (Recovered from session 22571151)

The 104 has SU(5)-universal Dynkin indices (T_1 = T_2 = T_3 = 12 for the 54).
This is a structural CONSTRAINT [CO], not a smoking-gun prediction.
Cannot differentially close the coupling triangle with the 104 alone.

The ~3.3% miss is the standard non-SUSY GUT result and can potentially be
closed by:
- Threshold corrections from the rich Higgs sector (104 + 45 + 24 + 5 = 178 components)
- Two-loop corrections
- Split multiplet spectra
- SUSY at an intermediate scale

---

## 9. Anomaly Cancellation (Recovered from sessions e10df509, 22571151)

SO(n) for n >= 7 has vanishing d_abc (rank-3 symmetric Casimir). For SO(14):
- All 6 anomaly conditions satisfied [MV in so14_anomalies.lean]
- Anomalies are algebraic (signature-independent) -- transfers to SO(3,11)
- Kill condition KC-FATAL-3: LIKELY PASS

The anomaly trace approach was later upgraded (Milestone 2 in "The Bridge" roadmap)
to prove `Tr(T^a {T^b, T^c}) = 0` from the antisymmetric trace identity:
for antisymmetric matrices A, B, C, the trace Tr(A{B,C}) = 0. This handles both
fundamental and adjoint representations of any so(n).

---

## 10. Open Questions for Lagrangian Construction (Recovered from session 22571151)

The following were identified as open/future work at the end of Phase 1:

1. **Threshold corrections**: The rich Higgs sector (104 + 45 + 24 + 5 = 178
   scalar components) provides many parameters. A dedicated computation could
   determine whether these naturally close the 1.57-unit gap without fine-tuning.

2. **Two-loop corrections**: The 2-loop beta coefficients for SO(14) have NOT
   been computed. These could shift the unification scale and quality.

3. **Proton decay channels**: SO(14) has additional gauge bosons beyond SU(5)
   X and Y bosons. The (10,4) mixed bosons mediate new processes but are at
   M_1 >> M_4, so their contribution is suppressed by (M_4/M_1)^4.

4. **Gravitational corrections**: At M_1 ~ 10^19 GeV (near M_Planck),
   gravitational loop corrections become relevant. Model-dependent.

5. **Full Lagrangian**: The explicit Lagrangian (Phase 2 deliverable:
   `docs/so14_lagrangian.md`) was planned but NOT completed. The experiment
   registry (Experiment 4) lists this as Phase 2.

6. **Yukawa sector**: Yukawa couplings for SO(14) were NOT computed beyond
   the general structure in `yukawa_couplings.lean` (which verifies
   hypercharge conservation for the SU(5) Yukawa).

---

## 11. Experiment 4 Status (Recovered from session 9c8101a0)

Pre-registered as Experiment 4: SO(14) Candidate Theory Construction.

| Phase | Status | Outcome |
|-------|--------|---------|
| Phase 0: Literature + matter content | COMPLETE | VIABLE-BUT-UNDEREXPLORED |
| Phase 1: RG + proton decay | COMPLETE | Both kill conditions PASS |
| Phase 2: Lagrangian + selection principle | **NOT STARTED** | Planned deliverables pending |
| Phase 3: Paper synthesis | **NOT STARTED** | Blocked on Phase 2 |

Phase 2 planned deliverables (not yet produced):
- `docs/so14_lagrangian.md` -- explicit Lagrangian
- `src/experiments/so14_proton_decay.py` -- proton lifetime computation (partially done in v2 script)
- `docs/so14_selection_principle.md` -- why SO(14)?

---

## 12. Verdict from Phase 1 (Recovered from session e10df509)

**SO(14) Physics Program -- PHASE 1 COMPLETE**:
- Breaking chain: corrected (sym. traceless 104, not adjoint 91) [MV+CO]
- RG: 0.88% coupling miss, proton safe by 10^{4.5} [CO]
- Verdict: **INTERESTING, not compelling. No accessible-energy distinction from SO(10)**
- Strategic direction: Contact Krasnov/Percacci AFTER Paper 1 acceptance
- DO NOT pursue: two-loop RG, threshold corrections, orbifold three-gen mechanisms
  (diminishing returns)

---

## 13. Signature Analysis (Recovered from session e10df509)

- 30/36 proofs (83%) are signature-independent -- transfer to SO(3,11) directly
- 3 proofs are compact-only (energy positivity = ghost problem in non-compact)
- 3 proofs need revision (spinor reality conditions)
- Strategy: SO(14) for proofs, SO(3,11) for physics

Key distinction:
- SO(14,0) compact: standard Yang-Mills gauge theory, no natural chirality
- SO(11,3) non-compact: contains SO(3,1) Lorentz, Majorana-Weyl spinors exist,
  but non-compact gauge fields lead to ghost problems

The Lie algebra is the same (D_7 root system, 91 generators) regardless of
signature. Casimir eigenvalues are identical.

---

## Summary

The so14-lagrangian-engineer agent was DEFINED as part of the SO(14) physics
agent team but its primary deliverable (the explicit Lagrangian) was never
completed in the transcripts. The extensive findings recovered here are from
Phase 0 (literature survey) and Phase 1 (RG/beta function/proton decay), which
were completed by the phenomenologist and engineer agents collaboratively.

**What was completed**:
- Full one-loop beta function table for all scales
- Complete Dynkin index table for all relevant representations
- Three approaches to coupling unification (0.88%-3.3% miss)
- Proton decay prediction (safe by 4+ orders of magnitude)
- Breaking chain correction (104, not 91)
- Anomaly cancellation verification
- Comparison with SO(10)
- Signature analysis

**What was NOT completed**:
- Explicit SO(14) Lagrangian (gauge kinetic + fermion + scalar potential + Yukawa)
- Two-loop beta coefficients
- Threshold corrections
- Explicit Yukawa coupling matrices
- Higgs potential V(S, Sigma, Sigma', H) with all quartic terms
