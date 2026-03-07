# Architecture

## System Overview

```
  UPSTREAM (read-only)                    THIS PROJECT                    DOWNSTREAM
  ====================                   ============                    ==========

  source_materials/
  (Dollard PDFs)  --------+
                           |
  N-Phase Patent Ready     |         analysis/               src/lean_proofs/
  (1162 tests, real data)--+--->    (claim triage)    --->   (formal proofs)
                                                                  |
                                                                  v
                                                         docs/experiments/
                                                        (experiment registry)
                                                                  |
                                                                  v
                                                         src/experiments/         N-Phase
                                                        (Python runners)   --->  (depends on
                                                                  |              Track B)
                                                                  v
                                                      src/experiments/results/
                                                        (reproducible output)
```

## Evidence Pipeline

Two classes of evidence flow into claim triage:

1. **Formal (Lean 4)**: Mathematical certainty. Proofs accepted or rejected.
2. **Computational (N-Phase)**: 1162 tests across N=2..12. Machine-precision validation.
3. **Empirical (N-Phase experiments)**: Real-world datasets with statistical tests.
   EEG (p=0.033), 3-phase power (d=3.1), bearing faults, finance (negative result).

Claims in `analysis/CLAIM_TRIAGE.md` cite both formal and computational evidence.

## Data Flow

1. **Source materials** (read-only PDFs) contain Dollard's claims
2. **N-Phase evidence** (read-only) provides computational and empirical validation
3. **Analysis** extracts and triages claims with honest verdicts
4. **Lean proofs** formally verify or disprove mathematical claims
5. **Experiments** are pre-registered, then executed with Python
6. **Results** are immutable once written (protected by hook)

## Key Boundaries

- `source_materials/` is read-only reference material
- `src/lean_proofs/` only contains code that compiles (or has explicit `sorry`)
- `src/experiments/results/` is append-only (protected by `protect-results.sh`)
- `analysis/` documents must cite Lean proofs or carry UNVERIFIED tags
- `docs/decisions/` uses ADR format for architectural decisions

## Lean 4 Module Structure

```
src/lean_proofs/
  foundations/          -- h, j, k operator definitions and properties
    basic_operators.lean
  telegraph/            -- Telegraph equation verification
    telegraph_equation.lean
  polyphase/            -- Polyphase/Fortescue mathematics (to build)
  integration/          -- Cross-module consistency checks (to build)
```

## Upstream: N-Phase Patent Ready

**Path**: `C:\Users\ianar\Documents\CODING\March_2026\N_Phase_Patent_Ready`
**Status**: READ-ONLY. Complete, under validation. Patent provisional 63/996,504.
**Evidence catalog**: `source_materials/N_PHASE_EVIDENCE.md`

The N-Phase system implements the same mathematics this project formally verifies.
Its test suite and experimental results provide computational evidence that
complements Lean 4 formal proofs. Key contributions:

- 133 versor algebra tests (complete Cayley table, Z_4 confirmation)
- 491 Fortescue decomposition tests (N=2..12, cross-validated against numpy.fft)
- 175 quaternary expansion tests (then deprecated by E006a -- math correct, not useful)
- 11 real-world experiments with statistical significance testing

## Downstream: N-Phase Signal Processing

The N-Phase system depends on Track B verified mathematics.
See `CONTRIBUTING.md` for the sync protocol.
