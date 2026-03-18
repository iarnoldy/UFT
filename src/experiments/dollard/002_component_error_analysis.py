"""
Experiment 002: Component Error Analysis of Z4 Cyclic Convolution
=================================================================

Follows from Experiment 001 (systematic n-sweep).

QUESTION: Why does u-nu = exact cos at n={400,500,600,1000} but NOT at
n={100,200,300,700,800,900}? All 10 are integer-pi multiples with cos=+-1.

APPROACH (per Ian's investigation plan):
1. Track u and nu errors SEPARATELY against mpmath true values
2. Check if error_u == error_nu at zero-error points (forced symmetry)
3. Test multiple theta values to distinguish angle vs step-count dependence

TAG: [CO] — Computational Observation. IEEE 754 interacting with Z4 structure.

IMPORTS: From canonical src/dollard_exact_construction.py (Rule 9).
REFERENCE: Pinned to float(mpmath.cos(n * theta)) where theta is float64 (Rule 10).

True component values (from DFT diagonalization of Z4 circulant):
  u_true(n*theta) = (cosh(n*theta) + cos(n*theta)) / 2
  nu_true(n*theta) = (cosh(n*theta) - cos(n*theta)) / 2
  u_true - nu_true = cos(n*theta)  [exact in exact arithmetic]
"""

import sys
import os
import json
import numpy as np
import mpmath
from datetime import datetime

# Rule 9: Import from canonical
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dollard_exact_construction import (
    dollard_quaternary_expansion,
    dollard_multiply,
    dollard_to_complex,
    dollard_gross_net,
)

mpmath.mp.dps = 50


def true_components_mpmath(n, theta):
    """
    Compute true u and nu after n Z4 multiplications using mpmath.

    From DFT diagonalization of the Z4 circulant matrix:
      u_n = (cosh(n*theta) + cos(n*theta)) / 2
      nu_n = (cosh(n*theta) - cos(n*theta)) / 2

    Uses the PINNED reference: n * theta computed in float64, then
    passed to mpmath (matching the canonical script's reference path).
    """
    # Rule 10: pinned reference — float64 product, then mpmath
    angle = n * theta  # float64 product
    cosh_val = mpmath.cosh(angle)
    cos_val = mpmath.cos(angle)
    u_true = float((cosh_val + cos_val) / 2)
    nu_true = float((cosh_val - cos_val) / 2)
    return u_true, nu_true


def run_sweep(theta, n_max, label):
    """Run component error sweep for given theta."""
    step = dollard_quaternary_expansion(theta)
    state = (1.0, 0.0, 0.0, 0.0)

    records = []

    for n in range(1, n_max + 1):
        state = dollard_multiply(state, step)

        u_computed = state[0]
        nu_computed = state[2]
        u_true, nu_true = true_components_mpmath(n, theta)

        error_u = u_computed - u_true
        error_nu = nu_computed - nu_true
        error_diff = abs(error_u - error_nu)

        # cos extraction
        cos_computed = u_computed - nu_computed
        # Rule 10: pinned reference
        cos_true = float(mpmath.cos(n * theta))
        cos_error = abs(cos_computed - cos_true)

        records.append({
            'n': n,
            'total_angle_pi': n * theta / np.pi,
            'u_computed': u_computed,
            'nu_computed': nu_computed,
            'u_true': u_true,
            'nu_true': nu_true,
            'error_u': error_u,
            'error_nu': error_nu,
            'error_u_abs': abs(error_u),
            'error_nu_abs': abs(error_nu),
            'error_diff': error_diff,
            'errors_identical': (error_u == error_nu),
            'cos_computed': cos_computed,
            'cos_true': cos_true,
            'cos_error': cos_error,
            'cos_zero_error': (cos_error == 0.0),
        })

    return records


def analyze_and_print(records, theta, label):
    """Print analysis of component errors."""
    print(f"\n{'='*110}")
    print(f"  {label}: theta = {theta:.15e} (theta/pi = {theta/np.pi:.6f})")
    print(f"{'='*110}")

    # Header
    print(f"  {'n':>5} {'err_u':>14} {'err_nu':>14} {'err_u-err_nu':>14} "
          f"{'identical?':>10} {'cos_error':>14} {'cos=0?':>6} {'angle/pi':>10}")
    print(f"  {'-'*100}")

    # Print at multiples of pi and near zero-error points
    pi_step = round(np.pi / theta)  # n steps per pi
    check_ns = set()
    for k in range(1, 11):
        base = k * pi_step
        check_ns.update([base - 1, base, base + 1])
    # Also check at half-pi multiples
    half_pi_step = round(np.pi / (2 * theta))
    for k in range(1, 21):
        check_ns.add(k * half_pi_step)
    # First few
    check_ns.update(range(1, 11))

    check_ns = sorted(n for n in check_ns if 1 <= n <= len(records))

    zero_cos_ns = []
    identical_err_ns = []

    for r in records:
        n = r['n']
        if r['cos_zero_error']:
            zero_cos_ns.append(n)
        if r['errors_identical']:
            identical_err_ns.append(n)

        if n in check_ns:
            print(f"  {n:>5} {r['error_u']:>14.6e} {r['error_nu']:>14.6e} "
                  f"{r['error_u'] - r['error_nu']:>14.6e} "
                  f"{'YES' if r['errors_identical'] else 'no':>10} "
                  f"{r['cos_error']:>14.4e} "
                  f"{'ZERO!' if r['cos_zero_error'] else '':>6} "
                  f"{r['total_angle_pi']:>10.3f}")

    print(f"\n  Zero cos-error at n: {zero_cos_ns}")
    print(f"  Identical component errors at n: {identical_err_ns[:50]}{'...' if len(identical_err_ns) > 50 else ''}")
    print(f"  Count identical: {len(identical_err_ns)}/{len(records)}")

    # Key question: at zero-cos-error points, are component errors identical?
    if zero_cos_ns:
        print(f"\n  KEY: At zero-cos-error points, are component errors identical?")
        for n in zero_cos_ns:
            r = records[n - 1]
            print(f"    n={n}: err_u={r['error_u']:.6e}, err_nu={r['error_nu']:.6e}, "
                  f"identical={r['errors_identical']}, diff={r['error_u']-r['error_nu']:.6e}")

    # At NON-zero pi multiples, what's the error difference?
    pi_multiples = [k * pi_step for k in range(1, 11) if k * pi_step <= len(records)]
    nonzero_pi = [n for n in pi_multiples if n not in zero_cos_ns]
    if nonzero_pi:
        print(f"\n  NON-ZERO pi multiples (cos=+-1 but cos_error != 0):")
        for n in nonzero_pi:
            r = records[n - 1]
            print(f"    n={n} ({r['total_angle_pi']:.1f}*pi): err_u={r['error_u']:.6e}, "
                  f"err_nu={r['error_nu']:.6e}, diff={r['error_u']-r['error_nu']:.6e}, "
                  f"cos_err={r['cos_error']:.4e}")

    return zero_cos_ns


# ========== MAIN ==========
if __name__ == "__main__":
    print("Experiment 002: Component Error Analysis")
    print("Tag: [CO] — IEEE 754 + Z4 cyclic convolution interaction")
    print()

    # === Part 1: theta = pi/100 (baseline, matches Experiment 001) ===
    theta_100 = np.pi / 100
    records_100 = run_sweep(theta_100, 1000, "pi/100")
    zeros_100 = analyze_and_print(records_100, theta_100, "BASELINE")

    # === Part 2: theta = pi/50 ===
    theta_50 = np.pi / 50
    records_50 = run_sweep(theta_50, 500, "pi/50")
    zeros_50 = analyze_and_print(records_50, theta_50, "THETA=pi/50")

    # === Part 3: theta = pi/200 ===
    theta_200 = np.pi / 200
    records_200 = run_sweep(theta_200, 2000, "pi/200")
    zeros_200 = analyze_and_print(records_200, theta_200, "THETA=pi/200")

    # === Part 4: theta = pi/1000 ===
    theta_1000 = np.pi / 1000
    records_1000 = run_sweep(theta_1000, 10000, "pi/1000")
    zeros_1000 = analyze_and_print(records_1000, theta_1000, "THETA=pi/1000")

    # === CROSS-THETA COMPARISON ===
    print(f"\n{'='*110}")
    print("CROSS-THETA COMPARISON: Are zeros at same ANGLE or same STEP COUNT?")
    print(f"{'='*110}")

    print(f"\n  theta=pi/100  (1 step = pi/100):  zeros at n={zeros_100}")
    if zeros_100:
        print(f"    -> angles: {[n * theta_100 / np.pi for n in zeros_100]} * pi")

    print(f"\n  theta=pi/50   (1 step = pi/50):   zeros at n={zeros_50}")
    if zeros_50:
        print(f"    -> angles: {[n * theta_50 / np.pi for n in zeros_50]} * pi")

    print(f"\n  theta=pi/200  (1 step = pi/200):  zeros at n={zeros_200}")
    if zeros_200:
        print(f"    -> angles: {[n * theta_200 / np.pi for n in zeros_200]} * pi")

    print(f"\n  theta=pi/1000 (1 step = pi/1000): zeros at n={zeros_1000}")
    if zeros_1000:
        angles = [n * theta_1000 / np.pi for n in zeros_1000[:20]]
        print(f"    -> angles (first 20): {angles} * pi")

    # Do the same TOTAL ANGLES appear across thetas?
    angles_100 = set(round(n * 100 / 100) for n in zeros_100) if zeros_100 else set()
    angles_50 = set(round(n * 50 / 50) for n in zeros_50) if zeros_50 else set()
    angles_200 = set(round(n * 200 / 200) for n in zeros_200) if zeros_200 else set()

    print(f"\n  Angles (as integer pi) where zero-error occurs:")
    print(f"    pi/100:  {sorted(angles_100)}")
    print(f"    pi/50:   {sorted(angles_50)}")
    print(f"    pi/200:  {sorted(angles_200)}")

    if angles_100 and angles_50:
        common = angles_100 & angles_50
        print(f"    Common (pi/100 & pi/50): {sorted(common)}")
    if angles_100 and angles_200:
        common = angles_100 & angles_200
        print(f"    Common (pi/100 & pi/200): {sorted(common)}")

    # === Save results ===
    output_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(output_dir, exist_ok=True)

    output = {
        'experiment': '002-component-error-analysis',
        'timestamp': datetime.now().isoformat(),
        'findings': {
            'zeros_pi100': zeros_100,
            'zeros_pi50': zeros_50,
            'zeros_pi200': zeros_200,
            'zeros_pi1000': zeros_1000[:100] if zeros_1000 else [],
        },
    }
    outpath = os.path.join(output_dir, f'002_component_errors_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to: {outpath}")
