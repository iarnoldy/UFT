#!/usr/bin/env python3
"""
Compute all 45 representation matrices for the 16-dim spinor rep of so(10).

Uses the fermionic Fock space construction:
  - 5 pairs of creation/annihilation operators a_k^+, a_k (k=1..5)
  - Fock states |n_1,...,n_5> with n_k in {0,1}
  - Positive chirality = odd total occupation sum(n_k)
  - Gamma matrices: gamma_{2k-1} = a_k + a_k^+,  gamma_{2k} = i(a_k - a_k^+)
  - so(10) generators: M_{ij} = (1/4)[gamma_i, gamma_j]

The representation matrices are computed in the occupation number basis
and then reordered to match the weight table in spinor_rep.lean.

Output: Lean 4 code for all 45 basis matrices and the rho map.
"""

import numpy as np
from fractions import Fraction

# Weight table matching spinor_rep.lean (signs s_k, weight = s_k/2)
weight_table = [
    ( 1, 1, 1, 1, 1),   # 0
    (-1,-1, 1, 1, 1),   # 1
    (-1, 1,-1, 1, 1),   # 2
    (-1, 1, 1,-1, 1),   # 3
    (-1, 1, 1, 1,-1),   # 4
    ( 1,-1,-1, 1, 1),   # 5
    ( 1,-1, 1,-1, 1),   # 6
    ( 1,-1, 1, 1,-1),   # 7
    ( 1, 1,-1,-1, 1),   # 8
    ( 1, 1,-1, 1,-1),   # 9
    ( 1, 1, 1,-1,-1),   # 10
    (-1,-1,-1,-1, 1),   # 11
    (-1,-1,-1, 1,-1),   # 12
    (-1,-1, 1,-1,-1),   # 13
    (-1, 1,-1,-1,-1),   # 14
    ( 1,-1,-1,-1,-1),   # 15
]

# Convert signs to occupation numbers: s_k = +1 means n_k = 1, s_k = -1 means n_k = 0
occ_table = [tuple((s + 1) // 2 for s in w) for w in weight_table]

# Build the Fock space (32-dimensional, all occupation patterns)
# State index: n_1 * 16 + n_2 * 8 + n_3 * 4 + n_4 * 2 + n_5
def state_idx(n1, n2, n3, n4, n5):
    return n1 * 16 + n2 * 8 + n3 * 4 + n4 * 2 + n5

# Map from occupation tuple to weight-table index (for positive chirality states)
occ_to_widx = {occ: idx for idx, occ in enumerate(occ_table)}

# Full Fock space indices for positive chirality states (odd occupation sum)
pos_chiral_fock = []
for occ in occ_table:
    pos_chiral_fock.append(state_idx(*occ))

# Build creation operators a_k^+ (k=0..4, 0-indexed) as 32x32 matrices
def build_creation(k):
    """a_k^+ on the 32-dim Fock space. k is 0-indexed."""
    mat = np.zeros((32, 32))
    for state in range(32):
        bits = [(state >> (4 - j)) & 1 for j in range(5)]
        if bits[k] == 0:
            new_bits = list(bits)
            new_bits[k] = 1
            new_state = sum(b << (4 - j) for j, b in enumerate(new_bits))
            sign = (-1) ** sum(bits[:k])  # Jordan-Wigner sign
            mat[new_state, state] = sign
    return mat

a_dag = [build_creation(k) for k in range(5)]
a_ann = [ad.T.copy() for ad in a_dag]  # a_k = (a_k^+)^T

# Build gamma matrices (complex, 32x32)
# gamma_{2k-1} = a_k + a_k^+  (real)
# gamma_{2k}   = i(a_k - a_k^+)  (imaginary)
gammas = []
for k in range(5):
    gammas.append(a_dag[k] + a_ann[k])       # gamma_{2k+1}, real
    gammas.append(1j * (a_ann[k] - a_dag[k]))  # gamma_{2k+2}, imaginary

# Verify Clifford relations
print("Verifying Clifford algebra {gamma_i, gamma_j} = 2 delta_{ij}...")
for i in range(10):
    for j in range(10):
        anticomm = gammas[i] @ gammas[j] + gammas[j] @ gammas[i]
        expected = 2 * (1 if i == j else 0) * np.eye(32)
        assert np.max(np.abs(anticomm - expected)) < 1e-12
print("  PASSED")

# Compute so(10) generators: M_{ij} = (1/4)[gamma_i, gamma_j] for i < j
# Restrict to positive chirality subspace (16-dim)
pairs = [(i, j) for i in range(1, 11) for j in range(i+1, 11)]
assert len(pairs) == 45

# Projection onto positive chirality: extract rows/cols corresponding to pos_chiral_fock
P = np.array(pos_chiral_fock)  # 16 Fock-space indices

M_full = {}  # 32x32 generators
M_16 = {}    # 16x16 restricted generators

for (i, j) in pairs:
    comm_ij = gammas[i-1] @ gammas[j-1] - gammas[j-1] @ gammas[i-1]
    gen = comm_ij / 4.0
    M_full[(i, j)] = gen
    # Restrict to positive chirality
    restricted = gen[np.ix_(P, P)]
    M_16[(i, j)] = restricted

# Check Cartan generators
print("\nCartan generator verification:")
for k in range(5):
    idx = (2*k+1, 2*k+2)
    mat = M_16[idx]
    is_diag = np.max(np.abs(mat - np.diag(np.diag(mat)))) < 1e-12
    diag_vals = np.diag(mat)
    expected = [w[k] / 2.0 for w in weight_table]
    # Check if diagonal matches (may need phase adjustment)
    err = np.max(np.abs(diag_vals - expected))
    print(f"  H_{k+1} = M{idx}: diagonal={is_diag}, diag_error={err:.2e}")
    if not is_diag or err > 1e-10:
        print(f"    diag_vals = {[f'{v:.4f}' for v in diag_vals.real]}")
        print(f"    expected  = {[f'{v:.4f}' for v in expected]}")

# The issue is that the Fock space ordering may not match our weight table ordering.
# Let me check what weight each Fock state has.
print("\nFock state weights:")
cartan_mats = [M_full[(2*k+1, 2*k+2)] for k in range(5)]
for fock_idx_pos, fock_idx in enumerate(pos_chiral_fock):
    weights = [cartan_mats[k][fock_idx, fock_idx].real for k in range(5)]
    signs = tuple(1 if w > 0 else -1 for w in weights)
    occ = tuple((fock_idx >> (4 - j)) & 1 for j in range(5))
    matching_w = "?"
    for w_idx, w in enumerate(weight_table):
        if w == signs:
            matching_w = str(w_idx)
    print(f"  pos_idx={fock_idx_pos:2d}, fock={fock_idx:2d}, occ={occ}, weights={[f'{w:+.1f}' for w in weights]}, wt_idx={matching_w}")

# Now let's reorder: find which pos_chiral_fock index maps to which weight_table index
fock_to_weight = {}
for fock_pos_idx in range(16):
    fock_idx = pos_chiral_fock[fock_pos_idx]
    weights = [cartan_mats[k][fock_idx, fock_idx].real for k in range(5)]
    signs = tuple(1 if w > 0 else -1 for w in weights)
    for w_idx, w in enumerate(weight_table):
        if w == signs:
            fock_to_weight[fock_pos_idx] = w_idx
            break

print(f"\nFock->Weight mapping: {fock_to_weight}")

# Build permutation matrix
perm = np.zeros((16, 16))
for old, new in fock_to_weight.items():
    perm[new, old] = 1

# Apply permutation
for key in M_16:
    M_16[key] = perm @ M_16[key] @ perm.T

# Re-verify Cartan generators
print("\nAfter reordering:")
for k in range(5):
    idx = (2*k+1, 2*k+2)
    mat = M_16[idx]
    expected = [w[k] / 2.0 for w in weight_table]
    err = np.max(np.abs(np.diag(mat) - expected))
    print(f"  H_{k+1}: max error = {err:.2e}")

# Now handle the complex phases.
# The Cartan generators are real and diagonal. Good.
# The off-Cartan generators may have complex entries.
# For so(10,0), the 16-dim semispinor is a real representation.
# We need to find phases for each basis vector to make all matrices real.

print("\nMax imaginary parts per generator:")
max_imag_all = 0
for key, mat in M_16.items():
    mi = np.max(np.abs(mat.imag))
    max_imag_all = max(max_imag_all, mi)
print(f"  Overall max imaginary: {max_imag_all:.2e}")

if max_imag_all > 1e-10:
    print("  Matrices are complex, need phase fixing...")

    # Strategy: find phases theta_0,...,theta_15 such that
    # e^{i*theta_m} * M_{m,n} * e^{-i*theta_n} is real for all m,n and all generators.
    # Fix theta_0 = 0 and propagate.

    phases = np.zeros(16)
    fixed = [False] * 16
    fixed[0] = True

    changed = True
    while changed:
        changed = False
        for key, mat in M_16.items():
            for m in range(16):
                for n in range(16):
                    if abs(mat[m, n]) > 1e-12:
                        if fixed[m] and not fixed[n]:
                            # Set theta_n from: mat[m,n] * exp(i(theta_n - theta_m)) real
                            angle = np.angle(mat[m, n])
                            phases[n] = phases[m] - angle
                            fixed[n] = True
                            changed = True
                        elif fixed[n] and not fixed[m]:
                            angle = np.angle(mat[m, n])
                            phases[m] = phases[n] + angle
                            fixed[m] = True
                            changed = True

    if all(fixed):
        print(f"  All 16 phases determined")
    else:
        unfixed = [i for i in range(16) if not fixed[i]]
        print(f"  WARNING: unfixed phases at indices {unfixed}")

    # Apply phase transformation
    phase_mat = np.diag(np.exp(1j * phases))
    phase_inv = np.diag(np.exp(-1j * phases))
    for key in M_16:
        M_16[key] = phase_mat @ M_16[key] @ phase_inv

    max_imag_after = max(np.max(np.abs(mat.imag)) for mat in M_16.values())
    print(f"  After phase fix, max imaginary: {max_imag_after:.2e}")

# Extract real part
M_real = {}
for key, mat in M_16.items():
    M_real[key] = mat.real.copy()

# Re-verify Cartan
for k in range(5):
    idx = (2*k+1, 2*k+2)
    expected = [w[k] / 2.0 for w in weight_table]
    err = np.max(np.abs(np.diag(M_real[idx]) - expected))
    assert err < 1e-10, f"Cartan H_{k+1} broken: err={err}"

# Verify homomorphism: [M_ij, M_kl] = structure_constants
print("\nVerifying Lie algebra homomorphism...")

def bracket_result(ij, kl):
    """Structure constants of so(10)."""
    i, j = ij
    k, l = kl
    result = {}
    terms = []
    if j == k: terms.append((i, l, +1))
    if i == k: terms.append((j, l, -1))
    if j == l: terms.append((i, k, -1))
    if i == l: terms.append((j, k, +1))
    for p, q, coeff in terms:
        if p == q: continue
        key = (min(p,q), max(p,q))
        sign = 1 if p < q else -1
        result[key] = result.get(key, 0) + coeff * sign
    return {k: v for k, v in result.items() if v != 0}

max_hom_err = 0
for ij in pairs:
    for kl in pairs:
        comm = M_real[ij] @ M_real[kl] - M_real[kl] @ M_real[ij]
        bkt = bracket_result(ij, kl)
        expected = np.zeros((16, 16))
        for gen, coeff in bkt.items():
            expected += coeff * M_real[gen]
        err = np.max(np.abs(comm - expected))
        max_hom_err = max(max_hom_err, err)
        if err > 1e-8:
            print(f"  [{ij},{kl}]: err={err:.2e}")

print(f"  Max homomorphism error: {max_hom_err:.2e}")
assert max_hom_err < 1e-8, "Homomorphism FAILED!"
print("  PASSED")

# Rationalize: entries should be multiples of 1/2
print("\nRationalizing entries...")
M_rat = {}
for key, mat in M_real.items():
    M_rat[key] = np.round(mat * 2) / 2

# Verify rationalized homomorphism
max_rat_err = 0
for ij in pairs:
    for kl in pairs:
        comm = M_rat[ij] @ M_rat[kl] - M_rat[kl] @ M_rat[ij]
        bkt = bracket_result(ij, kl)
        expected = np.zeros((16, 16))
        for gen, coeff in bkt.items():
            expected += coeff * M_rat[gen]
        err = np.max(np.abs(comm - expected))
        max_rat_err = max(max_rat_err, err)

print(f"  Max error after rationalization: {max_rat_err:.2e}")
if max_rat_err > 1e-10:
    print("  Rationalization fails! Entries are not half-integers.")
    # Check what values appear
    vals = set()
    for mat in M_real.values():
        for i in range(16):
            for j in range(16):
                v = mat[i,j]
                if abs(v) > 1e-10:
                    vals.add(round(v, 6))
    print(f"  Distinct nonzero values: {sorted(vals)}")
    print("  Will use higher precision rationalization...")
    # Try denominators up to 8
    M_rat2 = {}
    for key, mat in M_real.items():
        rmat = np.zeros((16,16))
        for i in range(16):
            for j in range(16):
                fr = Fraction(mat[i,j]).limit_denominator(8)
                rmat[i,j] = float(fr)
        M_rat2[key] = rmat

    # Re-verify
    max_rat_err2 = 0
    for ij in pairs:
        for kl in pairs:
            comm = M_rat2[ij] @ M_rat2[kl] - M_rat2[kl] @ M_rat2[ij]
            bkt = bracket_result(ij, kl)
            expected = np.zeros((16, 16))
            for gen, coeff in bkt.items():
                expected += coeff * M_rat2[gen]
            err = np.max(np.abs(comm - expected))
            max_rat_err2 = max(max_rat_err2, err)
    print(f"  Max error with limit_denom(8): {max_rat_err2:.2e}")
    if max_rat_err2 < 1e-10:
        M_rat = M_rat2
        print("  PASSED with denominator 8")
    else:
        print("  FAILED - using floating point")
        M_rat = M_real  # fallback
else:
    print("  PASSED - all entries are half-integers")

# Field names
def field_name(i, j):
    def idx(k):
        return str(k) if k <= 9 else chr(ord('a') + k - 10)
    return f"l{idx(i)}{idx(j)}"

pair_to_field = {(i,j): field_name(i,j) for i,j in pairs}

# Print matrix info
print("\nMatrix summary:")
for (i, j) in pairs:
    mat = M_rat[(i, j)]
    nnz = np.count_nonzero(np.abs(mat) > 1e-12)
    is_diag = np.max(np.abs(mat - np.diag(np.diag(mat)))) < 1e-12
    if is_diag:
        print(f"  M[{i:2d},{j:2d}] ({field_name(i,j)}): diagonal")
    else:
        print(f"  M[{i:2d},{j:2d}] ({field_name(i,j)}): nnz={nnz:3d}")

# Generate Lean 4 code
print("\n" + "="*70)
print("GENERATING LEAN 4 CODE")
print("="*70)

def val_to_lean(v):
    """Convert a floating point value to Lean literal."""
    if abs(v) < 1e-12:
        return "0"
    fr = Fraction(v).limit_denominator(8)
    if fr == Fraction(1, 2):
        return "(1:ℝ)/2"
    elif fr == Fraction(-1, 2):
        return "-(1:ℝ)/2"
    elif fr == Fraction(1, 1):
        return "1"
    elif fr == Fraction(-1, 1):
        return "-1"
    elif fr.denominator == 1:
        return str(fr.numerator)
    elif fr.numerator > 0:
        return f"({fr.numerator}:ℝ)/{fr.denominator}"
    else:
        return f"-({abs(fr.numerator)}:ℝ)/{fr.denominator}"

def mat_to_lean_def(name, mat, doc=""):
    """Generate Lean definition for a 16x16 matrix."""
    lines = []
    if doc:
        lines.append(f"/-- {doc} -/")
    # Use Matrix.of format: !![ row1; row2; ... ]
    lines.append(f"noncomputable def {name} : RepMatrix := !![")
    for row in range(16):
        entries = [val_to_lean(mat[row, col]) for col in range(16)]
        line = ", ".join(entries)
        if row < 15:
            line += ";"
        lines.append("  " + line)
    lines.append("]")
    return "\n".join(lines)

# Generate all 45 definitions
lean_code_parts = []
for (i, j) in pairs:
    fname = field_name(i, j)
    doc = f"Basis rep matrix for generator L_{{{i},{j}}} in the 16-dim spinor."
    lean_code_parts.append(mat_to_lean_def(f"basisRep_{fname}", M_rat[(i, j)], doc))

# Generate rho definition
rho_lines = []
rho_lines.append("/-- The 16-dimensional spinor representation rho: so(10) -> gl(16,R).")
rho_lines.append("    rho(X) = sum_{i<j} X.l_{ij} * M_{ij} where M_{ij} are the basis matrices. -/")
rho_lines.append("noncomputable def rho (X : SO10) : RepMatrix :=")
terms = []
for (i, j) in pairs:
    fname = field_name(i, j)
    terms.append(f"X.{fname} • basisRep_{fname}")
# Format with line breaks
for idx, term in enumerate(terms):
    if idx == 0:
        rho_lines.append(f"  {term} +")
    elif idx < len(terms) - 1:
        rho_lines.append(f"  {term} +")
    else:
        rho_lines.append(f"  {term}")
rho_def = "\n".join(rho_lines)

# Write output
output_path = "scripts/so10_spinor_lean_output.txt"
with open(output_path, 'w') as f:
    f.write("-- Generated by scripts/so10_spinor_rep.py\n")
    f.write("-- All 45 basis representation matrices + rho definition\n\n")
    for part in lean_code_parts:
        f.write(part + "\n\n")
    f.write(rho_def + "\n")

print(f"\nOutput written to: {output_path}")

# Also print a compact summary for manual verification
print("\nCompact matrix summary (nonzero entries only):")
for (i, j) in pairs[:10]:  # First 10 for brevity
    mat = M_rat[(i, j)]
    fname = field_name(i, j)
    entries = []
    for r in range(16):
        for c in range(16):
            v = mat[r, c]
            if abs(v) > 1e-12:
                fr = Fraction(v).limit_denominator(8)
                entries.append(f"  ({r},{c})={fr}")
    print(f"M_{fname}: {len(entries)} entries")
    for e in entries[:8]:
        print(e)
    if len(entries) > 8:
        print(f"  ... ({len(entries) - 8} more)")

print("\nDone!")
