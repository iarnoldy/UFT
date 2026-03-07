# N-Phase Patent Ready: Evidence Catalog

**Source**: `C:\Users\ianar\Documents\CODING\March_2026\N_Phase_Patent_Ready`
**Status**: Complete, under validation. Patent provisional 63/996,504 filed 2026-03-04.
**Test suite**: 1194 passing / 1 xfailed (confirmed live 2026-03-07)
**Relationship**: READ-ONLY upstream source. Do not modify. Extract evidence only.

---

## What N-Phase Proves (Computationally)

The N-Phase system implements Dollard's versor algebra and Fortescue's symmetrical
components in PyTorch with comprehensive test coverage. Its results provide
**computational validation** that complements this project's Lean 4 **formal proofs**.

---

## Evidence by Claim

### Claim 1: h, j, k as 4th Roots of Unity

**N-Phase evidence**: CONFIRMED (133 tests)
**Source files**:
- `src/versor_algebra/tests/test_operators.py` (367 lines, 133 tests)
- `src/versor_algebra/operators.py` (296 lines)

**Key results**:
- `test_j_fourth_power_is_identity()` -- J*J*J*J == ONE
- `test_j_squared_is_h()` -- J*J == H
- `test_all_16_products()` -- Complete Cayley table matches Dollard
- `test_cayley_table_is_latin_square()` -- Each element once per row/column
- `test_associativity()` -- All triples verify
- `test_commutativity()` -- Abelian group confirmed (Z_4)

**Assessment**: Confirms Lean proof findings. The versor algebra is Z_4.

### Claim 2: Telegraph Equation Expansion

**N-Phase evidence**: Not directly tested (telegraph equation not in scope)
**Note**: N-Phase focuses on signal decomposition, not transmission line analysis.

### Claim 3: Four-Factor Independence

**N-Phase evidence**: Not directly tested.

### Claim 4: Versor Form Equivalence

**N-Phase evidence**: IMPLICITLY CONFIRMS DISPROOF
**Reasoning**: The N-Phase implementation uses standard DFT matrix A_N[p,s] = omega^(ps),
NOT Dollard's claimed versor form ZY = h(XB+RG) + j(XG-RB). The system works
precisely because it uses the standard form, not the versor form. The versor form
would introduce sign errors in the real part (as the Lean proof demonstrates).

**Key observation**: `src/fortescue/decomposer.py` constructs A_N as:
```python
omega = np.exp(2j * np.pi / N)
A_N[p, s] = omega^(p*s)
```
This is standard Fortescue/DFT, not Dollard's versor form.

### Claim 5: Universal Polyphase Formula (k^n_N = exp(j*2*pi*n/N))

**N-Phase evidence**: CONFIRMED (491 tests, N=2..12)
**Source files**:
- `src/fortescue/tests/test_decomposer.py` (486 lines, 491 tests)
- `src/fortescue/decomposer.py` (180 lines)

**Key results**:
- `test_orthogonality_explicit()` -- A_N^H @ A_N = N*I_N (all N=2..12)
- `test_reconstruction_2d()` -- Lossless round-trip, NMSE < 1e-10
- `test_parseval_*()` -- Energy conservation verified
- `test_scipy_fft_cross_validation()` -- Cross-validated against numpy.fft
- `test_balanced_positive_sequence()` -- x[p]=omega^p decomposes to s=1 only
- `test_balanced_negative_sequence()` -- x[p]=omega^(-p) decomposes to s=N-1 only

**Assessment**: This computationally validates the polyphase formula that Experiment 0
(BLOCKING) targets for Lean proof. The formula is standard roots-of-unity math,
and N-Phase proves it works to machine precision.

### Claim 6: h = sqrt(+1)^(1/2) Notation

**N-Phase evidence**: CONFIRMS h = -1 interpretation
**Source**: `src/versor_algebra/operators.py` defines H = VectorOperator corresponding
to -1 in complex representation. No alternative interpretation is used.

### Claim 7: Sequence Periodicity

**N-Phase evidence**: CONFIRMED (implicit in DFT structure)
**Note**: The A_N matrix inherently encodes period-N sequences. For N=4,
the rows cycle through {1, j, h, k} as expected.

### Claim 8: Dimensional Consistency (Q = Psi * Phi)

**N-Phase evidence**: Not tested (outside signal processing scope).

### Quaternary Expansion (Additional -- not in original triage)

**N-Phase evidence**: CONFIRMED then DEPRECATED
**Source files**:
- `src/versor_algebra/tests/test_quaternary.py` (375 lines, 175 tests)

**Key results**:
- `test_closed_form_identities()` -- u,x,v,y verified to 12 decimal places
- `test_four_exponential_identities()` -- e^+theta, e^-theta, e^(j*theta), e^(-j*theta)
- `test_series_matches_closed_form()` -- Series summation matches closed forms

**Critical finding**: Experiment E006a DEPRECATED the quaternary cosh/sinh features.
They are mathematically correct but computationally redundant -- cosh/sinh encode
the same information as magnitude, and cause catastrophic condition number collapse
on real data (EEG). The math is valid; the application is not useful.

**Assessment**: This is a perfect example of honest verification. The math checks out,
but empirical testing shows it doesn't help. Mathematical correctness != practical utility.

---

## Domain-Specific Validation Results

### Where Fortescue Decomposition Works

| Domain | Result | Evidence |
|--------|--------|----------|
| 3-phase power | DOMINATES (d=3.1, p<0.001) | E008c |
| EEG motor imagery | Significant vs CSP+LDA (p=0.033) | E007 |
| Bearing fault diagnosis | Competitive (94.3%) | E002 |

### Where It Does Not Work

| Domain | Result | Evidence |
|--------|--------|----------|
| Finance | NOT MET -- no physical phase coupling | E011 |

### Implications for Track C

The N-Phase results show that Fortescue decomposition is powerful **where physical
phase structure exists** (power grids, EEG electrode arrays) and useless where it
doesn't (financial time series). This is consistent with the decomposition being
standard DFT applied to polyphase signals -- not evidence for aether, over-unity,
or other extraordinary claims.

---

## How to Use This Document

1. **Cross-reference**: When updating CLAIM_TRIAGE.md, cite specific N-Phase tests
2. **Read-only**: Never modify the N-Phase codebase from this project
3. **Computational vs Formal**: N-Phase provides computational validation (tests pass);
   this project provides formal validation (Lean proofs accepted). Both are needed.
4. **Honest reporting**: N-Phase's own experiments include honest negatives (E006a, E011).
   Follow the same standard here.
