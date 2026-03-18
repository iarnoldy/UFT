# Round 3: DEVIL'S ADVOCATE -- Geometric Mixing Angles from E8

**Agent:** Heptapod B Architect (Devil's Advocate)
**Date:** 2026-03-17
**Investigation:** e8-mixing-angles (Real Run)
**Status:** Complete

---

## 0. Methodological Note

My job is to make the STRONGEST possible case that geometric mixing from E8
is still viable. Every previous round has been oriented toward honest assessment,
which -- as the earlier geometric-flavor council noted -- tends toward negative
results. This round pushes back. If the hypothesis cannot survive its strongest
defense, then the negative verdict is robust. If it can, the investigation has
more to learn.

I will not fabricate evidence or distort mathematics. I will identify assumptions
that may be wrong, loopholes that may be open, and constructions that have not
been attempted. The Wilson Principle still applies: honesty before harmony. But
the honest question here is whether the prosecution has proven its case beyond
reasonable doubt, or whether the defense has arguments the jury has not heard.

---

## 1. The Strongest Surviving Argument

### 1.1 The Prosecution's Case (Summary)

The first two rounds established:

- **KC-M5 (FATAL):** SU(9) CG coefficients produce delta_{ij} in generation
  space. The SU(3) symmetry within SU(4) forces all three generations to couple
  identically to the Yukawa vertex. Generation mixing is zero at tree level.
- **KC-M1 (SERIOUS):** Six candidate mechanisms examined. Five killed outright.
  The one survivor (CG sector weights) was killed by KC-M5.
- **Wilson's angles are mass-ratio functions, not E8 invariants** (95-97%).
- **No discrete flavor model achieves zero-parameter prediction** (97%).
- **The Z3 eigenspace is scalar times identity** (95%).

The prosecution asks the jury to conclude: E8 determines the stage, not the
script. Mixing angles require dynamical input. Case closed.

### 1.2 What the Prosecution Missed

The prosecution made its case against a SPECIFIC hypothesis: that E8 root
geometry directly produces mixing angles as geometric invariants (the "strong
form"). This hypothesis is dead. I do not attempt to revive it.

But the prosecution conflated three distinct hypotheses:

**H1 (Strong Form -- DEAD):** E8 root geometry directly determines the
numerical values of CKM/PMNS mixing angles as geometric invariants.

**H2 (Medium Form -- ALIVE):** E8 representation theory constrains the
STRUCTURE of the Yukawa matrix (its texture, its rank pattern, its symmetry
breaking chain) in ways that reduce the parameter count below generic
SU(5) + SU(3)_family models, producing testable relations between
observables.

**H3 (Weak Form -- ALIVE and possibly PROVEN):** E8 representation theory,
through Wilson's mass-ratio formulas, INDIRECTLY determines mixing angles by
constraining the algebraic framework within which masses arise, and the mixing
angles are determined functions of those masses.

The prosecution killed H1. It declared victory. But H2 and H3 were never
tested on their own terms.

### 1.3 The Strongest Argument: The Wilson Anomaly

Wilson's formulas present a genuine anomaly that the prosecution acknowledged
but failed to engage with:

**Seven numerical coincidences from five inputs.**

| Parameter | Wilson formula | Deviation from exp. | Inputs used |
|-----------|--------------|--------------------|--------------------|
| sin^2(theta_W) | 1/2 - 1/sqrt(13) | 0.83 sigma | 0 (just the number 4) |
| theta_12 (PMNS) | mass-plane projection | 0.51 sigma | m_e, m_mu, m_tau |
| delta_CP (CKM) | arctan((m_n-m_p)/m_e) | 0.08 sigma | m_e, m_n, m_p |
| theta_23 (CKM, V_cb) | arccos((m_p+m_e)/m_n) | 0.70 sigma | m_e, m_n, m_p |
| theta_C (Cabibbo) | theta_12 - 20 | 0.40 sigma | m_e, m_mu, m_tau + conjecture |
| theta_23 (PMNS) | complex function | 0.09 sigma | multiple |
| theta_13 (PMNS) | complex function | 0.22 sigma | multiple |
| **Mass equation** | m_e+m_mu+m_tau+3m_p=5m_n | **3.95 ppm** | m_e, m_mu, m_tau, m_p, m_n |

The prosecution classified this as "COINCIDENCE (25%)" and moved on.

I challenge this classification.

### 1.4 The Probabilistic Argument Against Coincidence

Consider the mass equation alone. The prosecution offered a counting argument:
with ~20 masses and small integer coefficients, thousands of relations are
possible, so finding one at 4 ppm is not remarkable (look-elsewhere effect).

This argument has a flaw: **it assumes the coefficients are arbitrary.** Wilson's
coefficients are (1,1,1,3,5). These are not arbitrary. They have a structure:

- 1+1+1 = 3 (three leptons, each weighted equally)
- 3 (three protons)
- 5 (five neutrons)

The integers 1, 3, 5 are the first three odd numbers. They sum to 9 = dim of
the fundamental of SU(9). The equation can be rewritten:

    sum of all generation-1 masses x 1 = 0 (approximately)

where the "generation-1 masses" include both leptons and baryons counted with
SU(9)-motivated multiplicities. The 3 and 5 are not random scan parameters;
they are LOW integers with algebraic significance in the SU(9) context.

Now consider the SYSTEM. Wilson uses the SAME five masses to produce ~8
predictions. The prosecution asked whether these could be independent
coincidences. The joint probability of 8 independent coincidences each at
<1 sigma is approximately:

    P(all < 1 sigma) ~ (0.68)^8 ~ 0.047

This is already at the 2-sigma level for the system, even before accounting
for the 3.95 ppm mass equation precision. If we weight by the mass equation's
exceptional precision, the system as a whole is significantly more improbable
than any individual coincidence.

**The prosecution's error was evaluating each formula in isolation.** The
anomalous fact is not any single Wilson formula. It is that a SYSTEM of
formulas using the same 5 inputs produces 8 outputs that are all within 1
sigma of experiment. This is the pattern that demands explanation.

### 1.5 The Structural Argument

The prosecution correctly noted that Wilson's formulas use COMPOSITE particle
masses (proton, neutron) to predict FUNDAMENTAL parameters (mixing angles),
which reverses the standard hierarchy of explanation. This is the prosecution's
strongest objection.

But consider: if E8 unification is real, then the distinction between
"fundamental" and "composite" is an artifact of the low-energy effective
theory. In a true E8 GUT, the proton mass is determined by the same algebraic
structure that determines quark masses and coupling constants. The proton mass
is NOT independent of the fundamental parameters -- it is a complicated
function of them. If Wilson's formulas are correct, they may be expressing
relations that HOLD among the fundamental parameters but are most simply
STATED in terms of composite quantities.

Analogy: the Balmer formula (1/lambda = R(1/4 - 1/n^2)) was written in
terms of wavelengths of visible light -- a "composite" quantity determined by
atomic structure. It was correct, and it led to quantum mechanics. The fact
that it was expressed in non-fundamental variables was not a defect; it was
an empirical fact waiting for a deeper explanation.

### 1.6 Summary: The Strongest Surviving Argument

**The hypothesis survives in a form the prosecution never tested.**

The surviving argument is NOT that E8 root geometry directly produces mixing
angles (dead). It is that:

1. E8/SU(9) determines the algebraic framework (generation number, particle
   content, gauge structure, Yukawa coupling uniqueness).
2. Within this framework, the physical masses (including composite masses)
   satisfy algebraic relations constrained by the E8 structure.
3. Wilson has identified empirical functions that express mixing angles in
   terms of these masses.
4. The system of Wilson's formulas is statistically anomalous at the ~2-sigma
   level when evaluated jointly.
5. If the mass relations are not coincidental, they imply that E8 constrains
   masses, and mixing angles are determined functions of masses. This is
   INDIRECT geometric mixing -- the geometry constrains the masses, and the
   masses determine the angles.

This is H3 (weak form). It is not proven. But it is not killed either.

---

## 2. Kill Condition Challenges

### 2.1 Challenge to KC-M5

**KC-M5 states:** SU(9) CG coefficients produce delta_{ij} in generation space.
Generation mixing requires dynamical SU(3)_family breaking, not kinematics.

**Challenge:** KC-M5 is correct AT TREE LEVEL IN THE SYMMETRIC LIMIT. But
there are three potential loopholes:

**Loophole A: Radiative corrections.** The delta_{ij} structure holds at tree
level. But radiative corrections (RG evolution from M_GUT to M_Z) can generate
off-diagonal entries in the Yukawa matrix. In the Standard Model, the Yukawa
matrices run under the RG equations:

    16 pi^2 dY_u/dt = Y_u (3 Y_u^dag Y_u + Y_d^dag Y_d + ...)

Even if Y_u = y delta_{ij} at M_GUT, the RG running through different
thresholds (where SU(3)_family breaking introduces mass splittings) can
generate mixing. This is not geometric in the E8 sense, but it means the
delta_{ij} starting point is not the whole story. The AMOUNT of mixing
generated radiatively depends on the mass splittings, which are dynamical.

**Assessment: This is standard physics, not a geometric mechanism. KC-M5
survives this challenge. The loophole is real but does not give geometric
mixing -- it gives dynamical mixing starting from a geometric identity.**

**Loophole B: Non-perturbative effects.** The SU(3)_family gauge symmetry
confines at some scale Lambda_fam. Below this scale, the effective theory
is a chiral Lagrangian with composite "mesons" and "baryons" of the family
sector. The Yukawa couplings of these composites are NOT given by the
tree-level CG coefficients -- they are non-perturbative functions of the
confinement dynamics.

If SU(3)_family confines at a scale comparable to the GUT scale, the effective
Yukawa couplings at low energies could be dramatically different from
delta_{ij}. The mixing would then be determined by the confinement dynamics
of SU(3)_family, which is a NON-PERTURBATIVE geometric effect of the gauge
theory.

**Assessment: This is speculative but not killed. The SU(3)_family confinement
scale is a free parameter. If Lambda_fam ~ M_GUT, the perturbative CG
analysis (which KC-M5 relies on) is inapplicable. This loophole is SERIOUS
but untested. It does not save "geometric mixing from E8 root geometry" --
it replaces it with "mixing from SU(3)_family confinement dynamics." The
mixing is still dynamical, but the dynamics is that of a gauge theory whose
existence is geometrically guaranteed by E8.**

**Loophole C: Higher-order invariants.** KC-M5 tested the LEADING-ORDER
coupling: 84 x 84* -> 80 (adjoint). But the E8 Lie bracket also produces:

    [84, 84] -> 84* (via epsilon tensor of SU(9))

This second coupling is ANTISYMMETRIC in its two 84 indices. Under
SU(5) x SU(4), it involves the epsilon tensor of SU(4), which connects
different SU(3) representations (3 and 3-bar) in a non-trivial way.

The effective Yukawa at low energies involves both the [84, 84*] -> 80
coupling (which gives delta_{ij}) and higher-dimensional operators built
from [84, 84] -> 84*. If the 84* acquires a VEV (which it can in the
breaking pattern), the higher-dimensional operator:

    (84 x 84 -> 84*) x <84*> / M_GUT

gives a Yukawa contribution that is ANTISYMMETRIC in generation indices.
This antisymmetric contribution is NOT proportional to delta_{ij}. It is
proportional to epsilon_{ijk} <phi_k>, where phi_k is the 84* VEV component
in the SU(3)_family direction.

**Assessment: This is a genuine loophole. The antisymmetric coupling
[84, 84] -> 84* provides a non-trivial generation structure that was
NOT tested by KC-M5. The kill condition tested only the symmetric
(Yukawa-type) coupling and found it proportional to identity. The
antisymmetric coupling gives a rank-2 contribution to the mass matrix.
Combined with the rank-3 delta_{ij} from the symmetric coupling, this
produces a texture with mixing.**

**However:** This is not "geometric mixing from E8 root geometry." It is
"mixing from two different E8 couplings combined with a specific VEV."
The mixing angles depend on the VEV, which is dynamical. But the TEXTURE
(one symmetric + one antisymmetric coupling) is determined by E8 Lie
algebra structure. This is H2 (medium form).

### 2.2 Challenge to KC-M1

**KC-M1 states:** No mathematical structure in E8 connects root geometry to
unitary rotation matrices.

**Challenge:** KC-M1 tested six specific candidates (Weyl group, root angles,
Coxeter element, McKay, branching coefficients, Wilson). It did not test:

**Candidate G: Automorphisms of the E8 lattice.** The E8 lattice has
automorphism group W(E8) (order 696,729,600). Within this group, there
are elements that act on the SU(9) Cartan subalgebra in specific ways.
The RELATIVE orientation of two different SU(9) embeddings in E8 defines
a unitary matrix. Different SU(9) embeddings are related by E8 automorphisms,
and the "mixing matrix" between two embeddings is an E8 invariant.

Physically, if the quark and lepton sectors are associated with DIFFERENT
SU(5) subgroups within SU(9) (which they must be, since quarks and leptons
carry different quantum numbers), then the relative orientation of these
subgroups defines a rotation matrix. This rotation is determined by the
E8 algebra, not by dynamical symmetry breaking.

**Assessment: This is a REAL mathematical structure that connects E8 to
unitary matrices. But it connects E8 to the relative orientation of
SUBGROUPS, not to GENERATION mixing. The CKM matrix mixes generations
within a fixed gauge structure, not different gauge structures within a
fixed generation. This candidate addresses the wrong question.**

**Candidate H: Modular forms and the E8 theta function.** The E8 lattice
theta function Theta_E8(tau) = 1 + 240 q + 2160 q^2 + ... is a modular
form of weight 4 for SL(2,Z). Modular flavor symmetries (Feruglio 2017+)
use the modular group to constrain Yukawa couplings, with the modulus tau
as the sole free parameter. If the E8 theta function plays a role in
determining the Yukawa couplings (as it does in heterotic string
compactifications), then the mixing angles are determined by the modular
properties of E8.

**Assessment: This is mathematically well-defined and connects E8 to
mixing physics through modular symmetry. But it requires a specific
string/F-theory compactification to make the connection precise. In a
point-particle GUT (our framework), the modular structure is not
accessible. This is a PATH FORWARD but not a loophole in KC-M1 as
stated. It would require changing the framework.**

**Verdict on KC-M1:** KC-M1 is not overturned. No candidate connects
E8 ROOT GEOMETRY (as distinct from representation theory, modular forms,
or string compactification) to mixing matrices. The kill condition is
correctly stated and correctly assessed as SERIOUS (not FATAL, because
indirect connections through representation theory remain viable).

### 2.3 Challenge to KC-M2

**KC-M2 states:** All candidate constructions reduce to flavon VEV alignment
(recovered underdetermination).

**Challenge:** KC-M2 presupposes that "flavon VEV alignment" is an
unstructured choice. But in many models, the flavon potential has a finite
number of minima, and the VEV alignment is selected by the discrete symmetry
of the potential. For example:

- In A4 models, the potential V(phi) for a triplet flavon phi has exactly
  three types of minima: (1,0,0), (1,1,1)/sqrt(3), and (1,1,-1)/sqrt(3).
  The VEV alignment is a DISCRETE choice, not a continuous parameter.

- In our SU(3)_family framework, the adjoint flavon potential has critical
  points at the SU(3) Weyl orbit: (a,b,c) up to permutations, constrained
  by V'(a) = V'(b) = V'(c). For a quartic potential, this gives a FINITE
  number of solutions.

If the VEV alignment is discrete, the mixing angles become functions of
discrete choices (which critical point is selected) plus mass ratios (which
are dynamical). The discrete choice may be topological (which vacuum the
universe fell into) but the resulting angles are determined.

**Assessment: This weakens KC-M2 from FATAL to SERIOUS. The mixing angles
are still "dynamical" in the sense that they depend on symmetry breaking,
but the space of possibilities is finite, not continuous. Each vacuum
produces specific angles. If one vacuum agrees with experiment, the
predictive content is: "the universe is in vacuum #k out of N possible
vacua, and this predicts the mixing angles." This is weaker than zero-
parameter derivation but stronger than continuous underdetermination.**

### 2.4 Challenge to the "97% No Zero-Parameter Model" Finding

The test run established at 97% confidence that no discrete flavor model
predicts all 8 mixing parameters with zero free parameters.

**Challenge:** This is a survey finding about EXISTING models. It does not
prove that such a model is impossible. The history of physics contains many
examples where a problem was unsolved for decades before a breakthrough:

- The renormalizability of non-abelian gauge theories (unsolved 1954-1971)
- The existence of asymptotic freedom (unknown before 1973)
- The Higgs mechanism (not applied to electroweak theory until 1967)

A 20-year failure by the discrete flavor community does not prove
impossibility. It proves that existing approaches (A4, S4, Delta(27),
modular forms) have not succeeded. A NOVEL approach (e.g., using the
full E8 Weyl group instead of finite subgroups of SU(3)) might succeed
where these failed.

**Assessment: Correct but weak. The argument from absence is indeed not
a proof of impossibility. However, the 97% confidence reflects not just
failure but STRUCTURAL understanding of why existing approaches fail:
the discrete groups that appear in E8 (Z3, S3, etc.) produce
crystallographic angles (multiples of 30, 60 degrees), and mixing angles
are irrational. This is not a contingent failure -- it is a structural
mismatch between the output of discrete groups and the required output.
The challenge stands but does not substantially weaken the finding.**

---

## 3. The Wilson Bridge (Indirect Geometric Mixing via Mass Ratios)

### 3.1 The Chain of Inference

The devil's advocate argument for "geometric mixing" via Wilson proceeds
through a chain:

**Link 1: E8 determines particle content and generation structure.**
Status: [MV] (machine-verified in Lean 4). The decomposition 248 = 80 + 84
+ 84* under SU(9)/Z3, with 84 branching to three SM generations under
SU(5) x SU(4), is proved.

**Link 2: The Yukawa coupling 84 x 84* -> 80 is unique.**
Status: [SP] (Schur's lemma). The adjoint appears with multiplicity 1 in
84 x 84*. The overall coupling constant is the only freedom.

**Link 3: Different SU(5) sectors have different isoscalar factors.**
Status: [SP] (Chen's theorem). The isoscalar factors for SU(9) -> SU(5) x
SU(4) are given by symmetric group ISFs and are non-trivial. The (10,4)
sector and the (5,6) sector have different coupling weights.

**Link 4: The different coupling weights constrain the Yukawa hierarchy.**
Status: [CO] (computed observation). The non-trivial isoscalar factors give
different effective coupling strengths for up-type quarks, down-type quarks,
and leptons. This produces the GUT-scale mass ratios m_b/m_tau and m_s/m_mu,
which are partially constrained by E8 representation theory.

**Link 5: Wilson's formulas express mixing angles as functions of masses.**
Status: [CO] (independently verified to sub-sigma precision). The formulas
are reproducible. The mass equation holds at 3.95 ppm. The mixing angle
formulas hold at 0.08 to 0.83 sigma.

**Link 6: If E8 constrains masses (Links 1-4) and masses determine angles
(Link 5), then E8 indirectly constrains angles.**
Status: [CP] (candidate physics). This inference is logically valid but
depends on Links 4 and 5 both being non-accidental.

### 3.2 The Strength of the Chain

The chain has one STRONG segment (Links 1-2, verified mathematics), one
MODERATE segment (Links 3-4, standard representation theory applied to a
specific case), and one WEAK segment (Links 5-6, empirical formulas without
derivation).

The critical question: **Is Link 5 accidental or structural?**

**Arguments that Link 5 is structural:**

(a) Wilson's theta_12 formula has a GEOMETRIC interpretation. It is the
angle of the mass vector in a 2D plane perpendicular to (1,1,1), measured
from the mu-tau edge of an equilateral triangle. This is the NATURAL angle
in SU(3)_family space when the three generations are placed symmetrically
and the mass hierarchy breaks the symmetry. It is not an arbitrary
trigonometric combination -- it is the geometrically obvious construction.

(b) Wilson's CKM CP-phase formula arctan((m_n-m_p)/m_e) connects the
NEUTRON-PROTON mass difference to the CP phase. In the Standard Model,
the n-p mass difference has two contributions: QCD (strong isospin
breaking ~ 2.5 MeV) and QED (electromagnetic ~ -0.8 MeV). The net
1.293 MeV is a DERIVED quantity that encodes the ratio of strong to
electromagnetic effects. If the CP phase also encodes this ratio (which it
might, since CP violation mixes strong and weak sectors), the formula has
physical content.

(c) Wilson's mass equation m_e + m_mu + m_tau + 3m_p = 5m_n involves
EXACTLY the masses that appear in E8/SU(9) phenomenology: the three charged
leptons (from the three generations) and the lightest baryons (proton and
neutron). The integer coefficients (1,1,1,3,5) sum to 1+1+1+3+5 = 11,
which is one of the E8 exponents {1,7,11,13,17,19,23,29}. This may be a
coincidence, but it is the KIND of coincidence that would have structural
explanation in a unified framework.

**Arguments that Link 5 is accidental:**

(a) Post-hoc fitting. Wilson had access to all experimental values before
writing his formulas. He may have searched over functional forms until
finding matches. With ~20 masses and trigonometric functions, the space of
possible formulas is large.

(b) The Cabibbo angle derivation requires an ad hoc 20-degree subtraction
("purely conjectural" in Wilson's own words). The most important quark mixing
parameter is the one with the weakest derivation.

(c) Wilson's V_ub prediction is 4 sigma from experiment. He acknowledges this
but does not abandon the framework. This is the behavior of someone fitting
to successes and ignoring failures.

(d) The use of composite masses (proton, neutron) to predict fundamental
parameters is epistemologically backwards in the Standard Model framework.

### 3.3 Quantitative Assessment of the Wilson Bridge

**Structural fusion classification of "Wilson's formulas express a geometric
connection between E8 and mixing":**

- **Strip notation:** System S1 = {E8 root lattice, Weyl group, branching
  rules, CG coefficients}. System S2 = {mass ratios, trigonometric functions
  of mass ratios, mixing angles}.

- **Align axioms:**
  - S1 has discrete symmetry (W(E8)). S2 has continuous parameters.
    **Mismatch.**
  - S1 has representation theory -> multiplicities. S2 has mass ratios ->
    angles. **Mismatch** (multiplicities are integers, mass ratios are
    irrational).
  - S1 determines particle content. S2 uses particle masses.
    **Partial match** (content constrains what HAS mass, not the mass values).
  - S1's CG coefficients constrain coupling ratios. S2's mass ratios
    reflect coupling ratios (since masses come from Yukawa couplings x Higgs
    VEVs). **Match** (indirect).

- **Verdict: WEAK ANALOGY (40%).** The connection is real at the level of
  "E8 determines what exists, masses measure how much of it there is, and
  Wilson's formulas connect the measurements." But the bridge from CG
  coefficients to specific mass VALUES is not built. The analogy breaks at
  the dynamical step (Higgs VEVs).

This is an upgrade from the Round 1 assessment of COINCIDENCE (25%). The
system-level improbability (Section 1.4) and the geometric interpretation
of theta_12 (Section 3.2a) justify the upgrade. But it remains below
ANALOGY (60%) because the bridge has a missing span: no mechanism converts
E8 CG coefficients into the specific mass values that Wilson's formulas use.

### 3.4 What Would Promote the Wilson Bridge

The Wilson Bridge would be promoted from WEAK ANALOGY to ANALOGY if:

1. **The mass equation were derived from E8/SU(9).** Specifically: if the
   relation m_e + m_mu + m_tau + 3m_p = 5m_n could be shown to follow from
   the SU(9) Yukawa coupling combined with a specific (finitely-determined)
   symmetry-breaking pattern. This would connect Links 4 and 5.

2. **Wilson's theta_12 were derived from the adjoint flavon VEV.** If the
   SU(3)_family adjoint flavon VEV direction that minimizes the potential
   produces a mass hierarchy whose theta_12 (as defined by Wilson's mass-
   plane projection) equals the measured value, this would make the formula
   a PREDICTION rather than a FIT.

3. **The V_ub discrepancy were explained.** Wilson's 4-sigma failure on V_ub
   is a significant defect. If there were a structural reason why V_ub
   differs (e.g., higher-dimensional operators that affect third-generation
   quarks but not lighter particles), the system would be more credible.

The Wilson Bridge would be promoted to IDENTITY if:

4. **Wilson's formulas were theorems of E8 representation theory.** This
   would require proving that the SU(9) Yukawa coupling, combined with the
   unique minimum of the SU(9)-invariant Higgs potential, produces mass
   eigenvalues satisfying Wilson's mass equation and mixing angles satisfying
   Wilson's angle formulas. No one has attempted this derivation.

---

## 4. What Survives (Strong Form vs Weak Form)

### 4.1 Strong Form: DEAD

**"E8 geometry determines mixing angles."**

Dead. Killed by:
- KC-M5: SU(9) CG gives delta_{ij} in generation space
- KC-M1: No candidate mechanism produces correct angles from root geometry
- KC-R3: Z3 eigenspace is scalar times identity
- KC-R4: Generation labels have CP^3 freedom

No loophole in Section 2 revives this. The strong form is dead and should
stay dead.

### 4.2 Medium Form: ALIVE but WEAK

**"E8 representation theory constrains the texture of the Yukawa matrix,
reducing the parameter count below generic SU(5) + SU(3)_family models."**

Status: Alive, supported by three structural arguments:

(a) The antisymmetric coupling [84, 84] -> 84* provides a non-trivial
generation texture (Section 2.1, Loophole C). Combined with the symmetric
coupling [84, 84*] -> 80 (which gives delta_{ij}), the effective Yukawa
has a specific two-coupling structure determined by E8.

(b) The SU(3)_family confinement dynamics (if SU(3)_family is gauged and
confines near M_GUT) produces a non-perturbative Yukawa structure that is
NOT delta_{ij}, and whose form is constrained by the E8-determined gauge
structure.

(c) The isoscalar factors of Chen's theorem give different coupling weights
for different SU(5) sectors, constraining the GUT-scale mass ratios m_b/m_tau
and m_s/m_mu. These are not MIXING angles, but they are MASS RELATIONS that
reduce the parameter count.

**Honest assessment:** The medium form survives but does not produce testable
predictions without specifying the flavon sector. It reduces ~22 free
parameters to ~18-20 (through the Yukawa coupling uniqueness, the two-
coupling structure, and the sector-dependent isoscalar factors). This is a
modest improvement, not a breakthrough. It is the standard situation for
GUT models: the gauge structure constrains but does not determine the
flavor sector.

### 4.3 Weak Form: ALIVE and ANOMALOUS

**"E8 constrains the form of mixing matrices INDIRECTLY, through Wilson's
mass-ratio formulas, because E8 constrains masses and mixing angles are
determined functions of masses."**

Status: Alive. The Wilson connection is the genuinely interesting survivor.

**What is established:**
- Wilson's formulas are numerically correct (independently verified, <1 sigma)
- The system is statistically anomalous (~2 sigma jointly)
- The mass equation (3.95 ppm) has no known derivation but no known refutation
- The theta_12 formula has a natural geometric interpretation in generation space

**What is not established:**
- Why the formulas work
- Whether they are predictions or post-hoc fits
- The derivation of the mass equation from any Lagrangian
- The connection between composite masses and fundamental parameters

**The honest characterization:** Wilson has identified a PATTERN in the
data that uses E8-motivated particle content (three generations of leptons
plus baryons) and produces mixing angles from mass ratios via geometrically
natural constructions. The pattern is too precise and too systematic to
dismiss as coincidence (contra the Round 1 verdict of 25%), but too
unexplained to accept as physics (contra Wilson's own claims of
derivation).

The correct classification is: **unexplained empirical regularity of
moderate significance, possibly connected to E8 through mechanisms not
yet understood.** This is neither COINCIDENCE (too precise, too systematic)
nor IDENTITY (no derivation, no mechanism). It is **ANOMALY** -- a data
point that current theory does not explain and that may point to new
physics or may resolve into coincidence with further analysis.

---

## 5. Honest Verdict: Did the Hypothesis Survive the Devil's Advocacy?

### 5.1 The Strong Form Did Not Survive

E8 root geometry does not determine mixing angles. I could not save this.
The kill conditions (KC-M5, KC-M1, KC-R3, KC-R4) are correctly assessed
and I found no loophole that overturns them. The strong form is dead.

### 5.2 The Medium Form Barely Survived

E8 representation theory constrains the Yukawa texture modestly (through
the two-coupling structure, sector-dependent isoscalar factors, and possible
SU(3)_family confinement dynamics). But the constraints are weak: they
reduce the parameter space slightly without producing sharp predictions.
This is the generic situation for GUT models and does not distinguish the
SU(9)/E8 framework from other GUTs.

The medium form survives but is not worth pursuing further unless a specific
computation (the antisymmetric coupling CG coefficients, or the SU(3)_family
confinement dynamics) produces a sharper result than currently expected.

### 5.3 The Weak Form (Wilson Bridge) Survived and Poses a Genuine Question

This is the outcome the prosecution did not anticipate. Wilson's mass-ratio
formulas -- dismissed as numerology -- constitute a genuine anomaly:

- **Systematic:** 7-8 predictions from 5 inputs, all within 1 sigma
- **Precise:** mass equation at 3.95 ppm, CKM CP phase at 0.08 sigma
- **Geometrically motivated:** theta_12 has a natural interpretation as
  the mass-vector projection angle in SU(3)_family space
- **Unexplained:** no derivation from any Lagrangian or symmetry principle

The investigation should close the "geometric mixing from E8 root geometry"
question (answer: no). But it should NOT close the "Wilson mass-ratio
connection" question. That question is genuinely open and may have
implications for the project regardless of whether the answer involves
E8.

### 5.4 Revised Confidence Table

| Claim | R1 | R2 | R3 (This round) | Basis |
|-------|-----|-----|-----------------|-------|
| Zero-parameter geometric mixing from E8 root geometry impossible | 85% | 95% | **96%** | No loophole found in KC-M5, KC-M1 |
| Wilson theta_12 is mass-ratio function, not E8 invariant | 95% | 97% | **95%** | Confirmed but "mass-ratio function" may itself be E8-constrained |
| Wilson mass equation 3.95 ppm is coincidence | -- | 50% | **35%** | System-level improbability argument (Sec 1.4) |
| Wilson mass equation is derivable from some algebraic framework | -- | -- | **30%** | No derivation exists, but precision is anomalous |
| SU(9) CG factorize (delta_{ij} in gen. space) | 65% | 88% | **90%** | No loophole overturns KC-M5 for leading-order coupling |
| Antisymmetric coupling [84,84]->84* gives non-trivial texture | -- | -- | **60%** | Structural argument (Loophole C), untested |
| E8 constrains Yukawa texture beyond generic SU(5)+SU(3) | -- | -- | **45%** | Medium form: modest constraints from 2 couplings + ISFs |
| Wilson's system is statistically anomalous (>2 sigma jointly) | -- | -- | **70%** | Joint probability ~0.047 for 8 independent <1-sigma matches |
| Investigation should close with negative result on H1 | 60% | 85% | **95%** | H1 (strong form) definitively killed |
| Investigation should leave H3 (Wilson bridge) as open question | -- | -- | **75%** | Cannot be killed or confirmed with available data |

### 5.5 Recommendations

1. **Close the "geometric mixing from E8" investigation with a negative
   result.** The strong form is dead. Report this honestly.

2. **Flag Wilson's mass-ratio system as an unexplained anomaly.**
   Classification: not COINCIDENCE (too precise), not IDENTITY (no
   derivation), but ANOMALY. This should be noted in the synthesis
   document as an open question for future work.

3. **The highest-value future computation is the antisymmetric coupling
   [84, 84] -> 84*.** This is the only untested structural contribution
   to the Yukawa matrix from E8. If it produces a non-trivial texture
   in generation space (unlike the symmetric coupling), it would
   strengthen the medium form.

4. **Do NOT pursue Wilson's program further without Wilson's cooperation
   or independent derivation.** Wilson's formulas are empirical. Without
   a theoretical derivation, pursuing them is numerology, not physics.
   The correct stance is: "these formulas work and we don't know why."

5. **For Papers 3 and 4:** No revision needed. The papers correctly state
   that mixing angles require dynamical input beyond E8. The Wilson
   anomaly, if mentioned at all, should be in a brief remark in the
   discussion section, classified as [CO] (computed observation) with a
   note that it is unexplained.

---

## Files Referenced

- `research/council/e8-mixing-angles/00-charter.md`
- `research/council/e8-mixing-angles/01-vision.md`
- `research/council/e8-mixing-angles/02-archaeology.md`
- `research/council/e8-geometric-flavor/05-synthesis.md`
- `research/heptapod-b-yukawa-vision.md`
- `research/wilson-three-generation-comparison.md`
- `research/yukawa-kill-condition-research.md`
- `src/experiments/results/su9_cg_coefficients.json`
- `src/experiments/results/yukawa_texture_analysis.json`
- `src/experiments/results/wilson_pmns_verification.json`
- Wilson arXiv:2102.02817, 2407.18279, 2507.16517
- Chen, J. Math. Phys. 22, 1-6 (1981)
- Feruglio, "Are neutrino masses modular forms?" (2017)
