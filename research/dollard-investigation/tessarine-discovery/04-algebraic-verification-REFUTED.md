# Tessarine vs Dollard Versor Algebra: Algebraic Verification

**Date**: 2026-03-17
**Agent**: dollard-theorist
**Question**: Is Dollard's versor algebra the tessarine algebra (Cockle, 1848)?
Is the versor form ZY = h(XB+RG) + j(XG-RB) correct in tessarines?

## Executive Summary

**Both claims are FALSE**, verified by SymPy computation and cross-validated
against the project's existing Lean 4 proofs.

1. Dollard's versor algebra is NOT the tessarine algebra.
2. The versor form ZY = h(XB+RG) + j(XG-RB) is WRONG in both algebras.
3. Dollard's axioms {j^2=-1, hj=k, jk=1} force h=-1, collapsing to Z_4.
4. Tessarines require dropping jk=1 and are commutative; Dollard's axioms
   are non-commutative and (when taken at face value with h != -1)
   produce a NON-ASSOCIATIVE structure.

## Methodology

A Python/SymPy script (`src/experiments/tessarine_versor_verification.py`)
implements both algebras as classes with explicit multiplication tables and
tests all claims computationally.

## Results

### Test 1: Tessarine Multiplication Table -- VERIFIED

The tessarine algebra {1, j, h, k} with j^2=-1, h^2=+1, k=hj=jh (commutative):

```
  x |    1 |    j |    h |    k
  1 |    1 |    j |    h |    k
  j |    j |   -1 |    k |   -h
  h |    h |    k |    1 |    j
  k |    k |   -h |    j |   -1
```

Key properties: commutative, k^2 = -1, jk = -h.

### Test 2: Z*Y Product in Tessarines

For Z = R + jX (impedance) and Y = G - jB (admittance, Dollard's sign convention):

```
Z*Y = (RG + XB) + j*(XG - RB)
```

This is a PURELY COMPLEX result. No h or k components appear because
Z and Y lie in the {1, j} subspace, and tessarines are commutative, so
the product stays in that subspace.

### Test 3: The Claimed Form -- REFUTED

The claim ZY = h(XB+RG) + j(XG-RB) places real power in the h-component.
The actual result places it in the 1-component:

| Component | Claimed | Actual |
|-----------|---------|--------|
| 1 (real)  | 0       | RG+XB  |
| j         | XG-RB   | XG-RB  |
| h         | XB+RG   | 0      |
| k         | 0       | 0      |

The j-component matches; the 1 and h components are swapped. The claim
erroneously assigns real power to the hyperbolic direction.

**Exhaustive search of alternative forms** (Test 5):
- Form A: Z = hR + jX, Y = G - jB --> does NOT match target
- Form B: Z = R + jX, Y = hG - jB --> does NOT match target
- Form C: Z = hR + jX, Y = hG - jB --> does NOT match target

No choice of h-prefixing on Z or Y produces the claimed form.

### Test 4: Dollard's Algebra is NOT Tessarines

Three structural differences:

| Property | Tessarines | Dollard |
|----------|-----------|---------|
| Commutativity | Yes (hj = jh = k) | No (hj = k, jh = -j) |
| k^2 | -1 | h (if associative) |
| jk | -h | 1 (axiom) |

**Critical**: The Lean-verified proof in `algebraic_necessity.lean` shows
that Dollard's axioms {j^2=-1, hj=k, jk=1} FORCE h=-1 over any field.
The algebra collapses to Z_4 = {1, i, -1, -i}.

Proof sketch:
- jk = 1 implies k = j^(-1) = j^3 = -j
- hj = k = -j implies h = -1
- Therefore h^2 = 1, but h = -1 (a scalar, not an independent basis element)

### Test 5: Non-Associativity of Naive Dollard Algebra

If one attempts to build a 4D algebra with Dollard's axioms but h != -1,
the resulting Cayley table:

```
  x |    1 |    j |    h |    k
  1 |    1 |    j |    h |    k
  j |    j |   -1 |   -j |    1
  h |    h |    k |    1 |    j
  k |    k |   -h |   -k |    h
```

This table is NON-ASSOCIATIVE. Eight triple products fail:
- (j*j)*h != j*(j*h): LHS = -h, RHS = 1
- (j*j)*k != j*(j*k): LHS = -k, RHS = j
- (j*k)*h != j*(k*h): LHS = h, RHS = -1
- (j*k)*k != j*(k*k): LHS = k, RHS = -j
- (k*j)*h != k*(j*h): LHS = -1, RHS = h
- (k*j)*k != k*(j*k): LHS = -j, RHS = k
- (k*k)*h != k*(k*h): LHS = 1, RHS = -h
- (k*k)*k != k*(k*k): LHS = j, RHS = -k

**This means there is no 4D associative algebra satisfying Dollard's axioms
with h != -1.** The only associative solution is h = -1 (Z_4).

### Test 6: Z*Y in Dollard's Algebra -- Same Result

Even in Dollard's non-commutative algebra, Z*Y for Z = R+jX and Y = G-jB
gives (RG+XB) + j(XG-RB), because Z and Y only involve {1, j} and j
commutes with real scalars. The non-commutativity is invisible within
the {1, j} subspace.

### Test 7: Idempotent Decomposition -- VERIFIED (Tessarines Only)

In tessarines, e+ = (1+h)/2 and e- = (1-h)/2 are orthogonal idempotents:
- e+^2 = e+, e-^2 = e-, e+*e- = 0, e+ + e- = 1
- Tessarine ~= C (+) C (isomorphism to direct sum of complex numbers)
- z*e+ + z*e- = z for all tessarines z

This decomposition does NOT exist in Dollard's algebra (h = -1 makes
e+ = 0 and e- = 1, trivializing the decomposition).

### Test 8: Quaternary Identities -- VERIFIED (Series)

For Dollard's four-subseries decomposition of e^t:
- u = sum t^(4n)/(4n)!
- x = sum t^(4n+1)/(4n+1)!
- v = sum t^(4n+2)/(4n+2)!
- y = sum t^(4n+3)/(4n+3)!

The identities hold to order 79 (verified by coefficient comparison):
- u - v = cos(t)
- x - y = sin(t)
- u + v = cosh(t)
- x + y = sinh(t)

**Important distinction**: These identities are about the four subseries
of the SCALAR exponential e^t, NOT about the tessarine exponential
e^(j*theta + h*delta). The tessarine exponential gives:
- u - v = cos(theta)*exp(-delta), NOT cos(theta)
- The identities only reduce to the simple forms when delta=0 or theta=0.

### Test 9: jk in Tessarines

In tessarines: jk = j(hj) = (jh)j = kj (by commutativity) = (hj)j = h(j^2) = -h.
So jk = -h, NOT 1.

This is the key structural difference. Dollard needs jk = 1 for his
"counter-rotation cancellation" interpretation. Tessarines don't provide this.

## Cross-Validation Against Existing Lean Proofs

The SymPy results are fully consistent with the project's Lean 4 proofs:

| Lean proof file | What it proves | Consistent with SymPy? |
|----------------|----------------|----------------------|
| `basic_operators.lean` | j^4=1, h=-1, Cayley table is Z_4 | Yes |
| `algebraic_necessity.lean` | j^2=-1 + hj=k + jk=1 forces h=-1 | Yes |
| `telegraph_equation.lean` | ZY = (RG+XB)+j(XG-RB) with Dollard's signs | Yes |
| `telegraph_equation.lean` | Versor form h(XB+RG)+j(XG-RB) has wrong sign (h=-1 negates real part) | Yes |
| `cl11.lean` | Cl(1,1) has jk != 1 (e2*e12 = e1, not 1) | Yes: tessarines (which ARE Cl(1,1)) have jk = -h |

## Conclusions

1. **Dollard's algebra != tessarines.** They share j^2=-1, h^2=+1 but
   diverge on commutativity (tessarines yes, Dollard no), k^2 (tessarines: -1,
   Dollard: h or degenerately +1), and jk (tessarines: -h, Dollard: 1).

2. **The versor form ZY = h(XB+RG) + j(XG-RB) is wrong in both algebras.**
   The correct product is (RG+XB) + j(XG-RB) regardless of which algebra
   you use, because Z and Y have no h or k components.

3. **Dollard's axioms are self-collapsing.** The combination {j^2=-1, hj=k, jk=1}
   forces h=-1, reducing the "four operators" to the cyclic group Z_4.
   This is a Lean-verified mathematical theorem, not an interpretation choice.

4. **Tessarines (= Cl(1,1) = split-complex x complex) are what Dollard
   SHOULD have used** if he wanted a genuinely 4D algebra with h^2=+1 and
   j^2=-1. But then jk = -h (not 1), and the "counter-rotation cancellation"
   interpretation breaks.

5. **The quaternary identities are correct** but are about the scalar
   Taylor series decomposition, not the tessarine exponential.

## Files

- Verification script: `src/experiments/tessarine_versor_verification.py`
- This report: `research/dollard-theorist/2026-03-17-tessarine-versor-verification.md`
- Existing Lean proofs: `src/lean_proofs/foundations/algebraic_necessity.lean`,
  `src/lean_proofs/telegraph/telegraph_equation.lean`, `src/lean_proofs/clifford/cl11.lean`
- Existing analysis: `analysis/VERIFICATION_RESULTS.md`, `analysis/CLAIM_TRIAGE.md`
