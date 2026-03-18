# Round 5: SYNTHESIS -- Final Assessment

**Investigation**: quaternary-performance
**Round**: 5 of 5
**Date**: 2026-03-17
**Purpose**: Integrate all rounds into a final verdict on the quaternary computational pathway.

---

## What We Asked

Does the quaternary computational pathway -- computing u, x, v, y as four mod-4 subseries -- have different performance characteristics than the standard pathway of computing cos, sin, cosh, sinh directly?

## What We Found

### The Answer is: Yes, but mostly for the worse.

The quaternary pathway has exactly ONE computational advantage and THREE computational disadvantages relative to standard approaches.

### The Advantage: Stride-4 Recurrence (H4)

When implementing Taylor series from scratch, the mod-4 grouping allows each recurrence step to advance by 4 indices instead of 2. This means:

- 30 quaternary iterations cover the same Taylor order as 60 standard iterations
- Net FLOP savings: ~40% (696 vs 1180 core FLOPs for order-120 computation)
- Measured speedup: 0.60x (quaternary takes 60% of standard time) consistently across scalar and vectorized implementations

This is a genuine algorithmic property. It is not a Python artifact -- the FLOP count confirms it. The mod-4 grouping is computationally more efficient than the mod-2 grouping used by standard trig/hyp Taylor series because each recurrence step does proportionally more work per index advanced.

**Significance**: Niche. This matters ONLY when:
1. You implement Taylor series yourself (not using library functions)
2. You need all four trig/hyp functions simultaneously
3. You are in a context where 40% FLOP savings matters (embedded, FPGA, custom GPU kernels)

For standard scientific computing with numpy/BLAS libraries, this advantage does not apply.

### The Disadvantages

**1. Catastrophic cancellation for trig outputs (H1, H2)**

Computing cos(t) = u - v and sin(t) = x - y involves subtracting two quantities that both grow as cosh(t)/2 ~ e^t/4, to produce a result bounded by 1. The condition number is cosh(t)/|cos(t)|, which grows exponentially with t and diverges at the zeros of cosine.

Measured penalty:
- At t = 5: 19x worse ULP error than standard Taylor
- At t = 10: 16x worse
- At t = 20: 68x worse

The standard Taylor cosine series also has cancellation (alternating signs), but its condition number grows polynomially, not exponentially. The quaternary "trades" distributed cancellation (many small subtractions) for concentrated cancellation (one catastrophic subtraction), and the concentrated form is worse.

This is the most important finding of the investigation. The monotone convergence of each subseries (u, v, x, y) is real -- they DO each converge without internal cancellation. But this advantage is completely overwhelmed by the single final subtraction, which concentrates ALL the cancellation into the worst possible form.

**2. No advantage for compiled library functions (H4 Part C)**

The quaternary-from-numpy approach is 25-75% SLOWER than direct numpy calls because it does strictly more work (4 function calls + 12 arithmetic operations vs 4 function calls).

**3. No gradient flow advantage (H5)**

The cyclic derivative structure is mathematically elegant but computationally identical to standard derivatives. It changes the labeling, not the computation.

### The Trivial Finding: Early Warning (H3)

The quaternary ratio |u-v|/(u+v) = |cos(t)|/cosh(t) detects resonance 2-2.5x earlier than |cos(t)| alone. This is mathematically correct but trivial: dividing by cosh(t) > 1 makes any quantity smaller, so the threshold is crossed earlier. This is a property of normalization, not of the quaternary decomposition.

## Revised Understanding of the Quaternary Pathway

The prior council (dollard-pure-construction) established that the quaternary decomposition IS the Z4 group algebra acting on the exponential series. This investigation adds:

**The Z4 structure has a computational fingerprint**: the mod-4 grouping naturally enables stride-4 recurrences, which are more efficient per iteration than stride-2 recurrences for the same convergence order. This is a real property of the algebraic structure, not an implementation accident.

**But the Z4 structure also has a computational cost**: recovering cos/sin from u-v/x-y introduces catastrophic cancellation that worsens exponentially with argument magnitude. The algebraic decomposition is "uphill" (into large-valued components) followed by "downhill" (subtraction to get small-valued results), and the round trip loses precision.

**The net assessment**: For the specific use case of computing all four functions via Taylor series at small-to-moderate arguments (|t| < 3), the quaternary pathway is faster AND accurate. For |t| > 5, the speed advantage persists but accuracy degrades. For |t| > 20, the accuracy degradation makes the results unreliable without argument reduction. For compiled-library use, there is no advantage.

## Does This Contradict the Prior Council?

No. The prior council said the quaternary decomposition IS Z4, same algebra, same results. This council says: same algebra, same results, but different computational pathway characteristics. Specifically:
- Faster to compute via Taylor series (fewer recurrence steps)
- Less accurate for trig outputs at large arguments (catastrophic cancellation in the final subtraction)
- No advantage for compiled libraries

These are engineering findings about computation, not mathematical findings about algebra. The Z4 identity is untouched.

## The 3% Uncertainty Resolution

The prior council allocated 3% uncertainty to "the possibility that the quaternary expansion has practical computational advantages in specific lossy propagation problems." This investigation finds:

- There IS a computational advantage (40% FLOP savings in Taylor series)
- It is NICHE (custom implementations only)
- It comes with an accuracy TRADE-OFF (worse for trig at large arguments)
- It does NOT extend to compiled-library use

The 3% should be resolved as: "A modest algorithmic advantage exists for custom Taylor implementations, but it does not constitute a practical advantage for standard scientific computing."
