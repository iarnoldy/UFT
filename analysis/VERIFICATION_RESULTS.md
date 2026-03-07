# Verification Results

## Summary

Two independent verification methods applied to Dollard's versor algebra:

1. **Lean 4 formal proofs** (this project): mathematical certainty
2. **N-Phase computational tests** (upstream, 1194 passing): machine-precision validation

Both produce the same conclusion: the versor algebra is standard Z_4 arithmetic,
the polyphase formula is standard DFT, the versor form equivalence is wrong,
and the physics claims have no formal backing.

## Verified Claims

### Basic Operators (Trivial)

The h, j, k operator system is mathematically consistent when interpreted as the
4th roots of unity: {1, i, -1, -i}.

| Property | Lean result | N-Phase result | Assessment |
|----------|------------|----------------|------------|
| j^4 = 1 | Verified | 133 tests pass | Standard: i^4 = 1 |
| j^2 = -1 | Verified | Cayley table verified | Standard: i^2 = -1 |
| h^2 = 1 (with h=-1) | Verified | H operator = -1 | Trivial: (-1)^2 = 1 |
| h^1 = -1 | Verified | H operator = -1 | Trivial: (-1)^1 = -1 |
| k = hj = -j | Verified | All 16 products match | Trivial: (-1)(i) = -i |
| jk = 1 | Verified | Counter-rotation verified | Trivial: i(-i) = 1 |
| Sequence periodicity | Verified | DFT structure inherent | By construction |
| Complete Cayley table | N/A | Latin square verified | Abelian group Z_4 |

**Assessment**: Both formal and computational verification confirm the versor algebra
is isomorphic to Z_4 under multiplication. Not a novel algebraic finding.

### Telegraph Equation (Standard)

| Property | Lean result | Assessment |
|----------|------------|------------|
| (R+jX)(G+jB) = (RG+XB) + j(XG-RB) | Verified | Standard complex multiplication |
| Four factors exist | Verified | Existence proof (witness: R=X=G=B=1) |
| Physical interpretations | N/A | Outside scope of formal verification |

**Assessment**: The algebraic expansion is correct but is standard Heaviside (1880s).
The four-factor analysis is a valid observation about complex multiplication,
not a novel contribution.

## Disproved Claims

### Versor Form Equivalence (Genuine Finding)

**Claim**: ZY = h(XB+RG) + j(XG-RB) is equivalent to the standard telegraph form.

**Disproof**: With h = -1 (the only consistent interpretation):
- Versor form: -(XB+RG) + j(XG-RB)
- Standard form: +(XB+RG) + j(XG-RB)
- These differ by sign in the real part.

**Evidence**: `src/lean_proofs/telegraph/telegraph_equation.lean:85-92`

**Significance**: This is the project's one genuine non-trivial result. It shows
that Dollard's claimed equivalence between standard and versor forms contains a
mathematical error. Either:
1. The h operator should be +1 (contradicting h^1 = -1), or
2. The versor form is simply wrong.

No repair preserves both h = -1 and the equivalence claim.

**Corroboration from N-Phase**: The N-Phase system's `decomposer.py` uses the standard
DFT formula A_N[p,s] = omega^(ps), not Dollard's versor form. The system works to
machine precision precisely because it avoids the versor form.

## Computationally Validated (Lean Proof Pending)

### Polyphase Formula (N-Phase: 491 tests, N=2..12)

The universal polyphase formula k^n_N = exp(j*2*pi*n/N) is validated by the N-Phase
system to machine precision (<1e-10 NMSE). Key properties confirmed:

| Property | N-Phase result | Lean status |
|----------|---------------|-------------|
| Orthogonality: A_N^H @ A_N = N*I_N | Verified (N=2..12) | Not yet attempted |
| Lossless reconstruction | NMSE < 1e-10 | Not yet attempted |
| Parseval's theorem (energy conservation) | Verified | Not yet attempted |
| Cross-validation vs numpy.fft | Match | Not yet attempted |
| N=4 matrix matches Dollard's versor matrix | Confirmed | Not yet attempted |

Lean formal proof is Experiment 0 (BLOCKING).

### Quaternary Expansion (N-Phase: 175 tests, then DEPRECATED)

Dollard's quaternary decomposition of e^(j*theta) into four subseries (u,x,v,y)
is mathematically correct (verified to 12 decimal places by N-Phase). However,
N-Phase experiment E006a showed the cosh/sinh features are redundant with magnitude
and cause catastrophic condition number collapse on real data.

**Lesson**: Mathematical correctness does not imply practical utility.

## Known Gaps

| Gap | Location | Status |
|-----|----------|--------|
| `sorry` in `factors_independent_variation` | telegraph_equation.lean:66-69 | Incomplete proof |
| Polyphase formula | Not yet attempted | Experiment 0 (blocking) |
| Dimensional analysis | Not yet attempted | Experiment 3 |

## Methodology Assessment

**What worked**: Lean 4 successfully identified both valid and invalid mathematical
claims. The disproof of versor form equivalence demonstrates the value of formal
verification for alternative mathematical frameworks.

**What was trivial**: Most verified claims reduce to standard complex arithmetic.
The proofs are correct but do not reveal novel mathematics.

**What Lean cannot address**: Physics claims (aether, over-unity, E=mc2 replacement)
have no mathematical formalization and cannot be verified or falsified by Lean 4.

## Proof Compilation Status

| File | Status | `sorry` count |
|------|--------|---------------|
| foundations/basic_operators.lean | Compiles | 0 |
| telegraph/telegraph_equation.lean | Compiles with sorry | 2 |
| polyphase/ | Empty | N/A |
| integration/ | Empty | N/A |
