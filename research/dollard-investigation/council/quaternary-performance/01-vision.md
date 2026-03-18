# Round 1: VISION -- Theoretical Analysis of Quaternary Computational Properties

**Investigation**: quaternary-performance
**Round**: 1 of 5
**Date**: 2026-03-17
**Purpose**: Before writing any code, analyze what theoretical grounds exist for the quaternary pathway having different computational properties from the standard pathway.

---

## Background

The quaternary expansion decomposes the exponential e^t into four mod-4 subseries:

```
u(t) = sum_{n=0}^{inf} t^{4n} / (4n)!        (terms 0, 4, 8, 12, ...)
x(t) = sum_{n=0}^{inf} t^{4n+1} / (4n+1)!    (terms 1, 5, 9, 13, ...)
v(t) = sum_{n=0}^{inf} t^{4n+2} / (4n+2)!    (terms 2, 6, 10, 14, ...)
y(t) = sum_{n=0}^{inf} t^{4n+3} / (4n+3)!    (terms 3, 7, 11, 15, ...)
```

For real positive t, ALL terms in ALL four subseries are POSITIVE. The standard trig/hyperbolic functions are recovered by:

```
cos(t)  = u - v
sin(t)  = x - y
cosh(t) = u + v
sinh(t) = x + y
```

The prior council established this is the Z4 group algebra acting on the exponential series -- identical algebra, potentially different computational pathway.

---

## Hypothesis-by-Hypothesis Theoretical Analysis

### H1: Numerical Stability Near Resonance

**Theoretical prediction: MIXED -- quaternary is WORSE for cos/sin computation, but provides useful intermediate quantities.**

Near t = pi/2, cos(t) ~ 0. In the quaternary pathway, cos(t) = u(t) - v(t) where both u and v are large positive numbers (u(pi/2) ~ 1.32, v(pi/2) ~ 1.32). This is CATASTROPHIC CANCELLATION -- subtracting two nearly-equal numbers to get a small result. The standard Taylor series for cos(t) also has alternating signs, but those cancel progressively and the partial sums oscillate around the true value.

However, the standard pathway computing cos(t) directly via its Taylor series also suffers from alternating-sign cancellation for large |t|. The key question is: which cancellation is worse?

For the standard cosine Taylor series at t = pi/2:
cos(pi/2) = 1 - (pi/2)^2/2 + (pi/2)^4/24 - ...

The partial sums oscillate: 1, -0.23, 0.02, ... converging to 0.

For the quaternary pathway:
u(pi/2) = 1 + (pi/2)^4/24 + (pi/2)^8/40320 + ...
v(pi/2) = (pi/2)^2/2 + (pi/2)^6/720 + ...
cos(pi/2) = u - v

Both u and v grow with |t|. The relative precision of u - v depends on the condition number |u+v|/|u-v| = cosh(t)/|cos(t)|, which diverges at the zeros of cosine. This is EXACTLY the resonance condition.

**Key insight**: The condition number cosh(t)/|cos(t)| tells us precisely how many digits of precision we lose in the subtraction u - v. Near t = pi/2, cosh(pi/2) ~ 2.51, so we lose about 0.4 digits. Near t = 5*pi/2, cosh(5*pi/2) ~ 2334, so we lose about 3.4 digits. The standard cosine series also loses precision for large arguments, but through a different mechanism.

**Testable prediction**: For moderate |t| (say |t| < 10), the precision loss from u-v cancellation should be measurable but small. For large |t| (say |t| > 50), it could become significant.

### H2: Monotone Convergence

**Theoretical prediction: REAL ADVANTAGE for summation stability, but modest.**

The standard cosine series has alternating signs: 1, -(pi/2)^2/2, +(pi/2)^4/24, ... Each term changes sign. For large |t|, intermediate terms can be enormous (the maximum term of cos(t) series occurs around n ~ t^2/2), and the final sum is small, meaning there is massive cancellation within the series.

The quaternary subseries u(t) = 1 + t^4/24 + t^8/40320 + ... has ALL POSITIVE terms. The partial sums are monotonically increasing and bounded by cosh(t). No internal cancellation occurs. The sum is always moving in one direction toward its limit.

This means:
- Forward summation of u(t) is numerically stable (no cancellation)
- Forward summation of cos(t) = 1 - t^2/2 + ... has cancellation for large |t|
- The cancellation happens ONCE (u - v) rather than at EVERY term

For |t| up to ~10, the maximum term in the cosine series is modest and this advantage is negligible. For |t| > 50, the maximum term in cos(t) can exceed 10^40, while the final answer is O(1), losing ~40 digits. The quaternary subseries u(t) still has no internal cancellation -- all the cancellation is concentrated in the single final subtraction u - v.

**Testable prediction**: For large |t|, computing u and v via their monotone series and then subtracting should give BETTER precision than directly summing the alternating cosine series. The advantage should scale with |t|.

### H3: Resonance Early Warning

**Theoretical prediction: GENUINE but TRIVIAL advantage.**

The ratio |u-v|/(u+v) = |cos(t)|/cosh(t) is a smoothly-decaying envelope. Near resonance (cos(t) -> 0), this ratio approaches 0. As a resonance detector, it gives a smooth, monotone-ish signal.

But |cos(t)| itself is also a perfectly good resonance detector. The ratio |cos(t)|/cosh(t) just re-normalizes by cosh(t), which is a monotonically increasing function of |t|. This is not fundamentally new information.

The ONLY scenario where the quaternary form adds value is if you ALREADY have u and v computed (from the quaternary engine) and want to check for resonance WITHOUT computing cos(t). In that case, checking |u-v|/(u+v) is equivalent. But this is circular -- you need the quaternary engine to get u,v.

**Testable prediction**: The early-warning horizon should be IDENTICAL because the information content is the same. The quaternary form is just a re-expression.

### H4: All-Four-at-Once Efficiency

**Theoretical prediction: DEPENDS ON IMPLEMENTATION LEVEL.**

**Taylor series level**: Computing u, x, v, y via their subseries requires evaluating terms at indices 4n, 4n+1, 4n+2, 4n+3 -- the SAME total terms as computing cos, sin, cosh, sinh individually. Actually, if you compute all four standard functions via Taylor series, you compute the SAME individual terms and then combine differently:
- cos = even terms with alternating signs
- cosh = even terms with all positive signs
- sin = odd terms with alternating signs
- sinh = odd terms with all positive signs

So the quaternary pathway groups terms into mod-4 classes, while the standard pathway groups into even/odd with sign patterns. The total floating-point operations should be essentially IDENTICAL.

One potential difference: the quaternary pathway uses only additions (all terms positive within each subseries), while the standard pathway uses additions and subtractions (alternating signs). On modern hardware, addition and subtraction have identical latency, so this should not matter for speed -- only for numerical stability (H2).

**Compiled library level**: Calling np.cos, np.sin, np.cosh, np.sinh invokes highly optimized C library functions (usually Intel MKL or similar). Each call has overhead: function dispatch, memory traversal, SIMD setup. If a single function could compute all four simultaneously, it would save 3x of this overhead.

But numpy does NOT have a "compute all four trig/hyp functions at once" function. The quaternary pathway would need to be implemented as a custom function. Unless that custom function is also compiled and SIMD-optimized, it will be SLOWER than four numpy calls.

**Testable prediction**:
- Taylor series: quaternary should be approximately equal in speed, possibly slightly faster due to simpler addition pattern.
- Numpy calls: quaternary will be SLOWER because it cannot compete with compiled vectorized library functions.

### H5: Gradient Flow Properties

**Theoretical prediction: NO ADVANTAGE for autodiff.**

The derivatives of the quaternary functions cycle:
```
du/dt = y, dx/dt = u, dv/dt = x, dy/dt = v
```

This is a cyclic permutation -- the Jacobian is a permutation matrix times appropriate factors. For autodiff, the backward pass through u-v to get cos(t) requires:
```
d(cos)/dt = du/dt - dv/dt = y - x = -sin(t)
```

This is exactly the same computation as the standard d(cos)/dt = -sin(t). The quaternary decomposition does not change the computational graph in a way that helps autodiff. The gradients are the same functions, just re-expressed.

The ONLY potential advantage would be if computing all four gradients simultaneously has the same "all-four-at-once" benefit as H4. But this reduces to H4.

**Testable prediction**: No measurable difference in autodiff timing or precision.

---

## Structural Requirements for the Benchmarks

1. **Fair comparison**: Both pathways must compute to the SAME precision target (not "compute until tolerance" which advantages one pathway).
2. **Controlled variables**: Same hardware, same number of series terms, same array sizes.
3. **Multiple regimes**: Small |t| (< 1), moderate |t| (1-10), large |t| (10-100), very large |t| (100+).
4. **Reference values**: Use mpmath with 50+ digits as the ground truth.
5. **Statistical rigor**: At least 10 trials per benchmark, report mean and std.

## Summary of Predictions

| Hypothesis | Predicted Outcome | Confidence |
|------------|-------------------|------------|
| H1: Stability near resonance | Quaternary WORSE (catastrophic cancellation in u-v) | 80% |
| H2: Monotone convergence | Quaternary BETTER for large |t| (no internal cancellation) | 75% |
| H3: Early warning | IDENTICAL (same information content) | 90% |
| H4: All-four efficiency (Taylor) | Approximately EQUAL | 85% |
| H4: All-four efficiency (numpy) | Quaternary SLOWER | 95% |
| H5: Gradient flow | NO DIFFERENCE | 90% |

The honest expectation: the quaternary pathway offers a modest advantage for H2 (large-argument stability) and is otherwise equivalent or slightly worse. This would be a null result for practical computing but an interesting numerical analysis observation.

---

## Kill Conditions Identified

From the charter:
- K1: Uniformly slower for all array sizes → STOP
- K2: Worse stability near resonance → STOP on stability claim
- K3: No measurable advantage on any hypothesis → STOP, report null

Additional kill condition identified by this analysis:
- K4: If the H2 advantage only manifests for |t| > 100 where double precision is already exhausted anyway → the advantage is real but useless

## Recommended Search Directions for Round 2

1. Implement both pathways as pure Python (for direct comparison) and numpy-vectorized
2. Use mpmath for ground truth at arbitrary precision
3. Focus most effort on H2 (most likely to show a real effect) and H4 (most practically relevant)
4. Don't over-invest in H3 and H5 (likely null results, but still test them honestly)
