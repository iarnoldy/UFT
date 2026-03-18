# Investigation Status — Dollard Exact Construction

**Last Updated**: 2026-03-17 (Session: dollard-exact-z4-investigation)
**Overall Status**: RESOLVED — Zero-error finding explained as IEEE 754 coincidence

## What Is Proven

| Claim | Status | Evidence | Confidence |
|-------|--------|----------|------------|
| h = -1 | PROVEN | Lean proof + SymPy + 3 councils | 99.9% |
| Algebra = Z4 = {1, j, -1, -j} | PROVEN | Lean + SymPy + 3 councils | 99.9% |
| Versor form ZY wrong | PROVEN | 7/7 test cases, wrong sign | 100% |
| Quaternary identities (u-v=cos etc) | PROVEN | Verified to 10^-15 | 100% |
| Stride-4 Taylor saves 40% FLOPs | PROVEN | Benchmarked, algorithmic | 99% |

## What Was Incorrectly Analyzed (Three Councils)

| Council | What It Tested | What It Should Have Tested |
|---------|---------------|--------------------------|
| quaternary-performance | Mod-4 of real e^t (bare vector) | Dollard's epsilon^j with operators |
| lifted-representation | DPQA on bare real 4-vector | Z4 algebra multiplication with operators |
| dollard-pure-construction | Dollard's algebra → Z4 (CORRECT) | N/A — this council was right |

The councils' eigenvalue analysis (spectral radius e^theta > 1, exponential error growth)
was CONFIRMED by the systematic sweep. The Z4 path does exhibit exponential error growth.

## The Finding — NOW RESOLVED

### Original observation (pre-investigation)

Zero error at n=500, 1000 (theta=pi/100) while standard rotation accumulated ~4e-14.
Scalar parts u, nu both ~11 trillion, difference = 1.0 exactly.

### Experiment 001: Systematic N-Sweep (ALL n from 1 to 1000)

Revealed the full picture that selected sampling had obscured:

| Metric | Dollard Z4 | Standard rotation |
|--------|-----------|-------------------|
| Better at N of 1000 | **19** | **979** |
| Mean error | 1.04e-4 | 1.36e-14 |
| Zero-error points | {400, 500, 600, 1000} | {1, 56} |

Z4 error grows exponentially between zero-error points. At n=950: error = 1.46e-3.
Standard rotation: 4.7e-15 at the same point. Ten orders of magnitude difference.

### Experiment 002: Component Error Analysis

**Mechanism identified**: At zero-error points, err_u == err_nu EXACTLY (bitwise identical).
The rounding errors in both components are forced into equality at those chain lengths.
Subtraction u-nu then cancels the error perfectly.

At non-zero pi multiples (n=100,200,300,700,800,900), err_u != err_nu. The difference
IS the cos error.

### Cross-theta comparison (DECISIVE)

| Theta | Zero-error n | Zero-error angles |
|-------|-------------|-------------------|
| pi/100 | {400, 500, 600, 1000} | {4pi, 5pi, 6pi, 10pi} |
| pi/50 | {28, 29, 250} | {0.56pi, 0.58pi, 5pi} |
| pi/200 | {1, 21, 27} | {0.005pi, 0.105pi, 0.135pi} |
| pi/1000 | {1, 2, 560} | {0.001pi, 0.002pi, 0.56pi} |

**No common pattern.** Different thetas produce zero-error at completely different angles
AND different step counts. The zeros are not predictable from total angle or chain length.

### Verdict

**Hypothesis (B) confirmed: floating-point coincidence.** The zero-error points are where
accumulated IEEE 754 rounding errors in u and nu happen to align bitwise, specific to each
theta value. Not a structural property of Z4 algebra. Not predictable. Not a computational
advantage (standard rotation wins 979/1000).

Tag: [CO] → **RESOLVED as IEEE 754 artifact.**

## What Remains

The algebraic results are unchanged and valid:
- h = -1 (Lean-verified)
- Algebra = Z4 (multi-method verified)
- Dollard's quaternary expansion works exactly as described (eq 18-82)
- The chaining operation [OUR APPLICATION] is mathematically sound but numerically inferior

The investigation question is closed. The Lean proofs in the sibling repo are unaffected.
