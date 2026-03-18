# QA Audit: su9_yukawa_texture.py

**Date**: 2026-03-16
**File**: `src/experiments/su9_yukawa_texture.py`
**Auditor**: dollard-theorist (Opus)
**Scope**: Experimental values, mathematical correctness, code correctness, conclusion validity

---

## Summary

The script has **6 genuine errors**, **4 issues of concern**, and **3 minor items**. The overall conclusion ("Outcome C, underdetermined") is directionally correct but rests on wrong parameter counting. Several experimental values are internally inconsistent.

---

## 1. Experimental Values

### 1.1 CKM Matrix Elements

| Parameter | Code Value | PDG 2024 | Status |
|-----------|-----------|----------|--------|
| V_us | 0.2243 +/- 0.0005 | 0.22431 +/- 0.00085 | ACCEPTABLE |
| V_cb | 0.0422 +/- 0.0008 | ~0.0411 +/- 0.004 (combined) | STALE (matches PDG 2022 inclusive only) |
| V_ub | 0.00394 +/- 0.00036 | excl: 0.00370, incl: 0.00413 | ACCEPTABLE (plausible average) |

### 1.2 CKM Angles -- INTERNAL INCONSISTENCY [ERROR]

| Parameter | Code Value | Derived from V_us=0.2243 | Discrepancy |
|-----------|-----------|--------------------------|-------------|
| theta_12 | 13.04 deg | arcsin(0.2243) = 12.96 deg | **0.08 deg** |
| theta_23 | 2.42 deg | arcsin(0.0422) = 2.42 deg | 0 |
| theta_13 | 0.226 deg | arcsin(0.00394) = 0.226 deg | 0 |

**Finding**: `theta_12 = 13.04` is inconsistent with `V_us = 0.2243`. The value 13.04 corresponds to `sin(13.04 deg) = 0.2256`, which matches V_us ~ 0.2257 (a different vintage). The code stores both values but they disagree. Since these constants are never jointly used in computation, this doesn't affect results, but it is sloppy.

### 1.3 CKM CP Phase -- OUTDATED

| Parameter | Code Value | PDG 2024 / LHCb | Status |
|-----------|-----------|------------------|--------|
| delta_CP | 68 deg +/- 11 | LHCb direct: 63.8 +/- 3.5, indirect: 66.3 +/- 1.9 | HIGH by ~1.2 sigma |

The value 68 degrees appears to come from an older fit. The PDG 2024 combined result is closer to 65-66 degrees.

### 1.4 PMNS Angles -- ACCEPTABLE

| Parameter | Code Value | NuFit 5.2 (PDG 2024) | NuFit 6.0 (Sep 2024) |
|-----------|-----------|----------------------|----------------------|
| theta_12 | 33.41 | 33.41 | 33.66 |
| theta_23 | 49.1 | 49.1 | 47.44 |
| theta_13 | 8.54 | 8.54 | 8.52 |
| delta_CP | 197 | 197 | 234 |

The code exactly matches NuFit 5.2, which is what PDG 2024 adopted. Acceptable. However, NuFit 6.0 has significant shifts in theta_23 (1.7 deg) and delta_CP (37 deg).

### 1.5 Quark Mass Ratios -- ACCEPTABLE WITH CAVEAT

The code header says "at M_Z, MS-bar" which is correct. The values (mu=1.27 MeV, mc=0.619 GeV, etc.) are consistent with standard running mass tables (e.g., Xing, Zhang, Zhou 2008). However:
- md = 2.67 MeV vs reference ~2.90 MeV (low by ~8%)
- ms = 53.5 MeV vs reference ~55.0 MeV (low by ~3%)
- mb = 2.85 GeV vs reference ~2.89 GeV (low by ~1%)

These discrepancies are within the range of different RG running prescriptions and are acceptable for the purpose of this script (order-of-magnitude comparison).

### 1.6 Lepton Masses -- CORRECT

me = 0.511 MeV, mmu = 105.7 MeV, mtau = 1.777 GeV. All correct.

---

## 2. Mathematical Correctness

### 2.1 SVD-Based CKM Extraction -- CORRECT

The code computes `CKM = U_uL.conj().T @ U_dL` where `U_uL, s, Vh = svd(Yu)`. This is the standard and correct formula. The SVD decomposition gives `Yu = U_uL @ diag(s) @ V_R^H`, so `U_uL` is the left unitary matrix. The product of two unitary matrices is unitary. Verified numerically: `|V_CKM V_CKM^H - I| < 10^{-15}`.

### 2.2 Mixing Angle Extraction -- CORRECT (with edge-case caveat)

The standard parametrization extraction is:
- s13 = |V[0,2]| (correct: V_{ub} = s13 * e^{-i delta})
- s12 = |V[0,1]| / c13 (correct: V_{us} = s12 * c13)
- s23 = |V[1,2]| / c13 (correct: V_{cb} = s23 * c13)

Roundtrip verified: input angles are recovered exactly.

**Edge case**: If s13 = 1, the code sets c13 = 1e-10, which prevents division by zero but gives meaningless s12, s23 values. These are then clipped by `np.clip(s, 0, 1)`, so `arcsin` won't fail. The result would be theta_12 = theta_23 = 90 degrees, which is physically wrong but won't crash. Risk is LOW since s13 ~ 0.004 in practice.

### 2.3 Gell-Mann Matrices -- CORRECT

All 8 matrices verified:
- Hermitian: PASS
- Traceless: PASS
- Trace orthogonality Tr(lambda_a lambda_b) = 2 delta_ab: PASS

### 2.4 Adjoint Flavon Symmetry Breaking Claims -- CORRECT

- VEV along lambda_3 preserves U(1) x U(1): Verified. Only lambda_3 and lambda_8 commute with lambda_3.
- VEV along lambda_8 preserves SU(2) x U(1): Verified. lambda_1, lambda_2, lambda_3, and lambda_8 commute with lambda_8.

### 2.5 Adjoint Flavon Eigenvalue Computation -- LATENT BUG [ERROR]

Line 211: `masses_gen = np.sort(np.linalg.eigvalsh(Y_gen.real + Y_gen.real.T) / 2)`

The code takes `Y_gen.real`, discarding imaginary parts, then symmetrizes. Since `Y_gen` is Hermitian (sum of Hermitian matrices with real coefficients), the correct operation is `np.linalg.eigvalsh(Y_gen)` directly.

For the specific VEV direction used (lambda_3 + lambda_8 only), `Y_gen` is real diagonal, so the code gives correct results by accident. If the VEV had components along lambda_2, lambda_5, or lambda_7 (which are purely imaginary off-diagonal), the code would give **wrong eigenvalues**.

Verified: with a general VEV, the eigenvalues differ by up to 10%.

### 2.6 PMNS Extraction -- TWO LATENT BUGS [ERROR]

Line 95: `eigenvalues, U_nu = np.linalg.eigh(np.real(Mnu.conj().T @ Mnu))`

**Bug 1**: `np.real(M^H @ M)` discards imaginary parts of a Hermitian matrix. For complex `Mnu`, `M^H @ M` is Hermitian but generally has nonzero off-diagonal imaginary parts. Taking `np.real()` is mathematically wrong. For real `Mnu`, it is harmless.

**Bug 2**: `eigh(M^H @ M)` gives eigenvectors of `M^H @ M`, which are the **right singular vectors** of `M`. For the PMNS, we need the **left unitary transformation** that diagonalizes `M`. For real symmetric `M`, eigenvectors of `M` and `M^T M` coincide (verified numerically), so the code works. For complex `M`, this is wrong.

**Mitigating factor**: `extract_pmns` is never called in the script. These are latent bugs.

### 2.7 Parameter Counting -- WRONG [ERROR]

**Adjoint scenario (line 217)**: Claims "8 - 1 - 3 = 4 independent parameters."

This is wrong. Any adjoint VEV can be rotated by an SU(3) transformation into the Cartan subalgebra (span of lambda_3, lambda_8). The orbit of a generic adjoint element under SU(3) has dimension dim(SU(3)) - dim(stabilizer) = 8 - 2 = 6 (stabilizer is U(1) x U(1), the Cartan torus). So the correct counting is:

8 (VEV components) - 1 (overall scale) - 6 (orbit) = **1 free parameter** (the ratio v3/v8).

Furthermore, a single adjoint VEV gives a **diagonal** Yukawa matrix, so mixing angles are **identically zero**. To get CKM mixing requires different VEVs in the up and down sectors, or multiple flavons.

The code's claim that the adjoint has "4 parameters for 6 observables -- underdetermined" is wrong on both sides: it has 1 parameter, and it cannot produce mixing angles at all from a single sector.

**Sextet scenario (line 271)**: Claims "5 free parameters for 4 CKM observables."

A symmetric 3x3 real matrix has 6 parameters. Under SU(3), it can be diagonalized (removing 3 rotation angles), leaving 3 eigenvalues. Minus 1 scale = 2 free mass ratios. A single sextet determines mass ratios but not mixing angles (it gives CKM = I). To get CKM mixing requires two different sextets (up and down), which gives 4 mass ratios + 3 relative angles = 7 parameters for 10 observables (6 masses + 4 CKM) -- overconstrained.

The code conflates the number of matrix entries (6) with the number of physically independent parameters after symmetry reduction (2).

---

## 3. Code Correctness

### 3.1 CKM Unitarity -- CORRECT

Verified: `V_ckm @ V_ckm.conj().T` = I to machine precision.

### 3.2 SVD Sorting -- CORRECT

`np.sort(s_u)` sorts singular values in ascending order. `masses_u[-1]` is the largest. Mass ratios `m/masses[-1]` are correct.

### 3.3 Unicode Encoding -- BUG [ERROR]

Lines 193-194 use Unicode characters (subscript digits in lambda_3, lambda_8). On Windows with default cp1252 encoding, `print()` raises `UnicodeEncodeError`. The script crashes before producing output.

**Fix**: Either replace Unicode with ASCII (`lambda_3`, `lambda_8`) or add `# -*- coding: utf-8 -*-` and `PYTHONIOENCODING=utf-8`.

### 3.4 Triplet Scenario Structural Limitation -- NOT FLAGGED

The triplet scenario with `phi = (0, 0, 1)` and `phi' = (0, 1, 0)` produces Yukawa matrices where the first generation completely decouples: `Y[0,1] = Y[0,2] = Y[1,0] = Y[2,0] = 0`. Both `U_uL` and `U_dL` have `(1, 0, 0)` as a left singular vector, so `V_13 = V_31 = 0` identically and `V_23 = V_32 = 0` identically (because the 2-3 rotation is in a block that doesn't affect the first row/column).

The best-fit output confirms this: `theta_23 = 0.0, theta_13 = 0.0`. This is a structural limitation of the chosen VEV directions, not a tuning failure. The code does not flag or discuss this.

### 3.5 Mass Ratio Comparison -- MISLEADING

The sextet scenario prints mass ratios from its example matrix and compares them to quark mass ratios, but these come from a hand-chosen matrix. Since the matrix was chosen to be "hierarchical," the comparison has no predictive content.

---

## 4. Conclusion Validity

### 4.1 "Outcome C (underdetermined)" Assessment

The overall conclusion is **directionally correct** but **technically wrong** in its reasoning.

**Correct**: The SU(9) framework does not uniquely determine Yukawa textures. The flavon sector (representation, VEV direction, number of flavons) introduces enough freedom that the framework cannot make unique predictions for CKM/PMNS without additional input.

**Wrong**: The specific claim that each scenario is "underdetermined" (more parameters than observables) is wrong for the adjoint and sextet scenarios, where the parameter counting is incorrect. The adjoint scenario with a single flavon has 1 free parameter and cannot produce mixing at all. The sextet has 2 free mass ratios and cannot produce mixing from a single sector.

**More accurate conclusion**: The SU(9) framework provides the group-theoretic embedding but the Yukawa sector requires:
1. Multiple flavons or different VEVs in different sectors
2. A specific choice of flavon representations
3. Fine-tuning of VEV directions

This makes the framework **generic** (consistent with a wide range of parameters) rather than **predictive**. The correct physics term is "generic family symmetry" -- it is underdetermined not because individual scenarios have too many parameters, but because the framework does not select a unique scenario.

### 4.2 Comparison to Standard SU(5)

The claim "SU(5) part gives standard GUT Yukawa relations (m_b = m_tau at GUT scale, etc.)" is reasonable but not demonstrated in this script. It is a standard result from SU(5) GUT theory.

---

## 5. Issue Summary

### Errors (must fix)

| # | Location | Issue |
|---|----------|-------|
| E1 | Line 41/37 | theta_12=13.04 inconsistent with V_us=0.2243 (should be 12.96) |
| E2 | Line 211 | `Y_gen.real` discards imaginary parts; should use `eigvalsh(Y_gen)` directly |
| E3 | Line 95 | `np.real(M^H @ M)` is wrong for complex M (latent, never called) |
| E4 | Line 95 | `eigh(M^H @ M)` gives right singular vectors not left rotation (latent) |
| E5 | Lines 217, 271 | Parameter counting wrong for adjoint (1 not 4) and sextet (2 not 5) |
| E6 | Lines 193-194 | Unicode subscripts crash on Windows cp1252 encoding |

### Concerns (should address)

| # | Location | Issue |
|---|----------|-------|
| C1 | Line 39 | V_cb=0.0422 is PDG 2022 inclusive; PDG 2024 combined is ~0.0411 |
| C2 | Line 44 | delta_CP=68 is high vs LHCb 2024 (63.8) and indirect (66.3) |
| C3 | Lines 148-149 | Triplet VEV choice structurally gives theta_23=theta_13=0 (not flagged) |
| C4 | Lines 308-328 | Overall "underdetermined" conclusion has correct direction but wrong reasoning |

### Minor

| # | Location | Issue |
|---|----------|-------|
| M1 | Line 54 | Comment says "at M_Z, MS-bar" -- correct but should cite source |
| M2 | Line 264-267 | Sextet mass ratio comparison is from hand-chosen matrix, not a prediction |
| M3 | Line 172 | "3 free parameters can always fit 3 mixing angles" -- only fits 1 (V_us) |
