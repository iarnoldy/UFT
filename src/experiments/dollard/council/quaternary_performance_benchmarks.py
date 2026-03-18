#!/usr/bin/env python3
"""
Quaternary Computational Engine -- Performance Benchmarks
==========================================================

Investigation: quaternary-performance (Research Council)
Date: 2026-03-17

Tests 5 hypotheses about whether the quaternary pathway (u, x, v, y subseries)
has different computational properties from the standard pathway (cos, sin, cosh, sinh).

Requires: numpy, mpmath, time, json
Optional: matplotlib (for figures)

Usage:
    python quaternary_performance_benchmarks.py
"""

import numpy as np
import time
import json
import sys
import os
from math import factorial
from pathlib import Path

# Try importing mpmath for arbitrary precision ground truth
try:
    import mpmath
    mpmath.mp.dps = 50  # 50 decimal digits
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    print("WARNING: mpmath not available. Ground truth will use numpy (limited precision).")

# Try importing matplotlib for figures
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("WARNING: matplotlib not available. Figures will be skipped.")


# ============================================================================
# CORE ENGINES
# ============================================================================

def quaternary_subseries(t, n_terms=30):
    """
    Compute u, x, v, y via their mod-4 Taylor subseries.

    u(t) = sum_{k=0}^{n_terms-1} t^{4k} / (4k)!
    x(t) = sum_{k=0}^{n_terms-1} t^{4k+1} / (4k+1)!
    v(t) = sum_{k=0}^{n_terms-1} t^{4k+2} / (4k+2)!
    y(t) = sum_{k=0}^{n_terms-1} t^{4k+3} / (4k+3)!

    All terms are positive for t > 0.
    Returns (u, x, v, y).
    """
    u = 0.0
    x = 0.0
    v = 0.0
    y = 0.0
    for k in range(n_terms):
        # Compute t^(4k+j) / (4k+j)! using progressive multiplication
        # to avoid overflow in factorial
        if k == 0:
            term_u = 1.0  # t^0 / 0! = 1
            term_x = t    # t^1 / 1! = t
            term_v = t**2 / 2.0  # t^2 / 2!
            term_y = t**3 / 6.0  # t^3 / 3!
        else:
            # From previous k, multiply by t^4 / ((4k)(4k-1)(4k-2)(4k-3))
            # for u: t^(4(k-1)) / (4(k-1))! * t^4 / (4k * (4k-1) * (4k-2) * (4k-3))
            n4k = 4 * k
            factor = t**4 / (n4k * (n4k - 1) * (n4k - 2) * (n4k - 3))
            term_u *= factor
            # For x: similar factor but shifted
            n4k1 = 4 * k + 1
            factor_x = t**4 / (n4k1 * (n4k1 - 1) * (n4k1 - 2) * (n4k1 - 3))
            term_x *= factor_x
            # For v:
            n4k2 = 4 * k + 2
            factor_v = t**4 / (n4k2 * (n4k2 - 1) * (n4k2 - 2) * (n4k2 - 3))
            term_v *= factor_v
            # For y:
            n4k3 = 4 * k + 3
            factor_y = t**4 / (n4k3 * (n4k3 - 1) * (n4k3 - 2) * (n4k3 - 3))
            term_y *= factor_y
        u += term_u
        x += term_x
        v += term_v
        y += term_y
    return u, x, v, y


def standard_taylor_cos(t, n_terms=60):
    """Compute cos(t) via standard alternating Taylor series with same effective terms."""
    result = 0.0
    term = 1.0  # t^0 / 0!
    for k in range(n_terms):
        result += term
        # Next term: multiply by -t^2 / ((2k+1)(2k+2))
        term *= -t**2 / ((2 * k + 1) * (2 * k + 2))
    return result


def standard_taylor_sin(t, n_terms=60):
    """Compute sin(t) via standard alternating Taylor series."""
    result = 0.0
    term = t  # t^1 / 1!
    for k in range(n_terms):
        result += term
        term *= -t**2 / ((2 * k + 2) * (2 * k + 3))
    return result


def standard_taylor_cosh(t, n_terms=60):
    """Compute cosh(t) via standard Taylor series (all positive)."""
    result = 0.0
    term = 1.0
    for k in range(n_terms):
        result += term
        term *= t**2 / ((2 * k + 1) * (2 * k + 2))
    return result


def standard_taylor_sinh(t, n_terms=60):
    """Compute sinh(t) via standard Taylor series (all positive)."""
    result = 0.0
    term = t
    for k in range(n_terms):
        result += term
        term *= t**2 / ((2 * k + 2) * (2 * k + 3))
    return result


def quaternary_to_standard(u, x, v, y):
    """Convert quaternary (u,x,v,y) to standard (cos, sin, cosh, sinh)."""
    return u - v, x - y, u + v, x + y


# ============================================================================
# VECTORIZED ENGINES (for H4 numpy benchmarks)
# ============================================================================

def quaternary_subseries_vectorized(t_array, n_terms=30):
    """
    Vectorized quaternary subseries computation.
    t_array: numpy array of values.
    Returns (u, x, v, y) as numpy arrays.
    """
    u = np.ones_like(t_array, dtype=np.float64)
    x = t_array.copy()
    v = t_array**2 / 2.0
    y = t_array**3 / 6.0

    term_u = np.ones_like(t_array, dtype=np.float64)
    term_x = t_array.copy()
    term_v = t_array**2 / 2.0
    term_y = t_array**3 / 6.0

    t4 = t_array**4

    for k in range(1, n_terms):
        n4k = 4 * k
        term_u *= t4 / (n4k * (n4k - 1) * (n4k - 2) * (n4k - 3))
        u += term_u

        n4k1 = 4 * k + 1
        term_x *= t4 / (n4k1 * (n4k1 - 1) * (n4k1 - 2) * (n4k1 - 3))
        x += term_x

        n4k2 = 4 * k + 2
        term_v *= t4 / (n4k2 * (n4k2 - 1) * (n4k2 - 2) * (n4k2 - 3))
        v += term_v

        n4k3 = 4 * k + 3
        term_y *= t4 / (n4k3 * (n4k3 - 1) * (n4k3 - 2) * (n4k3 - 3))
        y += term_y

    return u, x, v, y


def standard_taylor_all_four_vectorized(t_array, n_terms=60):
    """
    Vectorized standard Taylor computation of cos, sin, cosh, sinh.
    """
    cos_val = np.ones_like(t_array, dtype=np.float64)
    sin_val = t_array.copy()
    cosh_val = np.ones_like(t_array, dtype=np.float64)
    sinh_val = t_array.copy()

    t2 = t_array**2

    cos_term = np.ones_like(t_array, dtype=np.float64)
    sin_term = t_array.copy()
    cosh_term = np.ones_like(t_array, dtype=np.float64)
    sinh_term = t_array.copy()

    for k in range(1, n_terms):
        cos_term *= -t2 / ((2*k - 1) * (2*k))
        cos_val += cos_term

        sin_term *= -t2 / ((2*k) * (2*k + 1))
        sin_val += sin_term

        cosh_term *= t2 / ((2*k - 1) * (2*k))
        cosh_val += cosh_term

        sinh_term *= t2 / ((2*k) * (2*k + 1))
        sinh_val += sinh_term

    return cos_val, sin_val, cosh_val, sinh_val


# ============================================================================
# GROUND TRUTH
# ============================================================================

def ground_truth(t):
    """Compute ground truth cos, sin, cosh, sinh using mpmath (50-digit precision)."""
    if HAS_MPMATH:
        t_mp = mpmath.mpf(t)
        return (float(mpmath.cos(t_mp)), float(mpmath.sin(t_mp)),
                float(mpmath.cosh(t_mp)), float(mpmath.sinh(t_mp)))
    else:
        return np.cos(t), np.sin(t), np.cosh(t), np.sinh(t)


def ground_truth_uxvy(t):
    """Compute ground truth u, x, v, y using mpmath."""
    if HAS_MPMATH:
        t_mp = mpmath.mpf(t)
        cos_t = mpmath.cos(t_mp)
        sin_t = mpmath.sin(t_mp)
        cosh_t = mpmath.cosh(t_mp)
        sinh_t = mpmath.sinh(t_mp)
        u = (cosh_t + cos_t) / 2
        x = (sinh_t + sin_t) / 2
        v = (cosh_t - cos_t) / 2
        y = (sinh_t - sin_t) / 2
        return float(u), float(x), float(v), float(y)
    else:
        cos_t, sin_t, cosh_t, sinh_t = np.cos(t), np.sin(t), np.cosh(t), np.sinh(t)
        return ((cosh_t + cos_t)/2, (sinh_t + sin_t)/2,
                (cosh_t - cos_t)/2, (sinh_t - sin_t)/2)


def ulp_error(computed, reference):
    """Compute error in ULPs (Units in the Last Place)."""
    if reference == 0.0:
        if computed == 0.0:
            return 0.0
        return abs(computed) / np.finfo(np.float64).tiny
    return abs(computed - reference) / abs(np.spacing(reference))


def relative_error(computed, reference):
    """Compute relative error, handling zero reference."""
    if reference == 0.0:
        return abs(computed)
    return abs(computed - reference) / abs(reference)


# ============================================================================
# H1: NUMERICAL STABILITY NEAR RESONANCE
# ============================================================================

def benchmark_h1_stability():
    """
    H1: Compare precision of cos(t) computed via:
      (a) Standard Taylor series
      (b) Quaternary: u - v
      (c) numpy cos (as baseline)
    near resonance (t ~ pi/2, 5*pi/2, 9*pi/2).
    """
    print("\n" + "="*70)
    print("H1: NUMERICAL STABILITY NEAR RESONANCE")
    print("="*70)

    results = {}

    # Test near multiple zeros of cosine
    resonance_points = [np.pi/2, 5*np.pi/2, 9*np.pi/2, 25*np.pi/2]
    epsilons = [1e-1, 1e-3, 1e-5, 1e-7, 1e-9, 1e-11, 1e-13]

    for t0 in resonance_points:
        results[f"t0={t0:.4f}"] = {}
        print(f"\n--- Near t = {t0:.4f} (= {t0/np.pi:.1f}*pi) ---")
        print(f"  {'epsilon':>12s}  {'cos_true':>14s}  {'std_taylor_err':>14s}  {'quat_err':>14s}  {'numpy_err':>14s}  {'winner':>10s}")

        for eps in epsilons:
            t = t0 + eps

            # Ground truth
            cos_true, sin_true, cosh_true, sinh_true = ground_truth(t)

            # Standard Taylor (60 terms = same computational effort as 30 quaternary terms)
            cos_std = standard_taylor_cos(t, n_terms=60)

            # Quaternary
            u, x, v, y = quaternary_subseries(t, n_terms=30)
            cos_quat = u - v

            # Numpy
            cos_np = np.cos(t)

            # Errors in ULPs
            err_std = ulp_error(cos_std, cos_true)
            err_quat = ulp_error(cos_quat, cos_true)
            err_np = ulp_error(cos_np, cos_true)

            winner = "EQUAL"
            if err_std < err_quat and err_std < err_np:
                winner = "STD_TAYLOR"
            elif err_quat < err_std and err_quat < err_np:
                winner = "QUATERNARY"
            elif err_np < err_std and err_np < err_quat:
                winner = "NUMPY"

            print(f"  {eps:>12.1e}  {cos_true:>14.6e}  {err_std:>14.1f}  {err_quat:>14.1f}  {err_np:>14.1f}  {winner:>10s}")

            results[f"t0={t0:.4f}"][f"eps={eps}"] = {
                "cos_true": cos_true,
                "err_std_ulp": err_std,
                "err_quat_ulp": err_quat,
                "err_numpy_ulp": err_np,
                "winner": winner
            }

    return results


# ============================================================================
# H2: MONOTONE CONVERGENCE
# ============================================================================

def benchmark_h2_monotone_convergence():
    """
    H2: For large |t|, compare precision of:
      (a) Standard Taylor cos(t) -- alternating signs, internal cancellation
      (b) Quaternary u, v computed separately (monotone), then cos = u - v

    The key test: for large t, the standard series has massive internal
    cancellation. The quaternary subseries have no internal cancellation.
    """
    print("\n" + "="*70)
    print("H2: MONOTONE CONVERGENCE (LARGE ARGUMENT STABILITY)")
    print("="*70)

    results = {}

    # Test at increasing values of |t|
    test_values = [1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0]
    n_terms_quat = 40  # 40 quaternary terms = terms up to index 4*39+3 = 159
    n_terms_std = 80   # 80 standard terms = terms up to index 2*79 = 158 (comparable)

    print(f"\n  {'t':>6s}  {'cos_true':>14s}  {'std_taylor_err':>14s}  {'quat_err':>14s}  {'max_std_term':>14s}  {'max_u_term':>14s}  {'winner':>10s}")

    for t in test_values:
        cos_true = ground_truth(t)[0]

        # Standard Taylor
        cos_std = standard_taylor_cos(t, n_terms=n_terms_std)

        # Quaternary
        u, x, v, y = quaternary_subseries(t, n_terms=n_terms_quat)
        cos_quat = u - v

        # Compute max intermediate term for standard cosine series
        max_std_term = 0.0
        term = 1.0
        for k in range(n_terms_std):
            max_std_term = max(max_std_term, abs(term))
            term *= -t**2 / ((2*k + 1) * (2*k + 2))

        # Compute max intermediate term for u subseries
        max_u_term = 0.0
        term = 1.0
        for k in range(n_terms_quat):
            max_u_term = max(max_u_term, abs(term))
            if k > 0:
                n4k = 4*k
                term *= t**4 / (n4k * (n4k-1) * (n4k-2) * (n4k-3))
            else:
                term = t**4 / 24.0  # First non-trivial term

        err_std = ulp_error(cos_std, cos_true)
        err_quat = ulp_error(cos_quat, cos_true)

        winner = "EQUAL"
        if err_std < err_quat * 0.5:
            winner = "STD"
        elif err_quat < err_std * 0.5:
            winner = "QUAT"

        print(f"  {t:>6.1f}  {cos_true:>14.6e}  {err_std:>14.1f}  {err_quat:>14.1f}  {max_std_term:>14.2e}  {max_u_term:>14.2e}  {winner:>10s}")

        results[f"t={t}"] = {
            "cos_true": cos_true,
            "err_std_ulp": err_std,
            "err_quat_ulp": err_quat,
            "max_std_intermediate": max_std_term,
            "max_u_intermediate": max_u_term,
            "digits_at_risk_std": np.log10(max_std_term / (abs(cos_true) + 1e-300)) if cos_true != 0 else float('inf'),
            "winner": winner
        }

    return results


# ============================================================================
# H3: RESONANCE EARLY WARNING
# ============================================================================

def benchmark_h3_early_warning():
    """
    H3: Compare resonance detection via:
      (a) |cos(t)| < threshold
      (b) |u-v|/(u+v) < threshold

    At what distance from resonance does each detector fire?
    """
    print("\n" + "="*70)
    print("H3: RESONANCE EARLY WARNING")
    print("="*70)

    results = {}
    threshold = 0.01  # Resonance warning threshold

    # Approach resonance at t = pi/2 from below
    t_values = np.linspace(0.0, np.pi/2, 10000)

    cos_vals = np.cos(t_values)
    cosh_vals = np.cosh(t_values)

    # Standard detector: |cos(t)| < threshold
    std_detection_idx = np.where(np.abs(cos_vals) < threshold)[0]
    std_first = t_values[std_detection_idx[0]] if len(std_detection_idx) > 0 else None

    # Quaternary detector: |cos(t)|/cosh(t) < threshold
    # NOTE: This is mathematically |u-v|/(u+v)
    quat_ratio = np.abs(cos_vals) / cosh_vals
    quat_detection_idx = np.where(quat_ratio < threshold)[0]
    quat_first = t_values[quat_detection_idx[0]] if len(quat_detection_idx) > 0 else None

    print(f"\n  Threshold: {threshold}")
    print(f"  Standard detector |cos(t)| < {threshold}:")
    print(f"    First fires at t = {std_first:.6f}" if std_first else "    Never fires")
    print(f"    Distance to resonance: {np.pi/2 - std_first:.6f}" if std_first else "")
    print(f"  Quaternary detector |u-v|/(u+v) < {threshold}:")
    print(f"    First fires at t = {quat_first:.6f}" if quat_first else "    Never fires")
    print(f"    Distance to resonance: {np.pi/2 - quat_first:.6f}" if quat_first else "")

    # Compare at multiple thresholds
    thresholds = [0.1, 0.05, 0.01, 0.005, 0.001]
    print(f"\n  {'threshold':>10s}  {'std_fires_at':>14s}  {'quat_fires_at':>14s}  {'std_horizon':>14s}  {'quat_horizon':>14s}  {'earlier':>10s}")

    for th in thresholds:
        std_idx = np.where(np.abs(cos_vals) < th)[0]
        quat_idx = np.where(quat_ratio < th)[0]

        std_t = t_values[std_idx[0]] if len(std_idx) > 0 else None
        quat_t = t_values[quat_idx[0]] if len(quat_idx) > 0 else None

        std_horizon = np.pi/2 - std_t if std_t else 0
        quat_horizon = np.pi/2 - quat_t if quat_t else 0

        earlier = "EQUAL"
        if std_horizon > quat_horizon * 1.01:
            earlier = "STD"
        elif quat_horizon > std_horizon * 1.01:
            earlier = "QUAT"

        print(f"  {th:>10.4f}  {std_t:>14.6f}  {quat_t:>14.6f}  {std_horizon:>14.6f}  {quat_horizon:>14.6f}  {earlier:>10s}")

        results[f"threshold={th}"] = {
            "std_fires_at": std_t,
            "quat_fires_at": quat_t,
            "std_horizon": std_horizon,
            "quat_horizon": quat_horizon,
            "earlier": earlier
        }

    return results


# ============================================================================
# H4: ALL-FOUR-AT-ONCE EFFICIENCY
# ============================================================================

def benchmark_h4_efficiency():
    """
    H4: Wall-clock time for computing all four functions:
      (a) Standard Taylor: compute cos, sin, cosh, sinh via their series
      (b) Quaternary Taylor: compute u, x, v, y, then add/subtract
      (c) Numpy: call np.cos, np.sin, np.cosh, np.sinh
      (d) Quaternary from numpy: compute u,v,x,y from numpy trig, then return

    Tests both Taylor-level and compiled-library-level.
    """
    print("\n" + "="*70)
    print("H4: ALL-FOUR-AT-ONCE EFFICIENCY")
    print("="*70)

    results = {}
    n_trials = 10

    # --- Part A: Taylor series comparison (scalar) ---
    print("\n--- Part A: Taylor Series (scalar, single value) ---")

    t_test = 3.7  # Arbitrary test value
    n_terms_quat = 30
    n_terms_std = 60  # Comparable total terms

    # Warm up
    _ = quaternary_subseries(t_test, n_terms_quat)
    _ = standard_taylor_cos(t_test, n_terms_std)

    # Quaternary Taylor
    times_quat = []
    for _ in range(n_trials):
        start = time.perf_counter()
        for _j in range(1000):
            u, x, v, y = quaternary_subseries(t_test, n_terms_quat)
            cos_t, sin_t, cosh_t, sinh_t = quaternary_to_standard(u, x, v, y)
        elapsed = (time.perf_counter() - start) / 1000
        times_quat.append(elapsed)

    # Standard Taylor
    times_std = []
    for _ in range(n_trials):
        start = time.perf_counter()
        for _j in range(1000):
            cos_t = standard_taylor_cos(t_test, n_terms_std)
            sin_t = standard_taylor_sin(t_test, n_terms_std)
            cosh_t = standard_taylor_cosh(t_test, n_terms_std)
            sinh_t = standard_taylor_sinh(t_test, n_terms_std)
        elapsed = (time.perf_counter() - start) / 1000
        times_std.append(elapsed)

    mean_quat = np.mean(times_quat)
    mean_std = np.mean(times_std)

    print(f"  Quaternary Taylor (30 terms): {mean_quat*1e6:.1f} +/- {np.std(times_quat)*1e6:.1f} us")
    print(f"  Standard Taylor (60 terms):   {mean_std*1e6:.1f} +/- {np.std(times_std)*1e6:.1f} us")
    print(f"  Ratio (quat/std): {mean_quat/mean_std:.3f}")

    results["taylor_scalar"] = {
        "quat_mean_us": mean_quat * 1e6,
        "quat_std_us": np.std(times_quat) * 1e6,
        "std_mean_us": mean_std * 1e6,
        "std_std_us": np.std(times_std) * 1e6,
        "ratio": mean_quat / mean_std,
        "winner": "QUATERNARY" if mean_quat < mean_std else "STANDARD"
    }

    # --- Part B: Taylor series comparison (vectorized, arrays) ---
    print("\n--- Part B: Taylor Series (vectorized numpy arrays) ---")

    array_sizes = [100, 1000, 10000, 100000]

    for size in array_sizes:
        t_array = np.linspace(0.1, 10.0, size)

        # Warm up
        _ = quaternary_subseries_vectorized(t_array, n_terms_quat)
        _ = standard_taylor_all_four_vectorized(t_array, n_terms_std)

        # Quaternary vectorized
        times_qv = []
        for _ in range(n_trials):
            start = time.perf_counter()
            u, x, v, y = quaternary_subseries_vectorized(t_array, n_terms_quat)
            cos_v = u - v
            sin_v = x - y
            cosh_v = u + v
            sinh_v = x + y
            elapsed = time.perf_counter() - start
            times_qv.append(elapsed)

        # Standard vectorized
        times_sv = []
        for _ in range(n_trials):
            start = time.perf_counter()
            cos_v, sin_v, cosh_v, sinh_v = standard_taylor_all_four_vectorized(t_array, n_terms_std)
            elapsed = time.perf_counter() - start
            times_sv.append(elapsed)

        mean_qv = np.mean(times_qv)
        mean_sv = np.mean(times_sv)

        print(f"  Array size {size:>7d}: Quat {mean_qv*1e3:.2f}ms  Std {mean_sv*1e3:.2f}ms  Ratio {mean_qv/mean_sv:.3f}  {'QUAT' if mean_qv < mean_sv else 'STD'}")

        results[f"taylor_vec_{size}"] = {
            "quat_mean_ms": mean_qv * 1e3,
            "std_mean_ms": mean_sv * 1e3,
            "ratio": mean_qv / mean_sv,
            "winner": "QUATERNARY" if mean_qv < mean_sv else "STANDARD"
        }

    # --- Part C: Numpy compiled function comparison ---
    print("\n--- Part C: Numpy Compiled Functions (arrays) ---")

    for size in array_sizes:
        t_array = np.linspace(0.1, 10.0, size)

        # Method 1: Four separate numpy calls
        times_np4 = []
        for _ in range(n_trials):
            start = time.perf_counter()
            cos_v = np.cos(t_array)
            sin_v = np.sin(t_array)
            cosh_v = np.cosh(t_array)
            sinh_v = np.sinh(t_array)
            elapsed = time.perf_counter() - start
            times_np4.append(elapsed)

        # Method 2: Compute u,v,x,y from numpy, then combine
        # u = (cosh + cos)/2, v = (cosh - cos)/2, etc.
        times_npq = []
        for _ in range(n_trials):
            start = time.perf_counter()
            cos_v = np.cos(t_array)
            cosh_v = np.cosh(t_array)
            sin_v = np.sin(t_array)
            sinh_v = np.sinh(t_array)
            # Reconstruct as if from quaternary
            u = (cosh_v + cos_v) / 2
            v = (cosh_v - cos_v) / 2
            x = (sinh_v + sin_v) / 2
            y = (sinh_v - sin_v) / 2
            # Convert back
            cos_out = u - v  # = cos
            sin_out = x - y  # = sin
            cosh_out = u + v  # = cosh
            sinh_out = x + y  # = sinh
            elapsed = time.perf_counter() - start
            times_npq.append(elapsed)

        # Method 3: Just compute cos and cosh, derive sin/sinh via identity
        # sin = sqrt(1 - cos^2) [sign ambiguity], sinh = sqrt(cosh^2 - 1) [sign]
        # This is a potential optimization: 2 function calls instead of 4
        times_np2 = []
        for _ in range(n_trials):
            start = time.perf_counter()
            cos_v = np.cos(t_array)
            cosh_v = np.cosh(t_array)
            # Derive the other two -- but this requires knowing the sign of sin/sinh
            # For fair comparison, just measure the 2-call approach
            sin_v = np.sin(t_array)  # Still need this for sign
            sinh_v = np.sinh(t_array)
            elapsed = time.perf_counter() - start
            times_np2.append(elapsed)

        mean_np4 = np.mean(times_np4)
        mean_npq = np.mean(times_npq)

        print(f"  Array size {size:>7d}: 4xNumpy {mean_np4*1e3:.3f}ms  Quat-from-numpy {mean_npq*1e3:.3f}ms  Ratio {mean_npq/mean_np4:.3f}  {'SLOWER' if mean_npq > mean_np4 else 'FASTER'}")

        results[f"numpy_{size}"] = {
            "numpy_4calls_ms": mean_np4 * 1e3,
            "quat_from_numpy_ms": mean_npq * 1e3,
            "ratio": mean_npq / mean_np4,
            "winner": "NUMPY_DIRECT" if mean_np4 < mean_npq else "QUAT_FROM_NUMPY"
        }

    return results


# ============================================================================
# H5: GRADIENT FLOW PROPERTIES
# ============================================================================

def benchmark_h5_gradient():
    """
    H5: Compare autodiff properties.

    Since pytorch may not be available, we test:
    (a) Manual gradient computation stability
    (b) Finite difference gradient accuracy
    """
    print("\n" + "="*70)
    print("H5: GRADIENT FLOW PROPERTIES")
    print("="*70)

    results = {}

    # Test: compute d(cos(t))/dt = -sin(t) via two methods
    # (a) Standard: directly compute -sin(t)
    # (b) Quaternary: compute du/dt - dv/dt = y - x = -(x - y) = -sin(t)
    #     where du/dt = y, dv/dt = x (from the cyclic derivative relations)

    test_points = [0.1, 1.0, np.pi/2, 3.0, 10.0, 50.0]

    print(f"\n  {'t':>8s}  {'true_deriv':>14s}  {'std_err_ulp':>14s}  {'quat_err_ulp':>14s}  {'fd_err_ulp':>14s}  {'winner':>10s}")

    for t in test_points:
        # Ground truth: -sin(t)
        true_deriv = -float(mpmath.sin(mpmath.mpf(t))) if HAS_MPMATH else -np.sin(t)

        # Standard: -sin via Taylor
        std_deriv = -standard_taylor_sin(t, n_terms=60)

        # Quaternary: du/dt = y, dv/dt = x, so d(cos)/dt = y - x = -sin
        u, x, v, y = quaternary_subseries(t, n_terms=30)
        quat_deriv = y - x  # = -(x - y) = -sin(t)

        # Finite difference (for comparison)
        h = 1e-8
        fd_deriv = (np.cos(t + h) - np.cos(t - h)) / (2 * h)

        err_std = ulp_error(std_deriv, true_deriv)
        err_quat = ulp_error(quat_deriv, true_deriv)
        err_fd = ulp_error(fd_deriv, true_deriv)

        winner = "EQUAL"
        if err_std < err_quat * 0.5 and err_std < err_fd * 0.5:
            winner = "STD"
        elif err_quat < err_std * 0.5 and err_quat < err_fd * 0.5:
            winner = "QUAT"
        elif err_fd < err_std * 0.5 and err_fd < err_quat * 0.5:
            winner = "FD"

        print(f"  {t:>8.2f}  {true_deriv:>14.6e}  {err_std:>14.1f}  {err_quat:>14.1f}  {err_fd:>14.1f}  {winner:>10s}")

        results[f"t={t}"] = {
            "true_deriv": true_deriv,
            "err_std_ulp": err_std,
            "err_quat_ulp": err_quat,
            "err_fd_ulp": err_fd,
            "winner": winner
        }

    # Also test: does the quaternary form give any advantage for second derivatives?
    # d2(cos)/dt2 = -cos(t)
    # Quaternary: d2(u-v)/dt2 = d(y-x)/dt = v - u = -(u - v) = -cos(t)
    # Same computation, same result.
    print("\n  Second derivative test: d2(cos)/dt2 = -cos(t)")
    print("  Quaternary: d(y-x)/dt = dv/dt - du/dt... wait, du/dt = y, dv/dt = x")
    print("  Actually: d(y-x)/dt = dy/dt - dx/dt = v - u = -(u-v) = -cos(t)")
    print("  This is exactly the same computation. No advantage.")
    results["second_derivative"] = "IDENTICAL_COMPUTATION"

    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*70)
    print("QUATERNARY COMPUTATIONAL ENGINE -- PERFORMANCE BENCHMARKS")
    print("="*70)
    print(f"Date: 2026-03-17")
    print(f"Python: {sys.version}")
    print(f"Numpy: {np.__version__}")
    print(f"mpmath: {'available (50 digits)' if HAS_MPMATH else 'NOT AVAILABLE'}")
    print(f"matplotlib: {'available' if HAS_MATPLOTLIB else 'NOT AVAILABLE'}")
    print()

    all_results = {}

    # Run all benchmarks
    all_results["H1_stability"] = benchmark_h1_stability()
    all_results["H2_monotone"] = benchmark_h2_monotone_convergence()
    all_results["H3_early_warning"] = benchmark_h3_early_warning()
    all_results["H4_efficiency"] = benchmark_h4_efficiency()
    all_results["H5_gradient"] = benchmark_h5_gradient()

    # Save results
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    results_file = results_dir / "quaternary_performance_results.json"

    # Convert numpy types for JSON serialization
    def convert_numpy(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_numpy(i) for i in obj]
        return obj

    with open(results_file, 'w') as f:
        json.dump(convert_numpy(all_results), f, indent=2)

    print(f"\n\nResults saved to: {results_file}")

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    # H1 summary
    h1_wins = {"QUATERNARY": 0, "STD_TAYLOR": 0, "NUMPY": 0, "EQUAL": 0}
    for t_key in all_results["H1_stability"]:
        for eps_key in all_results["H1_stability"][t_key]:
            w = all_results["H1_stability"][t_key][eps_key]["winner"]
            h1_wins[w] = h1_wins.get(w, 0) + 1
    print(f"\n  H1 (Stability): Wins -- Quat={h1_wins.get('QUATERNARY',0)} Std={h1_wins.get('STD_TAYLOR',0)} Numpy={h1_wins.get('NUMPY',0)} Equal={h1_wins.get('EQUAL',0)}")

    # H2 summary
    h2_wins = {"QUAT": 0, "STD": 0, "EQUAL": 0}
    for key in all_results["H2_monotone"]:
        w = all_results["H2_monotone"][key]["winner"]
        h2_wins[w] = h2_wins.get(w, 0) + 1
    print(f"  H2 (Monotone):  Wins -- Quat={h2_wins.get('QUAT',0)} Std={h2_wins.get('STD',0)} Equal={h2_wins.get('EQUAL',0)}")

    # H3 summary
    h3_all_equal = all(
        all_results["H3_early_warning"][k]["earlier"] == "EQUAL"
        for k in all_results["H3_early_warning"]
    )
    print(f"  H3 (Early Warning): {'All thresholds EQUAL' if h3_all_equal else 'Differences found'}")

    # H4 summary
    h4_taylor = all_results["H4_efficiency"].get("taylor_scalar", {})
    print(f"  H4 (Efficiency):")
    print(f"    Taylor scalar: {h4_taylor.get('winner', 'N/A')} (ratio {h4_taylor.get('ratio', 'N/A'):.3f})" if h4_taylor else "    Taylor scalar: N/A")
    for size in [100, 1000, 10000, 100000]:
        key = f"taylor_vec_{size}"
        if key in all_results["H4_efficiency"]:
            d = all_results["H4_efficiency"][key]
            print(f"    Taylor vec {size}: {d['winner']} (ratio {d['ratio']:.3f})")
        key = f"numpy_{size}"
        if key in all_results["H4_efficiency"]:
            d = all_results["H4_efficiency"][key]
            print(f"    Numpy {size}: {d['winner']} (ratio {d['ratio']:.3f})")

    # H5 summary
    h5_wins = {"STD": 0, "QUAT": 0, "FD": 0, "EQUAL": 0}
    for key in all_results["H5_gradient"]:
        if key == "second_derivative":
            continue
        w = all_results["H5_gradient"][key]["winner"]
        h5_wins[w] = h5_wins.get(w, 0) + 1
    print(f"  H5 (Gradient):  Wins -- Quat={h5_wins.get('QUAT',0)} Std={h5_wins.get('STD',0)} FD={h5_wins.get('FD',0)} Equal={h5_wins.get('EQUAL',0)}")

    return all_results


if __name__ == "__main__":
    main()
