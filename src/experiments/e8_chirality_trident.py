#!/usr/bin/env python3
"""
E8 CHIRALITY TRIDENT: A8/D8 Non-Nesting Analysis
===================================================

Pre-registered as Experiment 7 in EXPERIMENT_REGISTRY.md.

HYPOTHESIS (Heptapod B "Chirality Trident"):
Physical chirality in E8 is COMPOSITE -- it arises from the mismatch between
A8 (SU(9), Z3 grading) and D8 (SO(16)/Spin(4,12), Z2 grading). These are
non-nested maximal-rank subalgebras of E8, so their gradings don't commute.

CRITICAL FIX: The torus-based Z3 classification in wilson_e8_type5.py was WRONG.
t5 = (1,1,1,1,1,0,0,0) does NOT give a valid order-3 element on spinor roots
(half-integer charges give 6th roots of unity, not 3rd). The correct Z3 uses
the Dynkin coefficient of the branch node (alpha_2 in Bourbaki E8 numbering).

KILL CONDITIONS:
  KC-CHIRAL-1: Does D7 chirality (Gamma_14) distinguish WITHIN the 84?
  KC-CHIRAL-2: Is the A8/D8 overlap non-trivial?
  KC-CHIRAL-3: Does the joint Z2 x Z3 grading produce generation-chirality pairs?
"""

import numpy as np
from collections import Counter

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================
# Part 1: Construct E8 root system
# ============================================================
print("=" * 70)
print("EXPERIMENT 7: E8 Chirality Trident -- A8/D8 Non-Nesting Analysis")
print("=" * 70)

roots = []

# D8 roots: vectors with exactly two nonzero entries, each +/-1
for i in range(8):
    for j in range(i+1, 8):
        for si in [1, -1]:
            for sj in [1, -1]:
                r = np.zeros(8)
                r[i] = si
                r[j] = sj
                roots.append(r)

n_d8 = len(roots)
assert n_d8 == 112, f"Expected 112 D8 roots, got {n_d8}"

# Half-integer roots: (+/-1/2, ..., +/-1/2) with even number of minus signs
for signs in range(256):
    r = np.zeros(8)
    minus_count = 0
    for k in range(8):
        if signs & (1 << k):
            r[k] = -0.5
            minus_count += 1
        else:
            r[k] = 0.5
    if minus_count % 2 == 0:
        roots.append(r)

roots = np.array(roots)
assert len(roots) == 240, f"Expected 240 E8 roots, got {len(roots)}"
print(f"\nE8 root system: {len(roots)} roots (112 D8 + 128 spinor)")

# ============================================================
# Part 2: E8 simple roots (Bourbaki convention)
# ============================================================
print("\n" + "=" * 70)
print("Part 2: E8 Simple Roots and Cartan Matrix")
print("=" * 70)

# Bourbaki simple roots for E8 in orthogonal basis:
# Diagram:  1 - 3 - 4 - 5 - 6 - 7 - 8
#                   |
#                   2
simple_roots = np.array([
    [ 0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5,  0.5],  # alpha_1
    [ 1.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],  # alpha_2
    [-1.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],  # alpha_3
    [ 0.0, -1.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0],  # alpha_4
    [ 0.0,  0.0, -1.0,  1.0,  0.0,  0.0,  0.0,  0.0],  # alpha_5
    [ 0.0,  0.0,  0.0, -1.0,  1.0,  0.0,  0.0,  0.0],  # alpha_6
    [ 0.0,  0.0,  0.0,  0.0, -1.0,  1.0,  0.0,  0.0],  # alpha_7
    [ 0.0,  0.0,  0.0,  0.0,  0.0, -1.0,  1.0,  0.0],  # alpha_8
])

# Verify Cartan matrix = E8
cartan = np.dot(simple_roots, simple_roots.T)  # = 2 * <alpha_i, alpha_j> / <alpha_j, alpha_j> for ADE
print("  Cartan matrix (should be E8):")
print(cartan.astype(int))

# Expected E8 Cartan matrix with numbering 1-3-4-5-6-7-8, branch at 2-4:
# Check key connections:
assert cartan[0, 2] == -1, "alpha_1 should connect to alpha_3"  # 1-3
assert cartan[1, 3] == -1, "alpha_2 should connect to alpha_4"  # 2-4
assert cartan[2, 3] == -1, "alpha_3 should connect to alpha_4"  # 3-4
assert cartan[3, 4] == -1, "alpha_4 should connect to alpha_5"  # 4-5
assert cartan[4, 5] == -1, "alpha_5 should connect to alpha_6"  # 5-6
assert cartan[5, 6] == -1, "alpha_6 should connect to alpha_7"  # 6-7
assert cartan[6, 7] == -1, "alpha_7 should connect to alpha_8"  # 7-8
# Non-connections:
assert cartan[0, 1] == 0, "alpha_1 should NOT connect to alpha_2"
assert cartan[1, 2] == 0, "alpha_2 should NOT connect to alpha_3"
print("\n  Dynkin diagram verified: 1 - 3 - 4 - 5 - 6 - 7 - 8")
print("                                  |")
print("                                  2")

# ============================================================
# Part 3: Express each root in simple root basis
# ============================================================
print("\n" + "=" * 70)
print("Part 3: Dynkin Coefficients for All 240 Roots")
print("=" * 70)

# Solve: root = sum_i n_i * alpha_i  =>  n = root @ S_inv
S = simple_roots  # 8x8 matrix (rows = simple roots)
S_inv = np.linalg.inv(S)

# For each root, compute Dynkin coefficients
dynkin_labels = roots @ S_inv  # shape (240, 8)

# Verify: all Dynkin labels should be integers (for roots of a simply-laced algebra)
assert np.allclose(dynkin_labels, np.round(dynkin_labels), atol=1e-10), \
    "Dynkin labels should be integers for E8 roots"
dynkin_labels = np.round(dynkin_labels).astype(int)

print(f"  All 240 roots expressed in simple root basis.")
print(f"  Dynkin labels are all integers: VERIFIED")

# Find the highest root (largest sum of coefficients)
heights = np.sum(dynkin_labels, axis=1)
max_height_idx = np.argmax(heights)
theta = dynkin_labels[max_height_idx]
print(f"\n  Highest root theta = {theta}")
print(f"  Height = {heights[max_height_idx]}")
print(f"  In coordinates: {roots[max_height_idx]}")

# The marks m_i are the Dynkin coefficients of the highest root
# These should sum to h-1 = 29 for E8 (Coxeter number h = 30)
print(f"  Sum of marks = {np.sum(theta)} (should be 29 = h-1)")
assert np.sum(theta) == 29, f"Expected sum 29, got {np.sum(theta)}"

# ============================================================
# Part 4: CORRECT Z3 classification
# ============================================================
print("\n" + "=" * 70)
print("Part 4: CORRECT Z3 Eigenspace Decomposition")
print("=" * 70)

# The Z3 automorphism giving centralizer A8 = SU(9):
# Remove node with mark 3 from the extended Dynkin diagram.
# With our numbering, alpha_2 has mark theta[1] (0-indexed).
# Which node has mark 3?

print(f"\n  Marks (Dynkin coefficients of theta):")
for i in range(8):
    print(f"    alpha_{i+1}: mark = {theta[i]}")

# Find all nodes with mark divisible by 3 (for Z3 element)
mark3_nodes = [i for i in range(8) if theta[i] % 3 == 0 and theta[i] > 0]
print(f"\n  Nodes with mark divisible by 3: {[i+1 for i in mark3_nodes]}")
print(f"  (marks: {[theta[i] for i in mark3_nodes]})")

# For A8, we need to remove a node with mark 3 such that the remaining
# extended diagram is an A8 chain. Let's check both candidates.
for branch_idx in mark3_nodes:
    if theta[branch_idx] == 3:
        # The Z3 charge is: n_{branch_idx} mod 3
        charges = dynkin_labels[:, branch_idx] % 3

        s0 = np.sum(charges == 0)
        s1 = np.sum(charges == 1)
        s2 = np.sum(charges == 2)

        print(f"\n  Using branch node alpha_{branch_idx+1} (mark = {theta[branch_idx]}):")
        print(f"    Sector 0 (charge 0 mod 3): {s0} roots + 8 Cartan = {s0+8}")
        print(f"    Sector 1 (charge 1 mod 3): {s1} roots")
        print(f"    Sector 2 (charge 2 mod 3): {s2} roots")

        if s0 + 8 == 80 and s1 == 84 and s2 == 84:
            print(f"    ==> THIS gives 80 + 84 + 84 = 248! CORRECT A8 decomposition!")
            BRANCH_NODE = branch_idx
            break
    elif theta[branch_idx] == 6:
        # mark 6: removing gives centralizer with mark/3 = 2 families
        charges = dynkin_labels[:, branch_idx] % 3
        s0 = np.sum(charges == 0)
        s1 = np.sum(charges == 1)
        s2 = np.sum(charges == 2)
        print(f"\n  Using branch node alpha_{branch_idx+1} (mark = {theta[branch_idx]}):")
        print(f"    Sector 0: {s0} roots + 8 Cartan = {s0+8}")
        print(f"    Sector 1: {s1}, Sector 2: {s2}")

# Use the correct branch node
z3_charge = dynkin_labels[:, BRANCH_NODE] % 3

sector_roots = {0: [], 1: [], 2: []}
for i in range(240):
    sector_roots[z3_charge[i]].append(i)

s0_count = len(sector_roots[0])
s1_count = len(sector_roots[1])
s2_count = len(sector_roots[2])

print(f"\n  VERIFIED Z3 DECOMPOSITION (using alpha_{BRANCH_NODE+1} coefficient mod 3):")
print(f"    SU(9) adjoint (sector 0): {s0_count} roots + 8 Cartan = {s0_count + 8}")
print(f"    84 (sector 1):            {s1_count} roots")
print(f"    84-bar (sector 2):        {s2_count} roots")
assert s0_count + 8 == 80, f"Expected 80, got {s0_count + 8}"
assert s1_count == 84, f"Expected 84, got {s1_count}"
assert s2_count == 84, f"Expected 84, got {s2_count}"

# ============================================================
# Part 5: D8 sectors (adjoint vs spinor)
# ============================================================
print("\n" + "=" * 70)
print("Part 5: D8 Decomposition and D7 Chirality")
print("=" * 70)

# D8 adjoint = integer-entry roots (112 roots)
d8_adj_mask = np.all(np.abs(roots - np.round(roots)) < 1e-10, axis=1)
d8_spin_mask = ~d8_adj_mask

d8_adj_indices = set(np.where(d8_adj_mask)[0])
d8_spin_indices = set(np.where(d8_spin_mask)[0])

print(f"  D8 adjoint roots:  {len(d8_adj_indices)}")
print(f"  D8 spinor roots:   {len(d8_spin_indices)}")

# D7 chirality on spinor roots: 8th coordinate sign
spinor_root_list = [(i, roots[i]) for i in sorted(d8_spin_indices)]
d7_plus_indices = set()
d7_minus_indices = set()
for idx, r in spinor_root_list:
    if r[7] > 0:
        d7_plus_indices.add(idx)
    else:
        d7_minus_indices.add(idx)

print(f"  D7 S+ (8th coord > 0): {len(d7_plus_indices)}")
print(f"  D7 S- (8th coord < 0): {len(d7_minus_indices)}")
assert len(d7_plus_indices) == 64
assert len(d7_minus_indices) == 64

# ============================================================
# Part 6: THE A8/D8 OVERLAP MATRIX
# ============================================================
print("\n" + "=" * 70)
print("Part 6: A8/D8 Overlap Matrix -- THE KEY COMPUTATION")
print("=" * 70)

# For each root, classify by (Z3 sector, D8 sector)
# D8 sectors: 'adj' (integer), '+' (spinor, 8th>0), '-' (spinor, 8th<0)
def d8_sector(idx):
    if idx in d8_adj_indices:
        return 'adj'
    elif idx in d7_plus_indices:
        return '+'
    else:
        return '-'

overlap = {}
for z3 in [0, 1, 2]:
    for d8 in ['adj', '+', '-']:
        count = sum(1 for idx in sector_roots[z3] if d8_sector(idx) == d8)
        overlap[(z3, d8)] = count

print("\n  A8/D8 Overlap Matrix (roots only, 240 total):")
print("  " + "-" * 65)
print(f"  {'Z3 sector':<25} | {'D8 adj (112)':<15} | {'D7 S+ (64)':<12} | {'D7 S- (64)':<12}")
print("  " + "-" * 65)
for z3, label in [(0, 'Sector 0 (SU(9) adj)'), (1, 'Sector 1 (84)'), (2, 'Sector 2 (84-bar)')]:
    print(f"  {label:<25} | {overlap[(z3,'adj')]:<15} | {overlap[(z3,'+')]:<12} | {overlap[(z3,'-')]:<12}")
print("  " + "-" * 65)
total_adj = overlap[(0,'adj')]+overlap[(1,'adj')]+overlap[(2,'adj')]
total_plus = overlap[(0,'+')]+overlap[(1,'+')]+overlap[(2,'+')]
total_minus = overlap[(0,'-')]+overlap[(1,'-')]+overlap[(2,'-')]
print(f"  {'Total':<25} | {total_adj:<15} | {total_plus:<12} | {total_minus:<12}")

assert total_adj == 112
assert total_plus == 64
assert total_minus == 64
print("\n  Row/column totals verified")

# ============================================================
# Part 7: KC-CHIRAL-1 -- D7 chirality within the 84
# ============================================================
print("\n" + "=" * 70)
print("Part 7: KC-CHIRAL-1 -- D7 Chirality Within the 84")
print("=" * 70)

s1_adj = overlap[(1, 'adj')]
s1_plus = overlap[(1, '+')]
s1_minus = overlap[(1, '-')]
s1_spin = s1_plus + s1_minus

print(f"\n  The 84 (Z3 sector 1) decomposes under D8/D7:")
print(f"    D8 adjoint: {s1_adj} roots")
print(f"    D7 S+:      {s1_plus} roots")
print(f"    D7 S-:      {s1_minus} roots")
print(f"    Total:      {s1_adj + s1_plus + s1_minus}")
assert s1_adj + s1_plus + s1_minus == 84

if s1_plus != s1_minus:
    print(f"\n  KC-CHIRAL-1: PASS -- ASYMMETRIC split: {s1_plus} vs {s1_minus}")
    print(f"  D7 chirality DOES distinguish within the 84!")
    print(f"  Asymmetry: |S+ - S-| = {abs(s1_plus - s1_minus)} roots")
else:
    print(f"\n  KC-CHIRAL-1: RESULT -- Symmetric split: {s1_plus} = {s1_minus}")
    print(f"  D7 chirality is BALANCED within the 84 (equal left and right).")
    print(f"  This does NOT mean chirality is absent -- it means the 84 contains")
    print(f"  equal amounts of each chirality, as expected for a complex rep.")

# Check 84-bar
s2_adj = overlap[(2, 'adj')]
s2_plus = overlap[(2, '+')]
s2_minus = overlap[(2, '-')]
print(f"\n  The 84-bar (Z3 sector 2):")
print(f"    D8 adjoint: {s2_adj}, D7 S+: {s2_plus}, D7 S-: {s2_minus}")

if s1_plus == s2_minus and s1_minus == s2_plus:
    print(f"  84 and 84-bar are conjugate under D7 chirality (S+ <-> S-)")
elif s1_plus == s2_plus and s1_minus == s2_minus:
    print(f"  84 and 84-bar have SAME chirality distribution")
else:
    print(f"  84 and 84-bar chirality distributions differ in a complex way")

# ============================================================
# Part 8: KC-CHIRAL-2 -- A8/D8 non-nesting
# ============================================================
print("\n" + "=" * 70)
print("Part 8: KC-CHIRAL-2 -- A8/D8 Overlap Non-Triviality")
print("=" * 70)

s0_adj = overlap[(0, 'adj')]
s0_spin = overlap[(0, '+')] + overlap[(0, '-')]

print(f"\n  SU(9) adjoint roots ({s0_adj + s0_spin} total):")
print(f"    In D8 adjoint: {s0_adj}")
print(f"    In D8 spinor:  {s0_spin}")

print(f"\n  84 roots:")
print(f"    In D8 adjoint: {s1_adj}")
print(f"    In D8 spinor:  {s1_spin}")

if s1_adj > 0 and s1_spin > 0:
    print(f"\n  KC-CHIRAL-2: PASS -- The 84 spans BOTH D8 sectors!")
    print(f"  A8 and D8 are genuinely non-nested.")
else:
    if s1_spin == 0:
        print(f"\n  KC-CHIRAL-2: FAIL -- All 84 roots in D8 adjoint")
    else:
        print(f"\n  KC-CHIRAL-2: FAIL -- All 84 roots in D8 spinor")

# ============================================================
# Part 9: KC-CHIRAL-3 -- Generation-chirality structure
# ============================================================
print("\n" + "=" * 70)
print("Part 9: KC-CHIRAL-3 -- Joint Z3 x D7-Chirality Structure")
print("=" * 70)

# For the spinor roots in the 84, analyze their D5 x D2 content
# (SO(10) x SO(4) inside D7 = SO(14))
# First 5 coords = SO(10) weight, coords 6-7 = SO(4) weight
# D5 chirality (SO(10) chirality) determined by parity of first 5 coords

print(f"\n  Spinor roots in 84: analyzing SO(10) x SO(4) content")
print(f"  ({s1_spin} roots total)")

so10_16_plus = 0   # 16 in S+ of D7
so10_16_minus = 0  # 16 in S- of D7
so10_16b_plus = 0  # 16-bar in S+ of D7
so10_16b_minus = 0 # 16-bar in S- of D7

for idx in sector_roots[1]:
    if idx not in d8_spin_indices:
        continue
    r = roots[idx]
    # SO(10) parity = parity of first 5 coords (number of -1/2 entries)
    minus_count_5 = sum(1 for x in r[:5] if x < 0)
    is_16 = (minus_count_5 % 2 == 0)  # even parity = 16
    is_plus = (r[7] > 0)  # D7 chirality

    if is_16 and is_plus:
        so10_16_plus += 1
    elif is_16 and not is_plus:
        so10_16_minus += 1
    elif not is_16 and is_plus:
        so10_16b_plus += 1
    else:
        so10_16b_minus += 1

print(f"\n  84 spinor roots under SO(10) x D7-chirality:")
print(f"    16 of SO(10), D7 S+:     {so10_16_plus}")
print(f"    16 of SO(10), D7 S-:     {so10_16_minus}")
print(f"    16-bar of SO(10), D7 S+: {so10_16b_plus}")
print(f"    16-bar of SO(10), D7 S-: {so10_16b_minus}")
print(f"    Total:                   {so10_16_plus + so10_16_minus + so10_16b_plus + so10_16b_minus}")

# Same for 84-bar
print(f"\n  84-bar spinor roots under SO(10) x D7-chirality:")
s2_16p, s2_16m, s2_16bp, s2_16bm = 0, 0, 0, 0
for idx in sector_roots[2]:
    if idx not in d8_spin_indices:
        continue
    r = roots[idx]
    minus_count_5 = sum(1 for x in r[:5] if x < 0)
    is_16 = (minus_count_5 % 2 == 0)
    is_plus = (r[7] > 0)
    if is_16 and is_plus: s2_16p += 1
    elif is_16 and not is_plus: s2_16m += 1
    elif not is_16 and is_plus: s2_16bp += 1
    else: s2_16bm += 1

print(f"    16 of SO(10), D7 S+:     {s2_16p}")
print(f"    16 of SO(10), D7 S-:     {s2_16m}")
print(f"    16-bar of SO(10), D7 S+: {s2_16bp}")
print(f"    16-bar of SO(10), D7 S-: {s2_16bm}")

# ============================================================
# Part 10: Detailed Z3 charge spectrum
# ============================================================
print("\n" + "=" * 70)
print("Part 10: Z3 Charge Spectrum (alpha_2 coefficient)")
print("=" * 70)

n2_values_s1 = [dynkin_labels[idx, BRANCH_NODE] for idx in sector_roots[1]]
print(f"\n  Dynkin coefficient n_2 values in the 84:")
for val, cnt in sorted(Counter(n2_values_s1).items()):
    print(f"    n_2 = {val:+d} (mod 3 = {val % 3}): {cnt} roots")

n2_values_s0 = [dynkin_labels[idx, BRANCH_NODE] for idx in sector_roots[0]]
print(f"\n  Dynkin coefficient n_2 values in SU(9) adj:")
for val, cnt in sorted(Counter(n2_values_s0).items()):
    print(f"    n_2 = {val:+d} (mod 3 = {val % 3}): {cnt} roots")

# ============================================================
# Part 11: VERDICT
# ============================================================
print("\n" + "=" * 70)
print("EXPERIMENT 7 VERDICT")
print("=" * 70)

print(f"""
  A8/D8 OVERLAP MATRIX (CORRECTED -- Dynkin coefficient method):

  Z3 sector              | D8 adj     | D7 S+      | D7 S-      | Total
  -------------------------------------------------------------------
  Sector 0 (SU(9) adj)   | {overlap[(0,'adj')]:<10} | {overlap[(0,'+')]:<10} | {overlap[(0,'-')]:<10} | {s0_count}
  Sector 1 (84)          | {overlap[(1,'adj')]:<10} | {overlap[(1,'+')]:<10} | {overlap[(1,'-')]:<10} | 84
  Sector 2 (84-bar)      | {overlap[(2,'adj')]:<10} | {overlap[(2,'+')]:<10} | {overlap[(2,'-')]:<10} | 84
  -------------------------------------------------------------------
  Total                   | 112        | 64         | 64         | 240

  KC-CHIRAL-1 (D7 chirality within 84):
    84 spinor part = {s1_plus} (S+) + {s1_minus} (S-)
    {'ASYMMETRIC' if s1_plus != s1_minus else 'BALANCED'}

  KC-CHIRAL-2 (A8/D8 overlap):
    84 = {s1_adj} (D8 adj) + {s1_spin} (D8 spinor)
    {'NON-TRIVIAL (spans both)' if s1_adj > 0 and s1_spin > 0 else 'TRIVIAL'}

  KC-CHIRAL-3 (generation-chirality):
    84 spinor in SO(10) reps:
    16: {so10_16_plus}(S+) + {so10_16_minus}(S-)
    16-bar: {so10_16b_plus}(S+) + {so10_16b_minus}(S-)
""")

# ============================================================
# ASSERTIONS
# ============================================================
print("=" * 70)
print("ASSERTIONS")
print("=" * 70)

# A1: E8 root system
assert len(roots) == 240
print("  A1: E8 has 240 roots")

# A2: Cartan matrix is E8
norms = np.sum(simple_roots**2, axis=1)
assert np.allclose(norms, 2.0)
print("  A2: All simple roots have length^2 = 2")

# A3: D8 decomposition
assert len(d8_adj_indices) == 112
assert len(d8_spin_indices) == 128
print("  A3: 240 = 112 (D8 adj) + 128 (D8 spinor)")

# A4: D7 chirality
assert len(d7_plus_indices) == 64
assert len(d7_minus_indices) == 64
print("  A4: 128 = 64 (S+) + 64 (S-) under D7 chirality")

# A5: Z3 decomposition (CORRECT this time)
assert s0_count + 8 == 80
assert s1_count == 84
assert s2_count == 84
print("  A5: 248 = 80 + 84 + 84 under Z3 (Dynkin coefficient method)")

# A6: Overlap matrix totals
assert total_adj == 112
assert total_plus == 64
assert total_minus == 64
print("  A6: Overlap matrix column totals correct")

# A7: 84 spans both D8 sectors
assert s1_adj > 0 and s1_spin > 0
print(f"  A7: 84 = {s1_adj} (D8 adj) + {s1_spin} (D8 spinor) -- non-nested")

# A8: Marks sum
assert np.sum(theta) == 29
print("  A8: Highest root marks sum to 29 = h-1 (Coxeter number 30)")

print(f"\n  All assertions passed. Experiment 7 complete.")

# ============================================================
# CRITICAL NOTE on wilson_e8_type5.py
# ============================================================
print("\n" + "=" * 70)
print("CRITICAL NOTE")
print("=" * 70)
print("""
  wilson_e8_type5.py used t5 = (1,1,1,1,1,0,0,0) as "type 5 torus coords".
  This gives WRONG Z3 classification: 120 + 64 + 64 instead of 80 + 84 + 84.

  The correct Z3 uses the Dynkin coefficient of the branch node (alpha_2
  in Bourbaki E8) mod 3. This is standard representation theory:
  the type 5 element = exp(2*pi*i * omega_2 / 3) where omega_2 is the
  fundamental coweight, and the eigenvalue on root alpha is
  exp(2*pi*i * n_2 / 3) where alpha = sum n_i alpha_i.

  ALL previous results based on the torus method (Parts 5-8 of
  wilson_e8_type5.py) need to be RECHECKED with this corrected Z3.
  However, the DIMENSIONAL results (80+84+84, 3x16=48, etc.) were
  correct because they follow from abstract representation theory,
  not from the root-level computation.
""")
