# Round 1: VISION — Is "Operational Content vs. Algebraic Structure" a Coherent Distinction?

**Agent**: Heptapod B Architect (teleological reasoning)
**Date**: 2026-03-17
**Investigation**: dollard-pure-construction
**Charter**: `research/council/dollard-pure-construction/00-charter.md`

---

## The Question

What does Dollard's mathematics imply when we follow his construction step-by-step
from epsilon, in HIS order of presentation, without mapping to any known algebra
until the final round? Specifically: is there a coherent distinction between
"operational content" (what mathematical objects DO) and "algebraic structure"
(what multiplication table they satisfy)?

## Prior Context

Two prior investigations killed Dollard's structure by projecting standard algebras
onto it:
1. **Z_4 analysis**: Proved h = -1 forced by axioms {j^2=-1, hj=k, jk=1}
2. **Tessarine hypothesis**: Three agents proposed tessarines; a fourth refuted
   with exhaustive SymPy verification

Both asked "what known algebra is this?" and force-fit. The question now is whether
this methodology killed genuine content that lives in operations rather than algebra.

---

## Step 1: Assume the Answer Exists

The answer exists. It says one of three things:

**(A)** There IS operational content in Dollard's construction that algebraic
classification misses. This content lives in the specific way he composes
exponentials, in the order of construction, in the physical interpretations
that constrain how symbols are used even when algebraically they collapse.

**(B)** There is NO such content. Algebraic classification fully captures everything.
Once h = -1 is established, every formula Dollard writes is a formula in
standard complex analysis with no residual meaning. The "operational" reading
is a psychological artifact, not a mathematical one.

**(C)** The distinction itself is incoherent. "Operational content" and "algebraic
structure" are not independent categories for finite-dimensional associative
algebras. Asking about one without the other is like asking about the shape
of a number.

I must determine which of (A), (B), or (C) is correct.

## Step 2: Characterize the Necessary Structure

### What would (A) require?

For operational content to survive algebraic collapse, there must exist at least
one of:

1. **A computation where the process matters, not just the result.** Example:
   computing e^(h*delta) step-by-step through the Taylor series produces
   intermediate objects (partial sums with h-coefficients) that have physical
   meaning even though the final sum equals e^(-delta). If these intermediates
   are physically accessible (e.g., truncated series in engineering practice),
   the operational content is real.

2. **A context where h acts differently from -1.** This would require leaving
   the algebra where h = -1 is forced — either by working in a larger algebra
   where the axiom jk=1 is relaxed, or by interpreting h as an operator on
   a function space rather than as an element of a number system.

3. **A notational discipline that prevents errors.** If treating h as an
   independent symbol (even though h = -1 algebraically) systematically
   prevents sign errors that practitioners make when using -1 directly,
   then the operational content is real in a *pragmatic* sense, even if not
   in a *mathematical* sense.

4. **The quaternary expansion having computational content beyond what
   standard exp(t) provides.** The four-subseries decomposition u, x, v, y
   of e^t is a verified identity. If this decomposition reveals structure
   in lossy propagation problems that direct computation of e^t does not
   readily expose, the content is real.

### What would (B) require?

For algebraic classification to be exhaustive:

1. Every formula Dollard writes, after substituting h = -1, must reduce to
   a standard formula in complex analysis.
2. The quaternary expansion must be derivable from standard Taylor series
   manipulation without invoking Dollard's operator framework.
3. No computation using Dollard's operators can produce a result that
   differs from the same computation using standard complex numbers.
4. The Fortescue/polyphase extension (Versor Algebra book, Ch. 2) must
   be standard DFT with no additional structure.

### What would (C) require?

For the distinction to be incoherent:

1. A theorem showing that for any finite-dimensional associative algebra A,
   knowing the multiplication table of A determines all "operational content"
   — i.e., there is no additional information in HOW computations are performed
   beyond WHAT the algebra is.
2. This theorem exists and is essentially trivial: an associative algebra IS
   its multiplication table (plus the vector space structure). There is no
   room for "extra content" because the multiplication table determines all
   products, and therefore all composite operations.

## Step 3: The Critical Analysis

### The distinction IS coherent — but only in specific senses

The naive form of (C) is wrong. Here is why:

**Fact 1: Presentations vs. algebras.** The same algebra can have many different
presentations (generators + relations). A presentation carries information
that the abstract algebra does not: it specifies which elements are "primitive"
and which are "derived." This is not algebraic content — it is *pedagogical*
or *computational* content. But it is real content.

Dollard's construction is a PRESENTATION of (a subalgebra of) the complex
numbers. The presentation says: start with epsilon, define h as the operator
that takes epsilon to its reciprocal, define j as the operator that rotates
by 90 degrees. This is a different presentation from "the complex numbers
are R[x]/(x^2+1)." The abstract algebra is the same. The presentation is not.

**Fact 2: Interpretations vs. structure.** An interpretation assigns physical
meaning to algebraic elements. The complex number z = R + jX can be
interpreted as an impedance (R = resistance, X = reactance). This
interpretation is not part of the algebra. It constrains how the algebra
is used. Dollard's h-operator carries an interpretation (reciprocation,
decay, counterspace) that constrains its use even though h = -1.

**Fact 3: Computational paths vs. results.** In exact arithmetic, all
computational paths through an algebra that reach the same result are
equivalent. But in approximate arithmetic (truncated series, numerical
computation, engineering practice), the PATH matters. Dollard's quaternary
expansion provides a specific decomposition path for e^t that exposes
circular-vs-hyperbolic structure at each partial sum. This path is not
"wrong" — it is a specific choice of computation that may or may not be
useful.

### Where the boundary lies

The operational/algebraic distinction is coherent in THREE specific senses:

1. **Presentation content**: which generators and relations are chosen
2. **Interpretive content**: which physical meanings are assigned to elements
3. **Computational path content**: which decomposition routes are followed

It is NOT coherent in the sense that "Dollard's algebra has different
multiplication rules from complex numbers." The algebra IS the complex
numbers (after h = -1). The multiplication table is fixed. No operational
reading changes 1 * 1 into something other than 1.

## Step 4: What Must the Investigation Contain?

A reconstruction of Dollard's construction on his own terms must:

1. **Follow his presentation order**: epsilon first, then h, then j, then k,
   then quaternary expansion, then polyphase.

2. **At each step, distinguish three layers**:
   - The ALGEBRAIC CONSEQUENCE (what the multiplication table forces)
   - The PRESENTATIONAL CONTENT (what this step adds to the generator/relation set)
   - The INTERPRETIVE CONTENT (what physical meaning Dollard assigns)

3. **Identify precisely where algebraic collapse happens**: the step where
   h = -1 becomes forced. Then ask: does the presentational or interpretive
   content survive this collapse?

4. **Test the quaternary expansion for computational content**: does the
   four-subseries decomposition of e^t reveal structure that standard
   Taylor series does not? This is a testable question.

5. **Test the polyphase extension**: Dollard's k^n_N = e^(j*2*pi*n/N) is
   standard roots of unity. But does his construction path (through versors
   rather than through abstract DFT) add anything?

## Step 5: Kill Conditions

### Kill Condition 1 (for the investigation as a whole)
If the distinction between operational content and algebraic structure is
incoherent IN ALL THREE SENSES (presentation, interpretation, computational
path), the investigation is over. **Assessment: this kill condition does NOT
fire.** The distinction is coherent in at least the presentation and
interpretation senses. Whether it is also coherent in the computational
path sense is an empirical question for Rounds 3-4.

### Kill Condition 2 (for finding genuine mathematical content)
If every piece of Dollard's operational content, once carefully stated,
turns out to be a well-known fact about complex analysis or Taylor series
presented in nonstandard notation, then the mathematical content is zero
and the value is purely pedagogical. This is a plausible outcome — it would
mean Dollard is a good teacher of standard material, not an inventor of
new mathematics. This is not a kill for the investigation (the answer
"purely pedagogical" is still an answer) but it is a kill for the hope
of finding new mathematical structure.

### Kill Condition 3 (for Round 3 specifically)
If the step-by-step reconstruction shows that h = -1 fires at the FIRST
step where h appears (before any operational content is built using h),
then there is no operational content that precedes the algebraic collapse.
The collapse is immediate and total.

## Step 6: Recommended Search Directions for Round 2

The Polymathic Researcher should investigate:

1. **Presentations of algebras as mathematical objects**: Does the choice of
   generators and relations carry content beyond the abstract algebra?
   Look at: combinatorial group theory, rewriting systems, Groebner bases,
   computational algebra. The concept of a "canonical form" vs. a
   "presentation" is well-studied.

2. **Operational semantics in computer science**: The distinction between
   denotational semantics (what a program computes = the algebra) and
   operational semantics (how it computes it = the presentation) is
   EXACTLY the distinction Dollard's question raises. This is a massive,
   well-developed field.

3. **Constructive mathematics**: In constructive math, HOW you prove
   something matters, not just THAT it is true. A constructive proof of
   e^(-delta) carries more information than a classical proof. Does
   Dollard's construction have constructive content?

4. **Process algebras (Milner, Hoare)**: Mathematical frameworks where the
   PROCESS of computation is a first-class object. CCS, CSP, pi-calculus.
   These formalize exactly the distinction between "what is computed" and
   "how it is computed."

5. **Physicist's operational definitions**: Bridgman's operationalism,
   which says physical quantities ARE the operations used to measure them.
   This is directly relevant to Dollard's insistence that h, j, k are
   operators (things that DO something) rather than numbers.

6. **Heaviside's operational calculus**: Dollard explicitly follows Heaviside.
   Heaviside's operational calculus was NOT abstract algebra — it was a
   system of rules for manipulating operators (d/dt) as if they were
   numbers. The rules worked even though they were not rigorously justified
   until distribution theory (Schwartz, 1940s). Is Dollard doing the same
   thing?

## Step 7: The Vision (Seen from the End)

The answer, seen from the end, has this structure:

**Dollard's construction is a specific PRESENTATION of a known algebra
(essentially the complex numbers, or C[Z_4]) equipped with a specific
INTERPRETATION (electrical engineering) and a specific COMPUTATIONAL
DECOMPOSITION (the quaternary expansion).** The algebra is not new. The
presentation carries non-trivial content in three areas:

1. The quaternary expansion of e^t into four subseries is a genuine
   mathematical identity with potential computational applications in
   lossy propagation analysis. It is not new mathematics (it follows from
   standard Taylor series) but it is a non-obvious decomposition.

2. The insistence on h as a distinct operator from -1, even though h = -1
   algebraically, provides a bookkeeping discipline analogous to dimensional
   analysis: it prevents certain classes of sign errors by maintaining
   the distinction between "negation" and "reciprocation in the exponent."

3. The polyphase extension to N-phase systems via k^n_N is standard
   Fortescue/DFT but presented through a construction path (versors)
   that makes the connection to physical rotation explicit.

**The investigation will conclude that there is genuine COMPUTATIONAL CONTENT
in the quaternary expansion (a useful decomposition), genuine PEDAGOGICAL
CONTENT in the operator presentation (a useful discipline), but NO NEW
ALGEBRAIC CONTENT (the algebra is Z_4 or equivalently the complex numbers
restricted to fourth roots of unity).** The operational content is real but
lives in the presentation and interpretation layers, not in the algebra layer.

This is not a kill. It is a substantive answer. The value of Dollard's work
is in his presentation and decomposition, not in his algebra.

---

## Structural Requirements for Subsequent Rounds

1. Round 2 must find prior work on presentation content vs. algebraic content.
   The key domains are operational semantics, constructive mathematics, and
   Heaviside's operational calculus.

2. Round 3 must follow Dollard's construction step-by-step and mark exactly
   where h = -1 fires, and what operational content (if any) was built before
   that collapse.

3. Round 4 must computationally test whether the quaternary expansion
   reveals structure in lossy propagation that standard exp(t) does not,
   and whether epsilon-as-operator ever produces different NUMERICAL results
   from e-as-number.

4. Round 5 must synthesize all findings into a verdict on the precise nature
   and extent of Dollard's mathematical contribution.

## Confidence Calibration

| Component | Confidence | Basis |
|-----------|-----------|-------|
| Distinction is coherent (not killed) | 95% | Standard math: presentations != algebras |
| Algebra is Z_4 / complex numbers | 99% | Lean-verified, SymPy-verified |
| Quaternary expansion has computational value | 50% | Genuinely open question |
| No new algebraic content | 90% | Would require non-associative structure |
| Pedagogical value is real | 70% | Depends on engineering practice analysis |
| Heaviside connection is substantive | 60% | Needs Round 2 research |
