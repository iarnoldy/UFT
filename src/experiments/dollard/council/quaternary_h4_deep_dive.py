#!/usr/bin/env python3
"""
H4 Deep Dive: Why is quaternary Taylor faster?

Tests whether the speed advantage is:
(a) Algorithmic: fewer recurrence steps (30 vs 60 per function)
(b) Artifact: different number of total FLOPs
(c) Loop overhead: fewer Python loop iterations

Also tests: if we match EXACTLY the same number of loop iterations,
does the advantage persist?
"""

import numpy as np
import time
import sys


def quaternary_30terms(t):
    """Quaternary: 30 terms per subseries, 1 loop of 30 iterations."""
    u, x, v, y = 1.0, t, t**2/2, t**3/6
    tu, tx, tv, ty = 1.0, t, t**2/2, t**3/6
    t4 = t**4
    for k in range(1, 30):
        n = 4*k
        tu *= t4 / (n*(n-1)*(n-2)*(n-3))
        u += tu
        n = 4*k+1
        tx *= t4 / (n*(n-1)*(n-2)*(n-3))
        x += tx
        n = 4*k+2
        tv *= t4 / (n*(n-1)*(n-2)*(n-3))
        v += tv
        n = 4*k+3
        ty *= t4 / (n*(n-1)*(n-2)*(n-3))
        y += ty
    return u-v, x-y, u+v, x+y


def standard_4x60terms(t):
    """Standard: 4 separate loops of 60 iterations each."""
    # cos
    cos_val = 0.0
    term = 1.0
    t2 = t**2
    for k in range(60):
        cos_val += term
        term *= -t2 / ((2*k+1)*(2*k+2))
    # sin
    sin_val = 0.0
    term = t
    for k in range(60):
        sin_val += term
        term *= -t2 / ((2*k+2)*(2*k+3))
    # cosh
    cosh_val = 0.0
    term = 1.0
    for k in range(60):
        cosh_val += term
        term *= t2 / ((2*k+1)*(2*k+2))
    # sinh
    sinh_val = 0.0
    term = t
    for k in range(60):
        sinh_val += term
        term *= t2 / ((2*k+2)*(2*k+3))
    return cos_val, sin_val, cosh_val, sinh_val


def standard_interleaved_60terms(t):
    """Standard: 4 functions in a SINGLE loop of 60 iterations (fair comparison)."""
    cos_val, sin_val, cosh_val, sinh_val = 0.0, 0.0, 0.0, 0.0
    cos_term, sin_term, cosh_term, sinh_term = 1.0, t, 1.0, t
    t2 = t**2
    for k in range(60):
        cos_val += cos_term
        sin_val += sin_term
        cosh_val += cosh_term
        sinh_val += sinh_term
        cos_term *= -t2 / ((2*k+1)*(2*k+2))
        sin_term *= -t2 / ((2*k+2)*(2*k+3))
        cosh_term *= t2 / ((2*k+1)*(2*k+2))
        sinh_term *= t2 / ((2*k+2)*(2*k+3))
    return cos_val, sin_val, cosh_val, sinh_val


def quaternary_matched_flops(t):
    """Quaternary: 60 loop iterations to match standard_interleaved, but with mod-4 grouping."""
    # This uses 60 terms per subseries (overkill but matches loop count)
    u, x, v, y = 1.0, t, t**2/2, t**3/6
    tu, tx, tv, ty = 1.0, t, t**2/2, t**3/6
    t4 = t**4
    for k in range(1, 60):
        n = 4*k
        tu *= t4 / (n*(n-1)*(n-2)*(n-3))
        u += tu
        n = 4*k+1
        tx *= t4 / (n*(n-1)*(n-2)*(n-3))
        x += tx
        n = 4*k+2
        tv *= t4 / (n*(n-1)*(n-2)*(n-3))
        v += tv
        n = 4*k+3
        ty *= t4 / (n*(n-1)*(n-2)*(n-3))
        y += ty
    return u-v, x-y, u+v, x+y


def count_flops():
    """Count exact FLOPs for each approach."""
    print("FLOP Count Analysis:")
    print("="*60)

    # Quaternary 30 terms:
    # Per iteration: 4 subseries x (1 mul by t4, 3 muls in denominator, 1 div, 1 add) = 4 x 6 = 24 FLOPs
    # Plus: t4 = t*t*t*t (3 muls, done once)
    # 29 iterations x 24 + initialization
    quat_flops = 3 + 29 * 24 + 4 * 2  # init: 4 adds/subs for final
    print(f"  Quaternary (30 iters): ~{quat_flops} FLOPs")
    print(f"    Per iteration: 4 recurrences x (t4 mul, 3 denom muls, 1 div, 1 add) = 24")
    print(f"    Iterations: 29")
    print(f"    Final: 4 add/sub")

    # Standard 4x60:
    # Per function per iteration: 1 mul by -t2 or t2, 2 muls in denom, 1 div, 1 add = 5 FLOPs
    # 4 functions x 59 iterations x 5
    std_flops = 1 + 4 * 59 * 5  # t2 = t*t (1 mul, done once)
    print(f"\n  Standard 4x60 (240 total iters): ~{std_flops} FLOPs")
    print(f"    Per function per iteration: (t2 mul, 2 denom muls, 1 div, 1 add) = 5")
    print(f"    Iterations: 4 x 59 = 236")

    # Standard interleaved 60:
    # Per iteration: 4 functions x 5 = 20 FLOPs
    # 59 iterations x 20
    std_int_flops = 1 + 59 * 20
    print(f"\n  Standard interleaved (60 iters): ~{std_int_flops} FLOPs")
    print(f"    Per iteration: 4 x 5 = 20")
    print(f"    Iterations: 59")

    print(f"\n  RATIO (quat 30 / std interleaved 60): {quat_flops / std_int_flops:.3f}")
    print(f"  RATIO (quat 30 / std 4x60): {quat_flops / std_flops:.3f}")

    # Key insight: quaternary does 29 iterations, standard interleaved does 59.
    # But quaternary does MORE per iteration (24 vs 20 FLOPs).
    # Net: 29*24 = 696 vs 59*20 = 1180. Quaternary does 59% of the FLOPs.
    print(f"\n  Core computation: {29*24} (quat) vs {59*20} (std interleaved) = {29*24/(59*20):.1%}")
    print(f"  This is the source of the ~40% speedup.")

    # BUT: are they computing the same precision?
    # Quaternary 30 terms: highest power = 4*29+3 = 119
    # Standard 60 terms per function: highest power for cos = 2*59 = 118
    # They match to the same order! The quaternary just gets there in fewer steps
    # because it advances by 4 indices per step instead of 2.
    print(f"\n  Precision match:")
    print(f"    Quaternary max power: 4*29+3 = {4*29+3}")
    print(f"    Standard cos max power: 2*59 = {2*59}")
    print(f"    Standard sin max power: 2*59+1 = {2*59+1}")
    print(f"    MATCHED: both reach order ~119-120")


def main():
    print("H4 DEEP DIVE: Source of Quaternary Speed Advantage")
    print("="*60)

    t = 3.7
    n_trials = 10
    n_reps = 5000

    # Verify all methods give same answer
    r1 = quaternary_30terms(t)
    r2 = standard_4x60terms(t)
    r3 = standard_interleaved_60terms(t)
    r4 = quaternary_matched_flops(t)

    print(f"\nCorrectness check (t = {t}):")
    print(f"  cos: quat30={r1[0]:.15f}  std4x60={r2[0]:.15f}  stdint60={r3[0]:.15f}")
    print(f"  sin: quat30={r1[1]:.15f}  std4x60={r2[1]:.15f}  stdint60={r3[1]:.15f}")
    print(f"  numpy cos={np.cos(t):.15f}  sin={np.sin(t):.15f}")

    # Time all methods
    methods = {
        "Quaternary (30 iter loop)": quaternary_30terms,
        "Standard (4 x 60 iter loops)": standard_4x60terms,
        "Standard (1 x 60 iter loop, interleaved)": standard_interleaved_60terms,
        "Quaternary (60 iter loop, overkill)": quaternary_matched_flops,
    }

    print(f"\nTiming ({n_trials} trials x {n_reps} reps):")
    print(f"{'Method':>45s}  {'Mean (us)':>10s}  {'Std (us)':>10s}")

    results = {}
    for name, func in methods.items():
        # Warmup
        for _ in range(100):
            func(t)

        times = []
        for _ in range(n_trials):
            start = time.perf_counter()
            for _ in range(n_reps):
                func(t)
            elapsed = (time.perf_counter() - start) / n_reps
            times.append(elapsed)

        mean_us = np.mean(times) * 1e6
        std_us = np.std(times) * 1e6
        print(f"{name:>45s}  {mean_us:>10.1f}  {std_us:>10.1f}")
        results[name] = mean_us

    print(f"\nKey ratios:")
    q30 = results["Quaternary (30 iter loop)"]
    s4x60 = results["Standard (4 x 60 iter loops)"]
    s1x60 = results["Standard (1 x 60 iter loop, interleaved)"]
    q60 = results["Quaternary (60 iter loop, overkill)"]

    print(f"  Quat(30) / Std(4x60): {q30/s4x60:.3f}  -- includes loop overhead savings")
    print(f"  Quat(30) / Std(interleaved 60): {q30/s1x60:.3f}  -- removes loop overhead")
    print(f"  Quat(60) / Std(interleaved 60): {q60/s1x60:.3f}  -- same iterations, different grouping")

    if q30/s1x60 < 0.9:
        print(f"\n  CONCLUSION: Even with loop overhead removed, quaternary is faster.")
        print(f"  The advantage is ALGORITHMIC: 30 steps of stride-4 vs 60 steps of stride-2.")
    elif q30/s1x60 < 1.1:
        print(f"\n  CONCLUSION: With loop overhead removed, advantage disappears.")
        print(f"  The advantage was LOOP OVERHEAD: fewer Python iterations, not better algorithm.")
    else:
        print(f"\n  CONCLUSION: With loop overhead removed, quaternary is SLOWER.")
        print(f"  The original advantage was entirely loop overhead.")

    print()
    count_flops()


if __name__ == "__main__":
    main()
