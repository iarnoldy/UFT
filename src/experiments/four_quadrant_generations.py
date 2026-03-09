#!/usr/bin/env python3
"""
Four-Quadrant Three-Generation Mechanism for SO(14)
====================================================

The abstract argument:
  SO(14) → SO(10) × SO(4) gives 64+ = (16, 2, 1) + (16-bar, 1, 2)
  SO(4) = SU(2)_L × SU(2)_R
  Under diagonal SU(2)_D: 2 ⊗ 2 = 3 ⊕ 1

  If the four fermion sectors organize as a bi-fundamental,
  the diagonal SU(2)_D splits them as 3 + 1.

  Three generations = triplet of diagonal SU(2)
  Fourth mode = singlet (zero sequence / common mode)

This is the Dollard connection:
  Four-quadrant (u,v,x,y) → three non-trivial Z4 characters + one trivial
  Fortescue N=4: three non-trivial sequences + zero sequence

We test whether this abstract pattern is realized in the concrete
representation theory of SO(14).
"""

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================
# Part 1: Abstract SU(2) × SU(2) → diagonal SU(2)
# ============================================================
print("=" * 60)
print("Part 1: 2 ⊗ 2 = 3 ⊕ 1 (Clebsch-Gordan)")
print("=" * 60)

# SU(2) generators in fundamental (2-dim) representation
J1 = np.array([[0, 1], [1, 0]], dtype=complex) / 2
J2 = np.array([[0, -1j], [1j, 0]], dtype=complex) / 2
J3 = np.array([[1, 0], [0, -1]], dtype=complex) / 2
I2 = np.eye(2, dtype=complex)

# SU(2)_L × SU(2)_R generators on 2 ⊗ 2 = 4-dim space
# L_i = J_i ⊗ I, R_i = I ⊗ J_i
L1, L2, L3 = np.kron(J1, I2), np.kron(J2, I2), np.kron(J3, I2)
R1, R2, R3 = np.kron(I2, J1), np.kron(I2, J2), np.kron(I2, J3)

# Diagonal SU(2)_D: D_i = L_i + R_i
D1, D2, D3 = L1 + R1, L2 + R2, L3 + R3

# Casimir of diagonal SU(2)_D
C2_D = D1 @ D1 + D2 @ D2 + D3 @ D3
evals_D, evecs_D = np.linalg.eigh(C2_D)
print(f"  Diagonal SU(2) Casimir eigenvalues: {np.round(evals_D, 4)}")
print(f"  j(j+1) = 0 → j=0 (singlet), j(j+1) = 2 → j=1 (triplet)")

# D3 eigenvalues on the triplet
D3_evals = np.linalg.eigvalsh(D3)
print(f"  D3 eigenvalues: {np.sort(D3_evals)}")
print(f"  Triplet: m = -1, 0, +1 (three generations)")
print(f"  Singlet: m = 0 (zero mode / fourth quadrant)")

# Identify the triplet and singlet states
singlet_mask = np.abs(evals_D) < 0.01
triplet_mask = np.abs(evals_D - 2.0) < 0.01
print(f"\n  Singlet (j=0): {np.sum(singlet_mask)} state(s)")
print(f"  Triplet (j=1): {np.sum(triplet_mask)} state(s)")
print(f"  Total: {np.sum(singlet_mask) + np.sum(triplet_mask)} (should be 4)")

# The Clebsch-Gordan basis
# |j=1, m=1⟩ = |+⟩|+⟩
# |j=1, m=0⟩ = (|+⟩|-⟩ + |-⟩|+⟩)/√2
# |j=1, m=-1⟩ = |-⟩|-⟩
# |j=0, m=0⟩ = (|+⟩|-⟩ - |-⟩|+⟩)/√2  (antisymmetric = singlet)

# ============================================================
# Part 2: The Dollard Four-Quadrant Map
# ============================================================
print("\n" + "=" * 60)
print("Part 2: Dollard's Four-Quadrant ↔ SU(2) × SU(2)")
print("=" * 60)

# Dollard's four quadrants via Z4 characters:
# χ_0(k) = 1    for all k  (zero sequence)
# χ_1(k) = j^k               (positive sequence)
# χ_2(k) = (-1)^k             (alternating sequence)
# χ_3(k) = (-j)^k             (negative sequence)

# The Z4 DFT matrix:
j = 1j
omega = np.exp(2j * np.pi / 4)  # = j
F4 = np.array([
    [1, 1, 1, 1],
    [1, omega, omega**2, omega**3],
    [1, omega**2, omega**4, omega**6],
    [1, omega**3, omega**6, omega**9],
]) / 2

print("  Z4 DFT matrix (Fortescue for N=4):")
print(f"  {np.round(F4, 4)}")

# The four sequences:
# Sequence 0 (zero): trivial character, sum of all
# Sequence 1 (positive): phase rotation by j
# Sequence 2 (alternating): phase rotation by -1
# Sequence 3 (negative): phase rotation by -j

# Map to Dollard's operators:
# u = (1/4)(χ0 + χ1 + χ2 + χ3)  -- all add constructively at k=0
# v = (1/4)(χ0 - χ1 + χ2 - χ3)  -- alternating signs at k=0
# x, y similar

# The KEY: under the Z2 subgroup {χ0, χ2} vs {χ1, χ3}:
# Even characters: χ0 (zero), χ2 (alternating) → cos, cosh (REAL)
# Odd characters: χ1 (positive), χ3 (negative) → sin, sinh (IMAGINARY)

print("\n  Character table Z4:")
print("  k=0  k=1  k=2  k=3")
for n in range(4):
    chars = [omega**(n*k) for k in range(4)]
    label = ["zero", "positive", "alternating", "negative"][n]
    print(f"  χ_{n} ({label:11s}): " + "  ".join(f"{c:+.0f}" if c.imag == 0 else f"{c:+.0f}" for c in chars))

print(f"\n  Non-trivial characters: χ₁, χ₂, χ₃ (three of them)")
print(f"  Trivial character: χ₀ (zero sequence)")
print(f"  4 - 1 = 3: THREE non-trivial sequences")

# ============================================================
# Part 3: Connecting to SO(14) representation theory
# ============================================================
print("\n" + "=" * 60)
print("Part 3: SO(14) four sectors → 3+1 decomposition")
print("=" * 60)

# Build Cl(14) = Cl(8) ⊗ Cl(6) as before
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
I8 = np.eye(8, dtype=complex)
I16 = np.eye(16, dtype=complex)
I128 = np.eye(128, dtype=complex)

def kron3(a, b, c): return np.kron(a, np.kron(b, c))
def kron4(a, b, c, d): return np.kron(a, np.kron(b, np.kron(c, d)))

# Cl(8): 16x16
g8 = [1j * kron4(sx, I2, I2, I2), 1j * kron4(sy, I2, I2, I2),
      1j * kron4(sz, sx, I2, I2), 1j * kron4(sz, sy, I2, I2),
      1j * kron4(sz, sz, sx, I2), 1j * kron4(sz, sz, sy, I2),
      1j * kron4(sz, sz, sz, sx), 1j * kron4(sz, sz, sz, sy)]

Gamma8 = np.eye(16, dtype=complex)
for g in g8:
    Gamma8 = Gamma8 @ g
phase8 = (Gamma8 @ Gamma8)[0, 0]
Gamma8_n = Gamma8 / np.sqrt(phase8)

# Cl(6): 8x8
g6 = [1j * kron3(sx, I2, I2), 1j * kron3(sy, I2, I2),
      1j * kron3(sz, sx, I2), 1j * kron3(sz, sy, I2),
      1j * kron3(sz, sz, sx), 1j * kron3(sz, sz, sy)]

# Cl(14): 128x128
gammas14 = []
for i in range(8):
    gammas14.append(np.kron(g8[i], I8))
for j in range(6):
    gammas14.append(np.kron(Gamma8_n, g6[j]))

# Chirality
Gamma14 = np.eye(128, dtype=complex)
for g in gammas14:
    Gamma14 = Gamma14 @ g
phase14 = (Gamma14 @ Gamma14)[0, 0]
Gamma14_n = Gamma14 / np.sqrt(phase14)

# Semi-spinor projectors
evals14, evecs14 = np.linalg.eigh(Gamma14_n)
order = np.argsort(-evals14)
evals14, evecs14 = evals14[order], evecs14[:, order]
B_plus = evecs14[:, :64]   # 128 x 64

# SO(10) generators: directions 1-10
so10_gens = []
for i in range(10):
    for j in range(i + 1, 10):
        so10_gens.append((1j / 2) * gammas14[i] @ gammas14[j])

# SO(4) generators: directions 11-14 (indices 10-13 in gammas14)
so4_indices = [10, 11, 12, 13]
so4_gens = []
for i in range(4):
    for j in range(i + 1, 4):
        so4_gens.append((1j / 2) * gammas14[so4_indices[i]] @ gammas14[so4_indices[j]])

print(f"  SO(10): {len(so10_gens)} generators, SO(4): {len(so4_gens)} generators")

# Project SO(4) to 64+
so4_64 = [B_plus.conj().T @ g @ B_plus for g in so4_gens]

# Identify SU(2)_L × SU(2)_R within SO(4)
# SO(4) generators σ_{ij} for i,j ∈ {11,12,13,14}:
# σ12, σ13, σ14, σ23, σ24, σ34
# SU(2)_L = (σ12 + σ34)/2, (σ13 - σ24)/2, (σ14 + σ23)/2
# SU(2)_R = (σ12 - σ34)/2, (σ13 + σ24)/2, (σ14 - σ23)/2

# Map: so4_gens indices: (10,11)=σ12, (10,12)=σ13, (10,13)=σ14,
#                         (11,12)=σ23, (11,13)=σ24, (12,13)=σ34

s12, s13, s14, s23, s24, s34 = so4_64

JL1 = (s12 + s34) / 2
JL2 = (s13 - s24) / 2
JL3 = (s14 + s23) / 2

JR1 = (s12 - s34) / 2
JR2 = (s13 + s24) / 2
JR3 = (s14 - s23) / 2

# Verify SU(2) algebras
def check_su2(J1, J2, J3, label):
    c12 = J1 @ J2 - J2 @ J1
    err = np.max(np.abs(c12 - 1j * J3))
    err2 = np.max(np.abs(c12 + 1j * J3))
    if err < 1e-10:
        print(f"  {label}: [J1,J2] = +iJ3 (err={err:.2e})")
        return 1
    elif err2 < 1e-10:
        print(f"  {label}: [J1,J2] = -iJ3 (err={err2:.2e})")
        return -1
    else:
        print(f"  {label}: [J1,J2] ≠ ±iJ3 (errs={err:.2e}, {err2:.2e})")
        return 0

sL = check_su2(JL1, JL2, JL3, "SU(2)_L")
sR = check_su2(JR1, JR2, JR3, "SU(2)_R")

# Cross-check: [L, R] = 0
cross = max(np.max(np.abs(JL1 @ JR1 - JR1 @ JL1)),
            np.max(np.abs(JL2 @ JR2 - JR2 @ JL2)),
            np.max(np.abs(JL3 @ JR3 - JR3 @ JL3)))
print(f"  [SU(2)_L, SU(2)_R] max = {cross:.2e}")

# Casimirs
C2L = JL1 @ JL1 + JL2 @ JL2 + JL3 @ JL3
C2R = JR1 @ JR1 + JR2 @ JR2 + JR3 @ JR3

c2l_evals = np.linalg.eigvalsh(C2L)
c2r_evals = np.linalg.eigvalsh(C2R)
print(f"\n  SU(2)_L Casimir on 64+: {np.unique(np.round(c2l_evals, 4))}")
print(f"  SU(2)_R Casimir on 64+: {np.unique(np.round(c2r_evals, 4))}")

# ============================================================
# Part 4: THE KEY COMPUTATION - Diagonal SU(2)_D on 64+
# ============================================================
print("\n" + "=" * 60)
print("Part 4: Diagonal SU(2)_D = SU(2)_L + SU(2)_R on 64+")
print("=" * 60)

# Diagonal generators
if sL == sR:
    JD1 = JL1 + JR1
    JD2 = JL2 + JR2
    JD3 = JL3 + JR3
else:
    # If signs differ, need to flip one set for consistent convention
    JD1 = JL1 + JR1
    JD2 = JL2 + JR2
    JD3 = JL3 + JR3
    # Check if diagonal closes
    check_su2(JD1, JD2, JD3, "SU(2)_D (L+R)")
    # Try anti-diagonal
    JD1a = JL1 - JR1
    JD2a = JL2 - JR2
    JD3a = JL3 - JR3
    check_su2(JD1a, JD2a, JD3a, "SU(2)_D (L-R)")

# Diagonal Casimir
C2D = JD1 @ JD1 + JD2 @ JD2 + JD3 @ JD3
c2d_evals = np.linalg.eigvalsh(C2D)
c2d_unique = np.unique(np.round(c2d_evals, 4))
print(f"\n  Diagonal SU(2)_D Casimir on 64+:")
for val in c2d_unique:
    mult = np.sum(np.abs(c2d_evals - val) < 0.01)
    j = (-1 + np.sqrt(1 + 4 * val)) / 2 if val >= 0 else -1
    print(f"    C2 = {val:.4f} (j = {j:.1f}): multiplicity {mult}")

# D3 eigenvalues
d3_evals = np.linalg.eigvalsh(JD3)
d3_unique = np.unique(np.round(d3_evals, 4))
print(f"\n  D3 eigenvalues on 64+:")
for val in d3_unique:
    mult = np.sum(np.abs(d3_evals - val) < 0.01)
    print(f"    m = {val:+.4f}: multiplicity {mult}")

# ============================================================
# Part 5: Does SU(2)_D commute with SO(10)?
# ============================================================
print("\n" + "=" * 60)
print("Part 5: [SU(2)_D, SO(10)] = ?")
print("=" * 60)

JD_128 = [JL1 + JR1, JL2 + JR2, JL3 + JR3]
# Wait, these are on 64+. Need 128-dim versions.
JD_128 = []
for g in so4_gens:
    pass  # Need to redo in 128-dim

# Actually, work in 128-dim first, then project
s12_128 = so4_gens[0]
s13_128 = so4_gens[1]
s14_128 = so4_gens[2]
s23_128 = so4_gens[3]
s24_128 = so4_gens[4]
s34_128 = so4_gens[5]

JL1_128 = (s12_128 + s34_128) / 2
JL2_128 = (s13_128 - s24_128) / 2
JL3_128 = (s14_128 + s23_128) / 2
JR1_128 = (s12_128 - s34_128) / 2
JR2_128 = (s13_128 + s24_128) / 2
JR3_128 = (s14_128 - s23_128) / 2

JD1_128 = JL1_128 + JR1_128
JD2_128 = JL2_128 + JR2_128
JD3_128 = JL3_128 + JR3_128

max_comm = 0
for gen in so10_gens:
    for JD in [JD1_128, JD2_128, JD3_128]:
        c = np.max(np.abs(JD @ gen - gen @ JD))
        max_comm = max(max_comm, c)

print(f"  max |[SU(2)_D, SO(10)]| = {max_comm:.2e}")

if max_comm < 1e-10:
    print("  >>> SU(2)_D COMMUTES with SO(10) <<<")
    print("  >>> This is a genuine family symmetry! <<<")
else:
    print("  >>> SU(2)_D does NOT commute with SO(10) <<<")

# Also check: does the anti-diagonal SU(2)_A = L - R commute?
JA1_128 = JL1_128 - JR1_128
JA2_128 = JL2_128 - JR2_128
JA3_128 = JL3_128 - JR3_128

max_comm_A = 0
for gen in so10_gens:
    for JA in [JA1_128, JA2_128, JA3_128]:
        c = np.max(np.abs(JA @ gen - gen @ JA))
        max_comm_A = max(max_comm_A, c)

print(f"  max |[SU(2)_A, SO(10)]| = {max_comm_A:.2e}")

# ============================================================
# Part 6: SO(10) content of the 3+1 sectors
# ============================================================
print("\n" + "=" * 60)
print("Part 6: SO(10) content of diagonal SU(2)_D sectors on 64+")
print("=" * 60)

# Build SO(10) Casimir on 64+
C2_so10 = np.zeros((64, 64), dtype=complex)
for gen in so10_gens:
    gen_64 = B_plus.conj().T @ gen @ B_plus
    C2_so10 += gen_64 @ gen_64

# Joint diagonalization: C2D and C2_so10
# Check if they commute
comm_casimirs = np.max(np.abs(C2D @ C2_so10 - C2_so10 @ C2D))
print(f"  [C2_D, C2_SO(10)] = {comm_casimirs:.2e}")

# Diagonalize C2D, then check SO(10) content in each sector
c2d_evals_full, c2d_evecs = np.linalg.eigh(C2D)

for c2d_val in c2d_unique:
    mask = np.abs(c2d_evals_full - c2d_val) < 0.01
    dim = np.sum(mask)
    j = (-1 + np.sqrt(1 + 4 * c2d_val)) / 2 if c2d_val >= 0 else -1

    sector_basis = c2d_evecs[:, mask]
    C2_sector = sector_basis.conj().T @ C2_so10 @ sector_basis
    so10_evals = np.linalg.eigvalsh(C2_sector)
    so10_unique = np.unique(np.round(so10_evals, 2))

    print(f"\n  j_D = {j:.1f} sector (dim={dim}):")
    for so10_val in so10_unique:
        mult = np.sum(np.abs(so10_evals - so10_val) < 0.1)
        # Identify SO(10) rep: 16 has C2 = 45/4 = 11.25, 10 has C2 = 9, etc.
        if abs(so10_val - 11.25) < 0.5:
            rep = "16/16-bar (spinor)"
        elif abs(so10_val - 9.0) < 0.5:
            rep = "10 (vector)"
        elif abs(so10_val - 0.0) < 0.5:
            rep = "1 (singlet)"
        elif abs(so10_val - 18.0) < 0.5:
            rep = "45 (adjoint)"
        else:
            rep = f"unknown (C2={so10_val:.2f})"
        print(f"    C2_SO(10) = {so10_val:.2f} [{rep}]: x{mult}")

# ============================================================
# Part 7: The Z4 / Fortescue interpretation
# ============================================================
print("\n" + "=" * 60)
print("Part 7: Z4 Character / Fortescue Interpretation")
print("=" * 60)

# The Z4 subgroup of SO(4) is generated by a specific element
# In SU(2)_L × SU(2)_R, consider the Z4 generated by
# exp(2πi J3_L / 2) × exp(2πi J3_R / 2)
# or equivalently, the eigenvalues of J3_L + J3_R (mod integers)

# Use JL3 + JR3 = JD3 (the diagonal J3)
# and JL3 - JR3 = JA3 (the anti-diagonal J3)
# Together they give the full torus of SO(4)

JA3_64 = B_plus.conj().T @ JA3_128 @ B_plus

# Joint eigenvalues of (JD3, JA3) label the four sectors
jd3_evals_64, jd3_evecs = np.linalg.eigh(JD3 if isinstance(JD3, np.ndarray) and JD3.shape == (64,64) else B_plus.conj().T @ JD3_128 @ B_plus)
ja3_evals_64 = np.diag(jd3_evecs.conj().T @ JA3_64 @ jd3_evecs).real

print("  Joint (m_D, m_A) spectrum on 64+:")
pairs = {}
for k in range(64):
    pair = (round(jd3_evals_64[k], 2), round(ja3_evals_64[k], 2))
    pairs[pair] = pairs.get(pair, 0) + 1

for (md, ma), mult in sorted(pairs.items()):
    # Map to Dollard quadrants
    if md > 0 and ma > 0:
        quad = "I (u: cos+cosh)"
    elif md > 0 and ma < 0:
        quad = "II (x: sin+sinh)"
    elif md < 0 and ma > 0:
        quad = "III (y: -sin+sinh)"
    elif md < 0 and ma < 0:
        quad = "IV (v: -cos+cosh)"
    elif md == 0 and ma == 0:
        quad = "CENTER (zero sequence)"
    elif md == 0:
        quad = "D-neutral"
    elif ma == 0:
        quad = "A-neutral"
    else:
        quad = "other"
    print(f"    (m_D={md:+.1f}, m_A={ma:+.1f}): x{mult}  [{quad}]")

# ============================================================
# VERDICT
# ============================================================
print("\n" + "=" * 60)
print("VERDICT: Four-Quadrant → Three-Generation Mechanism")
print("=" * 60)
print("""
  ABSTRACT ARGUMENT:
    SO(4) = SU(2)_L × SU(2)_R gives 4 fermion sectors in 64+
    Under diagonal SU(2)_D: 2 ⊗ 2 = 3 ⊕ 1
    Triplet (j=1) = three generations
    Singlet (j=0) = zero mode / fourth quadrant (decoupled)

  DOLLARD CONNECTION:
    Four-quadrant (u,v,x,y) = Z4 character decomposition
    Z4 has 4 characters: 1 trivial + 3 non-trivial
    Fortescue N=4: zero sequence + positive + negative + alternating
    The zero sequence always decouples (no net contribution)

  PHYSICAL INTERPRETATION:
    If SO(4) → diagonal SU(2)_D via symmetry breaking,
    the singlet (zero mode) gets a DIFFERENT mass from the triplet.
    If the singlet is heavy: 3 light generations remain.
    If the singlet is light: it's a sterile/dark sector.

  See numerical results above for the actual SO(10) content
  of the triplet vs singlet sectors.
""")
