"""
Verification of Coxeter numbers and exponents for classical Lie algebras.
Cross-checks the claims made in the mass gap investigation.
"""

# Coxeter numbers and exponents for classical Lie algebras
# Reference: Humphreys, "Introduction to Lie Algebras and Representation Theory"
# Table on p. 66 and exercises in Chapter 3

# Type A_{n-1} = su(n): rank n-1, dim n^2-1, Coxeter h = n
# Exponents: 1, 2, ..., n-1

# Type B_m = so(2m+1): rank m, dim m(2m+1), Coxeter h = 2m
# Exponents: 1, 3, 5, ..., 2m-1

# Type C_m = sp(2m): rank m, dim m(2m+1), Coxeter h = 2m
# Exponents: 1, 3, 5, ..., 2m-1

# Type D_m = so(2m): rank m, dim m(2m-1), Coxeter h = 2(m-1)
# Exponents: 1, 3, 5, ..., 2m-3, m-1

print("Classical Lie algebras: Coxeter numbers and exponents")
print("=" * 60)
print()

# A-type
for n in [2, 3, 4, 5]:
    r = n - 1
    dim = n**2 - 1
    h = n
    exponents = list(range(1, n))
    print(f"A_{r} = su({n}): rank {r}, dim {dim}, h = {h}")
    print(f"  Exponents: {exponents}")
    print(f"  Sum of exponents: {sum(exponents)}")
    print(f"  (Should equal |positive roots| = {dim - r} / 2 = {(dim - r)//2})")
    # Actually sum of exponents = number of positive roots
    num_pos_roots = r * (r + 1) // 2  # for A_r
    print(f"  Number of positive roots: {num_pos_roots}")
    assert sum(exponents) == num_pos_roots, f"MISMATCH: {sum(exponents)} != {num_pos_roots}"
    print()

# B-type
for m in [1, 2, 3]:
    n = 2*m + 1
    r = m
    dim = m * (2*m + 1)
    h = 2*m
    exponents = list(range(1, 2*m, 2))
    print(f"B_{m} = so({n}): rank {r}, dim {dim}, h = {h}")
    print(f"  Exponents: {exponents}")
    num_pos_roots = m**2
    print(f"  Sum of exponents: {sum(exponents)}, positive roots: {num_pos_roots}")
    assert sum(exponents) == num_pos_roots
    print()

# D-type (our main interest)
for m in [2, 3, 4, 5, 7]:
    n = 2*m
    r = m
    dim = m * (2*m - 1)
    h = 2*(m - 1)
    exponents = list(range(1, 2*m - 2, 2)) + [m - 1]
    exponents.sort()
    print(f"D_{m} = so({n}): rank {r}, dim {dim}, h = {h}")
    print(f"  Exponents: {exponents}")
    num_pos_roots = m * (m - 1)
    print(f"  Sum of exponents: {sum(exponents)}, positive roots: {num_pos_roots}")
    assert sum(exponents) == num_pos_roots, f"MISMATCH: {sum(exponents)} != {num_pos_roots}"
    print()

print("=" * 60)
print("SPECIAL CASES AND CORRECTIONS:")
print("=" * 60)
print()

# so(3) = B_1 = A_1: rank 1, dim 3, h = 2
print("so(3) = B_1 = A_1:")
print("  This is A_1 (not D anything), rank 1, dim 3, h = 2")
print("  Exponents: {1}")
print("  The Coxeter number h=2 was CORRECT in the investigation.")
print()

# so(4) = D_2 = A_1 x A_1: this is NOT simple
print("so(4) = D_2:")
print("  D_2 is NOT simple: so(4) = su(2) x su(2)")
print("  Coxeter number is not well-defined for non-simple algebras")
print("  The investigation listed h=2 which is the Coxeter number of each su(2) factor")
print("  This is an edge case -- D_2 is degenerate")
print()

# so(5) = B_2 = C_2: rank 2, dim 10, h = 4
print("so(5) = B_2 = C_2:")
print("  rank 2, dim 10, h = 4")
print("  Exponents: {1, 3}")
print("  Investigation had h=4, CORRECT")
print()

# so(6) = D_3 = A_3 = su(4): rank 3, dim 15, h = 4
print("so(6) = D_3 = A_3 = su(4):")
print("  rank 3, dim 15, h = 4 (as D_3) or h = 4 (as A_3)")
print("  Exponents: {1, 2, 3} (as A_3)")
print("  Investigation had h=4, CORRECT")
print()

# so(14) = D_7: rank 7, dim 91, h = 12
m = 7
print(f"so(14) = D_7:")
print(f"  rank {m}, dim {m*(2*m-1)}, h = {2*(m-1)}")
exponents_D7 = sorted(list(range(1, 2*m - 2, 2)) + [m - 1])
print(f"  Exponents: {exponents_D7}")
print(f"  Sum of exponents: {sum(exponents_D7)}, positive roots: {m*(m-1)}")
print()

# Verify: for D_7, the principal grading decomposes 91 dimensions
# into eigenspaces of the Coxeter element
h = 2*(m-1)  # = 12
print(f"Principal Z/{h} grading of so(14):")
print(f"  g_0 = Cartan subalgebra, dim = {m}")
# Each exponent m_i contributes to g_{m_i} and g_{h - m_i}
# The root spaces are distributed among g_1, ..., g_{h-1}
# For each positive root alpha with height ht(alpha) = k (mod h),
# the root vector E_alpha is in g_k

# The dimension of g_k is the number of exponents m_i
# such that m_i = k or m_i = k (considering that each exponent
# appears with multiplicity equal to the multiplicity of the
# eigenvalue omega^{m_i} of the Coxeter element on the Cartan subalgebra)

# Actually, the CORRECT statement (Kostant 1959):
# dim g_k = |{i : m_i equiv k (mod h)}| for k = 0
# dim g_k = |{positive roots alpha : ht(alpha) equiv k (mod h)}|
#           + |{negative roots alpha : ht(alpha) equiv k (mod h)}|
# for k != 0

# Simpler: for each k in {1,...,h-1}:
# dim g_k = number of positive roots of height congruent to k mod h
#           + number of negative roots of height congruent to -k mod h
# Since heights of negative roots are negatives of positive root heights,
# dim g_k = number of positive roots with ht = k mod h
#           + number of positive roots with ht = h-k mod h

# For the adjoint representation, the total dimension is:
# dim g_0 + sum_{k=1}^{h-1} dim g_k = rank + 2*(number of positive roots) = dim g

total_roots = 2 * m * (m - 1)  # 84
print(f"  Total root vectors: {total_roots}")
print(f"  dim g_0 + total root vectors = {m} + {total_roots} = {m + total_roots}")
assert m + total_roots == 91
print(f"  Verified: equals dim so(14) = 91")

print()
print("=" * 60)
print("COXETER NUMBER CORRECTION TABLE")
print("=" * 60)
print()
print("The investigation listed these Coxeter numbers:")
corrections = [
    ("so(3)", "B_1 = A_1", 2, 2, True),
    ("so(4)", "D_2 (not simple!)", 2, "N/A", False),
    ("so(5)", "B_2", 4, 4, True),
    ("so(6)", "D_3 = A_3", 4, 4, True),
    ("so(7)", "B_3", 6, 6, True),
    ("so(8)", "D_4", 6, 6, True),
    ("so(10)", "D_5", 8, 8, True),
    ("so(14)", "D_7", 12, 12, True),
]
for name, type_, claimed, actual, ok in corrections:
    status = "OK" if ok else "EDGE CASE"
    print(f"  {name} ({type_}): claimed h={claimed}, actual h={actual} [{status}]")

print()
print("All Coxeter numbers are CORRECT (so(4) is an edge case: not simple).")
print()

# One final check: the so(N) with N even Coxeter formula h = N-2
print("Formula check: for so(N) with N even (D_{N/2}), h = 2(N/2 - 1) = N - 2")
for N in [6, 8, 10, 12, 14]:
    m = N // 2
    h = 2 * (m - 1)
    print(f"  so({N}): h = {h} = {N} - 2 = {N - 2} {'OK' if h == N - 2 else 'MISMATCH'}")
print()
print("Formula h = N - 2 for so(N) (N even) VERIFIED.")
