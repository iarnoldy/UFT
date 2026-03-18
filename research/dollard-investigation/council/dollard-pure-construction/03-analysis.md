# Round 3: RIGOR — Step-by-Step Reconstruction of Dollard's Construction

**Agent**: Dollard Theorist (mathematical rigor)
**Date**: 2026-03-17
**Investigation**: dollard-pure-construction
**Prior rounds**: `01-vision.md` (structural requirements), `02-literature.md` (prior work)
**Source materials**: `02_versoralgebra.pdf` (primary), `01_fourquadbook.pdf` (supplementary)

---

## Methodology

Follow Dollard's construction in the exact order he presents it in
"Versor Algebra as Applied to Polyphase Power Systems" (2015), Chapter One.
At each step, record three layers:
- **ALGEBRAIC**: What the mathematics forces
- **PRESENTATIONAL**: What this step adds to the construction
- **INTERPRETIVE**: What physical meaning Dollard assigns

Do NOT compare to named algebras. Mark the exact point where h = -1 fires.

---

## Step-by-Step Reconstruction

### Step 1: The Log Base Epsilon (Sections [2]-[3], pp. 10-15)

**Dollard's content**: Epsilon (= e = 2.718...) is introduced as the Napierian
log base, defined via the limit (1 + 1/n)^n as n -> infinity, and via the
infinite series 1/0! + 1/1! + 1/2! + ... (eq. 7).

**ALGEBRAIC**: This is the standard definition of the number e. No freedom here.
e is a specific real number. There is no operator content — epsilon IS e.

**PRESENTATIONAL**: Dollard frames epsilon as a "geometric ratio" — a
dimensionless number that describes the natural rate of change. He emphasizes
that d/dt(e^t) = e^t — the function that is its own derivative.

**INTERPRETIVE**: Dollard gives epsilon a physical meaning: it is the natural
rate of electrical variation. One Neper = one unit decrement from 100% to
36.8% (= 1/e). This is standard EE (the RC time constant).

**Operational content at this step**: NONE beyond standard calculus.
Epsilon = e = 2.718... is a number, not an operator. The presentation
is pedagogically clear but mathematically standard.

### Step 2: Powers of Epsilon (Section [4], pp. 16-17)

**Dollard's content**: e^1 = 2.718, e^2 = 7.389 (growth). e^(-1) = 0.368,
e^(-2) = 0.135 (decay). The Taylor series for e^n is given with general
exponent: e^n = sum n^k/k! (eqs. 14-17).

**ALGEBRAIC**: Standard. e^n for real n is a real number. The series is the
standard exponential Taylor series.

**PRESENTATIONAL**: Dollard treats positive powers as "growth" and negative
powers as "decay." He frames this as a duality: growth vs. decay =
positive vs. negative exponent.

**INTERPRETIVE**: Positive power = runaway growth (seldom in practice).
Negative power = charge/discharge (common: capacitor discharging through
conductance). The physical application: phi = e^(-n) * phi_0 where
n = C/G (eq. 23).

**Operational content at this step**: NONE beyond standard calculus.
The growth/decay duality is standard (e^t vs e^(-t)).

### Step 3: Introduction of h — The DC Imaginary (Section [5], pp. 18-22)

**THIS IS THE CRITICAL STEP.**

**Dollard's content**: Dollard introduces h as the "DC operator" — the
"imaginary" corresponding to negative numbers.

His definition (eq. 18):
- h^n = +1^(1/2) — the square root of positive one
- h^2 = +1
- h = -1
- h^1 = -1

Then immediately (eq. 20): epsilon^h = epsilon^(-1) = 1/epsilon.

**ALGEBRAIC**: Dollard defines h as the square root of +1 and then IMMEDIATELY
identifies it with -1. This is not an implicit consequence discovered
later — it is his DEFINITION. In equation (18), he writes h = -1 explicitly.

**The collapse is INSTANTANEOUS.** There is no step where h exists as an
independent element before being identified with -1. Dollard himself
performs the identification in the same equation where he introduces h.

**PRESENTATIONAL**: Despite h = -1, Dollard continues to USE the symbol h
rather than -1. He writes epsilon^h rather than epsilon^(-1). He writes
h^0 = 1, h^1 = h, h^2 = 1, h^3 = h, ... (the sequence 1, h, 1, h, ...
which is 1, -1, 1, -1, ... once h = -1 is substituted). See equation (33).

**The presentational content is a BOOKKEEPING CONVENTION**: h labels "the
operation of negation" even though h IS the number -1. Writing epsilon^h
rather than epsilon^(-1) preserves the ORIGIN of the negative sign (it
came from "reversal" rather than from "subtraction").

**INTERPRETIVE**: h represents "reciprocation" or "arithmetic reversal."
Physically: h converts growth to decay. epsilon^(h*delta) = epsilon^(-delta)
= decay. The Neper rate. The physical distinction between "I negated the
exponent" and "I multiplied the result by -1" is real in EE: these
correspond to different physical operations (time-reversal of the process
vs. phase inversion of the signal).

**Key observation (eq. 37)**: When Dollard writes the Taylor series of
epsilon^h, he gets:
epsilon^h = 1/0! + h/1! + 1/2! + h/3! + 1/4! + h/5! + ...

The coefficients alternate between 1 (real) and h (imaginary). He then
separates into even/odd terms (eq. 39-40):
epsilon^h = (1/0! + 1/2! + 1/4! + ...) + h*(1/1! + 1/3! + 1/5! + ...)
          = cosh(1) + h*sinh(1)
          = cosh(1) - sinh(1)    [since h = -1]
          = e^(-1)

**This is the mod-2 subseries decomposition of e^t** evaluated at t = 1.
It is standard.

**Operational content at this step**: The ONLY operational content is the
bookkeeping convention of writing h instead of -1. This is genuinely
useful in engineering contexts (it tracks the REASON for a sign) but it
is not mathematical content. The algebra collapsed before any structure
was built.

### Step 4: Hyperbolic Functions (Section [6], pp. 23-31)

**Dollard's content**: From epsilon^h, Dollard derives cosh and sinh:
- alpha = even terms of Taylor series = cosh(delta) (eq. 55)
- beta = odd terms = sinh(delta) (eq. 55)
- epsilon^(+delta) = cosh(delta) + sinh(delta) (eq. 56)
- epsilon^(-delta) = cosh(delta) - sinh(delta) (eq. 57)
- Constraint: alpha^2 - beta^2 = 1 (eq. 47) [= cosh^2 - sinh^2 = 1]

**ALGEBRAIC**: Entirely standard. These are the definitions of cosh and sinh
via the exponential function. The identity cosh^2 - sinh^2 = 1 is
a standard hyperbolic identity.

**PRESENTATIONAL**: Dollard derives cosh and sinh FROM the mod-2 decomposition
of the exponential series, rather than defining them directly. This is a
valid pedagogical choice.

**INTERPRETIVE**: The even terms (cosh) are "real" and the odd terms (sinh) are
"imaginary" (= prefixed by h). This is standard: the even part of a function
f is (f(x)+f(-x))/2 = cosh when f = exp.

**Operational content at this step**: NONE. Standard cosh/sinh.

### Step 5: Introduction of j — The AC Imaginary (Section [7], pp. 32-35)

**Dollard's content**: j is introduced as the "quaternary operator" — the
square root of -1. His definition (eq. 61):
- j = sqrt(-1)
- j^n = (-1)^(1/2)
- j^1 = +j, j^3 = -j
- j^0 = +1, j^2 = -1

Then j^4 = j^0 = +1 (eq. 64). The sequence of powers is:
+1, +j, -1, -j, +1, +j, ... (eq. 70).

**ALGEBRAIC**: j = i (the standard imaginary unit). j^2 = -1 = h (eq. 64).
The powers of j cycle with period 4.

**PRESENTATIONAL**: Dollard presents j as a "fourth order" operator, in contrast
to h which is "second order" (period 2). The sequence +1, +j, -1, -j is
the group Z_4 = {1, i, -1, -i}. Dollard calls this the "quaternary" form
vs. the "duo-binary" (bipolar) form.

**INTERPRETIVE**: j represents rotation by 90 degrees. Physically: j converts
between real and reactive components. Epsilon^(j*theta) = cos(theta) +
j*sin(theta). This is Euler's formula — standard.

**Operational content at this step**: NONE beyond standard complex analysis.

### Step 6: Introduction of k and the axiom jk = 1 (Section [8], p. 33)

**Dollard's content**: k is defined as the "contrary rotation" operator:
- j^3 = -j = hj = k (eq. 65)
- jk = +1 (eq. 66) — "cancellation of the contrary operations"

**ALGEBRAIC**: Since k = hj = (-1)(j) = -j, and j(-j) = -j^2 = -(-1) = 1,
we get jk = 1. This is consistent.

But notice: k is NOT a new element. k = -j. It is already in Z_4.
The "four operators" {1, h, j, k} are {1, -1, j, -j} = Z_4.

**PRESENTATIONAL**: Dollard treats k as a separate entity from -j, giving it
the name "counter-rotation." The axiom jk = 1 is presented as a physical
fact (counter-rotations cancel) rather than as an algebraic consequence
of k = -j.

**INTERPRETIVE**: k represents rotation opposite to j. When j and k are
combined, they cancel to unity. Physically: positive and negative sequence
currents in a motor produce opposing torques.

**The jk = 1 axiom is NOT an independent axiom** — it is a CONSEQUENCE of
k = hj and h = -1. Specifically:
- k = hj = (-1)j = -j
- jk = j(-j) = -j^2 = -(-1) = 1

It LOOKS like an axiom but it is a theorem. When we proved in Lean that
jk = 1 forces h = -1, we were proving the CONVERSE: if you START from
jk = 1 and hj = k, you can DERIVE h = -1. Both directions work because
the statements are equivalent.

**Operational content at this step**: NONE. k = -j is not a new operator.

### Step 7: The Quaternary Expansion (Section [7] continued, following from
the j-power Taylor series, pp. 34-35)

**Dollard's content**: The Taylor series of epsilon^j is:
epsilon^j = 1/0! + j/1! - 1/2! - j/3! + 1/4! + j/5! - ... (eq. 69)

The coefficient sequence is +1, +j, -1, -j, +1, +j, ... (eq. 70).
This is the mod-4 version of the same decomposition.

The full quaternary expansion of epsilon^t (developed later in the book)
decomposes into FOUR subseries:
- u = sum t^(4n)/(4n)!     [terms where power is 0 mod 4]
- x = sum t^(4n+1)/(4n+1)! [terms where power is 1 mod 4]
- v = sum t^(4n+2)/(4n+2)! [terms where power is 2 mod 4]
- y = sum t^(4n+3)/(4n+3)! [terms where power is 3 mod 4]

With the identities:
- u - v = cos(t), u + v = cosh(t)
- x - y = sin(t), x + y = sinh(t)

**ALGEBRAIC**: This is the standard mod-4 subseries decomposition. The identities
follow from the roots-of-unity filter:
u(t) = (e^t + e^(it) + e^(-t) + e^(-it))/4
x(t) = (e^t + i*e^(it) - e^(-t) - i*e^(-it))/(4i) * i  [etc.]

Actually, more precisely:
u = (e^t + e^(jt) + e^(-t) + e^(-jt))/4 = (cosh(t) + cos(t))/2
x = (e^t + j*e^(jt) - e^(-t) - j*e^(-jt))/(4) [needs careful treatment]

But the point is: this is standard Fourier analysis applied to the Taylor
coefficients.

**PRESENTATIONAL**: This is where Dollard's construction adds its most
distinctive content. The quaternary expansion is a REAL mathematical identity
that simultaneously exposes both circular (cos, sin) and hyperbolic (cosh, sinh)
structure in a single framework. Most treatments of the exponential derive
EITHER the circular functions (from e^(jt)) OR the hyperbolic functions
(from e^(ht) = e^(-t)). Dollard's quaternary expansion does BOTH SIMULTANEOUSLY
from a single series decomposition.

**INTERPRETIVE**: The four subseries correspond to four physical quadrants:
energy storage (u), energy transfer (x), energy return (v), energy loss (y).
In a lossy transmission line, all four are present simultaneously.

**Operational content at this step**: THIS is where genuine computational content
exists. The quaternary expansion is not new mathematics, but it IS a non-obvious
decomposition that makes explicit the coupled circular-hyperbolic structure of
lossy propagation. Whether this has practical computational value is an
empirical question for Round 4.

### Step 8: The Polyphase Extension (Chapter Two)

**Dollard's content**: The versor operator for N-phase systems is:
k^n_N = e^(j*2*pi*n/N) — the Nth roots of unity (eq. in Ch. 2).

This is Fortescue's method of symmetrical components (1918).

**ALGEBRAIC**: Standard DFT. The Nth roots of unity form the cyclic group Z_N.
Fortescue's method is the DFT applied to polyphase systems.

**PRESENTATIONAL**: Dollard arrives at the DFT through his versor construction
(rotation operators) rather than through abstract Fourier analysis. This
makes the physical meaning (rotating fields) explicit.

**INTERPRETIVE**: Each root of unity corresponds to a "sequence" (positive,
negative, zero for 3-phase). The physical meaning is well-established
in power systems engineering.

**Operational content at this step**: NONE beyond standard Fortescue/DFT.

---

## Summary: Where Does the Collapse Happen?

| Step | Content | h = -1 status | Operational content |
|------|---------|---------------|-------------------|
| 1. Epsilon definition | e = 2.718 | Not yet introduced | None |
| 2. Powers of epsilon | e^n, e^(-n) | Not yet introduced | None |
| 3. **h introduced** | **h defined as -1** | **IMMEDIATE** | Bookkeeping convention only |
| 4. Hyperbolic functions | cosh, sinh | Already collapsed | None (standard) |
| 5. j introduced | j = sqrt(-1) | Already collapsed | None (standard) |
| 6. k = hj, jk = 1 | k = -j (consequence) | Already collapsed | None (k is redundant) |
| 7. Quaternary expansion | mod-4 decomposition | Already collapsed | **YES** — non-obvious decomposition |
| 8. Polyphase extension | Roots of unity / DFT | Already collapsed | None (standard Fortescue) |

**The collapse is instantaneous.** Dollard introduces h and identifies it with -1
in the SAME equation (eq. 18, p. 18 of Versor Algebra). There is no intermediate
state where h is independent. There is no construction built using h-as-independent
that is later killed. h IS -1 from the moment it appears.

---

## Analysis of Each Lead from Round 2

### Lead 1: The Mikusiński Path

Does Dollard's h, j, k system have a Mikusiński-type justification where the
operators act on solutions to the telegraph equation?

**Analysis**: No. Mikusiński's construction works because the differentiation
operator d/dt is NOT a number — it is a genuine operator on an
infinite-dimensional function space. You can build a quotient field because
the convolution ring has no zero divisors.

Dollard's h IS a number (-1). It does not act on a function space in any way
different from multiplication by -1. The Mikusiński path requires h to be an
operator on functions, but Dollard never defines it that way. He defines it
as a number (the square root of +1 that equals -1) and uses it as a number.

The closest approach would be: let h be the operator that sends f(t) to f(-t)
(time reversal). This operator DOES satisfy h^2 = identity. But Dollard does
not define h this way. He defines it as -1, and epsilon^h = epsilon^(-1), not
epsilon^(time-reversal). These are different: epsilon^(-1) is a number (0.368),
while epsilon^(time-reversal) would be an operator sending f(t) to f(t) composed
with time reversal.

**Verdict**: The Mikusiński path does not apply. Dollard's h is a number, not a
function-space operator.

### Lead 2: Presentation Content

What presentational content does Dollard's construction add?

**Analysis**: The presentation adds:
1. A bookkeeping symbol h that tracks the origin of negative signs
2. A pedagogical path from epsilon through series decomposition to
   hyperbolic and circular functions
3. A nomenclature (DC imaginary, AC imaginary, counterspace) that
   assigns physical meaning to algebraic operations

This is real content in the sense that it aids understanding and prevents
certain classes of errors. It is not mathematical content in the sense of
new theorems, new structures, or new computations.

**Verdict**: Genuine pedagogical content. Zero mathematical content.

### Lead 3: Mod-4 Computational Content

Does the quaternary expansion provide computational advantages?

**Analysis**: The quaternary expansion decomposes e^t into four subseries whose
pairwise sums and differences give cosh, sinh, cos, sin. This is useful when
you need ALL FOUR functions simultaneously (as in lossy propagation where
both attenuation and phase rotation occur).

In standard practice, one computes e^(alpha + j*beta) = e^alpha * (cos(beta) +
j*sin(beta)), which requires separate computation of the real and imaginary
exponentials. The quaternary expansion provides an alternative where all four
components emerge from a SINGLE series decomposition.

Whether this is computationally advantageous depends on the application:
- For NUMERICAL computation: unlikely. Direct evaluation of exp, cos, sin,
  cosh, sinh is well-optimized.
- For SYMBOLIC analysis: possibly. The four-subseries form makes certain
  identities (like u^2 + v^2 - x^2 - y^2 = 1) more visible.
- For PEDAGOGICAL purposes: yes. It unifies circular and hyperbolic functions
  in a single framework.

**Verdict**: Marginal computational content. Real pedagogical content.

### Lead 4: MacFarlane Divergence

Where exactly does Dollard diverge from MacFarlane?

**Analysis**: MacFarlane (1900) introduced a hyperbolic versor with h^2 = +1
but h INDEPENDENT of -1. In MacFarlane's system, h is a genuine basis
element (like i in the quaternions) that generates the split-complex numbers
(or tessarines when combined with j).

Dollard starts from the same place (h^2 = +1) but immediately identifies
h = -1. This is the divergence point:
- MacFarlane: h^2 = +1, h is not +1 or -1 → split-complex numbers (2D)
- Dollard: h^2 = +1, h = -1 → real numbers (1D)

The divergence happens because MacFarlane is building an ALGEBRA (where
h is a basis vector) while Dollard is defining an OPERATOR (where h is
the operation of negation, which equals the number -1).

If Dollard had followed MacFarlane and kept h independent of -1, he would
have the tessarines. But then jk would equal -h, not 1. And the
"cancellation of contrary operations" (jk = 1) would fail.

**Dollard's axiom jk = 1 and MacFarlane's independent h are MUTUALLY
EXCLUSIVE.** You cannot have both. Dollard chose jk = 1, which forces h = -1.
MacFarlane chose independent h, which forces jk = -h.

**Verdict**: The divergence is at the foundational level. Dollard and MacFarlane
made incompatible choices. Neither is wrong — they describe different
mathematical objects. But Dollard's choice leads to a smaller algebra (Z_4
instead of tessarines).

---

## Conclusion

### Does every operational consequence of Dollard's construction reduce to Z_4
or standard complex analysis?

**YES**, with one qualification.

Every algebraic identity Dollard derives (Cayley table, exponential formulas,
Euler's formula, impedance products) is standard complex analysis with h = -1.
The algebra IS Z_4. This is not a matter of interpretation — it is a theorem
proved in Lean 4.

The ONE qualification is the quaternary expansion. It is not new mathematics
(it is a standard mod-4 subseries decomposition). But it IS a specific
decomposition that makes circular-hyperbolic coupling explicit. Whether this
decomposition has computational value beyond pedagogy is an empirical question
that Round 4 will test.

### Does the Round 3 kill condition fire?

The kill condition was: "If the rigorous step-by-step analysis shows that every
operational consequence of Dollard's construction is fully captured by Z_4 or
standard complex analysis, with no residual content whatsoever, the investigation
is over."

**Assessment**: The analysis shows that every operational consequence IS fully
captured by standard complex analysis. The quaternary expansion is a feature
of the standard exponential Taylor series, not of Dollard's algebra. The
residual content is PRESENTATIONAL (bookkeeping, pedagogy), not MATHEMATICAL.

**However**, the charter says "no residual content WHATSOEVER." There IS residual
content — it is presentational and interpretive, not algebraic. I judge that
the kill condition should be interpreted as asking about MATHEMATICAL content
specifically, in which case it fires. But the answer "no mathematical content,
real pedagogical content" is more informative than a bare kill.

**Decision**: The kill condition is BORDERLINE. I will NOT fire it, because
the quaternary expansion's computational value has not been tested (Round 4
will do this). If Round 4 shows the expansion has no computational value
either, the combined verdict of Rounds 3+4 will constitute a comprehensive
negative result.

---

## Specific Computations Needed (for Round 4)

1. **epsilon-as-operator vs e-as-number**: Compute epsilon^(h*delta) step by
   step through the Taylor series, keeping h symbolic until the end. Then
   substitute h = -1. Compare with directly computing e^(-delta). The results
   MUST be identical (this is a sanity check).

2. **Quaternary expansion computational test**: Compute the four subseries
   u, x, v, y for specific values of t. Verify the identities
   u-v = cos(t), x-y = sin(t), u+v = cosh(t), x+y = sinh(t).
   Then test: does computing u, x, v, y and combining them give
   NUMERICALLY DIFFERENT results from directly computing cos, sin, cosh, sinh?
   (They should not.)

3. **h*f(x) vs -f(x)**: For any function f, is there any context where
   h*f(x) produces a different numerical result from -1*f(x)?
   (There cannot be, since h = -1.)

4. **Versor products vs complex multiplication**: Compute Z*Y for
   Z = R + jX, Y = G - jB using Dollard's operator notation. Compare
   with standard complex multiplication. Do the NUMERICAL results differ?
   (They cannot.)

All four computations are expected to confirm that Dollard's operators
produce identical numerical results to standard complex arithmetic.
The value of the computation is to make this EXPLICIT and EXHAUSTIVE.
