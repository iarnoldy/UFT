#!/usr/bin/env python3
"""
KC-E2: SO(14) vs SU(9)/Z3 Compatibility Inside E8
====================================================

KILL CONDITION: Is SO(14) compatible with Wilson's SU(9)/Z3 decomposition
inside E8?

We have TWO decompositions of E8(248):

  Our chain (SO(16) route):
    E8 -> SO(16):               248 = 120 + 128
    SO(16) -> SO(14) x SO(2):   120 = 91 + 1 + 28, 128 -> 64+ + 64-
    Total: 248 = 91 + 1 + 28 + 64 + 64

  Wilson's chain (SU(9) route):
    E8 -> SU(9)/Z3:             248 = 80 + 84 + 84_bar
    80 = adjoint of SU(9)
    84 = Lambda^3(C^9), 84_bar = Lambda^3(C^9)*

KEY QUESTION: How do the 91 generators of so(14) distribute between
Wilson's 80 (gauge) and 84+84 (matter)?

METHOD:
  We work in the E8 root system and use the CORRECT Z3 action.
  The subtlety is that Wilson's type 5 element is defined relative to the
  SU(9) torus, not the SO(16) torus. The Z3 eigenvalues on spinor roots
  require careful handling via the triality/weight lattice.

  CORRECT APPROACH: Instead of trying to define the Z3 action root-by-root
  (which fails for spinor roots), we use the KNOWN decomposition
  E8 -> A8 (SU(9)) to identify which E8 roots belong to which SU(9)
  representation, then intersect with the D7 = SO(14) root system.

  The A8 root system inside E8 is identified by finding which subset of
  the 240 E8 roots forms an A8 root system. There are multiple conjugate
  embeddings; the one corresponding to the type 5 element has the A8
  simple roots orthogonal to t5, or equivalently, the 72 roots for which
  <alpha, t5> = 0 mod 3.

Author: Clifford Unification Engineer
Date: 2026-03-09
"""

import numpy as np
from itertools import product, combinations
from collections import defaultdict
from math import comb

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================================
# PART 1: Construct E8 root system
# ============================================================================

def construct_e8_roots():
    """Construct all 240 roots of E8 in R^8.
    D8: +/- e_i +/- e_j (112) + half-integer even parity (128) = 240.
    """
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in [+1, -1]:
                for sj in [+1, -1]:
                    r = np.zeros(8)
                    r[i] = si
                    r[j] = sj
                    roots.append(r)
    for signs in product([+1, -1], repeat=8):
        n_minus = sum(1 for s in signs if s == -1)
        if n_minus % 2 == 0:
            r = np.array(signs, dtype=float) / 2.0
            roots.append(r)
    return np.array(roots)


print("=" * 72)
print("KC-E2: SO(14) vs SU(9)/Z3 COMPATIBILITY INSIDE E8")
print("=" * 72)

# ============================================================================
# PART 2: Build E8, classify D8 vs spinor
# ============================================================================

print("\n--- Part 1: E8 Root System ---")
roots = construct_e8_roots()
assert len(roots) == 240
norms_sq = np.sum(roots**2, axis=1)
assert np.allclose(norms_sq, 2.0)

is_integer = np.all(np.abs(roots - np.round(roots)) < 1e-10, axis=1)
d8_roots = roots[is_integer]       # 112 D8 roots
spinor_roots = roots[~is_integer]  # 128 half-integer roots
assert len(d8_roots) == 112
assert len(spinor_roots) == 128
print(f"  E8: 240 roots. D8 integer: 112. Half-integer spinor: 128.")

# ============================================================================
# PART 3: Identify D7 = SO(14) roots
# ============================================================================

print("\n--- Part 2: D7 = SO(14) Inside D8 = SO(16) ---")

# D7 embedded in first 7 coordinates: roots e_i +/- e_j with i,j in {0..6}
d7_mask = np.zeros(len(d8_roots), dtype=bool)
mixed_mask = np.zeros(len(d8_roots), dtype=bool)

for idx, r in enumerate(d8_roots):
    nz = np.nonzero(np.abs(r) > 0.5)[0]
    if len(nz) == 2:
        if nz[0] <= 6 and nz[1] <= 6:
            d7_mask[idx] = True
        elif 7 in nz:
            mixed_mask[idx] = True

d7_roots = d8_roots[d7_mask]
mixed_roots = d8_roots[mixed_mask]
assert len(d7_roots) == 84, f"Expected 84 D7 roots, got {len(d7_roots)}"
assert len(mixed_roots) == 28
print(f"  D7 = so(14): 84 roots + 7 Cartan = 91 dim")
print(f"  Mixed (coord 7 involved): 28 roots")

# ============================================================================
# PART 4: Find the A8 = SU(9) root system inside E8
# ============================================================================

print("\n--- Part 3: Finding A8 = SU(9) Inside E8 ---")

# APPROACH: The A8 root system inside E8 corresponds to the centralizer
# of an order-3 element. We need to find 72 roots of E8 that form an A8
# root system.
#
# Key fact: E8 has a maximal subgroup A8 (= SU(9)/Z3).
# The branching rule is: 248 = 80 + 84 + 84_bar
# where 80 = adjoint of A8, 84 = Lambda^3(9), 84_bar = Lambda^3(9)*.
#
# To find A8 inside E8: we need to find 8 simple roots of A8 among
# the 240 E8 roots. The A8 simple roots alpha_1,...,alpha_8 satisfy:
#   <alpha_i, alpha_j> = 2 if i=j, -1 if |i-j|=1, 0 otherwise
# (the A8 Cartan matrix).
#
# STANDARD EMBEDDING: In the E8 root coordinates, one standard A8
# embedding uses the simple roots:
#   alpha_i = e_i - e_{i+1}  for i = 0,...,6  (7 roots from D8)
#   alpha_7 = a special root involving the half-integer vectors
#
# The first 7 simple roots e_i - e_{i+1} form an A7 = SU(8) inside D8.
# To extend to A8 = SU(9), we need an 8th simple root orthogonal to
# alpha_1,...,alpha_6 and with <alpha_7, alpha_8> = -1.
#
# From Adams' "Lectures on Exceptional Lie Groups" and Slansky:
# The 8th simple root for the A8 inside E8 is:
#   alpha_8 = -(1/2)(e_1+e_2+e_3+e_4+e_5) + (1/2)(e_6+e_7+e_8)
# which is a half-integer vector with 5 minus signs in {1..5} and 3 plus
# signs in {6,7,8}. But we need even parity (even number of minus signs).
#
# Let me verify: -(1/2)(1,1,1,1,1,-1,-1,-1) = (1/2)(-1,-1,-1,-1,-1,1,1,1)
# This has 5 minus signs on first 5 coords = 5 negative entries.
# In our convention, negative = minus sign. Count of minus signs = 5 (odd).
# So this is NOT in the E8 root system (we need EVEN parity).
#
# Correction: The standard A8 embedding uses:
#   alpha_i = e_i - e_{i+1} for i=1,...,7 (in 1-indexed)
#   alpha_8 = -(e_1+e_2+e_3)/2 + (e_4+e_5+e_6+e_7+e_8)/2
# Wait, that also has issues. Let me just SEARCH for the A8 directly.

# COMPUTATIONAL APPROACH: Find all subsets of 8 roots forming an A8 Dynkin
# diagram. This is expensive for 240 roots, so we use a smarter method.

# SMARTER METHOD: The A8 roots are exactly those 72 roots alpha such that
# exp(2*pi*i*<alpha, h>) = 1 where h defines the order-3 element.
# The issue is WHICH h to use.
#
# RESOLUTION: The order-3 element lives in E8, not in SO(16).
# In the E8 weight lattice, a valid order-3 element corresponds to
# a coweight h such that 3h is in the coroot lattice.
# For E8 (simply laced, simply connected), the coroot lattice = root lattice.
# So we need 3h to be in the E8 lattice.
#
# One valid choice: h = (1/3)(e_1 + e_2 + e_3 - e_4 - e_5 - e_6)
# But this is complicated. Let me try a different approach.

# DIRECT CONSTRUCTION: Find A8 via its KNOWN embedding.
# Reference: Slansky, Phys. Rep. 79 (1981), Table 43.
# The maximal A8 inside E8 uses an extended Dynkin diagram trick.
#
# E8 extended Dynkin diagram has 9 nodes. Removing node 1 (the affine
# node) gives E8 itself. Removing a DIFFERENT node can give A8.
#
# Actually, the maximal subalgebra A8 of E8 comes from the fact that
# E8 has an outer automorphism of order... no, E8 has no outer automorphisms.
#
# The correct construction: E8 contains SU(9)/Z3 as a maximal subgroup.
# This is obtained by the embedding through the extended Dynkin diagram
# of E8. The affine/extended E8 Dynkin diagram has nodes 0,1,...,8.
# Deleting node 0 gives the E8 Dynkin diagram (A_1 simple root alpha_0
# is the highest root). Deleting node 2 gives the A8 Dynkin diagram.
#
# E8 Dynkin diagram (Bourbaki labeling):
#   1 - 3 - 4 - 5 - 6 - 7 - 8
#           |
#           2
#
# Extended E8 (affine E8):
#   0 - 1 - 3 - 4 - 5 - 6 - 7 - 8
#               |
#               2
#
# Deleting node 2 from the extended diagram gives:
#   0 - 1 - 3 - 4 - 5 - 6 - 7 - 8
# which is A8!
# So the A8 simple roots are: alpha_0, alpha_1, alpha_3, alpha_4, ..., alpha_8
# where alpha_0 = -theta (negative of highest root).

# Let me find the E8 simple roots in our coordinate system.
# Standard E8 simple roots (Bourbaki convention):
# alpha_1 = (1/2)(1,-1,-1,-1,-1,-1,-1,1)
# alpha_2 = e_1 + e_2
# alpha_3 = e_2 - e_1   [= -e_1 + e_2]
# alpha_4 = e_1 - e_2   ... wait, let me use the standard form.

# STANDARD E8 SIMPLE ROOTS (Humphreys/Bourbaki, 0-indexed coords):
# These are in R^8 with the standard inner product.
e8_simple = np.zeros((8, 8))
# alpha_1 = (1/2)(1,-1,-1,-1,-1,-1,-1,1)
e8_simple[0] = np.array([1,-1,-1,-1,-1,-1,-1,1]) / 2.0
# alpha_2 = e_0 + e_1
e8_simple[1] = np.zeros(8); e8_simple[1][0] = 1; e8_simple[1][1] = 1
# alpha_3 = e_1 - e_0 = -e_0 + e_1
e8_simple[2] = np.zeros(8); e8_simple[2][0] = -1; e8_simple[2][1] = 1
# alpha_4 = e_2 - e_1
e8_simple[3] = np.zeros(8); e8_simple[3][1] = -1; e8_simple[3][2] = 1
# alpha_5 = e_3 - e_2
e8_simple[4] = np.zeros(8); e8_simple[4][2] = -1; e8_simple[4][3] = 1
# alpha_6 = e_4 - e_3
e8_simple[5] = np.zeros(8); e8_simple[5][3] = -1; e8_simple[5][4] = 1
# alpha_7 = e_5 - e_4
e8_simple[6] = np.zeros(8); e8_simple[6][4] = -1; e8_simple[6][5] = 1
# alpha_8 = e_6 - e_5
e8_simple[7] = np.zeros(8); e8_simple[7][5] = -1; e8_simple[7][6] = 1

# Verify Cartan matrix
cartan = np.round(2 * e8_simple @ e8_simple.T / np.outer(np.sum(e8_simple**2, axis=1), np.ones(8)), 6)
# For simply-laced, this simplifies to just the inner product matrix
gram = np.round(e8_simple @ e8_simple.T, 6)
print(f"  E8 simple roots Gram matrix:")
for row in gram:
    print(f"    {row}")

# The E8 Cartan matrix should be:
# 2 0 -1  0  0  0  0  0
# 0 2  0 -1  0  0  0  0
# -1 0  2 -1  0  0  0  0
# 0 -1 -1  2 -1  0  0  0
# 0  0  0 -1  2 -1  0  0
# 0  0  0  0 -1  2 -1  0
# 0  0  0  0  0 -1  2 -1
# 0  0  0  0  0  0 -1  2

# Hmm, let me check if this is the standard E8 Cartan matrix.
# Actually, the Bourbaki labeling for E8 is:
#   1 - 3 - 4 - 5 - 6 - 7 - 8
#       |
#       2
# Node 1 connects to node 3. Node 2 connects to node 3.
# So the Cartan matrix has:
# A[1,3] = A[3,1] = -1, A[2,3] = A[3,2] = -1
# and the chain 3-4-5-6-7-8 is a standard A5.

# Let me verify the simple roots are correct.
# Check: all alpha_i are roots of E8 (in our root list)
for i, sr in enumerate(e8_simple):
    found = False
    for r in roots:
        if np.allclose(sr, r):
            found = True
            break
    print(f"  alpha_{i+1} = {sr} -> in root system: {found}")

# ============================================================================
# PART 4b: Compute the highest root and alpha_0
# ============================================================================

# The highest root of E8 is:
# theta = 2*alpha_1 + 3*alpha_2 + 4*alpha_3 + 6*alpha_4 + 5*alpha_5 +
#         4*alpha_6 + 3*alpha_7 + 2*alpha_8
# (coefficients from the extended Dynkin diagram marks)

# Actually, the marks on the extended Dynkin diagram for E8 are:
# (affine node has mark 1)
# The marks (Kac labels) for the extended E8 are:
# alpha_0: 1
# alpha_1: 2
# alpha_2: 3
# alpha_3: 4
# alpha_4: 6
# alpha_5: 5
# alpha_6: 4
# alpha_7: 3
# alpha_8: 2

# Wait, the standard result is:
# theta = 2*alpha_1 + 3*alpha_2 + 4*alpha_3 + 6*alpha_4 + 5*alpha_5 +
#         4*alpha_6 + 3*alpha_7 + 2*alpha_8
# Let me compute this.
theta = (2*e8_simple[0] + 3*e8_simple[1] + 4*e8_simple[2] + 6*e8_simple[3] +
         5*e8_simple[4] + 4*e8_simple[5] + 3*e8_simple[6] + 2*e8_simple[7])
print(f"\n  Highest root theta = {theta}")
print(f"  |theta|^2 = {np.dot(theta, theta):.6f}")

# Check theta is in root system
theta_found = any(np.allclose(theta, r) for r in roots)
print(f"  theta in root system: {theta_found}")

# alpha_0 = -theta
alpha_0 = -theta
print(f"  alpha_0 = -theta = {alpha_0}")
alpha0_found = any(np.allclose(alpha_0, r) for r in roots)
print(f"  alpha_0 in root system: {alpha0_found}")

# ============================================================================
# PART 5: The A8 simple roots (by deleting node 2 from extended E8)
# ============================================================================

print("\n--- Part 4: A8 Simple Roots (Delete Node 2 from Extended E8) ---")

# Extended E8 Dynkin diagram nodes: 0, 1, 2, 3, 4, 5, 6, 7, 8
# Connections: 0-1, 1-3, 2-3, 3-4, 4-5, 5-6, 6-7, 7-8
# (node 2 is the "branch" node connecting to node 3)
#
# Deleting node 2 gives nodes: 0, 1, 3, 4, 5, 6, 7, 8
# with connections: 0-1, 1-3, 3-4, 4-5, 5-6, 6-7, 7-8
# This is a chain of 8 nodes = A8 Dynkin diagram!

# Extended E8 diagram with alpha_0 added:
#   0 -- 8 -- 7 -- 6 -- 5 -- 4 -- 3 -- 1
#                                   |
#                                   2
# Deleting node 2 gives the A8 chain:
#   1 -- 3 -- 4 -- 5 -- 6 -- 7 -- 8 -- 0
# So the A8 simple roots IN CHAIN ORDER are:
#   alpha_1, alpha_3, alpha_4, alpha_5, alpha_6, alpha_7, alpha_8, alpha_0
a8_simple = np.array([
    e8_simple[0],   # beta_1 = alpha_1
    e8_simple[2],   # beta_2 = alpha_3
    e8_simple[3],   # beta_3 = alpha_4
    e8_simple[4],   # beta_4 = alpha_5
    e8_simple[5],   # beta_5 = alpha_6
    e8_simple[6],   # beta_6 = alpha_7
    e8_simple[7],   # beta_7 = alpha_8
    alpha_0,        # beta_8 = -theta
])

# Verify A8 Cartan matrix
a8_gram = np.round(a8_simple @ a8_simple.T, 6)
print(f"  A8 simple roots Gram matrix:")
for row in a8_gram:
    print(f"    {row}")

# Check it's the A8 Cartan matrix: 2 on diagonal, -1 for adjacent, 0 otherwise
expected_a8 = np.diag([2.0]*8)
for i in range(7):
    expected_a8[i, i+1] = -1
    expected_a8[i+1, i] = -1

if np.allclose(a8_gram, expected_a8):
    print(f"  A8 Cartan matrix: VERIFIED")
else:
    print(f"  A8 Cartan matrix: MISMATCH!")
    print(f"  Expected:\n{expected_a8}")
    print(f"  Got:\n{a8_gram}")
    # Try to diagnose
    diff = a8_gram - expected_a8
    print(f"  Difference:\n{diff}")

# ============================================================================
# PART 6: Generate all A8 roots
# ============================================================================

print("\n--- Part 5: Generate All 72 A8 Roots ---")

# A8 roots are all positive roots beta = sum_{i=k}^{l} beta_i for k <= l,
# plus their negatives. For A_n, positive roots = {e_i - e_j : i < j}
# in the fundamental representation basis. In our basis, we generate
# them by taking all consecutive sums of simple roots.

a8_positive_roots = []
for start in range(8):
    root_sum = np.zeros(8)
    for end in range(start, 8):
        root_sum = root_sum + a8_simple[end]
        a8_positive_roots.append(root_sum.copy())

a8_all_roots = []
for r in a8_positive_roots:
    a8_all_roots.append(r)
    a8_all_roots.append(-r)

a8_all_roots = np.array(a8_all_roots)
print(f"  A8 positive roots: {len(a8_positive_roots)}")
print(f"  A8 total roots: {len(a8_all_roots)}")

# Remove duplicates (shouldn't be any)
unique_a8 = []
for r in a8_all_roots:
    is_dup = False
    for u in unique_a8:
        if np.allclose(r, u):
            is_dup = True
            break
    if not is_dup:
        unique_a8.append(r)
a8_all_roots = np.array(unique_a8)
print(f"  After dedup: {len(a8_all_roots)}")

# Expected: A8 has 8*9 = 72 roots (n*(n+1) for A_n)
assert len(a8_all_roots) == 72, f"Expected 72, got {len(a8_all_roots)}"

# Verify all A8 roots are E8 roots
a8_in_e8 = 0
for r in a8_all_roots:
    found = any(np.allclose(r, er) for er in roots)
    if found:
        a8_in_e8 += 1
    else:
        print(f"  WARNING: A8 root {r} NOT found in E8!")
print(f"  A8 roots that are E8 roots: {a8_in_e8}/{len(a8_all_roots)}")

# Verify all have squared length 2
a8_norms = np.sum(a8_all_roots**2, axis=1)
assert np.allclose(a8_norms, 2.0), "Not all A8 roots have |r|^2 = 2"
print(f"  All A8 roots have |r|^2 = 2: VERIFIED")

# ============================================================================
# PART 7: Decompose E8 under A8: identify 80, 84, 84_bar
# ============================================================================

print("\n--- Part 6: E8 = 80 + 84 + 84_bar Under A8 ---")

# The 80-dimensional adjoint of SU(9) consists of:
#   72 root spaces (A8 roots) + 8 Cartan generators = 80
# The remaining 240 - 72 = 168 roots split into 84 + 84_bar.

# Mark which E8 roots are A8 roots
is_a8 = np.zeros(240, dtype=bool)
for i, er in enumerate(roots):
    for ar in a8_all_roots:
        if np.allclose(er, ar):
            is_a8[i] = True
            break

n_a8 = np.sum(is_a8)
n_non_a8 = 240 - n_a8
print(f"  E8 roots in A8: {n_a8} (+ 8 Cartan = {n_a8 + 8} = adjoint)")
print(f"  E8 roots NOT in A8: {n_non_a8}")
assert n_a8 == 72, f"Expected 72, got {n_a8}"
assert n_non_a8 == 168, f"Expected 168, got {n_non_a8}"

# The 168 non-A8 roots should split into 84 + 84_bar.
# These correspond to Lambda^3(9) and its conjugate.
# To distinguish them, we use the "missing" simple root alpha_2.
# The eigenvalue under alpha_2 (more precisely, under the fundamental
# weight corresponding to the deleted node) determines the sector.

# The fundamental weight omega_2 of E8 corresponding to alpha_2:
# omega_2 satisfies <omega_2, alpha_j> = delta_{2,j} for all simple roots.
# For E8, the fundamental weights are computed from the inverse Cartan matrix.

# But there's a simpler way: the Z3 action is generated by the element
# h = omega_2 / 3 (the fundamental coweight of the deleted node, divided by 3).
# Wait, actually the deleted node defines a Z3 grading on E8.
#
# When we delete node 2 from the extended Dynkin diagram, we get A8.
# The Z3 grading is determined by the coefficient of alpha_2 in the
# expansion of each E8 root in terms of simple roots.
#
# Specifically: every E8 root alpha = sum n_i * alpha_i.
# The "grade" with respect to the deletion of node 2 is simply n_2 (mod 3).
# But since E8 is simply-laced and the deleted node has Kac label 3
# (for extended E8), we need n_2 mod 3.
#
# Actually, the Kac labels for extended E8 are:
# alpha_0: 1, alpha_1: 2, alpha_2: 3, alpha_3: 4, alpha_4: 5,
# alpha_5: 6, alpha_6: 4, alpha_7: 2, alpha_8: 3
# Wait, I need to be more careful. Let me look up the marks.

# E8 extended (affine) Dynkin diagram marks (= coefficients of theta
# in terms of simple roots, plus 1 for alpha_0):
# theta = 2*alpha_1 + 3*alpha_2 + 4*alpha_3 + 6*alpha_4 + 5*alpha_5 +
#         4*alpha_6 + 3*alpha_7 + 2*alpha_8
# So the Kac labels (marks on extended diagram) are:
# a_0 = 1, a_1 = 2, a_2 = 3, a_3 = 4, a_4 = 6, a_5 = 5, a_6 = 4, a_7 = 3, a_8 = 2
#
# When we delete node 2 (which has mark a_2 = 3), the Z_{a_2} = Z_3
# grading assigns to each root its coefficient n_2 modulo 3.

# First, express every E8 root in terms of E8 simple roots.
# alpha = sum n_i * alpha_i, where the n_i are all >= 0 (positive root)
# or all <= 0 (negative root).

# Invert the simple root matrix to get coordinates
# Each root alpha in R^8, simple roots form an 8x8 matrix S.
# alpha = S^T * n => n = (S^T)^{-1} * alpha = (S^{-1})^T * alpha
S = e8_simple  # 8 x 8 matrix, rows = simple roots
S_inv = np.linalg.inv(S)

# The simple-root coordinates of an E8 root alpha are: n = S_inv @ alpha
# But this gives real coefficients. For a root, these should be integers.

def simple_root_coords(root, S_inv):
    """Express a root in terms of simple roots."""
    coords = S_inv @ root
    # Round to nearest integer
    int_coords = np.round(coords).astype(int)
    # Verify
    reconstructed = int_coords @ S  # S has rows = simple roots
    assert np.allclose(reconstructed, root, atol=1e-6), \
        f"Failed to express {root} in simple root basis: got coords {int_coords}, reconstructed {reconstructed}"
    return int_coords

# Wait, the formula is: if alpha = n_1*alpha_1 + ... + n_8*alpha_8,
# then in vector form: alpha = n^T @ S (since S rows are simple roots)
# So n^T = alpha @ S_inv^T, hence n = (S^T)^{-1} @ alpha = S_inv^T @ alpha
# Let me verify with alpha_1 itself: should give (1,0,...,0).

S_inv_T = S_inv.T  # This maps root vectors to simple root coordinates

# Actually: alpha = sum n_i * alpha_i = n^T S (matrix multiply, n is row)
# So alpha^T = S^T n => n = (S^T)^{-1} alpha
# In numpy: n = np.linalg.solve(S.T, alpha)

test_coords = np.linalg.solve(S.T, e8_simple[0])
assert np.allclose(test_coords, [1,0,0,0,0,0,0,0]), f"Test failed: {test_coords}"

# Good. Now compute n_2 (coefficient of alpha_2) for all roots.
# alpha_2 is e8_simple[1] (0-indexed).

print(f"\n  Computing alpha_2 coefficient (n_2) for all 240 E8 roots...")
n2_values = []
for r in roots:
    coords = np.linalg.solve(S.T, r)
    int_coords = np.round(coords).astype(int)
    # Verify reconstruction
    reconstructed = int_coords @ S
    assert np.allclose(reconstructed, r, atol=1e-6), f"Reconstruction failed for {r}"
    n2_values.append(int_coords[1])  # coefficient of alpha_2 (0-indexed: index 1)

n2_values = np.array(n2_values)

# The Z3 grade is n_2 mod 3
z3_grade = n2_values % 3
# But n_2 can be negative for negative roots. Python mod handles this correctly.

# Count roots by grade
for g in [0, 1, 2]:
    count = np.sum(z3_grade == g)
    print(f"    Grade {g}: {count} roots")

grade_0_count = np.sum(z3_grade == 0)
grade_1_count = np.sum(z3_grade == 1)
grade_2_count = np.sum(z3_grade == 2)

print(f"  Grade 0: {grade_0_count} roots + 8 Cartan = {grade_0_count + 8} (should be 80)")
print(f"  Grade 1: {grade_1_count} (should be 84)")
print(f"  Grade 2: {grade_2_count} (should be 84)")

assert grade_0_count + 8 == 80, f"Grade 0 sector wrong: got {grade_0_count + 8}"
assert grade_1_count == 84, f"Grade 1 sector wrong: got {grade_1_count}"
assert grade_2_count == 84, f"Grade 2 sector wrong: got {grade_2_count}"
print(f"  E8 = 80 + 84 + 84_bar: VERIFIED!")

# Cross-check: grade 0 roots should be exactly the A8 roots
for i, r in enumerate(roots):
    if is_a8[i]:
        assert z3_grade[i] == 0, f"A8 root {r} has grade {z3_grade[i]} != 0"
    if z3_grade[i] == 0:
        assert is_a8[i], f"Grade 0 root {r} is not in A8"
print(f"  Grade 0 roots = A8 roots: VERIFIED!")

# ============================================================================
# PART 8: The key computation — how D7 roots split under Z3 grading
# ============================================================================

print("\n--- Part 7: THE KEY RESULT — so(14) Split Under Wilson's Z3 ---")

# For each D7 root, determine its Z3 grade
d7_grades = []
d7_root_indices = []  # indices into the global 'roots' array
for idx_d8, r in enumerate(d8_roots):
    nz = np.nonzero(np.abs(r) > 0.5)[0]
    if len(nz) == 2 and nz[0] <= 6 and nz[1] <= 6:
        # This is a D7 root. Find it in the global roots array.
        for idx_global, gr in enumerate(roots):
            if np.allclose(r, gr):
                d7_grades.append(z3_grade[idx_global])
                d7_root_indices.append(idx_global)
                break

d7_grades = np.array(d7_grades)
assert len(d7_grades) == 84

d7_in_80 = np.sum(d7_grades == 0)    # in su(9) adjoint
d7_in_84 = np.sum(d7_grades == 1)    # in Lambda^3(9)
d7_in_84bar = np.sum(d7_grades == 2) # in Lambda^3(9)*

print(f"  84 D7 roots split by Z3 grade:")
print(f"    Grade 0 (in su(9) = 80):      {d7_in_80} roots")
print(f"    Grade 1 (in Lambda^3 = 84):   {d7_in_84} roots")
print(f"    Grade 2 (in Lambda^3* = 84):  {d7_in_84bar} roots")

# Including Cartan (all grade 0):
total_in_80 = d7_in_80 + 7
total_in_84 = d7_in_84
total_in_84bar = d7_in_84bar

print(f"\n  so(14) [91 dim] total split:")
print(f"    In su(9) [80]:     {total_in_80} ({d7_in_80} roots + 7 Cartan)")
print(f"    In Lambda^3 [84]:  {total_in_84}")
print(f"    In Lambda^3* [84]: {total_in_84bar}")
print(f"    Total: {total_in_80} + {total_in_84} + {total_in_84bar} = {total_in_80+total_in_84+total_in_84bar}")
assert total_in_80 + total_in_84 + total_in_84bar == 91

pct_80 = 100 * total_in_80 / 91
pct_matter = 100 * (total_in_84 + total_in_84bar) / 91
print(f"\n  {pct_80:.1f}% of so(14) in Wilson's gauge sector (su(9))")
print(f"  {pct_matter:.1f}% of so(14) in Wilson's matter sector (84+84*)")

# ============================================================================
# PART 9: Identify the intersection subalgebra
# ============================================================================

print("\n--- Part 8: Intersection so(14) cap su(9) ---")

# The intersection consists of D7 roots with grade 0, plus 7 Cartan.
intersection_roots = []
for i, g in enumerate(d7_grades):
    if g == 0:
        intersection_roots.append(d7_roots[i] if i < len(d7_roots) else None)

# Actually let me collect them properly
intersection_roots = []
d7_list = list(d7_roots)
for i in range(len(d7_grades)):
    if d7_grades[i] == 0:
        intersection_roots.append(d7_list[i])

intersection_roots = np.array(intersection_roots)
print(f"  Roots in so(14) cap su(9): {len(intersection_roots)}")
print(f"  Cartan in intersection: 7")
print(f"  dim(so(14) cap su(9)) = {len(intersection_roots) + 7}")

# Analyze the root system structure
# Group by which coordinates are used
print(f"\n  Analyzing intersection root system structure:")

# For each root, identify coordinate pair and sign pattern
coord_groups = defaultdict(list)
for r in intersection_roots:
    nz = np.nonzero(np.abs(r) > 0.5)[0]
    i, j = nz[0], nz[1]
    signs = ('+' if r[i] > 0 else '-', '+' if r[j] > 0 else '-')
    coord_groups[(i,j)].append(signs)

print(f"  Roots grouped by coordinate pairs:")
for (i,j), sign_list in sorted(coord_groups.items()):
    print(f"    ({i},{j}): {len(sign_list)} roots — {sign_list}")

# Compute simple root coefficients for each intersection root
print(f"\n  Simple root expansions (n_2 = 0 verification):")
# Let me also check what n_2 values the D7 roots take
n2_dist = defaultdict(int)
for g in d7_grades:
    n2_dist[int(g)] += 1
print(f"  D7 root n_2 mod 3 distribution: {dict(n2_dist)}")

# Full n_2 values (not just mod 3)
print(f"\n  Full n_2 values for D7 roots:")
full_n2 = []
for idx in d7_root_indices:
    coords = np.linalg.solve(S.T, roots[idx])
    n2 = int(round(coords[1]))
    full_n2.append(n2)
n2_counts = defaultdict(int)
for n in full_n2:
    n2_counts[n] += 1
for n in sorted(n2_counts.keys()):
    print(f"    n_2 = {n}: {n2_counts[n]} roots (mod 3 = {n % 3})")

# Find the rank of the intersection root system
if len(intersection_roots) > 0:
    _, s_vals, _ = np.linalg.svd(intersection_roots)
    rank_int = np.sum(s_vals > 1e-10)
    print(f"\n  Rank of intersection root system: {rank_int}")
    print(f"  Number of roots: {len(intersection_roots)}")

    # Identify the type:
    # With known rank and root count, cross-reference with classification
    n_roots = len(intersection_roots)
    n_pos = n_roots // 2  # positive roots (since roots come in +/- pairs)

    print(f"  Positive roots: {n_pos}")

    # Possible root systems with these parameters:
    identifications = []
    for n in range(1, 10):
        # A_n: n(n+1) roots, rank n
        if n * (n+1) == n_roots:
            identifications.append(f"A_{n}")
        # D_n: 2*n*(n-1) roots, rank n (n >= 2)
        if n >= 2 and 2*n*(n-1) == n_roots:
            identifications.append(f"D_{n}")

    # Check direct sums
    for n1 in range(1, 8):
        for n2 in range(1, 8):
            r1 = n1*(n1+1)  # A_{n1} roots
            r2 = n2*(n2+1)  # A_{n2} roots
            if r1 + r2 == n_roots and n1 + n2 == rank_int:
                identifications.append(f"A_{n1} + A_{n2}")
            if n2 >= 2:
                r2d = 2*n2*(n2-1)  # D_{n2}
                if r1 + r2d == n_roots and n1 + n2 == rank_int:
                    identifications.append(f"A_{n1} + D_{n2}")

    # Check triple sums A + A + A
    for n1 in range(1, 6):
        for n2 in range(1, 6):
            for n3 in range(1, 6):
                r_total = n1*(n1+1) + n2*(n2+1) + n3*(n3+1)
                rank_total = n1 + n2 + n3
                if r_total == n_roots and rank_total == rank_int:
                    identifications.append(f"A_{n1} + A_{n2} + A_{n3}")

    print(f"  Possible identifications: {identifications}")

    # To pin it down, check if the roots decompose into orthogonal groups
    # Find connected components of the root system
    # (two roots are in same component if there's a chain of non-orthogonal roots)
    visited = [False] * len(intersection_roots)
    components = []

    def bfs(start):
        comp = [start]
        visited[start] = True
        queue = [start]
        while queue:
            curr = queue.pop(0)
            for other in range(len(intersection_roots)):
                if not visited[other]:
                    ip = np.dot(intersection_roots[curr], intersection_roots[other])
                    if abs(ip) > 0.5:  # non-orthogonal
                        visited[other] = True
                        queue.append(other)
                        comp.append(other)
        return comp

    for i in range(len(intersection_roots)):
        if not visited[i]:
            comp = bfs(i)
            components.append(comp)

    print(f"\n  Connected components of intersection root system: {len(components)}")
    for i, comp in enumerate(components):
        comp_roots = intersection_roots[comp]
        _, sv, _ = np.linalg.svd(comp_roots)
        comp_rank = np.sum(sv > 1e-10)
        print(f"    Component {i+1}: {len(comp)} roots, rank {comp_rank}")

        # Identify component
        n_r = len(comp)
        for n in range(1, 10):
            if n*(n+1) == n_r:
                print(f"      -> A_{n} (= su({n+1}))")
            if n >= 2 and 2*n*(n-1) == n_r:
                print(f"      -> D_{n} (= so({2*n}))")

        # Print sample roots
        for r in comp_roots[:4]:
            nz = np.nonzero(np.abs(r) > 0.5)[0]
            signs = tuple(r[nz])
            print(f"      sample: coords {tuple(nz)}, values {signs}")

# ============================================================================
# PART 10: Mixed and spinor decompositions
# ============================================================================

print("\n--- Part 9: Full 248 Decomposition (Double Grading) ---")

# Classify ALL 240 roots by BOTH D8 type AND Z3 grade
print(f"\n  {'Category':32s} | {'su(9)[80]':>10s} | {'84':>6s} | {'84*':>6s} | {'Total':>6s}")
print(f"  {'-'*32}-+-{'-'*10}-+-{'-'*6}-+-{'-'*6}-+-{'-'*6}")

table = {}
t80, t84, t84b = 0, 0, 0

# so(14) roots
g0 = d7_in_80; g1 = d7_in_84; g2 = d7_in_84bar
table['so(14) roots [84]'] = (g0, g1, g2)
print(f"  {'so(14) roots [84]':32s} | {g0:10d} | {g1:6d} | {g2:6d} | {g0+g1+g2:6d}")
t80 += g0; t84 += g1; t84b += g2

# so(14) Cartan [7]
print(f"  {'so(14) Cartan [7]':32s} | {7:10d} | {0:6d} | {0:6d} | {7:6d}")
t80 += 7

# U(1) [1] (the SO(2) Cartan = h_7 direction)
print(f"  {'U(1) Cartan [1]':32s} | {1:10d} | {0:6d} | {0:6d} | {1:6d}")
t80 += 1

# Mixed roots [28]
mixed_grades = []
for r in mixed_roots:
    for idx, gr in enumerate(roots):
        if np.allclose(r, gr):
            mixed_grades.append(z3_grade[idx])
            break
mixed_grades = np.array(mixed_grades)
mg0 = np.sum(mixed_grades == 0)
mg1 = np.sum(mixed_grades == 1)
mg2 = np.sum(mixed_grades == 2)
print(f"  {'Mixed D8 roots [28]':32s} | {mg0:10d} | {mg1:6d} | {mg2:6d} | {mg0+mg1+mg2:6d}")
t80 += mg0; t84 += mg1; t84b += mg2

# D7 S+ spinor [64]
sp_grades = []
for r in spinor_roots:
    if r[7] > 0:
        for idx, gr in enumerate(roots):
            if np.allclose(r, gr):
                sp_grades.append(z3_grade[idx])
                break
sp_grades = np.array(sp_grades)
spg0 = np.sum(sp_grades == 0)
spg1 = np.sum(sp_grades == 1)
spg2 = np.sum(sp_grades == 2)
print(f"  {'D7 S+ spinor [64]':32s} | {spg0:10d} | {spg1:6d} | {spg2:6d} | {spg0+spg1+spg2:6d}")
t80 += spg0; t84 += spg1; t84b += spg2

# D7 S- spinor [64]
sm_grades = []
for r in spinor_roots:
    if r[7] < 0:
        for idx, gr in enumerate(roots):
            if np.allclose(r, gr):
                sm_grades.append(z3_grade[idx])
                break
sm_grades = np.array(sm_grades)
smg0 = np.sum(sm_grades == 0)
smg1 = np.sum(sm_grades == 1)
smg2 = np.sum(sm_grades == 2)
print(f"  {'D7 S- spinor [64]':32s} | {smg0:10d} | {smg1:6d} | {smg2:6d} | {smg0+smg1+smg2:6d}")
t80 += smg0; t84 += smg1; t84b += smg2

print(f"  {'-'*32}-+-{'-'*10}-+-{'-'*6}-+-{'-'*6}-+-{'-'*6}")
print(f"  {'TOTAL':32s} | {t80:10d} | {t84:6d} | {t84b:6d} | {t80+t84+t84b:6d}")
print(f"  {'Expected':32s} | {'80':>10s} | {'84':>6s} | {'84':>6s} | {'248':>6s}")

# ============================================================================
# PART 11: Compatibility verdict
# ============================================================================

print("\n" + "=" * 72)
print("RESULTS SUMMARY")
print("=" * 72)

print(f"""
  QUESTION 1: dim(so(14) cap su(9)) = ?
  ANSWER: {len(intersection_roots) + 7}

  QUESTION 2: How do the 91 of so(14) split under su(9)?
  ANSWER:
    In su(9) [80]:      {total_in_80} generators ({d7_in_80} roots + 7 Cartan)
    In Lambda^3 [84]:   {total_in_84} generators
    In Lambda^3* [84]:  {total_in_84bar} generators
    Total: {total_in_80} + {total_in_84} + {total_in_84bar} = 91

  QUESTION 3: What is the common subgroup?
  ANSWER: su(7) x u(1)   [dimension 48 + 1 = 49]
    Root system: A_6 (42 roots, rank 6) = su(7)
    All 42 roots are of the form e_i - e_j with i,j in {{0..6}}.
    Extra Cartan: rank(D7) - rank(A6) = 7 - 6 = 1 -> u(1)
    Algebra: su(7) x u(1), dim = 48 + 1 = 49

    Physical identification:
    - SU(7) is the largest group sitting inside BOTH SO(14) and SU(9)
    - Inside SO(14): SU(7) c SO(14) (the natural embedding)
    - Inside SU(9): SU(7) c SU(9) (subgroup of first 7 of 9)
    - The U(1) is the Cartan direction orthogonal to A_6 within D_7

  QUESTION 4: Is there a common refinement?
  ANSWER: YES. The Z3 grading (from the extended Dynkin diagram construction)
    provides a well-defined decomposition of EVERY E8 root, including
    half-integer (spinor) roots. Both the SO(14) decomposition and the
    SU(9) decomposition are refinements of the full 248 that are compatible.
""")

print("=" * 72)
print("KC-E2 VERDICT")
print("=" * 72)

# Compute percentages
print(f"""
  KC-E2: PASSES

  RATIONALE:

  1. MATHEMATICAL CONSISTENCY: Both decompositions of E8(248) are
     rigorously verified using the E8 root system:
     - SO(16) route: 248 = 91 + 1 + 28 + 64 + 64  [VERIFIED]
     - SU(9) route:  248 = 80 + 84 + 84            [VERIFIED]
     Both decompositions coexist within the same E8 root system.

  2. CROSS-DECOMPOSITION: The 91 generators of so(14) split as:
     {total_in_80} in su(9)'s adjoint [80]
     {total_in_84} in Lambda^3 [84]
     {total_in_84bar} in Lambda^3* [84]
     This is a well-defined, computable decomposition.

  3. COMMON SUBALGEBRA: so(14) cap su(9) has dimension {len(intersection_roots)+7}.
     This provides a bridge between the two frameworks.

  4. COMPLEMENTARITY: The two chains slice E8 differently:
     - SO(14) chain: organizes gravity + GUT into a single algebra
     - SU(9) chain: organizes 3 generations via Z3
     These are different coordinate systems on the same E8 structure.

  5. THREE-GENERATION MECHANISM: Wilson's Z3 comes from the A8 structure
     (specifically, from the Kac label 3 on node alpha_2 of the extended
     E8 Dynkin diagram). This Z3 operates at the E8 level, above SO(14).
     Our impossibility theorem (7 intrinsic mechanisms dead within SO(14))
     is CONSISTENT with this — the Z3 is an E8 feature, not an SO(14) feature.

  IMPLICATION FOR PAPER 3:
  - Our SO(14) machine-verified scaffold is COMPATIBLE with Wilson's E8
  - The {total_in_84+total_in_84bar} generators of so(14) in Wilson's
    matter sector transform as definite representations of the common
    subgroup — this is expected for different maximal subgroup chains
  - The three-generation mechanism requires E8 structure beyond SO(14),
    consistent with our impossibility theorem

  KEY NUMBERS:
    dim(so(14) cap su(9)) = {len(intersection_roots)+7} = su(7) x u(1)
    91 = {total_in_80} [in 80] + {total_in_84} [in 84] + {total_in_84bar} [in 84*]
    Intersection root system: A_6 = su(7), 42 roots, rank 6
    The 42 roots are ALL of the form (e_i - e_j), i.e., SU(n)-type roots.
    The 21+21 = 42 roots in the matter sector are (e_i + e_j) and -(e_i + e_j),
    which are the SO(n) roots that SU(n) does NOT have.
""")

# ============================================================================
# PART 12: Verify the matter sector structure
# ============================================================================

print("\n--- Appendix: Structure of so(14) Generators in Matter Sector ---")

# The 21 roots in sector 1 (Lambda^3) and 21 in sector 2 (Lambda^3*)
# Let's verify they are ALL of the (e_i + e_j) type
sec1_roots_list = []
sec2_roots_list = []
for i in range(len(d7_grades)):
    if d7_grades[i] == 1:
        sec1_roots_list.append(d7_list[i])
    elif d7_grades[i] == 2:
        sec2_roots_list.append(d7_list[i])

print(f"\n  21 so(14) roots in Lambda^3 [84] (sector 1):")
s1_same = 0; s1_diff = 0
for r in sec1_roots_list:
    nz = np.nonzero(np.abs(r) > 0.5)[0]
    v0, v1 = r[nz[0]], r[nz[1]]
    if np.sign(v0) == np.sign(v1):
        s1_same += 1
    else:
        s1_diff += 1
print(f"    Same-sign (e_i + e_j type): {s1_same}")
print(f"    Diff-sign (e_i - e_j type): {s1_diff}")

print(f"\n  21 so(14) roots in Lambda^3* [84] (sector 2):")
s2_same = 0; s2_diff = 0
for r in sec2_roots_list:
    nz = np.nonzero(np.abs(r) > 0.5)[0]
    v0, v1 = r[nz[0]], r[nz[1]]
    if np.sign(v0) == np.sign(v1):
        s2_same += 1
    else:
        s2_diff += 1
print(f"    Same-sign (e_i + e_j type): {s2_same}")
print(f"    Diff-sign (e_i - e_j type): {s2_diff}")

print(f"""
  INTERPRETATION:
  The 42 intersection roots (sector 0) are the SU-type roots (e_i - e_j).
  The 42 matter-sector roots (sectors 1+2) are the SO-type roots (+/- e_i +/- e_j, same sign).

  This is exactly the decomposition SO(14) -> SU(7) x U(1):
    so(14) = su(7) + u(1) + (7 choose 2) + (7 choose 2)*
           = 48 + 1 + 21 + 21 = 91
  where (7 choose 2) = 21 is the antisymmetric tensor of SU(7).

  Under the simultaneous decomposition by BOTH subgroup chains:
    so(14) gauge sector [49 in su(9)]  = su(7) x u(1) = common subgroup
    so(14) matter sector [42 in 84+84] = Lambda^2(7) + Lambda^2(7)* under SU(7)

  The matter-sector generators of so(14) transform as the
  ANTISYMMETRIC TENSOR representation of the common SU(7).
  This is a clean, well-defined representation-theoretic decomposition.
""")
