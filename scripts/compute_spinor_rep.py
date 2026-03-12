#!/usr/bin/env python3
"""Compute the 45 generators of the 16-dim spinor representation of so(10).

Uses Clifford algebra Cl(10,0): build 10 gamma matrices as tensor products,
project to the positive chirality subspace (16-dim), compute
Gamma_{ij} = (1/2) gamma_i gamma_j restricted to that subspace.

Output: 45 matrices separated into real and imaginary parts for Lean 4.
"""
import numpy as np
from itertools import combinations

def build_gamma_matrices(n=10):
    """Build n gamma matrices for Cl(n,0) using tensor product construction.

    Uses: gamma_{2k+1} = sz^{otimes k} otimes sx otimes I^{otimes (m-k-1)}
          gamma_{2k+2} = sz^{otimes k} otimes (i*sy) otimes I^{otimes (m-k-1)}

    where m = n//2 = 5, giving 2^5 = 32 dim matrices.
    All square to +I (Euclidean signature).
    """
    m = n // 2
    I2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy_complex = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)

    gammas = []
    for k in range(m):
        # gamma_{2k+1}: sz^{k} x sx x I^{m-k-1}
        factors_odd = [sz]*k + [sx] + [I2]*(m-k-1)
        g_odd = factors_odd[0]
        for f in factors_odd[1:]:
            g_odd = np.kron(g_odd, f)
        gammas.append(g_odd)

        # gamma_{2k+2}: sz^{k} x (i*sy) x I^{m-k-1}
        factors_even = [sz]*k + [sy_complex] + [I2]*(m-k-1)
        g_even = factors_even[0]
        for f in factors_even[1:]:
            g_even = np.kron(g_even, f)
        gammas.append(g_even)

    return gammas


def verify_clifford(gammas):
    """Verify {gamma_i, gamma_j} = 2*delta_ij * I."""
    n = len(gammas)
    dim = gammas[0].shape[0]
    for i in range(n):
        for j in range(n):
            anticomm = gammas[i] @ gammas[j] + gammas[j] @ gammas[i]
            expected = 2 * (1 if i == j else 0) * np.eye(dim)
            if np.max(np.abs(anticomm - expected)) > 1e-10:
                print(f"  FAIL: gamma_{i+1}, gamma_{j+1}")
                return False
    print("  Clifford relation verified OK")
    return True


def build_chirality_projector(gammas):
    """Compute chirality = i * gamma_1...gamma_10, project to +1 eigenspace."""
    dim = gammas[0].shape[0]
    product = np.eye(dim, dtype=complex)
    for g in gammas:
        product = product @ g

    # For n=10: (gamma_1...gamma_10)^2 = (-1)^45 * I = -I
    # chirality = -i * product gives chirality^2 = (-i)^2*(-I) = (-1)(-I) = I
    # Use -i to get the POSITIVE chirality (even # of minus signs) matching signTable
    chirality = -1j * product

    chir_sq = chirality @ chirality
    assert np.allclose(chir_sq, np.eye(dim)), "chirality^2 != I"
    print("  Chirality^2 = I OK")

    P_plus = 0.5 * (np.eye(dim) + chirality)
    rank = int(np.round(np.real(np.trace(P_plus))))
    assert rank == 16, f"Expected rank 16, got {rank}"
    print(f"  +1 eigenspace dim = {rank} OK")

    # Find orthonormal basis for +1 eigenspace
    eigenvalues, eigenvectors = np.linalg.eig(chirality)
    plus_idx = np.where(np.abs(eigenvalues - 1) < 1e-8)[0]
    assert len(plus_idx) == 16
    basis = eigenvectors[:, plus_idx]

    return basis


def compute_generators(gammas, basis):
    """Compute 45 generators Gamma_{ij} = (1/2) gamma_i gamma_j on +1 eigenspace."""
    B = basis
    B_dag = B.conj().T
    generators = {}

    for i in range(len(gammas)):
        for j in range(i+1, len(gammas)):
            gen_full = 0.5 * gammas[i] @ gammas[j]
            gen_16 = B_dag @ gen_full @ B
            generators[(i+1, j+1)] = gen_16

    print(f"  Computed {len(generators)} generators OK")
    return generators


def verify_brackets(generators):
    """Verify all 990 bracket relations: [Gamma_ij, Gamma_kl] = sum of Gamma's."""
    errors = 0
    for (i1, j1), M1 in generators.items():
        for (i2, j2), M2 in generators.items():
            if (i1, j1) >= (i2, j2):
                continue
            comm = M1 @ M2 - M2 @ M1

            def get_gen(a, b):
                if a == b: return np.zeros((16, 16), dtype=complex)
                elif a < b: return generators.get((a, b), np.zeros((16, 16), dtype=complex))
                else: return -generators.get((b, a), np.zeros((16, 16), dtype=complex))

            expected = np.zeros((16, 16), dtype=complex)
            if j1 == i2: expected += get_gen(i1, j2)
            if i1 == i2: expected -= get_gen(j1, j2)
            if j1 == j2: expected -= get_gen(i1, i2)
            if i1 == j2: expected += get_gen(j1, i2)

            if np.max(np.abs(comm - expected)) > 1e-8:
                errors += 1
    print(f"  990 bracket pairs checked, errors: {errors}")
    return errors == 0


def find_basis_permutation(generators):
    """Find permutation to match the signTable basis in spinor_rep.lean.

    The existing Cartan generators are H_k with eigenvalues signTable[w][k]/2.
    Our Gamma_{2k-1,2k} should correspond to i*H_k (since the representation
    gives imaginary diagonal entries for Cartan generators).
    """
    sign_table = [
        [+1, +1, +1, +1, +1],
        [+1, +1, +1, -1, -1],
        [+1, +1, -1, +1, -1],
        [+1, +1, -1, -1, +1],
        [+1, -1, +1, +1, -1],
        [+1, -1, +1, -1, +1],
        [+1, -1, -1, +1, +1],
        [+1, -1, -1, -1, -1],
        [-1, +1, +1, +1, -1],
        [-1, +1, +1, -1, +1],
        [-1, +1, -1, +1, +1],
        [-1, +1, -1, -1, -1],
        [-1, -1, +1, +1, +1],
        [-1, -1, +1, -1, -1],
        [-1, -1, -1, +1, -1],
        [-1, -1, -1, -1, +1],
    ]

    cartan_pairs = [(1,2), (3,4), (5,6), (7,8), (9,10)]

    # Extract diagonal of Cartan generators (should be pure imaginary)
    computed_weights = []
    for w in range(16):
        weight = []
        for k, (i, j) in enumerate(cartan_pairs):
            val = generators[(i, j)][w, w]
            # Should be +i/2 or -i/2
            imag_val = val.imag
            weight.append(int(np.sign(imag_val)))
        computed_weights.append(tuple(weight))

    expected_weights = [tuple(row) for row in sign_table]

    # Find permutation
    perm = []
    for cw in computed_weights:
        for idx, ew in enumerate(expected_weights):
            if cw == ew and idx not in perm:
                perm.append(idx)
                break

    if len(set(perm)) == 16:
        print(f"  Basis permutation found OK")
        return perm
    else:
        print(f"  WARNING: Could not find valid permutation")
        return None


def reorder_generators(generators, perm):
    """Reorder matrices to match signTable basis."""
    P = np.zeros((16, 16), dtype=complex)
    for i, j in enumerate(perm):
        P[j, i] = 1.0
    return {key: P @ mat @ P.T for key, mat in generators.items()}


def classify_generators(generators):
    """Classify generators as real or imaginary."""
    real_gens = []
    imag_gens = []
    for (i, j), mat in sorted(generators.items()):
        real_err = np.max(np.abs(mat.imag))
        imag_err = np.max(np.abs(mat.real))
        if real_err < 1e-10:
            real_gens.append((i, j))
        elif imag_err < 1e-10:
            imag_gens.append((i, j))
        else:
            print(f"  WARNING: M{i}_{j} is neither real nor pure imaginary!")
    return real_gens, imag_gens


def so10_field_name(i, j):
    def digit(n): return 'a' if n == 10 else str(n)
    return f"l{digit(i)}{digit(j)}"


def val_to_lean(v, use_complex=False):
    """Convert a value (should be 0, +/-0.5, or +/-1) to Lean literal."""
    r = round(v * 2) / 2
    if abs(r) < 1e-10: return "0"
    elif abs(r - 0.5) < 1e-10: return "(1/2)"
    elif abs(r + 0.5) < 1e-10: return "(-1/2)"
    elif abs(r - 1.0) < 1e-10: return "1"
    elif abs(r + 1.0) < 1e-10: return "(-1)"
    else: return f"({r})"


def matrix_to_lean(mat_real, name, type_name="RepMatrix"):
    """Convert a real 16x16 matrix to Lean definition."""
    nonzero = [(i, j, mat_real[i, j]) for i in range(16) for j in range(16)
               if abs(mat_real[i, j]) > 1e-10]

    lines = [f"def {name} : {type_name} :="]
    if not nonzero:
        lines.append("  0")
    else:
        lines.append("  Matrix.of fun i j =>")
        lines.append("    match i, j with")
        for i, j, v in nonzero:
            lines.append(f"    | {i}, {j} => {val_to_lean(v)}")
        lines.append("    | _, _ => 0")
    return "\n".join(lines)


def generate_lean_code(generators, real_gens, imag_gens):
    """Generate complete Lean 4 code for the spinor representation."""

    lines = []
    lines.append("/-!")
    lines.append("  Auto-generated by scripts/compute_spinor_rep.py")
    lines.append("")
    lines.append("  45 basis matrices for the 16-dim spinor representation of so(10).")
    lines.append("  Split into real (20) and imaginary (25) parts:")
    lines.append("    - Same-parity pairs (odd-odd, even-even): REAL matrices")
    lines.append("    - Mixed-parity pairs (odd-even): PURE IMAGINARY matrices")
    lines.append("")
    lines.append("  The full complex representation is:")
    lines.append("    crho(X) = sum(real_terms) + I * sum(imag_terms)")
    lines.append("-/")
    lines.append("")

    # Real matrices (same-parity pairs)
    lines.append("/-! ### Real basis matrices (20 matrices, same-parity index pairs) -/")
    lines.append("")
    for i, j in real_gens:
        mat = np.real(generators[(i, j)])
        name = f"R{i}_{j}"
        lines.append(matrix_to_lean(mat, name))
        lines.append("")

    # Imaginary matrices (mixed-parity pairs) - output the imaginary PART as real matrix
    lines.append("/-! ### Imaginary basis matrices (25 matrices, mixed-parity index pairs)")
    lines.append("    These represent the imaginary parts: M_{ij} = i * J_{ij} -/")
    lines.append("")
    for i, j in imag_gens:
        mat = np.imag(generators[(i, j)])  # Extract imaginary part
        name = f"J{i}_{j}"
        lines.append(matrix_to_lean(mat, name))
        lines.append("")

    # Generate rhoReal definition
    lines.append("/-- Real part of rho: sum of X.l_{ij} * R_{ij} over same-parity pairs -/")
    lines.append("noncomputable def rhoReal (X : SO10) : RepMatrix :=")
    terms = [f"X.{so10_field_name(i,j)} \u2022 R{i}_{j}" for i, j in real_gens]
    lines.append("  " + " +\n  ".join(terms))
    lines.append("")

    # Generate rhoImag definition
    lines.append("/-- Imaginary part of rho: sum of X.l_{ij} * J_{ij} over mixed-parity pairs -/")
    lines.append("noncomputable def rhoImag (X : SO10) : RepMatrix :=")
    terms = [f"X.{so10_field_name(i,j)} \u2022 J{i}_{j}" for i, j in imag_gens]
    lines.append("  " + " +\n  ".join(terms))
    lines.append("")

    return "\n".join(lines)


def main():
    print("=" * 60)
    print("SO(10) Spinor Representation - Complex Analysis")
    print("=" * 60)

    print("\n[1] Building gamma matrices...")
    gammas = build_gamma_matrices(10)
    print(f"  {len(gammas)} matrices of size {gammas[0].shape}")

    print("\n[2] Verifying Clifford relations...")
    assert verify_clifford(gammas)

    print("\n[3] Building chirality projector...")
    basis = build_chirality_projector(gammas)

    print("\n[4] Computing 45 generators...")
    generators = compute_generators(gammas, basis)

    print("\n[5] Verifying all 990 brackets...")
    assert verify_brackets(generators)

    cartan_pairs = [(1,2), (3,4), (5,6), (7,8), (9,10)]
    sign_table = [
            [+1, +1, +1, +1, +1], [+1, +1, +1, -1, -1],
            [+1, +1, -1, +1, -1], [+1, +1, -1, -1, +1],
            [+1, -1, +1, +1, -1], [+1, -1, +1, -1, +1],
            [+1, -1, -1, +1, +1], [+1, -1, -1, -1, -1],
            [-1, +1, +1, +1, -1], [-1, +1, +1, -1, +1],
            [-1, +1, -1, +1, +1], [-1, +1, -1, -1, -1],
            [-1, -1, +1, +1, +1], [-1, -1, +1, -1, -1],
            [-1, -1, -1, +1, -1], [-1, -1, -1, -1, +1],
        ]

    # Debug: print computed weights before permutation
    print("\n  Computed weights (imaginary diag * 2):")
    for w in range(16):
        wt = tuple(int(round(2 * generators[(ci,cj)][w,w].imag)) for ci,cj in cartan_pairs)
        print(f"    weight {w:2d}: {wt}")

    print("\n[6] Finding basis permutation to match signTable...")
    perm = find_basis_permutation(generators)
    if perm:
        generators = reorder_generators(generators, perm)
        for k, (ci, cj) in enumerate(cartan_pairs):
            gen = generators[(ci, cj)]
            for w in range(16):
                expected_imag = sign_table[w][k] / 2.0
                actual_imag = gen[w, w].imag
                if abs(actual_imag - expected_imag) > 1e-10:
                    print(f"  MISMATCH: H_{k+1} weight {w}: got {actual_imag}, expected {expected_imag}")
        print("  Cartan generators match signTable (as i*diag) OK")
    else:
        print("  Proceeding without reordering")

    print("\n[7] Re-verifying brackets after reordering...")
    assert verify_brackets(generators)

    print("\n[8] Classifying generators...")
    real_gens, imag_gens = classify_generators(generators)
    print(f"  Real: {len(real_gens)} (same-parity pairs)")
    print(f"  Pure imaginary: {len(imag_gens)} (mixed-parity pairs)")

    # Show structure of real generators
    print("\n[9] Matrix sparsity:")
    for i, j in sorted(generators.keys()):
        mat = generators[(i, j)]
        is_real = (i, j) in real_gens
        nz_real = np.sum(np.abs(mat.real) > 1e-10)
        nz_imag = np.sum(np.abs(mat.imag) > 1e-10)
        kind = "REAL" if is_real else "IMAG"
        diag = "diag" if np.allclose(mat - np.diag(np.diag(mat)), 0, atol=1e-10) else f"{max(nz_real,nz_imag)}nz"
        print(f"  M{i}_{j} ({so10_field_name(i,j)}): {kind} {diag}")

    print("\n[10] Generating Lean code...")
    lean_code = generate_lean_code(generators, real_gens, imag_gens)

    output_file = "scripts/spinor_rep_matrices.lean.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(lean_code)
    print(f"  Written to {output_file}")

    # Summary stats
    total_nz = sum(np.sum(np.abs(generators[k]) > 1e-10) for k in generators)
    print(f"\n  Total non-zero entries: {total_nz}")
    print(f"  Average per matrix: {total_nz/45:.1f}")

    # Verify key identity: Cartan = i * diag(signTable/2)
    print("\n[11] Verifying Cartan = i * cartanH...")
    for k, (ci, cj) in enumerate(cartan_pairs):
        gen = generators[(ci, cj)]
        # gen should be i * diag(signTable[w][k]/2)
        for w in range(16):
            expected = 1j * sign_table[w][k] / 2
            actual = gen[w, w]
            if abs(actual - expected) > 1e-10:
                print(f"  FAIL: k={k}, w={w}: {actual} vs {expected}")
                break
        else:
            continue
        break
    else:
        print("  Gamma_{2k-1,2k} = i * cartanH(k) VERIFIED for all k=1..5")


if __name__ == "__main__":
    main()
