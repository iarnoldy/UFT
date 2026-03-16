"""
Cross-verification: Build adjoint matrices from JSON, verify against SageMath.

This script:
1. Loads structure constants from JSON
2. Builds 248x248 adjoint matrices from them
3. Asks SageMath to compute the same adjoint matrices independently
4. Compares entry-by-entry
5. Tests a few bracket equations (M_i * M_j - M_j * M_i = sum f^k_{ij} M_k)

If this passes, the Lean generator will produce correct matrices.
"""

from sage.all import *
import json
import os
import sys
import time


def main():
    t0 = time.time()

    # ── Load JSON ──
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'research', 'e8-construction', 'e8_structure_constants.json')
    print(f"Loading {json_path}...")
    with open(json_path) as f:
        data = json.load(f)

    sc = {}
    for key_str, terms in data['structure_constants'].items():
        i, j = map(int, key_str.split(','))
        sc[(i, j)] = [(k, c) for k, c in terms]

    # ── Build adjoint matrices from JSON ──
    print("\n[1/4] Building adjoint matrices from JSON structure constants...")
    n = 248
    ad_json = []  # ad_json[i] = 248x248 matrix for ad(B_i)

    for i in range(n):
        M = matrix(ZZ, n, n, sparse=True)
        for j in range(n):
            if i == j:
                continue
            if i < j:
                terms = sc.get((i, j), [])
                for k, c in terms:
                    M[k, j] = c
            else:
                terms = sc.get((j, i), [])
                for k, c in terms:
                    M[k, j] = -c
        ad_json.append(M)

    print(f"  Built {len(ad_json)} adjoint matrices")

    # ── Build adjoint matrices from SageMath directly ──
    print("\n[2/4] Building adjoint matrices from SageMath Lie algebra...")
    L = LieAlgebra(QQ, cartan_type=['E', 8])
    R = RootSystem(['E', 8])
    root_lattice = R.root_lattice()
    alpha = root_lattice.simple_roots()
    alphacheck = root_lattice.simple_coroots()

    pos_roots_unsorted = list(root_lattice.positive_roots())
    def root_sort_key(r):
        coeffs = tuple(r.coefficient(i) for i in range(1, 9))
        return (sum(coeffs), coeffs)

    pos_roots = sorted(pos_roots_unsorted, key=root_sort_key)
    neg_roots = [-r for r in pos_roots]

    B = L.basis()

    # Build ordered basis (same order as JSON)
    basis_list = []
    for i in range(1, 9):
        basis_list.append(B[alphacheck[i]])
    for r in pos_roots:
        basis_list.append(B[r])
    for r in neg_roots:
        basis_list.append(B[r])

    assert len(basis_list) == 248

    # Build root-to-index map for decomposition
    root_to_idx = {}
    for i in range(1, 9):
        root_to_idx[alphacheck[i]] = i - 1
    for idx, r in enumerate(pos_roots):
        root_to_idx[r] = 8 + idx
    for idx, r in enumerate(neg_roots):
        root_to_idx[r] = 128 + idx

    # Build adjoint matrices from SageMath
    ad_sage = []
    for i in range(n):
        M = matrix(ZZ, n, n, sparse=True)
        for j in range(n):
            if i == j:
                continue
            bracket = basis_list[i].bracket(basis_list[j])
            if bracket.is_zero():
                continue
            mc = bracket.monomial_coefficients()
            for key, coeff in mc.items():
                if key in root_to_idx:
                    k = root_to_idx[key]
                    M[k, j] = int(coeff)
        ad_sage.append(M)

    print(f"  Built {len(ad_sage)} adjoint matrices from SageMath")

    # ── Compare entry by entry ──
    print("\n[3/4] Comparing JSON vs SageMath adjoint matrices...")
    mismatches = 0
    for i in range(n):
        diff = ad_json[i] - ad_sage[i]
        if diff != 0:
            mismatches += 1
            # Find first mismatch
            for j in range(n):
                for k in range(n):
                    if diff[j, k] != 0:
                        print(f"  MISMATCH at ad[{i}][{j},{k}]: "
                              f"JSON={ad_json[i][j,k]}, SageMath={ad_sage[i][j,k]}")
                        break
                else:
                    continue
                break
            if mismatches >= 10:
                print("  ... (stopping after 10 mismatches)")
                break

    if mismatches == 0:
        print(f"  ALL 248 adjoint matrices match perfectly.")
    else:
        print(f"  {mismatches} matrices have mismatches!")
        return 1

    # ── Test bracket equations: M_i * M_j - M_j * M_i = sum_k f^k_{ij} M_k ──
    print("\n[4/4] Testing bracket equations (50 random pairs)...")
    import random
    random.seed(42)

    pairs = list(sc.keys())
    test_pairs = random.sample(pairs, min(50, len(pairs)))
    bracket_failures = 0

    for i, j in test_pairs:
        # Compute commutator
        commutator = ad_json[i] * ad_json[j] - ad_json[j] * ad_json[i]

        # Compute expected: sum_k f^k_{ij} M_k
        expected = matrix(ZZ, n, n, sparse=True)
        for k, c in sc[(i, j)]:
            expected += c * ad_json[k]

        if commutator != expected:
            bracket_failures += 1
            print(f"  BRACKET FAILURE: [{i},{j}]")
            if bracket_failures >= 5:
                break

    if bracket_failures == 0:
        print(f"  All 50 bracket equations verified.")
    else:
        print(f"  {bracket_failures} bracket failures!")
        return 1

    # ── Bonus: test 10 zero brackets ──
    print("  Testing 10 zero-bracket pairs...")
    all_pairs = set(sc.keys())
    zero_tested = 0
    for i in range(n):
        for j in range(i+1, n):
            if (i, j) not in all_pairs:
                commutator = ad_json[i] * ad_json[j] - ad_json[j] * ad_json[i]
                if commutator != 0:
                    print(f"  ZERO FAILURE: [{i},{j}] should be zero but isn't!")
                    return 1
                zero_tested += 1
                if zero_tested >= 10:
                    break
        if zero_tested >= 10:
            break
    print(f"  All {zero_tested} zero-bracket pairs confirmed zero.")

    # ── Summary ──
    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"VERIFICATION PASSED")
    print(f"{'='*60}")
    print(f"  248 adjoint matrices: JSON matches SageMath exactly")
    print(f"  50 nonzero bracket equations: all correct")
    print(f"  10 zero bracket equations: all correct")
    print(f"  Time: {elapsed:.1f}s")
    print(f"\nJSON structure constants are CORRECT for Lean code generation.")

    # ── Output matrix statistics for Lean chunking ──
    print(f"\n--- Matrix Statistics for Lean Generator ---")
    total_nonzero = sum(len(ad_json[i].nonzero_positions()) for i in range(n))
    print(f"  Total nonzero entries across all 248 matrices: {total_nonzero}")
    avg_nnz = total_nonzero / n
    print(f"  Average nonzero entries per matrix: {avg_nnz:.1f}")
    max_nnz = max(len(ad_json[i].nonzero_positions()) for i in range(n))
    print(f"  Max nonzero entries in single matrix: {max_nnz}")
    min_nnz = min(len(ad_json[i].nonzero_positions()) for i in range(n))
    print(f"  Min nonzero entries in single matrix: {min_nnz}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
