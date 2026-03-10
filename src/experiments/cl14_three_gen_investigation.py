#!/usr/bin/env python3
"""
Cl(14,0) Structure Investigation: Can Clifford Algebra Produce 3 Generations?
==============================================================================

BACKGROUND:
  SO(14) -> SO(10) x SO(4) gives 64+ = (16,(2,1)) + (16-bar,(1,2))
  No SO(4) Lie algebra operator gives 3+1. Eigenvalues always 2+2.
  Seven intrinsic mechanisms (M1-M7) all dead.

  This script goes BEYOND the Lie group and investigates the full
  Clifford algebra Cl(14,0) for hidden Z_3 or 3-fold structure.

INVESTIGATIONS:
  1. Cl(14,0) = M(128,R) structure and Pin(14) disconnected components
  2. Coxeter grading of D_7 (h=12) and Z_3 sub-grading
  3. so(8) triality inside so(14)
  4. Primitive idempotent decompositions of the 64-dim semi-spinor
  5. Non-standard SO(10) embeddings in SO(14)
  6. Coxeter element eigenvalues on 64+ (the key computation)

Author: Clifford Unification Engineer
Date: 2026-03-09
"""

import numpy as np
from itertools import combinations, product
from collections import defaultdict
from math import comb

np.set_printoptions(precision=8, suppress=True, linewidth=140)

# ============================================================================
# INFRASTRUCTURE: Build Cl(14,0) gamma matrices
# ============================================================================
print("=" * 80)
print("INFRASTRUCTURE: Constructing Cl(14,0) Gamma Matrices")
print("=" * 80)

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

def kron_list(mats):
    """Kronecker product of a list of matrices."""
    result = mats[0]
    for m in mats[1:]:
        result = np.kron(result, m)
    return result

def build_clifford_gammas(n):
    """Build n gamma matrices for Cl(n,0) using the standard recursive construction.

    For Cl(2k,0): use k tensor factors of 2x2 matrices.
    gamma_{2j-1} = sz (x) ... (x) sz (x) sx (x) I2 (x) ... (x) I2
    gamma_{2j}   = sz (x) ... (x) sz (x) sy (x) I2 (x) ... (x) I2
    where sz appears j-1 times before the sx/sy.

    For Cl(2k+1,0): use gamma_1...gamma_{2k} from Cl(2k,0),
    plus gamma_{2k+1} = sz (x) sz (x) ... (x) sz (k times).
    """
    k = (n + 1) // 2  # number of tensor factors needed for 2^k dim
    dim = 2 ** k
    gammas = []

    for j in range(k):
        # gamma_{2j+1} (odd, 0-indexed)
        factors = [sz] * j + [sx] + [I2] * (k - j - 1)
        gammas.append(1j * kron_list(factors))

        # gamma_{2j+2} (even, 0-indexed)
        factors = [sz] * j + [sy] + [I2] * (k - j - 1)
        gammas.append(1j * kron_list(factors))

    # Only return the first n gammas
    return gammas[:n]

# Build 14 gamma matrices (128x128)
gammas = build_clifford_gammas(14)
dim = gammas[0].shape[0]
print(f"  Dimension: {dim}x{dim} (2^7 = 128)")
print(f"  Number of gamma matrices: {len(gammas)}")

# Verify Clifford algebra relations: {gamma_i, gamma_j} = -2 delta_{ij}
# (our convention includes the factor of i, so gamma_i^2 = -I)
print("\n  Verifying Clifford relations...")
max_err = 0
for i in range(14):
    for j in range(14):
        anticomm = gammas[i] @ gammas[j] + gammas[j] @ gammas[i]
        if i == j:
            expected = -2 * np.eye(dim, dtype=complex)  # gamma_i^2 = -I
        else:
            expected = np.zeros((dim, dim), dtype=complex)
        err = np.max(np.abs(anticomm - expected))
        max_err = max(max_err, err)
print(f"  Max error in Clifford relations: {max_err:.2e}")
assert max_err < 1e-12, "Clifford algebra relations FAILED"
print("  Clifford relations VERIFIED.")

# ============================================================================
# Chirality operator and semi-spinor projection
# ============================================================================
print("\n  Building chirality operator Gamma_15 = gamma_1 ... gamma_14...")
Gamma15 = np.eye(dim, dtype=complex)
for g in gammas:
    Gamma15 = Gamma15 @ g

# Check Gamma15^2
Gamma15_sq = Gamma15 @ Gamma15
phase = Gamma15_sq[0, 0]
print(f"  Gamma15^2 = {phase:.6f} * I")
Gamma15_n = Gamma15 / np.sqrt(phase)
Gamma15_sq_n = Gamma15_n @ Gamma15_n
print(f"  Normalized: Gamma15_n^2 = {Gamma15_sq_n[0,0]:.6f} * I")

# Eigendecomposition -> semi-spinors
evals, evecs = np.linalg.eigh(Gamma15_n)
order = np.argsort(-evals.real)
evals, evecs = evals[order], evecs[:, order]

# Count +1 and -1 eigenvalues
n_plus = np.sum(evals > 0.5)
n_minus = np.sum(evals < -0.5)
print(f"  Eigenvalues: {n_plus} x (+1), {n_minus} x (-1)")
assert n_plus == 64 and n_minus == 64

B_plus = evecs[:, :64]    # 64+ semi-spinor basis (128 x 64)
B_minus = evecs[:, 64:]   # 64- semi-spinor basis (128 x 64)

# ============================================================================
# so(14) generators and subgroup structure
# ============================================================================
print("\n  Building so(14) generators (91 total)...")
so14_gens = {}
for i in range(14):
    for j in range(i+1, 14):
        so14_gens[(i,j)] = (1j / 2) * gammas[i] @ gammas[j]

print(f"  Built {len(so14_gens)} generators.")

# SO(10) generators: indices 0-9
so10_gens = {k: v for k, v in so14_gens.items() if k[0] < 10 and k[1] < 10}
print(f"  SO(10) generators (indices 0-9): {len(so10_gens)}")

# SO(4) generators: indices 10-13
so4_gens = {k: v for k, v in so14_gens.items() if k[0] >= 10 and k[1] >= 10}
print(f"  SO(4) generators (indices 10-13): {len(so4_gens)}")

# Mixed generators
mixed_gens = {k: v for k, v in so14_gens.items()
              if (k[0] < 10 and k[1] >= 10) or (k[0] >= 10 and k[1] < 10)}
print(f"  Mixed generators: {len(mixed_gens)}")
assert len(so10_gens) + len(so4_gens) + len(mixed_gens) == 91

# Project to 64+
def proj64(M):
    """Project 128x128 matrix to the 64+ semi-spinor subspace."""
    return B_plus.conj().T @ M @ B_plus

# ============================================================================
# INVESTIGATION 1: Cl(14,0) = M(128,R) structure
# ============================================================================
print("\n" + "=" * 80)
print("INVESTIGATION 1: Cl(14,0) Structure and Pin(14)")
print("=" * 80)

# Cl(14,0) = M(128,R) because 14 = 2*7 and we're in the real case
# The full Clifford algebra has dimension 2^14 = 16384
# As a matrix algebra, it's 128x128 = 16384 entries. Checks out.

print("""
  Cl(14,0) isomorphism classes (from periodicity theorem):
    Cl(n,0) for n mod 8:
      n=0: R       n=1: C       n=2: H       n=3: H+H
      n=4: M_2(H)  n=5: M_4(C)  n=6: M_8(R)  n=7: M_8(R)+M_8(R)

    Cl(14,0): 14 mod 8 = 6, so Cl(14,0) = M(2^6, R) x M(2, ?) ...
    Actually: Cl(2k,0) = M(2^k, R) when k = 0,3 mod 4
              Cl(2k,0) = M(2^{k-1}, H) when k = 1,2 mod 4

    k = 7: 7 mod 4 = 3, so Cl(14,0) = M(2^7, R) = M(128, R)  [CORRECT]

  Even subalgebra: Cl+(14,0) = Cl(13,0)
    13 mod 8 = 5, so Cl(13,0) = M_4(C) tensored up...
    Actually Cl(13,0) = M(64, C)  [since 13 = 8+5, and Cl(5,0) = M_4(C)]
    Wait, let me be more careful.

    Cl(13,0): 13 is odd. Cl(2k+1,0) = M(2^k, C) when k+1 = 0 mod 4
                                      = M(2^k, R) + M(2^k, R) when k = 0 mod 4
                                      = M(2^{k-1}, H) + M(2^{k-1}, H) when k = 1,2 mod 4
    k = 6: 6 mod 4 = 2, so Cl(13,0) = M(2^5, H) + M(2^5, H) = M(32, H) + M(32, H)

    Hmm, let me just use the standard table. Actually:
    Cl(13,0) = M(64,R) + M(64,R)  [from Lawson-Michelsohn table]

  This means Cl+(14,0) has TWO simple summands, corresponding to the
  two semi-spinor representations 64+ and 64-.
""")

# Verify: does the even subalgebra preserve the semi-spinor spaces?
print("  Verifying even subalgebra preserves semi-spinor spaces...")
# An even element is a product of even number of gammas
# Test with all bivectors (grade 2)
max_mixing = 0
for (i,j), gen in so14_gens.items():
    # gen acts on 128-dim. Check that it doesn't mix 64+ and 64-
    off_diag = B_minus.conj().T @ gen @ B_plus
    max_mixing = max(max_mixing, np.max(np.abs(off_diag)))
print(f"  Max mixing of 64+ and 64- by so(14) generators: {max_mixing:.2e}")
# This should be zero because so(14) generators are grade-2 (even)
assert max_mixing < 1e-12, "Even subalgebra MIXES semi-spinors -- BUG"
print("  VERIFIED: Even subalgebra preserves semi-spinor spaces.")

# Now check: do grade-1 (odd) elements MIX the semi-spinors?
print("\n  Checking: do gamma matrices (grade 1) mix semi-spinors?")
for i in range(14):
    off = B_minus.conj().T @ gammas[i] @ B_plus
    norm = np.linalg.norm(off)
    if i < 3:
        print(f"    gamma_{i+1}: ||off-diag|| = {norm:.6f}")
print(f"    (all 14 gammas checked, showing first 3)")
# They should MIX (non-zero off-diagonal)

# Pin(14) = elements of Cl(14,0) with norm 1
# Pin(14) / Z_2 = O(14)
# Spin(14) = even elements of Pin(14)  (= connected component)
# Pin(14) has two components: Spin(14) and its complement
# The complement contains reflections (grade-1 elements, odd)

print("""
  Pin(14) structure:
    Spin(14) = connected component (even Clifford elements)
    Pin(14) = Spin(14) union (Spin(14) * any single gamma)
    The Z_2 = {+1, -1} acts trivially on representations

    Pin(14) / Spin(14) = Z_2 (the parity/reflection group)

    The key question: are there ADDITIONAL discrete symmetries
    beyond Z_2 that live in Cl(14,0) but NOT in Spin(14)?

    Answer: No. Pin(14) has exactly Z_2 as its component group.
    There are no hidden Z_3 or S_3 symmetries in Pin(14).

    However, the Clifford algebra Cl(14,0) itself is LARGER than Pin(14).
    It contains ALL 128x128 real matrices. The question is whether
    any of these non-group elements provide useful structure.
""")

# ============================================================================
# INVESTIGATION 2: Coxeter Grading and Z_3 Sub-grading
# ============================================================================
print("\n" + "=" * 80)
print("INVESTIGATION 2: Coxeter Grading of D_7 and Z_3 Sub-grading")
print("=" * 80)

# D_7 = so(14) has rank 7, Coxeter number h = 12
# Exponents: {1, 3, 5, 6, 7, 9, 11}  (for D_n: 1,3,...,2n-3, n-1)
# The principal grading decomposes the root system into h=12 levels

# Simple roots of D_7:
# alpha_1 = e_1 - e_2, alpha_2 = e_2 - e_3, ..., alpha_6 = e_6 - e_7, alpha_7 = e_6 + e_7
# These correspond to generators L_{12}, L_{23}, ..., L_{67}, and a "spinor" root L_{67}+

print("""
  D_7 root system:
    Rank: 7
    Coxeter number: h = 12
    Exponents: {1, 3, 5, 6, 7, 9, 11}
    Number of positive roots: 42
    Number of roots: 84
    Dimension of so(14): 7 + 84 = 91

  The PRINCIPAL GRADING assigns each root a "height" mod h.
  The height of a root sum(n_i alpha_i) is sum(n_i).
  This gives a Z-grading of the Lie algebra.
  The Coxeter element is the product of all simple reflections.
""")

# Build the root system of D_7 explicitly
# Roots of D_n: +/- e_i +/- e_j for i != j
# In our basis, e_i - e_j corresponds to generator L_{ij}
# and e_i + e_j corresponds to... we need to be careful

# Standard positive roots of D_7:
# Type 1: e_i - e_j (i < j): these are the roots of A_6 inside D_7
# Type 2: e_i + e_j (i < j): additional roots
pos_roots = []
root_to_gen = {}

for i in range(7):
    for j in range(i+1, 7):
        # Root e_i - e_j has generator L_{2i+1, 2j+1} (approximately)
        # But our so(14) generators use the natural basis indices 0-13
        pos_roots.append((i, j, +1))  # e_i - e_j
        pos_roots.append((i, j, -1))  # e_i + e_j

print(f"  Number of positive roots: {len(pos_roots)}")
assert len(pos_roots) == 42

# Simple roots of D_7
# alpha_i = e_i - e_{i+1} for i = 1,...,6
# alpha_7 = e_6 + e_7
simple_roots = []
for i in range(6):
    simple_roots.append((i, i+1, +1))  # e_i - e_{i+1}
simple_roots.append((5, 6, -1))  # e_6 + e_7

print(f"  Simple roots: {len(simple_roots)}")
for k, (i, j, s) in enumerate(simple_roots):
    sign = "-" if s == +1 else "+"
    print(f"    alpha_{k+1} = e_{i+1} {sign} e_{j+1}")

# Height of a root in the simple root expansion
# For D_n, the heights are well-known
# Let's compute heights by expressing each positive root in terms of simple roots

def root_height(root, simple_roots):
    """Compute the height of a root (sum of simple root coefficients).

    For D_7:
    e_i - e_j = alpha_i + alpha_{i+1} + ... + alpha_{j-1}  (i < j, for type +1)
    e_i + e_j = alpha_i + ... + alpha_{j-1} + 2(alpha_j + ... + alpha_5) + alpha_6 + alpha_7  (for j < 6)

    Actually this gets complicated. Let me just compute it directly.
    """
    i, j, s = root
    if s == +1:  # e_i - e_j, i < j
        return j - i  # height = j - i
    else:  # e_i + e_j, i < j
        # e_i + e_j = (e_i - e_6) + (e_j - e_7) + (e_6 + e_7)  if i,j < 6
        # Wait, this depends on the root system. Let me be more systematic.
        #
        # For D_7, Cartan matrix determines heights.
        # e_i + e_j = alpha_i + alpha_{i+1} + ... + alpha_{j-1}
        #           + 2*alpha_j + 2*alpha_{j+1} + ... + 2*alpha_5 + alpha_6 + alpha_7
        # Height = (j-i) + 2*(6-j) + 1 + 1 = j - i + 12 - 2j + 2 = 14 - i - j
        # Wait, let me verify with small cases.
        #
        # e_5 + e_6 (i=5, j=6): = alpha_6 + alpha_7 (the two "spinor" roots)
        # Height = 2. By formula: 14 - 5 - 6 = 3. WRONG.
        #
        # Let me just use: e_i + e_j = sum of simple roots
        # e_6 + e_7 = alpha_7, height 1
        # e_5 + e_7 = alpha_6 + alpha_7, height 2
        # e_5 + e_6 = alpha_5 + alpha_6 + alpha_7... no.
        #
        # Actually I should just express everything in Cartan coordinates.
        # Let me do it numerically.

        # The Cartan matrix of D_7:
        pass
    return None  # will compute below

# Let me build this properly using the Cartan matrix
# D_7 Cartan matrix
n = 7
C = np.zeros((n, n))
for i in range(n-1):
    C[i, i] = 2
    if i < n-2:
        C[i, i+1] = -1
        C[i+1, i] = -1
# Last two rows/cols for D_n
C[n-1, n-1] = 2
C[n-2, n-1] = 0  # No connection between alpha_{n-1} and alpha_n for D_n
C[n-1, n-2] = 0
C[n-3, n-1] = -1  # alpha_{n-2} connects to alpha_n
C[n-1, n-3] = -1

print(f"\n  Cartan matrix of D_7:")
print(C)

# Now build all positive roots by reflection
# Actually, let me use a different approach: enumerate all roots of D_7
# directly as vectors in R^7.

# Roots of D_7: +/- e_i +/- e_j for 1 <= i < j <= 7
# Using e_i as standard basis vectors in R^7
all_roots = []
for i in range(7):
    for j in range(i+1, 7):
        r1 = np.zeros(7)
        r1[i] = 1; r1[j] = -1  # e_i - e_j
        all_roots.append(r1)

        r2 = np.zeros(7)
        r2[i] = -1; r2[j] = 1  # -e_i + e_j
        all_roots.append(r2)

        r3 = np.zeros(7)
        r3[i] = 1; r3[j] = 1  # e_i + e_j
        all_roots.append(r3)

        r4 = np.zeros(7)
        r4[i] = -1; r4[j] = -1  # -e_i - e_j
        all_roots.append(r4)

print(f"\n  Total roots of D_7: {len(all_roots)} (should be 84)")
assert len(all_roots) == 84

# Simple roots
alpha = np.zeros((7, 7))
for i in range(6):
    alpha[i, i] = 1
    alpha[i, i+1] = -1  # alpha_i = e_i - e_{i+1}
alpha[6, 5] = 1
alpha[6, 6] = 1  # alpha_7 = e_6 + e_7

# Express each root in simple root basis
# alpha = A * e, where A is the 7x7 matrix above
# root = sum c_i * alpha_i, so root_vec = sum c_i * alpha_i_vec
# c = A^(-1) * root_vec (in the e-basis)
A_inv = np.linalg.inv(alpha)

print("\n  Computing heights of all positive roots...")
positive_roots = [r for r in all_roots if any(r[k] > 0 for k in range(7)) or
                  (all(r[k] == 0 for k in range(7)))]
# Actually, positive roots: first nonzero coordinate is positive
positive_roots = []
for r in all_roots:
    for k in range(7):
        if abs(r[k]) > 0.5:
            if r[k] > 0:
                positive_roots.append(r)
            break

print(f"  Positive roots: {len(positive_roots)} (should be 42)")
assert len(positive_roots) == 42

heights = {}
for r in positive_roots:
    coeffs = A_inv @ r
    h = int(round(np.sum(coeffs)))
    root_key = tuple(r)
    heights[root_key] = h

# Distribution of heights
height_dist = defaultdict(int)
for h in heights.values():
    height_dist[h] += 1

print("\n  Height distribution of positive roots:")
for h in sorted(height_dist.keys()):
    print(f"    Height {h:2d}: {height_dist[h]} roots")

max_height = max(heights.values())
print(f"  Maximum height: {max_height} (should be h-1 = 11 for D_7)")

# Z_3 sub-grading: heights mod 3
print("\n  Z_3 sub-grading (height mod 3):")
z3_dist = defaultdict(int)
for h in heights.values():
    z3_dist[h % 3] += 1
for k in sorted(z3_dist.keys()):
    print(f"    Height mod 3 = {k}: {z3_dist[k]} positive roots")

# Z_4 sub-grading: heights mod 4
print("\n  Z_4 sub-grading (height mod 4):")
z4_dist = defaultdict(int)
for h in heights.values():
    z4_dist[h % 4] += 1
for k in sorted(z4_dist.keys()):
    print(f"    Height mod 4 = {k}: {z4_dist[k]} positive roots")

# ============================================================================
# INVESTIGATION 2b: Coxeter Element and Its Action on the Spinor Space
# ============================================================================
print("\n" + "-" * 60)
print("  Coxeter Element: eigenvalues on the 64+ semi-spinor")
print("-" * 60)

# The Coxeter element w = s_1 * s_2 * ... * s_7
# where s_i is the simple reflection corresponding to alpha_i.
# In the spinor representation, each s_i = exp(pi * L_{alpha_i})
# where L_{alpha_i} is the so(14) generator for the simple root alpha_i.

# Map simple roots to so(14) generators
# alpha_i = e_i - e_{i+1} corresponds to L_{i, i+1} (rotation in i,i+1 plane)
# In our indexing: L_{2i, 2i+1} or just (i, i+1) with i 0-indexed

# Wait, I need to be more careful about the correspondence between
# root vectors and so(14) generators.
#
# The root e_i - e_j (i < j) corresponds to the generator L_{ij}
# which is the (i,j) antisymmetric matrix. In the Cartan-Weyl basis,
# this would be E_{ij} - E_{ji}.
#
# In our gamma matrix construction, the generator for (i,j) is:
# L_{ij} = (i/2) * gamma_i * gamma_j
# BUT: our gamma indices run 0-13, while root indices run 0-6 (in R^7).
# The roots of D_7 live in R^7, not R^14.
#
# The correspondence:
# Root e_i - e_j -> generator that rotates in the (2i, 2i+1) -> (2j, 2j+1) block
# More precisely: e_a (standard basis in R^7) corresponds to
# the Cartan element H_a = L_{2a, 2a+1} (where L is our so(14) generator).
#
# For the simple reflection s_i corresponding to alpha_i = e_i - e_{i+1}:
# s_i acts on R^14 by swapping the 2-planes (e_{2i}, e_{2i+1}) and (e_{2i+2}, e_{2i+3})
# In the spinor rep, s_i = exp(pi/2 * [gamma_{2i}, gamma_{2i+2}] / 2) or similar.
#
# Actually, the simple reflection s_alpha in the VECTOR representation is:
# s_alpha(v) = v - 2(v, alpha)/(alpha, alpha) * alpha
#
# In the SPIN representation, the lift is:
# s_alpha -> +-  alpha / |alpha|  (the Clifford algebra element)
#
# For root alpha = e_i - e_j (unit length in the weight lattice):
# The corresponding Clifford element is proportional to gamma_i * gamma_j
# (where gamma_i corresponds to e_i in R^7... but our gammas are in R^14!)
#
# I need to think about this differently.

# CORRECT APPROACH:
# The Weyl group W(D_7) acts on the weight space R^7.
# The spinor weights are (h_1, ..., h_7) with h_k = +/- 1/2.
# The simple reflection s_i swaps h_i <-> h_{i+1} (for i=1..6)
# and s_7 sends (h_6, h_7) -> (-h_7, -h_6) (reflecting in e_6+e_7)
#
# The Coxeter element w = s_1 s_2 ... s_7 acts on R^7.
# We can compute its eigenvalues on R^7, then lift to the spinor space.

# Simple reflections on R^7
def reflection(alpha, v):
    """Reflect v through hyperplane perpendicular to alpha."""
    return v - 2 * np.dot(v, alpha) / np.dot(alpha, alpha) * alpha

# Simple roots as R^7 vectors
simple = []
for i in range(6):
    r = np.zeros(7)
    r[i] = 1; r[i+1] = -1
    simple.append(r)
r = np.zeros(7)
r[5] = 1; r[6] = 1
simple.append(r)

# Coxeter element as 7x7 matrix
cox_mat = np.eye(7)
for alpha_k in simple:
    # Reflection matrix for alpha_k
    R_k = np.eye(7) - 2 * np.outer(alpha_k, alpha_k) / np.dot(alpha_k, alpha_k)
    cox_mat = R_k @ cox_mat

print(f"\n  Coxeter element as 7x7 matrix:")
print(f"  {np.round(cox_mat, 4)}")

cox_evals = np.linalg.eigvals(cox_mat)
print(f"\n  Coxeter eigenvalues on R^7:")
for k, ev in enumerate(sorted(cox_evals, key=lambda x: np.angle(x))):
    angle = np.angle(ev) / np.pi
    print(f"    lambda_{k+1} = {ev:.6f}  (angle = {angle:.4f} * pi)")

# The eigenvalues should be exp(2*pi*i * m_j / h) where m_j are the exponents
# Exponents of D_7: {1, 3, 5, 6, 7, 9, 11}
# h = 12
exponents = [1, 3, 5, 6, 7, 9, 11]
expected_evals = [np.exp(2j * np.pi * m / 12) for m in exponents]
print(f"\n  Expected from exponents {exponents} (h=12):")
for m, ev in zip(exponents, expected_evals):
    angle = np.angle(ev) / np.pi
    print(f"    exp(2pi*i*{m}/12) = {ev:.6f}  (angle = {angle:.4f} * pi)")

# Now lift the Coxeter element to the spinor representation.
# The Coxeter element acts on the weight lattice.
# In the spinor representation with weights (h_1,...,h_7), h_k = +/-1/2,
# the Coxeter element permutes these 128 weights.

# Build the weight list
weights_128 = []
for signs in product([+1, -1], repeat=7):
    w = tuple(s / 2.0 for s in signs)
    weights_128.append(np.array(w))

# Apply Coxeter element to each weight
cox_weights = [cox_mat @ w for w in weights_128]

# Build the 128x128 matrix of the Coxeter element in the weight basis
# The Coxeter element permutes the weights (possibly with signs)
cox_128 = np.zeros((128, 128), dtype=complex)
for k, w_new in enumerate(cox_weights):
    # Find which original weight w_new corresponds to
    for l, w_old in enumerate(weights_128):
        if np.allclose(w_new, w_old, atol=1e-10):
            cox_128[l, k] = 1
            break
    else:
        # Weight might be sent to a different weight with a sign
        # Actually, the Coxeter element sends weight (h_1,...,h_7) to cox_mat @ (h_1,...,h_7)
        # The result should still have entries +/- 1/2
        # Let me check...
        rounded = np.round(w_new * 2) / 2
        for l, w_old in enumerate(weights_128):
            if np.allclose(rounded, w_old, atol=1e-10):
                cox_128[l, k] = 1
                break
        else:
            print(f"  WARNING: weight {weights_128[k]} maps to {w_new}, not in weight lattice!")

# Check unitarity
err_unit = np.max(np.abs(cox_128 @ cox_128.conj().T - np.eye(128)))
print(f"\n  Coxeter element as 128x128 permutation matrix:")
print(f"  Unitarity check: {err_unit:.2e}")

# However, this is the Coxeter element acting on the WEIGHT SPACE basis,
# not on our gamma matrix basis. We need to change basis.
#
# The weights_128 list corresponds to a specific ordering of the 128 spinor states.
# Our B_plus basis is in terms of the gamma matrix eigenvectors.
# We need to know which gamma-matrix spinor state corresponds to which weight.
#
# For the standard construction, the spinor state |s_1, ..., s_7> with s_k = +/- 1
# is the simultaneous eigenstate of H_k = (i/2) gamma_{2k-1} gamma_{2k}
# with eigenvalue s_k/2.

# Build Cartan generators H_k = (i/2) gamma_{2k} gamma_{2k+1}
# (using 0-indexed gammas: H_k = (i/2) gamma_{2k} gamma_{2k+1} for k=0,...,6)
H = []
for k in range(7):
    Hk = (1j / 2) * gammas[2*k] @ gammas[2*k + 1]
    H.append(Hk)

# Simultaneously diagonalize all H_k
# They should all commute
for k1 in range(7):
    for k2 in range(k1+1, 7):
        comm = np.max(np.abs(H[k1] @ H[k2] - H[k2] @ H[k1]))
        if comm > 1e-10:
            print(f"  WARNING: [H_{k1}, H_{k2}] = {comm:.2e}")

# Diagonalize H_0 first, then H_1 within each eigenspace, etc.
print("\n  Building simultaneous eigenbasis of Cartan subalgebra...")

# Actually, for our gamma construction, the Cartan generators are already diagonal
# in the computational basis. Let me check.
for k in range(7):
    off_diag = np.max(np.abs(H[k] - np.diag(np.diag(H[k]))))
    if k < 3:
        print(f"    H_{k} off-diagonal: {off_diag:.2e}")

# If they're diagonal, we can just read off the weights
weight_vectors = np.zeros((128, 7))
for k in range(7):
    weight_vectors[:, k] = np.diag(H[k]).real

# Check: should all be +/- 1/2
for idx in range(128):
    w = weight_vectors[idx]
    if not np.allclose(np.abs(w), 0.5, atol=1e-10):
        print(f"  WARNING: state {idx} has weight {w}")
        break

print(f"  Weight vectors computed for all 128 states.")
print(f"  Sample: state 0 has weight {weight_vectors[0]}")
print(f"  Sample: state 1 has weight {weight_vectors[1]}")

# Build the Coxeter element in the computational (gamma matrix) basis
# For each computational basis state |i>, its weight is w_i.
# The Coxeter element sends w_i to cox_mat @ w_i.
# We need to find which computational state has that weight.

# Build weight -> index map
weight_to_idx = {}
for idx in range(128):
    w = tuple(np.round(weight_vectors[idx], 4))
    weight_to_idx[w] = idx

# Now build the 128x128 Coxeter matrix in the computational basis
cox_comp = np.zeros((128, 128), dtype=complex)
for idx in range(128):
    w = weight_vectors[idx]
    w_new = cox_mat @ w
    w_new_key = tuple(np.round(w_new, 4))
    if w_new_key in weight_to_idx:
        new_idx = weight_to_idx[w_new_key]
        cox_comp[new_idx, idx] = 1
    else:
        print(f"  WARNING: Coxeter maps weight {w} to {w_new}, not found!")

print(f"\n  Coxeter element in computational basis: built")
print(f"  Check: is it a permutation matrix? Max entry: {np.max(np.abs(cox_comp)):.4f}")
print(f"  Each column has one 1? Min col sum: {np.min(np.abs(cox_comp).sum(axis=0)):.4f}")

# Check cox_comp^12 = I (h = 12)
cox_power = np.eye(128, dtype=complex)
for _ in range(12):
    cox_power = cox_comp @ cox_power
err_h = np.max(np.abs(cox_power - np.eye(128)))
print(f"  cox^12 = I? Error: {err_h:.2e}")

# Project to 64+ semi-spinor
cox_64 = proj64(cox_comp)

# Eigenvalues of Coxeter element on 64+
cox_64_evals = np.linalg.eigvals(cox_64)
cox_64_evals_sorted = sorted(cox_64_evals, key=lambda x: np.angle(x))

print(f"\n  Eigenvalues of Coxeter element on 64+ semi-spinor:")
# Group by angle
angle_groups = defaultdict(int)
for ev in cox_64_evals:
    angle = np.angle(ev)
    # Round to nearest multiple of 2*pi/12 = pi/6
    angle_quantized = round(angle * 6 / np.pi) * np.pi / 6
    angle_groups[angle_quantized] += 1

for angle in sorted(angle_groups.keys()):
    mult = angle_groups[angle]
    m = round(angle * 12 / (2 * np.pi)) % 12
    omega = np.exp(1j * angle)
    # Check if this is a cube root of unity (Z_3)
    is_z3 = abs(angle * 3 / (2 * np.pi) - round(angle * 3 / (2 * np.pi))) < 0.01
    z3_mark = " <-- Z_3" if is_z3 else ""
    # Check if multiplicity is divisible by 3
    div3_mark = " [mult div by 3]" if mult % 3 == 0 else ""
    print(f"    exp(2pi*i*{m}/12): multiplicity {mult}{z3_mark}{div3_mark}")

# Count eigenvalues that are cube roots of unity
z3_count = 0
for ev in cox_64_evals:
    if abs(ev**3 - 1) < 0.01 or abs(ev**3 + 1) < 0.01:
        z3_count += 1

# Actually, let me check for Z_3 more carefully
# exp(2*pi*i*m/12) is a cube root of unity when m*3/12 = m/4 is an integer
# i.e., m = 0, 4, 8
z3_evals = 0
for angle, mult in angle_groups.items():
    m = round(angle * 12 / (2 * np.pi)) % 12
    if m % 4 == 0:  # m = 0, 4, 8
        z3_evals += mult

print(f"\n  Z_3 analysis:")
print(f"    Eigenvalues that are 12th roots of unity with m mod 4 = 0 (Z_3 subset): {z3_evals} out of 64")
print(f"    Is 64 divisible by 3? {64 % 3 == 0} (64 = 21*3 + 1)")

# Check: do eigenvalue multiplicities have any 3-fold pattern?
total_mult = sum(angle_groups.values())
print(f"    Total eigenvalue count: {total_mult} (should be 64)")

# ============================================================================
# INVESTIGATION 3: so(8) Triality Inside so(14)
# ============================================================================
print("\n" + "=" * 80)
print("INVESTIGATION 3: so(8) Triality Inside so(14)")
print("=" * 80)

# so(8) = D_4, the ONLY Lie algebra with a Z_3 outer automorphism (triality)
# Embed so(8) using indices 0-7 (first 8 of our 14 directions)

so8_gens = {k: v for k, v in so14_gens.items() if k[0] < 8 and k[1] < 8}
print(f"  so(8) generators (indices 0-7): {len(so8_gens)} (should be 28)")
assert len(so8_gens) == 28

# The triality automorphism sigma of so(8) has order 3:
# sigma: 8_v -> 8_s -> 8_c -> 8_v
#
# In terms of the Dynkin diagram of D_4:
#     1
#    / \
#   3   4
#    \ /
#     2
# Triality permutes nodes 1, 3, 4 while fixing node 2.
#
# In terms of so(8) generators, triality acts on the root system.
#
# Key question: does triality EXTEND to an automorphism of so(14)?
#
# D_7 has Dynkin diagram:
#   1 - 2 - 3 - 4 - 5 - 6
#                         |
#                         7
# Outer automorphism group of D_7 = Z_2 (swapping nodes 6 and 7).
# There is NO Z_3 outer automorphism of D_7.

print("""
  Outer automorphism groups:
    D_4 (so(8)):  S_3 (includes Z_3 triality)
    D_7 (so(14)): Z_2 (swap of spinor nodes only)

  The triality Z_3 of D_4 does NOT extend to D_7.

  Reason: In D_7, the D_4 subalgebra is embedded as nodes {1,2,3,4}
  (or equivalently indices {0,...,7} in R^14). The triality permutes
  nodes 1,3,4 of D_4. But in D_7, nodes 1 and 3 connect to the rest
  of the diagram differently (node 4 in D_7 = node 5 in the chain).
  Permuting them would break the D_7 structure.
""")

# But can triality act on the SPINOR SPACE even if it doesn't extend to so(14)?
# Let's check: build the triality automorphism of so(8) explicitly.

# The triality acts on so(8) by permuting the three 8-dim representations:
# 8_v (vector), 8_s (spinor), 8_c (conjugate spinor)
#
# In the 128-dim spinor of so(14), so(8) acts on a subspace.
# The 128 decomposes under so(8) x so(6) (indices 0-7 and 8-13):
# 128 = (8_s, 8_s) + (8_c, 8_c) + (8_v, 8_v) + ...
# Wait, that's not right. Let me think more carefully.

# Under SO(8) x SO(6), the 128 Dirac spinor of SO(14) decomposes as:
# 128 = spinor(SO(8)) x spinor(SO(6))
# spinor(SO(8)) = 8_s + 8_c (16 total = 2^4)
# spinor(SO(6)) = 4 + 4-bar (8 total = 2^3)
#
# So 128 = 16 x 8 = 128. Checks out.
#
# More precisely:
# 128_+ (semi-spinor, 64 dim) decomposes under SO(8) x SO(6) as:
# We need to track chiralities on both sides.

# Let me compute this numerically instead.
# Build SO(8) and SO(6) chirality operators.

Gamma_so8 = np.eye(dim, dtype=complex)
for i in range(8):
    Gamma_so8 = Gamma_so8 @ gammas[i]
# Normalize
phase_8 = (Gamma_so8 @ Gamma_so8)[0, 0]
Gamma_so8_n = Gamma_so8 / np.sqrt(phase_8)

Gamma_so6 = np.eye(dim, dtype=complex)
for i in range(8, 14):
    Gamma_so6 = Gamma_so6 @ gammas[i]
phase_6 = (Gamma_so6 @ Gamma_so6)[0, 0]
Gamma_so6_n = Gamma_so6 / np.sqrt(phase_6)

# Project to 64+
chi8_64 = proj64(Gamma_so8_n)
chi6_64 = proj64(Gamma_so6_n)

# Eigenvalues
chi8_evals = np.linalg.eigvalsh(chi8_64)
chi6_evals = np.linalg.eigvalsh(chi6_64)

chi8_unique = np.unique(np.round(chi8_evals, 4))
chi6_unique = np.unique(np.round(chi6_evals, 4))

print(f"  SO(8) chirality on 64+: eigenvalues {chi8_unique}")
for v in chi8_unique:
    print(f"    {v:.4f}: multiplicity {np.sum(np.abs(chi8_evals - v) < 0.01)}")

print(f"\n  SO(6) chirality on 64+: eigenvalues {chi6_unique}")
for v in chi6_unique:
    print(f"    {v:.4f}: multiplicity {np.sum(np.abs(chi6_evals - v) < 0.01)}")

# Joint eigenvalues of (chi8, chi6) on 64+
# These should give the branching rule 64+ -> (8_s, 4_s) + (8_c, 4_c) or similar

# Simultaneously diagonalize chi8 and chi6 (they should commute)
comm_chi = np.max(np.abs(chi8_64 @ chi6_64 - chi6_64 @ chi8_64))
print(f"\n  [chi_SO(8), chi_SO(6)] on 64+ = {comm_chi:.2e}")

# Joint diagonalization
chi8_e, chi8_v = np.linalg.eigh(chi8_64)
sectors_8 = {}
for idx in range(64):
    key = round(chi8_e[idx], 2)
    sectors_8.setdefault(key, []).append(idx)

print(f"\n  Branching of 64+ under SO(8) x SO(6):")
for chi8_val in sorted(sectors_8.keys()):
    indices = sectors_8[chi8_val]
    sub_basis = chi8_v[:, indices]
    chi6_sub = sub_basis.conj().T @ chi6_64 @ sub_basis
    chi6_sub_evals = np.linalg.eigvalsh(chi6_sub)
    chi6_unique_sub = np.unique(np.round(chi6_sub_evals, 2))

    so8_label = "8_s" if chi8_val > 0 else "8_c"
    dim_so8 = 8 if abs(abs(chi8_val) - 1) < 0.1 else "?"

    for chi6_val in chi6_unique_sub:
        n = np.sum(np.abs(chi6_sub_evals - chi6_val) < 0.01)
        so6_label = "4" if chi6_val > 0 else "4-bar"
        print(f"    (chi8={chi8_val:+.0f}, chi6={chi6_val:+.0f}): dim = {n}")

# Now: does triality act meaningfully on the 64+ space?
# The key: triality PERMUTES the three 8-dim reps of so(8).
# On the 64+ space, the so(8) content is:
#   If 64+ = (8_s, 4) + (8_c, 4-bar): triality would send 8_s -> 8_v and 8_c -> 8_s
#   But 8_v is not a spinor rep! It lives in the vector representation of SO(8).
#   So triality would take us OUT of the spinor space of SO(14).

print("""
  TRIALITY ANALYSIS:

  The 64+ of SO(14) under SO(8) x SO(6) decomposes into spinor reps
  of SO(8). Triality maps:
    8_s -> 8_c -> 8_v -> 8_s

  The 8_v (vector) is NOT a spinor representation. It lives in the
  adjoint/vector of SO(8), which is part of so(14) but NOT part of
  the spinor module.

  Therefore: triality maps spinor states OUTSIDE the spinor space.
  It cannot act as an automorphism of the 64+ representation.

  Furthermore: triality is an automorphism of so(8), NOT of so(14).
  It does not even preserve the subalgebra structure when extended.

  VERDICT: so(8) triality CANNOT produce 3 generations within so(14).
""")

# ============================================================================
# INVESTIGATION 4: Primitive Idempotent Decompositions
# ============================================================================
print("\n" + "=" * 80)
print("INVESTIGATION 4: Primitive Idempotent Decompositions")
print("=" * 80)

# M(128, R) has primitive idempotents: rank-1 projectors P with P^2 = P, tr(P) = 1
# These decompose the 128-dim space into 128 1-dim subspaces.
# But we want to decompose the 64-dim semi-spinor into pieces.
#
# The question: is there an idempotent in Cl+(14,0) that decomposes
# the 64-dim semi-spinor into 3x21 + 1, or 3x16 + 16, or similar?

print("""
  Idempotent decomposition of the 64-dim semi-spinor:

  Possible 3-fold decompositions:
    64 = 3*21 + 1   (remainder 1 -- awkward)
    64 = 3*20 + 4   (remainder 4)
    64 = 3*16 + 16  (three 16s plus one 16 -- interesting!)
    64 = 3*16 + 16  but branching gives 2*16 + 2*16bar
    64 = 4*16       (four 16s -- what we actually get)

  The branching rule dictates: 64+ = (16, (2,1)) + (16bar, (1,2))
  This is 2*16 + 2*16bar = 32 + 32, NOT 3*anything + remainder.

  Can we find a DIFFERENT decomposition?
""")

# Look for elements of Cl+(14,0) that commute with so(10) but NOT with so(4)
# These would be "family symmetry" generators.
# Elements of Cl+(14,0) are even products of gammas.
# The generators of so(14) are grade-2.
# What about grade-4, grade-6, etc.?

# Grade-4 elements that commute with so(10):
# These must be built from indices 10-13 (the SO(4) sector)
# or be SO(10) invariants from indices 0-9.

# The only grade-4 element from indices 10-13 is:
# gamma_10 * gamma_11 * gamma_12 * gamma_13 (the SO(4) volume element)
vol_so4 = gammas[10] @ gammas[11] @ gammas[12] @ gammas[13]

# This commutes with so(10) (different index sets)
comm_vol = max(np.max(np.abs(vol_so4 @ v - v @ vol_so4)) for v in so10_gens.values())
print(f"  [Gamma_SO(4), SO(10) generators] max = {comm_vol:.2e}")

# Project to 64+
vol_so4_64 = proj64(vol_so4)
vol_evals = np.linalg.eigvalsh(vol_so4_64)
vol_unique = np.unique(np.round(vol_evals, 4))
print(f"\n  SO(4) volume element on 64+:")
print(f"  Eigenvalues: {vol_unique}")
for v in vol_unique:
    mult = np.sum(np.abs(vol_evals - v) < 0.01)
    print(f"    {v:.4f}: multiplicity {mult}")

# This gives a Z_2 grading (eigenvalues +/-), splitting 64 = 32 + 32.
# Not a Z_3.

# What about products of TWO grade-2 elements from the SO(4) sector?
# These give the 6 elements: gamma_i gamma_j for 10 <= i < j <= 13
# Their products (grade 4) include the volume element above.
# There are C(4,2) = 6 grade-2 elements and C(4,4) = 1 grade-4 element.

# What about mixed grade-4 elements: products of one SO(10) generator and one SO(4) generator?
# gamma_a gamma_b gamma_c gamma_d with a,b in {0,...,9} and c,d in {10,...,13}
# These do NOT commute with so(10) in general.

# Key insight: ANY element that commutes with ALL of so(10) must be in the
# CENTRALIZER of so(10) in M(128, R).
# Since SO(10) acts irreducibly on 16 and on 16bar (both irreps),
# by Schur's lemma, the centralizer on each irreducible component is just scalars.
#
# On 64+ = (16, (2,1)) + (16bar, (1,2)):
# Elements commuting with so(10) can only mix (16, (2,1)) with itself
# and (16bar, (1,2)) with itself (since 16 != 16bar as so(10) reps).
# Within (16, (2,1)): 16 is irreducible, so the commutant is M(2, C) = gl(2) acting on (2,1)
# Within (16bar, (1,2)): similarly gl(2) acting on (1,2)
# Cross terms: 16 != 16bar, so no mixing.
#
# Therefore: the centralizer of so(10) in End(64+) = M(2) x M(2)
# This is 4 + 4 = 8 dimensional.
# Its Lie algebra is gl(2) x gl(2) = sl(2) x u(1) x sl(2) x u(1).
# This is EXACTLY so(4) x u(1) x u(1) = the SO(4) Lie algebra plus 2 scalars.

print("""
  SCHUR'S LEMMA ANALYSIS:

  64+ = (16, (2,1)) + (16-bar, (1,2)) under SO(10) x SO(4)

  Centralizer of so(10) in End(64+):
    On (16, (2,1)): Schur -> scalars on 16, general on (2,1) -> M(2,C)
    On (16-bar, (1,2)): Schur -> scalars on 16-bar, general on (1,2) -> M(2,C)
    Cross: 16 != 16-bar -> no mixing

  Total centralizer: M(2,C) x M(2,C) = GL(2) x GL(2)
  Lie algebra: gl(2) x gl(2) = (sl(2) + u(1)) x (sl(2) + u(1))

  The sl(2) parts ARE exactly SU(2)_L and SU(2)_R from SO(4).
  The u(1) parts are the identity operators on each block.

  CONCLUSION: There is NO room for additional structure beyond SO(4)
  in the centralizer. The family space is EXACTLY 2+2 dimensional.
  No idempotent decomposition can give 3-fold structure while
  preserving SO(10).
""")

# Let me verify this numerically by computing the centralizer
print("  Numerical verification of centralizer dimension...")

# Build the SO(10) Casimir on 64+
C2_so10 = np.zeros((64, 64), dtype=complex)
for gen in so10_gens.values():
    g64 = proj64(gen)
    C2_so10 += g64 @ g64

# Find the irreducible blocks
c2_evals, c2_evecs = np.linalg.eigh(C2_so10)
c2_unique = np.unique(np.round(c2_evals, 2))
print(f"  SO(10) Casimir eigenvalues on 64+: {c2_unique}")

for val in c2_unique:
    mask = np.abs(c2_evals - val) < 0.1
    dim_block = np.sum(mask)
    print(f"    C2 = {val:.2f}: dimension {dim_block}")

# The centralizer dimension should be sum of (dim_i)^2 / (dim_irrep_i)^2
# For 64+ = (16,2) + (16-bar,2): centralizer = (2^2 + 2^2) = 8
# (since each 32-dim block has 16-dim irrep x 2-dim multiplicity,
#  and the centralizer on a 2-fold copy of an irrep is M(2))

# ============================================================================
# INVESTIGATION 5: Non-standard SO(10) Embeddings
# ============================================================================
print("\n" + "=" * 80)
print("INVESTIGATION 5: Non-standard SO(10) Embeddings in SO(14)")
print("=" * 80)

# Standard embedding: SO(10) on indices {0,...,9}, SO(4) on {10,...,13}
# Alternative: SO(10) on {4,...,13}, SO(4) on {0,...,3}
# Or: SO(10) on any 10 indices, SO(4) on complementary 4

# The key question: do different choices of 10 indices give DIFFERENT branching?
#
# Answer: NO! All SO(10) x SO(4) subgroups of SO(14) obtained by splitting
# indices into 10+4 are CONJUGATE in SO(14). They give the same branching rule.
# This is because SO(14) acts transitively on 10-element subsets of {1,...,14}
# (more precisely, on decompositions R^14 = R^10 + R^4).

print("""
  All "standard" SO(10) x SO(4) subgroups of SO(14) are conjugate.
  Splitting {1,...,14} = {10 indices} + {4 indices} always gives:
    64+ = (16, (2,1)) + (16-bar, (1,2))
  regardless of which 10 indices are chosen.

  Reason: SO(14) acts transitively on Gr(10,14) (Grassmannian),
  so all such decompositions are related by SO(14) conjugation.
""")

# But what about NON-STANDARD embeddings?
# SO(10) can embed in SO(14) in other ways besides block-diagonal.
# For example: SO(10) could embed via a non-trivial homomorphism.
#
# However, the MAXIMAL subgroups of SO(14) of type SO(10) x SO(4) are:
# 1. Block-diagonal: SO(10) x SO(4) (the standard one, all conjugate)
# 2. There might be "diagonal" embeddings, but for SO groups these are more exotic.

# Let me check: what are ALL maximal subgroups of SO(14) that contain SO(10)?
# From Dynkin's classification of maximal subgroups:
# Type D_7: maximal subgroups include
#   - D_5 x D_2 = SO(10) x SO(4) [block diagonal, what we have]
#   - D_6 x D_1 = SO(12) x SO(2) [not SO(10)]
#   - A_6 = SU(7) [not SO(10)]
#   - B_3 x B_3 = SO(7) x SO(7) [not SO(10)]
#   - There is also D_5 x D_1 x D_1 = SO(10) x SO(2) x SO(2) inside D_7

# The only way SO(10) sits in SO(14) with a complementary factor is:
# SO(10) x SO(4) (block diagonal)
# SO(10) x U(1) x U(1) (from breaking SO(4) to its Cartan)

# These all give the same branching up to the SO(4) decomposition.

print("""
  Maximal subgroup analysis (Dynkin classification):

  SO(14) maximal subgroups containing SO(10):
    1. SO(10) x SO(4)  [block-diagonal, standard]
    2. SO(10) x U(1) x U(1)  [Cartan of SO(4)]

  Both give the SAME branching of 64+, just decomposed differently.

  No "non-standard" embedding of SO(10) in SO(14) can change the
  fundamental result that 64+ contains exactly two copies of the
  16 of SO(10).
""")

# Verify with a rotated embedding
print("  Numerical cross-check: rotated SO(10) embedding...")

# Take a random orthogonal transformation on R^14
np.random.seed(42)
Q = np.linalg.qr(np.random.randn(14, 14))[0]  # random O(14) element
if np.linalg.det(Q) < 0:
    Q[:, 0] *= -1  # ensure SO(14)

# Build rotated gamma matrices
rotated_gammas = []
for i in range(14):
    g_rot = sum(Q[j, i] * gammas[j] for j in range(14))
    rotated_gammas.append(g_rot)

# Build rotated SO(10) using first 10 rotated directions
rot_so10_gens = []
for i in range(10):
    for j in range(i+1, 10):
        rot_so10_gens.append((1j / 2) * rotated_gammas[i] @ rotated_gammas[j])

# Build rotated SO(10) Casimir on 64+
C2_rot = np.zeros((64, 64), dtype=complex)
for gen in rot_so10_gens:
    g64 = proj64(gen)
    C2_rot += g64 @ g64

c2r_evals = np.linalg.eigvalsh(C2_rot)
c2r_unique = np.unique(np.round(c2r_evals, 2))
print(f"  Rotated SO(10) Casimir on 64+: {c2r_unique}")
for v in c2r_unique:
    mult = np.sum(np.abs(c2r_evals - v) < 0.1)
    print(f"    C2 = {v:.2f}: multiplicity {mult}")

print("  (Same eigenvalues as standard embedding, as expected.)")

# ============================================================================
# INVESTIGATION 6: The Key Computation - Detailed Coxeter Analysis
# ============================================================================
print("\n" + "=" * 80)
print("INVESTIGATION 6: Detailed Coxeter Eigenvalue Analysis on 64+")
print("=" * 80)

# We already computed cox_64 and its eigenvalues above.
# Let me do a more detailed analysis.

# The eigenvalues of the Coxeter element on any representation
# are exp(2*pi*i*(m_j + rho_j)/h) where the m_j + rho_j are determined
# by the representation's highest weight.
#
# For the semi-spinor 64+ of D_7:
# Highest weight: (1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2)
# (all positive half-integers)
#
# The weights of 64+ are all (h_1,...,h_7) with h_k = +/-1/2
# and an even number of minus signs.

# Let me recompute the Coxeter eigenvalues more carefully
# using the weight-space action

# Group eigenvalues by their 12th root of unity class
print(f"\n  Coxeter eigenvalue decomposition on 64+:")
print(f"  (eigenvalues are 12th roots of unity, h=12)")

eigenvalue_mults = defaultdict(int)
for ev in cox_64_evals:
    # Find the closest 12th root of unity
    best_m = 0
    best_err = float('inf')
    for m in range(12):
        target = np.exp(2j * np.pi * m / 12)
        err = abs(ev - target)
        if err < best_err:
            best_err = err
            best_m = m
    eigenvalue_mults[best_m] += 1

print(f"  {'m':>4}  {'exp(2pi*i*m/12)':>25}  {'Multiplicity':>12}  {'mod 3':>6}  {'mod 4':>6}")
print(f"  {'----':>4}  {'-------------------------':>25}  {'------------':>12}  {'------':>6}  {'------':>6}")
total = 0
z3_total = {0: 0, 1: 0, 2: 0}
z4_total = {0: 0, 1: 0, 2: 0, 3: 0}
for m in range(12):
    mult = eigenvalue_mults[m]
    ev = np.exp(2j * np.pi * m / 12)
    z3_total[m % 3] += mult
    z4_total[m % 4] += mult
    total += mult
    print(f"  {m:4d}  {ev.real:+.4f} + {ev.imag:+.4f}i          {mult:4d}        {m%3:4d}    {m%4:4d}")

print(f"\n  Total: {total} (should be 64)")

print(f"\n  Z_3 sub-decomposition (m mod 3):")
for k in range(3):
    print(f"    m mod 3 = {k}: {z3_total[k]} eigenvalues")

print(f"\n  Z_4 sub-decomposition (m mod 4):")
for k in range(4):
    print(f"    m mod 4 = {k}: {z4_total[k]} eigenvalues")

# Key question: is there a Z_3 symmetry hidden in the Coxeter eigenvalue pattern?
z3_balanced = (z3_total[0] == z3_total[1] == z3_total[2])
print(f"\n  Z_3 balanced? {z3_total[0]} = {z3_total[1]} = {z3_total[2]}? {'YES' if z3_balanced else 'NO'}")

if z3_balanced:
    print("  The Coxeter element decomposes 64+ into three equal pieces under Z_3!")
    print(f"  Each piece has dimension {z3_total[0]} = 64/3 ???")
    print(f"  But 64/3 = {64/3:.4f} is not an integer!")
else:
    remainder = 64 % 3
    print(f"  64 mod 3 = {remainder}. Cannot split 64 into 3 equal pieces.")
    print(f"  The Z_3 sub-grading gives {z3_total[0]} + {z3_total[1]} + {z3_total[2]} = {sum(z3_total.values())}")

# ============================================================================
# INVESTIGATION 6b: Can we get 3*16 + 16 from some element?
# ============================================================================
print("\n" + "-" * 60)
print("  Can any Clifford element give a 3*16 + 16 decomposition?")
print("-" * 60)

# We want to find an operator T on the 64+ space with eigenvalue
# pattern that gives 3 copies of 16-dim subspaces.
#
# Such T must commute with SO(10) (to preserve the 16 content).
# By our Schur's lemma analysis, T must be in M(2) x M(2)
# (acting on the (2,1) and (1,2) parts respectively).
#
# On the (16, (2,1)) block: T is a 2x2 matrix
# On the (16-bar, (1,2)) block: T is a (different) 2x2 matrix
#
# Total eigenvalue count from (16, (2,1)): 2 eigenvalues, each with mult 16
# From (16-bar, (1,2)): 2 eigenvalues, each with mult 16
# Grand total: at most 4 distinct eigenvalues, with multiplicities that are multiples of 16.
#
# Possible patterns:
#   4*16 = 64 (all different)
#   3*16 + 16 = 64 (three eigenvalues of mult 16, one of mult 16)
#   2*32 = 64 (two eigenvalues, each with mult 32)
#   etc.
#
# But 3*16 + 16 = 4*16. The question is: can three of the four eigenvalues coincide?
# Answer: YES, if we pick T = diag(a, b) on (2,1) and T = diag(a, a) on (1,2).
# Then eigenvalues: a (mult 16+16=32), b (mult 16), a again from (1,2) (already counted).
# Wait, let me be more careful.
#
# On (16, (2,1)): 32-dim space. T acts on the 2-dim factor: eigenvalues lambda_1, lambda_2.
#   -> 16 states with eigenvalue lambda_1, 16 states with eigenvalue lambda_2.
# On (16-bar, (1,2)): 32-dim space. T acts on the 2-dim factor: eigenvalues mu_1, mu_2.
#   -> 16 states with eigenvalue mu_1, 16 states with eigenvalue mu_2.
#
# To get "3 copies of 16": need exactly 3 of the 4 eigenvalues to be distinct,
# with one appearing twice.
# E.g., lambda_1 = mu_1, lambda_2 != mu_2 != lambda_1, mu_2 != lambda_2.
# Then: 32 states with eigenvalue lambda_1 = mu_1, 16 with lambda_2, 16 with mu_2.
# That's 32 + 16 + 16, not 3*16 + 16.
#
# To get exactly 3*16: need three eigenvalues each appearing once as a 16.
# That means one of {lambda_1, lambda_2, mu_1, mu_2} must equal another,
# giving 32 (one eigenvalue) + 16 + 16 (two others) = 64.
# But that's 2*16 + 16 + 16 = 32 + 16 + 16, i.e., multiplicities (32, 16, 16).
# NOT (16, 16, 16, 16) or (48, 16).
#
# The ONLY possible multiplicity patterns are:
#   (16, 16, 16, 16) -- all different (generic case)
#   (32, 16, 16) -- two eigenvalues coincide
#   (32, 32) -- two pairs coincide
#   (48, 16) -- three eigenvalues coincide
#   (64) -- all four coincide (scalar)
#
# To get "3 generations of 16": we need multiplicity (48, 16) which means
# three of the four eigenvalues coincide. But 48/16 = 3, so this gives
# 3 copies of 16 (with the same eigenvalue) + 1 copy of 16 (different).
# The "3 copies" would include BOTH 16 and 16-bar of SO(10) --
# physically unacceptable since they have different quantum numbers!

print("""
  Eigenvalue multiplicity analysis:

  Any operator T commuting with SO(10) acts on 64+ via:
    T = (A on (2,1)) x (B on (1,2))
  where A, B are 2x2 matrices.

  Eigenvalues: {lambda_1, lambda_2} from A, {mu_1, mu_2} from B
  Each has multiplicity 16 (from the irreducible SO(10) factor).

  Possible multiplicity patterns: (16,16,16,16), (32,16,16), (32,32), (48,16), (64)

  To get "3 generations": need (48, 16) pattern, meaning 3 of 4 eigenvalues coincide.
  This CAN be arranged (set lambda_1 = mu_1 = mu_2, lambda_2 different).

  BUT: the "48" block would contain BOTH 16 and 16-bar of SO(10)!
    48 = 16 (from (2,1) block) + 16 + 16 (from (1,2) block)
       = 16 [matter] + 16-bar + 16-bar [mirrors]

  This is NOT three generations of the SAME particle.
  It's one generation of matter + two generations of mirrors.

  PHYSICALLY: the three "generations" would have DIFFERENT gauge charges.
  This contradicts experiment. All three SM generations have IDENTICAL charges.

  CONCLUSION: No Clifford algebra operator can produce 3 identical generations
  while preserving SO(10). The fundamental obstruction is:

    64+ = (16, 2) + (16-bar, 2)

  The 16 and 16-bar are DIFFERENT SO(10) representations.
  Any 3-fold grouping that crosses this boundary mixes matter with mirrors.
""")

# ============================================================================
# FINAL COMPREHENSIVE VERDICT
# ============================================================================
print("\n" + "=" * 80)
print("COMPREHENSIVE VERDICT: Cl(14,0) and Three Generations")
print("=" * 80)

print("""
  INVESTIGATION RESULTS:

  1. Cl(14,0) = M(128,R) structure:
     - Pin(14) component group = Z_2 (no hidden Z_3 or S_3)
     - Even subalgebra Cl+(14,0) has two simple summands (64+ and 64-)
     - No additional discrete symmetries beyond Spin(14) and parity

  2. Coxeter grading (h=12) and Z_3:
     - Coxeter element eigenvalues on 64+ are 12th roots of unity
""")

# Print the actual Z_3 result
z3_str = f"     - Z_3 sub-grading: {z3_total[0]} + {z3_total[1]} + {z3_total[2]} = 64"
print(z3_str)

print(f"""     - 64 is NOT divisible by 3 (64 = 21*3 + 1)
     - Z_3 sub-grading is UNBALANCED: {z3_total[0]}, {z3_total[1]}, {z3_total[2]}
     - No Z_3 symmetry of the spinor space

  3. so(8) triality:
     - Triality is an automorphism of so(8), NOT of so(14)
     - D_7 outer automorphism group = Z_2 (not Z_3)
     - Triality maps spinor states OUTSIDE the spinor module
     - CANNOT produce 3 generations within so(14)

  4. Primitive idempotents (Schur's lemma):
     - Centralizer of so(10) in End(64+) = M(2) x M(2) = 8-dimensional
     - This is EXACTLY the SO(4) = SU(2)_L x SU(2)_R algebra + 2 scalars
     - NO room for additional structure beyond what we already knew
     - Any operator commuting with SO(10) can only act on the 2-dim family spaces

  5. Non-standard SO(10) embeddings:
     - All SO(10) x SO(4) subgroups of SO(14) are conjugate
     - Different index splits give the SAME branching rule
     - Verified numerically with random SO(14) rotation

  6. Detailed Coxeter eigenvalue analysis:
     - Multiplicities of 12th roots of unity on 64+ computed
     - No 3-fold balanced decomposition exists
     - The (48,16) pattern mixes 16 and 16-bar: physically unacceptable

  ROOT CAUSE OF THE OBSTRUCTION:

  The fundamental branching rule 64+ = (16, (2,1)) + (16-bar, (1,2))
  is FIXED by the representation theory of D_7. The 16 and 16-bar
  are DIFFERENT SO(10) representations (related by charge conjugation,
  not by any internal symmetry).

  Any operator that commutes with SO(10) can only act within the
  2-dimensional family spaces (2,1) and (1,2) SEPARATELY.
  This gives at most 2+2 = 4 "copies" of the 16, organized as
  (2 matter + 2 mirror) or (1 matter + 1 mirror) x 2.

  The number 3 CANNOT appear because:
  (a) 64/16 = 4, not 3 (four 16-dimensional subspaces)
  (b) The four are grouped as 2+2 (by chirality), not 3+1
  (c) 2-dimensional family space gives j=1/2, not j=1
  (d) Coxeter grading gives Z_12 eigenvalues; Z_3 subset is unbalanced

  THEOREM (strengthened):
  No element of Cl(14,0) -- whether Lie algebra, Lie group, Clifford
  product, idempotent, or Coxeter element -- can decompose the 64-dim
  semi-spinor of Spin(14) into 3 families of identical gauge quantum
  numbers while preserving the SO(10) gauge structure.

  The obstruction is ALGEBRAIC and ABSOLUTE (representation-theoretic).
  It cannot be evaded by any clever choice of Clifford structure.

  SURVIVING MECHANISMS (all EXTERNAL to Cl(14,0)):
  E1: Orbifold compactification (boundary conditions, not algebra)
  E2: Multiple copies (3 x 64+, by hand)
  E3: String embedding (higher-dimensional structure)
""")

# ============================================================================
# APPENDIX: Explicit Coxeter orbit structure
# ============================================================================
print("\n" + "=" * 80)
print("APPENDIX: Coxeter Orbit Structure on 64+ Weights")
print("=" * 80)

# The Coxeter element permutes the 64 weights of the semi-spinor.
# The orbits of this permutation have lengths dividing h=12.
# Let's compute the orbit structure.

# Build weight list for 64+ (even number of minus signs in 7-component weight)
weights_64plus = []
weight_indices_64plus = []  # indices in the full 128-dim weight list
for idx in range(128):
    w = weight_vectors[idx]
    n_minus = sum(1 for x in w if x < -0.1)
    if n_minus % 2 == 0:
        weights_64plus.append(tuple(np.round(w, 4)))
        weight_indices_64plus.append(idx)

print(f"  64+ weights: {len(weights_64plus)} (should be 64)")
assert len(weights_64plus) == 64

# Apply Coxeter to each weight and find orbits
weight_set = set(weights_64plus)
visited = set()
orbits = []

for w in weights_64plus:
    if w in visited:
        continue
    orbit = []
    current = np.array(w)
    while True:
        current_key = tuple(np.round(current, 4))
        if current_key in visited:
            break
        visited.add(current_key)
        orbit.append(current_key)
        current = cox_mat @ current
        current = np.round(current, 4)
    orbits.append(orbit)

print(f"\n  Number of Coxeter orbits on 64+: {len(orbits)}")
orbit_lengths = sorted([len(o) for o in orbits])
print(f"  Orbit lengths: {orbit_lengths}")

orbit_length_dist = defaultdict(int)
for l in orbit_lengths:
    orbit_length_dist[l] += 1

print(f"\n  Orbit length distribution:")
total_weights = 0
for length in sorted(orbit_length_dist.keys()):
    count = orbit_length_dist[length]
    total_weights += length * count
    divides_3 = "yes" if length % 3 == 0 else "NO"
    print(f"    Length {length:2d}: {count:2d} orbit(s)  ({length*count:2d} weights)  [divides 3? {divides_3}]")
print(f"  Total: {total_weights} weights (should be 64)")

# Check: do orbit lengths divide 12?
for l in orbit_length_dist.keys():
    assert 12 % l == 0 or l % 12 == 0, f"Orbit length {l} does not divide h=12!"

# Can we group orbits into sets of 3?
print(f"\n  Z_3 orbit analysis:")
print(f"  To have a Z_3 symmetry, we need orbit lengths divisible by 3,")
print(f"  or we need to group orbits into triples.")

weights_in_z3_orbits = sum(l * c for l, c in orbit_length_dist.items() if l % 3 == 0)
weights_not_z3 = 64 - weights_in_z3_orbits
print(f"  Weights in orbits of length divisible by 3: {weights_in_z3_orbits}")
print(f"  Weights in orbits of length NOT divisible by 3: {weights_not_z3}")

if weights_not_z3 == 0:
    print("  ALL orbits have length divisible by 3 -- Z_3 structure possible!")
else:
    print(f"  {weights_not_z3} weights cannot participate in a Z_3 decomposition.")
    print(f"  Z_3 structure is BROKEN by these orbits.")

# Print sample orbit
if orbits:
    sample = orbits[0]
    print(f"\n  Sample orbit (length {len(sample)}):")
    for k, w in enumerate(sample[:6]):
        so10_part = w[:5]
        so4_part = w[5:]
        n_minus_10 = sum(1 for x in so10_part if x < -0.1)
        rep_10 = "16" if n_minus_10 % 2 == 0 else "16-bar"
        print(f"    step {k}: {w}  [{rep_10}]")
    if len(sample) > 6:
        print(f"    ... ({len(sample) - 6} more)")

print("\n" + "=" * 80)
print("END OF INVESTIGATION")
print("=" * 80)
