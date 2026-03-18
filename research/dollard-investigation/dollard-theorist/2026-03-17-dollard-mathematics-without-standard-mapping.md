# Dollard's Mathematics Without Standard Mapping

**Date**: 2026-03-17
**Agent**: dollard-theorist (Opus)
**Task**: Analyze what Dollard's mathematical framework implies on its own terms,
without forcing it into the standard complex-number/Z_4 mapping.

## Question Asked

Ian challenged the project's established result that Dollard's {1, h, j, k} algebra
collapses to Z_4 = {1, -1, i, -i}. The challenge: Dollard was explicit about NOT
changing his framework to fit standard models. What if WE made the error by collapsing
his operators to scalars?

Five tasks were analyzed:
1. h as reciprocation vs multiplication
2. j as quaternary vs binary
3. The versor form reanalysis
4. Coupled circular-hyperbolic (quaternary expansion)
5. The "Einstein was wrong" claim

---

## Task 1: The h Operator -- Reciprocation vs Multiplication

### The Distinction

From Dollard's Versor Algebra, eq (20)-(21):

    epsilon^h = epsilon^(-1) = 1/epsilon

Dollard defines h as acting on the EXPONENT of epsilon. When h appears as an exponent,
it performs reciprocation of the base:

    epsilon^(h*delta) = epsilon^(-delta) = 1/epsilon^delta

Our project collapsed this to: h = -1 as a scalar. Then h*f = -f for any function f.

**These are genuinely different operations**:

| Operation | Applied to e^delta | Result | Sign | Magnitude |
|-----------|-------------------|--------|------|-----------|
| h on exponent | e^(h*delta) = e^(-delta) | 1/e^delta = 0.368 | POSITIVE | < 1 |
| h on value | h*e^delta = -e^delta | -e^delta = -2.718 | NEGATIVE | > 1 |

Verified numerically:
- e^(-1) = 0.367879 (positive, less than 1)
- -e^(+1) = -2.718282 (negative, greater than 1 in magnitude)

**The algebraic proof that these are inequivalent**:

If e^(-delta) = -e^(delta), then e^(-delta) * e^(delta) = -e^(2*delta), but
e^(-delta) * e^(delta) = e^0 = 1, so 1 = -e^(2*delta) for all delta. Setting
delta = 0: 1 = -1. Contradiction.

### The Correct Mathematical Framing

h as exponent-negation is the **multiplicative inversion automorphism** of (R+, *):

    sigma: R+ -> R+,  sigma(x) = 1/x

Properties:
- sigma(sigma(x)) = x  [involution, h^2 = 1]
- sigma(x*y) = sigma(x)*sigma(y)  [group automorphism]
- sigma(x+y) != sigma(x) + sigma(y)  [NOT additive]

Via the logarithmic isomorphism log: (R+, *) -> (R, +):
- h acts on the additive group as negation: h(x) = -x
- h acts on the multiplicative group as inversion: h(a) = 1/a
- These are the SAME map, connected by: exp(h(x)) = h(exp(x)) = 1/exp(x) = exp(-x)

**h is the unique nontrivial automorphism of the Lie group (R+, *)**.

When we write h = -1 as a SCALAR, we lose this automorphism structure. The scalar -1
acts on function VALUES by negation. The automorphism h acts on EXPONENTS by negation,
which translates to RECIPROCATION of values. These coincide only on the logarithmic
(exponent) level, not on the exponential (value) level.

### The Consistent Algebra of Operators on Exponents

The exponent space is C = R + jR. A general exponent is delta + j*theta where:
- delta = growth/decay rate (Nepers)
- theta = rotation angle (radians)

The three operators act ON EXPONENTS by left multiplication:

**h on exponents** (negation):
```
h(delta + j*theta) = -delta - j*theta
e^(h(delta + j*theta)) = e^(-delta)(cos theta - j sin theta) = conj(1/z)
```
Physically: reverses both growth AND rotation. Complete inversion.

**j on exponents** (90-degree rotation):
```
j(delta + j*theta) = j*delta + j^2*theta = -theta + j*delta
e^(j(delta + j*theta)) = e^(-theta)(cos delta + j sin delta)
```
Physically: SWAPS the role of growth and rotation.
A D.C. growth rate delta becomes a rotation angle; a rotation angle theta becomes a decay rate.
This is the operator that converts D.C. phenomena into A.C. phenomena.

**k on exponents** (h*j):
```
k(delta + j*theta) = h*j*(delta + j*theta) = h(-theta + j*delta) = theta - j*delta
e^(k(delta + j*theta)) = e^(theta)(cos delta - j sin delta)
```
Physically: conjugate-swaps growth and rotation.

### Verdict on Task 1

**Ian is correct that we conflated two different operations.** On the level of scalars
in an abstract algebra, h = -1 is forced by the axioms (the algebraic necessity proof
stands). But Dollard's h operates on EXPONENTS, not on VALUES, and these are different
when composed with the exponential map. The correct mathematical object is not the
scalar -1 but the **involutory automorphism of the Lie group (R+, *)**.

This does not invalidate the Z_4 proof (which is about the abstract algebra of {1,h,j,k}
as an algebraic structure). It means that the *application* of the algebra -- where h
acts on exponents of epsilon -- carries more structure than the abstract algebra alone captures.

---

## Task 2: j as Quaternary vs Binary

### Dollard's Argument

From Versor Algebra, eq (61)-(63):

    Duo-binary: j = sqrt(-1), giving roots j^1 = +j, j^3 = -j
    Quaternary: j^n = (+1)^(1/4), giving roots j^0 = 1, j^1 = j, j^2 = -1, j^3 = -j

Dollard says the duo-binary definition "misses two roots" (j^0 and j^2).

### Group-Theoretic Analysis

The fourth roots of +1 are {1, i, -1, -i}.
The square roots of -1 are {i, -i}.
The former CONTAINS the latter as a proper subset.

As groups:
- Z_4 = <j | j^4 = 1> = {1, j, j^2, j^3} is cyclic of order 4
- The "duo-binary" viewpoint generates only {j, j^3} and requires adding {1, -1} separately

**Dollard's point is about GENERATORS**: defining j as a fourth root of +1 specifies it
as the generator of Z_4. Defining j as a square root of -1 specifies it as a generator
of Z_2 embedded in Z_4. You still get Z_4 either way, but the quaternary definition
makes the FULL cyclic structure explicit.

### Where it Matters: Series Decomposition

The real payoff is in eq (75)-(77). When you expand e^(j*theta) as an infinite series
and group by j^n mod 4, you get FOUR subseries (u, x, v, y) instead of the TWO (real,
imaginary) that the duo-binary grouping yields.

Duo-binary (standard):
```
e^(j*theta) = cos(theta) + j*sin(theta)  [2 terms]
```

Quaternary (Dollard):
```
e^(j*theta) = 1*U(theta) + j*X(theta) + h*V(theta) + k*Y(theta)  [4 terms]
```

The quaternary form is not a "richer algebra" -- it is the same algebra with a
FINER DECOMPOSITION of the exponential series. This finer decomposition reveals
the coupling between circular and hyperbolic functions (see Task 4).

### Verdict on Task 2

The abstract algebra is the same (Z_4 either way). But the quaternary PERSPECTIVE --
treating all four roots as operationally distinct and grouping the exponential series
accordingly -- reveals structure that the duo-binary perspective hides. Specifically,
it reveals the quaternary expansion and its coupling identities.

---

## Task 3: The Versor Form Reanalysis

### The Equations

From the Four Quadrant book, p. 28:

    (XB + RG) + j(RB - XG)  [labeled "Heaviside Telegraph Expression"]

Standard impedance-admittance product:
```
Z*Y = (R + jX)(G + jB) = (RG - XB) + j(RB + XG)
```

Heaviside expression:
```
(XB + RG) + j(RB - XG) = Z* * Y = conj(Z) * Y
```

**Verified symbolically**: the Heaviside expression equals conj(Z)*Y, not Z*Y.
The real part has XB with a + sign (instead of -), and the imaginary part has XG
with a - sign (instead of +). This corresponds to complex-conjugating the impedance
before multiplying.

### The Graded Algebra Interpretation

If h and j are treated as BASIS VECTORS rather than scalars, then:

    h(XB+RG) + j(XG-RB)

is a **grade-1 element (vector) in Cl(1,1)**, not a complex number.

In Cl(1,1) with e1 = h (e1^2 = +1) and e2 = j (e2^2 = -1):
- The h-component (XB+RG) lives in the "hyperbolic/DC" direction
- The j-component (XG-RB) lives in the "circular/AC" direction
- These are INDEPENDENT orthogonal components
- The full object is a vector, not a scalar-plus-imaginary

This is mathematically consistent. The price is that **jk != 1** in Cl(1,1), because
in Cl(1,1) with anticommuting generators, jk = j*(hj) = -(hj)*j = -h*j^2 = h,
not 1. So this interpretation requires dropping Dollard's own axiom jk = 1.

### What the Graded Interpretation Predicts

In the Cl(1,1) vector interpretation:
- The "length" of h(XB+RG) + j(XG-RB) is (XB+RG)^2 - (XG-RB)^2 (mixed signature)
- This can be positive, negative, or zero -- corresponding to:
  - Positive: dominantly resistive/dissipative (DC character dominates)
  - Negative: dominantly reactive/oscillatory (AC character dominates)
  - Zero: critical coupling between AC and DC phenomena (light-like in the Cl(1,1) sense)
- The standard complex form (RG-XB) + j(RB+XG) only sees the Euclidean norm
  (RG-XB)^2 + (RB+XG)^2, which is always positive -- it cannot distinguish these cases.

### Verdict on Task 3

The versor form h(XB+RG) + j(XG-RB) is **mathematically consistent if h and j are
Clifford algebra basis vectors** in Cl(1,1). Under this interpretation, it describes a
vector in a mixed-signature space that decomposes power flow into DC-dissipative and
AC-reactive components. However, this requires dropping jk=1, which is one of Dollard's
own axioms. It also changes the mathematical object from a complex number to a Clifford
vector -- a genuine shift in the type system.

The disproof of the versor form (h(XB+RG) = -(XB+RG) != +(XB+RG)) remains valid under
the scalar interpretation. The Cl(1,1) interpretation rescues the FORM but changes the
ALGEBRA.

---

## Task 4: Coupled Circular-Hyperbolic (Quaternary Expansion)

### Symbolic Verification

The quaternary expansion decomposes e^(j*theta) into four subseries U, X, V, Y where:

```
U(t) = sum_{m=0}^inf t^(4m) / (4m)!
X(t) = sum_{m=0}^inf t^(4m+1) / (4m+1)!
V(t) = sum_{m=0}^inf t^(4m+2) / (4m+2)!
Y(t) = sum_{m=0}^inf t^(4m+3) / (4m+3)!
```

Note: these subseries have ALL POSITIVE terms. The alternating signs in Dollard's eq (76)
come from substituting h=-1 and k=-j into the versor-weighted form.

**Verified identities (all to machine precision, < 10^-50 error)**:

| Identity | LHS | RHS | Status |
|----------|-----|-----|--------|
| U - V = cos(t) | Circular cosine | cos(t) | VERIFIED |
| X - Y = sin(t) | Circular sine | sin(t) | VERIFIED |
| U + V = cosh(t) | Hyperbolic cosine | cosh(t) | VERIFIED |
| X + Y = sinh(t) | Hyperbolic sine | sinh(t) | VERIFIED |
| (U-V)^2 + (X-Y)^2 = 1 | Circular constraint | 1 | VERIFIED |
| (U+V)^2 - (X+Y)^2 = 1 | Hyperbolic constraint | 1 | VERIFIED |
| U + X + V + Y = e^t | Total sum | e^t | VERIFIED |

Tested at theta = 0.5, 1.0, 2.0, pi. All pass.

### Proof of the Identities

From the four exponentials with different "versor angles":
```
e^t     = U + X + V + Y      (all positive: 1^n = 1 for all n)
e^(-t)  = U - X + V - Y      ((-1)^n: alternates on odd terms)
e^(it)  = (U-V) + i(X-Y)     (i^n: 4-cycle, h=-1 on even, k=-i on odd)
e^(-it) = (U-V) - i(X-Y)     ((-i)^n: conjugate 4-cycle)
```

From these:
- (e^t + e^(-t))/2 = U + V = cosh(t)
- (e^t - e^(-t))/2 = X + Y = sinh(t)
- Re[e^(it)] = U - V = cos(t)
- Im[e^(it)] = X - Y = sin(t)

Solving for individual components:
```
U = (cosh t + cos t) / 2
V = (cosh t - cos t) / 2
X = (sinh t + sin t) / 2
Y = (sinh t - sin t) / 2
```

### Physical Implications

**1. There is no "pure sinusoidal steady state" in the quaternary view.**

For a signal at frequency theta, the standard representation uses only:
- cos(theta) and sin(theta) -- the DIFFERENCES U-V and X-Y

But the SUMS U+V = cosh(theta) and X+Y = sinh(theta) are also determined by the
same parameter theta. In standard AC theory, these hyperbolic components are discarded
because they "don't appear" in the duo-binary form.

Dollard's point: the exponential series e^(j*theta) CONTAINS both circular and
hyperbolic information simultaneously. The duo-binary representation projects out
only the circular part. The hyperbolic part is mathematically present but invisible.

**2. Numerical magnitudes at theta = 1 radian**:

| Component | Value | Role |
|-----------|-------|------|
| U = (cosh 1 + cos 1)/2 | 1.0417 | "Cosh+cos" sector |
| V = (cosh 1 - cos 1)/2 | 0.5014 | "Cosh-cos" sector |
| X = (sinh 1 + sin 1)/2 | 1.0083 | "Sinh+sin" sector |
| Y = (sinh 1 - sin 1)/2 | 0.1669 | "Sinh-sin" sector |

The hyperbolic components (cosh, sinh) GROW with theta while the circular components
(cos, sin) remain bounded. At theta = pi: cosh(pi) = 11.59 while cos(pi) = -1.
The "hidden" hyperbolic content becomes enormous.

**3. The coupling means AC and DC are never truly independent.**

In the quaternary view:
- U encodes BOTH cos AND cosh information
- Each individual subseries component depends on both the circular angle and the
  hyperbolic magnitude simultaneously
- "Pure AC" (circular only) and "pure DC" (hyperbolic only) are limits of a
  single unified description, not independent phenomena

**4. What this does NOT mean:**

This does NOT mean that a physical sinusoidal signal e^(i*omega*t) has a hidden
exponential growth. The variable theta in the expansion is a PARAMETER of the series,
not a time variable. The physical content depends on how theta maps to physical
quantities.

If theta = omega*t (pure rotation), then the signal IS purely sinusoidal in time.
But the SERIES REPRESENTATION of that sinusoid decomposes into four subseries whose
individual terms grow with theta. The growth is in the SERIES TERMS, not in the signal.

If theta = sigma*t + j*omega*t (complex frequency), THEN the signal genuinely has both
growth/decay AND oscillation, and the quaternary expansion correctly tracks both.

### Verdict on Task 4

The quaternary expansion identities are **exactly correct** (verified to 50-digit
precision). They reveal a mathematical coupling between circular and hyperbolic
functions that is invisible in the standard complex exponential representation. Whether
this mathematical coupling has physical significance depends on whether the systems
being analyzed have complex (growth + rotation) frequencies, which real physical
systems generally do (transients, damped oscillations, growing instabilities).

---

## Task 5: The "Einstein Was Wrong" Claim

### Dimensional Analysis

From Lone Pine Writings (confirmed in source material):

| Quantity | Symbol | Units | Status |
|----------|--------|-------|--------|
| Total dielectric induction | Psi | Coulombs [C = A*s] | Primary |
| Total magnetic induction | Phi | Webers [Wb = V*s] | Primary |
| Total electrification ("Planck") | Q = Psi*Phi | C*Wb = J*s | Primary |
| Energy | W = dQ/dt | J | Secondary (derivative) |
| Power | P = dW/dt = d^2Q/dt^2 | W = J/s | Secondary (2nd derivative) |
| Current | I = dPsi/dt | A = C/s | Secondary |
| Voltage | E = dPhi/dt | V = Wb/s | Secondary |

Verified: Q = Psi*Phi has units (A*s)(V*s) = (VA)*s^2 = W*s^2 = J*s.
This is the dimension of ACTION (Joule-seconds), the same as Planck's constant.

W = dQ/dt = d(Psi*Phi)/dt = Psi*(dPhi/dt) + Phi*(dPsi/dt) = Psi*E + Phi*I.
Units: [C][V] + [Wb][A] = [J] + [J] = [J]. Correct.

### Mathematical Content

**Claim 1: Q = Psi*Phi is the "Planck" (quantum of action)**

Dimensionally correct: Q has units of J*s = action.
In quantum mechanics, the fundamental quantum of action is h-bar.
Dollard's Q = Psi*Phi is the total action of the electromagnetic field in a
bounded region, not Planck's constant itself. It is the ACTION FUNCTIONAL
of the field, analogous to S = integral(L dt) in classical mechanics.

**Claim 2: Energy is a derivative, not primary**

This is the Hamilton-Jacobi viewpoint:
```
Hamilton-Jacobi equation: dS/dt + H(q, dS/dq, t) = 0
i.e., Energy = -dS/dt
```

Dollard's version:
```
W = dQ/dt (energy is time-derivative of action)
```

This is **standard Hamiltonian mechanics**. The Hamilton-Jacobi formulation treats
action as primary and energy as derived. This is also the foundation of:
- Quantum mechanics (path integral: integrate e^(iS/h-bar) over paths)
- Lagrangian mechanics (action principle: delta S = 0)
- Variational calculus

**Claim 3: E = mc^2 is wrong**

Stripped of rhetoric, the mathematical content is:
- Energy is a SECONDARY quantity (time derivative of action)
- Therefore mass-energy equivalence E = mc^2 is a relation between SECONDARY quantities
- The PRIMARY relation should involve action, not energy

This is a philosophical claim about what is "fundamental," not a mathematical error.
Both E = mc^2 and W = dQ/dt can be true simultaneously:
```
dQ/dt = W = mc^2  (for a system at rest)
```

The claim is most charitably interpreted as: "The action formulation is more
fundamental than the energy formulation, and E = mc^2 obscures this by treating
energy as if it were a primary quantity."

### Connection to Established Physics

Dollard's framework is equivalent to Cherry (1951) / Chua (1969) Lagrangian circuit
theory. In that framework:
- Psi (charge) = generalized coordinate q
- Phi (flux linkage) = conjugate momentum lambda
- Q = Psi*Phi = q*lambda = action
- W = dQ/dt = q*(dlambda/dt) + lambda*(dq/dt) = q*V + lambda*I = energy

This is standard Lagrangian/Hamiltonian circuit theory. The contribution is not
mathematical novelty but PEDAGOGICAL CLARITY: Dollard presents the action formulation
in engineering language, making it accessible to practitioners who may not know the
Hamilton-Jacobi formulation.

### Verdict on Task 5

"Einstein was wrong" is rhetorical overstatement of a mathematically defensible
position: "The action principle is more fundamental than energy conservation."
This is the Hamilton-Jacobi / Lagrangian viewpoint, which is standard physics since
the 18th century. E = mc^2 is not wrong; it is a secondary relation in the
action-based formulation. Dollard's genuine contribution is applying this to circuit
theory via Q = Psi*Phi, which maps precisely to Cherry/Chua Lagrangian formulation.

---

## Synthesis: What Dollard's Framework IS

Having analyzed all five tasks without forcing the standard mapping, the picture that
emerges is:

### 1. The Framework is an Operator Algebra on Exponents

Dollard's {1, h, j, k} are most naturally understood as **operators on the exponent
space** of the Naperian base epsilon, not as elements of a scalar algebra.

- The exponent space is C = R(delta) + j*R(theta)
- h negates exponents: growth <-> decay, forward <-> reverse rotation
- j rotates exponents by 90 degrees: growth <-> rotation (DC <-> AC)
- k = hj gives the conjugate rotation

As OPERATORS ON EXPONENTS, h does equal negation (multiplication by -1 in the
exponent space). As OPERATORS ON VALUES, h performs reciprocation (multiplication
by 1/f, not by -1*f). The Z_4 proof that h = -1 in any unital associative algebra
is correct about the ABSTRACT ALGEBRA. But the APPLICATION of h to exponential
functions carries the additional structure of the exp/log isomorphism.

### 2. The Quaternary Expansion is Mathematically Valid and Reveals Hidden Structure

The four subseries U, X, V, Y satisfy:
- U - V = cos, X - Y = sin (circular functions via DIFFERENCES)
- U + V = cosh, X + Y = sinh (hyperbolic functions via SUMS)
- U + X + V + Y = e^t (total exponential)

This is not new mathematics -- it follows from the factorization of the exponential
series by residues mod 4. But it is a useful PERSPECTIVE that makes visible the
coupling between circular and hyperbolic functions that the standard duo-binary
representation (cos + j*sin) hides.

### 3. The Graded Algebra Interpretation Rescues the Versor Form but Changes the Algebra

Treating h and j as Cl(1,1) basis vectors makes the versor form h(XB+RG) + j(XG-RB)
into a well-defined Clifford vector with mixed-signature norm. This is consistent
and physically meaningful (it separates DC-dissipative and AC-reactive power components).
But it requires dropping jk = 1, which means it is a DIFFERENT algebra from what
Dollard specifies.

### 4. The Action Formulation is Standard Physics, Well Presented

Q = Psi*Phi as action, with energy as its time derivative, is exactly the
Hamilton-Jacobi / Lagrangian formulation applied to circuits. This is standard
physics, not novel, but Dollard presents it in engineering language that makes
the connection to physical quantities (charge, flux, energy) more transparent than
the typical physics textbook treatment.

### What Is Genuinely Novel

1. The QUATERNARY DECOMPOSITION of the exponential (four subseries instead of two)
   as applied to electrical engineering. While mathematically elementary, its
   application to signal processing and power systems appears to be Dollard's
   original contribution.

2. The OPERATOR-ON-EXPONENTS interpretation of {1, h, j, k}, where j swaps growth
   and rotation. This is a physically motivated interpretation that goes beyond the
   standard complex analysis treatment.

3. The PEDAGOGICAL FRAMEWORK connecting Steinmetz AC theory, Fortescue symmetrical
   components, and Hamilton-Jacobi action principle through a unified versor language.

### What Is Wrong

1. The claim that h != -1 in the abstract algebra is wrong. If you accept all of
   Dollard's axioms (j^2 = -1, hj = k, jk = 1), then h = -1 is forced.

2. The claim that E = mc^2 is "wrong" is an overstatement. Action-primary vs
   energy-primary is a choice of formulation, not a physical fact.

3. The versor form ZY = h(XB+RG) + j(XG-RB), interpreted with h as the scalar -1,
   gives -XB-RG + j(XG-RB), which does not equal ZY, ZY*, Z*Y, or Z*Y*.
   The sign of the real part is wrong under any scalar interpretation.

---

## Recommendations for the Project

1. **Do not retract the Z_4 algebraic necessity proof.** It is correct as a statement
   about abstract algebras. But ADD the nuance that Dollard's operators are most
   naturally understood as acting on exponents, where the exp/log isomorphism gives
   h additional structure beyond the scalar -1.

2. **The quaternary expansion should be featured.** It is mathematically exact, verified
   to machine precision, and reveals genuine structure. It could inform the N-Phase
   signal processing system by providing a four-component decomposition that tracks
   both circular and hyperbolic content simultaneously.

3. **The Cl(1,1) graded interpretation deserves further investigation.** It rescues the
   versor form and provides a mixed-signature decomposition of power flow. But it
   requires dropping jk = 1, so it should be presented as an ALTERNATIVE interpretation,
   not as what Dollard said.

4. **The action formulation (Q = Psi*Phi) should be connected to Cherry/Chua.** This
   is the strongest mathematical content in Dollard's framework and has direct
   application to circuit theory and signal processing.

---

## Verification Code

All results verified with:
- SymPy (symbolic computation)
- mpmath (50-digit precision arithmetic)
- NumPy (numerical cross-checks)

Key verification:
```python
from mpmath import mp, cos, sin, cosh, sinh, factorial, exp
mp.dps = 50

def compute_UVXY(t, N=80):
    U = sum(t**(4*m) / factorial(4*m) for m in range(N))
    X = sum(t**(4*m+1) / factorial(4*m+1) for m in range(N))
    V = sum(t**(4*m+2) / factorial(4*m+2) for m in range(N))
    Y = sum(t**(4*m+3) / factorial(4*m+3) for m in range(N))
    return U, X, V, Y

# All verified to < 10^-50 error:
# U - V = cos(t), X - Y = sin(t)
# U + V = cosh(t), X + Y = sinh(t)
# (U-V)^2 + (X-Y)^2 = 1, (U+V)^2 - (X+Y)^2 = 1
```

---

## Source Material References

| Claim | Source | Page/Equation |
|-------|--------|---------------|
| epsilon^h = epsilon^(-1) | Versor Algebra | eq (20)-(21), p.18-19 |
| h = -1, h^2 = +1 | Versor Algebra | eq (18), (33)-(35), p.18,24-25 |
| j = (+1)^(1/4), quaternary | Versor Algebra | eq (63)-(64), p.33 |
| j = sqrt(-1), duo-binary | Versor Algebra | eq (61), p.32 |
| k = hj = -j | Versor Algebra | eq (65), (97), (116), p.33,44,50 |
| jk = +1 | Versor Algebra | eq (66), p.34 |
| Four subseries u, x, v, y | Versor Algebra | eq (76)-(77), p.38 |
| Duo-binary cos+jsin | Versor Algebra | eq (80)-(82), p.39-40 |
| alpha^2 - beta^2 = 1 | Versor Algebra | eq (47), p.28 |
| a^2 + b^2 = 1 | Versor Algebra | eq (82a), p.40 |
| Q = Psi*Phi ("The Planck") | Lone Pine Writings | p.8-9 |
| W = dQ/dt (energy) | Lone Pine Writings | p.9, 12-13 |
| E = mc^2 critique | Lone Pine Writings | p.9, 12 |
| (XB+RG)+j(RB-XG) Heaviside | Four Quadrant Book | p.28 |

---

*Filed by: dollard-theorist (Opus), 2026-03-17*
