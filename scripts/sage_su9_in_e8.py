#!/usr/bin/env python3
"""
Identify SU(9) = A₈ root indices inside E₈ Chevalley basis.
Uses EXACTLY the same root ordering as sage_e8_structure_constants.py:
  sorted by height, then lexicographically by coefficients on simple roots.
"""
from sage.all import *

RS = RootSystem(['E', 8])
Phi = RS.root_lattice()
alpha = Phi.simple_roots()
highest = Phi.highest_root()

# Sort positive roots EXACTLY as in sage_e8_structure_constants.py
pos_roots_unsorted = list(Phi.positive_roots())

def root_sort_key(r):
    coeffs = tuple(r.coefficient(i) for i in range(1, 9))
    height = sum(coeffs)
    return (height,) + coeffs

positive_roots = sorted(pos_roots_unsorted, key=root_sort_key)
print(f"E₈: {len(positive_roots)} positive roots (sorted by height+lex)")

# Verify first few match expected pattern
for i in range(5):
    r = positive_roots[i]
    coeffs = [r.coefficient(j) for j in range(1, 9)]
    print(f"  root {i}: {coeffs} (height {sum(coeffs)})")

# A₈ simple roots (from extended Dynkin diagram, removing node 2):
a8_simples = [
    alpha[1], alpha[3], alpha[4], alpha[5],
    alpha[6], alpha[7], alpha[8], -highest
]

# Build all A₈ roots by BFS
all_e8_roots = set()
for r in positive_roots:
    coeffs = tuple(r.coefficient(i) for i in range(1, 9))
    all_e8_roots.add(coeffs)
    all_e8_roots.add(tuple(-c for c in coeffs))

a8_roots = set()
for s in a8_simples:
    c = tuple(s.coefficient(i) for i in range(1, 9))
    if c in all_e8_roots: a8_roots.add(c)
    neg = tuple(-x for x in c)
    if neg in all_e8_roots: a8_roots.add(neg)

changed = True
while changed:
    changed = False
    for r in list(a8_roots):
        for s in a8_simples:
            sc = tuple(s.coefficient(i) for i in range(1, 9))
            for sign in [1, -1]:
                new = tuple(r[i] + sign * sc[i] for i in range(8))
                if new in all_e8_roots and new not in a8_roots:
                    a8_roots.add(new)
                    changed = True

print(f"\nA₈ roots: {len(a8_roots)} (expected 72)")
assert len(a8_roots) == 72

# Map to Chevalley basis indices using the SORTED ordering
pos_root_to_sorted_idx = {}
for i, r in enumerate(positive_roots):
    coeffs = tuple(r.coefficient(j) for j in range(1, 9))
    pos_root_to_sorted_idx[coeffs] = i

su9_indices = list(range(8))  # All 8 Cartan generators

for r in a8_roots:
    if r in pos_root_to_sorted_idx:
        idx = pos_root_to_sorted_idx[r]
        su9_indices.append(8 + idx)
    else:
        neg = tuple(-c for c in r)
        if neg in pos_root_to_sorted_idx:
            idx = pos_root_to_sorted_idx[neg]
            su9_indices.append(128 + idx)

su9_indices.sort()
print(f"SU(9) indices: {len(su9_indices)} (expected 80)")
assert len(su9_indices) == 80

# Verify: check a few brackets using the actual structure constants
# Load the structure constants from the JSON file
import json, os
json_path = os.path.join(os.path.dirname(__file__),
    '..', 'research', 'e8-construction', 'e8_structure_constants.json')
if os.path.exists(json_path):
    with open(json_path) as f:
        sc_data = json.load(f)
    brackets = sc_data.get('brackets', {})
    print(f"\nLoaded {len(brackets)} brackets from JSON for verification")

    # Verify closure: for every pair of SU(9) indices, check that
    # all bracket output indices are also SU(9)
    su9_set = set(su9_indices)
    violations = 0
    for i in su9_indices:
        for j in su9_indices:
            key = f"{i},{j}"
            if key in brackets:
                for term in brackets[key]:
                    out_idx = term[0]
                    if out_idx not in su9_set:
                        violations += 1
                        if violations <= 5:
                            print(f"  VIOLATION: [{i},{j}] -> index {out_idx} (not in SU9)")

    if violations == 0:
        print("CLOSURE VERIFIED in Python!")
    else:
        print(f"CLOSURE FAILED: {violations} violations")
else:
    print(f"\nJSON not found at {json_path} — skipping Python verification")

# Print Lean output
print(f"\n{'='*60}")
print(f"LEAN OUTPUT")
print(f"{'='*60}")
print(f"def isSU9 (n : Nat) : Bool :=")
print(f"  match n with")
for idx in su9_indices:
    print(f"  | {idx} => true")
print(f"  | _ => false")
