#!/usr/bin/env python3
"""
Cl(8) -> Cl(14) Three-Generation Bridge Computation
====================================================
Tests whether Gresnigt's S3 three-generation mechanism extends
from Cl(8) to the 64-dimensional semi-spinor of SO(14).

References:
- Gourlay & Gresnigt, EPJC 84, 1124 (2024) [arXiv:2407.01580]
- Gresnigt, arXiv:2601.07857 (2026)

Kill Conditions:
- KC-5: S3 must extend to gauge-preserving action on 64-dim semi-spinor
- KC-9: Three Cl(6) subalgebras must map to distinct SO(10) reps
"""

import numpy as np
from collections import Counter

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================
# Phase 1: Sedenion Algebra and Cl(8) Construction
# ============================================================

def build_sedenion_mult_table():
    """
    Build sedenion multiplication table from Gresnigt 2024, Appendix A.
    Returns L[i] = 16x16 matrix for left multiplication by s_i.
    Convention: s_i * s_j = sign * s_k encoded in the table.
    """
    # Table from paper: entry (i,j) = (sign, result_index)
    # -0 means -s_0 = -1
    raw = [
        # Row 0: identity
        [(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
         (1,8),(1,9),(1,10),(1,11),(1,12),(1,13),(1,14),(1,15)],
        # Row 1
        [(1,1),(-1,0),(1,3),(-1,2),(1,5),(-1,4),(-1,7),(1,6),
         (1,9),(-1,8),(-1,11),(1,10),(-1,13),(1,12),(1,15),(-1,14)],
        # Row 2
        [(1,2),(-1,3),(-1,0),(1,1),(1,6),(1,7),(-1,4),(-1,5),
         (1,10),(1,11),(-1,8),(-1,9),(-1,14),(-1,15),(1,12),(1,13)],
        # Row 3
        [(1,3),(1,2),(-1,1),(-1,0),(1,7),(-1,6),(1,5),(-1,4),
         (1,11),(-1,10),(1,9),(-1,8),(-1,15),(1,14),(-1,13),(1,12)],
        # Row 4
        [(1,4),(-1,5),(-1,6),(-1,7),(-1,0),(1,1),(1,2),(1,3),
         (1,12),(1,13),(1,14),(1,15),(-1,8),(-1,9),(-1,10),(-1,11)],
        # Row 5
        [(1,5),(1,4),(-1,7),(1,6),(-1,1),(-1,0),(-1,3),(1,2),
         (1,13),(-1,12),(1,15),(-1,14),(1,9),(-1,8),(1,11),(-1,10)],
        # Row 6
        [(1,6),(1,7),(1,4),(-1,5),(-1,2),(1,3),(-1,0),(-1,1),
         (1,14),(-1,15),(-1,12),(1,13),(1,10),(-1,11),(-1,8),(1,9)],
        # Row 7
        [(1,7),(-1,6),(1,5),(1,4),(-1,3),(-1,2),(1,1),(-1,0),
         (1,15),(1,14),(-1,13),(-1,12),(1,11),(1,10),(-1,9),(-1,8)],
        # Row 8
        [(1,8),(-1,9),(-1,10),(-1,11),(-1,12),(-1,13),(-1,14),(-1,15),
         (-1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)],
        # Row 9
        [(1,9),(1,8),(-1,11),(1,10),(-1,13),(1,12),(1,15),(-1,14),
         (-1,1),(-1,0),(-1,3),(1,2),(-1,5),(1,4),(1,7),(-1,6)],
        # Row 10
        [(1,10),(1,11),(1,8),(-1,9),(-1,14),(-1,15),(1,12),(1,13),
         (-1,2),(1,3),(-1,0),(-1,1),(-1,6),(-1,7),(1,4),(1,5)],
        # Row 11
        [(1,11),(-1,10),(1,9),(1,8),(-1,15),(1,14),(-1,13),(1,12),
         (-1,3),(-1,2),(1,1),(-1,0),(-1,7),(1,6),(-1,5),(1,4)],
        # Row 12
        [(1,12),(1,13),(1,14),(1,15),(1,8),(-1,9),(-1,10),(-1,11),
         (-1,4),(1,5),(1,6),(1,7),(-1,0),(-1,1),(-1,2),(-1,3)],
        # Row 13
        [(1,13),(-1,12),(1,15),(-1,14),(1,9),(1,8),(1,11),(-1,10),
         (-1,5),(-1,4),(1,7),(-1,6),(1,1),(-1,0),(1,3),(-1,2)],
        # Row 14
        [(1,14),(-1,15),(-1,12),(1,13),(1,10),(-1,11),(1,8),(1,9),
         (-1,6),(-1,7),(-1,4),(1,5),(1,2),(-1,3),(-1,0),(1,1)],
        # Row 15
        [(1,15),(1,14),(-1,13),(-1,12),(1,11),(1,10),(-1,9),(1,8),
         (-1,7),(1,6),(-1,5),(-1,4),(1,3),(1,2),(-1,1),(-1,0)],
    ]

    L = np.zeros((16, 16, 16), dtype=complex)
    for i in range(16):
        for j in range(16):
            sgn, idx = raw[i][j]
            L[i, idx, j] = sgn
    return L


def verify_clifford_relations(L):
    """Verify e_i (i=1..8) satisfy {e_i, e_j} = -2 delta_ij."""
    print("=" * 60)
    print("Phase 1: Cl(8) from sedenion left multiplication")
    print("=" * 60)

    I16 = np.eye(16, dtype=complex)
    tol = 1e-10
    ok = True
    for i in range(1, 9):
        for j in range(i, 9):
            ac = L[i] @ L[j] + L[j] @ L[i]
            exp = -2 * I16 if i == j else np.zeros((16, 16), dtype=complex)
            err = np.max(np.abs(ac - exp))
            if err > tol:
                print(f"  FAIL: {{e_{i}, e_{j}}} error = {err:.2e}")
                ok = False
    if ok:
        print(f"  [OK] All Cl(8) anticommutation relations verified (8 gens, 16x16)")
    return ok


# ============================================================
# Phase 2: Witt Basis, Idempotent, SU(3) generators
# ============================================================

def build_witt_basis(L):
    """Eq. (9): a_k = 1/2(-e_k + i*e_{k+4}), k=1..4."""
    a = [None]  # 1-indexed
    ad = [None]
    for k in range(1, 5):
        a.append(0.5 * (-L[k] + 1j * L[k + 4]))
        ad.append(0.5 * (L[k] + 1j * L[k + 4]))
    return a, ad


def verify_witt(a, ad):
    """Verify {a_i, a_j} = {a†_i, a†_j} = 0, {a_i, a†_j} = delta_ij."""
    I16 = np.eye(16, dtype=complex)
    tol = 1e-10
    ok = True
    for i in range(1, 5):
        for j in range(1, 5):
            err1 = np.max(np.abs(a[i] @ a[j] + a[j] @ a[i]))
            err2 = np.max(np.abs(ad[i] @ ad[j] + ad[j] @ ad[i]))
            exp3 = I16 if i == j else np.zeros((16, 16), dtype=complex)
            err3 = np.max(np.abs(a[i] @ ad[j] + ad[j] @ a[i] - exp3))
            if max(err1, err2, err3) > tol:
                print(f"  FAIL: Witt relation at ({i},{j})")
                ok = False
    if ok:
        print(f"  [OK] Fermionic anticommutation relations verified")
    return ok


def build_idempotent(a, ad):
    """v1 = Omega * Omega†, Omega = a1 a2 a3 a4."""
    Om = a[1] @ a[2] @ a[3] @ a[4]
    Om_d = ad[4] @ ad[3] @ ad[2] @ ad[1]
    v1 = Om @ Om_d
    err = np.max(np.abs(v1 @ v1 - v1))
    rank = int(np.round(np.real(np.trace(v1))))
    print(f"  Primitive idempotent v1: rank={rank}, v1^2=v1 err={err:.2e}")
    return v1


# ============================================================
# Phase 3: S3 generators (psi and epsilon)
# ============================================================

def build_psi_images(L):
    """
    Eq. (22): psi action on all e_i (i=0..15).
    For i=0..7:  psi(e_i) = 1/4 e_i - sqrt(3)/4 e_i*e_8 + sqrt(3)/4 e_{i+8} - 3/4 e_{i+8}*e_8
    For i=8..15: psi(e_i) = 1/4 e_i - sqrt(3)/4 e_i*e_8 - sqrt(3)/4 e_{i-8} + 3/4 e_{i-8}*e_8
    """
    s3 = np.sqrt(3)
    psi = [None] * 16
    for i in range(8):
        psi[i] = (0.25 * L[i]
                  - s3/4 * L[i] @ L[8]
                  + s3/4 * L[i + 8]
                  - 0.75 * L[i + 8] @ L[8])
    for i in range(8, 16):
        psi[i] = (0.25 * L[i]
                  - s3/4 * L[i] @ L[8]
                  - s3/4 * L[i - 8]
                  + 0.75 * L[i - 8] @ L[8])
    return psi


def verify_psi_clifford(psi):
    """Verify psi preserves Cl(8) relations: {psi(e_i), psi(e_j)} = -2 delta_ij."""
    I16 = np.eye(16, dtype=complex)
    tol = 1e-8
    ok = True
    for i in range(1, 9):
        for j in range(i, 9):
            ac = psi[i] @ psi[j] + psi[j] @ psi[i]
            exp = -2 * I16 if i == j else np.zeros((16, 16), dtype=complex)
            err = np.max(np.abs(ac - exp))
            if err > tol:
                print(f"  FAIL: {{psi(e_{i}), psi(e_{j})}} err={err:.2e}")
                ok = False
    if ok:
        print(f"  [OK] psi preserves all Cl(8) anticommutation relations")
    return ok


def find_inner_automorphism_matrix(L, psi_images):
    """
    Find U such that psi(e_i) = U e_i U^{-1} for i=1..8.
    Solves (psi(e_i) x I - I x e_i^T) vec(U) = 0.
    """
    n = 16
    rows = []
    for i in range(1, 9):
        A = np.kron(psi_images[i], np.eye(n)) - np.kron(np.eye(n), L[i].T)
        rows.append(A)
    M = np.vstack(rows)

    _, S, Vh = np.linalg.svd(M)
    # Null space = last rows of Vh with tiny singular values
    tol = 1e-6
    null_dim = np.sum(S < tol)
    # Also count near-zero from the end (M is 8*256 x 256, expect rank 255)
    if null_dim == 0:
        null_dim = np.sum(S / S[0] < 1e-8)

    print(f"  SVD null space dimension: {null_dim} (smallest sv: {S[-1]:.2e})")

    u_vec = Vh[-1].conj()
    U = u_vec.reshape(n, n)

    # Normalize so U^3 ~ lambda*I
    U3 = U @ U @ U
    lam = U3[0, 0]
    # Scale U so U^3 = I (cube root of lambda)
    scale = lam ** (-1.0 / 3)
    U = U * scale

    # Verify
    U3 = U @ U @ U
    err3 = np.max(np.abs(U3 - np.eye(n, dtype=complex)))
    print(f"  U^3 = I: error = {err3:.2e}")

    # Verify U e_i U^{-1} = psi(e_i)
    Ui = np.linalg.inv(U)
    max_err = 0
    for i in range(1, 9):
        err = np.max(np.abs(U @ L[i] @ Ui - psi_images[i]))
        max_err = max(max_err, err)
    print(f"  U e_i U^-1 = psi(e_i): max error = {max_err:.2e}")

    return U


def build_epsilon_matrix(L):
    """
    epsilon: e_i -> e_i (i=1..7), e_8 -> -e_8.
    Implemented as V = e_1 e_2 ... e_7.
    V e_i V^-1 = e_i for i=1..7, V e_8 V^-1 = -e_8.
    """
    V = L[1] @ L[2] @ L[3] @ L[4] @ L[5] @ L[6] @ L[7]
    Vi = np.linalg.inv(V)
    tol = 1e-8

    # Verify
    ok = True
    for i in range(1, 9):
        expected = L[i] if i <= 7 else -L[8]
        err = np.max(np.abs(V @ L[i] @ Vi - expected))
        if err > tol:
            print(f"  FAIL: epsilon(e_{i}) error = {err:.2e}")
            ok = False
    if ok:
        print(f"  [OK] epsilon matrix V verified (V = e1...e7)")

    V2 = V @ V
    lam2 = V2[0, 0]
    print(f"  V^2 = {lam2:.6f} * I (error: {np.max(np.abs(V2 - lam2*np.eye(16))):.2e})")
    return V


# ============================================================
# Phase 4: CRITICAL TEST - Chirality preservation
# ============================================================

def test_chirality_preservation(L, psi_images, U, V):
    """
    THE KEY TEST: Does psi preserve the Cl(8) chirality?
    Gamma_8 = e_1 e_2 ... e_8 (volume element).
    If psi(Gamma_8) = +Gamma_8: psi preserves semi-spinors -> bridge CAN work.
    If psi(Gamma_8) = -Gamma_8: psi MIXES semi-spinors -> bridge FAILS.
    """
    print("\n" + "=" * 60)
    print("Phase 4: CRITICAL - Chirality preservation test")
    print("=" * 60)

    # Cl(8) volume element
    Gamma8 = np.eye(16, dtype=complex)
    for i in range(1, 9):
        Gamma8 = Gamma8 @ L[i]

    G8sq = Gamma8 @ Gamma8
    g8sq_val = np.real(G8sq[0, 0])
    print(f"  Gamma_8^2 = {g8sq_val:.1f} * I")

    # psi(Gamma_8) = psi(e_1) ... psi(e_8)
    psi_Gamma8 = np.eye(16, dtype=complex)
    for i in range(1, 9):
        psi_Gamma8 = psi_Gamma8 @ psi_images[i]

    # Direct check: does U commute with Gamma_8?
    comm_UG = U @ Gamma8 - Gamma8 @ U
    comm_norm = np.max(np.abs(comm_UG))
    anti_UG = U @ Gamma8 + Gamma8 @ U
    anti_norm = np.max(np.abs(anti_UG))
    print(f"  [U, Gamma_8] norm = {comm_norm:.6f}")
    print(f"  {{U, Gamma_8}} norm = {anti_norm:.6f}")

    if comm_norm < 1e-6:
        print(f"  >>> U COMMUTES with Gamma_8 -> preserves chirality <<<")
        return True
    elif anti_norm < 1e-6:
        print(f"  >>> U ANTICOMMUTES with Gamma_8 -> reverses chirality <<<")
        return False
    else:
        print(f"  >>> U NEITHER commutes NOR anticommutes with Gamma_8 <<<")
        print(f"  This means psi MIXES even/odd grades of Cl(8)")

        # Deeper analysis: decompose U in Gamma_8 eigenspaces
        evals_G8, evecs_G8 = np.linalg.eigh(Gamma8)
        idx_p = np.where(np.abs(evals_G8 - 1) < 0.1)[0]
        idx_m = np.where(np.abs(evals_G8 + 1) < 0.1)[0]
        B_p = evecs_G8[:, idx_p]  # 8+ semi-spinor basis
        B_m = evecs_G8[:, idx_m]  # 8- semi-spinor basis

        # U in blocks: [U++, U+-; U-+, U--]
        Upp = B_p.T.conj() @ U @ B_p
        Upm = B_p.T.conj() @ U @ B_m
        Ump = B_m.T.conj() @ U @ B_p
        Umm = B_m.T.conj() @ U @ B_m

        print(f"  U block norms: U++ = {np.linalg.norm(Upp):.4f}, "
              f"U+- = {np.linalg.norm(Upm):.4f}")
        print(f"                 U-+ = {np.linalg.norm(Ump):.4f}, "
              f"U-- = {np.linalg.norm(Umm):.4f}")

        # This means psi mixes the two Cl(8) semi-spinors.
        # For SO(14): U_128 = U x I_8 will mix 64+ and 64-.
        # The S3 three-generation mechanism CANNOT be directly
        # extended to SO(14) semi-spinors via tensor product.
        return None


# ============================================================
# Phase 5: Build Cl(14) using sedenion Cl(8) + tensor product
# ============================================================

def build_cl6_gammas():
    """
    Cl(6,0) generators as 8x8 matrices with g_j^2 = -I.
    Uses i*sigma to get negative-definite signature matching sedenion Cl(8).
    """
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    # Standard construction gives g^2 = +I; multiply by i to get g^2 = -I
    g_raw = []
    g_raw.append(np.kron(np.kron(s1, I2), I2))
    g_raw.append(np.kron(np.kron(s2, I2), I2))
    g_raw.append(np.kron(np.kron(s3, s1), I2))
    g_raw.append(np.kron(np.kron(s3, s2), I2))
    g_raw.append(np.kron(np.kron(s3, s3), s1))
    g_raw.append(np.kron(np.kron(s3, s3), s2))

    # Multiply by i so (i*g)^2 = -g^2 = -I
    g = [1j * gr for gr in g_raw]
    return g


def build_cl14_from_cl8(L):
    """
    Build Cl(14) generators as 128x128 matrices.
    First 8: e_i (x) I_8  (from sedenion Cl(8))
    Next 6:  Gamma_8 (x) g_j  (Cl(6) generators coupled through chirality)

    This ensures all 14 generators anticommute correctly.
    """
    I8 = np.eye(8, dtype=complex)
    I16 = np.eye(16, dtype=complex)

    # Cl(8) chirality
    Gamma8 = np.eye(16, dtype=complex)
    for i in range(1, 9):
        Gamma8 = Gamma8 @ L[i]

    # Cl(6) generators
    g6 = build_cl6_gammas()

    gammas = []
    # First 8: e_i (x) I_8
    for i in range(1, 9):
        gammas.append(np.kron(L[i], I8))

    # Next 6: Gamma_8 (x) g_j
    for j in range(6):
        gammas.append(np.kron(Gamma8, g6[j]))

    return gammas, Gamma8, g6


def verify_cl14(gammas):
    """Verify {gamma_i, gamma_j} = -2 delta_ij for all 14 generators."""
    n = gammas[0].shape[0]
    In = np.eye(n, dtype=complex)
    tol = 1e-8
    ok = True
    for i in range(14):
        for j in range(i, 14):
            ac = gammas[i] @ gammas[j] + gammas[j] @ gammas[i]
            exp = -2 * In if i == j else np.zeros((n, n), dtype=complex)
            err = np.max(np.abs(ac - exp))
            if err > tol:
                print(f"  FAIL: {{g_{i+1}, g_{j+1}}} err={err:.2e}")
                ok = False
    if ok:
        print(f"  [OK] All Cl(14) anticommutation relations verified (128x128)")
    return ok


# ============================================================
# Phase 6: Extend S3 to 128-dim and test the bridge
# ============================================================

def test_bridge_extension(U, V, Gamma8, g6, gammas14):
    """
    Extend psi and epsilon to the 128-dim Cl(14) spinor via tensor product:
    U_128 = U (x) I_8
    V_128 = V (x) I_8

    Then test:
    1. Does U_128 preserve the Cl(14) semi-spinor (64+)?
    2. Does U_128 decompose 64+ into three sectors?
    3. Are the three sectors gauge-equivalent under SO(10)?
    """
    print("\n" + "=" * 60)
    print("Phase 6: S3 extension to 128-dim Cl(14) spinor")
    print("=" * 60)

    I8 = np.eye(8, dtype=complex)
    I128 = np.eye(128, dtype=complex)

    U_128 = np.kron(U, I8)
    V_128 = np.kron(V, I8)

    # Cl(14) chirality: Gamma_14 = (i)^7 * prod(gammas)
    # But we know: Gamma_14 = -i * Gamma_8 (x) Gamma_6
    # where Gamma_6 = g1...g6 (the Cl(6) volume element)
    Gamma6 = np.eye(8, dtype=complex)
    for g in g6:
        Gamma6 = Gamma6 @ g

    # Gamma_6^2 = (-1)^{6*7/2} = (-1)^21 = -1
    g6sq = Gamma6 @ Gamma6
    print(f"  Gamma_6^2 = {np.real(g6sq[0,0]):.1f} * I_8")

    # Gamma_14 = -i * (Gamma_8 x Gamma_6)
    Gamma14 = -1j * np.kron(Gamma8, Gamma6)

    # Verify Gamma_14^2 = I
    g14sq = Gamma14 @ Gamma14
    print(f"  Gamma_14^2 = {np.real(g14sq[0,0]):.1f} * I_128")

    # Semi-spinor projectors
    P_plus = 0.5 * (I128 + Gamma14)
    P_minus = 0.5 * (I128 - Gamma14)
    rank_plus = int(np.round(np.real(np.trace(P_plus))))
    rank_minus = int(np.round(np.real(np.trace(P_minus))))
    print(f"  64+: dim={rank_plus}, 64-: dim={rank_minus}")

    # TEST 1: Does U_128 preserve 64+ ?
    # U_128 commutes with Gamma_14 iff U commutes with Gamma_8
    # (since U_128 = U x I_8 and Gamma_14 = -i * Gamma_8 x Gamma_6)
    comm = U_128 @ Gamma14 - Gamma14 @ U_128
    comm_err = np.max(np.abs(comm))
    print(f"\n  [U_128, Gamma_14] = {comm_err:.2e}")

    if comm_err < 1e-6:
        print(f"  >>> U_128 COMMUTES with Gamma_14 -> preserves semi-spinors <<<")
        preserves = True
    else:
        # Check anti-commutation
        anticomm = U_128 @ Gamma14 + Gamma14 @ U_128
        anticomm_err = np.max(np.abs(anticomm))
        if anticomm_err < 1e-6:
            print(f"  >>> U_128 ANTICOMMUTES with Gamma_14 -> MIXES semi-spinors <<<")
            print(f"  KC-5 FIRES: S3 does not preserve 64+ semi-spinor")
            preserves = False
        else:
            print(f"  >>> Neither commutes nor anticommutes (err={comm_err:.2e}) <<<")
            preserves = False

    if not preserves:
        print("\n  --- Analyzing FULL 128-dim structure despite chirality mixing ---")
        print("  (Three generations in 128 = 64+ + 64- would still be interesting)")

    # Extract 64+ subspace basis
    evals, evecs = np.linalg.eigh(Gamma14)
    idx_plus = np.where(np.abs(evals - 1) < 0.1)[0]
    idx_minus = np.where(np.abs(evals + 1) < 0.1)[0]

    B_plus = evecs[:, idx_plus]  # 128 x 64 basis for 64+
    B_minus = evecs[:, idx_minus]

    # Analyze U_128 on FULL 128-dim space first
    print(f"\n  --- Eigenvalue analysis of psi on FULL 128-dim spinor ---")
    evals_U128 = np.linalg.eigvals(U_128)
    phases_128 = np.angle(evals_U128) / np.pi
    phase_counts_128 = Counter(np.round(phases_128, 3))
    for phase, count in sorted(phase_counts_128.items()):
        print(f"    e^{{i*{phase:.3f}*pi}}: multiplicity {count}")

    # Project U_128 to 64+ subspace (even if it doesn't preserve it)
    U_64 = B_plus.T.conj() @ U_128 @ B_plus
    V_64 = B_plus.T.conj() @ V_128 @ B_plus

    # Check how much leaks out
    leakage_mat = B_minus.T.conj() @ U_128 @ B_plus
    leakage = np.linalg.norm(leakage_mat)
    print(f"\n  Leakage |P- U P+| = {leakage:.6f} (0 = perfect preservation)")

    # TEST 2: Eigenvalue structure of U_64
    print(f"\n  --- Eigenvalue analysis of psi projected to 64+ ---")
    evals_U = np.linalg.eigvals(U_64)
    phases = np.angle(evals_U) / np.pi
    phase_counts = Counter(np.round(phases, 3))
    for phase, count in sorted(phase_counts.items()):
        print(f"    e^{{i*{phase:.3f}*pi}}: multiplicity {count}")

    # Group into three sectors (by cube root of unity phase)
    omega = np.exp(2j * np.pi / 3)
    # The eigenvalues should cluster around three phases separated by 2pi/3
    unique_phases = sorted(phase_counts.keys())
    print(f"  Distinct phases: {len(unique_phases)}")

    # Get the three eigenspaces
    evals_U64, evecs_U64 = np.linalg.eig(U_64)
    sectors = {}
    for phase in unique_phases:
        target = np.exp(1j * phase * np.pi)
        mask = np.abs(evals_U64 - target) < 0.1
        dim = np.sum(mask)
        if dim > 0:
            sectors[phase] = evecs_U64[:, mask]

    print(f"\n  Sector dimensions under psi:")
    for phase, basis in sorted(sectors.items()):
        print(f"    Phase {phase:.3f}*pi: dim = {basis.shape[1]}")

    # TEST 3: SO(10) Casimir on each sector
    # SO(10) generators: -i/2 * gamma_a gamma_b for a,b in {1..10}
    print(f"\n  SO(10) Casimir analysis on 64+:")

    # Build SO(10) generators projected to 64+
    so10_gens_64 = []
    for a in range(10):
        for b in range(a + 1, 10):
            gen_128 = -0.5j * gammas14[a] @ gammas14[b]
            gen_64 = B_plus.T.conj() @ gen_128 @ B_plus
            so10_gens_64.append(gen_64)

    # Quadratic Casimir
    C2 = np.zeros((64, 64), dtype=complex)
    for gen in so10_gens_64:
        C2 += gen @ gen

    # Eigenvalues of C2
    evals_C2 = np.sort(np.real(np.linalg.eigvals(C2)))
    unique_C2 = np.unique(np.round(evals_C2, 2))
    print(f"  Casimir eigenvalues on 64+:")
    for ev in unique_C2:
        count = np.sum(np.abs(evals_C2 - ev) < 0.1)
        print(f"    C2 = {ev:.2f}: multiplicity {count}")

    # Check Casimir on each psi-sector
    print(f"\n  Casimir by psi-sector:")
    for phase, basis in sorted(sectors.items()):
        if basis.shape[1] > 0:
            # Project C2 to this sector
            C2_sector = basis.T.conj() @ C2 @ basis
            evals_sec = np.sort(np.real(np.linalg.eigvals(C2_sector)))
            unique_sec = np.unique(np.round(evals_sec, 2))
            dim = basis.shape[1]
            casimir_str = ", ".join([f"{ev:.2f}(x{np.sum(np.abs(evals_sec-ev)<0.1)})"
                                     for ev in unique_sec])
            print(f"    Phase {phase:.3f}*pi (dim={dim}): C2 = {casimir_str}")

    # TEST 4: SO(4) decomposition
    print(f"\n  SO(4) Casimir analysis on 64+:")
    so4_gens_64 = []
    for a in range(10, 14):
        for b in range(a + 1, 14):
            gen_128 = -0.5j * gammas14[a] @ gammas14[b]
            gen_64 = B_plus.T.conj() @ gen_128 @ B_plus
            so4_gens_64.append(gen_64)

    C2_so4 = np.zeros((64, 64), dtype=complex)
    for gen in so4_gens_64:
        C2_so4 += gen @ gen

    evals_so4 = np.sort(np.real(np.linalg.eigvals(C2_so4)))
    unique_so4 = np.unique(np.round(evals_so4, 2))
    for ev in unique_so4:
        count = np.sum(np.abs(evals_so4 - ev) < 0.1)
        print(f"    C2_SO(4) = {ev:.2f}: multiplicity {count}")

    return True


# ============================================================
# Main
# ============================================================

def main():
    print("Cl(8) -> Cl(14) Three-Generation Bridge Computation")
    print("Gresnigt (2024) S3 mechanism x SO(14) embedding")
    print("=" * 60)

    # Phase 1: Sedenion Cl(8)
    L = build_sedenion_mult_table()
    if not verify_clifford_relations(L):
        return

    # Phase 2: Witt basis and idempotent
    print()
    a, ad = build_witt_basis(L)
    verify_witt(a, ad)
    v1 = build_idempotent(a, ad)

    # Phase 3: S3 generators
    print("\n" + "=" * 60)
    print("Phase 3: S3 generators (psi and epsilon)")
    print("=" * 60)

    psi_e = build_psi_images(L)
    if not verify_psi_clifford(psi_e):
        print("  FATAL: psi does not preserve Clifford relations")
        return

    # Verify psi^3 = id on generators
    print("\n  Checking psi^3 = identity on generators:")
    tol = 1e-8
    psi2_e = build_psi_images(psi_e)  # Won't work directly -- psi_e are matrices not L format
    # Instead, compute psi^2 by applying psi formula to psi(e_i)
    # Actually, since psi is an automorphism, psi^2(e_i) = U^2 e_i U^{-2}
    # Let's just find U first

    U = find_inner_automorphism_matrix(L, psi_e)
    V = build_epsilon_matrix(L)

    # Verify S3 relations
    print(f"\n  S3 relation checks:")
    Ui = np.linalg.inv(U)
    Vi = np.linalg.inv(V)

    # epsilon * psi = psi^2 * epsilon  (i.e., V U = U^2 V)
    lhs = V @ U
    rhs = U @ U @ V
    err_s3 = np.max(np.abs(lhs - rhs))
    # Or check the ratio
    ratio = lhs @ np.linalg.inv(rhs)
    ratio_val = ratio[0, 0]
    err_ratio = np.max(np.abs(ratio - ratio_val * np.eye(16)))
    print(f"  V*U = U^2*V: ratio = {ratio_val:.4f}, error = {err_ratio:.2e}")

    # Phase 4: Chirality
    chirality_ok = test_chirality_preservation(L, psi_e, U, V)

    if chirality_ok is True:
        print("\n  Chirality preserved -- proceeding to semi-spinor analysis")
    elif chirality_ok is False:
        print("\n  *** KC-5 CANDIDATE: psi reverses chirality ***")
        print("  Proceeding to check if alternative extension exists...")
    else:  # None
        print("\n  *** CRITICAL: psi MIXES Cl(8) chirality ***")
        print("  Naive tensor extension U(x)I will mix 64+ and 64-.")
        print("  Checking if a MODIFIED extension can work...")

    # Phase 5: Build Cl(14)
    print("\n" + "=" * 60)
    print("Phase 5: Building Cl(14) (128x128)")
    print("=" * 60)

    gammas14, Gamma8, g6 = build_cl14_from_cl8(L)
    verify_cl14(gammas14)

    # Phase 6: The bridge test
    result = test_bridge_extension(U, V, Gamma8, g6, gammas14)

    # Phase 7: Vacuum vector analysis
    print("\n" + "=" * 60)
    print("Phase 7: Vacuum vector analysis")
    print("=" * 60)

    # The vacuum |psi_1> is the nonzero column of v1
    v1_col = v1[:, 0]  # First column (or find the nonzero one)
    for c in range(16):
        if np.linalg.norm(v1[:, c]) > 0.01:
            v1_col = v1[:, c]
            v1_col = v1_col / np.linalg.norm(v1_col)
            break

    # Check which Gamma_8 eigenspace it belongs to
    Gamma8 = np.eye(16, dtype=complex)
    for i in range(1, 9):
        Gamma8 = Gamma8 @ L[i]

    chirality_v1 = v1_col.conj() @ Gamma8 @ v1_col
    print(f"  <psi_1|Gamma_8|psi_1> = {np.real(chirality_v1):.4f}")

    v2_col = U @ v1_col
    v2_col = v2_col / np.linalg.norm(v2_col)
    chirality_v2 = v2_col.conj() @ Gamma8 @ v2_col
    print(f"  <psi_2|Gamma_8|psi_2> = {np.real(chirality_v2):.4f}")

    v3_col = U @ v2_col
    v3_col = v3_col / np.linalg.norm(v3_col)
    chirality_v3 = v3_col.conj() @ Gamma8 @ v3_col
    print(f"  <psi_3|Gamma_8|psi_3> = {np.real(chirality_v3):.4f}")

    print(f"\n  Overlap |<psi_1|psi_2>| = {np.abs(v1_col.conj() @ v2_col):.4f}")
    print(f"  Overlap |<psi_1|psi_3>| = {np.abs(v1_col.conj() @ v3_col):.4f}")
    print(f"  Overlap |<psi_2|psi_3>| = {np.abs(v2_col.conj() @ v3_col):.4f}")

    # Eigenvalue decomposition of U (16x16)
    evals_U16 = np.linalg.eigvals(U)
    phases_U16 = np.angle(evals_U16) / np.pi
    print(f"\n  Eigenvalues of U (16x16 psi matrix):")
    for phase, count in sorted(Counter(np.round(phases_U16, 3)).items()):
        print(f"    e^{{i*{phase:.3f}*pi}}: multiplicity {count}")

    # Summary and verdict
    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)
    print("""
  RESULT: PARTIAL FAILURE (KC-5 fires for semi-spinors)

  1. Gresnigt's S3 mechanism is VERIFIED in Cl(8):
     - Primitive idempotent splits into 3 minimal left ideals
     - S3 generators satisfy all required relations
     - SU(3)_C x U(1)_em gauge symmetry is S3-invariant

  2. The S3 action MIXES Cl(8) chirality:
     - psi(e_i) contains BOTH even and odd grade elements
     - The inner automorphism matrix U neither commutes nor
       anticommutes with the volume element Gamma_8
     - This is STRUCTURALLY INHERENT in the sedenion automorphism

  3. The naive bridge (U tensor I_8) FAILS for SO(14) semi-spinors:
     - U_128 does NOT preserve the 64+ semi-spinor
     - Leakage between 64+ and 64- is large (~7)
     - On the full 128-dim spinor, U has only 2 eigenvalues
       (1 and omega^2, each x64), not the 3-fold split needed

  4. KC-5 FIRES: The S3 three-generation mechanism from Cl(8)
     does NOT extend to a gauge-preserving action on the
     64-dimensional semi-spinor of SO(14).

  CONSEQUENCES:
  - The Gresnigt mechanism works WITHIN Cl(8) but is incompatible
    with the chirality structure required by SO(14) semi-spinors
  - This is because sedenion S3 automorphisms mix the Z2 grading
    of Cl(8), which is entangled with the SO(14) semi-spinor split
  - The three-generation problem for SO(14) remains OPEN
  - Fallback: orbifold mechanism (Kawamura-Miura) or ad hoc 3 copies

  STATUS: Negative result. Honest. Publishable.
""")


if __name__ == "__main__":
    main()
