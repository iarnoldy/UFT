"""
Pinpoint: check if root ordering in JSON matches a fresh SageMath computation,
and trace specific bracket mismatches.
"""

from sage.all import *
import json
import os


def main():
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'research', 'e8-construction', 'e8_structure_constants.json')
    with open(json_path) as f:
        data = json.load(f)

    # Check root ordering
    R = RootSystem(['E', 8])
    root_lattice = R.root_lattice()

    pos_roots_unsorted = list(root_lattice.positive_roots())
    def root_sort_key(r):
        coeffs = tuple(r.coefficient(i) for i in range(1, 9))
        return (sum(coeffs), coeffs)

    pos_roots = sorted(pos_roots_unsorted, key=root_sort_key)

    json_coords = data['positive_root_coords']

    print("=== Root ordering comparison ===")
    mismatched = 0
    for idx, r in enumerate(pos_roots):
        sage_coords = [int(r.coefficient(i)) for i in range(1, 9)]
        json_c = json_coords[idx]
        if sage_coords != json_c:
            print(f"  ROOT MISMATCH at index {idx}: sage={sage_coords} json={json_c}")
            mismatched += 1
            if mismatched >= 5:
                break

    if mismatched == 0:
        print("  All 120 positive root orderings MATCH.")
    else:
        print(f"  {mismatched} root ordering mismatches!")
        return

    # Now check specific bracket: (8, 128)
    print("\n=== Bracket [B_8, B_128] ===")
    print(f"  B_8 = E_{{alpha_1}} with coords {json_coords[0]}")
    print(f"  B_128 = F_{{alpha_1}} (negative of above)")

    # From JSON
    sc_key = "8,128"
    json_terms = data['structure_constants'].get(sc_key, None)
    print(f"  JSON terms for ({sc_key}): {json_terms}")

    # From SageMath
    L = LieAlgebra(QQ, cartan_type=['E', 8])
    B = L.basis()
    alphacheck = root_lattice.simple_coroots()

    basis_list = []
    for i in range(1, 9):
        basis_list.append(B[alphacheck[i]])
    for r in pos_roots:
        basis_list.append(B[r])
    for r in [-r for r in pos_roots]:
        basis_list.append(B[r])

    bracket = basis_list[8].bracket(basis_list[128])
    print(f"  SageMath bracket: {bracket}")

    root_to_idx = {}
    for i in range(1, 9):
        root_to_idx[alphacheck[i]] = i - 1
    for idx, r in enumerate(pos_roots):
        root_to_idx[r] = 8 + idx
    for idx, r in enumerate([-r for r in pos_roots]):
        root_to_idx[r] = 128 + idx

    mc = bracket.monomial_coefficients()
    sage_terms = []
    for key, coeff in mc.items():
        if key in root_to_idx:
            sage_terms.append([root_to_idx[key], int(coeff)])
        else:
            print(f"  WARNING: key {key} not in root_to_idx!")
            print(f"  Key type: {type(key)}")
            # Try to identify what this key is
            print(f"  Key repr: {repr(key)}")
    sage_terms.sort()
    print(f"  SageMath terms (indexed): {sage_terms}")

    # Check all Cartan elements
    print("\n=== Cartan element identification ===")
    for i in range(1, 9):
        ac = alphacheck[i]
        idx = root_to_idx.get(ac, "NOT FOUND")
        print(f"  alphacheck[{i}] = {ac} -> index {idx}")

    # Check what keys the bracket has
    print(f"\n  Bracket mc keys: {list(mc.keys())}")
    print(f"  Bracket mc key types: {[type(k) for k in mc.keys()]}")
    for k in mc.keys():
        if k not in root_to_idx:
            print(f"  UNMAPPED KEY: {k}")
            # Check if it equals any alphacheck
            for i in range(1, 9):
                if k == alphacheck[i]:
                    print(f"    -> equals alphacheck[{i}]")
                    break
            else:
                print(f"    -> does NOT equal any alphacheck")


if __name__ == '__main__':
    main()
