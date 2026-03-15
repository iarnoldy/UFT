#!/usr/bin/env sage
"""
E₈ Structure Constants via SageMath — Ground Truth Oracle
==========================================================

Uses SageMath's built-in Lie algebra machinery (GAP + Chevie) to compute
ALL structure constants of E₈ in the Chevalley basis. This bypasses the
sign problem that blocked 3 pure-Python approaches (Tits cocycle,
Jacobi derivation, Casselman-Kottwitz sign transfer).

SageMath computes correct signs because its internal implementation
builds the basis and signs simultaneously via extraspecial pairs
(Carter Ch4), which is the mathematically correct approach.

Output: JSON file with all nonzero bracket pairs for Lean 4 code generation.
Format matches e8_structure_constants.py output for downstream compatibility.

Run: wsl sage scripts/sage_e8_structure_constants.py

Basis ordering (248 elements):
  0-7:     H_1 .. H_8    (Cartan subalgebra, coroots alphacheck[i])
  8-127:   E_1 .. E_120  (positive root vectors, sorted by height then lex)
  128-247: F_1 .. F_120  (negative root vectors, same order as positive)
"""

from sage.all import *
import json
import os
import sys
import time

def main():
    t0 = time.time()

    print("=" * 60)
    print("E8 Structure Constants — SageMath Oracle")
    print("=" * 60)

    # ── Step 1: Construct E₈ Lie algebra ──
    print("\n[1/5] Constructing E8 Lie algebra (Chevalley basis)...")
    L = LieAlgebra(QQ, cartan_type=['E', 8])
    print(f"  Dimension: {L.dimension()}")
    assert L.dimension() == 248, f"Expected dim 248, got {L.dimension()}"

    # ── Step 2: Build ordered basis ──
    print("\n[2/5] Building ordered basis...")

    # Get the root system
    R = RootSystem(['E', 8])
    root_lattice = R.root_lattice()
    alpha = root_lattice.simple_roots()

    # Get all positive roots sorted by height then lexicographically
    pos_roots_unsorted = list(root_lattice.positive_roots())
    print(f"  Positive roots: {len(pos_roots_unsorted)}")
    assert len(pos_roots_unsorted) == 120

    def root_sort_key(r):
        """Sort by height, then by coefficients lexicographically."""
        coeffs = tuple(r.coefficient(i) for i in range(1, 9))
        return (sum(coeffs), coeffs)

    pos_roots = sorted(pos_roots_unsorted, key=root_sort_key)
    neg_roots = [-r for r in pos_roots]

    # Build basis list: H_1..H_8, E_1..E_120, F_1..F_120
    B = L.basis()

    # Identify basis elements
    # In SageMath's Chevalley basis:
    #   B[alpha[i]]       = e_i (positive simple root vector)
    #   B[-alpha[i]]      = f_i (negative simple root vector)
    #   B[alphacheck[i]]  = h_i (coroot / Cartan element)
    # For non-simple roots, the key is the root itself

    alphacheck = root_lattice.simple_coroots()

    basis_list = []
    basis_keys = []

    # Cartan elements (indices 0-7)
    for i in range(1, 9):
        basis_list.append(B[alphacheck[i]])
        basis_keys.append(f"H_{i}")

    # Positive root vectors (indices 8-127)
    for idx, r in enumerate(pos_roots):
        basis_list.append(B[r])
        coeffs = tuple(r.coefficient(i) for i in range(1, 9))
        basis_keys.append(f"E_{coeffs}")

    # Negative root vectors (indices 128-247)
    for idx, r in enumerate(neg_roots):
        basis_list.append(B[r])
        coeffs = tuple((-r).coefficient(i) for i in range(1, 9))
        basis_keys.append(f"F_{coeffs}")

    assert len(basis_list) == 248, f"Expected 248 basis elements, got {len(basis_list)}"
    print(f"  Basis: {len(basis_list)} elements (8 Cartan + 120 pos + 120 neg)")

    # ── Step 3: Compute all structure constants ──
    print("\n[3/5] Computing structure constants...")
    print(f"  Computing {248*247//2} bracket pairs...")

    # Build a map from basis element to index for decomposition
    # We need to express bracket results in terms of our ordered basis

    # First, build a lookup from root lattice element to basis index
    root_to_idx = {}
    for i in range(1, 9):
        root_to_idx[alphacheck[i]] = i - 1
    for idx, r in enumerate(pos_roots):
        root_to_idx[r] = 8 + idx
    for idx, r in enumerate(neg_roots):
        root_to_idx[r] = 128 + idx

    sc = {}  # (i, j) -> [(k, coeff), ...] for i < j
    total_nonzero = 0
    total_pairs = 248 * 247 // 2

    checkpoint = max(1, total_pairs // 10)
    pair_count = 0

    for i in range(248):
        for j in range(i + 1, 248):
            pair_count += 1
            if pair_count % checkpoint == 0:
                elapsed = time.time() - t0
                print(f"    {pair_count}/{total_pairs} ({100*pair_count//total_pairs}%) "
                      f"[{elapsed:.0f}s elapsed]")

            bracket = basis_list[i].bracket(basis_list[j])

            if bracket.is_zero():
                continue

            # Decompose bracket into basis coefficients
            terms = []
            mc = bracket.monomial_coefficients()
            for key, coeff in mc.items():
                if coeff == 0:
                    continue
                if key in root_to_idx:
                    terms.append((root_to_idx[key], int(coeff)))
                else:
                    print(f"  WARNING: Unknown key {key} in bracket [{i},{j}]")

            if terms:
                sc[(i, j)] = terms
                total_nonzero += 1

    elapsed = time.time() - t0
    print(f"  Done: {total_nonzero} nonzero bracket pairs in {elapsed:.1f}s")

    # Count by type
    hh = sum(1 for (i,j) in sc if i < 8 and j < 8)
    he = sum(1 for (i,j) in sc if i < 8 and j >= 8)
    ee_pp = sum(1 for (i,j) in sc if 8 <= i < 128 and 8 <= j < 128)
    ee_pn = sum(1 for (i,j) in sc if 8 <= i < 128 and j >= 128)
    ee_nn = sum(1 for (i,j) in sc if i >= 128 and j >= 128)
    print(f"  [H,H]: {hh}, [H,E]: {he}, [E+,E+]: {ee_pp}, "
          f"[E+,E-]: {ee_pn}, [E-,E-]: {ee_nn}")

    # ── Step 4: Verify Jacobi identity ──
    print("\n[4/5] Verifying Jacobi identity (1000 random triples)...")

    import random
    random.seed(42)

    def bracket_pair(i, j):
        """Get [B_i, B_j] as list of (index, coeff) pairs."""
        if i == j:
            return []
        if i < j:
            return sc.get((i, j), [])
        else:
            return [(k, -c) for k, c in sc.get((j, i), [])]

    def bracket_with_vec(i, vec):
        """Compute [B_i, vec] where vec is a list of (index, coeff)."""
        result = {}
        for k, c_k in vec:
            for m, c_m in bracket_pair(i, k):
                result[m] = result.get(m, 0) + c_k * c_m
        return [(m, c) for m, c in result.items() if c != 0]

    failures = 0
    n_samples = 1000
    for _ in range(n_samples):
        i, j, k = random.sample(range(248), 3)

        bjk = bracket_pair(j, k)
        term1 = bracket_with_vec(i, bjk)
        bki = bracket_pair(k, i)
        term2 = bracket_with_vec(j, bki)
        bij = bracket_pair(i, j)
        term3 = bracket_with_vec(k, bij)

        total = {}
        for terms in [term1, term2, term3]:
            for m, c in terms:
                total[m] = total.get(m, 0) + c
        nonzero = {m: c for m, c in total.items() if c != 0}

        if nonzero:
            failures += 1
            if failures <= 5:
                print(f"  JACOBI FAILURE #{failures}: ({i},{j},{k}) -> {nonzero}")

    if failures == 0:
        print(f"  Random Jacobi: PASSED (0/{n_samples})")
    else:
        print(f"  Random Jacobi: FAILED ({failures}/{n_samples})")
        print("  ABORTING — structure constants are incorrect.")
        return 1

    # ── Step 5: Save to JSON ──
    print("\n[5/5] Saving structure constants...")

    # Root coordinates for reference
    pos_root_coords = []
    for r in pos_roots:
        coords = [int(r.coefficient(i)) for i in range(1, 9)]
        pos_root_coords.append(coords)

    neg_root_coords = [[-c for c in coords] for coords in pos_root_coords]

    data = {
        'generator': 'sage_e8_structure_constants.py (SageMath oracle)',
        'rank': 8,
        'dimension': 248,
        'n_positive_roots': 120,
        'basis_ordering': [
            'H_1..H_8 (indices 0-7, Cartan coroots)',
            'E_{alpha_1}..E_{alpha_120} (indices 8-127, positive roots by height)',
            'F_{alpha_1}..F_{alpha_120} (indices 128-247, negatives in same order)',
        ],
        'positive_root_coords': pos_root_coords,
        'negative_root_coords': neg_root_coords,
        'nonzero_brackets': total_nonzero,
        'structure_constants': {},
    }

    for (i, j), terms in sorted(sc.items()):
        key = f"{i},{j}"
        data['structure_constants'][key] = [[k, c] for k, c in sorted(terms)]

    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'research', 'e8-construction')
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, 'e8_structure_constants.json')

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=1)

    file_size = os.path.getsize(json_path)
    print(f"  Saved to {json_path} ({file_size:,} bytes)")

    t_total = time.time() - t0
    print(f"\nTotal time: {t_total:.1f}s")
    print(f"Nonzero brackets: {total_nonzero}")
    print(f"\nSUCCESS. Structure constants verified (Jacobi 0/{n_samples}).")
    print("Next: Full Jacobi verification, then Lean code generation.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
