# E8 Mixing Angles -- Rigorous Mathematical Assessment

**Date:** 2026-03-17
**Agent:** Dollard Theorist (Opus)
**Context:** Research Council Round 4 (RIGOR) for e8-mixing-angles investigation
**Primary output:** `research/council/e8-mixing-angles/04-rigor.md`

## Question Asked

Apply PhD-level mathematical rigor to four specific claims from the Devil's
Advocate (Round 3) regarding geometric mixing angles from E8:

1. Does [84,84]->84* antisymmetric coupling produce non-trivial generation mixing?
2. Is Wilson's sin^2(theta_W) = 3/13 a good match to experiment?
3. What is Wilson's genuine joint significance after honest counting?
4. Is there a theoretical framework for the mass equation?

## Key Findings

### Task 1: Antisymmetric Coupling

The [84,84]->84* coupling IS non-trivial in generation space. The map is the
wedge product Lambda^3 ^ Lambda^3 -> Lambda^6. Under SU(5) x SU(4), the
generation-relevant channel (10,4) x (10,4) -> (5-bar, 6) uses the SU(4)
contraction 4 ^ 4 -> 6, which under SU(3)_fam gives the Levi-Civita tensor
epsilon_{ijk}.

However, the combined Yukawa Y = y*I + g*A (identity from symmetric +
antisymmetric from epsilon) has eigenvalues {y, y+ig|phi|, y-ig|phi|}, giving
singular values {y, sqrt(y^2+g^2|phi|^2), sqrt(y^2+g^2|phi|^2)}. **Two masses
are always degenerate.** This is a theorem (conjugate-pair property of
antisymmetric matrix eigenvalues), not fixable by parameter choice.

The 2-fold degeneracy makes the texture incompatible with the observed quark
mass hierarchy. CKM mixing requires different VEV directions for up and down
sectors (dynamical, not geometric).

**Verdict: NEUTRAL (leaning NEGATIVE).** The coupling exists but has wrong structure.

### Task 2: sin^2(theta_W)

Two different formulas were conflated across rounds:
- 3/13 = 0.23077: **11 sigma off** from MS-bar (0.23121), **26 sigma off** from on-shell (0.22290)
- 1/2 - 1/sqrt(13) = 0.22265: **214 sigma off** from MS-bar, **0.83 sigma** from on-shell only

Wilson does not specify which scheme or scale his prediction targets.
The Round 3 claim of "0.10 sigma" for 3/13 was an error.

**Verdict: NEGATIVE.** Neither formula works universally.

### Task 3: Joint Significance

Honest counting of independent predictions: 3.5 (not 7-8 as claimed in Round 3).
- Mass equation (1), theta_12 (1), delta_CP (1), theta_23 partially dependent on delta_CP (0.5)
- Cabibbo has ad hoc offset (0 independent predictions)
- sin^2(theta_W) is separate, scheme-dependent
- V_ub is a 4-sigma FAILURE

Joint probability of 3.5 within 1 sigma: P = 0.6827^3.5 = 0.26, equivalent to ~1.1 sigma.
All predictions are post-hoc (none pre-registered). Look-elsewhere effect applies.

**Verdict: NEGATIVE.** The "2 sigma anomaly" claim was overcounted. Corrected: ~1.1 sigma.

### Task 4: Mass Equation

m_e + m_mu + m_tau + 3*m_p = 5*m_n holds at 3.95 ppm (0.15 sigma as m_tau prediction).
More precise than Koide (9.2 ppm) by factor ~2. No theoretical derivation exists.
The equation mixes Yukawa-determined (lepton) masses with QCD-determined (baryon) masses,
which arise from fundamentally different mechanisms. No SU(9) trace identity, E8 relation,
Koide generalization, or string compactification produces this equation.

Combinatorial argument: ~10^9 candidate linear relations with small integer coefficients
exist among ~20 particle masses. Finding one at 4 ppm is not unprecedented.

**Verdict: NEUTRAL.** Unexplained but not proven anomalous.

## Conclusions

1. Strong form (H1): DEAD at 97%. E8 root geometry does not determine mixing angles.
2. Medium form (H2): Alive but weak at 55%. E8 constrains texture (6 params vs 18),
   but 2-fold degeneracy prevents realistic masses.
3. Weak form (H3/Wilson bridge): NOT anomalous at 30%. Joint significance only ~1.1 sigma
   after honest counting, with scheme problems and post-hoc construction.
4. Mass equation: Unexplained empirical regularity, not confirmed anomaly.

The investigation should close with a NEGATIVE result on geometric mixing from E8.
Wilson's formulas should NOT be cited in Papers 3-4 (marginal significance, post-hoc,
would invite justified criticism).
