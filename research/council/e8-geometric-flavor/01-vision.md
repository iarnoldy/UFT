# Round 1: VISION -- Teleological Analysis of the Three-Generation Problem in E8

**Date:** 2026-03-17
**Agent:** Heptapod B Architect
**Investigation:** e8-geometric-flavor
**Status:** COMPLETE

---

## Step 0: Methodological Note

This analysis follows the seven-step teleological reasoning method. I assume the
solution exists, characterize its necessary structure, inventory what exists, identify
the precise gap, assess whether a bridge can be built, and check kill conditions. The
Wilson Principle applies throughout: honesty before harmony. The Optik of Berlinski
applies throughout: say exactly what is true, not more, not less.

---

## Section 1: Teleological Vision

**The question:** Is there a mathematical structure beyond SU(9)/Z_3 that
distinguishes exactly 3 generations in E_8 without assuming Z_3 as input?

**Assume the solution exists. What does it look like?**

The solution, if it exists, would be a theorem of the form:

> **Theorem (Hypothetical):** Let g = e_8 and let phi be [some intrinsic structure
> of E_8]. Then phi induces a decomposition of the matter representation into
> exactly N copies of a standard model generation, where N is determined by
> [some invariant of phi]. For E_8, N = 3.

The solution MUST satisfy all of the following:

**N1.** The number 3 emerges as OUTPUT, not INPUT. It must follow from a property
of E_8 that does not have "3" built into its definition.

**N2.** The mechanism must distinguish 3 from 2, 4, and other small integers. Not
just "3 appears somewhere in E_8" but "3 is the UNIQUE answer to a well-posed
question about E_8."

**N3.** The mechanism must connect to the Standard Model generation structure:
three copies of (16 of SO(10)) or equivalent, with the correct quantum numbers
for quarks and leptons.

**N4.** The mechanism must be compatible with the Distler-Garibaldi chirality
obstruction (no net chirality from E_8 in a single real form). Either it works
within that constraint (via massive fermions and decoupling of mirrors) or it
explicitly evades it (via multiple real forms or other mechanism).

**N5.** If the mechanism produces mixing angles, those angles must be geometric
invariants of E_8, not dependent on basis choices or free parameters.

---

## Section 2: Candidate Structures

I now inventory every mathematical structure in E_8 that contains or produces the
number 3, and assess whether each could satisfy N1-N5.

### Candidate 1: Z_3 center of SU(9) (The Wilson Route)

**What it is:** E_8 contains SU(9)/Z_3 as a maximal subgroup. The Z_3 is a
discrete automorphism that decomposes 248 = 80 + 84 + 84*. Under SU(5) x SU(4),
the 84 contains 3 copies of the 16 via (10,3) + (5-bar,3-bar) + (1,3-bar).

**Assessment:**
- N1: FAILS. The number 3 enters as dim(fundamental of SU(3)_family) = 3.
  Wilson's argument starts from "require Z_3" and derives SU(9)/Z_3 as unique.
  But WHY Z_3? The answer "because 3 generations" is circular.
- N2: PASSES within its own framework: Wilson shows Type 5 is unique among Z_3
  conjugacy classes.
- N3: PASSES. Correct SM quantum numbers in the decomposition.
- N4: ACKNOWLEDGED but not resolved. Wilson argues massive fermions evade
  Distler-Garibaldi.
- N5: FAILS for mixing angles. M8.2 shows Yukawa texture is underdetermined.
  Wilson's angle derivation feeds in measured Cabibbo angle.

**Verdict:** The best available mechanism, but it does NOT explain WHY 3. It
explains: IF you assume Z_3, THEN the embedding is unique. The circularity is
real and acknowledged.

### Candidate 2: Triality of D_4 inside E_8

**What it is:** E_8 contains D_4 (= SO(8)) as a subalgebra. The Dynkin diagram
of D_4 has the unique property of S_3 (= symmetric group on 3 letters) as its
automorphism group. This S_3 permutes the three 8-dimensional representations:
vector 8_v, spinor 8_s, and cospinor 8_c. No other Dynkin diagram has an
automorphism group of order greater than 2.

**Assessment:**
- N1: PARTIALLY PASSES. S_3 acts on D_4 and has a Z_3 subgroup, but S_3 (order 6)
  is a larger structure. The 3 in "three 8-dimensional reps" is intrinsic to D_4.
  However, it is not intrinsic to E_8 -- D_4 is a subalgebra, and its triality
  does not extend to an E_8 automorphism. The outer automorphism group of E_8 is
  trivial (Aut(E_8)/Inn(E_8) = 1).
- N2: UNCLEAR. The number 3 in D_4 triality distinguishes 3 rep types, but
  whether these correspond to 3 GENERATIONS of fermions is a separate question.
  The 8_v, 8_s, 8_c are different representations, not three copies of the same one.
- N3: PROBLEMATIC. The three 8-dimensional reps of SO(8) are NOT three copies of
  a SM generation. A SM generation lives in the 16 of SO(10), not in 8-dimensional
  reps of SO(8). The connection would require a non-trivial chain of embeddings
  and branchings.
- N4: UNADDRESSED.
- N5: UNKNOWN but unlikely. Triality permutes reps; it does not directly produce
  rotation matrices.

**Verdict:** ANALOGY, not IDENTITY. D_4 triality is a beautiful mathematical
structure involving the number 3, but the connection to three generations of
fermions is loose. The three objects being permuted are three DIFFERENT
representations, not three copies of the SAME representation. This is a
fundamental mismatch. Structural fusion score: 35% (weak analogy).

### Candidate 3: The Exceptional Jordan Algebra J_3(O)

**What it is:** The exceptional Jordan algebra is the algebra of 3x3 Hermitian
matrices over the octonions O, with product A . B = (AB + BA)/2. Its
automorphism group is F_4 (dim 52). The "reduced structure group" (structure
group of the determinant form) is E_6 (dim 78). The Freudenthal construction
builds E_7 (dim 133) from J_3(O). And E_8 arises as the "magic square" endpoint.

The 3 in J_3(O) is the dimension of the matrices. This "3" is mathematically
deep: it connects to the three octonionic projective planes, to the three
division algebras in the Freudenthal-Tits magic square, and to the three roots
of the cubic norm form.

**Assessment:**
- N1: PARTIALLY PASSES. The "3" in J_3(O) is intrinsic -- it comes from the fact
  that J_n(O) only exists for n = 1, 2, 3 (Albert's theorem). There is no J_4(O).
  So the number 3 is FORCED by the algebraic structure. However, connecting this
  to "3 generations of fermions" requires a physical interpretation that is not
  established.
- N2: PASSES. Albert's theorem is sharp: n = 3 is the maximum. This distinguishes
  3 from all other integers.
- N3: PROBLEMATIC. The connection from J_3(O) to the Standard Model is not direct.
  The automorphism group F_4 does not contain the Standard Model gauge group.
  E_6 does (via E_6 -> SO(10) -> SM), but the 27-dimensional representation of E_6
  is the "matter" content in E_6 GUT models, and it naturally gives 1 generation,
  not 3. The 3 in J_3(O) refers to the matrix dimension, not to the number of
  copies of a generation.
- N4: UNADDRESSED. Different framework.
- N5: The cubic norm form on J_3(O) does produce invariant quantities. Whether
  these connect to mixing angles is completely unknown.

**Verdict:** The most tantalizing mathematical candidate for "why 3." Albert's
theorem gives a sharp reason why 3 is special in the context of exceptional
structures. But the physical connection -- from "3x3 octonionic matrices" to
"3 copies of a SM generation" -- has a structural gap. The J_3(O) "3" is a
matrix dimension; the generation "3" is a multiplicity. These are
categorically different kinds of "3." Structural fusion score: 45%
(analogy with potential).

### Candidate 4: E_8 Weyl Group Elements of Order 3

**What it is:** The Weyl group W(E_8) has order 696,729,600 = 2^14 x 3^5 x 5^2 x 7.
It contains elements of order 3. The number of such elements and their conjugacy
classes is a specific combinatorial fact about E_8.

**Assessment:**
- N1: The Weyl group of E_8 contains elements of many orders (1 through 30).
  Why single out order 3? Only because we are looking for 3. This is circular.
- N2: FAILS. Elements of order 2, 4, 5, 6, 7, etc. also exist. Nothing
  privileges order 3.
- N3-N5: NOT ASSESSED (candidate already fails).

**Verdict:** FALSE lead. The Weyl group contains elements of order 3 because
it is a large group. This is not special to E_8 and says nothing about
generations.

### Candidate 5: Rank 8 and the Decomposition 8 = 5 + 3

**What it is:** E_8 has rank 8. The Standard Model needs SU(5) (rank 4) or SO(10)
(rank 5) for the gauge group. The remaining rank (8 - 5 = 3) could correspond
to a family symmetry of rank 3 (i.e., SU(4) or SU(3) x U(1)).

**Assessment:**
- N1: PARTIALLY PASSES. The rank is intrinsic to E_8. The decomposition 8 = 5 + 3
  follows from requiring SO(10) as a subgroup. But rank 3 corresponds to SU(4),
  not SU(3). The number 3 is the rank, not the fundamental dimension. Dim(fund
  of SU(4)) = 4, not 3. To get 3 generations from SU(4), you need to break
  SU(4) -> SU(3) x U(1), and then dim(fund of SU(3)) = 3. This adds a step
  (and a choice).
- N2: WEAKLY PASSES. If you need SO(10) in E_8, the complementary rank is forced
  to be 3. But this does not uniquely select 3 generations -- it selects a
  family group of rank 3.
- N3-N5: NOT ASSESSED beyond the above.

**Verdict:** This is essentially the algebraic origin of SU(9)/Z_3: rank 8 =
rank 5 (SO(10)) + rank 3 (family). It provides a reason why the family group
has rank 3, but not why there are 3 generations rather than 4 (which SU(4)
would naturally give). The SU(9) route (Candidate 1) is the developed form
of this observation. Structural fusion score: 55% (essentially the same
argument as Candidate 1, rephrased).

### Candidate 6: The Root System E_8 and Its Sub-Root-Systems

**What it is:** The root system of E_8 has 240 roots. Various sub-root-systems
correspond to subalgebras. The longest chain of exceptional inclusions is
E_8 > E_7 > E_6. Both E_7 and E_6 appear naturally.

**Assessment:**
- N1: The chain E_8 > E_7 > E_6 has 3 exceptional groups, but this is not
  connected to generations in any known way.
- N2-N5: NOT ASSESSED (no mechanism proposed).

**Verdict:** COINCIDENCE. Three exceptional groups in the chain is a fact of
classification theory, not a generation mechanism.

### Candidate 7: The Leech Lattice and Vertex Operator Algebra

**What it is:** E_8 x E_8 appears in the heterotic string, where compactification
on a 6-dimensional Calabi-Yau manifold can produce 3 generations. The number 3
comes from the Euler characteristic of the Calabi-Yau: |chi|/2 = 3 for specific
manifolds.

**Assessment:**
- N1: PASSES in context. The Euler characteristic is a topological invariant of
  the compactification manifold, not put in by hand. Different manifolds give
  different generation counts.
- N2: FAILS as a UNIQUE mechanism. Many Calabi-Yau manifolds exist with
  |chi|/2 = 3, and many more exist with different values. No known selection
  principle picks |chi| = 6.
- N3: PASSES (by construction in heterotic string compactification).
- N4: PASSES (chirality from topology).
- N5: Mixing angles arise from geometry of the Calabi-Yau, but depend on
  moduli (free parameters).

**Verdict:** This is the most developed "explanation" of 3 generations in the
literature, but it requires string theory and a specific compactification.
It does not derive 3 from E_8 alone -- it derives 3 from E_8 PLUS a specific
6-manifold. The manifold introduces both the solution and the problem: why
THIS manifold? Structural fusion score: 60% (genuine mechanism, incomplete
selection principle).

---

## Section 3: The Octonion Question

**Does J_3(O) connect to generations?**

This is the deepest mathematical question in the investigation. Let me be precise
about what is known and what is not.

### What Is Known

1. **Albert's theorem (1934):** The only finite-dimensional formally real Jordan
   algebras that are simple and exceptional are J_3(O) (dim 27) and its split form
   J_3(O_s) (dim 27). The number 3 is the maximum matrix size: J_4(O) does not
   exist because the octonionic 4x4 case fails the Jordan identity due to
   non-associativity.

2. **Freudenthal-Tits magic square:** Systematically connects the four division
   algebras (R, C, H, O) and the four Jordan algebras (J_3(R), J_3(C), J_3(H),
   J_3(O)) to the five exceptional Lie groups (G_2, F_4, E_6, E_7, E_8).

3. **E_8 and J_3(O):** The Lie algebra e_8 arises in the magic square as
   Der(J_3(O)) + J_3(O)_0 + J_3(O)_0 + tri(O), where tri(O) is the triality
   algebra of O. More precisely, Vinberg's construction gives e_8 from J_3(O)
   and the split octonions. The 248-dimensional e_8 decomposes as
   248 = 52 (f_4) + 26 (J_3(O)_0) + 26 (J_3(O)_0) + 26 x ... -- the exact
   decomposition depends on the construction used.

4. **Gursey, Ramond, and Sikivie (1976):** Proposed E_6 as a GUT group, with
   matter in the 27 (= J_3(O)_0 + 1). Each 27 contains one generation. Three
   generations would require 27 + 27 + 27, which is NOT a single E_6 representation
   but three copies. E_6 does not explain why there are 3 copies.

5. **Dray and Manogue (2010-present):** Developed the octonionic description of
   one generation of fermions using 2x2 octonionic matrices (Cl(9,1) description).
   For three generations, they need 3 copies of their construction, which again
   puts 3 in by hand.

### The Key Structural Question

**Is the "3" in J_3(O) (matrix dimension) the SAME "3" as in "3 generations"?**

To make this precise: the 3 in J_3(O) indexes the rows/columns of the Jordan
algebra. A 3x3 Hermitian octonionic matrix has the form:

    [ a    z*   y  ]
    [ z    b    x* ]
    [ y*   x    c  ]

where a, b, c are real and x, y, z are octonionic. The "3" refers to the three
diagonal entries (a, b, c) and the three off-diagonal octonionic entries (x, y, z).

In the generation picture, "3 generations" means three copies of the same
representation: (e, nu_e), (mu, nu_mu), (tau, nu_tau). These are three IDENTICAL
OBJECTS distinguished by a label.

**These are different kinds of "3":**

- J_3(O): The 3 indexes components of a SINGLE algebraic object. The three
  diagonal entries are NOT copies of each other -- they are a, b, c with
  different positions.
- Generations: The 3 indexes copies of the SAME algebraic object. The three
  generations are copies of the same quantum numbers.

For the connection to work, one would need a mechanism where the 3 rows/columns
of J_3(O) become 3 IDENTICAL copies of something after a physical identification.
This is not impossible (the symmetry group of J_3(O) permutes the three diagonal
entries under certain conditions), but it is not established.

### The Specific Connection Attempt

The closest attempt is via E_6 -> SU(3) x SU(3) x SU(3). Under this maximal
subgroup decomposition:

    27 = (3,3,1) + (1,3,3) + (3,1,3)

If one SU(3) is identified as color, the other two could be generation and
electroweak structure. But this is a choice, not a derivation. And the 27
contains ONE generation's worth of states (including exotic ones), not three.

### Verdict on the Octonion Connection

**Classification: ANALOGY (45%), not IDENTITY.**

The "3" in J_3(O) and the "3" in "3 generations" are structurally different.
The former is a matrix dimension; the latter is a multiplicity. These could be
connected by a physical identification (the Freudenthal-Tits magic square does
connect algebraic structures in non-obvious ways), but no such identification
has been constructed.

Albert's theorem gives the sharpest reason why "3 is special" in the context of
exceptional mathematics: J_4(O) does not exist. This is a genuine mathematical
fact about the number 3, not circular. But the bridge from "J_4(O) doesn't
exist" to "nature has 3 generations" has not been built. The gap is a physical
interpretation, not a mathematical construction.

**The honest summary:** The octonion connection is the most mathematically
compelling candidate for "why 3," but it remains an analogy. The gap between
the mathematical "3" and the physical "3" is precisely identified: it is the
identification of J_3(O) matrix indices with generation labels. If anyone
constructs this identification rigorously, it would be a major result.
No one has.

---

## Section 4: Kill Condition Assessment

### KC-R1: No coherent mathematical structure connects discrete automorphisms to continuous rotation angles

**Status: PARTIALLY FIRES (severity: SERIOUS, not FATAL)**

Here is the honest assessment:

**Structures that connect discrete symmetries to continuous parameters DO exist
in mathematics.** They include:

1. **Representation theory of discrete groups:** Z_3 has three irreducible
   representations (trivial, omega, omega^2). The Clebsch-Gordan coefficients
   for Z_3 reps produce specific numerical factors. But these are rational
   numbers (1, omega, omega^2), not irrational mixing angles.

2. **Projection operators from discrete eigenspaces:** If V = V_1 + V_2 + V_3
   (eigenspace decomposition under Z_3), the change of basis from one
   decomposition to another produces a unitary matrix. This matrix has entries
   that are continuous parameters. BUT: the matrix depends on the choice of
   WHICH decomposition (Z_3 relative to WHAT), which introduces freedom.

3. **Discrete symmetry breaking to continuous angles:** In condensed matter,
   discrete crystal symmetries restrict but do not fix continuous order parameters.
   The rotation angles within a symmetry-allowed manifold are continuous.

**What does NOT exist (to my knowledge):**

A mechanism where a discrete symmetry of E_8 produces SPECIFIC numerical values
for mixing angles with zero free parameters and no physical input. Every known
construction either:
- (a) Feeds in measured values (Wilson's Cabibbo angle input)
- (b) Has free parameters from symmetry breaking (flavon VEV alignment)
- (c) Produces only rational multiples of pi (discrete group CG coefficients)

**Assessment:** KC-R1 does not fire in its FATAL form (coherent structures exist).
But it fires in a SERIOUS form: no known construction produces irrational mixing
angles from E_8 discrete symmetries alone. The question is not whether such
structures exist in abstract mathematics (they do), but whether they exist in
E_8 specifically and produce the correct numbers.

### KC-R2: All prior work on discrete symmetry -> mixing angles requires free parameters

**Status: TO BE ASSESSED IN ROUND 2.**

This requires a systematic literature survey of the entire discrete flavor
symmetry program (A_4, S_4, Delta(27), Delta(96), etc.). The polymathic
researcher should investigate whether ANY discrete symmetry model in the
literature produces ALL mixing parameters without free inputs.

**Preliminary assessment based on current knowledge:** No pure discrete symmetry
model achieves zero-parameter prediction of ALL mixing angles. The Altarelli-
Feruglio program (A_4 for PMNS) and the King-Luhn program (S_4, Delta(27))
all have at least some free parameters. The "golden ratio" prediction of
theta_12 from A_5 (Everett, Stuart 2009) is the closest to a zero-parameter
angle, but it is a single angle prediction, not the full mixing matrix.

---

## Section 5: Recommended Next Steps for Round 2

### For the Polymathic Researcher (Round 2 -- ARCHAEOLOGY)

The following questions require systematic literature investigation:

**Q1 (Critical): Has anyone connected J_3(O) matrix indices to generation labels?**
- Search: Dray, Manogue, Todorov, Dubois-Violette, Boyle, Farnsworth
- Key question: Is there a published identification where the "3" in J_3(O)
  becomes "3 generations" via a specific mathematical map?
- If YES: Read carefully and assess whether it introduces free parameters.
- If NO: This gap is precisely identified and characterizes the state of the field.

**Q2 (Important): What is the full landscape of "3" in E_8?**
- All ways the number 3 appears as a mathematical invariant of E_8 (not just
  "a subalgebra has a 3" but "a defining property of E_8 produces 3").
- Include: center of E_8 (trivial -- Z(E_8) = 1), pi_1 (fundamental group),
  Weyl group structure, root system invariants.
- E_8 lattice theta series coefficients, kissing numbers, etc.

**Q3 (Important): Zero-parameter discrete flavor models.**
- Has ANY discrete symmetry model achieved zero-parameter prediction of ALL
  CKM AND PMNS mixing parameters simultaneously?
- Search: "predictive flavor model" + "no free parameters" or "parameter-free"
- Include: A_4, S_4, Delta(27), Delta(96), A_5, PSL(2,7), Sigma(168)

**Q4 (Valuable): Boyle-Farnsworth spectral Standard Model.**
- Latham Boyle and Shane Farnsworth (2020+) have a program connecting
  noncommutative geometry to the Standard Model. Does their construction
  explain 3 generations?
- Also check: Connes-Chamseddine spectral action. Does it fix the generation
  number?

**Q5 (Valuable): Heterotic landscape statistics.**
- In the landscape of heterotic string compactifications, what fraction of
  Calabi-Yau manifolds give |chi| = 6 (i.e., 3 generations)?
- Is there a statistical or anthropic argument for 3?

---

## The Honest Verdict

### What the teleological analysis reveals

If the solution to "why 3 generations" EXISTS within E_8, it must have one of
two forms:

**Form A (Algebraic):** A property of E_8 that produces the integer 3 as an
output of a well-posed algebraic computation. The most credible candidate is
the connection to J_3(O) via Albert's theorem (n_max = 3 for exceptional
Jordan algebras). But the bridge from algebraic "3" to physical "3" has not
been built.

**Form B (Geometric):** A property of the E_8 root system or Lie group geometry
that distinguishes 3 copies of a representation. The most credible candidate
is the SU(9)/Z_3 embedding. But the Z_3 is assumed, not derived.

**What is NOT available:**

A mechanism where E_8 algebra ALONE -- without assuming Z_3, without choosing
a Calabi-Yau manifold, without specifying a flavon sector -- produces exactly
3 generations as a theorem. No such mechanism exists in the current mathematical
literature. This is not a gap in our search; it is a gap in the field.

### Why this matters for the project

The M8 experiment results (M8.1-M8.3b) tell a consistent story:

1. The SU(9)/Z_3 framework is algebraically correct [MV].
2. The Yukawa coupling is unique at leading order (Schur) [SP].
3. The texture is underdetermined (Outcome C) [CO].
4. Wilson's angle predictions are numerically striking but not derived from
   pure E_8 geometry [CO].

**The algebra gives you the stage. It does not write the play.** This verdict
from the prior Heptapod B analysis (2026-03-16) is confirmed and sharpened:
not only does E_8 not write the play, but no known mathematical structure
can be proved to write it. The "play" (specific mixing angles) requires
either physical input (Wilson's approach) or free parameters (flavon VEV
alignment).

### Confidence Calibration

| Claim | Confidence |
|-------|-----------|
| No known mechanism derives 3 from E_8 without assuming Z_3 | 92% |
| J_3(O) is the most compelling mathematical source of "3" | 80% |
| The J_3(O)-to-generations bridge has NOT been built | 88% |
| D_4 triality is an analogy, not a generation mechanism | 85% |
| KC-R1 partially fires (SERIOUS, not FATAL) | 78% |
| Zero-parameter discrete flavor models do not exist | 70% (needs Round 2 confirmation) |
| If the solution exists, it involves J_3(O) or a construction we haven't seen | 55% |
| The honest answer may be "3 is environmental, not algebraic" | 40% |

### What "environmental" means

The 40% probability assigned to "3 is environmental" deserves explanation. In
the string landscape, the number of generations depends on the compactification
manifold. Different manifolds give 0, 1, 2, 3, 4, ... generations. Nature has 3,
possibly because:
- (a) 3 is selected by some unknown dynamical principle (optimistic)
- (b) 3 is selected by anthropic reasoning (our universe is compatible with life
  only if N_gen >= 3, from asymptotic freedom of QCD requiring N_gen <= 8, and
  CP violation requiring N_gen >= 3) -- this gives 3 <= N_gen <= 8 with 3 as
  the minimum
- (c) We are in one pocket of a multiverse with no deeper explanation

None of these are satisfying. But the teleological analysis forces us to confront
the possibility that the number 3 is not derivable from E_8 algebra alone.

---

## Summary of Structural Fusion Verdicts

| Candidate | Connection to 3 | Fusion Score | Verdict |
|-----------|----------------|-------------|---------|
| SU(9)/Z_3 (Wilson) | Z_3 assumed as input | 55% | ANALOGY (begs the question) |
| D_4 triality | 3 rep types, not 3 copies | 35% | WEAK ANALOGY |
| J_3(O) / Albert | n_max = 3 (sharp) | 45% | ANALOGY (bridge unbuilt) |
| Weyl group order 3 | Exists but not special | 10% | COINCIDENCE |
| Rank 8 = 5 + 3 | Same as SU(9)/Z_3 | 55% | ANALOGY (reformulation) |
| Root system chains | E_8 > E_7 > E_6 | 15% | COINCIDENCE |
| Heterotic Calabi-Yau | chi/2 = 3 for specific CY | 60% | GENUINE but not E_8-intrinsic |

---

## Key Files for Round 2

- This vision: `research/council/e8-geometric-flavor/01-vision.md`
- M8 results: `src/experiments/results/su9_cg_coefficients.json`
- M8 results: `src/experiments/results/yukawa_texture_analysis.json`
- M8 results: `src/experiments/results/wilson_pmns_verification.json`
- Prior analysis: `research/heptapod-b-yukawa-vision.md`
- Friction catalog: `docs/PHYSICS_MATH_FRICTION_CATALOG.md`
- Generation analysis: `research/so14-generation-specialist/2026-03-16-e8-generation-analysis.md`
