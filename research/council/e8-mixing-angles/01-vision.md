# Round 1: VISION -- Geometric Mixing Angles from E8

**Agent:** Heptapod B Architect
**Date:** 2026-03-17
**Investigation:** e8-mixing-angles (Real Run)
**Status:** Complete

---

## 0. Methodological Note

This document executes the seven-step teleological reasoning method. The
conclusion is seen from the beginning: **the answer to "can E8 root geometry
determine mixing angles?" is almost certainly NO for a zero-parameter
derivation, but there is a precisely identifiable mathematical structure --
the Weyl group action on branching multiplicities -- that could reduce the
parameter count below the flavon approach, and Wilson's construction
identifies the exact location where this structure lives, even though his
specific angle computations are not geometric derivations but mass-ratio
fits dressed in geometric language.**

---

## 1. Teleological Vision (Necessary Structure)

### Step 1: Assume the Solution Exists

*The solution exists. I am reading it. What does it say?*

A geometric mixing mechanism in E8 is a mathematical construction that:
- Takes as input ONLY the E8 root system (240 roots in R8), its Weyl group
  W(E8) of order 696,729,600, and the lattice automorphisms
- Produces as output one or both of the CKM and PMNS matrices (3x3 unitary,
  8 total real parameters: 3 angles + 1 phase each)
- Has zero continuous free parameters (discrete choices are acceptable if
  the number of choices is finite and the correct one is selected by a
  principle, not by fitting)

If such a thing existed, it would be a theorem of the form:

> **Theorem (hypothetical).** Let Phi be the E8 root system and W its Weyl
> group. Let sigma in W be the type-5 Z3 element with centralizer SU(9)/Z3.
> Then the restriction of the adjoint representation to SU(5) x SU(3)_fam,
> combined with a specific geometric projection operator P_geom defined by
> root inner products, uniquely determines a 3x3 unitary matrix U whose
> entries are algebraic numbers, and this U agrees with the PMNS matrix to
> within experimental error.

### Step 2: What MUST the Solution Contain?

**N1 (Unitarity).** The output must be a 3x3 unitary matrix. This means we
need a map from E8 data to U(3). The natural such maps are:
- Weyl group elements (W(E8) acts on R8; restriction to a 3-plane gives O(3))
- Branching rule matrices (coefficients when restricting representations)
- Clebsch-Gordan coefficients (tensor product decomposition)
- Projection operators onto root subsystems

**N2 (Three-dimensionality).** The output acts on a 3-dimensional space
(the generation space). This space must be identified WITHIN E8 in a
canonical way. The only candidate is the SU(3) factor in E8 -> E6 x SU(3)
or the SU(3)_fam in E8 -> SU(9)/Z3 -> SU(5) x SU(3)_fam x U(1).

**N3 (Basis independence).** The mixing matrix must be a geometric invariant,
not a coordinate artifact. This means it must be defined by ROOT GEOMETRY
(inner products, angles, lengths) or REPRESENTATION THEORY (multiplicities,
Casimir eigenvalues), not by a choice of basis in the Cartan subalgebra.

**N4 (Correct numerical values).** The CKM matrix has small off-diagonal
entries (Cabibbo angle ~13 deg). The PMNS matrix has large off-diagonal
entries (theta_12 ~33 deg, theta_23 ~49 deg). Any geometric mechanism must
produce BOTH patterns from the same E8, differentiated only by which sector
(quarks vs leptons) is being examined. This is a severe constraint.

**N5 (CP violation).** Both CKM and PMNS have nonzero CP-violating phases
(delta_CKM ~68 deg, delta_PMNS ~194 deg). A purely real geometric
construction cannot produce these. The mechanism MUST involve complex
structure somewhere -- either through the complex representations of SU(9),
or through the complexification of the root system.

---

## 2. Candidate Mechanisms (Inventory with Viability)

I enumerate every mathematical structure in E8 that could conceivably
connect root geometry to unitary rotation matrices.

### Candidate A: Weyl Group Elements as Rotation Matrices

**The idea.** W(E8) has order 696,729,600. Its elements act on R8 by
orthogonal transformations. The SU(9)/Z3 embedding defines a 3-dimensional
"generation subspace" (the root space of SU(3)_fam). Restricting a Weyl
group element to this 3-plane gives an element of O(3). Specific Weyl group
elements could define the CKM or PMNS rotation.

**Viability: LOW (20%).**

The problem is not finding rotations -- W(E8) contains plenty. The problem
is SELECTING the right one. W(E8) restricted to the SU(3)_fam Cartan
gives the Weyl group of SU(3), which is S3 (order 6). S3 acting on R2
produces only rotations by multiples of 60 degrees and reflections. These
are the WRONG angles (CKM needs ~13 deg, PMNS needs ~33 deg).

To get non-trivial angles, we would need Weyl group elements that are NOT
in the SU(3)_fam Weyl group -- i.e., elements that MIX the generation
directions with other E8 directions. But then the 3x3 matrix is obtained by
projecting an 8x8 orthogonal matrix onto a 3-plane, and the result depends
on the choice of projection (violating N3).

**Kill condition test:** The Weyl group of SU(3) acting on the generation
Cartan is S3 = {id, (12), (13), (23), (123), (132)}. This group is
discrete with rotations only at 0, 120, 240 degrees. No Cabibbo angle
here. CANDIDATE A FAILS N4.

### Candidate B: Root System Angles

**The idea.** The E8 root system has specific angles between roots. Under
E8 -> SU(9), the 240 roots decompose into groups. The angles between roots
in different SU(5) x SU(3) sectors might define mixing angles.

**Viability: VERY LOW (10%).**

The angles between E8 roots are highly constrained: for a simply-laced root
system, the angle between any two roots is one of {0, 60, 90, 120, 180}
degrees. None of these is 13 degrees (Cabibbo) or 33 degrees (solar PMNS).
The only way to get non-standard angles is through linear combinations of
roots, but then the construction depends on which linear combinations you
choose (violating N3 again).

**Kill condition test:** Inner products of E8 roots take values in
{0, +/-1, +/-2}. The angle arccos(1/2) = 60 deg appears but not 13 or 33.
CANDIDATE B FAILS N4.

### Candidate C: Coxeter Element and Coxeter Number

**The idea.** E8 has Coxeter number h = 30. A Coxeter element (product of
all simple reflections) has order 30. Its eigenvalues are exp(2*pi*i*m_j/30)
where m_j are the exponents {1, 7, 11, 13, 17, 19, 23, 29}. The angles
2*pi*m_j/30 could relate to mixing angles.

**Viability: LOW (15%).**

The Coxeter angles are 12, 84, 132, 156, 204, 228, 276, 348 degrees. None
of these is directly a CKM or PMNS angle. One COULD note that 360/30 = 12,
which is close to the Cabibbo angle (13.04), but this is a 1-degree
discrepancy (8% relative error), and there is no mechanism to bridge it.

More damaging: the Coxeter element lives in the FULL 8-dimensional space,
not in the 2-dimensional generation Cartan. Projecting it onto the
generation subspace is again basis-dependent.

**Kill condition test:** Closest Coxeter angle to Cabibbo = 12 deg
(vs 13.04 measured). Relative error 8%. No mechanism for correction.
CANDIDATE C IS MARGINAL -- does not pass N4 cleanly but is close enough
to investigate further.

### Candidate D: McKay Correspondence

**The idea.** The McKay correspondence connects finite subgroups of SU(2)
to ADE Dynkin diagrams. E8 corresponds to the binary icosahedral group
2I (order 120). The representation theory of 2I has specific characters
that could define mixing matrices.

**Viability: LOW (15%).**

The McKay correspondence gives a BIJECTION between irreps of 2I and nodes
of the E8 Dynkin diagram. It does NOT naturally produce 3x3 unitary
matrices. To get a mixing matrix, one would need to:
1. Identify 3 specific irreps of 2I as "generations"
2. Define an inner product between them using the McKay graph
3. Extract rotation angles from this inner product

Step (1) is arbitrary (2I has 9 irreps; choosing 3 requires a principle).
Step (2) has been done (the McKay graph gives adjacency matrix = Cartan
matrix), but the resulting matrix is integer-valued, not unitary.

**Kill condition test:** The McKay graph adjacency matrix for E8 is the
extended Cartan matrix, which is a 9x9 integer matrix with eigenvalues
related to Coxeter exponents. No 3x3 unitary submatrix with CKM-like
entries. CANDIDATE D FAILS N1.

### Candidate E: Branching Rule Coefficients

**The idea.** When E8 representations branch under subgroups, the branching
multiplicities define matrices. The 248 under E8 -> SU(5) x SU(3) gives
specific multiplicities. These multiplicities, suitably normalized, could
define rotation angles.

**Viability: MODERATE (35%).**

This is the most promising purely algebraic candidate. The branching
248 -> sum of (R_SU5, R_SU3) pairs gives a matrix of integers (branching
multiplicities). If we focus on the (10, 3) + (5-bar, 3) + (1, 3) sectors
-- the three irreps of SU(3)_fam that appear with different SU(5) quantum
numbers -- the CG coefficients for the Yukawa coupling 84 x 84* -> 80
define a 3x3 matrix in generation space.

The problem: this matrix is determined by SU(9) representation theory
(Schur's lemma makes it unique up to normalization), so it is proportional
to the identity. The Z3 eigenspace projection is scalar x identity, as
the test run established at 95% confidence (KC-R3).

HOWEVER: the CG coefficients for DIFFERENT SU(5) sectors (10 vs 5-bar vs 1)
within the 84 have different numerical values. If the Yukawa coupling
involves a sum over sectors with different CG weights, the effective 3x3
mass matrix is NOT proportional to identity -- it has a nontrivial texture
determined by the CG coefficients.

**Kill condition test:** This is exactly the computation planned for M8.1-8.3.
If the SU(9) CG coefficients factorize completely as (SU(5) part) x (SU(3)
part), then the generation mixing is trivial and CANDIDATE E FAILS.
If they do NOT factorize, the non-factorizable part defines a geometric
mixing contribution. STATUS: UNTESTED.

### Candidate F: Wilson's Group Algebra Construction

**The idea.** Wilson (arXiv:2102.02817, 2507.16517) does NOT derive mixing
angles from E8 root geometry. He derives them from the GROUP ALGEBRA of
finite symmetry groups (Z3, Q8, binary tetrahedral group 2T), using mass
ratios as inputs. His approach is:

1. Embed 3 generations as vertices of equilateral triangle in mass plane
2. Define a "mass direction" using measured lepton masses (e, mu, tau)
3. Compute the angle between this direction and a triangle edge
4. This gives theta_12 = arctan(sqrt((tau - mu)/(tau - e))) ~ 33.02 deg

For the Cabibbo angle, he subtracts 20 degrees from theta_12, arguing
that "the generation symmetry for quarks cubes to the colour symmetry
rather than cubing to the identity," introducing rotations of order 9
(hence 360/9 = 40, and the 20 deg comes from 40/2).

For CKM angles, he uses mass ratios of electron, proton, and neutron.

**Viability as GEOMETRIC mechanism: LOW (20%).**
**Viability as MASS-RATIO-BASED mechanism: MODERATE (50%).**

Wilson's construction is honest about its nature: it uses measured masses
as inputs and the group algebra of FINITE groups (not E8 root geometry) as
the organizing principle. The E8 connection enters only in providing the
ALGEBRAIC FRAMEWORK (SU(9)/Z3, three generations) within which the finite
group algebra sits.

The striking numerical agreements (theta_12 = 33.02 vs 33.41 +/- 0.75,
theta_13 = 8.586 vs 8.54 +/- 0.12) are real but their significance is
uncertain because:
- theta_12 follows from lepton masses (3 inputs -> 1 output, not zero-parameter)
- theta_13 requires an ad hoc splitting
- the Cabibbo angle subtraction (20 deg from order-9 rotation) is conjectural

**Kill condition test:** KC-M3 asks whether Wilson's derivation is
reproducible. His theta_12 IS reproducible (it is just arctan of a mass
ratio). His Cabibbo angle subtraction is NOT derived from E8 geometry.
CANDIDATE F PARTIALLY PASSES (mass-ratio part) and PARTIALLY FAILS
(geometric-derivation part).

---

## 3. Wilson Deconstruction (What Is He Actually Computing?)

This section is critical. Wilson's work is the ONLY extant claim of mixing
angles from E8-adjacent mathematics. Understanding exactly what he does
and does not compute determines the trajectory of this investigation.

### Wilson Paper 1: "Finite symmetry groups in physics" (2102.02817)

Wilson's 2021 paper (v5, 60+ pages) develops a systematic program:

**Core method:** Replace continuous gauge groups with their finite subgroups
(Z3 for U(1), Q8 for SU(2), 2T for the combined electroweak group). Then
use the GROUP ALGEBRA of these finite groups as the organizing structure.
The group algebra naturally decomposes into irreducible components that
match the Standard Model representation structure.

**Mixing angle derivations (what he actually computes):**

1. **theta_12 (PMNS solar angle):** Embed 3 electron generations as
   vertices of equilateral triangle in 2D mass plane. Mass direction is
   defined by vector (m_e, m_mu, m_tau) projected onto this plane. The
   angle between the mass direction and a triangle edge gives:

   theta = angle of mass-deviation vector from mu-tau edge
           of equilateral triangle in generation space

   Concretely: place three generation vertices at 120-degree intervals
   in a 2D plane perpendicular to (1,1,1) in mass space. The mass
   vector (m_e, m_mu, m_tau) projects onto this plane as a deviation
   from the centroid. The angle between this deviation and the mu-tau
   edge is theta ~ 33.024 deg.

   Using m_e = 0.511 MeV, m_mu = 105.66 MeV, m_tau = 1776.86 MeV:
   theta = 33.024 deg (independently verified numerically)

   **INPUT:** three measured lepton masses.
   **OUTPUT:** one angle (33.024 deg).
   **GEOMETRIC CONTENT:** the equilateral triangle (Z3 symmetry).
   **VERDICT:** This is NOT a zero-parameter prediction. It is a 3-to-1
   reduction (3 masses -> 1 angle). The angle is a FUNCTION OF MASSES,
   not a geometric invariant of E8.

2. **Electroweak mixing angle:** From the Z4 symmetry of fermion types
   (nu, e, d, u as vertices of a square), Wilson computes:

   tan(2*phi) = 3/2, giving phi/2 ~ 28.155 deg

   Alternatively sin^2(theta_W) ~ 3/13 = 0.2308 (exact)

   **INPUT:** the number of fermion types (4) and their charge assignments.
   **OUTPUT:** sin^2(theta_W) = 3/13.
   **GEOMETRIC CONTENT:** the square (Z4 symmetry) in the charge plane.
   **VERDICT:** This IS a zero-parameter prediction (3/13 = 0.2308 vs
   measured 0.2312 at M_Z). It is numerologically striking but the
   derivation assumes that the four fermion types sit at square vertices
   in a specific charge/hypercharge plane, which is a MODEL ASSUMPTION,
   not a theorem of E8.

3. **CKM angles from mass ratios:** Using the quaternionic group algebra
   of Q8, Wilson spans a 4-space with (3 generations of electron + proton).
   He then computes angles from mass ratios:

   arctan(m_e/(m_p - m_n)) ~ 21.1 deg (CKM CP phase ~ 21.1 vs ~20.9 exp.)
   arctan(m_e/(m_n - m_p)) ~ 14.4 deg (CKM 2-3 mixing ~ 14.4 vs ~14.5 exp.)

   The key mass ratio is m_e / (m_n - m_p):
   arctan(m_e/(m_n - m_p)) = 21.56 deg, complement = 68.44 deg
   arctan((m_n - m_p)/m_e) = 68.44 deg (vs CKM delta_CP ~ 68.8 +/- 4.5)

   Wilson uses the complement form. The 68.44 deg prediction matches
   the CKM CP-violating phase at 0.08 sigma. Independently verified
   numerically.

4. **Cabibbo angle:** Wilson subtracts 20 deg from theta_12 to get
   ~13.02 deg, justifying 20 deg as coming from the difference between
   order-3 (generation) and order-9 (generation x color) symmetry.

   **INPUT:** theta_12 (itself derived from masses) plus conjectural
   order-9 hypothesis.
   **OUTPUT:** Cabibbo angle ~ 13.02 deg.
   **GEOMETRIC CONTENT:** The order-9 conjecture.
   **VERDICT:** This is the most speculative step. The 20-degree
   subtraction has no derivation beyond "it is easy to imagine that a
   20 deg rotation arises from the difference between a 4/9 rotation
   and a 1/2 rotation" (his words).

### Wilson Paper 2: "Embeddings of the Standard Model in E8" (2507.16517)

This later paper shifts from finite group algebras to the Lie algebra
so(7,3) as the relevant structure:

- Claims SO(7,3) = Spin(7,3) contains all of the Standard Model
- The mixing angles "depend on masses" and masses "emerge from quantum
  interactions with the dynamic background spacetime (vacuum)"
- Gives the same theta_12 = 33.024 calculation (lepton mass formula)
- Introduces a mass equation: m_e + m_mu + m_tau + 3*m_p = 5*m_n
  (remarkably accurate to experimental precision)
- Derives CKM angles from m_e/m_p and m_e/m_n mass ratios

**Key observation:** Wilson's 2025 paper DOES NOT use E8 root geometry to
derive mixing angles. He uses mass ratios computed within a framework that
USES E8 to organize the particle content. The E8 provides the stage
(representation slots, generation structure), and the mass ratios provide
the script. The angles are functions of masses, period.

### Summary Verdict on Wilson

| Claim | Method | Inputs | Status |
|-------|--------|--------|--------|
| theta_12 = 33.02 | Mass ratio in Z3 group algebra | m_e, m_mu, m_tau | REPRODUCIBLE, not zero-parameter |
| sin^2(theta_W) = 3/13 | Charge geometry in Z4 group algebra | Number of fermion types | ZERO-PARAMETER but model-dependent |
| Cabibbo = theta_12 - 20 | Conjectural order-9 subtraction | theta_12 + hypothesis | CONJECTURAL |
| CKM CP phase | arctan((m_n-m_p)/m_e) in Q8 group algebra | m_e, m_p, m_n | REPRODUCIBLE: 68.44 vs 68.8+/-4.5 (0.08 sigma) |
| m_tau prediction | Mass equation from generation symmetry | m_e, m_mu, m_p, m_n | STRIKING (18.5 keV = 3.9 ppm, 0.15 sigma) |

**Structural fusion verdict on "Wilson derives mixing from E8 geometry":**
**COINCIDENCE (25%).** Wilson derives mixing from MASS RATIOS organized by
FINITE GROUP ALGEBRAS. E8 enters only as the ambient algebraic structure
that justifies the existence of 3 generations and specific fermion types.
The mixing angles themselves are not E8 invariants; they are mass-ratio
functions. The E8 connection is real at the organizational level but absent
at the computational level.

---

## 4. KC-M1 Preliminary Assessment

**Kill condition KC-M1:** "No mathematical structure in E8 connects root
geometry to unitary rotation matrices."

### Assessment: KC-M1 does NOT fire FATAL, but fires SERIOUS.

**Why it does not fire FATAL:**

There IS a mathematical structure connecting E8 to unitary matrices:
the Clebsch-Gordan coefficients of the SU(9) Yukawa coupling
(84 x 84* -> 80). These CG coefficients are determined by E8
representation theory and produce a 3x3 matrix in generation space
(Candidate E above). Whether this matrix is trivial (proportional to
identity) or nontrivial is the untested question for M8.1-M8.3.

**Why it fires SERIOUS:**

Every candidate mechanism examined (A through D) fails at least one
necessary condition (N1-N5). The only surviving candidate (E, CG
coefficients) requires a specific computation that the test run
identified as likely to produce a trivial result (the SU(9) coupling
is unique by Schur's lemma, and the Z3 projection is scalar x identity).
The SU(9) CG coefficients might produce non-trivial generation structure
through DIFFERENT SU(5) sector weights, but this is the sole remaining
hope, not a broad landscape of possibilities.

Wilson's approach (F) produces numerical matches but is not a geometric
derivation from E8.

**Verdict:** Proceed to Round 2 with SERIOUS caution. The question is
sharply focused: do SU(9) CG coefficients for different SU(5) sectors
produce non-trivial generation mixing? Everything else is dead or
Wilson-style mass fitting.

---

## 5. The Gap (Step 4 of Teleological Reasoning)

### What exists:
- E8 root system, Weyl group, representation theory [STANDARD]
- SU(9)/Z3 decomposition 248 = 80 + 84 + 84* [MV, Lean-verified]
- Z3 eigenspace is scalar x identity [COMPUTED, 95%]
- Yukawa coupling 84 x 84* -> 80 is unique [STANDARD, Schur's lemma]
- Wilson's mass-ratio formulas for mixing angles [REPRODUCIBLE, not geometric]
- Branching 84 -> (10,1) + (10,3) + (5,6) + (1,4-bar) under SU(5) x SU(4) [MV]

### What is missing:
- **The SU(9) CG coefficients for different SU(5) sectors.** Specifically:
  the relative coupling strength of (10,3) x (10-bar,3-bar) -> (24,1)
  vs (5,3-bar) x (5-bar,3) -> (24,1) within the 84 x 84* -> 80 coupling.
  If these are DIFFERENT, the effective Yukawa matrix in generation space
  has a nontrivial texture determined by E8 representation theory.
  If they are the SAME, the generation structure is trivial and E8 adds
  nothing beyond standard SU(5) + SU(3)_family.

- **A mechanism to connect Wilson's mass-ratio angles to E8 geometry.**
  Wilson's theta_12 = arctan(sqrt((m_tau - m_mu)/(m_tau - m_e))) matches
  experiment beautifully. But WHY should this mass ratio equal a group
  algebra angle? If E8 geometry constrains the mass ratios (not just the
  mixing angles), then Wilson's formulas become PREDICTIONS rather than
  fits. But no mechanism for E8-determined mass ratios is known.

- **A basis-independent construction.** All candidates that produce
  non-trivial angles do so by projecting high-dimensional objects onto
  low-dimensional subspaces. The projection is basis-dependent. What is
  needed: a construction that produces an INVARIANT (like a trace, a
  determinant, or a cross-ratio) that happens to equal a mixing angle.

### The precise gap:
**A theorem connecting SU(9) CG coefficients to the texture of the 3x3
Yukawa matrix in generation space, where the texture is non-trivial and
determined by E8 representation theory alone (not by flavon VEV alignment).**

This gap is either:
(a) Fillable -- the CG coefficients are non-trivially sector-dependent,
    giving at most 1-3 constraints on the 8 mixing parameters.
(b) Unfillable -- the CG coefficients factorize, giving zero constraints,
    and mixing is entirely determined by dynamics (flavon sector).

The M8.1-M8.3 computation will decide.

---

## 6. The Bridge (If It Existed)

Using the constructive vision methodology: what would fill the gap?

### Constraint satisfaction:
- C1: Must be a 3x3 matrix in generation space (unitary or Hermitian)
- C2: Must be determined by E8 data (root system, CG coefficients)
- C3: Must differentiate quark and lepton sectors
- C4: Must contain CP violation (complex entries)
- C5: Must reduce to known limits (identity matrix when SU(3)_fam is unbroken)

### The simplest satisfying object:
A "geometric Yukawa tensor" Y^{ij}_a defined by:

Y^{ij}_a = sum over SU(5) sectors R of:
  CG(84_i x 84*_j -> 80) restricted to (R, R*) -> adj
  weighted by sector-dependent E8 root geometry factor f_R

where i,j = 1,2,3 are generation indices and a = 1,...,80 is the adjoint
index.

If f_R is the same for all sectors, Y^{ij}_a is proportional to delta^{ij}
and we get trivial mixing. If f_R varies across sectors (10 vs 5-bar vs 1),
we get nontrivial texture.

The sector-dependent factor f_R would need to arise from E8 ROOT GEOMETRY --
for example, from the number of E8 roots that project onto a given
SU(5) x SU(3) sector, or from the lengths of such projections. This is
computable from the branching rules.

### The bridge I CANNOT build:
Even if f_R is non-trivial, the resulting Y^{ij}_a gives a Yukawa TEXTURE
(pattern of zeros and relative magnitudes), not specific angles. Going from
texture to angles requires knowing the eigenvalues (masses), which are
dynamical. So the best possible outcome is:

**E8 representation theory constrains the TEXTURE of the Yukawa matrix,
reducing the 8 mixing parameters by 1-3 (through relations between quark
and lepton sectors). The remaining parameters are dynamical (mass-dependent).**

This is a PARTIAL answer, not a full derivation. It is the maximum that
the mathematics can deliver.

---

## 7. Kill Conditions (Step 6)

| # | Condition | Test | Status | Severity |
|---|-----------|------|--------|----------|
| KC-M1 | No structure connects E8 to unitary rotation matrices | Enumerate candidates (done above) | SERIOUS (not FATAL) -- one candidate survives | SERIOUS |
| KC-M2 | All candidates reduce to flavon VEV alignment | Compute SU(9) CG coefficients (M8.1-8.3) | UNTESTED | FATAL |
| KC-M3 | Wilson's angles irreproducible or require hidden inputs | Reproduce Wilson's theta_12 and Cabibbo computations | PARTIALLY TESTED -- theta_12 reproducible, Cabibbo conjectural | SERIOUS |
| KC-M4 | Only paths to mixing are already covered by test run | This vision identifies Candidate E (CG sector weights) as new | PASSED (new path identified) | FATAL |
| KC-M5 (new) | SU(9) CG coefficients factorize completely (trivial generation structure) | SageMath computation | UNTESTED | FATAL |
| KC-M6 (new) | Wilson's mass equation m_e + m_mu + m_tau + 3m_p = 5m_n is coincidence | Check precision, compute higher-order corrections | UNTESTED | INFORMATIONAL |

**The cheapest kill is KC-M5.** If SU(9) CG coefficients factorize as
(SU(5) CG) x (SU(3) CG), then E8 adds ZERO generation mixing beyond
generic SU(5) + SU(3)_fam models. This can be checked in 1-2 days with
SageMath and would terminate the "geometric mixing from E8" program.

---

## 8. Recommendations for Round 2

The Round 2 Polymathic Researcher should investigate exactly **two**
targeted questions:

### Question 1: SU(9) CG Factorization

**Do the Clebsch-Gordan coefficients of the SU(9) Yukawa coupling
(84 x 84* -> 80), when decomposed under SU(5) x SU(4), factorize as
independent SU(5) and SU(4) contributions? Or do they contain
non-factorizable "entanglement" between the GUT and family sectors?**

This is the make-or-break computation. Literature search should focus on:
- Slansky's tables (Phys. Rep. 79, 1981) for SU(9) branching
- Any computation of SU(N) CG coefficients for exterior powers Lambda^k
- Whether Schur-Weyl duality forces the factorization

**If factorized:** KC-M5 fires FATAL. Geometric mixing from E8 is dead.
**If not factorized:** This is the mechanism. Quantify the non-trivial part.

### Question 2: Wilson's Finite Group Algebra -- Mathematical Status

**What is the mathematical status of Wilson's group algebra program?
Specifically: (a) Is the mass equation m_e + m_mu + m_tau + 3m_p = 5m_n
a theorem of some algebraic framework, or an empirical coincidence?
(b) Is the theta_12 mass-ratio formula derivable from E8 representation
theory, or is it specific to the finite group algebra approach?
(c) Has anyone other than Wilson reproduced his angle calculations?**

This determines whether Wilson's work is:
- A genuine mathematical program that could interface with our Lean proofs
- A collection of striking numerological coincidences
- Something in between (a correct observation about mass-angle correlations
  that lacks a derivation)

### Question NOT to ask in Round 2:

Do NOT investigate further discrete flavor symmetry models (A4, S4, Delta(27)).
The test run established at 97% confidence that no such model predicts all
8 mixing parameters at zero free parameters. This door is closed.

---

## 9. Confidence Calibration

| Claim | Confidence |
|-------|-----------|
| Zero-parameter geometric mixing from E8 root geometry is impossible | 85% |
| Wilson's theta_12 is a mass-ratio function, not an E8 invariant | 95% |
| Wilson's mass equation is numerically accurate (sub-MeV) | 90% (needs independent check) |
| SU(9) CG coefficients factorize (KC-M5 will fire) | 65% |
| If CG does NOT factorize, it provides 1-3 constraints on mixing | 70% (conditional) |
| Wilson's 20-degree Cabibbo subtraction has no derivation | 95% |
| The maximum achievable from E8 is texture constraints, not angle values | 80% |
| Wilson's program, despite striking matches, is not peer-reviewed physics | 99% (factual) |
| This investigation will close with a negative result (no geometric mixing) | 60% |

---

## 10. The Honest Verdict

Seen from the end, the landscape is bleak for zero-parameter geometric
mixing from E8. The root geometry produces only crystallographic angles
(multiples of 30 and 60 degrees). The Weyl group, restricted to the
generation subspace, gives only the symmetric group S3. The representation
theory, channeled through Schur's lemma, produces identity matrices in
generation space.

The ONE surviving hope is that the SU(9) Clebsch-Gordan coefficients, when
decomposed under SU(5) x SU(4), carry non-trivial "entanglement" between
the GUT and family sectors. This would not give mixing ANGLES (those depend
on masses), but it would give mixing TEXTURES (patterns of which entries
are zero, and what their relative magnitudes are). This is a weaker but
still valuable result -- it would mean E8 constrains the FORM of the CKM
and PMNS matrices even if it does not fix the VALUES.

Wilson's work is valuable not because it derives angles from geometry
(it does not), but because it demonstrates a CORRELATION between mass ratios
and mixing angles that may have a deeper explanation. Whether that
explanation lives in E8, in finite group algebras, or in something else
entirely, remains open.

The algebra gives the stage. The masses write the script. But the stage
might constrain the script more than we currently know.

---

## Files Referenced

- `research/council/e8-mixing-angles/00-charter.md`
- `research/heptapod-b-yukawa-vision.md`
- `research/wilson-three-generation-comparison.md`
- `research/yukawa-kill-condition-research.md`
- `src/experiments/results/wilson_pmns_verification.json`
- Wilson arXiv:2102.02817 ("Finite symmetry groups in physics")
- Wilson arXiv:2407.18279 ("Uniqueness of an E8 model")
- Wilson arXiv:2507.16517 ("Embeddings of the Standard Model in E8")
