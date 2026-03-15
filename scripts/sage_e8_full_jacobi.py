#!/usr/bin/env python3
"""
Full Jacobi verification for E₈ structure constants.
Checks ALL C(248,3) = 2,511,496 ordered triples.
Pure Python — no SageMath needed (reads from JSON).
"""

import json
import os
import sys
import time


def main():
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'research', 'e8-construction', 'e8_structure_constants.json')

    print(f"Loading {json_path}...")
    with open(json_path) as f:
        data = json.load(f)

    print(f"  Dimension: {data['dimension']}, Nonzero brackets: {data['nonzero_brackets']}")

    # Parse structure constants
    sc = {}
    for key_str, terms in data['structure_constants'].items():
        i, j = map(int, key_str.split(','))
        sc[(i, j)] = [(k, c) for k, c in terms]

    n = data['dimension']

    def bracket(i, j):
        if i == j:
            return []
        if i < j:
            return sc.get((i, j), [])
        else:
            return [(k, -c) for k, c in sc.get((j, i), [])]

    def bracket_with_vec(i, vec):
        result = {}
        for k, c_k in vec:
            for m, c_m in bracket(i, k):
                result[m] = result.get(m, 0) + c_k * c_m
        return [(m, c) for m, c in result.items() if c != 0]

    total = n * (n - 1) * (n - 2) // 6
    print(f"\nChecking ALL {total:,} ordered triples (i < j < k)...")

    failures = 0
    count = 0
    t0 = time.time()
    checkpoint = max(1, total // 20)

    for i in range(n):
        for j in range(i + 1, n):
            bij = bracket(i, j)
            for k in range(j + 1, n):
                count += 1
                if count % checkpoint == 0:
                    elapsed = time.time() - t0
                    rate = count / elapsed if elapsed > 0 else 0
                    eta = (total - count) / rate if rate > 0 else 0
                    print(f"  {count:,}/{total:,} ({100*count//total}%) "
                          f"[{elapsed:.0f}s elapsed, ~{eta:.0f}s remaining]")

                bjk = bracket(j, k)
                term1 = bracket_with_vec(i, bjk)
                bki = bracket(k, i)
                term2 = bracket_with_vec(j, bki)
                term3 = bracket_with_vec(k, bij)

                tot = {}
                for terms in [term1, term2, term3]:
                    for m, c in terms:
                        tot[m] = tot.get(m, 0) + c
                nonzero = {m: c for m, c in tot.items() if c != 0}

                if nonzero:
                    failures += 1
                    if failures <= 10:
                        print(f"  JACOBI FAILURE #{failures}: ({i},{j},{k}) -> {nonzero}")

    elapsed = time.time() - t0
    print(f"\nChecked {count:,} triples in {elapsed:.1f}s")

    if failures == 0:
        print(f"FULL JACOBI: PASSED (0/{total:,} failures)")
        print("E8 structure constants are VERIFIED.")
    else:
        print(f"FULL JACOBI: FAILED ({failures}/{total:,} failures)")

    return 0 if failures == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
