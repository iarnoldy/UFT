#!/usr/bin/env python3
"""
Verify that quaternary 30 terms and standard 60 terms give EQUIVALENT accuracy.

This is the critical claim: the speed advantage is real only if the accuracy is matched.
If quaternary is faster but less accurate, it's just cutting corners.
"""

import numpy as np
import mpmath

mpmath.mp.dps = 50


def quaternary_subseries(t, n_terms=30):
    u, x, v, y = 1.0, t, t**2/2, t**3/6
    tu, tx, tv, ty = 1.0, t, t**2/2, t**3/6
    t4 = t**4
    for k in range(1, n_terms):
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


def standard_taylor_all(t, n_terms=60):
    t2 = t**2
    cos_val, sin_val, cosh_val, sinh_val = 0.0, 0.0, 0.0, 0.0
    cos_term, sin_term, cosh_term, sinh_term = 1.0, t, 1.0, t
    for k in range(n_terms):
        cos_val += cos_term
        sin_val += sin_term
        cosh_val += cosh_term
        sinh_val += sinh_term
        cos_term *= -t2 / ((2*k+1)*(2*k+2))
        sin_term *= -t2 / ((2*k+2)*(2*k+3))
        cosh_term *= t2 / ((2*k+1)*(2*k+2))
        sinh_term *= t2 / ((2*k+2)*(2*k+3))
    return cos_val, sin_val, cosh_val, sinh_val


def ulp_error(computed, reference):
    if reference == 0.0:
        return abs(computed) / np.finfo(np.float64).tiny if computed != 0 else 0
    return abs(computed - reference) / abs(np.spacing(reference))


print("Accuracy Verification: Quaternary (30 terms) vs Standard (60 terms)")
print("="*70)
print(f"{'t':>6s}  {'func':>5s}  {'true_val':>16s}  {'quat_ulp':>10s}  {'std_ulp':>10s}  {'same?':>6s}")

test_values = [0.1, 0.5, 1.0, 2.0, 3.7, 5.0, 8.0, 10.0, 15.0, 20.0]

for t in test_values:
    t_mp = mpmath.mpf(t)
    true_cos = float(mpmath.cos(t_mp))
    true_sin = float(mpmath.sin(t_mp))
    true_cosh = float(mpmath.cosh(t_mp))
    true_sinh = float(mpmath.sinh(t_mp))

    q_cos, q_sin, q_cosh, q_sinh = quaternary_subseries(t, 30)
    s_cos, s_sin, s_cosh, s_sinh = standard_taylor_all(t, 60)

    for name, q_val, s_val, true_val in [
        ("cos", q_cos, s_cos, true_cos),
        ("sin", q_sin, s_sin, true_sin),
        ("cosh", q_cosh, s_cosh, true_cosh),
        ("sinh", q_sinh, s_sinh, true_sinh),
    ]:
        q_ulp = ulp_error(q_val, true_val)
        s_ulp = ulp_error(s_val, true_val)
        same = "YES" if abs(q_ulp - s_ulp) < max(q_ulp, s_ulp, 1) * 0.5 + 1 else "NO"
        print(f"{t:>6.1f}  {name:>5s}  {true_val:>16.8e}  {q_ulp:>10.1f}  {s_ulp:>10.1f}  {same:>6s}")

# Also check: what's the LAST TERM magnitude for each approach?
print(f"\n\nLast term magnitude comparison:")
print(f"{'t':>6s}  {'quat_last_u':>14s}  {'std_last_cos':>14s}  {'ratio':>10s}")

for t in test_values:
    # Quaternary: last u term is t^(4*29) / (116)!
    quat_last = float(mpmath.power(t, 116) / mpmath.factorial(116))

    # Standard: last cos term is t^(2*59) / (118)!
    std_last = float(mpmath.power(t, 118) / mpmath.factorial(118))

    print(f"{t:>6.1f}  {quat_last:>14.2e}  {std_last:>14.2e}  {quat_last/(std_last+1e-300):>10.2e}")
