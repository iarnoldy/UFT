"""
Dollard's Exact Construction — Implemented Step by Step from Source Text
=========================================================================

Source: "Versor Algebra As Applied To Polyphase Power Systems" (2015)
         Eric P. Dollard, source_materials/02_versoralgebra_extracted.txt

RULE: Every step references an equation number from Dollard's text.
      No operations are introduced that Dollard does not specify.
      No arguments are changed from what Dollard uses.
      Comments quote Dollard directly where possible.

This script implements Dollard's construction FROM HIS TEXT, not our
interpretation of it. If a property emerges, it's from his process.
If it doesn't, we don't force it.
"""

import numpy as np
import mpmath
from math import factorial

mpmath.mp.dps = 50  # 50-digit reference precision


# =============================================================================
# STEP 1: The Log Base Epsilon (Section [3], eq 5-9)
# "The geometric ratio Epsilon finds its origin in the Newton-Leibnitz
#  mathematics." — p.13
# =============================================================================

# Eq (7): Epsilon as infinite series
def epsilon_series(N_terms=20):
    """Eq (7): E = 1/0! + 1/1! + 1/2! + 1/3! + ..."""
    return sum(1.0 / factorial(n) for n in range(N_terms))

EPSILON = epsilon_series()


# =============================================================================
# STEP 2: Powers of Epsilon (Section [4], eq 12-17)
# "Epsilon raised to any positive power expresses a rate of growth,
#  this compounding upon itself." — p.16
# =============================================================================

def epsilon_to_power(delta, N_terms=40):
    """Eq (14-17): E^δ = Σ δ^n / n!  (the Taylor series of e^δ)"""
    return sum(delta**n / factorial(n) for n in range(N_terms))


# =============================================================================
# STEP 3: Imaginary Exponents, h (Section [5], eq 18-26)
# "two imaginaries are possible, one is the D.C. operator:" — p.18
#
# Eq (18): h^n = +1^(1/2), h^2 = +1, h = -1, h^1 = -1
# Eq (20): E^h = E^(-1)
# =============================================================================

# Dollard defines h = -1 explicitly in eq (18)
h = -1  # This is Dollard's definition, not our derivation


# =============================================================================
# STEP 4: Hyperbolic Functions (Section [6], eq 27-59)
# "Separating the infinite series expression into its even and odd
#  components" — p.27
#
# Eq (37): E^h = 1/0! + h/1! + 1/2! + h/3! + 1/4! + h/5! + ...
# Eq (39): Even/odd separation → Alpha (cosh) and Beta (sinh)
# Eq (55): α = cosh(δ), β = sinh(δ)
# =============================================================================

def epsilon_to_h_decomposed(delta, N_terms=40):
    """
    Eq (37-40): E^(h·δ) decomposed into even (α) and odd (β) parts.

    The h operator alternates: h^0=1, h^1=h, h^2=1, h^3=h, ...
    Even terms (real): α = Σ δ^(2n) / (2n)!  = cosh(δ)  [eq 42, 55]
    Odd terms (imaginary h): β = Σ δ^(2n+1) / (2n+1)!  = sinh(δ)  [eq 43, 55]

    Full expression: E^(h·δ) = α + h·β = cosh(δ) + h·sinh(δ)
    Since h = -1: E^(h·δ) = cosh(δ) - sinh(δ) = e^(-δ)
    """
    alpha = sum(delta**(2*n) / factorial(2*n) for n in range(N_terms))
    beta = sum(delta**(2*n+1) / factorial(2*n+1) for n in range(N_terms))
    return alpha, beta


# =============================================================================
# STEP 5: Imaginary Exponents, j (Section [7], eq 60-82)
# "By definition the imaginary j is a quaternary operator, the result
#  of a fourth order expression" — p.33
#
# Eq (61): j = √(-1)
# Eq (63): j^0 = +1, j^1 = +j, j^2 = -1, j^3 = -j
# Eq (64): j^4 = j^0 = +1, j^2 = h^1 = -1
# Eq (65): j^3 = -j = hj = k
# Eq (66): jk = +1
# =============================================================================

j = 1j  # Standard imaginary unit (Dollard's j)
k = h * j  # Eq (65): k = hj = (-1)(j) = -j

# Eq (70): The sequence +1, +j, -1, -j, +1, +j, ...
operators = [1, j, h, k]  # = [1, j, -1, -j] — the Z4 group


# =============================================================================
# STEP 6: The Quaternary Expansion (Section [7] continued, eq 67-82)
#
# THIS IS THE CRITICAL SECTION.
# Dollard decomposes E^j into four groups by operator.
#
# Eq (67): E^j = j^0/0! + j^1/1! + j^2/2! + j^3/3! + j^4/4! + ...
# Eq (73): E^j = 1/0! + j/1! + h/2! + k/3! + 1/4! + j/5! + h/6! + k/7! + ...
#
# Eq (76): Grouped by operator, factoring out each operator:
#   1(u) = [scalar series] · 1
#   j(x) = [scalar series] · j
#   h(ν) = [scalar series] · h
#   k(y) = [scalar series] · k
#
# Eq (77): E^j = 1(μ) + j(x) + h(ν) + k(y)
# =============================================================================

def dollard_quaternary_expansion(theta, N_terms=40):
    """
    Dollard's quaternary expansion of E^(jθ) — eq (67)-(77).

    Implements EXACTLY Dollard's process:
    1. Compute E^(jθ) = Σ (jθ)^n / n!
    2. Group terms by which operator they carry (1, j, h, k)
    3. Factor out the operator, leaving scalar parts u, x, ν, y

    The scalar parts are:
      u = Σ θ^(4n)   / (4n)!     [terms where j^(4n)   = 1]
      x = Σ θ^(4n+1) / (4n+1)!   [terms where j^(4n+1) = j, factor out j]
      ν = Σ θ^(4n+2) / (4n+2)!   [terms where j^(4n+2) = h, factor out h]
      y = Σ θ^(4n+3) / (4n+3)!   [terms where j^(4n+3) = k, factor out k]

    Returns: (u, x, nu, y) — all POSITIVE real scalars for θ > 0
    Also returns: operators (1, j, h, k) for reconstruction
    """
    u_scalar = 0.0   # coefficient of operator 1
    x_scalar = 0.0   # coefficient of operator j
    nu_scalar = 0.0  # coefficient of operator h
    y_scalar = 0.0   # coefficient of operator k

    for n in range(N_terms):
        for r in range(4):
            idx = 4 * n + r
            term = theta**idx / factorial(idx)
            if r == 0:
                u_scalar += term    # operator 1
            elif r == 1:
                x_scalar += term    # operator j
            elif r == 2:
                nu_scalar += term   # operator h
            elif r == 3:
                y_scalar += term    # operator k

    return u_scalar, x_scalar, nu_scalar, y_scalar


def _demo_steps_6_7():
    """Demo output for Steps 6-7 (quaternary expansion and duo-binary form)."""
    print(f"\nStep 6 — Dollard's quaternary expansion (eq 67-77):")
    print(f"  Computing E^(jθ) for θ = 1 (unit angle):")

    u, x, nu, y = dollard_quaternary_expansion(1.0)

    print(f"\n  Scalar parts (ALL should be positive for θ > 0):")
    print(f"    u  = {u:.10f}  (coefficient of operator 1)")
    print(f"    x  = {x:.10f}  (coefficient of operator j)")
    print(f"    ν  = {nu:.10f}  (coefficient of operator h)")
    print(f"    y  = {y:.10f}  (coefficient of operator k)")
    print(f"    All positive? u>{0}: {u>0}, x>{0}: {x>0}, ν>{0}: {nu>0}, y>{0}: {y>0}")

    # Reconstruct using Dollard's eq (77): E^j = 1(u) + j(x) + h(ν) + k(y)
    reconstructed = 1*u + j*x + h*nu + k*y
    direct = np.exp(1j)  # Direct computation of e^j

    print(f"\n  Reconstruction (eq 77): 1·u + j·x + h·ν + k·y")
    print(f"    = {u} + {j}·{x:.6f} + ({h})·{nu:.6f} + ({k})·{y:.6f}")
    print(f"    = {reconstructed:.10f}")
    print(f"    Direct E^j = {direct:.10f}")
    print(f"    Match: {abs(reconstructed - direct) < 1e-12}")

    # --- Step 7: Duo-Binary Form (eq 79-82) ---
    a = u - nu   # eq (81): the "real" part = cos(θ)
    b = x - y    # eq (81): the "imaginary" part = sin(θ)

    print(f"\nStep 7 — Duo-binary form (eq 79-82):")
    print(f"  a = u - ν = {a:.10f}  (cos(1) = {np.cos(1):.10f})")
    print(f"  b = x - y = {b:.10f}  (sin(1) = {np.sin(1):.10f})")
    print(f"  a² + b² = {a**2 + b**2:.10f}  (eq 82a: should be 1)")

    cosh_val = u + nu
    sinh_val = x + y
    print(f"\n  Gross quantities (no subtraction needed):")
    print(f"  u + ν = {cosh_val:.10f}  (cosh(1) = {np.cosh(1):.10f})")
    print(f"  x + y = {sinh_val:.10f}  (sinh(1) = {np.sinh(1):.10f})")


# =============================================================================
# *** DEPARTURE POINT ***
# Steps 1-7 above implement Dollard's EXPLICIT process from his source text.
# Steps 8-10 below are OUR APPLICATION of his algebra to CHAINING operations.
# Dollard does NOT describe multiplying two quaternary elements or chaining.
# The Z4 multiplication table is derived from his operators (eq 63-66) but
# the chaining operation itself is our construction.
# TAG: [OUR APPLICATION] — built on Dollard's algebra, not from his text.
# =============================================================================

# =============================================================================
# STEP 8: What Dollard's Construction ACTUALLY Gives You
#
# The full algebraic element is: 1·u + j·x + h·ν + k·y
# This is NOT a real 4-vector. It is a Z4-GRADED element.
# The operators constrain the result to the unit circle.
#
# Let's see what happens when we CHAIN operations using Dollard's
# algebra — WITH the operators, not stripped.
# =============================================================================

def main():
    """Run the full demonstration of Dollard's exact construction."""
    print(f"Step 1 — Epsilon (eq 7): {EPSILON:.15f}")
    print(f"  Standard e:            {np.e:.15f}")
    print(f"  Match: {abs(EPSILON - np.e) < 1e-14}")

    print(f"\nStep 2 — Powers of Epsilon:")
    print(f"  E^1 (eq 12): {epsilon_to_power(1):.6f}  (Dollard: 2.718)")
    print(f"  E^2 (eq 13): {epsilon_to_power(2):.6f}  (Dollard: 7.389)")

    print(f"\nStep 3 — The DC operator h:")
    print(f"  h = {h}  (eq 18: h = -1)")
    print(f"  h^2 = {h**2}  (eq 18: h^2 = +1)")
    print(f"  E^h = E^(-1) = {epsilon_to_power(h):.6f}  (eq 20, Dollard: 1/2.718 = 0.368)")

    print(f"\nStep 4 — Hyperbolic functions from h decomposition:")
    for delta in [1.0, 2.0]:
        alpha, beta = epsilon_to_h_decomposed(delta)
        print(f"  δ = {delta}:")
        print(f"    α = {alpha:.10f}  (cosh({delta}) = {np.cosh(delta):.10f})")
        print(f"    β = {beta:.10f}  (sinh({delta}) = {np.sinh(delta):.10f})")
        print(f"    α + h·β = {alpha + h*beta:.10f}  (E^(-{delta}) = {np.exp(-delta):.10f})")
        print(f"    α² - β² = {alpha**2 - beta**2:.10f}  (eq 47: should be 1)")

    print(f"\nStep 5 — The AC operator j and the sequence operator k:")
    print(f"  j = {j}  (eq 61)")
    print(f"  j^2 = {j**2}  (eq 63: should be -1 = h)")
    print(f"  k = hj = {k}  (eq 65: should be -j)")
    print(f"  jk = {j*k}  (eq 66: should be +1)")
    print(f"  Operator sequence (eq 70): {[complex(op) for op in operators]}")

    _demo_steps_6_7()

    print(f"\n{'='*70}")
    print(f"STEP 8: CHAINING IN DOLLARD'S ALGEBRA (with operators)")
    print(f"{'='*70}")

def dollard_multiply(elem1, elem2):
    """
    Multiply two Dollard quaternary elements using Z4 algebra.

    Each element is (u, x, ν, y) representing 1·u + j·x + h·ν + k·y.

    Multiplication table (from Z4 = {1, j, h=-1, k=-j}):
      1·1 = 1    1·j = j    1·h = h    1·k = k
      j·1 = j    j·j = h    j·h = k    j·k = 1
      h·1 = h    h·j = k    h·h = 1    h·k = j
      k·1 = k    k·j = 1    k·h = j    k·k = h

    So for (1·u₁ + j·x₁ + h·ν₁ + k·y₁) × (1·u₂ + j·x₂ + h·ν₂ + k·y₂):

    Coefficient of 1: u₁u₂ + x₁y₂ + ν₁ν₂ + y₁x₂  (from 1·1, j·k, h·h, k·j)
    Coefficient of j: u₁x₂ + x₁u₂ + ν₁y₂ + y₁ν₂  (from 1·j, j·1, h·k, k·h)
    Coefficient of h: u₁ν₂ + x₁x₂ + ν₁u₂ + y₁y₂  (from 1·h, j·j, h·1, k·k)
    Coefficient of k: u₁y₂ + x₁ν₂ + ν₁x₂ + y₁u₂  (from 1·k, j·h, h·j, k·1)
    """
    u1, x1, n1, y1 = elem1
    u2, x2, n2, y2 = elem2

    u3 = u1*u2 + x1*y2 + n1*n2 + y1*x2
    x3 = u1*x2 + x1*u2 + n1*y2 + y1*n2
    n3 = u1*n2 + x1*x2 + n1*u2 + y1*y2
    y3 = u1*y2 + x1*n2 + n1*x2 + y1*u2

    return (u3, x3, n3, y3)


def dollard_to_complex(elem):
    """Convert Dollard element to standard complex: (u-ν) + j(x-y)"""
    u, x, nu, y = elem
    return complex(u - nu, x - y)


def dollard_gross_net(elem):
    """Extract gross and net from Dollard element."""
    u, x, nu, y = elem
    return {
        'cosh': u + nu,    # gross real (no subtraction)
        'sinh': x + y,     # gross imaginary (no subtraction)
        'cos': u - nu,     # net real (subtraction)
        'sin': x - y,      # net imaginary (subtraction)
        'all_positive': all(v > 0 for v in [u, x, nu, y]),
    }


    # Chain: multiply Dollard elements for angle θ, n times
    # This should give E^(jnθ) = cos(nθ) + j·sin(nθ)

    theta = np.pi / 6  # 30 degrees — Dollard's domain
    step = dollard_quaternary_expansion(theta)

    print(f"\n  θ = π/6 = {theta:.6f}")
    print(f"  Step element: u={step[0]:.8f}, x={step[1]:.8f}, ν={step[2]:.8f}, y={step[3]:.8f}")
    print(f"  All positive? {all(s > 0 for s in step)}")
    print(f"  Complex value: {dollard_to_complex(step):.10f}")
    print(f"  Direct e^(jθ): {np.exp(1j*theta):.10f}")

    print(f"\n  CHAINING — multiplying Dollard elements n times:")
    print(f"  {'n':>5} {'cos(nθ) Dollard':>18} {'cos(nθ) exact':>18} {'abs error':>12} "
          f"{'all positive?':>14} {'gross/net':>10}")
    print(f"  {'-'*80}")

    # Start with identity element: (1, 0, 0, 0) = 1·1 + j·0 + h·0 + k·0
    state = (1.0, 0.0, 0.0, 0.0)

    # Also track standard rotation for comparison
    c_std, s_std = 1.0, 0.0
    ct, st = np.cos(theta), np.sin(theta)

    for n in range(1, 25):
        state = dollard_multiply(state, step)
        c_std, s_std = c_std*ct - s_std*st, s_std*ct + c_std*st

        # Reference — pinned: float64 product to mpmath (Rule 10)
        exact_cos = float(mpmath.cos(n * theta))
        dollard_cos = state[0] - state[2]
        err_d = abs(dollard_cos - exact_cos)
        err_s = abs(c_std - exact_cos)

        gn = dollard_gross_net(state)
        ratio = gn['cosh'] / (abs(gn['cos']) + 1e-300)

        if n <= 12 or n == 24:
            print(f"  {n:>5} {dollard_cos:>18.12f} {exact_cos:>18.12f} {err_d:>12.2e} "
                  f"{'YES' if gn['all_positive'] else 'NO':>14} {ratio:>10.1f}")

    # =================================================================
    # STEP 9: Compare Dollard vs Standard — WHO WINS?
    # =================================================================

    print(f"\n{'='*70}")
    print(f"STEP 9: COMPARISON — Dollard's Z4 algebra vs Standard rotation")
    print(f"{'='*70}")

    state = (1.0, 0.0, 0.0, 0.0)
    c_std, s_std = 1.0, 0.0

    theta_small = np.pi / 100
    step_small = dollard_quaternary_expansion(theta_small)
    ct_s, st_s = np.cos(theta_small), np.sin(theta_small)

    print(f"\n  θ = π/100 = {theta_small:.6f}, chaining up to n=1000 (total = 10π)")
    print(f"\n  {'n':>6} {'Dollard err':>14} {'Standard err':>14} {'Ratio D/S':>10} "
          f"{'u+ν (cosh)':>14} {'u-ν (cos)':>14}")
    print(f"  {'-'*80}")

    for n in range(1, 1001):
        state = dollard_multiply(state, step_small)
        c_std, s_std = c_std*ct_s - s_std*st_s, s_std*ct_s + c_std*st_s

        # Reference — pinned: float64 product to mpmath (Rule 10)
        exact_cos = float(mpmath.cos(n * theta_small))
        err_d = abs((state[0] - state[2]) - exact_cos)
        err_s = abs(c_std - exact_cos)

        if n in [1, 10, 50, 100, 200, 500, 1000]:
            ratio = err_d / (err_s + 1e-300)
            gross = state[0] + state[2]
            net = state[0] - state[2]
            print(f"  {n:>6} {err_d:>14.4e} {err_s:>14.4e} {ratio:>10.1f}x "
                  f"{gross:>14.6f} {net:>14.10f}")

    print(f"\n  Final state scalars:")
    print(f"    u  = {state[0]:.10f}")
    print(f"    x  = {state[1]:.10f}")
    print(f"    ν  = {state[2]:.10f}")
    print(f"    y  = {state[3]:.10f}")
    print(f"    All positive? {all(s > 0 for s in state)}")
    print(f"    u + ν = cosh(10π) = {state[0]+state[2]:.6e}  (exact: {np.cosh(1000*theta_small):.6e})")
    print(f"    u - ν = cos(10π)  = {state[0]-state[2]:.10f}  (exact: {float(mpmath.cos(1000*theta_small)):.10f})")

    # =================================================================
    # STEP 10: THE QUESTION
    # =================================================================

    print(f"\n{'='*70}")
    print(f"STEP 10: Does the operator structure change anything?")
    print(f"{'='*70}")

    print(f"""
  Dollard's full element: 1·u + j·x + h·ν + k·y

  The Z4 multiplication is the cyclic convolution — SAME operation
  whether or not we write the operators.

  The scalar parts u, x, ν, y follow the SAME recurrence regardless
  of whether we conceptualize them as "coefficients of operators" or
  "components of a real 4-vector."

  The numerical values are identical. The errors are identical.

  The operators don't change the arithmetic. They change the INTERPRETATION.

  When Dollard writes 1·u + j·x + h·ν + k·y, he's saying:
  - u is the STORAGE component (operator 1, real positive)
  - x is the TRANSFER component (operator j, rotation)
  - ν is the RETURN component (operator h, reversal)
  - y is the DISSIPATION component (operator k, counter-rotation)

  These labels provide PHYSICAL MEANING to each scalar.
  They don't change the numbers.
""")

    print(f"  Verification: Z4 multiply == complex multiply?")
    for total_n in [1, 5, 12, 24]:
        elem = dollard_quaternary_expansion(total_n * theta)

        chained = (1.0, 0.0, 0.0, 0.0)
        for _ in range(total_n):
            chained = dollard_multiply(chained, dollard_quaternary_expansion(theta))

        z_direct = dollard_to_complex(elem)
        z_chained = dollard_to_complex(chained)
        z_numpy = np.exp(1j * total_n * theta)

        print(f"    n={total_n:>2}: direct={z_direct:.8f}  chained={z_chained:.8f}  "
              f"numpy={z_numpy:.8f}  match={abs(z_direct - z_numpy) < 1e-10}")


if __name__ == "__main__":
    main()
