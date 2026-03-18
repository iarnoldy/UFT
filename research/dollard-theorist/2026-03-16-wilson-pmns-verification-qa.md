# QA Report: wilson_pmns_verification.py

**Date**: 2026-03-16
**Reviewer**: dollard-theorist (Opus)
**File**: `src/experiments/wilson_pmns_verification.py`
**Status**: COMPLETE -- 3 errors, 5 warnings, 4 notes

---

## Executive Summary

The script is structurally sound and intellectually honest about its limitations, but
contains **one factual error in Wilson's claimed predictions**, **one silent data
corruption bug**, and **one misleading reference**. The E8 root system construction,
SU(9) decomposition verification, and Z3 eigenvalue analysis are all correct. The
script's candid admission that it cannot reproduce Wilson's full derivation is its
strongest feature.

---

## Issue 1 [ERROR]: theta_12 = 33.21 is NOT Wilson's prediction

**Location**: Line 54, `WILSON_PREDICTIONS`

**Claim in script**:
```python
"theta_12": {"value": 33.21, "source": "arXiv:2407.18279"},
```

**What Wilson actually says** (arXiv:2407.18279, Section 7):
> "The measured Cabibbo angle of 13.02 deg is added to the 20 deg twist to
> produce the angle of 33.02 deg"

Wilson's value is **33.02 degrees**, not 33.21 degrees. The value 33.21 does not
appear anywhere in arXiv:2407.18279.

Moreover, this is NOT a pure geometric prediction. Wilson derives 33.02 by adding
the *measured* Cabibbo angle (13.02 deg, an experimental input) to a 20 deg geometric
offset. This makes theta_12 a *post-diction* (uses experimental data as input), not
a zero-parameter prediction like the script's framing implies.

**Fix**: Change value to 33.02 and add a note that this angle requires the measured
Cabibbo angle as input.

**Severity**: HIGH -- this is a factual error about the claimed prediction.

---

## Issue 2 [ERROR]: Wilson's PMNS derivation is NOT zero-parameter

**Location**: Lines 8-14 (docstring), line 429 (conclusion)

**Claim in script** (docstring, lines 8-9):
> "Independently verifies Wilson's claimed PMNS predictions from E8 geometry"

And line 12:
> theta_12 = 33.21 deg (experiment: ...) -- <1% match

**What Wilson actually does** (arXiv:2407.18279, Section 7):

1. theta_13: Wilson starts from a "natural" value of 10 deg (from 1/4 - 2/9 = 1/36
   of a circle), then subtracts a correction of 1.414 deg derived by splitting the
   CKM angle 2.337 deg (itself computed in a *separate paper* using proton mass as
   input) in the ratio cos(10 deg)/cos(50 deg). Result: 10 - 1.414 = 8.586 deg.

2. theta_23: Wilson starts from 50 deg (from 1/4 - 1/9 = 5/36 of a circle), then
   subtracts the complementary correction 0.923 deg. Result: 50 - 0.923 = 49.077 deg.

3. theta_12: Wilson adds the *experimentally measured* Cabibbo angle (13.02 deg) to
   a 20 deg geometric offset. Result: 13.02 + 20 = 33.02 deg.

Wilson himself acknowledges (Section 7): "there is no theoretical justification for
this calculation, which remains purely conjectural."

The derivation is NOT from pure E8 geometry with zero free parameters. It uses:
- The proton mass (to compute the CKM angle 2.337 deg in reference [15])
- The measured Cabibbo angle (13.02 deg, for theta_12)
- An ad hoc splitting ratio (cos 10 deg / cos 50 deg)

The script's "significance_assessment" (line 441-444) claiming "three PMNS angles
from pure geometry (zero free parameters)" is therefore **misleading**.

**Fix**: Revise docstring and significance assessment to accurately reflect that
Wilson's derivation uses experimental inputs and is self-described as "conjectural."

**Severity**: HIGH -- misrepresents the epistemic status of Wilson's claims.

---

## Issue 3 [ERROR]: Silent data corruption via numpy view mutation

**Location**: Lines 334-339

```python
V_w_su4 = V_w[5:9, :]  # 4x3 matrix  (line 334)
# ...
for j in range(3):                      # (line 338)
    V_w_su4[:, j] /= np.linalg.norm(V_w_su4[:, j])  # (line 339)
```

`V_w[5:9, :]` returns a numpy *view*, not a copy. The normalization loop modifies
`V_w_su4` in place, which **also modifies the original `V_w` matrix**. After this
loop, `V_w` no longer contains valid eigenvectors of sigma_9 (column norms are
~1.29 and ~1.15 instead of 1.0).

This bug does not affect the script's output because `V_w` is not used after the
normalization loop, but it is a latent correctness hazard.

**Fix**: Use `V_w_su4 = V_w[5:9, :].copy()` or avoid in-place modification.

**Severity**: MEDIUM -- silent data corruption, currently harmless but fragile.

---

## Issue 4 [WARNING]: Reference arXiv:2504.xxxxx is a placeholder

**Location**: Line 34

```python
- Wilson, "E8 and the Standard Model", arXiv:2504.xxxxx (2025)
```

This is a placeholder arXiv ID. The actual 2025 Wilson paper is
arXiv:2507.16517, "Embeddings of the Standard Model in E_8."

**Fix**: Replace with `arXiv:2507.16517` or remove if not actually used.

---

## Issue 5 [WARNING]: arXiv:2210.06029 does NOT contain PMNS predictions

**Location**: Lines 10-13 (docstring), line 56

The docstring lists arXiv:2210.06029 as a source for the PMNS predictions. That
paper ("Chirality in an E_8 model") discusses chirality, not mixing angles. The
PMNS angle predictions appear only in arXiv:2407.18279.

**Fix**: Remove 2210.06029 from the PMNS prediction attribution. It is relevant
to the chirality discussion but not to the mixing angles.

---

## Issue 6 [WARNING]: The Z3 permutation is NOT Wilson's type 5

**Location**: Lines 260-272

The script constructs sigma = (1 4 7)(2 5 8)(3 6 9) as a 9x9 permutation matrix
and correctly acknowledges (lines 377-380) that this is a "simplified model" and
not Wilson's actual construction.

However, the relationship between this permutation and Wilson's type 5 element is
not just "simplified" -- it is **categorically different**:

- Wilson's type 5 is a *torus element* exp(2*pi*i/3 * H) where H is a specific
  cocharacter in the maximal torus of E8 with coordinates (1,1,1,1,1,0,0,0).
- The permutation (1 4 7)(2 5 8)(3 6 9) is a Weyl group element, not a torus element.
- A torus element acts by *diagonal* phase multiplication on weight spaces.
  A Weyl group element acts by *permuting* weight spaces.

These are fundamentally different types of group elements. The fact that both have
order 3 and 3+3+3 eigenvalue structure does not make them equivalent.

The script's language ("simplified model") understates this gap. A more accurate
statement: "This permutation is a toy model sharing the Z3 eigenvalue structure
but not the geometric content of Wilson's type 5 torus element."

**Severity**: MEDIUM -- the script is honest about the limitation but understates
the mathematical gap.

---

## Issue 7 [WARNING]: SU(4) index identification is unverified

**Location**: Lines 316-331

The script identifies indices {5,6,7,8} (0-indexed) as the "SU(4) subspace" in
the 9 = 5 + 4 decomposition under SU(5) x SU(4). This identification assumes:

1. The first 5 coordinates correspond to SU(5)
2. The last 4 coordinates correspond to SU(4)
3. The SU(4) factor is the one carrying family structure

While this is a *natural* choice, it is not the only one. The 9-dimensional
fundamental of SU(9) can be split as 5+4 in multiple inequivalent ways depending
on which SU(5) x SU(4) subgroup is chosen. Different embeddings would give
different projections.

Since the script does not actually use this projection for any claimed result,
this is a documentation concern, not a correctness issue.

**Severity**: LOW

---

## Issue 8 [WARNING]: Experimental values may be outdated

**Location**: Lines 46-50

```python
PMNS_EXP = {
    "theta_12": {"value": 33.41, "error": 0.75, "unit": "degrees"},
    "theta_23": {"value": 49.1,  "error": 1.0,  "unit": "degrees"},
    "theta_13": {"value": 8.54,  "error": 0.12, "unit": "degrees"},
}
```

These values are attributed to "PDG 2024 / NuFIT 5.2". The NuFIT 5.2 values
(November 2022, with SK atmospheric data) for normal ordering are:

- theta_12 = 33.41 (+0.75, -0.72) deg -- MATCHES (asymmetric error symmetrized)
- theta_23 = 49.26 (+0.79, -0.83) deg -- CLOSE but script says 49.1
- theta_13 = 8.58 (+0.11, -0.11) deg  -- CLOSE but script says 8.54

The NuFIT 5.2 values without SK atmospheric data are slightly different:
- theta_23 = 42.2 (+1.1, -0.9) deg (normal ordering, without SK)

The script's theta_23 = 49.1 +/- 1.0 and theta_13 = 8.54 +/- 0.12 appear to
be from an older NuFIT version or PDG compilation. The exact source should be
pinned with a specific table reference.

Note: NuFIT has asymmetric error bars; the script symmetrizes them. This is
acceptable for a rough comparison but should be noted.

**Severity**: LOW -- values are close but not precisely NuFIT 5.2.

---

## Verified Correct

### E8 Root System (Lines 77-93)
- `RootSystem(['E', 8])` with `root_lattice.positive_roots()` is the correct
  SageMath API. CORRECT.
- 120 positive roots, 240 total roots, rank 8. CORRECT.

### SU(9) Dimension (Lines 136-138)
- `LieAlgebra(QQ, cartan_type=['A', 8])` gives SU(9). CORRECT.
- dim(SU(9)) = 9^2 - 1 = 80. CORRECT.

### Branching Verification (Lines 151-182)
- `WeylCharacterRing('E8', style='coroots')` is valid SageMath API. CORRECT.
- E8 adjoint = fundamental weight omega_8 in Bourbaki/coroot style. CORRECT.
- A8 adjoint: omega_1 + omega_8 (Dynkin labels [1,0,0,0,0,0,0,1]). CORRECT.
- Lambda^3(9) = omega_3 (Dynkin label [0,0,1,0,0,0,0,0]). CORRECT.
- Lambda^6(9) = omega_6 = (Lambda^3)*. CORRECT.
- 80 + 84 + 84 = 248. CORRECT.

### Z3 Permutation Matrix (Lines 266-276)
- Permutation matrix constructed with convention P[sigma(i), i] = 1. CORRECT.
- sigma(0)=3, sigma(1)=4, ..., sigma(6)=0, sigma(7)=1, sigma(8)=2. CORRECT.
- sigma^3 = I verified. CORRECT.

### Eigenvalue Counts (Lines 280-286)
- 3 eigenvalues equal to 1, 3 equal to omega, 3 equal to omega^2. CORRECT.
- This is the correct eigenvalue structure for three 3-cycles on 9 objects. CORRECT.

### Honest Limitations (Lines 390-408)
- "verified_algebraically" list is accurate. CORRECT.
- "not_yet_verified" list correctly identifies the key gaps. CORRECT.
- "blocking_questions" are the right questions to ask. CORRECT.

### JSON Output (Lines 459-466)
- Output path construction is correct. CORRECT.
- `json.dump` with `default=str` handles non-serializable types. CORRECT.
- Directory creation with `exist_ok=True`. CORRECT.

---

## Code Quality Notes

### Note 1: SageMath shebang
Line 1: `#!/usr/bin/env sage` -- this works for direct execution but the run
instruction (line 23) says `wsl sage src/experiments/...`. Both should work.

### Note 2: No try/except for SageMath imports
If run without SageMath (e.g., plain Python), line 37 `from sage.all import *`
will fail with an unhelpful ImportError. Consider wrapping in try/except with
a clear error message.

### Note 3: Unused V_1 and V_w2
Lines 305-307 compute `V_1`, `V_w`, `V_w2` (eigenspaces for eigenvalues 1, omega,
omega^2). Only `V_w` is used. The other two are computed but never referenced.

### Note 4: The branching E8 -> A8 is not actually computed
Lines 168-170 say "Computing branching E8 -> A8..." but then immediately print
"(Using known decomposition: 248 = 80 + 84 + 84*)". The actual SageMath branching
rule computation (which would use `e8_adjoint.branch(A8_ring, rule=...)`) is NOT
performed. The script only verifies the dimension sum. This is honest (it says
"Using known decomposition") but the print statement "Computing branching" is
slightly misleading.

---

## Summary of Required Fixes

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | HIGH | theta_12 = 33.21 is wrong | Change to 33.02, cite correctly |
| 2 | HIGH | "Zero parameter" framing is wrong | Revise docstring and significance |
| 3 | MEDIUM | numpy view mutation corrupts V_w | Use `.copy()` |
| 4 | LOW | Placeholder arXiv ID | Replace 2504.xxxxx with 2507.16517 |
| 5 | LOW | 2210.06029 misattributed for PMNS | Remove from PMNS attribution |
| 6 | LOW | "Simplified model" understates gap | Strengthen disclaimer language |
| 7 | LOW | SU(4) index choice unverified | Add caveat |
| 8 | LOW | Experimental values imprecise | Pin to specific NuFIT table |

---

## Verdict

The script's *algebraic verifications* (root counts, representation dimensions,
eigenvalue structure) are all correct and well-implemented. The script's *honesty*
about its limitations is commendable.

The critical issues are:
1. **Wilson predicts 33.02, not 33.21** -- a factual error that must be corrected.
2. **Wilson's derivation is NOT zero-parameter** -- it uses the measured Cabibbo
   angle and is self-described as "conjectural." The script's framing as "pure
   geometry" is misleading.

These two issues affect the scientific integrity of the output JSON and must be
fixed before the script is used for any downstream analysis or publication.
