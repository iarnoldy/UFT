# Round 5: SYNTHESIS — Dollard's Construction Seen from the End

**Agent**: Heptapod B Architect (teleological synthesis)
**Date**: 2026-03-17
**Investigation**: dollard-pure-construction
**Prior rounds**: All four (`01-vision.md` through `04-computation.md`)

---

## What the Evidence Shows

### Round 1 (VISION) asked: Is operational vs. algebraic content a coherent distinction?

**Answer**: Yes, in three senses: presentation content, interpretive content,
and computational path content. These are real categories recognized in
computer science (operational vs. denotational semantics), philosophy of
science (Bridgman's operationalism), and mathematics (presentations of
algebras). But the distinction TRIVIALIZES for finite-dimensional algebras
over exact arithmetic.

### Round 2 (ARCHAEOLOGY) asked: Has anyone studied this distinction before?

**Answer**: Yes, extensively. The six most relevant frameworks are:
1. **Operational/denotational semantics** (CS): exactly the right question,
   but the answer trivializes for finite structures
2. **Heaviside/Mikusiński operational calculus**: the historical precedent;
   Mikusiński showed operators CAN be given rigorous algebraic meaning, but
   only when they act on infinite-dimensional function spaces
3. **MacFarlane's versor algebra**: the historical source; Dollard's jk = 1
   axiom destroys what MacFarlane built (independent h with h^2 = +1)
4. **Mod-4 subseries decomposition**: the quaternary expansion is standard
5. **Constructive mathematics**: the right philosophy but wrong domain
6. **Presentations of algebras**: the right framework but trivializes for Z_4

### Round 3 (RIGOR) asked: What does step-by-step reconstruction reveal?

**Answer**: The algebraic collapse h = -1 is INSTANTANEOUS. Dollard himself
writes h = -1 in the same equation where he introduces h (Versor Algebra,
eq. 18). There is no intermediate state where h is independent. Every
subsequent step (hyperbolic functions, j introduction, k definition,
quaternary expansion, polyphase) is standard complex analysis or standard
Fourier analysis. The jk = 1 "axiom" is a CONSEQUENCE of h = -1 and k = hj,
not an independent assertion.

### Round 4 (COMPUTATION) asked: Do the numbers confirm?

**Answer**: Yes. Four tests, all confirming:
1. epsilon^(h*delta) = e^(-delta) exactly
2. Quaternary expansion = linear rearrangement of standard functions
3. h*f(x) = -f(x) for all tested functions (56/56)
4. Standard complex multiplication is correct; Dollard's versor form is wrong

---

## The Revised Vision

In Round 1, I predicted three possible answers:

**(A)** Operational content survives algebraic collapse
**(B)** No such content exists — algebraic classification is exhaustive
**(C)** The distinction is incoherent

The evidence decisively supports **a refined version of (B)**:

**The algebraic classification IS exhaustive for the MATHEMATICAL content.
But genuine PEDAGOGICAL and INTERPRETIVE content exists in Dollard's
presentation.** The content is real, but it is not mathematical.

Specifically:

### What Dollard Got RIGHT (Confirmed by Investigation)

1. **The quaternary expansion is a valid mathematical identity.** The four
   subseries u, x, v, y exist, satisfy the stated identities, and provide
   a unified view of circular-hyperbolic functions. This is correct mathematics.
   It is also KNOWN mathematics (mod-4 subseries decomposition, roots-of-unity
   filter).

2. **The distinction e^(h*delta) vs h*e^(delta) is real.** These are different
   operations (e^(-delta) vs -e^(delta)). Dollard's insistence on tracking
   WHERE h appears (exponent vs multiplier) prevents a genuine class of
   sign errors.

3. **Action Q = Psi * Phi is primary; W = dQ/dt.** This IS standard
   Hamilton-Jacobi theory and is a correct perspective on electrical
   quantities.

4. **The polyphase extension via versors (k^n_N) is correct.** This IS
   standard Fortescue/DFT, presented through a construction path that
   makes physical rotation explicit.

### What Dollard Got WRONG (Confirmed by Investigation)

1. **The versor form ZY = h(XB+RG) + j(XG-RB) is wrong.** The real power
   (RG+XB) appears in the 1-component, not the h-component. This is wrong
   in every algebra tested, because Z and Y live in the {1,j} subspace.

2. **The claim that jk = 1 is an independent axiom.** It is a consequence
   of h = -1 and k = hj. The three axioms {j^2=-1, hj=k, jk=1} are
   redundant — any two imply the third plus h = -1.

3. **The claim that h, j, k are four independent operators.** There are
   only two independent elements: 1 and j. The "four operators" {1, h, j, k}
   are {1, -1, j, -j} = Z_4.

4. **The claim that an "entirely new form of mathematics" is required.**
   The mathematics Dollard develops is standard complex analysis and
   standard Fourier analysis, presented with non-standard notation.

### What WE Got RIGHT (in prior investigations, confirmed here)

1. h = -1 forced by axioms (Lean-verified, SymPy-verified, now council-verified)
2. Algebra = Z_4 (confirmed from three independent directions)
3. Versor form disproved (confirmed with 7 test cases)
4. Quaternary expansion mathematically correct (confirmed with 9 test points)

### What WE Got WRONG (corrected here)

Nothing factually. But our FRAMING was incomplete:

**Previous investigations asked "what algebra is this?" and stopped when the
answer was Z_4.** This investigation shows that Z_4 is the complete answer
to the ALGEBRAIC question, but not the complete assessment of Dollard's
CONTRIBUTION. His contribution is:

1. A pedagogically effective presentation of complex analysis for EE
2. A bookkeeping discipline that tracks sign origins
3. An explicit connection between Taylor series decomposition and
   circular-hyperbolic duality
4. A construction path from epsilon through operators to polyphase theory
   that makes physical meaning visible at every step

These are real contributions. They are not algebraic contributions.

---

## Comparison to Known Algebras (Deferred to This Round)

Now, with all evidence in hand, the comparison:

| Structure | Match? | Evidence |
|-----------|--------|---------|
| **Z_4 = {1, i, -1, -i}** | **IDENTITY** | h=-1, j=i, k=-i. Cayley table matches. Lean-proved. |
| Complex numbers C | CONTAINS | Z_4 is the group of 4th roots of unity in C |
| Tessarines (Cockle, 1848) | NO | Tessarines have independent h, jk = -h. Dollard's jk = 1 breaks this. |
| Split-complex numbers | NO | Split-complex have independent h. Dollard's h = -1. |
| Quaternions | NO | Quaternions are non-commutative. Z_4 is commutative. |
| MacFarlane's hyperbolic versors | DEGENERACY | MacFarlane has independent h. Dollard's jk=1 collapses to Z_4 — a degenerate case. |
| Clifford algebra Cl(1,1) | NO | Cl(1,1) = tessarines. Same as tessarine case. |
| Heaviside operational calculus | ANALOGY (85%) | Same structure (operators as numbers) but Heaviside's operators act on infinite-dim function spaces. Dollard's are scalars. |
| Standard EE complex analysis | IDENTITY | After h=-1, Dollard's entire system IS standard Steinmetz phasor analysis. |

**Final algebraic verdict**: Dollard's versor algebra, taken on its own terms
and following his own construction, IS Z_4 equipped with a specific
presentation and physical interpretation. It is not a new algebra.

---

## Should This Line of Investigation Continue?

**No.** The investigation has reached a definitive conclusion. Further
investigation of Dollard's algebraic claims would be redundant — the algebra
is Z_4, and this has been proved from multiple independent directions (Lean,
SymPy, council analysis, computation).

The investigation SHOULD continue only if:
1. Someone proposes a SPECIFIC mechanism by which Dollard's operators could
   act on a larger space (the Mikusiński path), with a concrete proposal
   for what that space is. No such proposal currently exists.
2. The quaternary expansion is tested for practical computational advantages
   in a SPECIFIC lossy propagation problem. This would be an engineering
   evaluation, not a mathematical investigation.

Neither of these is likely to change the algebraic verdict.

---

## What Was Learned (Positive Results from a Negative Investigation)

1. **The operational/algebraic distinction is real but trivializes for finite
   algebras.** This is a genuine insight with broad applicability: when
   evaluating alternative mathematical systems, the question "what algebra
   is this?" is necessary and sufficient for finite-dimensional cases.
   Operational content can add pedagogical value but not mathematical value.

2. **Dollard's construction is a case study in how presentation can obscure
   algebraic simplicity.** The four-operator system {1, h, j, k} LOOKS
   four-dimensional but IS two-dimensional (complex numbers). The
   construction path through epsilon, h, j, k, quaternary expansion makes
   this non-obvious. This is valuable for understanding how non-standard
   notation creates the appearance of new mathematics.

3. **MacFarlane's independent h was the road not taken.** If Dollard had
   followed MacFarlane and kept h independent of -1, he would have had the
   tessarines — a genuinely 4-dimensional algebra with richer structure.
   But then jk = 1 would fail, and his "cancellation of contrary operations"
   interpretation would break. The mathematical and physical interpretations
   were in tension, and Dollard chose the physical interpretation.

4. **The quaternary expansion is worth knowing about.** It IS standard
   mathematics (mod-4 subseries), but it IS a non-obvious decomposition
   that unifies circular and hyperbolic functions. Whether it has practical
   applications remains untested but plausible.

5. **Kill conditions work.** This investigation demonstrates that
   pre-registered kill conditions can evaluate a speculative research
   direction without rationalization. The algebra IS Z_4. The computation
   confirms the analysis. The verdict is clear.

---

## Confidence Assessment

| Claim | Confidence | Basis |
|-------|-----------|-------|
| Dollard's algebra is Z_4 | 99.9% | Lean proof + SymPy + 3 council rounds |
| No new algebraic content | 99% | Step-by-step reconstruction + computation |
| Quaternary expansion is standard | 99% | Verified as mod-4 subseries + standard inverse formulas |
| Genuine pedagogical value exists | 80% | Would need EE practitioners to evaluate |
| Versor form ZY is wrong | 100% | 7/7 test cases, all wrong sign |
| Investigation is complete | 95% | Only the Mikusiński path and practical quaternary applications remain untested |
