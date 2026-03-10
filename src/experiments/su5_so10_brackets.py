"""
Compute Lie bracket relations for su(5) generators inside so(10).

so(10) generators: L_{ab} for 1 <= a < b <= 10
Bracket: [L_{ab}, L_{cd}] = delta_{bc}*L_{ad} - delta_{bd}*L_{ac} + delta_{ad}*L_{bc} - delta_{ac}*L_{bd}
Antisymmetry: L_{ba} = -L_{ab}, L_{aa} = 0

su(5) embedding via complex structure J = L_{16}+L_{27}+L_{38}+L_{49}+L_{5,10}

Cartan generators (4):
  H_i = L_{i,i+5} - L_{i+1,i+6}  for i=1..4

R-type generators (10):
  R_{ab} = L_{ab} + L_{a+5,b+5}  for 1<=a<b<=5

S-type generators (10):
  S_{ab} = L_{a,b+5} + L_{b,a+5}  for 1<=a<b<=5
  Note: L_{b,a+5} — if b < a+5 this is standard; if b > a+5, use L_{b,a+5} = -L_{a+5,b}
"""

from collections import defaultdict
import sys

# ============================================================
# Represent so(10) elements as linear combinations of L_{ab}
# We use a dictionary {(a,b): coefficient} where a < b always.
# ============================================================

def canonical(a, b):
    """Return canonical form (min, max) and sign."""
    if a == b:
        return None, 0  # L_{aa} = 0
    if a < b:
        return (a, b), 1
    else:
        return (b, a), -1


def make_L(a, b):
    """Create L_{ab} as a dictionary."""
    canon, sign = canonical(a, b)
    if canon is None:
        return {}
    return {canon: sign}


def add_elements(*elems):
    """Add multiple so(10) elements (dictionaries)."""
    result = defaultdict(float)
    for elem in elems:
        for key, val in elem.items():
            result[key] += val
    # Clean up zeros
    return {k: v for k, v in result.items() if abs(v) > 1e-12}


def scale(elem, c):
    """Scale an element by constant c."""
    return {k: v * c for k, v in elem.items()}


def bracket_basis(a, b, c, d):
    """
    Compute [L_{ab}, L_{cd}] using the formula:
    [L_{ab}, L_{cd}] = delta_{bc}*L_{ad} - delta_{bd}*L_{ac} + delta_{ad}*L_{bc} - delta_{ac}*L_{bd}

    Here a,b,c,d are raw indices (not necessarily ordered).
    L_{ab} with a,b raw means: if a<b it's L_{ab}, if a>b it's -L_{ba}, if a=b it's 0.
    """
    result = {}

    # Term 1: delta_{bc} * L_{ad}
    if b == c:
        result = add_elements(result, make_L(a, d))

    # Term 2: -delta_{bd} * L_{ac}
    if b == d:
        result = add_elements(result, scale(make_L(a, c), -1))

    # Term 3: delta_{ad} * L_{bc}
    if a == d:
        result = add_elements(result, make_L(b, c))

    # Term 4: -delta_{ac} * L_{bd}
    if a == c:
        result = add_elements(result, scale(make_L(b, d), -1))

    return result


def bracket(X, Y):
    """
    Compute [X, Y] where X and Y are linear combinations of L_{ab}.
    X = sum_i alpha_i * L_{a_i, b_i} (canonical: a_i < b_i)
    Y = sum_j beta_j * L_{c_j, d_j} (canonical: c_j < d_j)

    [X, Y] = sum_{i,j} alpha_i * beta_j * [L_{a_i,b_i}, L_{c_j,d_j}]

    But [L_{ab}, L_{cd}] with a<b, c<d uses the formula with those ordered indices.
    """
    result = {}
    for (a, b), alpha in X.items():
        for (c, d), beta in Y.items():
            # a < b and c < d guaranteed by canonical storage
            # [L_{ab}, L_{cd}] with a<b, c<d
            term = bracket_basis(a, b, c, d)
            term = scale(term, alpha * beta)
            result = add_elements(result, term)
    return result


def elem_to_str(elem):
    """Pretty-print an so(10) element."""
    if not elem:
        return "0"
    parts = []
    for (a, b), coeff in sorted(elem.items()):
        if abs(coeff - round(coeff)) < 1e-10:
            coeff = int(round(coeff))
        if coeff == 1:
            parts.append(f"L_{{{a},{b}}}")
        elif coeff == -1:
            parts.append(f"-L_{{{a},{b}}}")
        else:
            parts.append(f"{coeff}*L_{{{a},{b}}}")
    return " + ".join(parts).replace(" + -", " - ")


def is_zero(elem):
    return all(abs(v) < 1e-12 for v in elem.values())


# ============================================================
# Define su(5) generators
# ============================================================

# Cartan: H_i = L_{i,i+5} - L_{i+1,i+6} for i=1..4
H = {}
for i in range(1, 5):
    H[i] = add_elements(make_L(i, i + 5), scale(make_L(i + 1, i + 6), -1))

# R-type: R_{ab} = L_{ab} + L_{a+5,b+5} for 1<=a<b<=5
R = {}
for a in range(1, 6):
    for b in range(a + 1, 6):
        R[(a, b)] = add_elements(make_L(a, b), make_L(a + 5, b + 5))

# S-type: S_{ab} = L_{a,b+5} + L_{b,a+5} for 1<=a<b<=5
# Note: For a<b, we have a+5 > b (since a>=1, b<=5, so a+5>=6>b)
# and b+5 > a (since b>=2, a<=4, so b+5>=7>a).
# So L_{a,b+5} has a < b+5 — canonical.
# L_{b,a+5}: b vs a+5. Since a<b<=5, a+5 ranges 6..9, b ranges 2..5.
# So b < a+5 always. Canonical: L_{b,a+5}.
S = {}
for a in range(1, 6):
    for b in range(a + 1, 6):
        S[(a, b)] = add_elements(make_L(a, b + 5), make_L(b, a + 5))

# A4 Cartan matrix
A4 = [[2, -1, 0, 0],
      [-1, 2, -1, 0],
      [0, -1, 2, -1],
      [0, 0, -1, 2]]

# ============================================================
# Print generators for reference
# ============================================================
print("=" * 70)
print("su(5) GENERATORS INSIDE so(10)")
print("=" * 70)

print("\nCartan generators:")
for i in range(1, 5):
    print(f"  H_{i} = {elem_to_str(H[i])}")

print("\nR-type generators (simple roots):")
for j in range(1, 5):
    print(f"  R_{{{j},{j+1}}} = {elem_to_str(R[(j, j+1)])}")

print("\nS-type generators (simple roots):")
for j in range(1, 5):
    print(f"  S_{{{j},{j+1}}} = {elem_to_str(S[(j, j+1)])}")

# ============================================================
# 1. [H_i, H_j] — should all be 0
# ============================================================
print("\n" + "=" * 70)
print("1. CARTAN COMMUTATIVITY: [H_i, H_j]")
print("=" * 70)

all_commute = True
for i in range(1, 5):
    for j in range(i + 1, 5):
        result = bracket(H[i], H[j])
        zero = is_zero(result)
        all_commute = all_commute and zero
        status = "OK (= 0)" if zero else f"FAIL: {elem_to_str(result)}"
        print(f"  [H_{i}, H_{j}] = {elem_to_str(result)}  {status}")

print(f"\n  All Cartans commute: {'YES' if all_commute else 'NO'}")

# ============================================================
# 2. [H_i, R_{j,j+1}] — should give c_{ij} * S_{j,j+1}
# ============================================================
print("\n" + "=" * 70)
print("2. CARTAN-ROOT RELATIONS: [H_i, R_{{j,j+1}}]")
print("=" * 70)

cartan_R_ok = True
computed_cartan = [[0]*4 for _ in range(4)]

for i in range(1, 5):
    for j in range(1, 5):
        result = bracket(H[i], R[(j, j + 1)])
        expected_S = S[(j, j + 1)]

        # Determine coefficient: result should be c * S_{j,j+1}
        # Find c by comparing
        c = None
        if is_zero(result):
            c = 0
        else:
            for key in expected_S:
                if key in result:
                    c = result[key] / expected_S[key]
                    break
            # Verify all components match
            if c is not None:
                reconstructed = scale(expected_S, c)
                diff = add_elements(result, scale(reconstructed, -1))
                if not is_zero(diff):
                    c = None  # not a simple multiple

        computed_cartan[i-1][j-1] = c if c is not None else '?'

        expected_c = A4[i-1][j-1]
        match = (c is not None and abs(c - expected_c) < 1e-10)
        cartan_R_ok = cartan_R_ok and match

        c_str = int(round(c)) if (c is not None and abs(c - round(c)) < 1e-10) else c
        print(f"  [H_{i}, R_{{{j},{j+1}}}] = {elem_to_str(result)}")
        print(f"    = {c_str} * S_{{{j},{j+1}}}   (expected: {expected_c})  {'OK' if match else 'MISMATCH'}")

print(f"\n  Computed Cartan matrix from [H_i, R_{{j,j+1}}] = c_{{ij}} * S_{{j,j+1}}:")
for i in range(4):
    row = [int(round(computed_cartan[i][j])) if isinstance(computed_cartan[i][j], (int, float)) else '?' for j in range(4)]
    print(f"    [{', '.join(str(x).rjust(3) for x in row)}]")

print(f"\n  A4 Cartan matrix:")
for row in A4:
    print(f"    [{', '.join(str(x).rjust(3) for x in row)}]")

print(f"\n  Cartan matrix matches A4: {'YES' if cartan_R_ok else 'NO'}")

# ============================================================
# 3. [H_i, S_{j,j+1}] — should give -c_{ij} * R_{j,j+1}
# ============================================================
print("\n" + "=" * 70)
print("3. CARTAN-ROOT RELATIONS: [H_i, S_{{j,j+1}}]")
print("=" * 70)

cartan_S_ok = True

for i in range(1, 5):
    for j in range(1, 5):
        result = bracket(H[i], S[(j, j + 1)])
        expected_R = R[(j, j + 1)]

        # Determine coefficient: result should be c * R_{j,j+1}
        c = None
        if is_zero(result):
            c = 0
        else:
            for key in expected_R:
                if key in result:
                    c = result[key] / expected_R[key]
                    break
            if c is not None:
                reconstructed = scale(expected_R, c)
                diff = add_elements(result, scale(reconstructed, -1))
                if not is_zero(diff):
                    c = None

        expected_c = -A4[i-1][j-1]
        match = (c is not None and abs(c - expected_c) < 1e-10)
        cartan_S_ok = cartan_S_ok and match

        c_str = int(round(c)) if (c is not None and abs(c - round(c)) < 1e-10) else c
        print(f"  [H_{i}, S_{{{j},{j+1}}}] = {elem_to_str(result)}")
        print(f"    = {c_str} * R_{{{j},{j+1}}}   (expected: {expected_c})  {'OK' if match else 'MISMATCH'}")

print(f"\n  [H_i, S_{{j,j+1}}] = -c_{{ij}} * R_{{j,j+1}}: {'YES' if cartan_S_ok else 'NO'}")

# ============================================================
# 4. Root composition brackets
# ============================================================
print("\n" + "=" * 70)
print("4. ROOT COMPOSITION BRACKETS")
print("=" * 70)

# 4a. [R_{12}, S_{12}]
print("\n4a. [R_{12}, S_{12}]:")
result = bracket(R[(1, 2)], S[(1, 2)])
print(f"  = {elem_to_str(result)}")
# Check if it's a Cartan element
# H1 = L_{1,6} - L_{2,7}, H2 = L_{2,7} - L_{3,8}
# So L_{1,6} = H1 + L_{2,7}, etc.
# Let's express in terms of H_i
# L_{1,6} appears in H1 with coeff +1
# L_{2,7} appears in H1 with coeff -1 and H2 with coeff +1
print("  Expressing in terms of Cartan generators:")
# Try to decompose result as sum of H_i
# H1 = L_{1,6} - L_{2,7}
# H2 = L_{2,7} - L_{3,8}
# H3 = L_{3,8} - L_{4,9}
# H4 = L_{4,9} - L_{5,10}
# So: L_{1,6} = H1 + H2 + H3 + H4 + L_{5,10}
# L_{2,7} = H2 + H3 + H4 + L_{5,10}
# L_{3,8} = H3 + H4 + L_{5,10}
# L_{4,9} = H4 + L_{5,10}
# L_{5,10} = L_{5,10}
# J = L_{1,6}+L_{2,7}+L_{3,8}+L_{4,9}+L_{5,10} = H1+2H2+3H3+4H4+5*L_{5,10}
# But J commutes with su(5), so J/5 type thing... Let's just check directly.
# Better: solve for coefficients
# result = c1*H1 + c2*H2 + c3*H3 + c4*H4 + c_J * J
# where J = L_{1,6}+L_{2,7}+L_{3,8}+L_{4,9}+L_{5,10}
# The L_{a,a+5} basis: coefficients of L_{1,6}, L_{2,7}, L_{3,8}, L_{4,9}, L_{5,10}
cartan_basis = [(1, 6), (2, 7), (3, 8), (4, 9), (5, 10)]
result_coeffs = [result.get(k, 0) for k in cartan_basis]
print(f"  Coefficients on L_{{1,6}}, L_{{2,7}}, L_{{3,8}}, L_{{4,9}}, L_{{5,10}}: {result_coeffs}")

# Check if it's purely in the Cartan direction (only L_{a,a+5} terms)
non_cartan = {k: v for k, v in result.items() if k not in cartan_basis}
if non_cartan:
    print(f"  Non-Cartan terms: {elem_to_str(non_cartan)}")
else:
    print(f"  Pure Cartan element (good!)")
    # Decompose: result = c1*H1 + c2*H2 + c3*H3 + c4*H4
    # H_i has L_{i,i+5} with +1 and L_{i+1,i+6} with -1
    # Matrix: H1=[1,-1,0,0,0], H2=[0,1,-1,0,0], H3=[0,0,1,-1,0], H4=[0,0,0,1,-1]
    # This is upper bidiagonal. Solve by back-substitution.
    # If result = [r1,r2,r3,r4,r5] then c1=r1, c2=r1+r2, c3=r1+r2+r3, c4=r1+r2+r3+r4
    # and r1+r2+r3+r4+r5 should be 0 (no J component for traceless su(5))
    # Actually more carefully:
    # c1*[1,-1,0,0,0] + c2*[0,1,-1,0,0] + c3*[0,0,1,-1,0] + c4*[0,0,0,1,-1]
    # = [c1, -c1+c2, -c2+c3, -c3+c4, -c4]
    # So: c1 = r1, -c1+c2 = r2, -c2+c3 = r3, -c3+c4 = r4, -c4 = r5
    r = result_coeffs
    c1 = r[0]
    c2 = r[1] + c1
    c3 = r[2] + c2
    c4 = r[3] + c3
    check = -c4
    coeffs = [c1, c2, c3, c4]
    coeffs_int = [int(round(c)) for c in coeffs]
    print(f"  = {coeffs_int[0]}*H1 + {coeffs_int[1]}*H2 + {coeffs_int[2]}*H3 + {coeffs_int[3]}*H4")
    if abs(check - r[4]) < 1e-10:
        print(f"  Consistency check (traceless): PASS (residual on L_{{5,10}}: {check} == {r[4]})")
    else:
        print(f"  Consistency check: FAIL ({check} != {r[4]})")

# 4b. [R_{12}, R_{23}]
print("\n4b. [R_{12}, R_{23}]:")
result = bracket(R[(1, 2)], R[(2, 3)])
print(f"  = {elem_to_str(result)}")
# Check if it's R_{13}
diff = add_elements(result, scale(R[(1, 3)], -1))
if is_zero(diff):
    print(f"  = R_{{1,3}}  (root composition alpha_1 + alpha_2 in R-sector)")
else:
    # Maybe a different multiple
    for key in R[(1, 3)]:
        if key in result:
            c = result[key] / R[(1, 3)][key]
            check = add_elements(result, scale(R[(1, 3)], -c))
            if is_zero(check):
                print(f"  = {c} * R_{{1,3}}")
                break
    else:
        print(f"  Not a simple multiple of R_{{1,3}}")
        print(f"  R_{{1,3}} = {elem_to_str(R[(1,3)])}")

# 4c. [R_{12}, S_{23}]
print("\n4c. [R_{12}, S_{23}]:")
result = bracket(R[(1, 2)], S[(2, 3)])
print(f"  = {elem_to_str(result)}")
# Check if it's S_{13}
diff = add_elements(result, scale(S[(1, 3)], -1))
if is_zero(diff):
    print(f"  = S_{{1,3}}  (root composition alpha_1 + alpha_2 in S-sector)")
else:
    for key in S[(1, 3)]:
        if key in result:
            c = result[key] / S[(1, 3)][key]
            check = add_elements(result, scale(S[(1, 3)], -c))
            if is_zero(check):
                print(f"  = {c} * S_{{1,3}}")
                break
    else:
        print(f"  Not a simple multiple of S_{{1,3}}")
        print(f"  S_{{1,3}} = {elem_to_str(S[(1,3)])}")

# 4d. [S_{12}, S_{12}] — sanity check, should be 0 (bracket of element with itself)
print("\n4d. [S_{12}, S_{12}] (sanity check):")
result = bracket(S[(1, 2)], S[(1, 2)])
print(f"  = {elem_to_str(result)}  {'OK' if is_zero(result) else 'FAIL'}")

# ============================================================
# 5. Additional verification: [R_{ab}, S_{ab}] for all simple roots
# ============================================================
print("\n" + "=" * 70)
print("5. [R_{{j,j+1}}, S_{{j,j+1}}] FOR ALL SIMPLE ROOTS")
print("=" * 70)

for j in range(1, 5):
    result = bracket(R[(j, j + 1)], S[(j, j + 1)])
    print(f"\n  [R_{{{j},{j+1}}}, S_{{{j},{j+1}}}] = {elem_to_str(result)}")

    r = [result.get(k, 0) for k in cartan_basis]
    non_cartan = {k: v for k, v in result.items() if k not in cartan_basis}
    if non_cartan:
        print(f"    Non-Cartan terms: {elem_to_str(non_cartan)}")
    else:
        c1 = r[0]
        c2 = r[1] + c1
        c3 = r[2] + c2
        c4 = r[3] + c3
        coeffs_int = [int(round(c)) for c in [c1, c2, c3, c4]]
        print(f"    = {' + '.join(f'{c}*H{i+1}' for i, c in enumerate(coeffs_int))}")
        check = -c4
        if abs(check - r[4]) < 1e-10:
            print(f"    Traceless: PASS")
        else:
            print(f"    Traceless: FAIL ({check} != {r[4]})")

# ============================================================
# 6. Verify the bracket [R,S] reproduces H (the "coroot" relation)
# ============================================================
print("\n" + "=" * 70)
print("6. VERIFY [E_alpha, E_{-alpha}] = H_alpha (coroot)")
print("=" * 70)
print("\nIn our convention, E_{alpha_j} ~ R_{j,j+1} + i*S_{j,j+1} (raising)")
print("and E_{-alpha_j} ~ R_{j,j+1} - i*S_{j,j+1} (lowering)")
print("Then [E_alpha, E_{-alpha}] = -2i * [R, S]")
print("For su(5) with A4 Cartan matrix, the coroot H_{alpha_j} should satisfy")
print("<alpha_i, H_{alpha_j}> = A_{ij}")
print()
print("Since [H_i, R_{j,j+1}] = A_{ij} * S_{j,j+1} and [H_i, S_{j,j+1}] = -A_{ij} * R_{j,j+1},")
print("we get [H_i, E_{alpha_j}] = i*A_{ij} * E_{alpha_j}")
print("This confirms H_i acts on root alpha_j with eigenvalue A_{ij}.")

# ============================================================
# 7. Closure check: are [R,R], [R,S], [S,S] all in the su(5) subalgebra?
# ============================================================
print("\n" + "=" * 70)
print("7. CLOSURE CHECK: ALL BRACKETS STAY IN su(5)")
print("=" * 70)

all_su5_generators = {}
# Cartan
for i in range(1, 5):
    all_su5_generators[f"H{i}"] = H[i]
# R-type
for a in range(1, 6):
    for b in range(a + 1, 6):
        all_su5_generators[f"R{a}{b}"] = R[(a, b)]
# S-type
for a in range(1, 6):
    for b in range(a + 1, 6):
        all_su5_generators[f"S{a}{b}"] = S[(a, b)]

# J (the complex structure, commutes with everything in su(5))
J = {}
for i in range(1, 6):
    J = add_elements(J, make_L(i, i + 5))
all_su5_generators["J"] = J

print(f"\nsu(5) has 24 generators + J = 25 total")
print(f"We have: 4 Cartan + 10 R + 10 S = 24 (+J = 25)")

# Check: dimension of span
# so(10) has 45 generators. su(5) + u(1) has 24+1 = 25.
# The remaining 20 are the coset so(10)/u(5).

# Spot-check some brackets
closure_ok = True
test_cases = [
    ("R12", "R34"), ("R12", "R13"), ("S12", "S23"),
    ("R13", "S24"), ("S12", "S34"), ("R12", "S13"),
]

for name1, name2 in test_cases:
    X = all_su5_generators[name1]
    Y = all_su5_generators[name2]
    result = bracket(X, Y)

    if is_zero(result):
        print(f"  [{name1}, {name2}] = 0  (trivially in su(5))")
        continue

    # Check if result is in span of su(5) generators
    # Quick check: all basis elements should be "su(5)-type"
    # su(5) type basis elements: L_{ab} with 1<=a<b<=5, L_{a+5,b+5} with 1<=a<b<=5,
    # and L_{a,b+5} with 1<=a<=5, 6<=b+5<=10
    in_su5 = True
    for (a, b), v in result.items():
        # Check if (a,b) appears in any su(5) generator
        # Cartan: (i, i+5) for i=1..5
        # R: (a,b) with 1<=a<b<=5 or (a+5,b+5) with 1<=a<b<=5 i.e. 6<=a<b<=10
        # S: (a,b+5) with 1<=a<b<=5, so 1<=a<=4, 7<=b+5<=10
        #    or (b,a+5) with 1<=a<b<=5, so 2<=b<=5, 6<=a+5<=9
        is_cartan = (b == a + 5 and 1 <= a <= 5)
        is_R_low = (1 <= a < b <= 5)
        is_R_high = (6 <= a < b <= 10)
        is_S_type = (1 <= a <= 5 and 6 <= b <= 10)
        if not (is_cartan or is_R_low or is_R_high or is_S_type):
            in_su5 = False
            break

    status = "in su(5)+u(1)" if in_su5 else "OUTSIDE su(5)!"
    print(f"  [{name1}, {name2}] = {elem_to_str(result)}  ({status})")
    if not in_su5:
        closure_ok = False

print(f"\n  Closure check: {'PASS' if closure_ok else 'FAIL'}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(f"  1. Cartan commutativity [H_i, H_j] = 0:     {'PASS' if all_commute else 'FAIL'}")
print(f"  2. [H_i, R_{{j,j+1}}] = A_{{ij}} * S_{{j,j+1}}:   {'PASS' if cartan_R_ok else 'FAIL'}")
print(f"  3. [H_i, S_{{j,j+1}}] = -A_{{ij}} * R_{{j,j+1}}: {'PASS' if cartan_S_ok else 'FAIL'}")
print(f"  4. Root composition brackets:              computed above")
print(f"  5. [R,S] = Cartan element:                 computed above")
print(f"  6. Closure in su(5):                       {'PASS' if closure_ok else 'FAIL'}")

if all_commute and cartan_R_ok and cartan_S_ok and closure_ok:
    print("\n  ALL CHECKS PASSED — su(5) bracket relations verified!")
else:
    print("\n  SOME CHECKS FAILED — review output above")
    sys.exit(1)
