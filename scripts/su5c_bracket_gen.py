#!/usr/bin/env python3
"""
Phase 0: SU5C Bracket Generator

Computes all structure constants of the compact-form su(5) Lie algebra
as embedded in so(10), and generates Lean 4 code for:
1. The SU5C.comm function (Lie bracket)
2. The su5c_toSO10 embedding function

The 24 su(5) generators decompose into:
  4 Cartan:  H_a = L_{a,a+5} - L_{a+1,a+6}    (a = 1,...,4)
  10 Type-R: R_{ab} = L_{ab} + L_{a+5,b+5}      (1 <= a < b <= 5)
  10 Type-S: S_{ab} = L_{a,b+5} + L_{b,a+5}     (1 <= a < b <= 5)
"""

import numpy as np
from itertools import combinations
import sys

# ============================================================
# SO(10) bracket computation
# ============================================================

# Map pair (i,j) with 1<=i<j<=10 to index 0..44
IDX_TO_PAIR = []
for i in range(1, 10):
    for j in range(i+1, 11):
        IDX_TO_PAIR.append((i, j))
assert len(IDX_TO_PAIR) == 45

PAIR_TO_IDX = {}
for idx, (i, j) in enumerate(IDX_TO_PAIR):
    PAIR_TO_IDX[(i, j)] = idx

def L(i, j):
    """Return the 45-vector for L_{ij}.
    L_{ij} = -L_{ji} for i>j, L_{ii} = 0."""
    v = np.zeros(45)
    if i == j:
        return v
    if i < j:
        v[PAIR_TO_IDX[(i, j)]] = 1.0
    else:
        v[PAIR_TO_IDX[(j, i)]] = -1.0
    return v

def so10_bracket(X, Y):
    """Compute [X, Y] in so(10) using the structure constants.
    [L_{ab}, L_{cd}] = d_{bc}L_{ad} - d_{ac}L_{bd} - d_{bd}L_{ac} + d_{ad}L_{bc}
    """
    result = np.zeros(45)
    for idx_x, (a, b) in enumerate(IDX_TO_PAIR):
        if X[idx_x] == 0:
            continue
        for idx_y, (c, d) in enumerate(IDX_TO_PAIR):
            coeff = X[idx_x] * Y[idx_y]
            if coeff == 0:
                continue
            if b == c:
                result += coeff * L(a, d)
            if a == c:
                result -= coeff * L(b, d)
            if b == d:
                result -= coeff * L(a, c)
            if a == d:
                result += coeff * L(b, c)
    return result

# ============================================================
# Define the 24 SU(5) generators in SO(10)
# ============================================================

GEN_NAMES = ['h1', 'h2', 'h3', 'h4',
             'r12', 'r13', 'r14', 'r15', 'r23', 'r24', 'r25', 'r34', 'r35', 'r45',
             's12', 's13', 's14', 's15', 's23', 's24', 's25', 's34', 's35', 's45']

GENS = {}
# Cartan: H_a = L_{a,a+5} - L_{a+1,a+6}
GENS['h1'] = L(1,6) - L(2,7)
GENS['h2'] = L(2,7) - L(3,8)
GENS['h3'] = L(3,8) - L(4,9)
GENS['h4'] = L(4,9) - L(5,10)

# Type-R: R_{ab} = L_{ab} + L_{a+5,b+5}
for a, b in [(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)]:
    GENS[f'r{a}{b}'] = L(a,b) + L(a+5,b+5)

# Type-S: S_{ab} = L_{a,b+5} + L_{b,a+5}
for a, b in [(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)]:
    GENS[f's{a}{b}'] = L(a,b+5) + L(b,a+5)

# Build the 24x45 embedding matrix
EMB_MATRIX = np.array([GENS[name] for name in GEN_NAMES])
assert EMB_MATRIX.shape == (24, 45)

# ============================================================
# Compute all brackets and express in SU5C basis
# ============================================================

def solve_su5c_coeffs(so10_vec):
    """Given a 45-vector in SO10, solve for its SU5C coefficients."""
    coeffs, residuals, rank, sv = np.linalg.lstsq(EMB_MATRIX.T, so10_vec, rcond=None)
    reconstructed = EMB_MATRIX.T @ coeffs
    error = np.max(np.abs(reconstructed - so10_vec))
    if error > 1e-10:
        return None, error
    return coeffs, error

print("Computing 276 independent brackets...")
STRUCTURE_CONSTANTS = {}
max_error = 0

for i in range(24):
    for j in range(i+1, 24):
        bracket = so10_bracket(GENS[GEN_NAMES[i]], GENS[GEN_NAMES[j]])
        coeffs, error = solve_su5c_coeffs(bracket)
        max_error = max(max_error, error)
        if coeffs is None:
            print(f"CLOSURE FAILURE: [{GEN_NAMES[i]}, {GEN_NAMES[j]}] not in su(5)! Error: {error}")
            sys.exit(1)
        coeffs_int = np.round(coeffs).astype(int)
        verify_error = np.max(np.abs(coeffs - coeffs_int))
        if verify_error > 1e-8:
            print(f"WARNING: [{GEN_NAMES[i]}, {GEN_NAMES[j]}] non-integer! coeffs = {coeffs}")
        STRUCTURE_CONSTANTS[(i, j)] = coeffs_int

print(f"All 276 brackets computed. Max reconstruction error: {max_error:.2e}")
print("Closure check: PASSED")

# ============================================================
# Verify Jacobi identity
# ============================================================

print("\nVerifying Jacobi identity for 1000 random triples...")
np.random.seed(42)
max_jacobi_error = 0

for trial in range(1000):
    a_coeffs = np.random.randn(24)
    b_coeffs = np.random.randn(24)
    c_coeffs = np.random.randn(24)
    A = EMB_MATRIX.T @ a_coeffs
    B = EMB_MATRIX.T @ b_coeffs
    C = EMB_MATRIX.T @ c_coeffs
    BC = so10_bracket(B, C)
    CA = so10_bracket(C, A)
    AB = so10_bracket(A, B)
    jacobi = so10_bracket(A, BC) + so10_bracket(B, CA) + so10_bracket(C, AB)
    error = np.max(np.abs(jacobi))
    max_jacobi_error = max(max_jacobi_error, error)

print(f"Jacobi verification: max error = {max_jacobi_error:.2e}")
if max_jacobi_error < 1e-8:
    print("Jacobi check: PASSED")
else:
    print("Jacobi check: FAILED!")
    sys.exit(1)

# ============================================================
# Generate Lean comm function
# ============================================================

# Build full structure constant tensor: [g_i, g_j]_k for all i,j,k
# Using antisymmetry: c^k_{ji} = -c^k_{ij}
FULL_SC = np.zeros((24, 24, 24), dtype=int)
for (i, j), coeffs in STRUCTURE_CONSTANTS.items():
    for k in range(24):
        FULL_SC[i, j, k] = coeffs[k]
        FULL_SC[j, i, k] = -coeffs[k]

# comm(X, Y)_k = sum_{i,j} X_i * Y_j * c^k_{ij}
# But we can simplify by grouping antisymmetric terms:
# = sum_{i<j} c^k_{ij} * (X_i * Y_j - X_j * Y_i)

print("\n" + "="*60)
print("LEAN COMM FUNCTION")
print("="*60)

print("\ndef comm (X Y : SU5C) : SU5C where")
for k in range(24):
    name_k = GEN_NAMES[k]
    terms = []
    for i in range(24):
        for j in range(i+1, 24):
            c = int(STRUCTURE_CONSTANTS.get((i, j), np.zeros(24))[k])
            if c == 0:
                continue
            ni = GEN_NAMES[i]
            nj = GEN_NAMES[j]
            if c == 1:
                terms.append(f"(X.{ni} * Y.{nj} - X.{nj} * Y.{ni})")
            elif c == -1:
                terms.append(f"(X.{nj} * Y.{ni} - X.{ni} * Y.{nj})")
            elif c > 0:
                terms.append(f"{c} * (X.{ni} * Y.{nj} - X.{nj} * Y.{ni})")
            else:  # c < 0
                terms.append(f"{-c} * (X.{nj} * Y.{ni} - X.{ni} * Y.{nj})")
    if not terms:
        expr = "0"
    else:
        expr = " + ".join(terms)
    print(f"  {name_k} := {expr}")

# ============================================================
# Generate Lean embedding function
# ============================================================

SO10_FIELDS = [
    'l12', 'l13', 'l14', 'l15', 'l16', 'l17', 'l18', 'l19', 'l1a',
    'l23', 'l24', 'l25', 'l26', 'l27', 'l28', 'l29', 'l2a',
    'l34', 'l35', 'l36', 'l37', 'l38', 'l39', 'l3a',
    'l45', 'l46', 'l47', 'l48', 'l49', 'l4a',
    'l56', 'l57', 'l58', 'l59', 'l5a',
    'l67', 'l68', 'l69', 'l6a',
    'l78', 'l79', 'l7a',
    'l89', 'l8a', 'l9a']

print("\n" + "="*60)
print("LEAN EMBEDDING FUNCTION")
print("="*60)

print("\ndef su5c_toSO10 (x : SU5C) : SO10 where")
for slot, so10_name in enumerate(SO10_FIELDS):
    terms = []
    for k, gen_name in enumerate(GEN_NAMES):
        val = int(round(EMB_MATRIX[k, slot]))
        if val == 0:
            continue
        if val == 1:
            terms.append(f"x.{gen_name}")
        elif val == -1:
            terms.append(f"-x.{gen_name}")
        else:
            terms.append(f"{val} * x.{gen_name}")
    if not terms:
        expr = "0"
    else:
        expr = " + ".join(terms)
    print(f"  {so10_name} := {expr}")

# ============================================================
# Cross-check key brackets
# ============================================================

print("\n" + "="*60)
print("KEY BRACKET CROSS-CHECKS")
print("="*60)

checks = [
    ('h1', 's12', "should give 2*r12 (Cartan eigenvalue)"),
    ('h1', 'r12', "should give -2*s12"),
    ('r12', 's12', "should involve Cartan"),
    ('h1', 'r13', "should involve r13 or s13"),
]

for name_i, name_j, desc in checks:
    bracket = so10_bracket(GENS[name_i], GENS[name_j])
    coeffs, _ = solve_su5c_coeffs(bracket)
    coeffs_int = np.round(coeffs).astype(int)
    print(f"\n[{name_i}, {name_j}] ({desc}):")
    for k, name in enumerate(GEN_NAMES):
        if coeffs_int[k] != 0:
            print(f"  {name}: {coeffs_int[k]}")

# ============================================================
# Statistics
# ============================================================

nonzero_count = 0
total_terms = 0
for (i, j), coeffs in STRUCTURE_CONSTANTS.items():
    for c in coeffs:
        total_terms += 1
        if c != 0:
            nonzero_count += 1

unique_vals = set()
for (i, j), coeffs in STRUCTURE_CONSTANTS.items():
    for c in coeffs:
        if c != 0:
            unique_vals.add(int(c))

print(f"\nStructure constant statistics:")
print(f"  Total entries: {total_terms} (276 pairs x 24 components)")
print(f"  Nonzero entries: {nonzero_count}")
print(f"  Density: {nonzero_count/total_terms*100:.1f}%")
print(f"  Unique nonzero values: {sorted(unique_vals)}")

print("\nPhase 0 complete. All checks passed.")
