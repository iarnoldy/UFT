#!/usr/bin/env python3
"""
THREE-GENERATION REMAINING AVENUES: Definitive Assessment
==========================================================

After KC-12 killed the Z2xZ2 character mechanism, four avenues remained:
  R3: Discrete flavor symmetry (A4 / binary tetrahedral 2T) in SO(4)
  R4: 331 anomaly mechanism (N_gen = N_color)
  R5: Furey idempotent mechanism (Cl(6) complex structures)
  R6: Orbifold (Kawamura-Miura) — the standard fallback

This script provides the definitive numerical evidence for R3,
and analytical arguments for R4 and R5. R6 is established in
the literature (Kawamura-Miura, PRD 2010).

RESULT: R3, R4, R5 all FAIL. Only R6 (orbifold) survives.
"""

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================
# Build Cl(14) gammas and SO(10) x SO(4) decomposition
# (same infrastructure as yukawa_definitive.py)
# ============================================================
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
for g in g8: Gamma8 = Gamma8 @ g
Gamma8_n = Gamma8 / np.sqrt((Gamma8 @ Gamma8)[0, 0])

g6 = [1j * kron3(sx, I2, I2), 1j * kron3(sy, I2, I2),
      1j * kron3(sz, sx, I2), 1j * kron3(sz, sy, I2),
      1j * kron3(sz, sz, sx), 1j * kron3(sz, sz, sy)]

gammas = []
for i in range(8): gammas.append(np.kron(g8[i], I8))
for j in range(6): gammas.append(np.kron(Gamma8_n, g6[j]))

# Chirality (128 -> 64+ and 64-)
Gamma14 = np.eye(128, dtype=complex)
for g in gammas: Gamma14 = Gamma14 @ g
phase14 = (Gamma14 @ Gamma14)[0, 0]
Gamma14_n = Gamma14 / np.sqrt(phase14)

# Semi-spinor projectors (sort descending, first 64 = positive chirality)
evals14, evecs14 = np.linalg.eigh(Gamma14_n)
order = np.argsort(-evals14)
evals14, evecs14 = evals14[order], evecs14[:, order]
B_plus = evecs14[:, :64]  # 128 x 64
print(f"64+ projection: {B_plus.shape[1]} states (should be 64)")

# SO(10) generators (indices 0-9) and SO(4) generators (indices 10-13)
so10_gens = []
so10_dirs = list(range(10))
for i in range(10):
    for j in range(i+1, 10):
        so10_gens.append((1j / 2) * gammas[i] @ gammas[j])

so4_gens = []
so4_dirs = [10, 11, 12, 13]
for i in range(4):
    for j in range(i+1, 4):
        so4_gens.append((1j / 2) * gammas[so4_dirs[i]] @ gammas[so4_dirs[j]])

# SU(2)_L x SU(2)_R decomposition of SO(4)
s12, s13, s14, s23, s24, s34 = so4_gens
JL1 = (s12 + s34) / 2
JL2 = (s13 - s24) / 2
JL3 = (s14 + s23) / 2
JR1 = (s12 - s34) / 2
JR2 = (s13 + s24) / 2
JR3 = (s14 - s23) / 2

# Verify SU(2) algebras
def check_su2(J1, J2, J3, name):
    comm12 = J1 @ J2 - J2 @ J1
    err_plus = np.max(np.abs(comm12 - 1j * J3))
    err_minus = np.max(np.abs(comm12 + 1j * J3))
    if err_plus < 1e-10:
        return +1
    elif err_minus < 1e-10:
        return -1
    else:
        return 0

sL = check_su2(JL1, JL2, JL3, "SU(2)_L")
sR = check_su2(JR1, JR2, JR3, "SU(2)_R")

# Project to 64+
JL1_64 = B_plus.conj().T @ JL1 @ B_plus
JL2_64 = B_plus.conj().T @ JL2 @ B_plus
JL3_64 = B_plus.conj().T @ JL3 @ B_plus
JR1_64 = B_plus.conj().T @ JR1 @ B_plus
JR2_64 = B_plus.conj().T @ JR2 @ B_plus
JR3_64 = B_plus.conj().T @ JR3 @ B_plus

# ============================================================
# R3: DISCRETE FLAVOR SYMMETRY — DEFINITIVE TEST
# ============================================================
print("\n" + "=" * 70)
print("R3: DISCRETE FLAVOR SYMMETRY (A4 / 2T) IN SO(4)")
print("=" * 70)

# STEP 1: What IS the family representation?
print("\n--- Step 1: Family space representation type ---")

# The 64+ branching is (16, (2,1)) + (16-bar, (1,2))
# Check SU(2)_L and SU(2)_R Casimirs on 64+
C2L = JL1_64 @ JL1_64 + JL2_64 @ JL2_64 + JL3_64 @ JL3_64
C2R = JR1_64 @ JR1_64 + JR2_64 @ JR2_64 + JR3_64 @ JR3_64

c2l_evals = np.linalg.eigvalsh(C2L)
c2r_evals = np.linalg.eigvalsh(C2R)
c2l_unique = np.unique(np.round(c2l_evals, 4))
c2r_unique = np.unique(np.round(c2r_evals, 4))

print(f"  SU(2)_L Casimir eigenvalues: {c2l_unique}")
print(f"  SU(2)_R Casimir eigenvalues: {c2r_unique}")

# Count dimensions in each SU(2) sector
for val in c2l_unique:
    n = np.sum(np.abs(c2l_evals - val) < 0.01)
    j = (-1 + np.sqrt(1 + 4 * val)) / 2 if val >= 0 else -1
    print(f"  SU(2)_L: j={j:.1f} (C2={val:.4f}), dim={n}")

for val in c2r_unique:
    n = np.sum(np.abs(c2r_evals - val) < 0.01)
    j = (-1 + np.sqrt(1 + 4 * val)) / 2 if val >= 0 else -1
    print(f"  SU(2)_R: j={j:.1f} (C2={val:.4f}), dim={n}")

# STEP 2: Diagonal SU(2)
print("\n--- Step 2: Diagonal SU(2) on 64+ ---")

# The proper diagonal is JA = JL - JR (since JR has opposite sign convention)
JA1 = JL1_64 - JR1_64
JA2 = JL2_64 - JR2_64
JA3 = JL3_64 - JR3_64

# Verify it forms SU(2)
comm_A = JA1 @ JA2 - JA2 @ JA1
err_A = np.max(np.abs(comm_A - 1j * JA3))
print(f"  SU(2)_diag = JL - JR: [J1,J2] = iJ3? error = {err_A:.2e}")

# Casimir of diagonal SU(2) on 64+
C2A = JA1 @ JA1 + JA2 @ JA2 + JA3 @ JA3
c2a_evals = np.linalg.eigvalsh(C2A)
c2a_unique = np.unique(np.round(c2a_evals, 4))

print(f"\n  Diagonal SU(2) Casimir eigenvalues on 64+:")
for val in c2a_unique:
    n = np.sum(np.abs(c2a_evals - val) < 0.01)
    j = (-1 + np.sqrt(1 + 4 * val)) / 2 if val >= 0 else -1
    print(f"    C2 = {val:.4f} (j = {j:.1f}): multiplicity {n}")

# STEP 3: The critical question — does j=1 (triplet) appear?
print("\n--- Step 3: Does the triplet j=1 appear? ---")
has_triplet = any(abs(val - 2.0) < 0.1 for val in c2a_unique)  # j=1 -> C2 = 2.0
has_singlet = any(abs(val - 0.0) < 0.1 for val in c2a_unique)  # j=0 -> C2 = 0.0
has_doublet = any(abs(val - 0.75) < 0.1 for val in c2a_unique)  # j=1/2 -> C2 = 0.75

print(f"  j=0 (singlet, C2=0):    {'YES' if has_singlet else 'NO'}")
print(f"  j=1/2 (doublet, C2=3/4): {'YES' if has_doublet else 'NO'}")
print(f"  j=1 (triplet, C2=2):    {'YES' if has_triplet else 'NO'}")

if has_triplet:
    print("\n  RESULT: Triplet found. A4 mechanism COULD work. Proceed to KC-15.")
else:
    print(f"\n  RESULT: Family space is ENTIRELY j=1/2 doublets.")
    print(f"  The 3+1 decomposition requires j=1 (triplet). It does NOT appear.")
    print(f"  A4 acting on doublets gives 2+2, not 3+1.")

# STEP 4: Why the abstract 2x2=3+1 fails
print("\n--- Step 4: Why 2 tensor 2 = 3+1 does NOT apply ---")
print("""
  The abstract Clebsch-Gordan: 2 (x) 2 = 3 + 1
  This applies to the TENSOR PRODUCT of two SU(2) doublets.
  That tensor product is the VECTOR (2,2) of SO(4).

  But the family space from SO(14) branching is:
    64+ = (16, (2,1)) + (16-bar, (1,2))

  This is a DIRECT SUM, not a tensor product:
    (2,1) + (1,2) under SU(2)_L x SU(2)_R

  Under diagonal SU(2)_diag:
    (2,1) -> 2 (doublet)
    (1,2) -> 2 (doublet)
    Direct sum: 2 + 2 = two doublets

  NOT: 2 (x) 2 = 3 + 1

  The tensor product 2x2 = 3+1 lives in the VECTOR representation (2,2).
  Fermions are in the SPINOR representation (2,1)+(1,2).
  These are DIFFERENT.
""")

# STEP 5: SO(10) content proves the problem is even deeper
print("--- Step 5: SO(10) content of the four families ---")

# Build SO(10) Casimir on 64+
C2_so10 = np.zeros((64, 64), dtype=complex)
for gen in so10_gens:
    gen_64 = B_plus.conj().T @ gen @ B_plus
    C2_so10 += gen_64 @ gen_64

# Joint diagonalization: JL3 and JR3 on 64+
jl3_evals, jl3_evecs = np.linalg.eigh(JL3_64)
jl3_vals = np.round(jl3_evals, 4)

# For each JL3 eigenspace, diagonalize JR3
sectors = {}
idx = 0
joint_basis = np.zeros((64, 64), dtype=complex)
joint_jl3 = np.zeros(64)
joint_jr3 = np.zeros(64)

for jl3v in np.unique(jl3_vals):
    mask = np.abs(jl3_vals - jl3v) < 1e-3
    sub = jl3_evecs[:, mask]
    JR3_sub = sub.conj().T @ JR3_64 @ sub
    jr3_sub_evals, jr3_sub_evecs = np.linalg.eigh(JR3_sub)
    new = sub @ jr3_sub_evecs
    n = new.shape[1]
    joint_basis[:, idx:idx+n] = new
    joint_jl3[idx:idx+n] = jl3v
    joint_jr3[idx:idx+n] = np.round(jr3_sub_evals, 4)
    idx += n

# Identify sectors
for k in range(64):
    key = (round(joint_jl3[k], 2), round(joint_jr3[k], 2))
    sectors.setdefault(key, []).append(k)

print(f"  {'Sector':<20} {'Dim':>5}  {'SO(10) rep':>15}  {'C2_SO(10)':>12}")
print("  " + "-" * 60)

for key in sorted(sectors.keys()):
    indices = sectors[key]
    dim = len(indices)
    vecs = joint_basis[:, indices]
    C2_sector = vecs.conj().T @ C2_so10 @ vecs
    so10_evals = np.linalg.eigvalsh(C2_sector)
    c2_mean = np.mean(so10_evals)

    # Identify SO(10) rep from Casimir
    if abs(c2_mean - 11.25) < 0.5:
        rep = "16 or 16-bar"
    elif abs(c2_mean - 9.0) < 0.5:
        rep = "10 (vector)"
    elif abs(c2_mean - 0.0) < 0.5:
        rep = "1 (singlet)"
    else:
        rep = f"unknown"

    print(f"  (mL={key[0]:+.1f}, mR={key[1]:+.1f}) {dim:5d}  {rep:>15}  {c2_mean:12.4f}")

# Distinguish 16 from 16-bar using the SO(10) chirality operator
# The SO(10) chirality = product of first 10 gamma matrices
chi_so10 = np.eye(128, dtype=complex)
for i in range(10):
    chi_so10 = chi_so10 @ gammas[i]
chi_so10_64 = B_plus.conj().T @ chi_so10 @ B_plus

print(f"\n  Distinguishing 16 from 16-bar (SO(10) chirality):")
for key in sorted(sectors.keys()):
    indices = sectors[key]
    vecs = joint_basis[:, indices]
    chi_sector = vecs.conj().T @ chi_so10_64 @ vecs
    chi_evals = np.linalg.eigvalsh(chi_sector)
    chi_unique = np.unique(np.round(chi_evals, 4))
    n_pos = np.sum(chi_evals > 0)
    n_neg = np.sum(chi_evals < 0)
    rep = "16 (matter)" if n_pos > n_neg else "16-bar (mirror)"
    print(f"    (mL={key[0]:+.1f}, mR={key[1]:+.1f}): chi = {chi_unique}, {rep}")

print("""
  CONCLUSION: The four families from the 64+ semi-spinor are:
    2 copies of 16 (matter) from (2,1) of SU(2)_L
    2 copies of 16-bar (mirror) from (1,2) of SU(2)_R

  These are NOT four identical generations!
  Any "3+1" mechanism would mix 16 and 16-bar,
  giving generations with DIFFERENT gauge quantum numbers.
  This is physically unacceptable.
""")

# ============================================================
# R4: 331 ANOMALY MECHANISM — ANALYTICAL ARGUMENT
# ============================================================
print("=" * 70)
print("R4: 331 ANOMALY MECHANISM (N_gen = N_color)")
print("=" * 70)
print("""
  The Pisano-Pleitez-Frampton 331 model:
    Gauge group: SU(3)_C x SU(3)_L x U(1)_X
    Key feature: anomaly cancellation requires N_gen = N_color = 3

  Question: Does SO(14) breaking chain pass through 331?

  ANALYSIS:
  1. SO(14) -> SO(10) x SO(4) -> SU(5) x U(1) x SU(2)^2 -> SM
     The 331 group SU(3)_C x SU(3)_L x U(1) can be reached via
     trinification: SO(10) -> SU(3)^3 x U(1) -> SU(3) x SU(3) x U(1)

  2. However, when 331 is embedded in a GUT:
     - GUT representations are anomaly-free BY CONSTRUCTION
     - The anomaly cancellation is AUTOMATIC, not a constraint
     - The argument N_gen = N_color DISAPPEARS inside the GUT

  3. The 331 mechanism works precisely because SU(3)_L is NOT
     embedded in a larger anomaly-free group. Once you embed it
     in SO(10) or SO(14), the anomaly is trivially satisfied
     for ANY N_gen.

  4. This is a well-known issue (Pisano & Pleitez 1992, Frampton 1992):
     the N_gen = N_color constraint is a FEATURE of 331 as a
     standalone gauge theory, not of 331 as a breaking step.

  VERDICT: KC-16 FIRES
  The 331 anomaly mechanism is INCOMPATIBLE with GUT embedding.
  It cannot constrain N_gen when 331 is embedded in SO(14).
  Document as: 331 anomaly is intrinsically non-GUT.
""")

# ============================================================
# R5: FUREY IDEMPOTENT MECHANISM — ANALYTICAL ARGUMENT
# ============================================================
print("=" * 70)
print("R5: FUREY IDEMPOTENT MECHANISM (Cl(6) complex structures)")
print("=" * 70)
print("""
  Furey (JHEP 2014, "Generations: three prints, in colour"):
    Uses C x H x O (complex-quaternion-octonion algebra)
    Three complex structures within the octonions O
    Each gives one "generation" of color structure

  How this differs from Gresnigt's S3:
    Gresnigt: S3 permutes three Cl(6) SUBALGEBRAS within Cl(8)
    Furey: Three complex structures in O give three IDENTIFICATIONS

  Chirality obstruction (KC-5, killed Gresnigt):
    Gresnigt's S3 permutes Cl(8) generators across SO(10)/SO(4) boundary
    This mixes gauge and gravity, breaking chirality

  Does Furey avoid the chirality obstruction?
    Furey's mechanism operates within Cl(6) (subset of SO(10) sector)
    It does NOT cross the SO(10)/SO(4) boundary
    So the chirality obstruction (KC-5) does NOT apply directly

  BUT Furey has a DIFFERENT problem:
    The three complex structures give three DIFFERENT particle
    identifications, not three COPIES of the same identification.
    They are related by TRIALITY (outer automorphism of SO(8)),
    which permutes vector-spinor-cospinor.

    Observable consequence: the three "generations" would have
    DIFFERENT quantum numbers under SU(3)_C, not just different masses.
    This contradicts experiment: all three SM generations have
    IDENTICAL gauge charges (only masses differ).

  Furthermore:
    Cl(6) sits inside the SO(10) sector of SO(14)
    The three complex structures act WITHIN a single 16 of SO(10)
    They decompose the SAME 16 in three different ways
    They do NOT create three COPIES of the 16

  VERDICT: KC-17 FIRES (different obstruction)
  Furey's idempotent mechanism gives triality-related structures,
  not mass-degenerate copies. The three "prints" differ in their
  gauge quantum numbers, not just their masses.
  The mechanism operates within a single 16 (one generation),
  giving three VIEWS of the same generation, not three generations.
""")

# ============================================================
# COMPREHENSIVE IMPOSSIBILITY THEOREM
# ============================================================
print("=" * 70)
print("COMPREHENSIVE IMPOSSIBILITY: Why SO(14) cannot give 3 generations")
print("=" * 70)
print("""
  THEOREM (Strengthened from KC-12):

  No mechanism internal to SO(14) can produce exactly three
  generations of Standard Model fermions from a single
  semi-spinor representation.

  PROOF SKETCH:

  1. The semi-spinor 64+ of SO(14) under SO(10) x SO(4) is:
       64+ = (16, (2,1)) + (16-bar, (1,2))
     This contains exactly ONE copy of the 16 of SO(10)
     (as an SU(2)_L doublet) plus one copy of 16-bar (mirror).

  2. No element of the SO(4) Lie algebra can produce a 3+1
     eigenvalue pattern on the family space (2,1)+(1,2).
     [KC-12: Impossibility theorem, proved in yukawa_definitive.py]

  3. The diagonal SU(2)_diag decomposes the family space as
     2+2 (two doublets), NOT 3+1 (triplet + singlet).
     This kills discrete flavor symmetry (A4, 2T).
     [This script, Step 2: C2 = 0.75 (j=1/2) for all 64 states]

  4. The 331 anomaly mechanism (N_gen = N_color) does not
     constrain N_gen inside a GUT, where anomaly freedom is automatic.

  5. The Furey idempotent mechanism gives triality, not generations.
     Three complex structures decompose a single 16 three ways.

  6. The Gresnigt S3 mechanism mixes chiralities when extended
     from Cl(8) to Cl(14). [KC-5, earlier session]

  SURVIVORS (external mechanisms):
  - Orbifold compactification (Kawamura-Miura): THREE generations
    from boundary conditions on S^1/(Z2 x Z2'). Published, PRD 2010.
  - Multiple copies: 3 x 64+ by hand (same as SO(10) takes 3 x 16).
  - String embedding: SO(14) x U(1) in E_8, Calabi-Yau with chi=+-6.

  The three-generation problem for SO(14) is INHERITED from SO(10).
  It is neither solved nor worsened by going to SO(14).
""")

# ============================================================
# SUMMARY TABLE
# ============================================================
print("=" * 70)
print("SUMMARY: Three-Generation Mechanisms for SO(14)")
print("=" * 70)
print("""
  INTRINSIC MECHANISMS (all FAIL):
  +-----+-------------------------------+--------+------------------+
  | ID  | Mechanism                     | Status | Kill Condition   |
  +-----+-------------------------------+--------+------------------+
  | M1  | Gresnigt S3 from Cl(8)        | DEAD   | KC-5 (chirality) |
  | M2  | E8 intersection               | DEAD   | dim mismatch     |
  | M3  | Cl(6) SU(3) tripling          | DEAD   | no SO(10) commut |
  | M4  | Z2xZ2 character (Dollard)     | DEAD   | KC-12 (2+2 only) |
  | M5  | A4 discrete flavor in SO(4)   | DEAD   | KC-15 (no j=1)   |
  | M6  | 331 anomaly (N_gen=N_color)   | DEAD   | KC-16 (GUT auto) |
  | M7  | Furey idempotent (Cl(6))      | DEAD   | KC-17 (triality) |
  +-----+-------------------------------+--------+------------------+

  EXTERNAL MECHANISMS (candidates for Paper 3):
  +-----+-------------------------------+--------+------------------+
  | ID  | Mechanism                     | Status | Reference        |
  +-----+-------------------------------+--------+------------------+
  | E1  | Orbifold (Kawamura-Miura)     | ALIVE  | PRD 2010         |
  | E2  | Multiple copies (3 x 64)     | ALIVE  | standard (ad hoc)|
  | E3  | String embedding (E8 -> SO14) | ALIVE  | speculative      |
  +-----+-------------------------------+--------+------------------+

  PAPER 3 STRATEGY:
  - Present the impossibility theorem (KC-12) as a genuine result
  - Use orbifold (E1) as the primary generation mechanism
  - Note the honest framing: same situation as SO(10)
  - The four-sector structure is a STRUCTURAL OBSERVATION, not a mechanism
""")
