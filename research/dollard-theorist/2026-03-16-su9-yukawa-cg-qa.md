# QA Report: `src/experiments/su9_yukawa_cg.py`

> Date: 2026-03-16
> Reviewer: dollard-theorist (Opus)
> Scope: SageMath API correctness, mathematical correctness, runtime safety
> Verdict: **3 bugs found (1 CRITICAL, 2 MODERATE), 5 minor issues**

---

## Summary

The script computes SU(9) Clebsch-Gordan coefficients for the Yukawa kill-condition
(Milestone 8.1). It uses SageMath's `WeylCharacterRing` to decompose the tensor
product 84 x 84*, verify the adjoint appears, and analyze factorization under
SU(5) x SU(4).

**The script will crash at runtime** due to a critical API misuse in the tensor
product iteration loop (lines 97-107). Two mathematical labeling errors and
several minor issues are also present.

---

## CRITICAL Issues

### BUG 1 [CRITICAL]: Iteration over tensor product uses wrong API (lines 97-107)

**The code:**
```python
for rep, mult in product:
    dim = rep.degree()
    hw = rep.highest_weight()
    label = str(hw)
```

**The problem:** `WeylCharacterRing` inherits from `CombinatorialFreeModule`. The
`__iter__` method on `CombinatorialFreeModule.Element` yields `(basis_index, coefficient)`
pairs, where the basis index is a **weight lattice element** (a tuple-like object), NOT
a `WeylCharacterRingElement`. Confirmed by reading the SageMath source:

```python
# From sage/modules/with_basis/indexed_element.pyx:
def __iter__(self):
    return iter(self._monomial_coefficients.items())
```

And the `degree()` method itself uses this same iteration internally:
```python
# From sage/combinat/root_system/weyl_characters.py:
def degree(self):
    L = self.parent()._space
    return sum(L.weyl_dimension(k) * c for k, c in self)
```

Here `k` is a weight (basis index), not a ring element. Weight lattice elements do NOT
have `.degree()` or `.highest_weight()` methods.

**Result:** `AttributeError: '...' object has no attribute 'degree'` at runtime.

**Fix:** Use `monomials()` and `coefficients()` separately:
```python
monomials = product.monomials()
coefficients = product.coefficients()
for rep, mult in zip(monomials, coefficients):
    dim = rep.degree()
    hw = rep.highest_weight()
    label = str(hw)
```

Or reconstruct ring elements from weights:
```python
for weight, mult in product:
    rep = A8(weight)
    dim = rep.degree()
    hw = rep.highest_weight()
    label = str(hw)
```

**Recommended safest fix** (avoids ordering ambiguity between `monomials()` and
`coefficients()`):
```python
for weight, mult in product:
    rep = A8(weight)       # coerce weight back to ring element
    dim = rep.degree()
    hw = rep.highest_weight()
    label = str(hw)
    key = f"dim_{dim}_{label}"
    decomposition[key] = {"dim": int(dim), "multiplicity": int(mult), "dynkin": label}
    print(f"    {mult} x {dim} ({label})")
    if dim == 80:
        contains_adjoint = True
        adjoint_multiplicity = int(mult)
```

**Severity:** CRITICAL -- the script cannot run. Steps 3-5 will never execute.

**Verification source:** SageMath source code at
`github.com/sagemath/sage/blob/develop/src/sage/modules/with_basis/indexed_element.pyx`
and `github.com/sagemath/sage/blob/develop/src/sage/combinat/root_system/weyl_characters.py`.

---

## MODERATE Issues

### BUG 2 [MODERATE]: Branching of 84 mislabels (1,4-bar) as (1,4) (lines 143, 163-167)

**The code (line 143):**
```python
#          = (10,1) + (10,4) + (5,6) + (1,4)
```

**The code (line 167):**
```python
"(1,4)":  {"su5_dim": 1,  "su4_dim": 4, "total": 4},
```

**The problem:** Lambda^3(C^4) under SU(4) is the representation with highest weight
omega_3 of A3, which is the ANTI-fundamental (conjugate of the fundamental). That is:

  Lambda^3(C^4) = (C^4)^* = 4-bar

This is standard: for SU(n), Lambda^(n-1)(fund) = conj(fund). Here n=4, so
Lambda^3(4) = 4-bar.

The dimension is still 4, so the dimension check passes, but the representation label
is incorrect. The research notebook (`yukawa-kill-condition-research.md`, line 44)
correctly states `(1,4-bar)`.

**Fix:** Change `(1,4)` to `(1,4-bar)` in both the comment (line 143) and the
dictionary key (line 167).

**Impact:** The factorization analysis in Step 5 uses the correct labels for the
conjugate (`(1,4-bar)` on line 182), creating an inconsistency: the 84 branching says
`(1,4)` but the 84* branching says `(1,4-bar)`. The conjugate of `(1,4)` would be
`(1,4-bar)`, which happens to match -- but only by accident. With the corrected label
`(1,4-bar)` for 84, the conjugate for 84* should be `(1,4)`.

### BUG 3 [MODERATE]: Conjugate branching of 84* is inconsistent (lines 177-183)

**The code:**
```python
# Conjugate 84*: Lambda^3(5*+4*) = (10-bar,1) + (10-bar,4-bar) + (5-bar,6) + (1,4-bar)
branching_84_conj = {
    "(10-bar,1)":     {"su5_dim": 10, "su4_dim": 1,  "total": 10},
    "(10-bar,4-bar)": {"su5_dim": 10, "su4_dim": 4,  "total": 40},
    "(5-bar,6)":      {"su5_dim": 5,  "su4_dim": 6,  "total": 30},
    "(1,4-bar)":      {"su5_dim": 1,  "su4_dim": 4,  "total": 4},
}
```

**The problem:** Given the CORRECTED branching of 84:
```
84 = (10,1) + (10,4) + (5,6) + (1,4-bar)
```

The conjugate should flip every representation to its conjugate:
- 10 -> 10-bar (correct)
- 4 -> 4-bar (correct)
- 6 -> 6 (self-conjugate, correct)
- 4-bar -> 4 (NOT 4-bar)

So the correct conjugate branching is:
```
84* = (10-bar,1) + (10-bar,4-bar) + (5-bar,6) + (1,4)
```

The last entry should be `(1,4)`, not `(1,4-bar)`.

**Fix:** Change `"(1,4-bar)"` to `"(1,4)"` on line 182.

**Impact:** This error is self-consistent with BUG 2 (both bugs cancel in the
conjugation), so the downstream factorization analysis is not affected. But the
labels are wrong and would cause confusion if used as ground truth elsewhere.

---

## MINOR Issues

### ISSUE 4 [MINOR]: Dead code -- SU(5) and SU(4) representations never used (lines 150-161)

The script creates `su5_10`, `su5_5`, `su5_5bar`, `su5_10bar`, `su5_1`, `su4_4`,
`su4_6`, `su4_4bar`, `su4_1` but never uses any of them. The branching is done
entirely via hardcoded dictionaries.

**Impact:** Wasted computation. More importantly, the script CLAIMS to compute
branchings (line 131: "Branching 84 under SU(5) x SU(4)...") but actually just
asserts known answers. This is honest in the sense that the branching formula
Lambda^3(V+W) = sum Lambda^p(V) x Lambda^q(W) is a standard identity, but the
code gives the false impression that SageMath is verifying it.

**Recommendation:** Either use these representations with SageMath's `branch()`
method to actually compute the branching, or remove the unused variables and add
a comment clarifying this is a manual calculation.

### ISSUE 5 [MINOR]: Adjoint detection by dimension only (lines 105-107)

```python
if dim == 80:
    contains_adjoint = True
    adjoint_multiplicity = int(mult)
```

This checks for dimension 80 but does not verify the representation is actually
the adjoint (omega_1 + omega_8). There could in principle be other 80-dimensional
representations of SU(9). In practice, for A8, the only irrep of dimension 80 in
the decomposition of 84 x 84* IS the adjoint, so this works. But it is fragile.

**Fix:** Compare highest weights directly:
```python
adjoint_hw = (fund[1] + fund[8])
if rep.highest_weight() == adjoint_hw:
    contains_adjoint = True
```

(This fix depends on first fixing BUG 1 so that `rep` is a proper ring element.)

### ISSUE 6 [MINOR]: Comment arithmetic error left in code (line 199)

```python
# where 24+15+20+20+1 = 80 <- Wait, 24+15+20+20 = 79, need to check
```

This "working out loud" comment should be cleaned up for a production script.
The subsequent lines (201-209) correctly resolve the issue, but leaving the
confused intermediate state in the code is untidy.

### ISSUE 7 [MINOR]: No `metadata.capture()` call

The `CLAUDE.md` for `src/experiments/` states: "Every run must call
`metadata.capture()` for reproducibility." This script does not call any
metadata capture function. It does record runtime, but not SageMath version,
system info, etc.

### ISSUE 8 [MINOR]: Channel 2 SU(5) contraction label is misleading (line 255)

```python
"su5_contraction": "10 x 5-bar x 5-bar -> check",
```

The three SU(5) representations from the three sources are:
- from 84 `(10,4)`: SU(5) = **10**
- from 84_conj `(5-bar,6)`: SU(5) = **5-bar**
- from 80 `(5-bar,4)`: SU(5) = **5-bar**

So "10 x 5-bar x 5-bar" is correct. But the question mark "-> check" hides a
straightforward answer: 10 x 5-bar = 5 + 45, and 45 x 5-bar contains a singlet
(since 45 = Lambda^2(10) and 10 x 5-bar -> ...). Actually the full check:
5 x 5-bar = 1 + 24 (contains singlet), so 10 x 5-bar x 5-bar does contain a
singlet. This could be stated explicitly.

---

## Mathematical Correctness (Verified Claims)

The following claims in the script are mathematically correct:

| Claim | Status | Verification |
|-------|--------|-------------|
| `WeylCharacterRing('A8', style='coroots')` for SU(9) | CORRECT | A_n = SU(n+1), so A8 = SU(9) |
| `fund[1]` for fundamental 9-dim rep | CORRECT | omega_1 of A8 is the defining rep |
| `fund[3]` for Lambda^3(9) = 84 | CORRECT | omega_k of A_n is Lambda^k of fund; C(9,3) = 84 |
| `fund[6]` for conjugate Lambda^3* = 84 | CORRECT | In A8, omega_k and omega_(8-k) are conjugate; omega_6 = omega_(9-3) |
| `fund[1] + fund[8]` for adjoint (80-dim) | CORRECT | Adjoint of SU(n) has HW omega_1 + omega_(n-1); for SU(9), this is omega_1 + omega_8; dim = 9^2 - 1 = 80 |
| C(9,3) = 84 | CORRECT | 9!/(3!6!) = 84 |
| Branching dimensions 10+40+30+4 = 84 | CORRECT | |
| Adjoint branching 24+15+20+20+1 = 80 | CORRECT | su(5) + su(4) + u(1) + bifundamentals |
| Lambda^2(C^5) = 10-dim | CORRECT | C(5,2) = 10 |
| Lambda^2(C^4) = 6-dim (self-conjugate) | CORRECT | C(4,2) = 6; 6 of SU(4) is real |
| Schur uniqueness: adjoint appears once in R x R* | CORRECT | Standard result from Schur's lemma |

---

## Factorization Analysis Correctness

The conclusion (lines 286-295) that the Yukawa coupling factorizes into SU(5) x SU(4)
parts for the diagonal channel is **mathematically correct**. The assessment that this
gives degenerate masses in the SU(3)-symmetric limit (delta_{ij}) is also correct.

The conclusion that non-trivial Yukawa textures require SU(3)_family breaking is
standard physics and correct.

The classification as "Outcome C (underdetermined survival)" is an honest assessment.

However, this analysis is ENTIRELY MANUAL -- none of it is computed by SageMath. The
only actual SageMath computation is Step 3 (tensor product decomposition), which crashes
due to BUG 1. Steps 4 and 5 are hardcoded.

---

## Recommended Fix Priority

1. **BUG 1** (CRITICAL): Fix iteration API -- script cannot run without this
2. **BUG 2** (MODERATE): Fix `(1,4)` -> `(1,4-bar)` label in 84 branching
3. **BUG 3** (MODERATE): Fix `(1,4-bar)` -> `(1,4)` label in 84* branching
4. **ISSUE 4** (MINOR): Remove dead code or implement actual branching
5. **ISSUE 5** (MINOR): Check adjoint by highest weight, not dimension
6. **ISSUE 6** (MINOR): Clean up working-aloud comment
7. **ISSUE 7** (MINOR): Add metadata.capture()
8. **ISSUE 8** (MINOR): Resolve "-> check" with explicit answer

---

## Corrected Branching Summary

For reference, the correct branching labels are:

**84 = Lambda^3(C^9) under SU(5) x SU(4):**
```
84 = (10, 1) + (10, 4) + (5, 6) + (1, 4-bar)
```

**84* = Lambda^6(C^9) under SU(5) x SU(4):**
```
84* = (10-bar, 1) + (10-bar, 4-bar) + (5-bar, 6) + (1, 4)
```

**80 = adjoint of SU(9) under SU(5) x SU(4) x U(1):**
```
80 = (24, 1) + (1, 15) + (5, 4-bar) + (5-bar, 4) + (1, 1)
```
