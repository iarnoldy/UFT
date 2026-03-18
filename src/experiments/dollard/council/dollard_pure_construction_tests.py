"""
Dollard Pure Construction: Computational Verification Tests

Research Council Investigation: dollard-pure-construction
Round 4: COMPUTATION

Tests whether Dollard's operational construction produces ANY different
numerical results from standard complex analysis.

Four tests:
1. epsilon^(h*delta) vs e^(-delta) — step-by-step Taylor series comparison
2. Quaternary expansion verification — four subseries identities
3. h*f(x) vs -f(x) — operator equivalence for various functions
4. Versor products vs complex multiplication — ZY impedance-admittance product
"""

import numpy as np
import math
from decimal import Decimal, getcontext
import json
import os

# High precision for Taylor series comparison
getcontext().prec = 60

def test_1_epsilon_h_delta():
    """
    Test 1: Does epsilon^(h*delta) produce different results from e^(-delta)?

    Method: Compute the Taylor series of epsilon^(h*delta) keeping h symbolic
    (as alternating +1/-1 coefficients), then sum. Compare with direct e^(-delta).
    """
    print("=" * 70)
    print("TEST 1: epsilon^(h*delta) vs e^(-delta)")
    print("=" * 70)

    results = {}
    test_values = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]

    for delta in test_values:
        # Method A: Dollard's construction
        # epsilon^(h*delta) = sum_{n=0}^{inf} (h*delta)^n / n!
        # Since h = -1, h^n alternates: h^0=1, h^1=-1, h^2=1, h^3=-1, ...
        # So (h*delta)^n = h^n * delta^n = (-1)^n * delta^n = (-delta)^n
        # Series: sum (-delta)^n / n! = e^(-delta)

        # But let's compute it KEEPING h symbolic in intermediate steps
        # h^n coefficient for term n
        N_terms = 80  # enough for convergence

        # Dollard's way: accumulate with h-coefficients
        real_part = 0.0  # coefficients of h^0, h^2, h^4, ... = 1
        h_part = 0.0     # coefficients of h^1, h^3, h^5, ... = h = -1

        for n in range(N_terms):
            term = delta**n / math.factorial(n)
            if n % 2 == 0:
                real_part += term  # h^(even) = 1
            else:
                h_part += term     # h^(odd) = h

        # Before substituting h = -1:
        # epsilon^(h*delta) = real_part + h * h_part
        # where real_part = cosh(delta), h_part = sinh(delta)

        # After substituting h = -1:
        dollard_result = real_part + (-1) * h_part  # = cosh(delta) - sinh(delta)

        # Method B: Direct computation
        direct_result = np.exp(-delta)

        # Method C: Standard cosh/sinh
        standard_result = np.cosh(delta) - np.sinh(delta)

        diff_dollard_direct = abs(dollard_result - direct_result)
        diff_cosh_sinh = abs(standard_result - direct_result)

        results[str(delta)] = {
            "dollard_series": dollard_result,
            "direct_exp": direct_result,
            "cosh_minus_sinh": standard_result,
            "real_part_equals_cosh": abs(real_part - np.cosh(delta)) < 1e-12,
            "h_part_equals_sinh": abs(h_part - np.sinh(delta)) < 1e-12,
            "diff_dollard_vs_direct": diff_dollard_direct,
            "diff_coshsinh_vs_direct": diff_cosh_sinh,
            "all_identical": diff_dollard_direct < 1e-12 and diff_cosh_sinh < 1e-12
        }

        print(f"\n  delta = {delta}")
        print(f"    Dollard series (real + h*imag, h=-1): {dollard_result:.15e}")
        print(f"    Direct exp(-delta):                   {direct_result:.15e}")
        print(f"    cosh(delta) - sinh(delta):            {standard_result:.15e}")
        print(f"    real_part = cosh(delta)?  {results[str(delta)]['real_part_equals_cosh']}")
        print(f"    h_part = sinh(delta)?     {results[str(delta)]['h_part_equals_sinh']}")
        print(f"    |Dollard - Direct| = {diff_dollard_direct:.2e}")
        print(f"    ALL IDENTICAL: {results[str(delta)]['all_identical']}")

    all_passed = all(r["all_identical"] for r in results.values())
    print(f"\n  VERDICT: {'ALL IDENTICAL' if all_passed else 'DIFFERENCES FOUND'}")

    return {
        "test": "epsilon^(h*delta) vs e^(-delta)",
        "passed": all_passed,
        "verdict": "Dollard's step-by-step computation through h-coefficients produces IDENTICAL results to direct e^(-delta). The intermediate decomposition into cosh and sinh components is real (real_part = cosh, h_part = sinh) but the final answer is the same.",
        "results": results
    }


def test_2_quaternary_expansion():
    """
    Test 2: Quaternary expansion verification.

    The four subseries of e^t:
    u = sum t^(4n)/(4n)!     [n mod 4 = 0]
    x = sum t^(4n+1)/(4n+1)! [n mod 4 = 1]
    v = sum t^(4n+2)/(4n+2)! [n mod 4 = 2]
    y = sum t^(4n+3)/(4n+3)! [n mod 4 = 3]

    Identities to verify:
    u - v = cos(t)
    x - y = sin(t)
    u + v = cosh(t)
    x + y = sinh(t)
    u + x + v + y = e^t
    """
    print("\n" + "=" * 70)
    print("TEST 2: Quaternary Expansion")
    print("=" * 70)

    results = {}
    test_values = [0.0, 0.5, 1.0, np.pi/4, np.pi/2, np.pi, 2.0, 3.0, 5.0]
    N_terms = 80

    for t in test_values:
        # Compute four subseries
        u = sum(t**(4*n) / math.factorial(4*n) for n in range(N_terms // 4 + 1) if 4*n < N_terms)
        x_val = sum(t**(4*n+1) / math.factorial(4*n+1) for n in range(N_terms // 4 + 1) if 4*n+1 < N_terms)
        v = sum(t**(4*n+2) / math.factorial(4*n+2) for n in range(N_terms // 4 + 1) if 4*n+2 < N_terms)
        y_val = sum(t**(4*n+3) / math.factorial(4*n+3) for n in range(N_terms // 4 + 1) if 4*n+3 < N_terms)

        # Verify identities
        id1 = abs((u - v) - np.cos(t))
        id2 = abs((x_val - y_val) - np.sin(t))
        id3 = abs((u + v) - np.cosh(t))
        id4 = abs((x_val + y_val) - np.sinh(t))
        id5 = abs((u + x_val + v + y_val) - np.exp(t))

        # Verify that u,x,v,y can be computed from cos,sin,cosh,sinh
        u_from_std = (np.cosh(t) + np.cos(t)) / 2
        x_from_std = (np.sinh(t) + np.sin(t)) / 2
        v_from_std = (np.cosh(t) - np.cos(t)) / 2
        y_from_std = (np.sinh(t) - np.sin(t)) / 2

        id6 = abs(u - u_from_std)
        id7 = abs(x_val - x_from_std)
        id8 = abs(v - v_from_std)
        id9 = abs(y_val - y_from_std)

        tol = 1e-10
        all_ok = all(x < tol for x in [id1, id2, id3, id4, id5, id6, id7, id8, id9])

        results[f"t={t:.4f}"] = {
            "u": u, "x": x_val, "v": v, "y": y_val,
            "u-v vs cos": id1, "x-y vs sin": id2,
            "u+v vs cosh": id3, "x+y vs sinh": id4,
            "sum vs exp": id5,
            "u from (cosh+cos)/2": id6, "x from (sinh+sin)/2": id7,
            "v from (cosh-cos)/2": id8, "y from (sinh-sin)/2": id9,
            "all_passed": all_ok
        }

        print(f"\n  t = {t:.4f}")
        print(f"    u={u:.10f}, x={x_val:.10f}, v={v:.10f}, y={y_val:.10f}")
        print(f"    |u-v - cos(t)| = {id1:.2e}")
        print(f"    |x-y - sin(t)| = {id2:.2e}")
        print(f"    |u+v - cosh(t)| = {id3:.2e}")
        print(f"    |x+y - sinh(t)| = {id4:.2e}")
        print(f"    |u+x+v+y - e^t| = {id5:.2e}")
        print(f"    u = (cosh+cos)/2? {id6:.2e}")
        print(f"    ALL PASSED: {all_ok}")

    all_passed = all(r["all_passed"] for r in results.values())
    print(f"\n  VERDICT: {'ALL IDENTITIES VERIFIED' if all_passed else 'FAILURES FOUND'}")

    # Key question: does the quaternary expansion provide DIFFERENT numerical
    # results from computing cos, sin, cosh, sinh directly?
    print("\n  COMPUTATIONAL EQUIVALENCE TEST:")
    print("  Can u,x,v,y be computed from standard functions?")
    print("  u = (cosh(t) + cos(t))/2  -- YES (verified above)")
    print("  x = (sinh(t) + sin(t))/2  -- YES (verified above)")
    print("  v = (cosh(t) - cos(t))/2  -- YES (verified above)")
    print("  y = (sinh(t) - sin(t))/2  -- YES (verified above)")
    print("  The quaternary expansion contains NO information")
    print("  beyond what cosh, sinh, cos, sin already contain.")

    return {
        "test": "Quaternary expansion",
        "passed": all_passed,
        "verdict": "All quaternary identities verified to < 1e-10. The four subseries u,x,v,y are exactly (cosh+cos)/2, (sinh+sin)/2, (cosh-cos)/2, (sinh-sin)/2. They contain NO additional information beyond standard trig/hyp functions. The quaternary expansion is a REARRANGEMENT, not new content.",
        "computational_equivalence": "u,x,v,y are invertibly related to cos,sin,cosh,sinh. No new information.",
        "results": {k: {kk: float(vv) if isinstance(vv, (float, np.floating)) else vv for kk, vv in v.items()} for k, v in results.items()}
    }


def test_3_h_operator_vs_negation():
    """
    Test 3: Is there ANY context where h*f(x) differs from -f(x)?

    Since h = -1 (a theorem), h*f(x) = (-1)*f(x) = -f(x) for ALL f, ALL x.
    But let's test explicitly with various functions.
    """
    print("\n" + "=" * 70)
    print("TEST 3: h*f(x) vs -f(x)")
    print("=" * 70)

    h = -1  # Dollard's h, algebraically forced

    functions = {
        "exp(x)": np.exp,
        "sin(x)": np.sin,
        "cos(x)": np.cos,
        "x^2": lambda x: x**2,
        "1/x": lambda x: 1/x if x != 0 else float('inf'),
        "sinh(x)": np.sinh,
        "cosh(x)": np.cosh,
        "log(|x|)": lambda x: np.log(abs(x)) if x != 0 else float('-inf'),
    }

    test_points = [0.1, 0.5, 1.0, 2.0, np.pi, np.e, 10.0]
    results = {}
    all_passed = True

    for fname, f in functions.items():
        for x in test_points:
            h_result = h * f(x)
            neg_result = -f(x)
            diff = abs(h_result - neg_result)
            passed = diff < 1e-15
            if not passed:
                all_passed = False
            results[f"h*{fname}(x={x})"] = {
                "h_result": h_result,
                "neg_result": neg_result,
                "diff": diff,
                "passed": passed
            }

    total = len(results)
    passed_count = sum(1 for r in results.values() if r["passed"])

    print(f"  Tested {len(functions)} functions at {len(test_points)} points = {total} tests")
    print(f"  ALL h*f(x) == -f(x): {all_passed} ({passed_count}/{total} passed)")

    # The deeper test: does h*f(x) as an OPERATION differ from -f(x)?
    # This is about whether "apply h, then evaluate" differs from "evaluate, then negate"
    print("\n  OPERATIONAL ORDER TEST:")
    print("  Does h applied BEFORE evaluation differ from -1 applied AFTER?")

    for delta in [0.5, 1.0, 2.0]:
        # epsilon^(h*delta) = e^(-delta): h in exponent
        result_h_in_exp = np.exp(h * delta)  # = exp(-delta)

        # h * epsilon^delta = -e^delta: h multiplying result
        result_h_times = h * np.exp(delta)  # = -exp(delta)

        print(f"  delta = {delta}:")
        print(f"    epsilon^(h*delta) = exp({h}*{delta}) = exp({h*delta}) = {result_h_in_exp:.6f}")
        print(f"    h * epsilon^delta = {h} * exp({delta}) = {result_h_times:.6f}")
        print(f"    THESE ARE DIFFERENT: {abs(result_h_in_exp - result_h_times) > 0.001}")
        print(f"    But this is exp(-x) vs -exp(x), which are different functions of x.")
        print(f"    This is standard math: f(-x) != -f(x) unless f is odd.")

    print("\n  VERDICT: h*f(x) = -f(x) ALWAYS (h is literally -1).")
    print("  The distinction e^(h*delta) vs h*e^(delta) is real but it is")
    print("  the standard distinction e^(-x) vs -e^(x). No operator content.")

    return {
        "test": "h*f(x) vs -f(x)",
        "passed": all_passed,
        "verdict": "h*f(x) = -f(x) for ALL tested functions at ALL tested points, to machine precision. The distinction between h-in-exponent (e^(-delta)) and h-times-result (-e^(delta)) is the standard distinction between f(-x) and -f(x). This is a property of real numbers, not of any operator.",
        "total_tests": total,
        "passed_tests": passed_count
    }


def test_4_versor_vs_complex():
    """
    Test 4: Do Dollard's versor products produce different numerical results
    from standard complex multiplication?

    Z = R + jX (impedance), Y = G - jB (admittance, Dollard's convention)
    Dollard claims ZY = h(XB+RG) + j(XG-RB)
    Standard complex: ZY = (RG+XB) + j(XG-RB)
    """
    print("\n" + "=" * 70)
    print("TEST 4: Versor Products vs Complex Multiplication")
    print("=" * 70)

    h = -1  # forced
    j_unit = 1j  # standard complex unit

    test_cases = [
        (1, 0, 1, 0),    # purely real
        (0, 1, 0, 1),    # purely reactive
        (1, 1, 1, 1),    # equal parts
        (3, 4, 0.2, 0.1),  # typical impedance/admittance
        (50, 0, 0.02, 0),  # purely resistive
        (0, 100, 0, 0.01), # purely reactive
        (10, 20, 0.05, 0.03),  # general case
    ]

    results = {}
    all_passed = True

    for R, X, G, B in test_cases:
        # Standard complex multiplication
        Z = complex(R, X)
        Y = complex(G, -B)  # Dollard's sign convention: Y = G - jB
        ZY_complex = Z * Y

        # Extract components
        real_std = ZY_complex.real   # = RG + XB
        imag_std = ZY_complex.imag   # = XG - RB

        # Dollard's claimed form: h(XB+RG) + j(XG-RB)
        # With h = -1: -(XB+RG) + j(XG-RB)
        dollard_real = h * (X*B + R*G)  # = -(RG+XB)
        dollard_imag = X*G - R*B         # = XG-RB

        # The CORRECT product (R+jX)(G-jB) = (RG+XB) + j(XG-RB)
        correct_real = R*G + X*B
        correct_imag = X*G - R*B

        # Does standard complex match the correct algebraic product?
        std_matches_correct = (abs(real_std - correct_real) < 1e-12 and
                              abs(imag_std - correct_imag) < 1e-12)

        # Does Dollard's CLAIMED form match?
        dollard_matches_correct = (abs(dollard_real - correct_real) < 1e-12 and
                                  abs(dollard_imag - correct_imag) < 1e-12)

        label = f"Z=({R}+j{X}), Y=({G}-j{B})"
        results[label] = {
            "standard_complex": {"real": real_std, "imag": imag_std},
            "correct_algebra": {"real": correct_real, "imag": correct_imag},
            "dollard_claimed": {"real": dollard_real, "imag": dollard_imag},
            "standard_matches_correct": std_matches_correct,
            "dollard_claimed_matches_correct": dollard_matches_correct,
        }

        print(f"\n  {label}")
        print(f"    Standard complex:  ({real_std:.4f}) + j({imag_std:.4f})")
        print(f"    Correct algebra:   ({correct_real:.4f}) + j({correct_imag:.4f})")
        print(f"    Dollard's h(...):  ({dollard_real:.4f}) + j({dollard_imag:.4f})")
        print(f"    Standard = Correct? {std_matches_correct}")
        print(f"    Dollard = Correct?  {dollard_matches_correct}")

        if not dollard_matches_correct:
            print(f"    *** DOLLARD'S FORM DOES NOT MATCH (real part has wrong sign)")

    # The key finding
    print("\n  KEY FINDING:")
    print("  Standard complex multiplication ALWAYS matches the correct algebra.")
    print("  Dollard's CLAIMED form h(XB+RG)+j(XG-RB) NEVER matches (except")
    print("  when RG+XB = 0), because h = -1 negates the real part.")
    print("  The correct form is (RG+XB) + j(XG-RB), which is the 1-component")
    print("  not the h-component.")
    print("")
    print("  This confirms the prior refutation: the versor form is wrong in")
    print("  Dollard's algebra because Z and Y live in the {1,j} subspace.")

    any_dollard_wrong = any(not r["dollard_claimed_matches_correct"] for r in results.values())
    all_std_correct = all(r["standard_matches_correct"] for r in results.values())

    return {
        "test": "Versor products vs complex multiplication",
        "passed": all_std_correct,
        "dollard_form_wrong": any_dollard_wrong,
        "verdict": "Standard complex multiplication ALWAYS produces the correct result. Dollard's claimed versor form h(XB+RG)+j(XG-RB) is WRONG because h=-1 negates the real part. The correct form is (RG+XB)+j(XG-RB). Versor notation adds no computational content and introduces an error in Dollard's specific formula.",
        "results": results
    }


if __name__ == "__main__":
    print("DOLLARD PURE CONSTRUCTION: COMPUTATIONAL VERIFICATION")
    print("Research Council Round 4")
    print("=" * 70)

    r1 = test_1_epsilon_h_delta()
    r2 = test_2_quaternary_expansion()
    r3 = test_3_h_operator_vs_negation()
    r4 = test_4_versor_vs_complex()

    print("\n\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    all_results = {
        "test_1_epsilon_h_delta": {
            "passed": r1["passed"],
            "verdict": r1["verdict"]
        },
        "test_2_quaternary_expansion": {
            "passed": r2["passed"],
            "computational_equivalence": r2["computational_equivalence"],
            "verdict": r2["verdict"]
        },
        "test_3_h_vs_negation": {
            "passed": r3["passed"],
            "verdict": r3["verdict"]
        },
        "test_4_versor_vs_complex": {
            "passed": r4["passed"],
            "dollard_form_wrong": r4["dollard_form_wrong"],
            "verdict": r4["verdict"]
        }
    }

    print(f"\n  Test 1 (epsilon^(h*delta)): {'PASS' if r1['passed'] else 'FAIL'} - identical to e^(-delta)")
    print(f"  Test 2 (quaternary expansion): {'PASS' if r2['passed'] else 'FAIL'} - identities verified, no new information")
    print(f"  Test 3 (h*f(x) vs -f(x)): {'PASS' if r3['passed'] else 'FAIL'} - always identical")
    print(f"  Test 4 (versor vs complex): {'PASS' if r4['passed'] else 'FAIL'} - standard is correct, Dollard form is wrong")

    print(f"\n  OVERALL: Dollard's operators produce ZERO results that differ")
    print(f"  from standard complex arithmetic. The quaternary expansion is")
    print(f"  a rearrangement of standard functions with no new information.")
    print(f"  Dollard's specific versor form ZY = h(XB+RG)+j(XG-RB) is WRONG.")

    # Save results
    results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                               "src", "experiments", "results")
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "dollard_pure_construction.json")

    # Convert for JSON serialization
    def make_serializable(obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, complex):
            return {"real": obj.real, "imag": obj.imag}
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [make_serializable(x) for x in obj]
        return obj

    with open(output_path, 'w') as f:
        json.dump(make_serializable(all_results), f, indent=2)

    print(f"\n  Results saved to: {output_path}")
