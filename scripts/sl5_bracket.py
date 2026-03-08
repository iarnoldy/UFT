"""
Generate sl(5) Lie bracket in Chevalley basis for Lean 4.
Uses 5x5 matrix representation to compute [X,Y] = XY - YX.

24 generators:
  4 Cartan: h1..h4 (diagonal)
  4 simple roots: e1..e4, f1..f4
  3 two-step: e12,e23,e34, f12,f23,f34
  2 three-step: e123,e234, f123,f234
  1 four-step: e1234, f1234
"""
import numpy as np
import itertools

# Matrix units E_{ij}
def E(i, j):
    m = np.zeros((5, 5))
    m[i, j] = 1.0
    return m

# Chevalley basis as 5x5 matrices
basis = {
    'h1': E(0,0) - E(1,1),
    'h2': E(1,1) - E(2,2),
    'h3': E(2,2) - E(3,3),
    'h4': E(3,3) - E(4,4),
    'e1': E(0,1), 'f1': E(1,0),
    'e2': E(1,2), 'f2': E(2,1),
    'e3': E(2,3), 'f3': E(3,2),
    'e4': E(3,4), 'f4': E(4,3),
    'e12': E(0,2), 'f12': E(2,0),
    'e23': E(1,3), 'f23': E(3,1),
    'e34': E(2,4), 'f34': E(4,2),
    'e123': E(0,3), 'f123': E(3,0),
    'e234': E(1,4), 'f234': E(4,1),
    'e1234': E(0,4), 'f1234': E(4,0),
}

names = ['h1','h2','h3','h4',
         'e1','f1','e2','f2','e3','f3','e4','f4',
         'e12','f12','e23','f23','e34','f34',
         'e123','f123','e234','f234',
         'e1234','f1234']

def bracket(X, Y):
    return X @ Y - Y @ X

def decompose(M):
    """Express matrix M in the Chevalley basis. Returns dict of coefficients.

    For off-diagonal basis elements (matrix units), coefficient = matrix entry.
    For Cartan elements, solve the linear system properly:
      c1*h1 + c2*h2 + c3*h3 + c4*h4 = diag(a1,a2,a3,a4,a5)
      => c1=a1, c2=a1+a2, c3=a1+a2+a3, c4=a1+a2+a3+a4
    """
    coeffs = {}

    # Off-diagonal elements are easy (each is a single matrix unit)
    off_diag_map = {
        'e1': (0,1), 'f1': (1,0),
        'e2': (1,2), 'f2': (2,1),
        'e3': (2,3), 'f3': (3,2),
        'e4': (3,4), 'f4': (4,3),
        'e12': (0,2), 'f12': (2,0),
        'e23': (1,3), 'f23': (3,1),
        'e34': (2,4), 'f34': (4,2),
        'e123': (0,3), 'f123': (3,0),
        'e234': (1,4), 'f234': (4,1),
        'e1234': (0,4), 'f1234': (4,0),
    }
    for name, (i,j) in off_diag_map.items():
        c = M[i,j]
        if abs(c) > 1e-10:
            coeffs[name] = int(round(c))

    # Cartan elements from diagonal
    diag = [M[i,i] for i in range(5)]
    # c1 = a1, c2 = a1+a2, c3 = a1+a2+a3, c4 = a1+a2+a3+a4
    cumsum = [sum(diag[:k+1]) for k in range(4)]
    cartan_names = ['h1', 'h2', 'h3', 'h4']
    for i, name in enumerate(cartan_names):
        c = cumsum[i]
        if abs(c) > 1e-10:
            coeffs[name] = int(round(c))

    return coeffs

# Verify basic structure constants
print("=== VERIFYING KEY BRACKETS ===")
# [e1, f1] should be h1
result = bracket(basis['e1'], basis['f1'])
coeffs = decompose(result)
print(f"[e1, f1] = {coeffs}  (expect h1)")

# [e2, f2] should be h2
result = bracket(basis['e2'], basis['f2'])
coeffs = decompose(result)
print(f"[e2, f2] = {coeffs}  (expect h2)")

# [e3, f3] should be h3
result = bracket(basis['e3'], basis['f3'])
coeffs = decompose(result)
print(f"[e3, f3] = {coeffs}  (expect h3)")

# [e4, f4] should be h4
result = bracket(basis['e4'], basis['f4'])
coeffs = decompose(result)
print(f"[e4, f4] = {coeffs}  (expect h4)")

# [e12, f12] should be h1+h2
result = bracket(basis['e12'], basis['f12'])
coeffs = decompose(result)
print(f"[e12, f12] = {coeffs}  (expect h1+h2)")

# [e1234, f1234] should be h1+h2+h3+h4
result = bracket(basis['e1234'], basis['f1234'])
coeffs = decompose(result)
print(f"[e1234, f1234] = {coeffs}  (expect h1+h2+h3+h4)")

# [h1, e1] should be 2*e1
result = bracket(basis['h1'], basis['e1'])
coeffs = decompose(result)
print(f"[h1, e1] = {coeffs}  (expect 2*e1)")

print("\n=== ALL NONZERO BRACKETS ===")
for i, n1 in enumerate(names):
    for j, n2 in enumerate(names):
        if j <= i:
            continue
        result = bracket(basis[n1], basis[n2])
        coeffs = decompose(result)
        if coeffs:
            terms = " + ".join(f"{c}*{n}" if c != 1 else n for n, c in coeffs.items())
            print(f"[{n1}, {n2}] = {terms}")

# Build the bracket as a function: [A,B]_comp = sum_{i<j} c^comp_{ij} * (A_i*B_j - A_j*B_i)
# where c^comp_{ij} is the comp-coefficient of [basis_i, basis_j]
print("\n=== LEAN BRACKET DEFINITION ===")

# Precompute all structure constants
struct_const = {}  # (n1, n2) -> dict of component: coefficient
for i, n1 in enumerate(names):
    for j, n2 in enumerate(names):
        if j <= i:
            continue
        result = bracket(basis[n1], basis[n2])
        coeffs = decompose(result)
        if coeffs:
            struct_const[(n1, n2)] = coeffs

# For each component, find all contributing pairs
print("def comm (A B : SL5) : SL5 :=")
for k, comp in enumerate(names):
    terms = []
    for (n1, n2), coeffs in struct_const.items():
        if comp in coeffs:
            c = coeffs[comp]
            if c == 1:
                terms.append(f"(A.{n1} * B.{n2} - A.{n2} * B.{n1})")
            elif c == -1:
                terms.append(f"(A.{n2} * B.{n1} - A.{n1} * B.{n2})")
            elif c == 2:
                terms.append(f"2 * (A.{n1} * B.{n2} - A.{n2} * B.{n1})")
            elif c == -2:
                terms.append(f"2 * (A.{n2} * B.{n1} - A.{n1} * B.{n2})")
            else:
                if c > 0:
                    terms.append(f"{c} * (A.{n1} * B.{n2} - A.{n2} * B.{n1})")
                else:
                    terms.append(f"{-c} * (A.{n2} * B.{n1} - A.{n1} * B.{n2})")

    sep = "\n         + "
    prefix = "  { " if k == 0 else "    "
    expr = sep.join(terms) if terms else "0"
    comma = "," if k < len(names) - 1 else " }"
    print(f"{prefix}{comp} :=")
    for ti, t in enumerate(terms):
        if ti == 0:
            print(f"         {t}")
        else:
            print(f"       + {t}")
    if not terms:
        print(f"         0")
    if comma == " }":
        print(f"  {comma}")
    else:
        print(f"    {comma}")

# Verify Jacobi with CORRECT decomposition
print("\n=== JACOBI VERIFICATION (corrected decomposition) ===")

# Build bracket function using structure constants
def lie_bracket_components(A_dict, B_dict):
    """Compute [A,B] where A,B are dicts of component values."""
    result = {n: 0.0 for n in names}
    for (n1, n2), coeffs in struct_const.items():
        for comp, c in coeffs.items():
            # [n1, n2]_comp = c, so [A,B]_comp += c * (A_{n1}*B_{n2} - A_{n2}*B_{n1})
            result[comp] += c * (A_dict.get(n1, 0) * B_dict.get(n2, 0)
                                - A_dict.get(n2, 0) * B_dict.get(n1, 0))
    return result

# Test with random values
np.random.seed(42)
for trial in range(100):
    # Random sl(5) elements
    A_vals = {n: np.random.randn() for n in names}
    B_vals = {n: np.random.randn() for n in names}
    C_vals = {n: np.random.randn() for n in names}

    # Compute Jacobi: [A,[B,C]] + [B,[C,A]] + [C,[A,B]]
    BC = lie_bracket_components(B_vals, C_vals)
    CA = lie_bracket_components(C_vals, A_vals)
    AB = lie_bracket_components(A_vals, B_vals)

    t1 = lie_bracket_components(A_vals, BC)
    t2 = lie_bracket_components(B_vals, CA)
    t3 = lie_bracket_components(C_vals, AB)

    max_err = max(abs(t1[n] + t2[n] + t3[n]) for n in names)
    if max_err > 1e-8:
        print(f"JACOBI FAILED trial {trial}: max error = {max_err}")
        break
else:
    print("Jacobi identity holds for 100 random triples (numerical).")

# Also verify with actual matrices
for _ in range(100):
    A = np.random.randn(5, 5)
    A -= np.trace(A)/5 * np.eye(5)  # traceless
    B = np.random.randn(5, 5)
    B -= np.trace(B)/5 * np.eye(5)
    C = np.random.randn(5, 5)
    C -= np.trace(C)/5 * np.eye(5)

    jac = bracket(A, bracket(B, C)) + bracket(B, bracket(C, A)) + bracket(C, bracket(A, B))
    if np.max(np.abs(jac)) > 1e-10:
        print("MATRIX JACOBI FAILED")
        break
else:
    print("Matrix Jacobi holds for 100 random triples.")

# Verify structure constants are consistent between matrix and component form
print("\n=== CROSS-VALIDATION ===")
for trial in range(100):
    A_vals = {n: np.random.randn() for n in names}
    B_vals = {n: np.random.randn() for n in names}

    # Build matrices
    A_mat = sum(A_vals[n] * basis[n] for n in names)
    B_mat = sum(B_vals[n] * basis[n] for n in names)

    # Matrix bracket
    result_mat = bracket(A_mat, B_mat)
    result_decomp = decompose(result_mat)

    # Component bracket
    result_comp = lie_bracket_components(A_vals, B_vals)

    # Compare
    max_err = 0
    for n in names:
        mat_val = result_decomp.get(n, 0)
        comp_val = result_comp[n]
        max_err = max(max_err, abs(mat_val - comp_val))

    if max_err > 1e-8:
        print(f"CROSS-VALIDATION FAILED trial {trial}: max error = {max_err}")
        # Debug
        for n in names:
            mat_val = result_decomp.get(n, 0)
            comp_val = result_comp[n]
            if abs(mat_val - comp_val) > 1e-8:
                print(f"  {n}: matrix={mat_val}, component={comp_val}")
        break
else:
    print("Cross-validation passed: matrix and component brackets agree for 100 random pairs.")
