"""
Diagnose the transpose convention for adjoint matrices.

Standard convention: ad(X)_{a,b} = f^a_{Xb}  where [X, B_b] = sum_a f^a_{Xb} B_a
  => (k,j) entry = f^k_{ij}

Transposed convention: ad(X)_{j,k} = f^k_{Xj}
  => (j,k) entry = f^k_{ij}

Test: which convention makes [ad(X), ad(Y)] = ad([X,Y])?
"""

from sage.all import *
import json
import os


def main():
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'research', 'e8-construction', 'e8_structure_constants.json')
    with open(json_path) as f:
        data = json.load(f)

    sc = {}
    for key_str, terms in data['structure_constants'].items():
        i, j = map(int, key_str.split(','))
        sc[(i, j)] = [(k, c) for k, c in terms]

    n = 248

    def get_bracket(i, j):
        if i == j:
            return []
        if i < j:
            return sc.get((i, j), [])
        else:
            return [(_k, -_c) for _k, _c in sc.get((j, i), [])]

    # Build matrices BOTH ways for first 3 basis elements
    # Convention A: M[k, j] = f^k_{ij}  (standard)
    # Convention B: M[j, k] = f^k_{ij}  (transposed)

    def build_ad_standard(basis_idx):
        M = matrix(ZZ, n, n, sparse=True)
        for j in range(n):
            terms = get_bracket(basis_idx, j)
            for k, c in terms:
                M[k, j] = c  # standard: row=output component, col=input
        return M

    def build_ad_transposed(basis_idx):
        M = matrix(ZZ, n, n, sparse=True)
        for j in range(n):
            terms = get_bracket(basis_idx, j)
            for k, c in terms:
                M[j, k] = c  # transposed
        return M

    # Test pair (8, 9) - first positive root pair
    i, j = 8, 9
    bracket_ij = get_bracket(i, j)
    print(f"[B_{i}, B_{j}] = {bracket_ij}")

    print("\n=== Convention A: M[k,j] = f^k_ij (standard) ===")
    ad_A_i = build_ad_standard(i)
    ad_A_j = build_ad_standard(j)
    comm_A = ad_A_i * ad_A_j - ad_A_j * ad_A_i

    expected_A = matrix(ZZ, n, n, sparse=True)
    for k, c in bracket_ij:
        expected_A += c * build_ad_standard(k)

    diff_A = comm_A - expected_A
    print(f"  [ad(B_{i}), ad(B_{j})] == ad([B_{i},B_{j}])? {diff_A == 0}")

    print("\n=== Convention B: M[j,k] = f^k_ij (transposed) ===")
    ad_B_i = build_ad_transposed(i)
    ad_B_j = build_ad_transposed(j)
    comm_B = ad_B_i * ad_B_j - ad_B_j * ad_B_i

    expected_B = matrix(ZZ, n, n, sparse=True)
    for k, c in bracket_ij:
        expected_B += c * build_ad_transposed(k)

    diff_B = comm_B - expected_B
    print(f"  [ad(B_{i}), ad(B_{j})] == ad([B_{i},B_{j}])? {diff_B == 0}")

    # Check if transposed gives negative
    neg_expected_B = matrix(ZZ, n, n, sparse=True)
    for k, c in bracket_ij:
        neg_expected_B += c * build_ad_transposed(k)
    diff_neg_B = comm_B + neg_expected_B
    print(f"  [ad(B_{i}), ad(B_{j})] == -ad([B_{i},B_{j}])? {diff_neg_B == 0}")


if __name__ == '__main__':
    main()
