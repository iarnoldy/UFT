# Round 3: RIGOR -- Formal Conditioning Analysis of DPQA

**Investigation**: lifted-representation
**Round**: 3 of 5
**Agent**: dollard-theorist (PhD-level mathematical rigor)
**Date**: 2026-03-17

---

## Executive Summary

**DPQA (Deferred-Projection Quaternary Arithmetic) has a fatal conditioning flaw.**

The quaternary representation (u, x, v, y) mixes bounded oscillatory components
(cos, sin) with exponentially growing components (cosh, sinh). While the cyclic
convolution for argument addition is indeed cancellation-free, the rounding errors
at each step are proportional to the component magnitudes, which grow as e^t.
After n steps of chain length theta each:

- **Standard rotation chain**: absolute error = O(nu), condition number 1 per step
- **DPQA chain**: absolute error = O(nu * e^{n*theta}), spectral radius e^theta per step
- **Compensated rotation chain**: absolute error = O(nu^2), same condition as standard

DPQA is exponentially worse than the standard approach. The "cancellation-free"
property is real but numerically irrelevant -- it avoids O(u) cancellation errors
while introducing O(u * e^t) growth errors that dominate by an exponential factor.

**Kill condition K4 FIRES** (for the conditioning claim). The lift is algebraically
closed but numerically self-defeating. The standard rotation chain is provably
superior for all chain lengths and all total angles.

---

## A. Conditioning Bounds

### A1. The Standard Rotation Chain

**Setup.** Given a sequence of angles theta_1, ..., theta_n, compute
cos(s_n) and sin(s_n) where s_n = theta_1 + ... + theta_n by iterating:

```
c_{k+1} = c_k * cos(theta_{k+1}) - s_k * sin(theta_{k+1})
s_{k+1} = s_k * cos(theta_{k+1}) + c_k * sin(theta_{k+1})
```

This is the matrix-vector product:

```
[c_{k+1}]   [cos(theta)  -sin(theta)] [c_k]
[s_{k+1}] = [sin(theta)   cos(theta)] [s_k]  =  R(theta) * [c_k, s_k]^T
```

**Theorem A1 (Rotation chain absolute error bound).**

*The absolute error of the standard rotation chain after n steps satisfies*
*|epsilon_n| <= 3nu, independent of the values of s_k at intermediate steps,*
*including resonance crossings where cos(s_k) = 0.*

**Proof.** Let c_k = cos(s_k), s_k = sin(s_k) be exact values, and
c_hat_k, s_hat_k be computed values. Define the error vector
e_k = (epsilon_k, eta_k) = (c_hat_k - c_k, s_hat_k - s_k).

Using the standard floating-point error model fl(a op b) = (a op b)(1 + delta),
|delta| <= u (unit roundoff ~ 1.1e-16 for float64), the computed step is:

```
c_hat_{k+1} = fl(fl(c_hat_k * cos(theta)) - fl(s_hat_k * sin(theta)))
```

Expanding (dropping products of small quantities):

```
c_hat_{k+1} = c_{k+1} + epsilon_k*cos(theta) - eta_k*sin(theta)
              + c_k*cos(theta)*delta_1 - s_k*sin(theta)*delta_2
              + c_{k+1}*delta_3
```

The error recurrence is:

```
[epsilon_{k+1}]   [cos(theta)  -sin(theta)] [epsilon_k]   [r_{k+1}]
[  eta_{k+1}  ] = [sin(theta)   cos(theta)] [  eta_k  ] + [q_{k+1}]
```

where (r_{k+1}, q_{k+1}) is the new rounding error at step k+1.

**Key property: R(theta) is orthogonal.** Therefore ||R(theta)||_2 = 1, and the
error propagation is norm-preserving. The 2-norm of the error vector is NOT
amplified by passage through the rotation.

The new rounding error at each step has bounded magnitude. For the cosine
component:

```
|r_{k+1}| <= |c_k*cos(theta)|*u + |s_k*sin(theta)|*u + |c_{k+1}|*u
```

Using the identity |cos(a)cos(b)| + |sin(a)sin(b)| = max(|cos(a-b)|, |cos(a+b)|) <= 1
(proven via cos*cos = (cos(a-b)+cos(a+b))/2 and sin*sin = (cos(a-b)-cos(a+b))/2,
then |p| + |q| = (|p+q| + |p-q|)/2 = max(|cos(a-b)|, |cos(a+b)|)):

```
|r_{k+1}| <= u + |c_{k+1}|*u <= 2u
```

Similarly |q_{k+1}| <= 2u. So ||new_error||_2 <= 2*sqrt(2)*u < 3u.

After n steps, since each rotation preserves the error norm:

```
||e_n||_2 <= sum_{k=1}^{n} ||new_error_k||_2 <= 3nu   QED
```

**Corollary.** The relative error of cos(s_n) is:

```
|epsilon_n / cos(s_n)| <= 3nu / |cos(s_n)|
```

This is large when cos(s_n) ~ 0, but this is an inherent property of computing
a near-zero value -- not an artifact of the chain. The absolute error remains
O(nu) regardless of how many times cos(s_k) passes through zero during the chain.

**Critical insight: resonance crossings do NOT amplify error in the rotation chain.**
The "catastrophic cancellation" in cos(a+b) = cos(a)cos(b) - sin(a)sin(b) is
LOCAL: it means the computed cos(s_k) has poor relative precision at step k when
cos(s_k) ~ 0. But the absolute error remains O(ku), and the orthogonal propagation
means this poor-relative-precision intermediate does NOT inject extra error into
subsequent steps.

This demolishes the central premise of DPQA: that resonance crossings cause
cascading error accumulation in the standard chain. They do not.

---

### A2. The DPQA Chain

**Setup.** Represent the oscillatory state as (u, x, v, y) where:

```
u(t) = (cosh(t) + cos(t))/2     x(t) = (sinh(t) + sin(t))/2
v(t) = (cosh(t) - cos(t))/2     y(t) = (sinh(t) - sin(t))/2
```

Chain argument additions via cyclic convolution:

```
u' = u1*u2 + x1*y2 + v1*v2 + y1*x2
x' = u1*x2 + x1*u2 + v1*y2 + y1*v2
v' = u1*v2 + x1*x2 + v1*u2 + y1*y2
y' = u1*y2 + x1*v2 + v1*x2 + y1*u2
```

This is the circulant matrix-vector product:

```
[u']   [u2  y2  v2  x2] [u1]
[x'] = [x2  u2  y2  v2] [x1]  =  C(theta) * [u1, x1, v1, y1]^T
[v']   [v2  x2  u2  y2] [v1]
[y']   [y2  v2  x2  u2] [y1]
```

**Theorem A2 (Eigenvalue structure of the DPQA circulant).**

*The circulant matrix C(theta) has eigenvalues:*

```
lambda_0 = e^theta           (exponential growth)
lambda_1 = e^{j*theta}       (unit circle, |lambda|=1)
lambda_2 = e^{-theta}        (exponential decay)
lambda_3 = e^{-j*theta}      (unit circle, |lambda|=1)
```

*with corresponding eigenvectors w_p = (1, j^p, j^{2p}, j^{3p})/2,*
*p = 0, 1, 2, 3, where j = sqrt(-1).*

**Proof.** For a circulant with first row (a, b, c, d), the eigenvalues are
lambda_p = a + b*omega^p + c*omega^{2p} + d*omega^{3p} where omega = e^{2*pi*i/4} = j.

For C(theta) with first row (u_theta, y_theta, v_theta, x_theta):

```
lambda_0 = u + y + v + x = e^theta    (definition of quaternary expansion)
lambda_1 = u + j*y - v - j*x = (u-v) + j(y-... wait
```

Actually, let me recalculate. The first row of C is (u2, y2, v2, x2), so the
eigenvalues are:

```
lambda_p = u2 + y2*j^p + v2*j^{2p} + x2*j^{3p}
```

For p=0: u2 + y2 + v2 + x2 = e^theta ✓
For p=1: u2 + j*y2 - v2 - j*x2 = (u2 - v2) + j(y2 - x2) = cos(theta) - j*sin(theta) = e^{-j*theta}

Hmm wait, let me recheck. (u - v) = cos(theta), (x - y) = sin(theta),
(y - x) = -sin(theta). So:

lambda_1 = (u2 - v2) + j(y2 - x2) = cos(theta) + j(-sin(theta)) = e^{-j*theta}

For p=2: u2 - y2 + v2 - x2 = (u2+v2) - (x2+y2) = cosh(theta) - sinh(theta) = e^{-theta}

For p=3: u2 - j*y2 - v2 + j*x2 = (u2 - v2) + j(x2 - y2) = cos(theta) + j*sin(theta) = e^{j*theta}

So the eigenvalues are: {e^theta, e^{-j*theta}, e^{-theta}, e^{j*theta}}.

(The ordering differs from what I initially stated due to the column ordering
of the circulant, but the SET of eigenvalues is the same: {e^{+/-theta}, e^{+/-j*theta}}.)

The spectral radius is:

```
rho(C(theta)) = max(|lambda_p|) = max(e^theta, 1, e^{-theta}, 1) = e^{|theta|}
```

For theta > 0: rho = e^theta > 1.  **QED**

**Theorem A3 (DPQA chain error bound -- EXPONENTIAL GROWTH).**

*For a chain of n steps, each adding angle theta > 0, the absolute error*
*of the u-component satisfies:*

```
|epsilon_n^u| <= (7/4) * n * u * e^{n*theta}
```

*and the absolute error of the projection cos(s_n) = u_n - v_n satisfies:*

```
|epsilon_n^{u-v}| <= (7/2) * n * u * e^{n*theta}
```

**Proof.** The error propagation for the DPQA chain is:

```
e_{k+1} = C(theta) * e_k + delta_{k+1}
```

where delta_{k+1} is the new rounding error at step k+1 (from 4 multiplications
and 3 additions per component, so ~7 rounding contributions per component).

The magnitude of the new error at step k+1 is bounded by the magnitudes of
the computed values. Each product a*b contributes error |a*b|*u, and each
addition contributes error |partial_sum|*u. The total new error per component
is bounded by O(7u * component_value).

For the u-component at step k+1:

```
|delta_{k+1}^u| <= 7u * u(s_{k+1})
```

where u(s_{k+1}) = (cosh(s_{k+1}) + cos(s_{k+1}))/2.

Since the circulant C is normal (all circulants are normal), the 2-norm
||C|| = rho(C) = e^theta. The error from step k is amplified by at most
e^theta at step k+1, by at most e^{2*theta} at step k+2, etc.

After n steps:

```
|epsilon_n^u| <= sum_{k=1}^{n} e^{(n-k)*theta} * 7u * u(s_k)
```

For equal increments s_k = k*theta:

```
u(k*theta) = (cosh(k*theta) + cos(k*theta))/2 <= cosh(k*theta)/2 + 1/2
```

For large k*theta: u(k*theta) ~ e^{k*theta}/4. So:

```
|epsilon_n^u| <= 7u * sum_{k=1}^{n} e^{(n-k)*theta} * e^{k*theta}/4
              = 7u * sum_{k=1}^{n} e^{n*theta}/4
              = (7/4) * n * u * e^{n*theta}   QED
```

For the projection cos(s_n) = u_n - v_n:

```
|epsilon_n^{u-v}| <= |epsilon_n^u| + |epsilon_n^v| <= 2 * (7/4) * nu * e^{n*theta}
                   = (7/2) * nu * e^{n*theta}
```

(The subtraction rounding error adds O(u * |cos(s_n)|) which is negligible
compared to the propagated error.)  **QED**

---

### A3. Comparison: Standard vs. DPQA vs. Compensated

**Theorem A4 (Error comparison for chained angle addition).**

*For n steps of angle theta each (total angle s_n = n*theta > 0):*

| Method | Absolute error bound | Relative error (cos) | FLOPs/step |
|--------|---------------------|---------------------|------------|
| Standard rotation | 3nu | 3nu/\|cos(s_n)\| | 12 |
| DPQA cyclic conv | (7/2)nu*e^{s_n} | (7/2)nu*e^{s_n}/\|cos(s_n)\| | 28 |
| Compensated rotation | O(nu^2) | O(nu^2/\|cos(s_n)\|) | 12-42 |

*DPQA is worse than standard by factor e^{s_n} in absolute error.*
*Compensated is better than standard by factor u ~ 10^{16}.*

**Numerical examples** (u = 1.1e-16, n = 1000, theta = pi/1000):

| Total angle s_n | Standard abs err | DPQA abs err | Compensated abs err | DPQA/Standard |
|----------------|-----------------|-------------|--------------------|--------------|
| pi/2 ~ 1.57 | 3.3e-13 | 1.6e-12 | 3.6e-29 | 4.8x worse |
| pi ~ 3.14 | 3.3e-13 | 7.7e-12 | 3.6e-29 | 23x worse |
| 2*pi ~ 6.28 | 3.3e-13 | 1.8e-10 | 3.6e-29 | 535x worse |
| 10*pi ~ 31.4 | 3.3e-13 | 1.6e+1 | 3.6e-29 | 4.7e13 worse |

At s_n = 10*pi (five full rotations, 1000 steps), DPQA has absolute error ~16,
meaning the result is PURE NOISE. The standard chain retains ~13 digits of
accuracy. The compensated chain retains ~29 digits.

---

### A4. Why DPQA's "No Subtraction" Property Is Irrelevant

**The False Premise.** Round 1 argued that the subtraction in
cos(a+b) = cos(a)cos(b) - sin(a)sin(b) causes "catastrophic" error at resonance
(cos(a+b) ~ 0), and that DPQA avoids this by eliminating all subtractions.

**The Reality.** The subtraction in the rotation chain has absolute rounding error:

```
|delta_sub| = |cos(a)cos(b) - sin(a)sin(b)| * u = |cos(a+b)| * u
```

When cos(a+b) ~ 0, this error is TINY in absolute terms. The "catastrophic
cancellation" means that the RELATIVE error |delta_sub|/|cos(a+b)| is large,
but this is an inherent property of computing a near-zero value, not an
artifact of subtraction.

Furthermore, this large relative error does NOT propagate. At the next step,
the error vector (epsilon, eta) is rotated by R(theta), which preserves its
norm. The large relative error at step k becomes a modest absolute error
contribution at steps k+1, k+2, ..., because |epsilon_k| is still O(ku)
regardless of |cos(s_k)|.

**DPQA's trade-off.** DPQA eliminates O(u) subtraction errors but introduces
O(u * e^{k*theta}) growth errors. For any total angle s_n > 0, the growth
errors dominate by an exponential factor. The "cancellation-free" property is
algebraically real but numerically irrelevant.

**The deeper issue.** The quaternary representation mixes bounded (cos, sin)
and unbounded (cosh, sinh) quantities in a single vector. In the eigenspace
decomposition:

```
(u, x, v, y) = a_0*w_0 + a_1*w_1 + a_2*w_2 + a_3*w_3
```

where w_0 ~ (1,1,1,1) carries the exponential (e^t), w_1 and w_3 carry the
oscillatory (e^{jt}, e^{-jt}), and w_2 carries the inverse exponential (e^{-t}).

The projection cos(s_n) = u - v only involves w_1 and w_3 (bounded).
But rounding errors project onto ALL eigenvectors, including w_0 (exponentially
growing). The w_0 component of the error grows as e^{n*theta} per n steps.

**Crucially**: The projection (1, 0, -1, 0) IS orthogonal to (1, 1, 1, 1):

```
(1, 0, -1, 0) . (1, 1, 1, 1) = 1 + 0 - 1 + 0 = 0
```

So the exponential SIGNAL in w_0 is correctly cancelled by the projection.
But the exponential ROUNDING ERROR in w_0 is NOT cancelled, because rounding
errors are uncorrelated random perturbations. The projection reduces the
exponential error by a constant factor (not to zero).

This is analogous to computing cos(t) = Re(e^{jt}) via:
cos(t) = (e^t + e^{-t} + 2*cos(t))/4 - (e^t + e^{-t} - 2*cos(t))/4

Both terms grow as e^t/2, and their subtraction recovers cos(t). But rounding
errors proportional to e^t in each term do NOT cancel in the subtraction.

---

### A5. Can Rescaling Save DPQA?

**Question.** If we rescale (u, x, v, y) by dividing by e^{s_k} (or cosh(s_k))
at each step, does this prevent exponential error growth?

**Answer: No.** After rescaling by e^{s_k}:

```
u/e^s = (cosh(s) + cos(s))/(2*e^s) -> 1/4  as s -> infinity
v/e^s = (cosh(s) - cos(s))/(2*e^s) -> 1/4  as s -> infinity
```

The projection (u - v)/e^s = cos(s)/e^s -> 0. We now need to subtract two
values that are both ~ 1/4 to get a result ~ cos(s)/e^s ~ 0. This is the
SAME catastrophic cancellation, just rescaled.

**More fundamentally**: rescaling breaks the algebraic closure property. After
rescaling, the cyclic convolution no longer corresponds to argument addition.
The elegant Z4 algebra structure is lost.

**Verdict**: No rescaling scheme can simultaneously (a) keep components bounded,
(b) preserve algebraic closure, and (c) allow recovery of cos(s_n) without
catastrophic cancellation. This is because cos(s) is bounded while e^s is not,
and the quaternary representation encodes both.

---

## B. Operation Classification

### B1. Operations That Preserve the Lift

| # | Operation | Preserved? | Mechanism | All-positive? |
|---|-----------|-----------|-----------|---------------|
| 1 | Vector addition: (u1,...) + (u2,...) | YES | Componentwise | YES if all inputs positive |
| 2 | Scalar mult: alpha * (u,...) | YES | Componentwise | Only if alpha > 0 |
| 3 | Argument addition: t1+t2 | YES | Z4 cyclic convolution | YES for t1, t2 > 0 |
| 4 | Differentiation: d/dt | YES | Cyclic shift: (u,x,v,y) -> (y,u,x,v) | Preserved |
| 5 | Integration: int dt | YES | Cyclic shift: (u,x,v,y) -> (x,v,y,u) | Preserved |
| 6 | Integer arg mult: n*t | YES | Repeated convolution (squaring) | YES for n > 0 |

### B2. Operations That Break the Lift

| # | Operation | Preserved? | Why Not |
|---|-----------|-----------|---------|
| 7 | Pointwise mult: (u1*u2,...) | NO | Does not correspond to any standard operation (see below) |
| 8 | Composition: f(g(t)) | NO | Requires projection and re-lifting |
| 9 | Non-integer arg mult: t/2 | NO | Requires "square root" in Z4 algebra; not unique |
| 10 | Division: 1/(u,x,v,y) | NO | Would need inverse in Z4 algebra; division by near-zero |
| 11 | Nonlinear functions | NO | sin(cos(t)), exp(cos(t)), etc. require projection |

### B3. Pointwise Multiplication Analysis

Given (u1, x1, v1, y1) for t1 and (u2, x2, v2, y2) for t2, the pointwise
product (u1*u2, x1*x2, v1*v2, y1*y2) does NOT represent any standard function
of t1 and t2.

**Proof by example.** For t1 = t2 = 1:

```
u(1) = (cosh(1) + cos(1))/2 = (1.5431 + 0.5403)/2 = 1.0417
u(1)^2 = 1.0851
```

But for the argument-addition convolution (which gives t1+t2=2):

```
u(2) = (cosh(2) + cos(2))/2 = (3.7622 + (-0.4161))/2 = 1.6730
```

And for any other standard combination:

```
u(1*1) = u(1) = 1.0417  (argument multiplication)
u(0) = 1                 (argument subtraction? No, that gives different structure)
```

So u1*u2 = 1.0851 does not equal u(f(t1,t2)) for any standard function f.
The pointwise product is NOT in the image of the quaternary representation.

### B4. Composition Analysis

To compute f(g(t)) where f and g are represented in quaternary form, we would
need e^{g(t)} and its mod-4 subseries. The quaternary representation of g(t)
gives us (u_g, x_g, v_g, y_g), from which we can recover e^{g(t)} = u_g + x_g + v_g + y_g.
But to compute the mod-4 subseries of e^{g(t)}, we need the Taylor expansion
of g(t), which is NOT available from just (u_g, x_g, v_g, y_g).

**Exception**: If g(t) = alpha*t for constant alpha, then f(g(t)) = f(alpha*t),
which can be computed by re-initializing the quaternary representation with
argument alpha*t. But this requires knowing alpha and computing from scratch,
not composing two existing representations.

**Verdict**: Composition is NOT closed. The lift breaks under function composition.

### B5. Negative Arguments

For t < 0, the quaternary components are:
- u(t) = u(-t) > 0 (even function)
- x(t) = -x(-t) < 0 (odd function)
- v(t) = v(-t) > 0 (even function)
- y(t) = -y(-t) < 0 (odd function)

So x and y are NEGATIVE for t < 0. The cyclic convolution of two quaternary
vectors for negative arguments will have SOME NEGATIVE TERMS among the products,
restoring the possibility of cancellation.

The "all positive terms" property of DPQA holds ONLY for non-negative arguments.

---

## C. Kill Condition Evaluation

### K4: Mathematical Impossibility

**STATUS: FIRES (for the conditioning claim).**

The quaternary lift is algebraically closed under argument addition, differentiation,
and integration. The operations work. No mathematical impossibility in the
algebraic sense.

However, the CONDITIONING ANALYSIS proves that the lift is numerically self-defeating:

1. The circulant C(theta) has spectral radius e^theta > 1 for theta > 0.
2. Rounding errors are amplified by e^theta per step.
3. After n steps, the accumulated error is O(nu * e^{n*theta}).
4. The standard rotation has spectral radius 1 (orthogonal), with error O(nu).
5. DPQA is exponentially worse for any positive total angle.

The lift works algebraically but defeats its own purpose (conditioning improvement)
through exponential error growth. The operations "needed by candidate algorithms"
(chained argument addition) are precisely where DPQA is worst.

**Formal statement**: For any chain of n > 0 positive-angle additions with total
angle s_n > 0, DPQA's absolute error exceeds the standard rotation chain's
absolute error by a factor of at least e^{s_n}/3, which grows unboundedly.

### K5: FLOP Overhead Not Amortized

**STATUS: FIRES (by default).**

Since DPQA has WORSE conditioning than standard (not better), the 2.3x FLOP
overhead per step (28 vs 12 FLOPs) is never amortized by a conditioning advantage.
DPQA costs more AND performs worse.

The crossover point where DPQA's conditioning advantage would amortize the FLOP
overhead DOES NOT EXIST, because there is no conditioning advantage.

### K8: Float64 Overflow

**STATUS: FIRES for |t| > 710.**

The quaternary components u(t) and v(t) grow as cosh(t)/2 ~ e^{|t|}/4.
Float64 can represent values up to ~1.8e308. Overflow occurs when:

```
e^{|t|}/4 > 1.8e308
|t| > ln(7.2e308) ~ 710
```

For the standard rotation chain, cos(s_k) and sin(s_k) are always in [-1, 1].
No overflow is possible regardless of |s_k|.

**Mitigation**: Periodic rescaling (divide by e^{s_k}) is possible but:
1. Breaks the algebraic closure property
2. Requires tracking the scale factor
3. Doesn't solve the conditioning problem (see Section A5)

**For chains**: Even moderate chains overflow. A chain of 1000 steps of theta = 1
has s_n = 1000, and e^{1000} is astronomically beyond float64 range. The standard
rotation handles this trivially (all values in [-1, 1]).

---

## D. Computation Specifications for Round 4

Despite the theoretical analysis being conclusive, empirical verification should
confirm the theoretical predictions. Here are precise specifications:

### Test 1: Chained Rotation Error Growth

**Purpose**: Verify that standard error grows as O(n) and DPQA grows as O(n*e^{n*theta}).

**Setup**:
```python
theta = pi / 1000        # Small angle increment
n_max = 10000             # 10000 steps, total angle 10*pi
reference = mpmath.cos(n * theta)  # 50-digit precision reference

# Method A: Standard rotation chain
c, s = 1.0, 0.0
ct, st = cos(theta), sin(theta)
for k in range(n_max):
    c, s = c*ct - s*st, s*ct + c*st
    error_standard[k] = abs(c - float(mpmath.cos((k+1)*theta)))

# Method B: DPQA cyclic convolution chain
u, x, v, y = quaternary(0)   # = (1, 0, 0, 0)
ut, xt, vt, yt = quaternary(theta)
for k in range(n_max):
    u, x, v, y = cyclic_conv((u,x,v,y), (ut,xt,vt,yt))
    error_dpqa[k] = abs((u - v) - float(mpmath.cos((k+1)*theta)))

# Method C: Compensated rotation chain (using TwoProduct/TwoSum)
# [implement with EFT]
```

**Expected results**:
- error_standard[k] ~ 3k * 1.1e-16 (linear in k)
- error_dpqa[k] ~ 3.5k * 1.1e-16 * exp(k*theta) (exponential in k)
- At k=1000 (s=pi): standard ~3.3e-13, DPQA ~7.6e-12 (23x worse)
- At k=5000 (s=5*pi): standard ~1.65e-12, DPQA ~2.7e+4 (NOISE)
- At k=10000 (s=10*pi): standard ~3.3e-12, DPQA OVERFLOWS

### Test 2: Eigenvalue Verification

**Purpose**: Verify the spectral radius of the circulant matrix.

```python
theta = 0.1
C = circulant_matrix(quaternary(theta))  # 4x4 matrix
eigenvalues = np.linalg.eigvals(C)
print(sorted(abs(eigenvalues)))
# Expected: [e^{-0.1}, 1.0, 1.0, e^{0.1}] = [0.905, 1.0, 1.0, 1.105]
```

### Test 3: Projection Orthogonality

**Purpose**: Verify that (1,0,-1,0) is orthogonal to the exponentially growing
eigenvector (1,1,1,1).

```python
projection = np.array([1, 0, -1, 0])
exp_eigvec = np.array([1, 1, 1, 1])
print(np.dot(projection, exp_eigvec))  # Expected: 0
```

This confirms that the exponential SIGNAL cancels in the projection, but explain
why the exponential ROUNDING ERROR does not.

### Test 4: Single-Step Condition Number

**Purpose**: Verify that DPQA is cosh(t) times worse than standard for a single evaluation.

```python
for t in [0.1, 1.0, pi/2, pi, 2*pi, 5*pi]:
    # Standard: compute cos(t), sin(t) via rotation
    # DPQA: compute (u,x,v,y) via Taylor, project u-v
    # Reference: mpmath
    ratio = error_dpqa / error_standard
    print(f"t={t:.2f}: DPQA/Standard = {ratio:.1f}, cosh(t) = {cosh(t):.1f}")
    # Expected: ratio approximately equals cosh(t)
```

### Test 5: Resonance Crossing Non-Amplification

**Purpose**: Verify that passing through cos(s_k) = 0 does NOT amplify error in
the standard chain.

```python
# Chain through pi/2 (resonance) and beyond
theta = pi / 100
n_values = range(1, 200)  # s goes from pi/100 to 2*pi

for n in n_values:
    s_n = n * theta
    # Track absolute error (should be linear in n)
    # Track relative error (should spike at s_n ~ pi/2 but not propagate)
```

**Expected**: Absolute error is a straight line (linear in n). Relative error
spikes at n = 50 (s_n = pi/2) but returns to normal afterward.

### Test 6: Goertzel vs. Rotation vs. DPQA

**Purpose**: Compare error growth patterns for the Goertzel recurrence, rotation
chain, and DPQA chain.

```python
N = 1000
omega = 2*pi*7/N  # frequency bin 7
x = np.random.randn(N)  # test signal

# Method A: Goertzel (O(N^2) error growth)
# Method B: Rotation accumulation (O(N) error growth)
# Method C: DPQA accumulation (O(N*e^{N*omega}) error growth)
# Method D: numpy.fft reference
```

**Expected**: Goertzel O(N^2), Rotation O(N), DPQA O(N*e^{N*omega}) -- all worse
than FFT.

### Test 7: Compensated vs. DPQA Head-to-Head

**Purpose**: Settle the revised K7 question empirically.

```python
# Chain of n=100 steps through 2 resonance crossings
theta = pi / 50  # Total angle = 2*pi
# With FMA: compensated ~12 FLOPs, DPQA ~28 FLOPs
# Without FMA: compensated ~42 FLOPs, DPQA ~28 FLOPs
# Measure: max absolute error over the chain
```

**Expected**: Compensated wins in conditioning for ALL chain lengths. DPQA wins
in FLOPs only on non-FMA hardware AND only if you ignore that it's exponentially
less accurate.

---

## E. Salvageable Aspects of the Quaternary Framework

Despite DPQA's failure as a computational technique for chained operations,
the quaternary framework retains value in specific areas:

### E1. Conditioning Diagnostic (CONFIRMED, Round 2 H3)

The ratio cosh(t)/|cos(t)| = (u+v)/|u-v| provides a natural conditioning
indicator that can be computed from data already available in any algorithm
that tracks both cos and cosh. This doesn't require DPQA -- it requires
awareness of the gross/net relationship.

### E2. All-Four-at-Once Taylor (CONFIRMED, Round 2 H4)

The stride-4 recurrence for computing (cos, sin, cosh, sinh) simultaneously
saves 40% of Taylor series FLOPs. This is a real but niche advantage (applies
only to custom Taylor implementations, not to compiled libraries).

### E3. Interpretive Framework (CONFIRMED, prior councils)

The quaternary decomposition reveals gross/net energy structure:
- Gross = u + v = cosh (always well-conditioned)
- Net = u - v = cos (ill-conditioned near resonance)
- Ratio = cosh/|cos| = "numerical SWR"

This provides physical insight into why certain computations fail near resonance,
even though it doesn't fix the computation.

### E4. Single-Step Gross Energy Computation

For algorithms that need ONLY cosh(t) or sinh(t) (gross energy), the quaternary
approach provides these via u + v or x + y, which are sums of positive terms.
But computing cosh and sinh directly is equally well-conditioned, so there is
no advantage over standard approaches.

---

## F. The Fundamental Impossibility

**Theorem F1 (Impossibility of conditioning improvement via lifting to Z4).**

*No representation that includes the exponential e^t as a component can provide*
*better conditioning than the standard (cos, sin) representation for computing*
*cos(s_n) through a chain of argument additions.*

**Proof sketch.**

1. The quaternary representation (u, x, v, y) is the inverse DFT of
   (e^t, e^{jt}, e^{-t}, e^{-jt}).

2. Chaining via cyclic convolution is equivalent to pointwise multiplication
   in the DFT domain: lambda_p(s+theta) = lambda_p(s) * lambda_p(theta).

3. The lambda_0 = e^t component has |lambda_0| = e^theta > 1, causing
   exponential growth.

4. Any representation that includes this component carries exponentially
   growing values, with proportionally growing rounding errors.

5. Projecting to cos(s_n) requires extracting the bounded component from
   the growing representation, which recovers the signal but not the noise.

6. The standard (cos, sin) representation works ONLY in the bounded eigenspace
   (lambda_1, lambda_3), with all values in [-1, 1] and condition number 1.

**Corollary.** The only way to improve the conditioning of chained angle addition
beyond the standard rotation chain is through PRECISION EXTENSION (compensated
arithmetic, double-double, arbitrary precision), not through REPRESENTATION CHANGE.
The (cos, sin) representation is already optimal among bounded representations.

---

## G. Kill Condition Summary

| ID | Condition | Status | Evidence |
|----|-----------|--------|----------|
| K1 | No lifted computation exists | CLEAR | Operations are algebraically closed |
| K2 | Trivial advantage (<2x in all scenarios) | **FIRES** (predicted) | DPQA is WORSE, not better |
| K3 | Known published technique | CLEAR | Novel technique (confirmed Round 2) |
| **K4** | **Mathematical impossibility** | **FIRES** | **Exponential error growth; Theorem A3** |
| **K5** | **FLOP overhead not amortized** | **FIRES** | **No conditioning advantage to amortize** |
| K6 | No real algorithm chains enough ops | MOOT | No advantage at any chain length |
| K7 | Compensated arithmetic cheaper | SUPERSEDED | Compensated is better in every way |
| **K8** | **Overflow** | **FIRES for \|t\|>710** | **cosh overflows float64** |

**Three kill conditions fire (K4, K5, K8). K2 is predicted to fire in Round 4.**
**K6 and K7 are moot since DPQA has no advantage to compare against.**

---

## H. Honest Assessment

### What Rounds 1-2 Got Right

1. **Operation closure**: The cyclic convolution IS algebraically closed,
   cancellation-free, and elegant. This is real mathematics.

2. **Novelty**: The technique IS novel. No one has published Z4 cyclic convolution
   as a numerical method for chained angle addition.

3. **Structural parallels**: The analogy to homogeneous coordinates IS valid
   in structure. Both carry extra dimensions to avoid singularities.

### What Rounds 1-2 Got Wrong

1. **The central premise**: "Resonance crossings cause cascading error in the
   standard chain" is FALSE. The rotation matrix is orthogonal; errors don't
   cascade. This was assumed, not proven.

2. **The analogy depth**: Homogeneous coordinates work because ALL components
   remain bounded (the extra w coordinate doesn't grow exponentially). The
   quaternary analogy breaks precisely because the extra components DO grow
   exponentially.

3. **The FLOP comparison**: DPQA was compared to "standard" (12 FLOPs) and
   "compensated" (42 FLOPs) and found to be in between (28 FLOPs). But the
   conditioning comparison was assumed favorable for DPQA. In reality, DPQA
   has worse conditioning than BOTH alternatives.

### The Root Cause of the Error

The Round 1 analysis focused on the SINGLE-STEP condition number of the
subtraction cos(a)cos(b) - sin(a)sin(b) and correctly identified that it
diverges at resonance. But it failed to analyze how this condition number
PROPAGATES through the chain. The propagation analysis reveals that the
large condition number at a single step does NOT inject extra absolute error
into the chain, because the rotation preserves error norms.

This is a classic error in numerical analysis: confusing local condition
numbers with global error growth. The local condition number of one subtraction
can be terrible without the global error growing, if the subsequent propagation
is norm-preserving.

### The Verdict

**DPQA is a novel, algebraically elegant technique that is numerically inferior
to the standard rotation chain for every quantifiable metric.** Its value is
restricted to:

1. Interpretive insight (gross/net energy structure)
2. Stride-4 Taylor recurrence (40% FLOP savings, niche)
3. Conditioning diagnostics (cosh/|cos| ratio as health indicator)

These are the same conclusions reached by the prior councils. The lifted
representation hypothesis does NOT change this verdict. **Staying lifted is
worse than projecting**, because the lifted representation grows exponentially
while the projected representation stays bounded.

---

## Sources and Methods

- Error analysis framework: Higham, "Accuracy and Stability of Numerical
  Algorithms" (2002), Chapters 2-3 (error models), Chapter 18 (iterative methods)
- Circulant matrix eigenvalues: Davis, "Circulant Matrices" (1979)
- Compensated arithmetic: Ogita, Rump, Oishi (2005)
- Prior council results: quaternary-performance Round 4 (04-analysis.md)
- Eigenspace decomposition: verified against established quaternary identities
  (u+x+v+y = e^t, u-v = cos(t), etc.)
