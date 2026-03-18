# Round 2: IMPLEMENTATION -- Benchmark Code

**Investigation**: quaternary-performance
**Round**: 2 of 5
**Date**: 2026-03-17
**Purpose**: Write head-to-head benchmark code for all 5 hypotheses.

---

## Code Written

**File**: `src/experiments/council/quaternary_performance_benchmarks.py`

## Design Decisions

### Fair Comparison of Computational Effort

The quaternary subseries uses 30 terms per subseries. Each term has index 4k+j for j in {0,1,2,3}, so the maximum index used is 4*29+3 = 119. This means the quaternary pathway uses all exponential terms through t^119/119!.

The standard Taylor series for cos(t) uses terms at indices 0, 2, 4, ..., 2n. With 60 terms, the maximum index is 2*59 = 118. Similarly for sin, cosh, sinh.

So 30 quaternary terms ~ 60 standard terms per function. This is a fair comparison -- approximately the same number of floating-point operations.

### Two Levels of H4 Testing

1. **Taylor series level**: Both pathways implemented in pure Python with numpy vectorization. Tests whether the mathematical structure (mod-4 grouping vs mod-2 with signs) gives any intrinsic advantage.

2. **Compiled library level**: numpy's built-in cos/sin/cosh/sinh vs quaternary reconstruction from numpy. Tests whether the quaternary grouping helps when using optimized library functions.

### Ground Truth

Using mpmath at 50-digit precision. This gives about 34 digits more than float64, so any float64 error is unambiguously visible against the ground truth.

### Metrics

- **ULP error**: Units in the Last Place -- the standard metric for floating-point precision. 0 ULP = exact match, 1 ULP = off by the minimum representable difference.
- **Wall-clock time**: Using `time.perf_counter()` for microsecond resolution.
- **10 trials**: For statistical significance in timing benchmarks.

## Engines Implemented

1. `quaternary_subseries()` -- scalar, recurrence-based (no factorial overflow)
2. `standard_taylor_cos/sin/cosh/sinh()` -- scalar, recurrence-based
3. `quaternary_subseries_vectorized()` -- numpy array version
4. `standard_taylor_all_four_vectorized()` -- numpy array version
5. Ground truth via mpmath at 50 digits

## What Round 3 Will Do

Run this code and collect actual numbers. No prediction, no estimation -- real execution.
