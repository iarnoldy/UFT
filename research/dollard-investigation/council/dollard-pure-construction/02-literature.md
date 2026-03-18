# Round 2: ARCHAEOLOGY — Prior Work on Operational vs. Algebraic Content

**Agent**: Polymathic Researcher (cross-domain investigation)
**Date**: 2026-03-17
**Investigation**: dollard-pure-construction
**Prior round**: `research/council/dollard-pure-construction/01-vision.md`

---

## The Question

Has anyone distinguished operational/computational content from algebraic
classification? Specifically: does the choice of presentation (generators,
relations, construction order) carry mathematical content beyond the abstract
algebra itself?

## Search Domains

Based on Round 1's structural requirements, searched across:
1. Operational vs. denotational semantics (computer science)
2. Heaviside's operational calculus (mathematics/EE)
3. Presentations of algebras (abstract algebra)
4. Constructive mathematics (foundations)
5. Process algebras (concurrency theory)
6. Bridgman's operationalism (philosophy of physics)
7. MacFarlane's versor algebra (historical mathematics)
8. Mod-4 subseries decomposition (analysis)

---

## Findings by Domain

### 1. Operational vs. Denotational Semantics — IDENTITY (90%)

**The strongest parallel.** In computer science, the distinction between what a
program computes (denotational semantics) and HOW it computes (operational
semantics) is foundational and has been studied since the 1970s (Scott, Strachey,
Plotkin).

Key facts:
- **Denotational semantics** maps programs to mathematical objects (functions,
  domains). Two programs are equivalent if they denote the same object.
- **Operational semantics** describes step-by-step computation. Two programs
  are equivalent if they exhibit the same observable behavior (bisimulation).
- **These are NOT the same.** There exist programs that are denotationally
  equivalent but operationally distinguishable (they compute the same function
  but through different intermediate steps).
- **Full abstraction** is the property that denotational equivalence = operational
  equivalence. It is NOT automatic and proving it for real languages is a major
  research achievement.

**Structural-fusion verdict**: The Dollard question maps precisely:
- Denotational semantics = algebraic classification (what algebra IS it?)
- Operational semantics = construction path (what does each step DO?)
- The question "does operational content survive algebraic classification?"
  becomes "are there operationally distinguishable computations that are
  denotationally equivalent?"
- Answer from CS: YES, such computations exist in general. But for FINITE
  algebras over exact arithmetic, the answer is more subtle — the denotational
  semantics typically captures everything observable.

**Break point**: CS operational semantics deals with PROCESSES (potentially
infinite sequences of steps). Dollard's algebra is finite-dimensional. In
finite dimensions with exact arithmetic, there are no "infinite processes"
to distinguish operationally. The parallel holds for the STRUCTURE of the
question but may not hold for the ANSWER.

### 2. Heaviside's Operational Calculus — IDENTITY (85%)

**The most historically relevant parallel.** Dollard explicitly follows Heaviside
and names him as a predecessor. Heaviside's operational calculus treated the
differentiation operator p = d/dt as if it were a number — multiplying,
dividing, and taking functions of p.

Key facts:
- Heaviside's methods were NOT rigorously justified in his time (1880s-1890s).
  Pure mathematicians rejected them.
- Two rigorous justifications emerged:
  1. **Integral transform approach** (Bromwich 1920s, Carson, Doetsch): operational
     calculus = Laplace transform. The "algebra" is the transform domain.
  2. **Algebraic approach** (Mikusiński 1953): operational calculus = convolution
     quotient field. Differential operators become elements of a field
     constructed algebraically from continuous functions under convolution.
- Mikusiński's approach is EXACTLY the kind of "operational content becoming
  algebraic content" that this investigation asks about. He showed that
  Heaviside's operational rules, which looked like they were about processes
  (differentiation, integration), could be recast as ALGEBRAIC operations in
  a specific ring.

**Structural-fusion verdict**: Heaviside's situation is structurally identical
to Dollard's:
- Heaviside had operators (d/dt) that he manipulated as if they were numbers
- The manipulations worked even though the algebraic justification was missing
- Two paths of justification emerged: one killing the operational content
  (Laplace transform: just do the integral), one preserving it (Mikusiński:
  the operators ARE elements of a rigorously defined algebra)
- Dollard has operators (h, j, k) that he manipulates as if they were
  independent elements
- Our algebraic analysis killed them (h = -1, algebra = Z_4)
- The question is whether a Mikusiński-type justification exists that
  preserves the operational content

**Break point**: Heaviside's operators act on an INFINITE-dimensional function
space (solutions to ODEs). Dollard's operators act on a FINITE-dimensional
algebra. The Mikusiński construction works because the convolution ring of
continuous functions is an integral domain (no zero divisors). Dollard's
algebra is finite-dimensional and already classified. There may be no room
for a Mikusiński-type extension.

### 3. Presentations of Algebras — ANALOGY (70%)

**Well-studied but not quite the right fit.** In abstract algebra, a
"presentation" of a group or algebra is a set of generators and relations.
Different presentations can yield the same abstract group.

Key facts:
- The word problem for groups (given a presentation, determine if two words
  represent the same element) is UNDECIDABLE in general (Novikov 1955,
  Boone 1959).
- For FINITE groups/algebras, the word problem is decidable (enumerate all
  elements).
- Different presentations carry different COMPUTATIONAL complexity. Some
  presentations make certain computations easy, others hard.
- Groebner bases provide canonical forms for presentations of commutative
  algebras, resolving the choice-of-presentation question for that case.

**Structural-fusion verdict**: The parallel is real but limited:
- Dollard's presentation ({h, j, k} with specific relations) is a presentation
  of Z_4
- Different presentations of Z_4 exist ({i} with i^4 = 1, for example)
- Dollard's presentation carries information (which operations are "primitive")
  that the abstract group does not
- But for finite groups, this information is COMPUTATIONAL (affects speed of
  certain calculations) not MATHEMATICAL (does not change what is provable)

**Break point**: Presentations matter computationally for infinite groups
(undecidable word problem). For Z_4, the word problem is trivial regardless
of presentation. The presentation content is not mathematical but
computational/pedagogical.

### 4. Constructive Mathematics — ANALOGY (65%)

**The right philosophical framework but wrong mathematical domain.**
In constructive mathematics (Brouwer, Martin-Löf, HoTT), proofs carry
computational content. A constructive proof that x exists provides an
ALGORITHM for computing x, not just evidence that x exists.

Key facts:
- The Brouwer-Heyting-Kolmogorov interpretation: a proof of "A or B"
  must specify WHICH of A or B is true and provide a proof.
- Type theory (Martin-Löf, Lean 4): proofs are programs, propositions
  are types. The proof IS the computational content.
- In constructive math, two proofs of the same theorem can be
  DIFFERENT (they provide different algorithms). Classical math does
  not distinguish them.

**Structural-fusion verdict**: The analogy is illuminating:
- Dollard's construction of e^(h*delta) = e^(-delta) is like a constructive
  proof of "e^(-delta) exists." The proof says "start with e^delta, apply
  h (= reciprocation), get e^(-delta)."
- A different proof says "substitute delta → -delta in the Taylor series."
- Classically, these proofs are the same (same theorem). Constructively,
  they are different (different algorithms).
- Dollard's operational content is analogous to the constructive content
  of a proof.

**Break point**: Constructive content matters when you need to EXTRACT an
algorithm. For Dollard's finite algebra, there is no algorithm to extract —
the computation is just multiplication in Z_4. The constructive parallel
suggests Dollard's content is real but trivial in this case.

### 5. Process Algebras (CCS, CSP) — ANALOGY (55%)

**Relevant framework, limited applicability.**

Key facts:
- CCS (Milner), CSP (Hoare), ACP: formal languages for concurrent processes
- Key distinction: TRACE equivalence (same observable sequences) vs.
  BISIMULATION (same branching structure)
- Two processes can have the same traces (same denotation) but different
  branching (different operational behavior)
- This is EXACTLY the structure of the Dollard question at the abstract level

**Structural-fusion verdict**: The structure matches but the content does not.
Dollard's operators are not processes. They do not branch. They do not
communicate. The process algebra framework provides the right VOCABULARY
for the question (operational vs. denotational equivalence) but not the
right MATHEMATICS for the answer.

### 6. Bridgman's Operationalism — COINCIDENCE (30%)

**Philosophically suggestive, mathematically empty.**

Key facts:
- Bridgman (1927): concepts are defined by the operations used to measure them
- "Length" IS the set of operations by which length is determined
- For mental/mathematical concepts, the operations are mental operations
- Widely influential in psychology, less so in physics after 1950s

**Structural-fusion verdict**: Bridgman's operationalism is about PHYSICAL
concepts, not MATHEMATICAL structures. Dollard echoes Bridgman when he insists
that h, j, k are operators (defined by what they do) rather than numbers
(defined by what they are). But this is a philosophical position, not a
mathematical theorem. It cannot tell us whether h = -1 or h is independent.

### 7. MacFarlane's Versor Algebra — IDENTITY (95%)

**The historical source.** Dollard explicitly builds on MacFarlane.

Key facts:
- Alexander MacFarlane (1851-1913): introduced hyperbolic versors as an
  extension of Hamilton's quaternion versors
- MacFarlane used h^2 = +1 (hyperbolic imaginary) alongside i^2 = -1
  (circular imaginary) — exactly Dollard's h and j
- MacFarlane's work was connected to Cockle's tessarines (1848)
- MacFarlane's hyperbolic quaternions anticipated Minkowski space
- The modern mathematical framework: one-parameter groups (Lie theory)
  subsumes both versor and hyperbolic versor

**Structural-fusion verdict**: Dollard's versor algebra IS MacFarlane's
versor algebra, which IS a presentation of standard mathematical structures
(complex numbers, split-complex numbers, or tessarines depending on which
axioms you choose). MacFarlane's contribution was pedagogical and
historical, not algebraically novel. The "new math" Dollard claims to
need already existed in 1900.

**Critical observation**: MacFarlane kept h^2 = +1 as INDEPENDENT from -1.
He did not add the axiom jk = 1 that Dollard adds. MacFarlane's algebra
IS the tessarines (with h independent). Dollard's additional axiom jk = 1
collapses h to -1, destroying the structure MacFarlane built.

### 8. Mod-4 Subseries Decomposition — IDENTITY (99%)

**The quaternary expansion IS a well-known mathematical technique.**

Key facts:
- Given any power series sum a_n x^n, one can decompose it into q subseries
  based on the residue class of n modulo q
- For q = 4 and f(x) = e^x, this gives exactly Dollard's four subseries:
  u(x) = sum x^(4n)/(4n)!, x(t) = sum x^(4n+1)/(4n+1)!, etc.
- The identities u-v = cos, x-y = sin, u+v = cosh, x+y = sinh follow
  immediately from the roots-of-unity filter:
  u = (e^x + e^(ix) + e^(-x) + e^(-ix))/4, etc.
- This is standard analysis. It appears in treatments of the discrete
  Fourier transform applied to Taylor coefficients.
- The algebraic independence of such subseries has been studied
  (Nishioka et al., using the Lindemann-Weierstrass theorem).

**Structural-fusion verdict**: Dollard's quaternary expansion is a REDISCOVERY
of the standard mod-q subseries decomposition applied to e^x with q=4.
It is mathematically correct and non-trivial, but it is not new. The identities
Dollard presents follow from the roots-of-unity filter, which is a standard
technique in Fourier analysis.

The question of whether this decomposition has COMPUTATIONAL value beyond
what direct evaluation of e^x provides remains open. For lossy propagation
(where you need simultaneous circular and hyperbolic behavior), the
decomposition makes the coupled structure explicit. But the same information
is available by other means.

---

## Cross-Domain Synthesis

### The Pattern

Across all domains searched, the same pattern emerges:

1. **The distinction between operational and algebraic content IS recognized**
   in multiple fields (CS, constructive math, process algebra)
2. **The distinction IS mathematically substantive** for infinite/unbounded
   structures (infinite processes, infinite groups, infinite-dimensional
   function spaces)
3. **The distinction TRIVIALIZES** for finite structures with exact arithmetic
   (finite groups, finite-dimensional algebras)
4. **Dollard's algebra is finite** (4-dimensional, or really 2-dimensional
   since h = -1), placing it in the trivializing case

### The Mikusiński Exception

The one potential exception is the Mikusiński path: could Dollard's operators
be reinterpreted as elements of a LARGER algebraic structure (like Mikusiński
reinterpreted d/dt as an element of a convolution quotient field)? This would
require:
- An infinite-dimensional function space on which h, j, k act as operators
- A convolution or composition operation that gives this space a ring structure
- The demonstration that h, j, k are genuinely independent in this larger ring

This is essentially the "operator on function space" interpretation mentioned
in Round 1, item 2. The function space in question would be the space of
solutions to the telegraph equation (Dollard's primary application).

### Verdict on Prior Work

| Domain | Structural Fusion | Relevance |
|--------|------------------|-----------|
| Operational semantics (CS) | IDENTITY (90%) | Exactly the right question, but answer trivializes for finite case |
| Heaviside/Mikusiński | IDENTITY (85%) | Historical precedent; Mikusiński path is the best hope for residual content |
| Presentations of algebras | ANALOGY (70%) | Right framework, but finite groups kill the content |
| Constructive mathematics | ANALOGY (65%) | Right philosophy, wrong domain |
| Process algebras | ANALOGY (55%) | Right vocabulary, limited applicability |
| Bridgman operationalism | COINCIDENCE (30%) | Philosophy, not mathematics |
| MacFarlane versors | IDENTITY (95%) | Historical source; Dollard's axiom jk=1 destroys MacFarlane's structure |
| Mod-4 subseries | IDENTITY (99%) | Quaternary expansion is standard, not new |

---

## Concrete Leads for Round 3

1. **The Mikusiński path**: Does Dollard's h, j, k system have a
   Mikusiński-type justification where the operators act on solutions
   to the telegraph equation? If so, they might be independent in
   THAT larger structure even though h = -1 in the finite algebra.

2. **The presentation content**: Follow Dollard's construction step by step
   and identify exactly what PRESENTATIONAL content each step adds. Even
   if the algebra is Z_4, the presentation is not trivial.

3. **The mod-4 computational content**: Does the quaternary expansion
   provide computational advantages in lossy propagation analysis?
   This is an empirical question.

4. **The MacFarlane comparison**: Where exactly does Dollard's construction
   diverge from MacFarlane's? The jk = 1 axiom is the key. What motivated
   Dollard to add it, and what does it cost?

## Gaps Identified

1. **No prior work found** on the specific question of whether Dollard's
   versor algebra (with jk = 1) has content beyond Z_4. This is not
   surprising — the algebra is too small to attract mathematical interest.

2. **No prior work found** on applying Mikusiński-type construction to
   Dollard's operators specifically. The telegraph equation application
   exists in Heaviside's work but has not been connected to Dollard's
   notation.

3. **The quaternary expansion's computational value** for lossy propagation
   appears to be UNSTUDIED in the modern literature. It may have been
   known to Heaviside or Kennelly but lost.

---

## Warning Assessment

The charter says: "If NO prior work found in ANY adjacent field AND no
structural parallels, this is a SERIOUS warning."

**Assessment**: Prior work DOES exist in adjacent fields, and structural
parallels ARE strong. The warning does NOT fire. The prior work uniformly
suggests that operational content trivializes for finite algebras, which
is informative rather than fatal. Proceeding to Round 3.
