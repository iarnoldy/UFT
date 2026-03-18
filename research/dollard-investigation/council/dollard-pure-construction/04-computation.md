# Round 4: COMPUTATION — Numerical Verification of Dollard's Operational Claims

**Agent**: Direct Python execution
**Date**: 2026-03-17
**Investigation**: dollard-pure-construction
**Prior rounds**: `01-vision.md`, `02-literature.md`, `03-analysis.md`
**Script**: `src/experiments/council/dollard_pure_construction_tests.py`

---

## Tests Performed

Four computational tests designed to determine whether Dollard's operational
construction produces ANY numerical results that differ from standard complex
arithmetic.

### Test 1: epsilon^(h*delta) vs e^(-delta)

**Method**: Compute the Taylor series of e^(h*delta) step by step, keeping h
symbolic as alternating +1/-1 coefficients (the mod-2 subseries decomposition
into cosh and sinh). Then substitute h = -1 and compare with direct e^(-delta).

**Results**: For delta = 0, 0.5, 1.0, 2.0, 5.0: IDENTICAL to machine precision
(differences < 10^-12). For delta = 10.0: small numerical differences (~10^-12)
due to floating point precision loss in the 80-term Taylor series — this is a
numerical artifact, not a mathematical difference.

**Intermediate values verified**:
- The real part of the h-decomposition = cosh(delta) at ALL test points
- The h-part of the decomposition = sinh(delta) at ALL test points
- The final result (cosh - sinh) = e^(-delta) at ALL test points

**Verdict**: epsilon^(h*delta) IS e^(-delta). The intermediate decomposition
into cosh and sinh is real (the mod-2 subseries are genuinely cosh and sinh),
but the final numerical result is identical to direct computation.

### Test 2: Quaternary Expansion

**Method**: Compute the four subseries u, x, v, y of e^t (terms with exponents
congruent to 0, 1, 2, 3 mod 4) for t = 0, 0.5, 1, pi/4, pi/2, pi, 2, 3, 5.
Verify all identities.

**Results**: ALL identities verified to < 10^-10:

| Identity | Maximum error across all test points |
|----------|-------------------------------------|
| u - v = cos(t) | 2.2 x 10^-15 |
| x - y = sin(t) | 1.4 x 10^-15 |
| u + v = cosh(t) | 0 |
| x + y = sinh(t) | 1.8 x 10^-15 |
| u + x + v + y = e^t | 2.8 x 10^-14 |

**Computational equivalence**: The four subseries are EXACTLY:
- u = (cosh(t) + cos(t))/2 — verified to 0 error
- x = (sinh(t) + sin(t))/2 — verified to 0 error
- v = (cosh(t) - cos(t))/2 — verified to 0 error
- y = (sinh(t) - sin(t))/2 — verified to 0 error

**Verdict**: The quaternary expansion is a LINEAR REARRANGEMENT of the standard
trigonometric and hyperbolic functions. It contains ZERO information beyond
what cos, sin, cosh, sinh already contain. The transformation from
{cos, sin, cosh, sinh} to {u, x, v, y} is invertible (a 4x4 matrix with
entries +/-1/2), so no information is gained or lost. The quaternary
expansion is a change of basis, not new content.

### Test 3: h*f(x) vs -f(x)

**Method**: Test h*f(x) vs -f(x) for 8 different functions (exp, sin, cos,
x^2, 1/x, sinh, cosh, log|x|) at 7 test points each = 56 total tests.

**Results**: ALL 56 tests passed. h*f(x) = -f(x) to machine precision for
every function at every point.

**Operational order test**: The distinction between epsilon^(h*delta) = e^(-delta)
and h*epsilon^(delta) = -e^(delta) is confirmed to be real but is the standard
distinction between f(-x) and -f(x). This is a property of real-number
arithmetic (the exponential is not odd), not of any operator.

**Verdict**: h = -1 exactly and completely. There is no context in which h
produces a different numerical result from -1.

### Test 4: Versor Products vs Complex Multiplication

**Method**: Compute Z*Y for Z = R+jX, Y = G-jB using standard complex
multiplication and compare with Dollard's claimed form h(XB+RG)+j(XG-RB),
for 7 test cases.

**Results**: Standard complex multiplication ALWAYS produces the correct
algebraic result (RG+XB) + j(XG-RB). Dollard's claimed form h(XB+RG)+j(XG-RB)
NEVER matches (it negates the real part, since h = -1).

| Test case | Standard correct? | Dollard correct? |
|-----------|------------------|-----------------|
| Z=1, Y=1 | YES | NO (wrong sign) |
| Z=j, Y=-j | YES | NO (wrong sign) |
| Z=1+j, Y=1-j | YES | NO (wrong sign) |
| Z=3+4j, Y=0.2-0.1j | YES | NO (wrong sign) |
| Z=50, Y=0.02 | YES | NO (wrong sign) |
| Z=100j, Y=-0.01j | YES | NO (wrong sign) |
| Z=10+20j, Y=0.05-0.03j | YES | NO (wrong sign) |

**Verdict**: Dollard's versor form ZY = h(XB+RG)+j(XG-RB) is WRONG in his own
algebra. The real power (RG+XB) appears in the 1-component, not the
h-component. This confirms the prior refutation in
`research/tessarine-discovery/04-algebraic-verification-REFUTED.md`.

---

## Kill Condition Assessment

**Round 4 kill condition**: "If computation directly contradicts the mathematical
analysis from Round 3."

Round 3 concluded: every operational consequence is captured by standard
complex analysis. Round 4 confirms: every numerical result matches standard
complex arithmetic. The quaternary expansion contains no information beyond
standard functions.

**The computation DOES NOT contradict Round 3. Kill condition does NOT fire.**

The computation and the analysis are in agreement: Dollard's construction
produces identical numerical results to standard complex arithmetic, with
one specific formula (the versor form) being demonstrably wrong.

---

## Summary

| Question | Answer | Confidence |
|----------|--------|-----------|
| Does epsilon-as-operator differ from e-as-number? | NO | 99.9% |
| Does the quaternary expansion have new information? | NO — linear rearrangement of standard functions | 99.9% |
| Is there a context where h*f(x) differs from -f(x)? | NO — h = -1 exactly | 100% (theorem) |
| Do versor products differ from complex multiplication? | NO — standard complex is correct; Dollard's specific form is wrong | 100% |

The computational evidence is unambiguous: Dollard's operational construction
produces zero results that differ from standard complex arithmetic.
