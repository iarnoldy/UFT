"""
Experiment 001: Systematic N-Sweep of Dollard's Exact Z4 Construction
=====================================================================

Pre-registered: 2026-03-17 (docs/experiments/001-systematic-n-sweep.md)

Method: Run Dollard's Z4 cyclic convolution chaining for ALL n from 1 to 1000
(theta=pi/100) and compare against standard rotation, both measured against
50-digit mpmath reference.

Construction: Dollard eq 18-82 (operators preserved), chaining is [OUR APPLICATION].
Dollard Lens: ACTIVE. Source text verified for eq 67-77 (quaternary expansion).
"""

import numpy as np
import mpmath
import json
import os
from math import factorial
from datetime import datetime

mpmath.mp.dps = 50  # 50-digit reference precision


# === Dollard's quaternary expansion (eq 67-77) ===
def dollard_quaternary_expansion(theta, N_terms=40):
    """Eq (67)-(77): E^(jθ) = 1·u + j·x + h·ν + k·y"""
    u, x, nu, y = 0.0, 0.0, 0.0, 0.0
    for n in range(N_terms):
        for r in range(4):
            idx = 4 * n + r
            term = theta**idx / factorial(idx)
            if r == 0:   u += term
            elif r == 1: x += term
            elif r == 2: nu += term
            elif r == 3: y += term
    return u, x, nu, y


# === Z4 cyclic convolution multiply (from eq 63-66 operator table) ===
def dollard_multiply(elem1, elem2):
    """Z4 group algebra multiplication [OUR APPLICATION of Dollard's algebra]"""
    u1, x1, n1, y1 = elem1
    u2, x2, n2, y2 = elem2
    u3 = u1*u2 + x1*y2 + n1*n2 + y1*x2
    x3 = u1*x2 + x1*u2 + n1*y2 + y1*n2
    n3 = u1*n2 + x1*x2 + n1*u2 + y1*y2
    y3 = u1*y2 + x1*n2 + n1*x2 + y1*u2
    return (u3, x3, n3, y3)


# === Parameters ===
theta = np.pi / 100
N_MAX = 1000

# Step element
step = dollard_quaternary_expansion(theta)
ct, st = np.cos(theta), np.sin(theta)

# Initial states
state_dollard = (1.0, 0.0, 0.0, 0.0)  # identity
c_std, s_std = 1.0, 0.0                # standard rotation

# === Collect data for every n ===
results = []
zero_error_ns = []

print(f"Experiment 001: Systematic N-Sweep")
print(f"theta = pi/100 = {theta:.15f}")
print(f"Running n = 1 to {N_MAX}...")
print()
print(f"{'n':>5} {'Dollard err':>14} {'Standard err':>14} {'D/S ratio':>10} "
      f"{'cos(n*theta)':>14} {'u-nu':>18} {'zero?':>6}")
print("-" * 90)

for n in range(1, N_MAX + 1):
    # Dollard Z4 chain
    state_dollard = dollard_multiply(state_dollard, step)

    # Standard rotation chain
    c_std, s_std = c_std*ct - s_std*st, s_std*ct + c_std*st

    # 50-digit reference
    exact_cos = float(mpmath.cos(n * mpmath.mpf(str(theta))))
    exact_sin = float(mpmath.sin(n * mpmath.mpf(str(theta))))

    # Dollard cos/sin extraction (eq 80-81)
    dollard_cos = state_dollard[0] - state_dollard[2]
    dollard_sin = state_dollard[1] - state_dollard[3]

    # Errors
    err_d = abs(dollard_cos - exact_cos)
    err_s = abs(c_std - exact_cos)

    # Check if cos is exactly representable
    total_angle_over_pi = n / 100  # n * (pi/100) / pi
    is_half_int_pi = (n % 50 == 0)  # multiples of pi/2
    is_int_pi = (n % 100 == 0)      # multiples of pi

    # Record
    record = {
        'n': n,
        'total_angle_pi': n / 100,
        'dollard_error': err_d,
        'standard_error': err_s,
        'dollard_cos': dollard_cos,
        'standard_cos': c_std,
        'exact_cos': exact_cos,
        'u': state_dollard[0],
        'x': state_dollard[1],
        'nu': state_dollard[2],
        'y': state_dollard[3],
        'u_minus_nu': dollard_cos,
        'x_minus_y': dollard_sin,
        'u_plus_nu': state_dollard[0] + state_dollard[2],
        'x_plus_y': state_dollard[1] + state_dollard[3],
        'is_half_int_pi': is_half_int_pi,
        'is_int_pi': is_int_pi,
        'dollard_zero_error': (err_d == 0.0),
        'standard_zero_error': (err_s == 0.0),
    }
    results.append(record)

    if err_d == 0.0:
        zero_error_ns.append(n)

    # Print selected rows
    if n <= 10 or n % 50 == 0 or err_d == 0.0 or n in [25, 75, 99, 100, 101, 199, 200, 201, 499, 500, 501]:
        ratio_str = f"{err_d/(err_s+1e-300):.2f}x" if err_s > 0 else "---"
        zero_flag = "ZERO!" if err_d == 0.0 else ""
        print(f"{n:>5} {err_d:>14.4e} {err_s:>14.4e} {ratio_str:>10} "
              f"{exact_cos:>14.10f} {dollard_cos:>18.10f} {zero_flag:>6}")


# === Summary ===
print()
print("=" * 90)
print("SUMMARY")
print("=" * 90)

print(f"\nZero-error n values (Dollard): {zero_error_ns}")
print(f"Count: {len(zero_error_ns)}")

if zero_error_ns:
    print(f"\nAnalysis of zero-error points:")
    for n in zero_error_ns:
        total_pi = n / 100
        cos_val = float(mpmath.cos(n * mpmath.mpf(str(theta))))
        print(f"  n={n}: total angle = {total_pi}*pi, cos = {cos_val}")

# Check if standard also achieves zero error anywhere
std_zero_ns = [r['n'] for r in results if r['standard_zero_error']]
print(f"\nZero-error n values (Standard): {std_zero_ns}")
print(f"Count: {len(std_zero_ns)}")

# Error statistics
d_errors = [r['dollard_error'] for r in results]
s_errors = [r['standard_error'] for r in results]
print(f"\nDollard error: min={min(d_errors):.4e}, max={max(d_errors):.4e}, "
      f"mean={np.mean(d_errors):.4e}, median={np.median(d_errors):.4e}")
print(f"Standard error: min={min(s_errors):.4e}, max={max(s_errors):.4e}, "
      f"mean={np.mean(s_errors):.4e}, median={np.median(s_errors):.4e}")

# Count where Dollard is better vs worse
d_better = sum(1 for r in results if r['dollard_error'] < r['standard_error'])
s_better = sum(1 for r in results if r['standard_error'] < r['dollard_error'])
tied = sum(1 for r in results if r['dollard_error'] == r['standard_error'])
print(f"\nDollard better: {d_better}/{N_MAX}")
print(f"Standard better: {s_better}/{N_MAX}")
print(f"Tied: {tied}/{N_MAX}")

# === Falsification check ===
print(f"\n{'='*90}")
print("FALSIFICATION CHECK (from pre-registered experiment)")
print(f"{'='*90}")

# Check: do zero-error points occur ONLY at n where cos is 0, +1, -1?
non_trivial_zeros = []
for n in zero_error_ns:
    cos_val = float(mpmath.cos(n * mpmath.mpf(str(theta))))
    if abs(cos_val) not in [0.0, 1.0]:
        non_trivial_zeros.append((n, cos_val))

if not zero_error_ns:
    print("\nNo zero-error points found. Finding may not reproduce.")
elif non_trivial_zeros:
    print(f"\nZero-error at NON-TRIVIAL cos values: {non_trivial_zeros}")
    print("This SUPPORTS hypothesis (A): structural property of Z4.")
else:
    all_at_exact = all(
        abs(float(mpmath.cos(n * mpmath.mpf(str(theta))))) in [0.0, 1.0]
        for n in zero_error_ns
    )
    if all_at_exact:
        # But also check: are ALL such points zero-error?
        expected_zeros = [n for n in range(1, N_MAX+1)
                         if abs(float(mpmath.cos(n * mpmath.mpf(str(theta))))) in [0.0, 1.0]]
        actual_zeros = set(zero_error_ns)
        missing = [n for n in expected_zeros if n not in actual_zeros]
        if missing:
            print(f"\nZero-error occurs ONLY at exact cos values (0, +/-1),")
            print(f"but NOT at all such points. Missing: {missing}")
            print("Partial pattern — needs further investigation.")
        else:
            print(f"\nZero-error occurs at ALL and ONLY exact cos values.")
            print("This SUPPORTS hypothesis (B): floating-point coincidence.")
    else:
        print(f"\nZero-error at exact cos values only: {all_at_exact}")

# === Save results ===
output_dir = os.path.join(os.path.dirname(__file__), 'results')
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, f'001_systematic_n_sweep_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')

# Convert for JSON serialization
output_data = {
    'experiment': '001-systematic-n-sweep',
    'timestamp': datetime.now().isoformat(),
    'parameters': {
        'theta': theta,
        'theta_description': 'pi/100',
        'N_MAX': N_MAX,
        'mpmath_digits': 50,
        'taylor_terms': 40,
    },
    'summary': {
        'zero_error_ns_dollard': zero_error_ns,
        'zero_error_ns_standard': std_zero_ns,
        'dollard_better_count': d_better,
        'standard_better_count': s_better,
        'tied_count': tied,
        'non_trivial_zeros': non_trivial_zeros,
    },
    'data': results,
}

def make_serializable(obj):
    """Convert numpy/bool types for JSON."""
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    if isinstance(obj, tuple):
        return [make_serializable(v) for v in obj]
    return obj

with open(output_file, 'w') as f:
    json.dump(make_serializable(output_data), f, indent=2)

print(f"\nResults saved to: {output_file}")
