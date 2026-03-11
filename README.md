# Formal Verification of Alternative Mathematical Frameworks

Machine-verified algebraic scaffold from Dollard's versor algebra through Clifford algebras to SO(14), built in Lean 4 with mathlib.

## What This Is

A research project that applies interactive theorem provers (Lean 4) to claims from alternative mathematical frameworks. Starting from Eric Dollard's "versor algebra," we extract formalizable claims, prove or disprove each one, and trace the algebraic path from the source claims through Clifford algebras to gauge unification.

**46 proof files. Over 1,870 verified declarations. Zero `sorry` gaps. Zero build errors.**

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
Z4 --> Cl(1,1) --> Cl(3,0) --> Cl(1,3) --> SU(5) --> SO(10) --> SO(14) --> E8
 |        |          |           |           |          |          |         |
4th     Wave      Pauli      Spacetime   Georgi-   Grand     Full       Three
roots   decomp    algebra    algebra     Glashow   unified   unification generations
                  F=E+IB    nabla F=J   15-plet   16-plet   91 gens    via SU(9)
```

## Crown Jewel Theorems

| Theorem | File | What It Proves |
|---------|------|----------------|
| `so14_dimension` | `so14_unification` | dim so(14) = C(14,2) = 91 |
| `unification_decomposition` | `so14_unification` | 91 = 45 (gauge) + 6 (gravity) + 40 (mixed) |
| `centralizer_closed` | `su5_so10_embedding` | su(5) is Lie subalgebra of so(10) |
| `H1_R12`, `coroot_1` | `su5_lie_structure` | A4 root system identified (Cartan matrix = su(5)) |
| `charge_preserves_vev` | `symmetry_breaking` | Q = T3 + Y/2 preserves Higgs VEV (photon massless) |
| `anomaly_checklist` | `so14_anomalies` | All 6 anomaly conditions satisfied |
| `yang_mills_energy_nonneg` | `yang_mills_energy` | H >= 0 (classical energy positivity) |
| `gauss_law_magnetism` | `bianchi_identity` | div B = 0 from Bianchi identity |
| `three_generation_theorem` | `three_generation_theorem` | SO(14) impossibility + E8 = exactly 3 generations |
| `complete_dimensional_skeleton` | `three_generation_theorem` | 23-part conjunction: entire chain in one theorem |

## Publications

| Paper | Venue | Status |
|-------|-------|--------|
| Formal Verification of Alternative Mathematical Frameworks: A Case Study Using Lean 4 | CICM 2026 (Springer LNAI) | Submitted |
| Character Decomposition from Fortescue to Cartan-Weyl: Unifying Symmetrical Components and Root Space Decomposition via Clifford Algebras | Advances in Applied Clifford Algebras | Submitted |
| SO(14) Unification: A Machine-Verified Algebraic Scaffold with Phenomenological Predictions | Physical Review D | In preparation |
| Three Generations from E₈: A Machine-Verified Resolution | Letters in Mathematical Physics | In preparation |

## Build

```bash
# Install Lean 4 via elan (one-time)
curl https://elan-init.lean-lang.org/elan-init.sh -sSf | sh

# Build all proofs
lake build
```

Requires: Lean 4.29+, mathlib (fetched automatically by `lake build`).

## Proof Files

All proofs are in `src/lean_proofs/`:

**Foundations** (Dollard verification):
`basic_operators`, `algebraic_necessity`

**Polyphase/Telegraph**:
`polyphase_formula`, `telegraph_equation`

**Clifford Algebras**:
`cl11`, `cl30`, `cl31_maxwell`, `gauge_gravity`, `dirac`

**Gauge Theory**:
`su3_color`, `su3_cartan_weyl`, `su5_grand`, `su5_lie_structure`, `georgi_glashow`, `lie_bridge`, `so10_grand`, `su5_so10_embedding`

**Unification**:
`unification`, `unification_gravity`, `spinor_matter`, `grand_unified_field`, `so14_unification`, `so14_anomalies`, `so14_breaking_chain`, `symmetry_breaking`

**Three-Generation Problem** (E₈ ⊃ SU(9)/Z₃):
`spinor_parity_obstruction`, `e8_embedding`, `e8_su9_decomposition`, `e8_generation_mechanism`, `three_generation_theorem`, `e8_chirality_boundary`, `j_anomaly_free_eigenspaces`, `exterior_cube_chirality`

**Dynamics**:
`yang_mills_energy`, `covariant_derivative`, `rg_running`, `bianchi_identity`, `yang_mills_equation`, `yukawa_couplings`

**Spectral Theory**:
`grade2_lie_algebra`, `casimir_eigenvalues`, `casimir_spectral_gap`, `block_tridiagonal`

**Quantum**:
`hilbert_space`, `mass_gap`

**Lagrangian**:
`circuit_action`

## Project Structure

| Directory | Contents |
|-----------|----------|
| `src/lean_proofs/` | Lean 4 proof files (the core work) |
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

Ian M. Arnoldy
