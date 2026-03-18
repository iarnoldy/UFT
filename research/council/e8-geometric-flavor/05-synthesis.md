# Round 5: SYNTHESIS -- Final Verdict on Three Generations in E8

**Date:** 2026-03-17
**Agent:** Heptapod B Architect (Opus 4.6)
**Investigation:** e8-geometric-flavor
**Status:** COMPLETE -- INVESTIGATION CLOSED

---

## Methodological Note

This is the final document of a five-round research council investigation. The
charter question was: "Is there a mathematical structure beyond SU(9)/Z_3 that
distinguishes exactly 3 generations in E_8?" Four specialist rounds have
produced a comprehensive evidence base. This synthesis applies the seven-step
teleological method in reverse: we began by assuming the solution exists, and
we traced backward until we found where it breaks. The breaks are now fully
characterized.

The Wilson Principle applies throughout: honesty before harmony.
The Optik of Berlinski applies throughout: say exactly what is true.

---

## 1. THE VERDICT

**No mathematical structure internal to E_8 distinguishes exactly 3 generations
without assuming the number 3 as input.**

The investigation examined seven candidate mechanisms across four rounds. Every
candidate either assumes Z_3 directly (SU(9)/Z_3), borrows the number 3 from
a substructure (D_4 triality, J_3(O) matrix dimension), or requires a choice
external to E_8 (Calabi-Yau topology, flavon alignment). The two strongest
candidates -- Wilson's SU(9)/Z_3 and the exceptional Jordan algebra J_3(O) --
share a common limitation: the number 3 enters through a postulated
identification (generation symmetry = Z_3; matrix dimension = generation count)
that is not forced by any theorem of E_8. The systematic inventory of E_8's
topological and algebraic invariants (Round 2) confirms that no intrinsic
invariant of E_8 equals 3. Direct computation (Round 4) confirms that the
Z_3 eigenspace structure acts as a scalar on each sector and contains zero
information about generation mixing. The framework provides 3 generation
*slots* but not 3 generation *physics*. E_8 is a theater with the correct
number of seats. It does not write the script for who sits where, or why there
are exactly that many seats.

This is a negative result of genuine value. It delimits what the algebraic
structure can and cannot do, and it redirects effort toward the questions
that remain open.

---

## 2. WHAT WE LEARNED (Positive Findings)

### Algebraic and Representational Facts

**F1.** [MV] E_8 (248-dim) is verified as a Lie algebra via sparse Jacobi identity
in Lean 4. 88 proof files, ~2,900 declarations, zero sorry gaps. This is the first
formalization of E_8 in any interactive theorem prover.

**F2.** [MV] The decomposition 248 = 80 + 84 + 84* under SU(9)/Z_3 is dimensionally
verified. The Z_3 acts as scalar eigenvalues {1, w, w^2} on the three sectors.

**F3.** [MV] Within the 84, branching under SU(5) x SU(4) produces 3 copies of
the 16 of SO(10) via (10,4) with SU(4) -> SU(3) + 1. Each copy carries identical
SM quantum numbers. Anomaly freedom holds in each Z_3 eigenspace independently.

**F4.** [CO] The E_8 -> E_6 x SU(3) decomposition 248 = (78,1) + (1,8) + (27,3)
+ (27*,3*) resolves the "three types vs three copies" problem for this specific
chain. The tensor product (27,3) guarantees three identical copies by construction.
This is verified by SageMath branching computation.

**F5.** [CO] Under G_2 (the triality-invariant subgroup of SO(8)), all three D_4
triality representations (8_v, 8_s, 8_c) branch identically as 7 + 1. Restriction
to the invariant subgroup converts three types into three copies. This is a known
result, confirmed computationally.

**F6.** [CO] Singh's delta^2 = 3/8 for equal-diagonal J_3(O) elements with
normalization |x|^2 = 1/8 is an exact algebraic identity, confirmed to machine
precision (10^-15 deviation over 10,000 random trials). It follows from the Vieta
formula delta^2 = 3N for the reduced cubic characteristic equation.

**F7.** [SP] Albert's theorem (1934): J_n(O) exists only for n = 1, 2, 3. The
number 3 is the maximum matrix dimension for exceptional Jordan algebras. This is
the sharpest known mathematical reason why 3 is special in exceptional structures.

**F8.** [SP] No intrinsic topological or algebraic invariant of E_8 equals 3.
The center is trivial, the fundamental group is trivial, the outer automorphism
group is trivial, the exponents are {1,7,11,13,17,19,23,29}, and no Casimir
invariant has degree 3. The number 3 appears only through substructures.

**F9.** [SP] No discrete flavor symmetry model in the published literature predicts
all 8 mixing parameters (3 CKM angles + 1 CKM phase + 3 PMNS angles + 1 Dirac phase)
with zero free parameters. The best models reduce SM's 19 parameters to ~14.
Confirmed by comprehensive survey of A_4, S_4, Delta(27), A_5, and modular flavor
programs spanning 2006-2024.

**F10.** [SP] The noncommutative geometry / spectral action program (Connes,
Boyle-Farnsworth) does not fix the generation number. N_gen = 3 is input to the
construction, not output. An early argument from Poincare duality was invalidated
when massive neutrinos were included.

### Structural Insights

**F11.** The four algebraic sources of "3" in exceptional mathematics -- Z_3(SU(9)),
D_4 triality S_3, J_3(O) matrix dimension, sedenion automorphism S_3 -- share a
common root in octonionic algebra but are not unified by any single theorem.
Z_3(SU(9)) is an inner automorphism; Z_3(triality) is an outer automorphism. These
are categorically different. [SP]

**F12.** The "three types vs three copies" gap is closable in principle (Mechanism B:
restriction to SM subgroup makes D_4 triality reps identical), and is already closed
for the E_6 x SU(3) chain (Mechanism: tensor product). The gap remains open for a
direct D_4-triality-to-SM-generations construction. [SP + CO]

**F13.** The J_3(O)-to-generations identification is a CHOICE, not a theorem.
Multiple internally-consistent maps exist (eigenvalue map, off-diagonal triality
map, Gursey-Ramond-Sikivie single-generation map). The strongest argument for any
particular map would be correct predictions. Singh's eigenvalue map is the most
predictive, yielding mass ratio agreement at 1-7%. [SP]

---

## 3. WHAT WE KILLED (Negative Findings)

### Definitively Killed

**K1. Z_3 eigenspace mixing angles.** The Z_3 that decomposes 248 = 80 + 84 + 84*
acts as a scalar (w * I_84) on each eigenspace. It contains exactly zero information
about generation mixing. The hope that E_8 eigenspace projections might produce CKM
or PMNS-like rotation matrices is dead. [CO, KC-R3]

**K2. Geometric invariant mixing angles from E_8.** Generation labels within the
SU(9)/Z_3 framework depend on the choice of SU(3) inside SU(4), parameterized by
CP^3 (6 real parameters). This exceeds the CKM parametrization (4 real parameters).
Any "angles" extracted are artifacts of embedding choice, not geometric invariants.
The framework is structurally underdetermined for mixing physics. [CO, KC-R4]

**K3. Zero-parameter flavor prediction from discrete symmetry.** Twenty years of
the discrete flavor program (A_4, S_4, Delta(27), A_5, modular groups) have not
produced a single model that predicts all mixing parameters without free inputs.
Every specific angle prediction (theta_13 = 0, theta_23 = 45 deg, golden ratio
for theta_12) has been either falsified or marginalized by experiment. If E_8
discrete structure were to succeed where the entire field has failed, it would
need to explain why -- and no such explanation exists. [SP, KC-R2]

### Severely Damaged

**K4. Singh's "parameter-free" mass ratios.** The framework has genuine algebraic
content (delta^2 = 3N is an exact Vieta identity). But the "parameter-free" label
obscures three assumptions: the normalization N = 1/8 (convention), the trace
split 1:2:3 (free input that directly generates Prediction 1), and the minimality
principle (physical postulate). Prediction 2 (swap equality sqrt(m_tau/m_mu) =
sqrt(m_s/m_d)) shows 8% tension with central PDG values. The lepton ratios
(1-2% agreement) are the strongest component. Overall: interesting enough to track,
not strong enough to build on. [CO, KC-R5]

**K5. D_4 triality as generation mechanism.** The three 8-dimensional reps of SO(8)
are genuinely different representations. While they collapse to identical copies
under G_2 restriction, the full chain from G_2 through the Standard Model gauge
group has never been constructed. The "three types = three generations" claim
remains an analogy, not an identification. [SP]

### Weakened but Not Killed

**K6. J_3(O) as the origin of "3."** Albert's theorem (n_max = 3) remains the
sharpest mathematical reason why 3 is special. But the bridge from "3x3 matrices
are the maximum" to "nature has 3 generations" is a categorical gap: matrix
dimension is not the same concept as representation multiplicity. Multiple papers
(Todorov-DV, Boyle, Singh) postulate this identification; none prove it. The
program survives as a framework, not a theory. [SP]

---

## 4. KILL CONDITION FINAL ASSESSMENT

### KC-R1: No coherent mathematical structure connects discrete automorphisms to continuous rotation angles

**Verdict: SERIOUS**

Structures that connect discrete symmetries to continuous parameters exist in
abstract mathematics (e.g., projection operators between different eigenspace
decompositions). But no known construction produces specific irrational mixing
angles from E_8 discrete symmetries alone. Every known path introduces free
parameters at the symmetry-breaking stage. This kill condition does not destroy
the investigation outright (FATAL), because the mathematical possibility is not
excluded -- but it means any claimed success must explain why it works where
the entire discrete flavor program has failed.

### KC-R2: All prior work on discrete symmetry -> mixing angles requires free parameters

**Verdict: SERIOUS (97% confidence)**

Confirmed comprehensively by the Round 2 literature survey and strengthened by
Round 4 computation (trace split is free, SU(3) in SU(4) embedding has CP^3
freedom). Not FATAL because a novel mechanism might differ from existing approaches.
But the burden of proof is enormous: 20+ years of dedicated effort by hundreds of
researchers have not achieved zero-parameter flavor prediction from any discrete group.

### KC-R3: Z_3 eigenspace projections produce trivial rotation matrices

**Verdict: FIRES (SERIOUS)**

Confirmed by direct computation. The Z_3 acts as w * I on each eigenspace. This
is a structural fact about how the center of SU(9) acts on exterior powers, not a
limitation of our computation. There is no rotation matrix, no angle, no phase.
The Z_3 eigenspace splitting of E_8 is irrelevant to generation mixing.

This is SERIOUS rather than FATAL because the charter question asked about
structures "beyond SU(9)/Z_3." The Z_3 eigenspace is one specific structure;
other structures (J_3(O) spectral decomposition, D_4 triality) are not killed
by this result. But the most natural candidate for "geometric mixing from E_8
automorphisms" is eliminated.

### KC-R4: Angles depend on arbitrary basis choices, not geometric invariants

**Verdict: FIRES (SERIOUS)**

Confirmed by direct computation. Generation labels require choosing SU(3) inside
SU(4), parameterized by CP^3 (6 real parameters > CKM's 4). The framework is
underdetermined. This fires for the SU(9)/Z_3 approach specifically. Other
approaches (direct triality, Jordan eigenvalues) have different parametrizations
but face analogous freedom.

### KC-R5: delta^2 normalization is a convention

**Verdict: MODERATE**

Singh's delta^2 = 3/8 is exact algebra (Vieta), but equals 3N where N = |x|^2
is a normalization choice. Different N gives different delta^2. The mass ratio
predictions also require the trace split 1:2:3, which is unconstrained by the
algebra. This does not kill Singh's program outright -- it recharacterizes it as
a framework with hidden assumptions rather than a parameter-free prediction.

### Collective Meaning

The five kill conditions form a coherent picture. KC-R3 and KC-R4 together
eliminate the specific mechanism posed in the charter: geometric mixing angles
from E_8 eigenspace structure. KC-R1 and KC-R2 together constrain the broader
class of discrete-symmetry approaches. KC-R5 weakens the strongest positive
result from the investigation (Singh's mass ratios).

No single kill condition is FATAL to all approaches simultaneously. But the
combination closes the most natural paths and leaves only indirect, assumption-laden
frameworks. The investigation's charter question receives a clear negative answer
for the most literal interpretation, and a "not yet, possibly never" for the more
generous interpretation.

---

## 5. THE HONEST STATE OF THE FIELD

### Where the three-generation problem stands as of 2026

The number 3 is not derived from first principles in any existing framework.
Five distinct research programs have attempted it over decades; none has succeeded.

**Program 1: E_8 / GUT internal (Wilson, Bars, Ramond).** The most developed
algebraic approach. SU(9)/Z_3 provides 3 generation slots inside E_8 uniquely
(among Z_3 conjugacy classes). But "uniquely among Z_3 classes" is conditional
on assuming Z_3 in the first place. Wilson's recent papers (2022-2025) continue
to refine the embedding but do not derive 3 from E_8 invariants.

**Program 2: Exceptional Jordan algebra (Todorov, Dubois-Violette, Boyle, Singh).**
The most mathematically compelling. Albert's theorem provides a sharp algebraic
reason why 3 is maximal. Singh (2025) claims mass ratio predictions at the
few-percent level. But the identification of matrix dimension with generation
count is a postulate, multiple maps exist, and the "parameter-free" label
obscures assumptions. The bridge is HALF-BUILT: the algebraic side is solid,
the physical identification is asserted.

**Program 3: Division algebra / Clifford algebra (Furey, Stoica, Gresnigt).**
Derives 3 from S_3 automorphisms of sedenions or Cl(8). The algebraic "3" is
genuine. But sedenions are not part of E_8, and the connection between S_3(sedenions),
Z_3(SU(9)), and triality(D_4) has not been established. These may be three views
of one object, or three coincidences wearing the same number.

**Program 4: Heterotic string compactification.** Produces 3-generation models
from Calabi-Yau manifolds with |Euler| = 6. The "3" comes from topology, which
is genuine. But no selection principle picks |Euler| = 6 from the landscape.
"Triadophilia" (Candelas et al. 2007) names the observation that small-Hodge-number
manifolds cluster near 3 generations; it does not explain it.

**Program 5: Noncommutative geometry (Connes, Chamseddine, Boyle-Farnsworth).**
Does not fix the generation number. An early Poincare duality argument was
invalidated by massive neutrinos. N_gen = 3 is input.

### What would constitute progress

Three paths forward remain open, in decreasing order of plausibility:

**Path A: Physical dynamics selects 3.** Wilson's recent suggestion (arXiv:2507.16517)
that generation-number breaking is linked to electroweak symmetry breaking would
make the generation problem a dynamical question solved by vacuum selection, not
algebraic structure. This shifts the problem from "why does the algebra give 3?"
to "why does the vacuum break this way?" -- a question that at least has a known
mathematical framework (scalar potential minimization). This is the most physicially
promising path, but it requires a specific model with a computable potential, which
does not yet exist.

**Path B: The J_3(O) bridge is completed.** Someone proves a theorem of the form:
"Given the E_8 algebra constructed via the Freudenthal-Tits magic square from J_3(O),
the 3x3 matrix structure induces exactly 3 copies of a specific representation under
the SM gauge group." This would convert the postulate into a theorem. It requires
closing the categorical gap between matrix dimension and representation multiplicity.
The tools exist (representation theory, branching rules, Jordan algebra theory). The
theorem does not.

**Path C: The answer is environmental.** The number 3 is not derivable from any
algebra. It is selected by a combination of physical constraints (CP violation
requires N_gen >= 3, asymptotic freedom requires N_gen <= 8) and either anthropic
selection, vacuum statistics, or an unknown dynamical principle. In this case, the
correct response is to stop looking for an algebraic derivation and accept that 3
is a boundary condition, not a theorem.

### Is this a problem that CAN be solved within E_8?

Probably not, as stated. The investigation's most robust finding (F8) is that E_8
has no intrinsic invariant equal to 3. Every appearance of 3 comes from substructure.
If the answer were purely algebraic and internal to E_8, we would expect an invariant
of E_8 to equal 3 -- and none does. The paths that remain open (A, B, C) all involve
something beyond pure E_8 algebra: vacuum dynamics, a Jordan algebra identification
theorem, or environmental selection.

This does not mean E_8 is irrelevant to the generation problem. It means E_8 provides
the stage (the correct representation content, the correct gauge quantum numbers,
the correct number of generation slots) but not the script (why 3 slots and not 4,
what the mixing angles are, what the mass ratios are).

---

## 6. IMPLICATIONS FOR OUR PROJECT

### For Papers 3 and 4

The investigation strengthens the papers' existing framing. Both papers present
the E_8 formalization as a mathematical contribution (Track A), with the SO(14)
construction as a candidate theory (Track D, gate-controlled). The three-generation
mechanism is described accurately as "SU(9)/Z_3 decomposition with dimensionally
consistent generation structure and J-eigenspace anomaly freedom" [MV]. The papers
do NOT claim that 3 generations are derived from E_8 -- they claim the algebraic
scaffold accommodates them.

**Specific implications:**

1. **Paper 3 (methodology + E_8 formalization):** No revision needed for the
   three-generation content. The existing [MV] tags are accurate. The paper correctly
   states that the SU(9)/Z_3 decomposition is verified and that anomaly freedom holds
   in each eigenspace. It does not overclaim derivation of 3.

2. **Paper 4 (E_8 construction):** No revision needed. The paper presents the
   E_8 Lie algebra formalization and SO(16) subalgebra closure. Three-generation
   content is in Paper 3, not Paper 4.

3. **Future Paper 5 (phenomenology, if M8 continues):** The council findings
   provide critical framing. Any phenomenological paper must honestly state:
   "The SU(9)/Z_3 framework provides 3 generation slots but does not predict mixing
   angles or mass ratios. These require additional input (flavon sector, symmetry
   breaking pattern) not determined by E_8." The Outcome C characterization from
   M8.1-M8.2 is confirmed and should be central to the paper's framing.

### For the SO(14) Construction

The SO(14) construction (Track D) is unaffected by this investigation's negative
result. The SO(14) GUT is a candidate theory evaluated on its own merits
(coupling unification, proton decay, matter content). The three-generation question
is orthogonal: SO(14) inherits whatever generation mechanism E_8 provides, and this
investigation shows that mechanism is "slots without script."

The critical implication: if SO(14) phenomenology is pursued further, the generation
sector should be treated as parameterized (free Yukawa couplings in the generation
space), not predicted. Any claim that SO(14) "explains" 3 generations would be
overclaiming based on the evidence assembled here.

### For Milestone 8 (Yukawa Kill-Condition)

The investigation's findings are consistent with M8.1 (Outcome C: underdetermined).
The council provides the theoretical foundation for why Outcome C was inevitable:
the trace split is free, the SU(3) embedding is arbitrary, and the Z_3 eigenspace
contains no mixing information. M8 should proceed as planned (M8.1 CG coefficients
are computed; M8.2 texture extraction and M8.3 CKM/PMNS comparison remain), but
with the understanding that Outcome C is the expected and most honest result.

**Wilson PMNS verification (M8.3b) retains high value.** Wilson's claimed angle
matches (theta_13 = 8.586 vs exp 8.54; theta_23 = 49.077 vs exp 49.1) are
numerically striking regardless of their theoretical status. Independent verification
remains the single highest-value physics test available. If reproducible, they
constitute an empirical pattern worth understanding even if the theoretical derivation
is incomplete. If not reproducible, they save months of work on a wrong approach.

### For the Project's Honest Self-Assessment

This project's strength has always been Track A: Lean 4 as a tool for verifying
mathematical claims. The E_8 formalization is a genuine first-in-any-ITP achievement.
The chain SU(5) -> SO(10) -> SO(14) -> SO(16) of certified LieHoms is rigorous
mathematics. The council investigation confirms that the physics interpretation
(Track D) is speculative and underdetermined -- which is exactly how the project
frames it.

The temptation to overclaim is real: E_8 is verified, 3 generations fit inside it,
therefore E_8 "explains" 3 generations. This investigation provides the antidote.
E_8 accommodates. It does not explain.

---

## 7. COUNCIL FORMAT ASSESSMENT

### What Worked

**Round structure (Vision -> Archaeology -> Rigor -> Computation -> Synthesis).**
The progression from abstract to concrete was effective. Round 1 identified the
right candidates and necessary properties. Round 2 found the literature (including
the surprise finding of Singh 2025). Round 3 applied mathematical rigor to the
leads. Round 4 tested kill conditions computationally. Each round built on the
previous one without redundancy.

**Kill conditions registered upfront.** Pre-registering KC-R1 through KC-R4 in
the charter ensured the investigation could produce negative results without
feeling like failure. The kill conditions fired (KC-R3, KC-R4) and the
investigation produced a clear negative answer -- which is exactly what
pre-registration is designed to enable.

**Specialist agents for specialist tasks.** The Dollard Theorist (Round 3) caught
that Singh's "parameter-free" claim hides assumptions (trace split 1:2:3). The
Clifford Unification Engineer (Round 4) proved computationally that the Z_3
eigenspace projection is trivial. These findings required domain expertise that
a single generalist would have struggled to produce.

**Confidence calibration across rounds.** Tracking confidence levels for each
claim across all four rounds provided a visible trajectory. Some claims
strengthened (zero-parameter models don't exist: 70% -> 97%), others weakened
(Singh's mass ratios meaningful: 55% -> 45%), and some were stable (no mechanism
derives 3 without Z_3 input: 88-92%). This made the evidence accumulation
visible and honest.

### What Should Change

**Round 2 (Archaeology) was too broad.** Five research questions produced a
comprehensive survey but diluted focus. For a real run, the archaeology round
should have 2-3 targeted questions, not 5. The Boyle-Farnsworth and heterotic
landscape questions (Q4, Q5) produced useful context but did not change the
investigation's trajectory. Tighter scoping would save time.

**Round 4 (Computation) could have been split.** Four computational tasks in
one round is ambitious. The Z_3 eigenspace computation (Tasks 1) and the Singh
verification (Task 2) were the highest-value items. The triality branching
(Task 3) and trace split (Task 4) confirmed expectations without surprise.
For a real run, prioritize the kill-condition computations and defer confirmatory
computations to an optional round.

**Inter-round feedback was implicit, not explicit.** Each round read the previous
round's document, but there was no formal mechanism for one round to REQUEST
specific work from the next. Round 3's recommendation for Round 4 was helpful
but could have been more structured (e.g., "compute X with script Y, expect
result Z, interpret as follows"). A brief inter-round handoff document would
improve coordination.

**The synthesis round (this document) should have access to all computational
scripts.** I synthesized from the written reports but could not independently
verify the computations. In a real run, the synthesis agent should be able to
re-run key computations or at least inspect the scripts for correctness.

**Missing: adversarial round.** The investigation would benefit from a dedicated
"red team" round where an agent attempts to SAVE the hypothesis. Every round
was oriented toward honest assessment, which tends toward negative results. A
devil's advocate round -- "what is the strongest case FOR geometric flavor from
E_8?" -- would ensure the negative verdict is not premature. This is different
from avoiding negative results; it is ensuring the negative result survives its
strongest challenge.

### Recommended Format for Real Run

1. **Charter** (as done) -- question, kill conditions, agent assignments
2. **Vision** (Heptapod B) -- teleological structure, candidates, necessary properties
3. **Archaeology** (Polymathic Researcher) -- 2-3 TARGETED questions only
4. **Computation** (Domain specialist) -- kill-condition tests ONLY
5. **Devil's Advocate** (NEW) -- strongest case for the hypothesis surviving
6. **Rigor** (Dollard Theorist) -- mathematical assessment of both positive and
   negative cases, informed by computation and devil's advocate
7. **Synthesis** (Heptapod B) -- final verdict with access to all scripts

This is 7 rounds instead of 5, but the additional rounds (devil's advocate +
reordering rigor after computation) would produce a more robust verdict.

---

## FINAL CONFIDENCE TABLE

| Claim | R1 | R2 | R3 | R4 | R5 (Final) | Tag |
|-------|-----|-----|-----|-----|------------|-----|
| No mechanism derives 3 from E_8 without Z_3 input | 92% | 90% | 88% | 90% | **91%** | [SP] |
| J_3(O) most compelling mathematical source of "3" | 80% | 85% | 87% | 85% | **84%** | [SP] |
| J_3(O)-to-generations bridge NOT built | 88% | 80% | 82% | 85% | **85%** | [SP] |
| Zero-parameter discrete flavor models don't exist | 70% | 95% | 96% | 97% | **97%** | [SP] |
| D_4 triality is analogy, not generation mechanism | 85% | 88% | 85% | 88% | **87%** | [SP] |
| Z_3 eigenspace contains mixing info | -- | -- | -- | 5% | **5%** | [CO] |
| Mixing angles from E_8 discrete structure | -- | -- | -- | 10% | **8%** | [CO+SP] |
| Singh's mass ratios are meaningful | -- | -- | 55% | 45% | **40%** | [CO] |
| Types vs copies gap closable | -- | -- | 40% | 55% | **55%** | [SP+CO] |
| "3 is environmental, not algebraic" | 40% | 45% | 42% | 48% | **50%** | [OP] |

### Reading the Table

The final column represents the council's settled assessment after all evidence.
The most striking convergence: "No mechanism derives 3 from E_8 without Z_3 input"
held between 88-92% across all five rounds. No evidence moved it significantly in
either direction. This stability suggests the estimate is well-calibrated.

The most significant movement: "Zero-parameter discrete flavor models don't exist"
rose from 70% (prior to literature survey) to 97% (after comprehensive survey +
computation). This is a genuine finding of the investigation.

The most contested: "3 is environmental, not algebraic" drifted from 40% to 50%
across five rounds. The investigation did not resolve this question. It remains
an open problem of fundamental physics.

---

## APPENDIX: Investigation Artifact Index

| Round | Document | Key Findings |
|-------|----------|-------------|
| 0 | `00-charter.md` | Charter question, kill conditions, agent assignments |
| 1 | `01-vision.md` | Seven candidates evaluated; N1-N5 necessary properties; J_3(O) most promising |
| 2 | `02-archaeology.md` | Nine J_3(O) papers; no intrinsic "3" in E_8; KC-R2 fires; Singh surprise |
| 3 | `03-rigor.md` | Singh ratios 1-7%; identification is CHOICE not theorem; four "3"s share octonionic root |
| 4 | `04-computation.md` | KC-R3 fires (Z_3 trivial); KC-R4 fires (CP^3 freedom); delta^2=3N exact; E6xSU(3) resolves types/copies |
| 5 | `05-synthesis.md` | This document. Verdict: negative. E_8 accommodates 3, does not derive 3. |

### Supporting Files

| File | Contains |
|------|----------|
| `research/heptapod-b-yukawa-vision.md` | Prior teleological analysis: "algebra gives stage, not script" |
| `research/yukawa-kill-condition-research.md` | SU(9) Yukawa literature survey |
| `research/wilson-three-generation-comparison.md` | Wilson's approach vs ours |
| `src/experiments/results/su9_cg_coefficients.json` | M8.1 CG coefficient results |
| `src/experiments/results/yukawa_texture_analysis.json` | M8.2 texture results |
| `src/experiments/results/wilson_pmns_verification.json` | M8.3b Wilson angle verification |
| `src/experiments/z3_eigenspace_projections.py` | KC-R3/KC-R4 computation script |
| `src/experiments/singh_delta_verification.py` | Singh delta^2 verification script |
| `src/experiments/triality_sm_branching.py` | Triality branching computation |
| `src/experiments/trace_split_constraint.py` | Trace split freedom computation |

---

*Investigation closed 2026-03-17. The three-generation problem in E_8 remains open.*
*This council produced an honest negative result with precisely characterized boundaries.*
*The value is in knowing where the walls are.*
