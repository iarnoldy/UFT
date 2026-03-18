# Round 4: ANALYSIS -- Interpreting Results Against Hypotheses

**Investigation**: quaternary-performance
**Round**: 4 of 5
**Date**: 2026-03-17
**Purpose**: Rigorous interpretation of benchmark data from Round 3.

---

## Data Sources

- Main benchmarks: `src/experiments/council/quaternary_performance_benchmarks.py`
- H4 deep dive: `src/experiments/council/quaternary_h4_deep_dive.py`
- Accuracy verification: `src/experiments/council/quaternary_accuracy_verification.py`
- Results JSON: `src/experiments/results/quaternary_performance_results.json`

---

## Hypothesis-by-Hypothesis Verdict

### H1: Numerical Stability Near Resonance -- REFUTED

**Prediction (Round 1)**: Quaternary worse near resonance due to catastrophic cancellation in u - v.
**Result**: Confirmed. Quaternary is consistently worse.

Near t = pi/2 + epsilon:

| epsilon | Standard ULP | Quaternary ULP | Quaternary/Standard ratio |
|---------|-------------|----------------|--------------------------|
| 1e-3    | 56          | 844            | 15x worse                |
| 1e-7    | 329,103     | 4,626,597      | 14x worse                |
| 1e-13   | 2.76e12     | 1.27e13        | 4.6x worse               |

Near t = 25*pi/2 (large argument):

| epsilon | Standard ULP | Quaternary ULP | Quaternary/Standard ratio |
|---------|-------------|----------------|--------------------------|
| 1e-3    | 2.0e4       | 1.0e5          | 5x worse                 |
| 1e-7    | 6.9e8       | 1.1e10         | 16x worse                |

**Numpy's compiled cos achieves 0 ULP in ALL tests** because it uses Payne-Hanek argument reduction, not naive Taylor summation.

**Mathematical explanation**: The condition number of the subtraction u - v is (u+v)/|u-v| = cosh(t)/|cos(t)|. Near a zero of cosine, this diverges, causing catastrophic cancellation. The standard Taylor series for cos(t) avoids this because its partial sums oscillate around the true value rather than approaching it from one side via the difference of two large quantities.

**Kill condition K2 fires**: Quaternary has worse stability near resonance.

### H2: Monotone Convergence -- REFUTED (opposite of prediction)

**Prediction (Round 1)**: Quaternary better for large |t| because no internal cancellation.
**Result**: Quaternary is WORSE, and the gap widens with |t|.

| t   | Standard cos ULP | Quaternary cos ULP | Ratio (quat/std) |
|-----|------------------|--------------------|-------------------|
| 1   | 1                | 0                  | 0x (trivial)      |
| 5   | 9                | 167                | 19x worse         |
| 10  | 1,372            | 21,729             | 16x worse         |
| 20  | 10,273,857       | 694,462,527        | 68x worse         |
| 50  | 3.16e20          | 1.18e22            | 37x worse         |

**Why the prediction failed**: The theoretical argument was sound in isolation -- each quaternary subseries (u, v) converges monotonically with no internal cancellation. This IS true. The problem is that the accuracy of cos(t) = u - v depends not on the internal stability of u and v, but on the CONDITION NUMBER of their subtraction, which is cosh(t)/|cos(t)|. This grows exponentially with t.

The standard cosine Taylor series ALSO has cancellation (alternating signs), but its condition number is max_term/|cos(t)|, where max_term grows as ~(t^2/2)^(t^2/2e) / sqrt(pi*t^2/2e) -- polynomial in t for fixed position in the series, not exponential. The quaternary's cosh(t) ~ e^t growth is categorically worse.

**Key data from accuracy verification**: For cosh and sinh (computed via u+v and x+y, no cancellation), both methods achieve 0-3 ULP regardless of t. The problem is exclusively in the subtraction step for trig outputs.

### H3: Resonance Early Warning -- CONFIRMED but TRIVIAL

**Result**: The quaternary detector |u-v|/(u+v) fires 2-2.5x earlier than |cos(t)| at every threshold.

| Threshold | Standard horizon | Quaternary horizon | Ratio |
|-----------|-----------------|-------------------|-------|
| 0.10      | 0.100           | 0.209             | 2.1x  |
| 0.01      | 0.010           | 0.025             | 2.5x  |
| 0.001     | 0.001           | 0.002             | 2.4x  |

**Why this is trivial**: |cos(t)|/cosh(t) < threshold fires earlier than |cos(t)| < threshold because cosh(t) > 1, which shrinks the ratio. This is dividing by a number larger than 1. You could achieve the same effect by defining ANY detector |cos(t)|/f(t) where f(t) > 1. The cosh(t) factor comes naturally from the quaternary decomposition, but the early warning is a property of the normalization, not of the decomposition.

**Honest assessment**: This is real mathematics -- the quaternary form naturally provides a normalized resonance measure. But it is not a computational advantage. Anyone who knows cosh(t) could construct the same detector without the quaternary framework.

### H4: All-Four-at-Once Efficiency -- CONFIRMED with CRITICAL CAVEAT

**Taylor series level: Quaternary is 40% faster.**

| Test | Quaternary | Standard | Ratio | Winner |
|------|-----------|----------|-------|--------|
| Scalar | 11.8 us | 18.8 us | 0.63 | QUAT |
| Scalar (interleaved std) | 11.8 us | 19.6 us | 0.60 | QUAT |
| Vec 1K | 0.35 ms | 0.68 ms | 0.51 | QUAT |
| Vec 100K | 19.9 ms | 32.8 ms | 0.61 | QUAT |

**Source of advantage (deep dive)**: The quaternary recurrence advances 4 indices per step (t^4 multiplier), while the standard recurrence advances 2 indices per step (t^2 multiplier). To reach Taylor order ~120:
- Quaternary: 30 iterations x 24 FLOPs/iteration = 696 core FLOPs
- Standard: 60 iterations x 20 FLOPs/iteration = 1180 core FLOPs
- Ratio: 696/1180 = 0.59, matching the observed 0.60 ratio.

This is a genuine algorithmic difference. The mod-4 grouping allows a stride-4 recurrence that reaches the same Taylor order in half the iterations. Each quaternary iteration does 20% more work (24 vs 20 FLOPs), but there are half as many iterations, yielding a net 40% FLOP reduction.

**CRITICAL CAVEAT: Accuracy is NOT matched for trig outputs.**

From the accuracy verification:

| t | Quaternary cos ULP | Standard cos ULP | Penalty |
|---|-------------------|------------------|---------|
| 0.1-1 | 0-1 | 0-1 | None |
| 5 | 167 | 9 | 19x |
| 10 | 21,729 | 1,372 | 16x |
| 20 | 694M | 10M | 68x |

For cosh/sinh, both methods match (0-3 ULP). The speed advantage is REAL, but you pay for it with degraded cos/sin accuracy at moderate-to-large arguments.

**Compiled library level: Numpy wins.**

| Array size | 4x Numpy | Quat-from-numpy | Ratio |
|-----------|----------|-----------------|-------|
| 100 | 0.022 ms | 0.039 ms | 1.76x slower |
| 100K | 2.20 ms | 3.03 ms | 1.38x slower |

As predicted. The quaternary-from-numpy approach calls all four numpy functions AND does extra arithmetic. Strictly more work.

### H5: Gradient Flow -- REFUTED (no advantage)

The quaternary and standard pathways compute the same derivatives via the same number of operations. At small t, they are comparable (0-1 ULP each). At large t, both fail due to the same Taylor convergence issues. Finite differences (using numpy cos internally) win at large t.

The cyclic derivative structure (du/dt = y, dx/dt = u, dv/dt = x, dy/dt = v) is mathematically elegant but computationally identical to the standard derivative chain (d(cos)/dt = -sin, d(sin)/dt = cos, etc.). The quaternary form just relabels the same operations.

---

## Summary Table

| Hypothesis | Verdict | Practical Value | Confidence |
|------------|---------|-----------------|------------|
| H1: Stability near resonance | REFUTED: Quaternary worse | None (negative) | 99% |
| H2: Monotone convergence | REFUTED: Quaternary worse for trig | None for trig; neutral for hyp | 99% |
| H3: Early warning | CONFIRMED but trivial | Minimal (trivial normalization) | 95% |
| H4: Taylor efficiency | CONFIRMED: 40% fewer FLOPs | Real but comes with accuracy trade-off | 99% |
| H4: Numpy efficiency | REFUTED: Numpy faster | None (negative) | 99% |
| H5: Gradient flow | REFUTED: No advantage | None | 95% |

---

## Kill Condition Status

| ID | Fires? | Reason |
|----|--------|--------|
| K1 | NO | Quaternary Taylor IS faster |
| K2 | **YES** | Quaternary IS worse near resonance |
| K3 | NO | H4 Taylor shows >5% advantage |
| K4 (added in R1) | NO | H4 advantage exists even at small t |
| CONTINUE | **YES** | H4 Taylor shows measurable advantage |

Both K2 and CONTINUE fire. The investigation continues because there IS a real finding (H4 Taylor speed), even though the stability claims (H1, H2) are refuted.

---

## The Real Story

The quaternary decomposition has ONE genuine computational property: the mod-4 grouping enables a stride-4 recurrence that reaches a given Taylor order in half the iterations of a stride-2 recurrence, saving ~40% of FLOPs.

This advantage is PURELY about loop efficiency. It has nothing to do with:
- Numerical stability (which is worse for trig outputs)
- Resonance detection (which is a trivial normalization)
- Gradient properties (which are identical)
- Compiled library performance (which cannot be improved this way)

The stride-4 advantage is real but niche: it matters only when implementing Taylor series from scratch (embedded systems, FPGA, custom CUDA kernels) AND when you need all four trig/hyp functions simultaneously AND when you can tolerate the accuracy degradation for cos/sin at large arguments (or use argument reduction first).

For standard scientific computing, there is no advantage. Use numpy.
