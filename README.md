# Formal Verification of Alternative Mathematical Frameworks

Machine-verified dimensional scaffold from Dollard's versor algebra through Clifford algebras to SO(14), built in [Lean 4](https://lean-lang.org/) with mathlib. One certified Lie algebra morphism (su(5) →ₗ⁅ℝ⁆ so(10)); remaining links are dimensional consistency checks with algebraic upgrades in progress.

**62 proof files. ~2,800 verified declarations. Zero `sorry` gaps. Zero build errors.**

## What This Is

A research project that applies interactive theorem provers (Lean 4) to claims from alternative mathematical frameworks. Starting from Eric Dollard's "versor algebra," we extract formalizable claims, prove or disprove each one, and trace the algebraic path from the source claims through Clifford algebras to gauge unification.

Includes the first machine-verified so(10) spinor representation homomorphism in any interactive theorem prover: 1,980 bracket equations verified by `native_decide` over exact rational arithmetic.

Five Lie algebras — so(1,3), sl(3), sl(5), su(5), so(10) — carry certified `LieRing` and `LieAlgebra ℝ` instances via `Mathlib.Algebra.Lie.Basic`, connecting the hand-built structures to mathlib's type system. Includes the project's first certified `LieHom`: su(5) →ₗ⁅ℝ⁆ so(10).

## What This Proves — And What It Doesn't

Lean's kernel guarantees that every declaration in this project type-checks against its stated type. What that means depends on the declaration:

**Algebraic structure proofs (~250 declarations).** Jacobi identities, Lie bracket computations, subalgebra closures, embedding homomorphisms, and root system identifications. These are genuine algebraic theorems — the `ring` and `ext` tactics close them, but the *content* is mathematical: su(5) is a Lie subalgebra of so(10), the Lorentz algebra satisfies Jacobi, etc.

**Dimensional consistency checks (~1,500 declarations).** Verified arithmetic: dim so(14) = 91, the 16-plet decomposes as 1+5+10, anomaly traces sum to zero. These are correct and machine-verified, but mathematically straightforward — Lean confirms the arithmetic that a physicist would check by hand.

**Definitional infrastructure (~250 declarations).** Structure definitions, typeclass instances, and setup code. No theorems — just the scaffolding that lets the proofs compile.

**What is NOT proved here:**
- This is not a unified field theory. It is an algebraic scaffold that verifies the dimensional and structural consistency of a path toward unification.
- The Dollard starting point is historical and pedagogical. The mathematical content stands independently of Dollard's claims.
- Steps 7-11 (dynamics) are axiomatized structures — properties are verified from axioms, not derived from first principles.
- Step 15 (mass gap) is stated, not proved. That's the Millennium Prize problem.
- Physical identifications (which representations correspond to which particles) are axiomatized, not derived. This is standard in the field: no GUT formalization derives these identifications from first principles.

See `docs/PROOF_CLASSIFICATION.md` for per-file analysis and `docs/SIGNATURE_ANALYSIS.md` for which proofs depend on metric signature.

## Results Summary

| Category | Count | Example |
|----------|-------|---------|
| Verified | 7 | Z4 group structure, polyphase formula, telegraph expansion |
| Disproved | 2 | Versor form equivalence (sign error), four-factor independence |
| Algebraic Necessity | 1 | h = -1 forced by core axioms |
| Ambiguous | 1 | h = sqrt(+1)^(1/2) notation |
| Unfalsifiable | 5 | Physics/empirical claims |

## Algebraic Hierarchy

```
Z4 ··> Cl(1,1) ··> Cl(3,0) ··> Cl(1,3) ··> SU(5) ==> SO(10) ··> SO(14) ··> E8
 |        |          |           |           |          |          |         |
4th     Wave      Pauli      Spacetime   Georgi-   Grand     Full       Three
roots   decomp    algebra    algebra     Glashow   unified   unification generations
                  F=E+IB    nabla F=J   15-plet   16-plet   91 gens    via SU(9)

==>  Certified LieHom (bracket preservation proven)
··>  Dimensional consistency verified (morphism upgrade in progress)
```

## Crown Jewel Theorems

The headline results — each a genuine theorem, not dimensional arithmetic:

| Theorem | What It Proves |
|---------|----------------|
| `spinor_rep_homomorphism` | [ρ(X),ρ(Y)] = ρ([X,Y]) for all 990 so(10) basis pairs |
| `three_generation_theorem` | SO(14) impossibility + E₈ yields exactly 3 generations |
| `killing_form_unique` | Schur's Lemma → Killing form uniqueness (first in any ITP) |
| `complete_chirality_factorization` | Chirality emerges from 4D×10D unification |

<details>
<summary>Full theorem table (27 entries)</summary>

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
| `wilson_chirality` | `massive_chirality_definition` | Wilson's Λ³(C⁹) chirality argument, machine-verified |
| `massive_chirality_definition` | `massive_chirality_definition` | 12-part: two-level chirality definition (Def B + Def D) |
| `complete_massive_chirality_skeleton` | `massive_chirality_definition` | 20-part: full chirality certificate |
| `odd_nine_all_chiral` | `massive_chirality_definition` | All exterior powers of C⁹ are chiral (9 is odd) |
| `complete_chirality_factorization` | `chirality_factorization` | Chirality emerges from 4D×10D unification |
| `lagrangian_uniqueness` | `lagrangian_uniqueness` | Yang-Mills Lagrangian form is unique (Killing) |
| `killing_form_unique` | `schur_killing_uniqueness` | Schur's Lemma → Killing form uniqueness (Route A) |
| `spinor_rep_homomorphism_real/imag` | `spinor_rep_homomorphism` | [ρ(X),ρ(Y)] = ρ([X,Y]) for all 990 so(10) basis pairs |
| `d_squared_zero` | `differential_forms` | d²=0 from mathlib's extDeriv (replaces axiom) |
| `clifford_relation_cl13` | `cl31_maxwell` | Full Cl(1,3) Clifford relation verified from 256-term mul table |
| `comm_metric_independent` | `gauge_gravity` | Lie bracket is definitionally metric-independent (`rfl` proof) |
| `killingForm_eq_4_innerProduct` | `gauge_gravity` | Killing form = 4× Lorentzian inner product (signature enters HERE) |
| `signature_split` | `dirac` | 6 bivector squares bundle: boost²=+1, rotation²=-1 (Lorentzian witness) |

</details>

## Publications

| Paper | Venue | Status | About |
|-------|-------|--------|-------|
| [Paper 1](paper/paper1.tex) | CICM 2026 (Springer LNAI) | Submitted | Lean 4 as verification tool for alternative math frameworks |
| [Paper 2](paper/paper2.tex) | Advances in Applied Clifford Algebras | Submitted | Fortescue → Cartan-Weyl: unifying symmetrical components and root spaces |
| [Paper 3](paper/paper3.tex) | Physical Review D | In preparation | SO(14) machine-verified algebraic scaffold with phenomenological predictions |
| [Paper 4](paper/paper4.tex) | Letters in Mathematical Physics | In preparation | Three generations from E₈ via SU(9)/Z₃ |

## Build

```bash
# Install Lean 4 via elan (one-time)
curl https://elan-init.lean-lang.org/elan-init.sh -sSf | sh

# Fetch mathlib cache (first time, takes a few minutes)
lake update

# Build all proofs
lake build
```

Requires: Lean 4.29+, mathlib (fetched automatically by `lake update`).

## Proof Files

All proofs are in `src/lean_proofs/`. Entry points by interest:

- **Mathematician**: start with `schur_killing_uniqueness` (Schur → Killing uniqueness) and `spinor_rep_homomorphism` (990-bracket proof)
- **Physicist**: start with `gauge_gravity` (EM/gravity share algebraic structure) and `three_generation_theorem` (why 3 generations)
- **Formalist**: start with `differential_forms` (d²=0 from mathlib) and `cl31_maxwell` (256-term Clifford relation)

<details>
<summary>Full file listing by category</summary>

**Foundations** (Dollard verification):
`basic_operators`, `algebraic_necessity`

**Polyphase/Telegraph**:
`polyphase_formula`, `telegraph_equation`

**Clifford Algebras**:
`cl11`, `cl30`, `cl31_maxwell`, `gauge_gravity`, `dirac`

**Gauge Theory**:
`su3_color`, `su3_cartan_weyl`, `su5_grand`, `su5_lie_structure`, `su5c_compact` (compact form), `su5c_so10_liehom` (certified LieHom), `su5_subalgebra`, `georgi_glashow`, `lie_bridge`, `so10_grand`, `su5_so10_embedding`

**Unification**:
`unification`, `unification_gravity`, `spinor_matter`, `grand_unified_field`, `so14_unification`, `so14_anomalies`, `so14_breaking_chain`, `symmetry_breaking`

**Three-Generation Problem** (E₈ ⊃ SU(9)/Z₃):
`spinor_parity_obstruction`, `e8_embedding`, `e8_su9_decomposition`, `e8_generation_mechanism`, `three_generation_theorem`, `e8_chirality_boundary`, `j_anomaly_free_eigenspaces`, `exterior_cube_chirality`, `massive_chirality_definition`, `chirality_factorization`

**Representations**:
`spinor_rep` (Cartan eigenvalues, chirality, traces), `spinor_rep_full` (all 45 generators as 16×16 matrices), `spinor_rep_homomorphism` (990-bracket homomorphism proof via native_decide)

**Dynamics**:
`yang_mills_energy`, `covariant_derivative`, `rg_running`, `bianchi_identity`, `yang_mills_equation`, `yukawa_couplings`, `lagrangian_uniqueness`, `differential_forms`, `wedge_product` (axiomatized exterior product), `gauge_connection` (Lie-valued forms, F=dA+[A,A]), `bianchi_from_principles`, `yang_mills_variation`

**Spectral Theory**:
`grade2_lie_algebra`, `casimir_eigenvalues`, `casimir_spectral_gap`, `block_tridiagonal`, `schur_killing_uniqueness`

**Quantum**:
`hilbert_space`, `mass_gap`

**Lagrangian**:
`circuit_action`

</details>

## FAQ

**Is this a unified field theory?**
No. It is a machine-verified algebraic scaffold — it proves that the dimensional and structural relationships along the chain Z₄ → Cl(1,3) → SO(10) → SO(14) → E₈ are mathematically consistent. Whether this describes nature is a separate (and open) question.

**How do you get three generations?**
Via the E₈ ⊃ SU(9)/Z₃ embedding. The `three_generation_theorem` proves that SO(14) alone *cannot* produce 3 generations (its spinor yields only 1), but E₈'s 248-dimensional adjoint decomposes under SU(9) to give exactly 3 copies of the Standard Model fermion content. This follows Wilson's construction.

**What's speculative?**
Everything tagged [CP] (Candidate Physics) in the codebase. The algebraic proofs [MV] are rigorous; the physical interpretation is not. See `docs/PROOF_CLASSIFICATION.md` for the full tagging system.

**Can I use these proofs?**
Yes. All Lean proof files are original work. Source materials in `source_materials/` are referenced under fair use for academic analysis.

## Project Structure

| Directory | Contents |
|-----------|----------|
| `src/lean_proofs/` | Lean 4 proof files (the core work) |
| `paper/` | LaTeX sources and compiled PDFs (papers 1-4) |
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

## Author

Ian M. Arnoldy
