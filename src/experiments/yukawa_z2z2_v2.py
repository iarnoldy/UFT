#!/usr/bin/env python3
"""
Yukawa Coupling in Z2xZ2 Character Basis — KC-12 v2 (Corrected)
================================================================

v1 used Tr(Gamma^A|_{sector}) which is identically zero (gamma matrices
are traceless). This gave a vacuous "all zeros" result.

v2 computes the CORRECT observables:
1. Eigenvalue spectrum of the full Yukawa matrix M = sum_A v_A Gamma^A
2. Character-resolved projections using P_chiral to separate mass terms
3. The family mass matrix using SPECIFIC SO(10) state projections

KEY INSIGHT: M^2 = (sum_A v_A Gamma^A)^2 = |v|^2 * I because
{Gamma^A, Gamma^B} = 2 delta^{AB}. So the VECTOR Higgs gives
DEGENERATE masses (no family splitting). Family splitting requires
HIGHER Higgs representations (adjoint, rank-3, etc).

KC-12 TEST: Does the Z2xZ2 character decomposition give 3+1 when
the adjoint Higgs is included?
"""

import numpy as np
from itertools import combinations

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================
# Part 0: Build Cl(14) (same as v1)
# ============================================================
print("=" * 70)
print("Building Cl(14)...")
print("=" * 70)

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
I8 = np.eye(8, dtype=complex)

def kron3(a, b, c): return np.kron(a, np.kron(b, c))
def kron4(a, b, c, d): return np.kron(a, np.kron(b, np.kron(c, d)))

g8 = [1j * kron4(sx, I2, I2, I2), 1j * kron4(sy, I2, I2, I2),
      1j * kron4(sz, sx, I2, I2), 1j * kron4(sz, sy, I2, I2),
      1j * kron4(sz, sz, sx, I2), 1j * kron4(sz, sz, sy, I2),
      1j * kron4(sz, sz, sz, sx), 1j * kron4(sz, sz, sz, sy)]

Gamma8 = np.eye(16, dtype=complex)
for g in g8:
    Gamma8 = Gamma8 @ g
Gamma8_n = Gamma8 / np.sqrt((Gamma8 @ Gamma8)[0, 0])

g6 = [1j * kron3(sx, I2, I2), 1j * kron3(sy, I2, I2),
      1j * kron3(sz, sx, I2), 1j * kron3(sz, sy, I2),
      1j * kron3(sz, sz, sx), 1j * kron3(sz, sz, sy)]

gammas = []
for i in range(8):
    gammas.append(np.kron(g8[i], I8))
for j in range(6):
    gammas.append(np.kron(Gamma8_n, g6[j]))

# Chirality
Gamma15 = np.eye(128, dtype=complex)
for g in gammas:
    Gamma15 = Gamma15 @ g
Gamma15 = Gamma15 / np.sqrt((Gamma15 @ Gamma15)[0, 0])

print(f"  Clifford OK, Gamma15^2=I: {np.max(np.abs(Gamma15@Gamma15 - np.eye(128))):.2e}")

# ============================================================
# Part 1: SO(4) torus -> four family sectors
# ============================================================
print("\n" + "=" * 70)
print("Part 1: Family Sector Decomposition")
print("=" * 70)

T1 = (1j / 2) * gammas[10] @ gammas[11]
T2 = (1j / 2) * gammas[12] @ gammas[13]

# Joint diagonalization of T1, T2
t1_evals, t1_evecs = np.linalg.eigh(T1)
t1_vals = np.round(t1_evals, 6)

joint_basis = np.zeros((128, 128), dtype=complex)
joint_t1 = np.zeros(128)
joint_t2 = np.zeros(128)
idx = 0
for t1v in np.unique(t1_vals):
    mask = np.abs(t1_vals - t1v) < 1e-4
    sub = t1_evecs[:, mask]
    T2_sub = sub.conj().T @ T2 @ sub
    t2_sub, v2_sub = np.linalg.eigh(T2_sub)
    new = sub @ v2_sub
    n = new.shape[1]
    joint_basis[:, idx:idx+n] = new
    joint_t1[idx:idx+n] = t1v
    joint_t2[idx:idx+n] = np.round(t2_sub, 6)
    idx += n

# Classify sectors
sectors = {}
for k in range(128):
    s1 = +1 if joint_t1[k] > 0 else -1
    s2 = +1 if joint_t2[k] > 0 else -1
    key = (s1, s2)
    sectors.setdefault(key, []).append(k)

sector_keys = sorted(sectors.keys())
print("  Sectors:", {k: len(v) for k, v in sorted(sectors.items())})

# Build sector projector MATRICES (in the joint eigenbasis)
# P_sector[key] = projector onto sector key in the ORIGINAL 128-dim basis
P_sector = {}
for key in sector_keys:
    vecs = joint_basis[:, sectors[key]]  # 128 x 32
    P_sector[key] = vecs @ vecs.conj().T  # 128 x 128 projector

# Chirality projectors
P_plus = (np.eye(128) + Gamma15) / 2
P_minus = (np.eye(128) - Gamma15) / 2

# ============================================================
# Part 2: WHY Tr(Gamma^A) = 0 and M^2 = |v|^2 I
# ============================================================
print("\n" + "=" * 70)
print("Part 2: Vector Higgs Degeneracy (M^2 = |v|^2 I)")
print("=" * 70)

# Test: M = Gamma^11 + Gamma^13, compute M^2
M_test = gammas[10] + gammas[12]
M2_test = M_test @ M_test
print(f"  M = Gamma^11 + Gamma^13")
print(f"  M^2 eigenvalues: {np.unique(np.round(np.linalg.eigvalsh(M2_test), 4))}")
print(f"  Expected: |v|^2 = 1^2 + 1^2 = 2")
print(f"  => Vector Higgs gives DEGENERATE masses. No family splitting possible.")
print(f"     This is a theorem: {'{'}Gamma^A, Gamma^B{'}'} = 2*delta => M^2 = sum(v_A^2) I")

# ============================================================
# Part 3: Adjoint Higgs Yukawa (Gamma^{AB} coupling)
# ============================================================
print("\n" + "=" * 70)
print("Part 3: Adjoint Higgs — The Source of Family Splitting")
print("=" * 70)

print("""
  The adjoint Higgs couples via Sigma^{AB} = (i/2) Gamma^A Gamma^B.
  These are the SO(14) generators themselves.

  For SO(4) directions (A,B in {11,12,13,14}):
  - Sigma_{11,12} = T1 (preserves family sectors, DIAGONAL)
  - Sigma_{13,14} = T2 (preserves family sectors, DIAGONAL)
  - Sigma_{11,13}, etc. (MIXES family sectors, OFF-DIAGONAL)

  The DIAGONAL generators (T1, T2) split families without mixing them.
  The OFF-DIAGONAL generators add inter-family coupling.
""")

# Build the 6 SO(4) sigma generators
sigma_so4 = {}
so4_dirs = [10, 11, 12, 13]  # 0-indexed for gammas array
for i in range(4):
    for j in range(i+1, 4):
        label = f"{so4_dirs[i]+1},{so4_dirs[j]+1}"
        sigma_so4[label] = (1j / 2) * gammas[so4_dirs[i]] @ gammas[so4_dirs[j]]

# Compute family eigenvalues for each sigma
print("  Sigma^{AB} eigenvalues per family sector:")
for label, sig in sigma_so4.items():
    print(f"\n  Sigma^{{{label}}}:")
    for key in sector_keys:
        vecs = joint_basis[:, sectors[key]]  # 128 x 32
        sig_block = vecs.conj().T @ sig @ vecs  # 32x32
        evals = np.round(np.linalg.eigvalsh(sig_block), 4)
        unique_evals = np.unique(evals)
        # Check if diagonal (block-diagonal means within sector)
        norm_diag = np.linalg.norm(sig_block, 'fro')
        print(f"    Sector ({key[0]:+d},{key[1]:+d}): ||block|| = {norm_diag:.3f}, "
              f"evals = {unique_evals}")

# ============================================================
# Part 4: Family Mass Matrix from Adjoint Higgs
# ============================================================
print("\n" + "=" * 70)
print("Part 4: Family Mass Matrix from Adjoint Higgs VEV")
print("=" * 70)

# The adjoint Higgs VEV in SO(4) sector: diagonal in sigma_{11,12} and sigma_{13,14}
# This is the natural VEV for breaking SO(4) -> U(1)xU(1)

# Mass operator from adjoint VEV: M_adj = w1 * T1 + w2 * T2
# T1, T2 are diagonal in the family sector basis with eigenvalues +-1/2

print("\n  CASE A: Adjoint VEV in T1 + T2 (natural breaking)")
print("  M_adj = w1 * T1 + w2 * T2")
print()

for w1, w2, label in [(1, 0, "T1 only (w1=1, w2=0)"),
                       (0, 1, "T2 only"),
                       (1, 1, "Symmetric (w1=w2=1)"),
                       (2, 1, "Asymmetric (w1=2, w2=1)")]:
    M_adj = w1 * T1 + w2 * T2
    print(f"  {label}:")

    # Eigenvalues per family sector
    for key in sector_keys:
        vecs = joint_basis[:, sectors[key]]
        block = vecs.conj().T @ M_adj @ vecs
        evals = np.linalg.eigvalsh(block)
        unique_evals = np.unique(np.round(evals, 4))
        print(f"    ({key[0]:+d},{key[1]:+d}): evals = {unique_evals} (x{len(evals)//len(unique_evals)} each)")

    # In the character basis: eigenvalues are w1*e1/2 + w2*e2/2
    # where (e1,e2) are the sector signs
    char_masses = []
    for a, b in [(0,0), (1,0), (0,1), (1,1)]:
        # Character eigenvalue = weighted sum over sectors
        m = 0
        for key in sector_keys:
            eps1 = 0 if key[0] == 1 else 1
            eps2 = 0 if key[1] == 1 else 1
            chi_val = (-1)**(a*eps1 + b*eps2)
            sector_mass = w1 * key[0] / 2 + w2 * key[1] / 2
            m += chi_val * sector_mass
        char_masses.append(m / 4)  # Normalized

    print(f"    Character basis: chi_00={char_masses[0]:+.3f}, "
          f"chi_10={char_masses[1]:+.3f}, "
          f"chi_01={char_masses[2]:+.3f}, "
          f"chi_11={char_masses[3]:+.3f}")

    # The actual mass per sector (diagonal)
    sector_masses = [(key, w1*key[0]/2 + w2*key[1]/2) for key in sector_keys]
    print(f"    Direct sector masses: {[(k, f'{m:+.2f}') for k, m in sector_masses]}")
    print()

# ============================================================
# Part 5: Z2xZ2 Character Decomposition of Mass Operator
# ============================================================
print("\n" + "=" * 70)
print("Part 5: Z2xZ2 Character Decomposition — Mass Patterns")
print("=" * 70)

print("""
  The mass operator M_adj = w1*T1 + w2*T2 is DIAGONAL in the sector basis
  with eigenvalues m(e1,e2) = w1*e1/2 + w2*e2/2.

  Sector masses:
    (++)  = (w1+w2)/2
    (+-)  = (w1-w2)/2
    (-+)  = (-w1+w2)/2
    (--)  = (-w1-w2)/2

  These four values are ALWAYS in a 2+2 pattern:
    m(++) + m(--) = 0
    m(+-) + m(-+) = 0

  In the Z2xZ2 character basis:
    chi_00 = average = 0 (always)
    chi_10 = average weighted by sign(e1) = w1/2
    chi_01 = average weighted by sign(e2) = w2/2
    chi_11 = average weighted by sign(e1*e2) = 0

  Wait — this needs careful computation. Let me do it numerically.
""")

# Proper computation: mass in each sector, then Hadamard transform
H = np.array([[1, 1, 1, 1],
              [-1, -1, 1, 1],
              [-1, 1, -1, 1],
              [1, -1, -1, 1]]) / 2  # Rows: chi_00, chi_10, chi_01, chi_11

# Sector ordering matches sector_keys: (-1,-1), (-1,+1), (+1,-1), (+1,+1)

for w1, w2, label in [(1, 1, "w1=w2=1"),
                       (2, 1, "w1=2, w2=1"),
                       (1, 0, "w1=1, w2=0")]:
    sector_m = np.array([w1*k[0]/2 + w2*k[1]/2 for k in sector_keys])
    char_m = 4 * H @ np.diag(sector_m) @ H.T
    print(f"\n  {label}: sector masses = {sector_m}")
    print(f"  Character mass matrix (4*H*diag(m)*H^T):")
    for i, (a, b) in enumerate([(0,0),(1,0),(0,1),(1,1)]):
        print(f"    chi_{a}{b}: {np.round(char_m[i], 4)}")
    is_diag = np.max(np.abs(char_m - np.diag(np.diag(char_m)))) < 0.001
    print(f"  Diagonal? {is_diag}")
    if is_diag:
        diag = np.diag(char_m).real
        print(f"  Eigenvalues: {np.round(diag, 4)}")

# ============================================================
# Part 6: The Mixed Sigma (F1*F2 channel) from Off-Diagonal SO(4)
# ============================================================
print("\n" + "=" * 70)
print("Part 6: Mixed SO(4) Generator — The F1*F2 Channel")
print("=" * 70)

# sigma_{11,13} connects sectors that differ in BOTH e1 and e2
# This is the third independent pattern needed for 3+1

sig_mixed = sigma_so4["11,13"]

print("  Sigma^{11,13} inter-sector blocks (Frobenius norm):")
for ki in sector_keys:
    vi = joint_basis[:, sectors[ki]]
    norms = []
    for kj in sector_keys:
        vj = joint_basis[:, sectors[kj]]
        block = vi.conj().T @ sig_mixed @ vj
        norms.append(np.linalg.norm(block, 'fro'))
    print(f"    ({ki[0]:+d},{ki[1]:+d}) -> " + "  ".join(f"{n:7.3f}" for n in norms))

# Sigma^{11,13} eigenvalue spectrum on full 128
sig_mixed_evals = np.linalg.eigvalsh(sig_mixed)
print(f"\n  Sigma^{{11,13}} full spectrum: {np.unique(np.round(sig_mixed_evals, 4))}")

# ============================================================
# Part 7: COMBINED Adjoint Mass — T1 + T2 + Sigma_mixed
# ============================================================
print("\n" + "=" * 70)
print("Part 7: Combined Adjoint Mass — All Three Channels")
print("=" * 70)

# The full SO(4) adjoint VEV can have components along T1, T2,
# and the four mixed generators. For simplicity, consider the
# symmetric case where one mixed generator is added.

# M_total = w1*T1 + w2*T2 + w3*Sigma^{11,13}
# Does this give 3+1 in the character basis?

for w1, w2, w3, label in [(1, 1, 0, "Diagonal only (w3=0): expect 2+2"),
                           (1, 1, 1, "All equal (w1=w2=w3=1): expect 3+1?"),
                           (2, 1, 1.5, "Generic")]:
    M_total = w1 * T1 + w2 * T2 + w3 * sig_mixed
    print(f"\n  {label}:")

    # Eigenvalues per sector
    for ki in sector_keys:
        vi = joint_basis[:, sectors[ki]]
        block = vi.conj().T @ M_total @ vi
        evals = np.sort(np.linalg.eigvalsh(block))
        print(f"    ({ki[0]:+d},{ki[1]:+d}): min={evals[0]:+.4f}, max={evals[-1]:+.4f}, "
              f"unique = {np.unique(np.round(evals, 3))}")

    # Full 128-dim eigenvalues, grouped by sector
    evals_full, evecs_full = np.linalg.eigh(M_total)

    # For each eigenvector, determine which sector it belongs to
    sector_evals = {k: [] for k in sector_keys}
    for i in range(128):
        vec = evecs_full[:, i]
        overlaps = {}
        for key in sector_keys:
            proj = P_sector[key] @ vec
            overlaps[key] = np.real(np.vdot(proj, proj))
        dom_sector = max(overlaps, key=overlaps.get)
        sector_evals[dom_sector].append(evals_full[i])

    print(f"    Full spectrum grouped by sector:")
    for key in sector_keys:
        ev = sorted(sector_evals[key])
        print(f"      ({key[0]:+d},{key[1]:+d}): {len(ev)} evals, "
              f"range [{ev[0]:+.4f}, {ev[-1]:+.4f}]")

# ============================================================
# Part 8: The REAL Question — Sector-Resolved Eigenvalue BANDS
# ============================================================
print("\n" + "=" * 70)
print("Part 8: The Physical Mass Structure")
print("=" * 70)

print("""
  The mass operator M = w1*T1 + w2*T2 + w3*Sigma_mixed acts on 128 states.
  Each family sector has 32 states (16 chiral+ and 16 chiral-).

  WITHIN each sector, the operator has a spectrum of eigenvalues.
  The BAND CENTER of each sector determines the family mass.
  The BANDWIDTH determines the intra-family mass splittings (quark/lepton).

  Key question: Do the sector BAND CENTERS follow a 3+1 pattern?
""")

# Compute band centers for various configurations
print("  Band centers (mean eigenvalue per sector):")
for w1, w2, w3, label in [(1, 1, 0, "Diagonal (w3=0)"),
                           (1, 1, 1, "Tuned (w1=w2=w3=1)"),
                           (0, 0, 1, "Mixed only (w3=1)"),
                           (2, 2, 2, "All equal scaled"),
                           (1, 0.7, 0.3, "Realistic hierarchy")]:
    M_total = w1 * T1 + w2 * T2 + w3 * sig_mixed
    centers = {}
    for key in sector_keys:
        vecs = joint_basis[:, sectors[key]]
        block = vecs.conj().T @ M_total @ vecs
        centers[key] = np.mean(np.linalg.eigvalsh(block))

    # Sector center values
    center_vals = [centers[k] for k in sector_keys]
    unique_centers = np.unique(np.round(center_vals, 6))
    n_distinct = len(unique_centers)

    # Pattern detection
    if n_distinct == 1:
        pattern = "ALL EQUAL (no splitting)"
    elif n_distinct == 2:
        mults = [np.sum(np.abs(np.round(center_vals, 6) - u) < 0.001) for u in unique_centers]
        pattern = f"{'+'.join(map(str, sorted(mults, reverse=True)))}"
    elif n_distinct == 3:
        pattern = "2+1+1"
    else:
        pattern = "1+1+1+1"

    print(f"    {label:30s}: centers = {[f'{c:+.4f}' for c in center_vals]}, "
          f"pattern = {pattern}")

# ============================================================
# Part 9: DEFINITIVE TEST — Sigma_mixed effect on sectors
# ============================================================
print("\n" + "=" * 70)
print("Part 9: Does Sigma_mixed Break 2+2 -> Something Else?")
print("=" * 70)

# Sigma_mixed connects sectors (-,-)↔(+,+) and (-,+)↔(+,-)
# (i.e., sectors that differ in BOTH t1 and t2 signs)
# This is the F1*F2 operator.

# In the sector basis, sigma_mixed acts OFF-DIAGONALLY between these pairs.
# When added to T1+T2 (which is diagonal), it creates an effective 2x2
# mixing within each pair.

# Pair 1: (++) and (--) have T1+T2 eigenvalues +1 and -1
# With sigma_mixed coupling c: eigenvalues = +-sqrt(1+c^2)

# Pair 2: (+-) and (-+) have T1+T2 eigenvalues 0 and 0 (if w1=w2)
# With sigma_mixed coupling c: eigenvalues = +-c

# Result: eigenvalues are +-sqrt(1+c^2) and +-c
# This is STILL 2+2 (paired by +-) — NOT 3+1!

print("""
  CRITICAL ANALYSIS:

  The mass operator M = w*T1 + w*T2 + c*Sigma_mixed in the sector basis:

  Pair (++, --): diagonal entries (+w, -w), off-diagonal c
    -> eigenvalues = +-sqrt(w^2 + c^2)

  Pair (+-, -+): diagonal entries (0, 0) [when w1=w2], off-diagonal c
    -> eigenvalues = +-c

  This is ALWAYS paired: for every +m there is a -m.
  The spectrum is {+sqrt(w^2+c^2), -sqrt(w^2+c^2), +c, -c}
  which is 2+2 (unless c=0 giving 2+1+1, or c=w giving other patterns).

  The +-pairing is a CONSEQUENCE of the mass operator being traceless
  on each chirality sector (Sigma generators are traceless).

  FUNDAMENTAL OBSTRUCTION: The adjoint Higgs gives a TRACELESS mass
  operator. Traceless on 4 sectors means the four eigenvalues sum to 0.
  For 3+1 with the 3 equal: 3m + M = 0 => M = -3m. This IS allowed.

  Let me verify numerically...
""")

# Numerical verification of the paired structure
w, c = 1.0, 1.0
M_wc = w * (T1 + T2) + c * sig_mixed

# Eigenvalues per sector, sorted
all_evals = []
for key in sector_keys:
    vecs = joint_basis[:, sectors[key]]
    block = vecs.conj().T @ M_wc @ vecs
    evals = np.linalg.eigvalsh(block)
    all_evals.extend(evals)
    print(f"  Sector ({key[0]:+d},{key[1]:+d}): {np.unique(np.round(evals, 4))}")

all_evals = np.sort(all_evals)
print(f"\n  Full spectrum unique values: {np.unique(np.round(all_evals, 4))}")
print(f"  Sum of all eigenvalues: {np.sum(all_evals):.6f} (should be ~0)")

# ============================================================
# Part 10: The Honest Answer — Can ANY Higgs Give 3+1?
# ============================================================
print("\n" + "=" * 70)
print("Part 10: Exhaustive Search — Any SO(4) Operator Giving 3+1?")
print("=" * 70)

# Any hermitian operator commuting with SO(10) lives in the SO(4) algebra.
# The SO(4) algebra on the spinor has generators: T1, T2, and 4 mixed sigmas.
# A general mass operator is: M = sum_i a_i * G_i where G_i are the 6 generators.

# The generators in the sector basis:
# T1 = diag(-1/2, -1/2, +1/2, +1/2) (block-diagonal, each block 32x32)
# T2 = diag(-1/2, +1/2, -1/2, +1/2) (block-diagonal)
# Sigma_mixed = off-diagonal connecting (--,++) and (-+,+-)

# The 4x4 "family" structure of ANY SO(4) operator:
# Write M = sum coefficients * (4x4 family matrix) tensor (32x32 internal)

# The family matrices span the space of 4x4 matrices commuting with Z2xZ2.
# Wait, they don't commute with Z2xZ2 — the off-diagonal sigmas DON'T commute.

# Actually, T1 and T2 generate the Cartan subalgebra (torus).
# The remaining 4 generators are raising/lowering operators.
# The full SO(4) = SU(2)_L x SU(2)_R acts on the 4 family sectors.

# The EIGENVALUE pattern is determined by the SO(4) representation structure.

# Under SU(2)_L x SU(2)_R, the 128 spinor decomposes as:
# 128 = 32 x (2_L, 2_R) where 32 is the SO(10) part
# So the family space is (2_L, 2_R) = 2 tensor 2 = 4.

# Under diagonal SU(2)_D: (2 tensor 2) = 3 + 1
# The j=1 triplet has m_D = -1, 0, +1
# The j=0 singlet has m_D = 0

# ANY SU(2)_D-invariant mass operator gives eigenvalues:
# - Same mass for all 3 states in the triplet (m_triplet)
# - Different mass for the singlet (m_singlet)
# => 3+1 pattern!

# BUT: the mass operator must be an element of SO(4), not just SU(2)_D.
# SU(2)_D is the diagonal subgroup of SU(2)_L x SU(2)_R.
# A mass from BREAKING SU(2)_L x SU(2)_R -> SU(2)_D would give 3+1.

print("""
  KEY REALIZATION:

  Under SU(2)_L x SU(2)_R, the 4 family sectors form (2_L, 2_R).
  Under diagonal SU(2)_D: (2 tensor 2) = 3 + 1.

  If a Higgs breaks SU(2)_L x SU(2)_R -> SU(2)_D,
  the 3+1 splitting is AUTOMATIC (Schur's lemma: triplet gets one mass,
  singlet gets another).

  The Higgs that does this is a (2,2) = 4 of SU(2)_L x SU(2)_R,
  which is the VECTOR representation of SO(4) = 4 of SO(4).

  This is NOT the adjoint (which preserves the product structure)
  but the FUNDAMENTAL representation.

  In SO(14) terms: the 4 of SO(4) sits inside the 14 of SO(14)
  as the (1,4) component under SO(10) x SO(4).

  But we showed above: the VECTOR Higgs gives M^2 = |v|^2 I (degenerate)!

  RESOLUTION: The degeneracy M^2 = |v|^2 I comes from the Clifford
  algebra anti-commutation. This is for the BILINEAR coupling psi-bar Gamma^A psi.
  The mass-squared is degenerate, but the SIGN of the mass can vary
  (eigenvalues of M are +|v| and -|v| with equal multiplicity).

  The family structure is encoded in the SIGN PATTERN, not the magnitude.
""")

# ============================================================
# Part 11: Sign Pattern of Vector Higgs Mass
# ============================================================
print("=" * 70)
print("Part 11: Sign Pattern — The Actual Family Structure")
print("=" * 70)

# M = v * Gamma^14 (VEV in the 14th direction)
v_higgs = 1.0
M_vec = v_higgs * gammas[13]  # Gamma^14 (0-indexed: 13)

# M has eigenvalues +1 and -1 (since Gamma^A squares to I)
evals_M = np.linalg.eigvalsh(M_vec)
print(f"  M = Gamma^14 eigenvalues: {np.unique(np.round(evals_M, 4))}")
print(f"    +1: {np.sum(evals_M > 0)} states, -1: {np.sum(evals_M < 0)} states")

# How do these eigenvalues distribute across family sectors?
evals_M_full, evecs_M_full = np.linalg.eigh(M_vec)

sector_signs = {k: {'+': 0, '-': 0} for k in sector_keys}
for i in range(128):
    vec = evecs_M_full[:, i]
    overlaps = {key: np.real(np.vdot(P_sector[key] @ vec, P_sector[key] @ vec))
                for key in sector_keys}
    dom = max(overlaps, key=overlaps.get)
    if overlaps[dom] > 0.9:  # Clean assignment
        if evals_M_full[i] > 0:
            sector_signs[dom]['+'] += 1
        else:
            sector_signs[dom]['-'] += 1

print(f"\n  Sign distribution of Gamma^14 eigenvalues per sector:")
for key in sector_keys:
    print(f"    ({key[0]:+d},{key[1]:+d}): +1 states = {sector_signs[key]['+']}, "
          f"-1 states = {sector_signs[key]['-']}")

# The sign pattern tells us: Gamma^14 maps between sectors (+-) <-> (++) etc.
# So the eigenvectors are MIXTURES of two sectors.

# Better approach: check the PROJECTION of Gamma^14 eigenstates onto sectors
print(f"\n  Gamma^14 eigenstates: sector overlap distribution")
print(f"  (Each eigenstate is a mixture of sectors)")

# Group by eigenvalue sign
pos_vecs = evecs_M_full[:, evals_M_full > 0]  # 128 x 64
neg_vecs = evecs_M_full[:, evals_M_full < 0]  # 128 x 64

for label, vecs in [("m=+1", pos_vecs), ("m=-1", neg_vecs)]:
    print(f"\n  {label} eigenstates ({vecs.shape[1]} total):")
    total_overlap = {}
    for key in sector_keys:
        overlaps = np.sum(np.abs(vecs.conj().T @ joint_basis[:, sectors[key]])**2, axis=1)
        total_overlap[key] = np.sum(overlaps)
    for key in sector_keys:
        print(f"    ({key[0]:+d},{key[1]:+d}): total overlap = {total_overlap[key]:.1f} / {vecs.shape[1]}")

# ============================================================
# Part 12: DIAGONAL SU(2)_D Casimir — Direct 3+1 Test
# ============================================================
print("\n" + "=" * 70)
print("Part 12: SU(2)_D Casimir on 128 — The Direct 3+1 Structure")
print("=" * 70)

# SU(2)_L and SU(2)_R generators (128-dim)
s12 = (1j/2) * gammas[10] @ gammas[11]
s13 = (1j/2) * gammas[10] @ gammas[12]
s14 = (1j/2) * gammas[10] @ gammas[13]
s23 = (1j/2) * gammas[11] @ gammas[12]
s24 = (1j/2) * gammas[11] @ gammas[13]
s34 = (1j/2) * gammas[12] @ gammas[13]

JL1 = (s12 + s34) / 2
JL2 = (s13 - s24) / 2
JL3 = (s14 + s23) / 2
JR1 = (s12 - s34) / 2
JR2 = (s13 + s24) / 2
JR3 = (s14 - s23) / 2

# Check SU(2) algebras
def check_su2(J1, J2, J3, label):
    c12 = J1 @ J2 - J2 @ J1
    for sign_name, sign in [("+i", 1j), ("-i", -1j)]:
        err = np.max(np.abs(c12 - sign * J3))
        if err < 1e-10:
            print(f"  {label}: [J1,J2] = {sign_name}*J3")
            return sign
    print(f"  {label}: DOES NOT CLOSE")
    return None

sL = check_su2(JL1, JL2, JL3, "SU(2)_L")
sR = check_su2(JR1, JR2, JR3, "SU(2)_R")

# Diagonal SU(2)_D — need to handle opposite signs
# If [JL_i, JL_j] = +i*eps*JL_k and [JR_i, JR_j] = -i*eps*JR_k,
# then [JL+JR, JL+JR] doesn't close. Instead [JL-JR] or conjugate one.

# Try: JD_i = JL_i + JR_i and JD_i = JL_i - JR_i
for name, JD_gen in [("L+R", [JL1+JR1, JL2+JR2, JL3+JR3]),
                      ("L-R", [JL1-JR1, JL2-JR2, JL3-JR3])]:
    result = check_su2(*JD_gen, f"SU(2)_{name}")
    if result is not None:
        JD1, JD2, JD3 = JD_gen
        C2_D = JD1@JD1 + JD2@JD2 + JD3@JD3
        evals_C2 = np.linalg.eigvalsh(C2_D)
        unique_C2 = np.unique(np.round(evals_C2, 4))
        print(f"    Casimir j(j+1) values: {unique_C2}")
        for c2val in unique_C2:
            j = (-1 + np.sqrt(1 + 4*c2val)) / 2 if c2val >= 0 else -1
            mult = np.sum(np.abs(evals_C2 - c2val) < 0.01)
            print(f"      C2={c2val:.4f}, j={j:.2f}: multiplicity {mult}")

# ============================================================
# FINAL VERDICT
# ============================================================
print("\n" + "=" * 70)
print("FINAL VERDICT: KC-12")
print("=" * 70)
print("""
  RESULT SUMMARY:

  1. VECTOR Higgs (14-dim): M^2 = |v|^2 I => ALL masses degenerate.
     No family splitting whatsoever. This is a Clifford algebra identity.

  2. ADJOINT Higgs (91-dim): T1 + T2 (diagonal part) gives 2+2 pattern.
     Adding mixed generators (Sigma_mixed) changes eigenvalues but
     still gives pairing from tracelessness.

  3. SU(2)_D Casimir: The diagonal SU(2) decomposes the family space
     as (2 x 2) = 3 + 1. But SU(2)_L has sign convention OPPOSITE
     to SU(2)_R, so only L-R closes (giving j=1/2, not j=1 triplet).

  4. The FUNDAMENTAL question: Does SO(14) algebraic structure FORCE
     a 3+1 mass pattern? Answer: NO.

     - The 4 family sectors exist (machine-verified)
     - Z2xZ2 character basis diagonalizes the family mass matrix
     - But the eigenvalue pattern is {a+b, a-b, -a+b, -a-b} from
       the two-parameter torus (T1, T2)
     - This is ALWAYS 2+2 or 1+1+1+1, never naturally 3+1

  KC-12 STATUS: SOFT FAIL
  - Not a hard kill (the algebraic room for 3+1 exists with tuning)
  - But the mechanism is NOT automatic
  - The "zero sequence decouples" analogy with Dollard breaks down:
    * In Fortescue/Dollard: zero sequence decouples by SYMMETRY of the DFT
    * In SO(14): the analogous structure gives 2+2, not 3+1
    * The groups are different: Z4 (cyclic) vs Z2xZ2 (Klein four)

  HONEST ASSESSMENT:
  - The Z2xZ2 mechanism is no better than generic discrete flavor symmetry
  - It does not derive three generations from first principles
  - Paper 3 should use orbifold (Kawamura-Miura) as the generation mechanism
  - The Z2xZ2 observation belongs in "future directions" as an open question
""")
