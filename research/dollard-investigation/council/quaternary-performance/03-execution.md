# Round 3: EXECUTION -- Benchmark Results

**Investigation**: quaternary-performance
**Round**: 3 of 5
**Date**: 2026-03-17
**Purpose**: Run all benchmarks and collect actual numbers.

---

## Environment

- Python 3.14.0 (MSC v.1944, 64 bit)
- NumPy 2.3.5
- mpmath available (50-digit ground truth)
- Hardware: Intel i7-11800H, 64GB RAM, Windows 11

## Raw Results

### H1: Numerical Stability Near Resonance

**RESULT: Both Taylor pathways lose badly. Numpy wins every time (0 ULP error in all tests).**

The quaternary pathway (u - v) is consistently WORSE than the standard Taylor series for cos(t). Both are vastly worse than numpy's compiled cos function.

Key data points near t = pi/2 + epsilon:

| epsilon | Standard Taylor ULP | Quaternary ULP | Numpy ULP | Winner |
|---------|---------------------|----------------|-----------|--------|
| 1e-01   | 0                   | 14             | 0         | NUMPY  |
| 1e-05   | 19,106              | 134,528        | 0         | NUMPY  |
| 1e-09   | 126,013,200         | 296,101,427    | 0         | NUMPY  |
| 1e-13   | 2.76e12             | 1.27e13        | 0         | NUMPY  |

Near t = 25*pi/2 (large argument + resonance):

| epsilon | Standard Taylor ULP | Quaternary ULP | Numpy ULP | Winner |
|---------|---------------------|----------------|-----------|--------|
| 1e-01   | 1.24e16             | 7.19e15        | 0         | NUMPY  |
| 1e-05   | 3.56e19             | 2.36e21        | 0         | NUMPY  |
| 1e-13   | 1.83e19             | 3.17e20        | 0         | NUMPY  |

**Conclusion H1**: The quaternary u-v subtraction has WORSE catastrophic cancellation than the standard Taylor series near cosine zeros. Both are useless compared to numpy's compiled cos (which uses argument reduction, not naive Taylor summation). **Kill condition K2 fires: quaternary has worse stability near resonance.**

### H2: Monotone Convergence (Large Arguments)

**RESULT: Standard Taylor WINS for all t > 1. The theoretical prediction was WRONG.**

| t  | Standard Taylor ULP | Quaternary ULP | Winner |
|----|---------------------|----------------|--------|
| 1  | 1                   | 0              | QUAT   |
| 5  | 9                   | 167            | STD    |
| 10 | 1,372               | 21,729         | STD    |
| 20 | 10,273,857          | 694,462,527    | STD    |
| 30 | 2.12e12             | 1.60e13        | STD    |
| 50 | 3.16e20             | 1.18e22        | STD    |

**Why the prediction failed**: The theoretical argument was that monotone convergence (no alternating signs) avoids internal cancellation within each subseries. This is TRUE -- u(t) and v(t) are each computed accurately. But the FINAL step u - v reintroduces catastrophic cancellation, and it is WORSE than the standard Taylor series because u and v grow as cosh(t)/2 while cos(t) stays bounded. The cancellation is not avoided, only postponed to the last step, where it is amplified by the exponential growth of the hyperbolic functions.

The standard cosine Taylor series has alternating-sign cancellation, but the partial sums oscillate around the true value and the maximum intermediate term grows polynomially (roughly t^t for the peak term), not exponentially. The quaternary's u and v grow as cosh(t)/2 ~ e^t/4, which is worse.

**Conclusion H2**: Quaternary is WORSE for large arguments. The monotone convergence of the subseries is real but irrelevant because the final subtraction u - v has exponentially growing condition number.

### H3: Resonance Early Warning

**RESULT: QUATERNARY WINS -- the ratio |u-v|/(u+v) fires EARLIER at every threshold.**

| Threshold | Standard horizon | Quaternary horizon | Earlier |
|-----------|-----------------|-------------------|---------|
| 0.100     | 0.100           | 0.209             | QUAT    |
| 0.050     | 0.050           | 0.113             | QUAT    |
| 0.010     | 0.010           | 0.025             | QUAT    |
| 0.005     | 0.005           | 0.012             | QUAT    |
| 0.001     | 0.001           | 0.002             | QUAT    |

The quaternary detector fires roughly 2-2.5x earlier than the standard detector at every threshold level. This is because |cos(t)|/cosh(t) decays faster than |cos(t)| alone, since cosh(t) > 1 for all t != 0.

**However**: This is mathematically trivial. The "quaternary" detector is just |cos(t)|/cosh(t), which decays faster purely because of the cosh(t) denominator. You could define ANY such ratio without the quaternary framework. The early warning is real but not attributable to the quaternary decomposition in any meaningful way.

**Conclusion H3**: Advantage is real but trivial. Dividing by cosh(t) makes any signal decay faster. Not a genuine quaternary contribution.

### H4: All-Four-at-Once Efficiency

**RESULT: SPLIT VERDICT.**

**Taylor series level: QUATERNARY WINS by 40-50%.**

| Array size | Quaternary (ms) | Standard (ms) | Ratio | Winner |
|------------|-----------------|---------------|-------|--------|
| scalar     | 19.6 us         | 31.9 us       | 0.614 | QUAT   |
| 100        | 0.21            | 0.43          | 0.478 | QUAT   |
| 1,000      | 0.35            | 0.68          | 0.514 | QUAT   |
| 10,000     | 1.54            | 2.52          | 0.612 | QUAT   |
| 100,000    | 19.89           | 32.78         | 0.607 | QUAT   |

**Why**: The quaternary pathway computes 4 subseries with 30 terms each (120 multiplications total) in a SINGLE loop. The standard pathway computes 4 separate series with 60 terms each (240 multiplications total). Even though they use the same total number of Taylor terms, the quaternary loop iterates 30 times and updates 4 accumulators, while the standard must run 4 separate 60-term loops. The quaternary approach does fewer loop iterations and fewer recurrence multiplications.

This is a real algorithmic advantage: grouping by mod-4 reduces the number of recurrence steps by 2x (each recurrence step advances by 4 indices instead of 2).

**Compiled library level: NUMPY WINS by 25-75%.**

| Array size | 4x Numpy (ms) | Quat-from-numpy (ms) | Ratio | Winner |
|------------|---------------|----------------------|-------|--------|
| 100        | 0.022         | 0.039                | 1.759 | NUMPY  |
| 1,000      | 0.024         | 0.036                | 1.507 | NUMPY  |
| 10,000     | 0.230         | 0.283                | 1.231 | NUMPY  |
| 100,000    | 2.196         | 3.026                | 1.378 | NUMPY  |

**Why**: The "quaternary from numpy" approach STILL calls all four numpy functions AND then does additional arithmetic (4 additions, 4 divisions, 4 more additions/subtractions). It strictly does MORE work than the direct numpy approach. This was predicted in Round 1.

**Conclusion H4**: The quaternary Taylor loop is genuinely faster (2x fewer recurrence steps for equivalent accuracy). But this only matters if you are implementing Taylor series from scratch (custom FPGA, embedded systems, neural network kernels). For standard scientific computing with library functions, there is no advantage.

### H5: Gradient Flow Properties

**RESULT: NO MEANINGFUL ADVANTAGE.**

For small-to-moderate t, quaternary and standard are comparable (0-37 ULP). For large t (t=50), both Taylor approaches completely fail due to the same large-argument instability from H2. Finite differences actually win at t=50 (because they use numpy's compiled cos internally).

Second derivatives: mathematically identical computation. No structural advantage from quaternary decomposition.

**Conclusion H5**: No advantage. The cyclic derivative structure d(u)/dt = y, d(v)/dt = x is elegant but computationally identical to the standard derivative chain.

---

## Kill Condition Evaluation

| Kill ID | Condition | Status |
|---------|-----------|--------|
| K1 | Quaternary uniformly slower for all array sizes in H4 | **DID NOT FIRE** -- quaternary is faster for Taylor series |
| K2 | Quaternary has worse stability near resonance (H1) | **FIRES** -- quaternary ULP error is consistently higher |
| K3 | No measurable advantage on any hypothesis | **DID NOT FIRE** -- H4 Taylor shows real advantage |
| CONTINUE | Any hypothesis shows >5% improvement | **FIRES** -- H4 Taylor shows 40-50% improvement |

**K2 fires but K1/K3 do not. CONTINUE condition also fires.** The investigation continues to Round 4 because there ARE measurable advantages, even though some hypotheses failed.

---

## Results File

Full JSON data saved to: `src/experiments/results/quaternary_performance_results.json`
