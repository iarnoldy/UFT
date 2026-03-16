# SO(14) Phenomenology Research -- Recovered from Session Transcripts

## Source

Recovered from JSONL session transcripts on 2026-03-14.
Original sessions: `285e0cfe` (UFT), `9c8101a0` (dollard-formal-verification),
`05d77074` (UFT), `22571151` (dollard-formal-verification).
Original agents: so14-phenomenologist (referenced), clifford-unification-engineer,
polymathic-researcher, heptapod-b-architect.

## Search Methodology

Searched all JSONL files in:
- `~/.claude/projects/C--Users-ianar-Documents-CODING-UFT-dollard-formal-verification/` (12 sessions + subagents)
- `~/.claude/projects/C--Users-ianar-Documents-CODING-UFT/` (8 sessions + subagents)

Keywords searched: "proton decay", "coupling unification", "Weinberg angle", "sin^2 theta",
"gauge coupling", "M_GUT", "M_X", "lifetime", "Super-K", "neutrino mass", "seesaw",
"phenomenolog", "testable prediction", "experimental signature", "collider", "GUT scale",
"beta function", "Dynkin index", "threshold correction", "alpha_GUT".

Note: The so14-phenomenologist agent was defined in the project's agent roster but
the actual phenomenology work was done inline within main sessions (primarily
`285e0cfe` from 2026-03-08/09 and `9c8101a0` from 2026-03-11), not through a
dedicated subagent invocation. The agent roster entry references proton decay, coupling
unification, and testable predictions as the agent's scope.

---

## Findings

### 1. Phase 0: Literature Survey and Kill Condition Triage (Session 285e0cfe, 2026-03-08)

**Agents used**: polymathic-researcher (literature), clifford-unification-engineer (decomposition), heptapod-b-architect (strategy)

#### KC-0: Literature Viability
- **Status**: DOES NOT FIRE (clear)
- SO(14)/Spin(11,3) is viable-but-underexplored in the literature
- Key existing work: Nesti-Percacci (SISSA, "Graviweak unification" JPCAM 41, 2008) and Krasnov (Nottingham, arXiv:2104.01786)
- No no-go theorem found against SO(14) unification
- 15 references surveyed, 29KB literature survey produced (`research/so14-gut-literature.md`)

#### KC-3: Signature Question
- **Status**: YELLOW (manageable)
- Same Lie algebra D_7 underlies both SO(14,0) (compact, used in Lean proofs) and SO(11,3) (Lorentzian, needed for physics)
- The Lean proofs use compact signature Cl(14,0). Physical gravity requires the Lorentzian real form SO(11,3)
- All dimension-counting theorems hold identically in both signatures
- Algebraic structure constants are signature-independent; physical interpretation is not

#### KC-4: Three-Generation Problem
- **Status**: YELLOW (same challenge as SO(10))
- Spinor decomposition: 64_+ = (16, (2,1)) + (16_bar, (1,2)) under SO(10) x SO(4)
- This gives ONE generation with correct chirality
- Better than feared: no mirror fermion problem
- Three generations require an external mechanism -- same as in SO(10) GUTs
- Later investigation (session 9c8101a0) showed that 7 intrinsic SO(14) generation mechanisms are ALL dead; the number 3 must come from E_8 structure

### 2. Phase 1: RG Coupling Unification (Session 285e0cfe, 2026-03-08)

**Script**: `src/experiments/so14_rg_unification.py` (corrected version)
**Results**: `src/experiments/results/so14_rg_unification_results.json`

#### Input Parameters (at M_Z = 91.1876 GeV)
- alpha_1^{-1}(M_Z) = 59.0 (GUT normalized)
- alpha_2^{-1}(M_Z) = 29.6
- alpha_3^{-1}(M_Z) = 8.5
- b_1 = (3/5)(41/10) = 2.46 (GUT normalized, one-loop SM beta coefficient)
- b_2 = -19/6 = -3.167
- b_3 = -7.0

#### Normalization Bug Found and Fixed
- Initial bug: b_1_GUT was computed as (5/3)(41/10) = 6.83 instead of (3/5)(41/10) = 2.46
- The fraction was inverted. Correct relationship: alpha_1^{-1}_GUT = (3/5) alpha_1^{-1}_Y, so b_1_GUT = (3/5) b_1_Y
- Effect: U(1) coupling line fell 2.8x too steeply with the bug
- Fix applied by background agent; corrected script committed

#### Corrected Results

**Pairwise crossing scales** (log_10(mu/GeV)):
- alpha_1 = alpha_2 crossing: mu_12 = 1.65 x 10^16 GeV (log_10 = 16.22)
- alpha_1 = alpha_3 crossing: mu_13 = 3.36 x 10^16 GeV (log_10 = 16.53)
- alpha_2 = alpha_3 crossing: mu_23 = 9.55 x 10^16 GeV (log_10 = 16.98)

**Coupling values at crossings**:
- alpha^{-1} at 1-2 crossing: 46.15
- alpha^{-1} at 1-3 crossing: 45.87
- alpha^{-1} at 2-3 crossing: 47.03
- alpha_1^{-1} at the 2-3 crossing: 45.46

**Kill Condition KC-1 (Coupling Unification)**:
- Miss: 1.57 (absolute), **3.3% relative** -- under 5% threshold
- **Status: GREEN**
- This miss is GENERIC to all non-SUSY GUTs, not SO(14)-specific
- MSSM cross-check: 0.58% miss at 10^{16.35} GeV -- matches textbook values, validates the computation methodology

**Kill Condition KC-2 (Proton Decay)**:
- Proton lifetime: tau_p = 5.27 x 10^{39} years (log_10 = 39.7)
- Super-K experimental bound: tau > 1.6 x 10^{34} years (log_10 = 34.2)
- Safety factor: 3 x 10^5 above experimental bound
- **Status: GREEN** (safe by 5.5 orders of magnitude)

**SO(14)-specific threshold content**:
- The 40 mixed (10,4) generators of SO(14) contribute EQUALLY to all three SM beta coefficients: Delta(b_1) = Delta(b_2) = Delta(b_3) = 1/3
- Equal shifts cannot improve the coupling miss (they shift all three lines by the same amount)
- The (10,4) content has no differential lever arm on unification

**Overall Verdict**: SO(14) is ALIVE. Both Phase 0 and Phase 1 kill conditions passed.

### 3. Weinberg Angle

**From Lean proofs** (`src/lean_proofs/foundations/georgi_glashow.lean`):
- sin^2(theta_W) = 3/8 = 0.375 at the GUT scale (tree level)
- This is a standard SU(5)/SO(10) prediction, not SO(14)-specific
- The value runs down to the observed 0.2312 at M_Z via RG evolution (verified in `rg_running.lean`)

**From Wilson's E_8(-24) framework** (recovered from session 9c8101a0):
- Wilson predicts: sin^2(phi_W/2) = 1/2 - 1/sqrt(13) ~ 0.22265
- Experimental value: 0.23122 +/- 0.00003
- About 4% off at tree level; RG running could potentially fix the discrepancy
- This is a Wilson-specific prediction, different from the standard GUT sin^2 = 3/8

### 4. Wilson's E_8(-24) Three-Generation Mechanism (Session 9c8101a0, 2026-03-11)

A comprehensive investigation report was produced (700+ lines). Key findings:

#### The Type 5 Element
- In complex E_8, there are exactly 4 conjugacy classes of order-3 elements (types 1, 2, 3, 5)
- Type 5 element: torus representative (1,1,1,1,1,0,0,0)
- Its centralizer in compact E_8: SU(9)/Z_3
- Its centralizer in E_8(-24): SU(7,2)/Z_3
- Wilson argues type 5 is the UNIQUE order-3 element compatible with chirality + weak SU(2) + Lorentz invariance

#### Breaking Chain
```
E_8(-24) --> Spin(12,4) --> SU(7,2)/Z_3 --> Z_3 x SU(5) x SU(2,2)
                                              |
                                     generation symmetry
```
- The Z_3 persists through the entire chain as the generation symmetry
- SU(5) is Georgi-Glashow; SU(2,2) is conformal/twistor containing Lorentz group

#### Critical Computational Discovery: Z_3 on D_8 Spinor is Order 6
- The type 5 torus element gives half-integer charges on spinor weights
- Resulting eigenvalues are SIXTH roots of unity, not cube roots
- The Z_3 generation mechanism lives in the E_8 ADJOINT decomposition (248 = 80 + 84 + 84 under SU(9)), NOT in the D_8 SPINOR
- Wilson's mechanism fundamentally requires the full E_8 structure; it cannot be reduced to D_8 or D_7

#### D_7 Semi-Spinor Decomposition under Z_3
- Under nearest-cube-root classification: 64 weights --> 44 + 10 + 10
- This does NOT correspond to a generation structure (would need 3 x 16 or 4 x 16)
- Confirms: generation mechanism is an E_8-level phenomenon, not an SO(14)-level one

#### Compatibility with Our Impossibility Theorem
- Our result: 7 intrinsic SO(14) mechanisms for 3 generations are ALL dead
- Wilson's result: the number 3 comes from E_8 classification of finite elements, not from SO(14)
- These findings are COMPATIBLE -- both say SO(14) alone cannot produce 3 generations

#### Concerns
1. **Distler-Garibaldi objection** (2010): "There is no Theory of Everything inside E_8." Wilson's rebuttal relies on redefining chirality for massive fermions -- legitimate physics but non-standard
2. **Publication venue**: 2024 paper in physics.gen-ph (low prestige); 2025 paper in hep-ph (mainstream)
3. **Real 2-space claim**: 3 generations require only 2x DOF (32 complex spinor DOF, not 48). This differs from standard model's 3 independent copies
4. **No dynamical mechanism**: Z_3 symmetry identified but breaking mechanism not derived from a Lagrangian

#### Confidence Calibration
| Claim | Confidence |
|-------|-----------|
| Wilson's group theory (types, centralizers) | 95% |
| Type 5 Z_3 gives discrete generation symmetry | 85% |
| Wilson's model reproduces the Standard Model | 55% |
| PMNS predictions are non-accidental | 60% |
| Wilson's mechanism works for Spin(3,11) (our real form) | 50% |
| E_8 approach is the "right" answer to 3-gen problem | 30% |
| Connection to our Z_4 Coxeter grading | 25% |

### 5. Wilson's Mixing Angle Predictions (from 2025 paper, arXiv:2507.16517)

- **Weinberg angle**: sin^2(phi_W/2) = 1/2 - 1/sqrt(13) ~ 0.22265 (exp: 0.23122, ~4% off at tree level)
- **PMNS angles**: 8.586 deg and 49.077 deg (exp: 8.54 +/- 0.12 deg and 49.1 +/- 1.0 deg -- excellent match)
- **CKM structure**: derived from mass ratios
- **Mass relation**: m_e + m_mu + m_tau + 3 m_p = 5 m_n (approximate)
- **Neutrino sector**: SU(2,2) contains Lorentz + additional gauge DOF; neutrino masses emerge naturally

### 6. Signature Analysis

Four real forms of the D_7 Lie algebra discussed across sessions:

| Real form | Signature | Context |
|-----------|-----------|---------|
| Spin(14,0) | Compact | Our Lean proofs (algebraic scaffold) |
| Spin(12,4) | (12,4) | Wilson's D_8 in E_8(-24) |
| Spin(3,11) | (3,11) | Our Lorentzian physics choice |
| Spin(11,3) | (11,3) | Krasnov's framework |

- Spin(p,q) = Spin(q,p), so Spin(3,11) = Spin(11,3)
- Spin(12,4) != Spin(3,11) -- different real forms of Spin(14,C)
- Wilson's type 5 Z_3 element is defined at the complex level and works in any real form
- Whether Spin(3,11) embeds in E_8(-24) is KC-W1 (UNTESTED)

### 7. Matter Content Decomposition

**Script**: `src/experiments/so14_matter_decomposition.py` (737 lines)
All assertions passed; cross-checked analytically.

Key decompositions:
- Spin(14) Dirac spinor: dim = 2^7 = 128
- Weyl (semi-spinor): 128/2 = 64
- Under SO(10) x SO(4): 64_+ = (16, (2,1)) + (16_bar, (1,2))
- The 16 of SO(10) = one complete generation (u, d, e, nu_e + antiparticles)
- Under SO(4) ~ SU(2)_L x SU(2)_R: the (2,1) is left-handed, (1,2) is right-handed
- No mirror fermion problem -- chirality is correct for one generation

### 8. SO(14) Lagrangian Structure (from Lean proofs, session 05d77074)

The Yang-Mills Lagrangian on so(14):
```
L = -(1/4) Tr(F_{mu nu} F^{mu nu})
```
decomposes as:
```
L = L_SM + L_gravity + L_mixed
```
where:
- L_SM = -(1/4) Tr(F^{ab}_{mu nu} F^{ab, mu nu}) -- Standard Model (a,b = 1,...,10)
- L_gravity = -(1/4) Tr(R^{alpha beta}_{mu nu} R^{alpha beta, mu nu}) -- Gauss-Bonnet-like (alpha,beta = 1,...,4)
- L_mixed = -(1/4) Tr(Phi^{a alpha}_{mu nu} Phi^{a alpha, mu nu}) -- new Planck-scale physics

**Critical subtlety**: L_gravity is NOT the Einstein-Hilbert action (R). It is a higher-order
gravity action (R^2-type). To get standard GR from a gauge theory, one needs the
MacDowell-Mansouri mechanism (SO(1,4) de Sitter group), not simple Yang-Mills on SO(14,0).

Field strength component count (in 4D spacetime):
- Total: 6 spacetime 2-forms x 91 algebra components = 546
- SM part: 6 x 45 = 270
- Gravity part: 6 x 6 = 36 (= Riemann tensor in first-order Cartan formulation)
- Mixed part: 6 x 40 = 240

### 9. Strategic Assessment (Heptapod-B Architect, Session 285e0cfe)

Key strategic conclusions from the phenomenology analysis:

1. The scaffold's value is METHODOLOGICAL (Track A), not phenomenological (Track D)
2. The 3.3% coupling miss does NOT uniquely support SO(14) -- same generic miss applies to SO(10), E_6, and all non-SUSY GUTs
3. The (10,4) mixed generators cannot improve the coupling miss (equal beta shifts)
4. Paper 1 (CICM 2026, Track A methodology) should come before any physics paper
5. SO(14) physics should be pursued only after Paper 1 credibility is established and contact with Krasnov/Percacci is made
6. Kill-condition-first methodology validated: cheapest tests first saved weeks of wasted effort

### 10. Open Kill Conditions (Phenomenology-Related)

| ID | Description | Status | Estimated Difficulty |
|----|-------------|--------|---------------------|
| KC-W1 | Does Spin(3,11) embed in E_8(-24)? | UNTESTED | Medium |
| KC-W2 | Is the Distler-Garibaldi chirality objection fatal? | CONTESTED | High |
| KC-W3 | Does the "real 2-space" DOF count match SM? | UNTESTED | Medium |
| KC-W4 | Is there a dynamical Z_3 breaking mechanism? | ABSENT | High |
| KC-W5 | Can the Z_3 mechanism be verified in Lean 4? | UNTESTED | Very High |
| KC-W6 | Does Wilson's PMNS prediction survive loop corrections? | UNTESTED | Medium |
| KC-W7 | Has anyone independently verified Wilson's group theory? | NO | Medium |

### 11. Key References Identified

- Nesti & Percacci, "Graviweak unification" JPCAM 41 (2008)
- Krasnov, "Spin(11,3), particles, and octonions" arXiv:2104.01786
- Wilson, "Octions: An E8 description of the Standard Model" J. Math. Phys. 63, 081703 (2022)
- Wilson, "Uniqueness of an E8 model of elementary particles" arXiv:2407.18279 (2024)
- Wilson, "Embeddings of the Standard Model in E8" arXiv:2507.16517 (2025)
- Distler & Garibaldi, "There is No Theory of Everything Inside E8" (2010)
- Lisi, "An Exceptionally Simple Theory of Everything" (2007)
- Chamseddine, Connes, Mukhanov, "Quanta of Geometry" PRL 114 (2015)

---

## Files Produced by This Research

| File | Size | Status |
|------|------|--------|
| `research/so14-gut-literature.md` | 29KB | Committed |
| `src/experiments/so14_matter_decomposition.py` | 31KB | Committed |
| `src/experiments/so14_rg_unification.py` | ~42KB | Committed (corrected normalization) |
| `src/experiments/results/so14_rg_unification_results.json` | 1KB | Committed |
| `src/experiments/results/so14_rg_unification_plot.png` | -- | Committed |
| `research/wilson-e8-three-generations-investigation.md` | -- | Committed |
| `docs/SIGNATURE_ANALYSIS.md` | -- | Committed |
| `docs/PHYSICS_MATH_FRICTION_CATALOG.md` | -- | Committed |
