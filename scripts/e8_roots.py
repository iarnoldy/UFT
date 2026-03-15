#!/usr/bin/env python3
"""
E₈ Root System — Direct Construction
======================================

Constructs all 240 roots of E₈ directly from the mathematical definition,
bypassing SymPy's buggy all_roots() (which returns only 126 distinct vectors).

The E₈ roots in R^8 are:
  Type 1: +/- e_i +/- e_j  (i < j)  → 4 * C(8,2) = 112 roots
  Type 2: (1/2)(eps_1, ..., eps_8)  with eps_i = +/-1 and product(eps_i) = +1
           → 2^7 = 128 roots

Total: 240 roots.

Simple roots (standard choice matching SymPy's Cartan matrix):
  alpha_1 = (1/2, -1/2, -1/2, -1/2, -1/2, -1/2, -1/2, 1/2)
  alpha_2 = (1, 1, 0, 0, 0, 0, 0, 0)
  alpha_3 = (-1, 1, 0, 0, 0, 0, 0, 0)
  alpha_4 = (0, -1, 1, 0, 0, 0, 0, 0)
  alpha_5 = (0, 0, -1, 1, 0, 0, 0, 0)
  alpha_6 = (0, 0, 0, -1, 1, 0, 0, 0)
  alpha_7 = (0, 0, 0, 0, -1, 1, 0, 0)
  alpha_8 = (0, 0, 0, 0, 0, -1, 1, 0)
"""

from fractions import Fraction
from itertools import combinations
from sympy import Matrix as SympyMatrix


def construct_e8_roots():
    """Construct all 240 E₈ roots in R^8 with exact rational arithmetic."""
    roots = set()
    half = Fraction(1, 2)

    # Type 1: +/- e_i +/- e_j  (i != j)
    for i in range(8):
        for j in range(i + 1, 8):
            for si in [1, -1]:
                for sj in [1, -1]:
                    vec = [Fraction(0)] * 8
                    vec[i] = Fraction(si)
                    vec[j] = Fraction(sj)
                    roots.add(tuple(vec))

    # Type 2: (1/2)(eps_1, ..., eps_8) with product = +1
    for bits in range(256):  # 2^8 sign patterns
        eps = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        product = 1
        for e in eps:
            product *= e
        if product == 1:  # even number of -1's
            vec = tuple(half * e for e in eps)
            roots.add(vec)

    return roots


def get_simple_roots():
    """Return the 8 simple roots of E₈ (matching standard Cartan matrix)."""
    half = Fraction(1, 2)
    return {
        1: (half, -half, -half, -half, -half, -half, -half, half),
        2: (Fraction(1), Fraction(1), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        3: (Fraction(-1), Fraction(1), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        4: (Fraction(0), Fraction(-1), Fraction(1), Fraction(0),
            Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        5: (Fraction(0), Fraction(0), Fraction(-1), Fraction(1),
            Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        6: (Fraction(0), Fraction(0), Fraction(0), Fraction(-1),
            Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        7: (Fraction(0), Fraction(0), Fraction(0), Fraction(0),
            Fraction(-1), Fraction(1), Fraction(0), Fraction(0)),
        8: (Fraction(0), Fraction(0), Fraction(0), Fraction(0),
            Fraction(0), Fraction(-1), Fraction(1), Fraction(0)),
    }


def ip(a, b):
    """Standard Euclidean inner product."""
    return sum(x * y for x, y in zip(a, b))


def build_cartan_matrix(simple_roots):
    """Compute Cartan matrix from simple roots."""
    n = len(simple_roots)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            si = simple_roots[i + 1]
            sj = simple_roots[j + 1]
            A[i][j] = int(ip(si, sj) * 2 / ip(sj, sj))
    return A


def roots_to_simple_coords(roots, simple_roots, cartan_matrix):
    """
    Express each root as an integer combination of simple roots.
    Returns dict: root_vector -> tuple of integer coordinates.
    """
    n = len(simple_roots)

    # Exact inverse of Cartan matrix
    A_inv = SympyMatrix(cartan_matrix).inv()

    result = {}
    for root_vec in roots:
        # Compute <root, alpha_i^v> for each simple root
        alpha_check = []
        for i in range(n):
            si = simple_roots[i + 1]
            norm_sq = ip(si, si)
            alpha_check.append(ip(root_vec, si) * 2 / norm_sq)

        # coords = A_inv @ alpha_check
        coords = tuple(
            int(sum(Fraction(A_inv[i, j]) * alpha_check[j] for j in range(n)))
            for i in range(n)
        )

        # Verify: coords are integers and reconstruct the root
        reconstructed = tuple(
            sum(coords[i] * simple_roots[i + 1][k] for i in range(n))
            for k in range(8)
        )
        assert reconstructed == root_vec, \
            f"Reconstruction failed: {root_vec} -> coords {coords} -> {reconstructed}"

        result[root_vec] = coords

    return result


def classify_positive_negative(root_coords):
    """Classify roots as positive or negative by first nonzero coordinate."""
    positive = {}  # coords -> vector
    negative = {}

    for vec, coords in root_coords.items():
        is_pos = None
        for c in coords:
            if c > 0:
                is_pos = True
                break
            elif c < 0:
                is_pos = False
                break

        if is_pos:
            positive[coords] = vec
        else:
            negative[coords] = vec

    return positive, negative


if __name__ == '__main__':
    print("Constructing E8 root system...")
    roots = construct_e8_roots()
    print(f"  Total roots: {len(roots)} (expected 240)")
    assert len(roots) == 240, f"Expected 240 roots, got {len(roots)}"

    simple = get_simple_roots()
    cartan = build_cartan_matrix(simple)
    print(f"  Cartan matrix diagonal: {[cartan[i][i] for i in range(8)]}")

    print("  Converting to simple root coordinates...")
    root_coords = roots_to_simple_coords(roots, simple, cartan)
    print(f"  All {len(root_coords)} roots converted (reconstruction verified)")

    positive, negative = classify_positive_negative(root_coords)
    print(f"  Positive: {len(positive)}, Negative: {len(negative)}")
    assert len(positive) == 120
    assert len(negative) == 120

    print("\nE8 root system: VERIFIED")
    print(f"  240 roots, 120 positive, 120 negative")
    print(f"  All roots are integer combinations of simple roots")
    print(f"  All reconstructions verified exactly")
