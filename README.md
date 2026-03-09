# Formal Verification of Alternative Mathematical Frameworks

Machine-verified algebraic scaffold from Dollard's versor algebra through Clifford algebras to SO(14), built in Lean 4 with mathlib.

## What This Is

A research project that applies interactive theorem provers (Lean 4) to claims from alternative mathematical frameworks. Starting from Eric Dollard's "versor algebra," we extract formalizable claims, prove or disprove each one, and trace the algebraic path from the source claims through Clifford algebras to gauge theory.

**35 proof files. ~878 theorems. Zero `sorry` gaps. Zero build errors.**

## Results Summary

| Category | Count | Example |
|----------|-------|---------|
| Verified | 7 | Z4 group structure, polyphase formula, telegraph expansion |
| Disproved | 2 | Versor form equivalence (sign error), four-factor independence |
| Algebraic Necessity | 1 | h = -1 forced by core axioms |
| Ambiguous | 1 | h = sqrt(+1)^(1/2) notation |
| Unfalsifiable | 5 | Physics/empirical claims |

## Algebraic Hierarchy (all machine-verified)

```
Z4 --> Cl(1,1) --> Cl(3,0) --> Cl(1,3) --> SU(5) --> SO(10) --> SO(14)
 |        |          |           |           |          |          |
4th     Wave      Pauli      Spacetime   Georgi-   Grand     Full
roots   decomp    algebra    algebra     Glashow   unified   unification
                  F=E+IB    nabla F=J   15-plet   16-plet   91 generators
```

## Publications

| Paper | Venue | Status |
|-------|-------|--------|
| Formal Verification of Alternative Mathematical Frameworks: A Case Study Using Lean 4 | CICM 2026 (Springer LNAI) | Submitted |
| Character Decomposition from Fortescue to Cartan-Weyl (cross-domain identities) | Advances in Applied Clifford Algebras | In preparation |

## Build

```bash
# Install Lean 4 via elan (one-time)
curl https://elan-init.lean-lang.org/elan-init.sh -sSf | sh

# Build all proofs
lake build
```

Requires: Lean 4.29+, mathlib (fetched automatically by `lake build`).

## Proof Files

All proofs are in `UFT/`:

**Foundations** (Dollard verification):
`BasicOperators`, `AlgebraicNecessity`, `TelegraphEquation`, `PolyphaseFormula`

**Clifford Algebras**:
`Cl11`, `Cl30`, `Cl31Maxwell`, `GaugeGravity`, `Dirac`

**Gauge Theory**:
`SU3Color`, `SU5Grand`, `GeorgiGlashow`, `LieBridge`, `SO10Grand`, `SU5SO10Embedding`

**Unification**:
`Unification`, `UnificationGravity`, `SpinorMatter`, `GrandUnifiedField`
`SO14Unification`, `SO14Anomalies`, `SymmetryBreaking`

**Dynamics**:
`YangMillsEnergy`, `CovariantDerivative`, `RGRunning`, `BianchiIdentity`
`YangMillsEquation`, `YukawaCouplings`

**Spectral Theory**:
`Grade2LieAlgebra`, `CasimirEigenvalues`, `CasimirSpectralGap`, `BlockTridiagonal`

**Quantum**:
`HilbertSpace`, `MassGap`

**Lagrangian**:
`CircuitAction`

## Project Structure

| Directory | Contents |
|-----------|----------|
| `UFT/` | Lean 4 proof files (the core work) |
| `paper/` | LaTeX sources and compiled PDFs |
| `docs/` | Architecture, decisions, research notes |
| `source_materials/` | Dollard's original PDFs (read-only reference) |
| `src/experiments/` | Python verification scripts (pre-registered) |
| `research/` | Literature surveys and analysis |

## Research Methodology

Every experiment is pre-registered with falsification criteria before execution. Claims are tagged:
- **[MV]** Machine-Verified (Lean proof exists)
- **[CO]** Computational Only (Python, not formally verified)
- **[CP]** Candidate Physics (speculative, clearly marked)
- **[SP]** Standard Physics (textbook result)
- **[OP]** Open Problem

See `CLAUDE.md` for full development rules and `docs/decisions/` for architectural decision records.

## License

All Lean proof files are original work. Source materials in `source_materials/` are referenced under fair use for academic analysis.

## Author

Ian M. Arnoldy -- Independent Researcher
