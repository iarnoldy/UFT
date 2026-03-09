#!/usr/bin/env python3
"""
KC-12 DEFINITIVE TEST: Can SO(4) algebra produce 3+1 mass pattern?
===================================================================

From v2 we learned:
- Vector Higgs: M^2 = |v|^2 I (degenerate, no splitting)
- Adjoint Higgs: T1+T2 gives 2+1+1 sector pattern
- Mixed sigma connects (--,++) and (-+,+-) pairs

The general SO(4) mass operator has 4x4 block structure (in family basis):
  Block 1: (--,++) with diagonal +-alpha and off-diagonal c
  Block 2: (-+,+-) with diagonal +-beta and off-diagonal c'

Eigenvalues: {+-sqrt(alpha^2+c^2), +-sqrt(beta^2+c'^2)}

ALWAYS in +- pairs. Can 3+1 emerge? This script proves NO.
"""

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================
# Build Cl(14) and sector decomposition (compact version)
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

# SO(4) torus
T1 = (1j / 2) * gammas[10] @ gammas[11]
T2 = (1j / 2) * gammas[12] @ gammas[13]

# Joint diagonalization
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

sectors = {}
for k in range(128):
    key = (+1 if joint_t1[k] > 0 else -1, +1 if joint_t2[k] > 0 else -1)
    sectors.setdefault(key, []).append(k)
sector_keys = sorted(sectors.keys())

# All 6 SO(4) generators
so4_gens_128 = {}
so4_dirs = [10, 11, 12, 13]
for i in range(4):
    for j in range(i+1, 4):
        label = f"sigma_{so4_dirs[i]+1}_{so4_dirs[j]+1}"
        so4_gens_128[label] = (1j / 2) * gammas[so4_dirs[i]] @ gammas[so4_dirs[j]]

print("=" * 70)
print("KC-12 DEFINITIVE: Eigenvalue Structure of SO(4) Mass Operators")
print("=" * 70)

# ============================================================
# Part 1: Block structure analysis
# ============================================================
print("\n--- Part 1: Inter-sector coupling pattern ---")
print("  (Which sectors are coupled by each generator?)")

for label, gen in so4_gens_128.items():
    print(f"\n  {label}:")
    for ki in sector_keys:
        vi = joint_basis[:, sectors[ki]]
        row = []
        for kj in sector_keys:
            vj = joint_basis[:, sectors[kj]]
            block = vi.conj().T @ gen @ vj
            row.append(np.linalg.norm(block, 'fro'))
        print(f"    ({ki[0]:+d},{ki[1]:+d}) -> " + "  ".join(f"{n:6.3f}" for n in row))

# ============================================================
# Part 2: The 4x4 family block structure
# ============================================================
print("\n--- Part 2: Family mass operator structure ---")

# The 4x4 family structure for each generator
# (trace of the 32x32 block is zero, so use the mean eigenvalue)
print("\n  Mean eigenvalue per sector for each generator:")
for label, gen in so4_gens_128.items():
    sector_means = []
    for key in sector_keys:
        vecs = joint_basis[:, sectors[key]]
        block = vecs.conj().T @ gen @ vecs
        mean_eval = np.mean(np.linalg.eigvalsh(block))
        sector_means.append(mean_eval)
    print(f"  {label}: {[f'{m:+.4f}' for m in sector_means]}")

# ============================================================
# Part 3: Exhaustive eigenvalue search
# ============================================================
print("\n--- Part 3: Exhaustive eigenvalue pattern search ---")
print("  Testing all linear combinations of SO(4) generators")
print("  Looking for 3+1 pattern (3 equal + 1 different)")

found_3plus1 = False
n_tests = 0

# Systematic search over coefficients
for a in np.linspace(-2, 2, 9):  # T1 coefficient
    for b in np.linspace(-2, 2, 9):  # T2 coefficient
        for c in np.linspace(-2, 2, 5):  # sigma_{11,13} coefficient
            for d in np.linspace(-2, 2, 5):  # sigma_{11,14} coefficient
                n_tests += 1
                M = (a * so4_gens_128["sigma_11_12"] +
                     b * so4_gens_128["sigma_13_14"] +
                     c * so4_gens_128["sigma_11_13"] +
                     d * so4_gens_128["sigma_11_14"])

                # Get eigenvalues per sector (mean of 32 eigenvalues each)
                sector_evals = []
                for key in sector_keys:
                    vecs = joint_basis[:, sectors[key]]
                    block = vecs.conj().T @ M @ vecs
                    evals = np.linalg.eigvalsh(block)
                    sector_evals.append(np.mean(evals))

                # Check for 3+1 pattern
                sv = np.sort(sector_evals)
                # 3+1: three equal, one different
                for skip_idx in range(4):
                    remaining = [sv[i] for i in range(4) if i != skip_idx]
                    if np.max(remaining) - np.min(remaining) < 0.01 and \
                       abs(sv[skip_idx] - np.mean(remaining)) > 0.1:
                        found_3plus1 = True
                        print(f"\n  FOUND 3+1! a={a:.1f}, b={b:.1f}, c={c:.1f}, d={d:.1f}")
                        print(f"    Sector means: {[f'{v:.4f}' for v in sv]}")
                        break

print(f"\n  Tested {n_tests} combinations.")
if not found_3plus1:
    print("  RESULT: NO 3+1 pattern found in ANY linear combination of SO(4) generators.")

# ============================================================
# Part 4: PROOF that 3+1 is impossible
# ============================================================
print("\n--- Part 4: Algebraic proof of impossibility ---")

print("""
  The 128-dim spinor under SO(10) x SO(4) decomposes as:
    128 = 32_SO(10) x 4_SO(4)

  where 4 = (2_L, 2_R) under SU(2)_L x SU(2)_R = SO(4).

  Any mass operator from the SO(4) algebra acts as:
    M = Id_32 x M_family

  where M_family is a 4x4 Hermitian matrix in the Lie algebra so(4).

  The Lie algebra so(4) = su(2)_L + su(2)_R decomposes as:
    M_family = M_L x Id_2 + Id_2 x M_R

  where M_L is a 2x2 traceless Hermitian matrix (su(2) element)
  and M_R is a 2x2 traceless Hermitian matrix.

  The eigenvalues of M_family = M_L tensor I + I tensor M_R are:
    lambda_L(i) + lambda_R(j)  for all pairs (i,j)

  where lambda_L(1) = -lambda_L(2) = a (from M_L eigenvalues)
  and   lambda_R(1) = -lambda_R(2) = b (from M_R eigenvalues)

  So the 4 family eigenvalues are:
    {a+b, a-b, -a+b, -a-b}

  These ALWAYS satisfy:
    m1 + m4 = 0  (the (a+b) and (-a-b) pair)
    m2 + m3 = 0  (the (a-b) and (-a+b) pair)

  For 3+1 with three equal: m1 = m2 = m3, m4 different.
    a+b = a-b   =>  b = 0
    a+b = -a+b  =>  a = 0
    Both a=0 and b=0  =>  all masses zero!

  THEOREM: No element of the SO(4) Lie algebra acting on (2_L, 2_R)
  can produce a 3+1 eigenvalue pattern. The constraint m1+m4 = m2+m3 = 0
  (which follows from the tensor product structure) is incompatible with
  three equal eigenvalues unless all are zero.
""")

# ============================================================
# Part 5: Verify the theorem numerically
# ============================================================
print("--- Part 5: Numerical verification of impossibility theorem ---")

# General su(2)_L element: M_L = a * sigma_3 (WLOG, by rotation)
# General su(2)_R element: M_R = b * sigma_3 (WLOG, by rotation)
# M_family = a * sigma_3 x I + b * I x sigma_3

sigma3 = np.array([[1, 0], [0, -1]]) / 2
I2_r = np.eye(2)

print("\n  Scanning all (a,b) pairs:")
for a in np.linspace(-3, 3, 13):
    for b in np.linspace(-3, 3, 13):
        M_fam = a * np.kron(sigma3, I2_r) + b * np.kron(I2_r, sigma3)
        evals = np.sort(np.linalg.eigvalsh(M_fam))
        # Check 3+1
        for skip in range(4):
            rem = [evals[i] for i in range(4) if i != skip]
            if max(rem) - min(rem) < 0.001 and abs(evals[skip] - np.mean(rem)) > 0.01:
                print(f"    FOUND 3+1: a={a:.1f}, b={b:.1f}, evals={np.round(evals, 4)}")

print("  (No output = no 3+1 pattern found)")

# ============================================================
# Part 6: What about BREAKING SO(4)?
# ============================================================
print("\n--- Part 6: Can SO(4) breaking beyond the algebra help? ---")

print("""
  The SO(4) Lie ALGEBRA cannot produce 3+1. But what about:

  (a) Higgs VEV that breaks SO(4) -> discrete subgroup?
      The mass operator is still M_L tensor I + I tensor M_R.
      Breaking just selects specific (a,b) values. Still 2+2.

  (b) Higher-order operators (M^2, M^3, etc.)?
      M^2 has eigenvalues {(a+b)^2, (a-b)^2, (a-b)^2, (a+b)^2} = 2+2.
      No improvement.

  (c) Non-linear Higgs couplings (quartic, etc.)?
      These give polynomials in (a+b), (a-b), still paired.

  (d) Multiple Higgs fields?
      M_total = sum_k (a_k tensor I + I tensor b_k)
      = (sum a_k) tensor I + I tensor (sum b_k)
      = A tensor I + I tensor B
      Same structure. Still 2+2.

  (e) Spinorial Higgs (128-dim)?
      This goes beyond the SO(4) algebra framework.
      The mass operator is no longer M_L tensor I + I tensor M_R.
      This COULD give 3+1 but requires new representation content.

  CONCLUSION: Within the minimal SO(14) framework with adjoint and vector
  Higgs, the Z2xZ2 character mechanism gives at most 2+2.
  3+1 requires going beyond (spinorial Higgs or extra dimensions).
""")

# ============================================================
# Part 7: The honest comparison with Z4 (Fortescue/Dollard)
# ============================================================
print("--- Part 7: Why Dollard's Z4 would give 3+1 but Z2xZ2 cannot ---")
print("""
  Dollard/Fortescue uses Z4 (cyclic group of order 4).
  Z4 acts on a 4-dim space with eigenvalues {1, i, -1, -i}.
  A Z4-symmetric mass operator has 4 independent eigenvalues.
  The trivial character (eigenvalue 1) is canonically singled out.
  => 3+1 IS natural for Z4.

  SO(14) gives Z2xZ2 (Klein four-group), NOT Z4.
  Z2xZ2 acts on (2,2) via tensor product.
  A Z2xZ2-symmetric mass operator has eigenvalues {a+b, a-b, -a+b, -a-b}.
  These are constrained by the tensor product structure.
  => 3+1 is IMPOSSIBLE.

  The groups Z4 and Z2xZ2 are NOT isomorphic:
  - Z4 has an element of order 4. Z2xZ2 does not.
  - Z4 has 4 characters: {1, i, -1, -i}. All distinct.
  - Z2xZ2 has 4 characters: {(1,1), (1,-1), (-1,1), (-1,-1)}.
    These factor as products of Z2 characters.

  This factoring is precisely what forces the 2+2 constraint.
  The analogy Dollard <-> SO(14) breaks at the group structure level.

  CLASSIFICATION:
    Dollard Z4 <-> SO(14) Z2xZ2: FALSE ANALOGY
    (Same order, different structure, different physics)
""")

# ============================================================
# FINAL VERDICT
# ============================================================
print("=" * 70)
print("KC-12 VERDICT: FIRES")
print("=" * 70)
print("""
  The Z2xZ2 character mechanism CANNOT produce a 3+1 mass pattern.
  This is a THEOREM, not a numerical observation:

    Any mass operator from SO(4) = SU(2)_L x SU(2)_R acting on (2_L, 2_R)
    has eigenvalues {a+b, a-b, -a+b, -a-b} for some a,b in R.
    These cannot be 3+1 unless a=b=0 (all zero).

  The Dollard/Fortescue analogy is FALSE at the structural level:
    Z4 (cyclic) allows 3+1. Z2xZ2 (Klein) does not.
    SO(14) gives Z2xZ2, not Z4.

  STATUS: KC-12 FIRES. The Z2xZ2 three-generation mechanism is DEAD.

  SALVAGE:
    - The impossibility theorem is a genuine result (publishable)
    - The four-sector structure of SO(14) spinors remains true
    - Paper 3 should use orbifold (Kawamura-Miura) for three generations
    - The Z2xZ2 observation goes in "future directions" noting the 2+2
      structure and its Dollard connection (ANALOGY, now downgraded)
""")
