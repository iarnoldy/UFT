#!/usr/bin/env python3
"""
Quick fix: verify the Coxeter orbit structure and height computation
for D_7 roots. The previous script had a potential issue with root
height computation (some heights were negative, max was 9 not 11).
"""
import numpy as np
from collections import defaultdict

# D_7 simple roots in R^7:
# alpha_1 = e_1 - e_2
# alpha_2 = e_2 - e_3
# ...
# alpha_6 = e_6 - e_7
# alpha_7 = e_6 + e_7

alpha = np.zeros((7, 7))
for i in range(6):
    alpha[i, i] = 1
    alpha[i, i+1] = -1
alpha[6, 5] = 1
alpha[6, 6] = 1

# All positive roots of D_7: e_i - e_j (i < j) and e_i + e_j (i < j)
pos_roots = []
for i in range(7):
    for j in range(i+1, 7):
        r = np.zeros(7)
        r[i] = 1; r[j] = -1
        pos_roots.append(r)  # e_i - e_j

        r2 = np.zeros(7)
        r2[i] = 1; r2[j] = 1
        pos_roots.append(r2)  # e_i + e_j

print(f"Positive roots: {len(pos_roots)} (should be 42)")

# Express each positive root in terms of simple roots
# root = c_1 * alpha_1 + ... + c_7 * alpha_7
# Solve: alpha^T * c = root (since alpha rows are the simple roots)
A = alpha  # 7x7 matrix, rows = simple roots
A_inv = np.linalg.inv(A)

print("\nRoot expansions and heights:")
heights = {}
for r in pos_roots:
    c = A_inv @ r
    h = round(np.sum(c))
    r_key = tuple(r)
    heights[r_key] = h
    # Identify the root
    nonzero = [(k, r[k]) for k in range(7) if abs(r[k]) > 0.1]
    i, si = nonzero[0]
    j, sj = nonzero[1]
    sign = "-" if sj < 0 else "+"
    # Only print a few for verification
    if h <= 2 or h >= 10:
        c_str = " + ".join(f"{int(c[k])}*a{k+1}" for k in range(7) if abs(c[k]) > 0.01)
        print(f"  e{i+1}{sign}e{j+1}: height {h:2d}  ({c_str})")

# Check for negative coefficients (these would not be positive roots!)
for r in pos_roots:
    c = A_inv @ r
    if any(c_k < -0.01 for c_k in c):
        nonzero = [(k, r[k]) for k in range(7) if abs(r[k]) > 0.1]
        i, si = nonzero[0]
        j, sj = nonzero[1]
        sign = "-" if sj < 0 else "+"
        print(f"  WARNING: e{i+1}{sign}e{j+1} has NEGATIVE coefficients: {np.round(c, 2)}")
        print(f"    This root may not be positive in the simple root basis!")

# Height distribution
h_dist = defaultdict(int)
for h in heights.values():
    h_dist[h] += 1

print(f"\nHeight distribution:")
for h in sorted(h_dist.keys()):
    print(f"  Height {h:3d}: {h_dist[h]} roots")

max_h = max(heights.values())
min_h = min(heights.values())
print(f"\nMax height: {max_h} (expected: h-1 = 11)")
print(f"Min height: {min_h} (expected: 1)")

# The issue: our simple root basis has alpha_7 = e_6 + e_7
# But the standard positive root system requires that all positive
# roots have non-negative coefficients in the simple root basis.
#
# For D_n, the positive roots in terms of simple roots are:
# e_i - e_j (i < j): these have coefficients alpha_i + alpha_{i+1} + ... + alpha_{j-1}
#   (straightforward chain)
# e_i + e_j (i < j): need to go through alpha_7 = e_6 + e_7
#   e_i + e_j = alpha_i + ... + alpha_{j-1} + 2*alpha_j + ... + 2*alpha_{n-2} + alpha_{n-1} + alpha_n
#   where alpha_{n-1} = e_{n-1} - e_n and alpha_n = e_{n-1} + e_n
#
# Let me verify with a specific case.
# For n=7: alpha_6 = e_6 - e_7, alpha_7 = e_6 + e_7
# e_6 + e_7 = alpha_7 (height 1)
# e_5 + e_7 = (e_5 - e_6) + (e_6 + e_7) = alpha_5 + alpha_7 (height 2)
# e_5 + e_6 = (e_5 - e_7) + 2*e_7 = ... hmm
# Actually: e_5 + e_6 = alpha_5 + alpha_6 + alpha_7 (height 3)
# Check: alpha_5 + alpha_6 + alpha_7 = (e_5-e_6) + (e_6-e_7) + (e_6+e_7)
#       = e_5 - e_6 + e_6 - e_7 + e_6 + e_7 = e_5 + e_6. CORRECT!

print("\nManual verification of some roots:")
test_cases = [
    (np.array([0,0,0,0,0,1,1]), "e_6 + e_7"),  # should be alpha_7, h=1
    (np.array([0,0,0,0,1,0,1]), "e_5 + e_7"),  # should be alpha_5 + alpha_7, h=2
    (np.array([0,0,0,0,1,1,0]), "e_5 + e_6"),  # should be alpha_5 + alpha_6 + alpha_7, h=3
    (np.array([1,0,0,0,0,0,-1]), "e_1 - e_7"),  # should be alpha_1+...+alpha_6, h=6
    (np.array([1,0,0,0,0,0,1]), "e_1 + e_7"),   # should be alpha_1+...+alpha_5+alpha_7, h=6
    (np.array([1,0,0,0,0,1,0]), "e_1 + e_6"),   # h=7
    (np.array([1,1,0,0,0,0,0]), "e_1 + e_2"),   # highest root, h=11
]

for root, name in test_cases:
    c = A_inv @ root
    h = round(np.sum(c))
    c_str = " + ".join(f"{int(round(c[k]))}*a{k+1}" for k in range(7) if abs(c[k]) > 0.01)
    neg = any(c_k < -0.01 for c_k in c)
    flag = " <-- NEGATIVE COEFFS" if neg else ""
    print(f"  {name}: {c_str}  height = {h}{flag}")

# The problem is clear: some roots we enumerated as "positive" (using the
# convention "first nonzero coordinate is positive") are NOT positive in
# the simple root basis. This happens when our positivity convention
# disagrees with the Dynkin basis positivity.
#
# The correct positive roots of D_7 are those with ALL non-negative
# coefficients in the simple root basis.

print(f"\nCorrecting positive root list...")
correct_pos_roots = []
for r in pos_roots:
    c = A_inv @ r
    if all(c_k >= -0.01 for c_k in c):
        correct_pos_roots.append(r)

# Also check the negatives of roots we excluded
for r in pos_roots:
    c = A_inv @ r
    if any(c_k < -0.01 for c_k in c):
        r_neg = -r
        c_neg = A_inv @ r_neg
        if all(c_k >= -0.01 for c_k in c_neg):
            correct_pos_roots.append(r_neg)

print(f"Correct positive roots: {len(correct_pos_roots)} (should be 42)")

# Recompute heights
heights_correct = {}
for r in correct_pos_roots:
    c = A_inv @ r
    h = int(round(np.sum(c)))
    heights_correct[tuple(np.round(r, 4))] = h

h_dist_c = defaultdict(int)
for h in heights_correct.values():
    h_dist_c[h] += 1

print(f"\nCorrected height distribution:")
for h in sorted(h_dist_c.keys()):
    print(f"  Height {h:2d}: {h_dist_c[h]} roots")

max_h_c = max(heights_correct.values())
print(f"\nMax height: {max_h_c} (expected: 11)")

# The highest root of D_7 is e_1 + e_2
# = alpha_1 + 2*alpha_2 + 2*alpha_3 + 2*alpha_4 + 2*alpha_5 + alpha_6 + alpha_7
# height = 1 + 2 + 2 + 2 + 2 + 1 + 1 = 11
print(f"\nHighest root e_1 + e_2:")
hr = np.array([1,1,0,0,0,0,0], dtype=float)
c_hr = A_inv @ hr
print(f"  Coefficients: {np.round(c_hr)}")
print(f"  Height: {int(round(np.sum(c_hr)))}")
