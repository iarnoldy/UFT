# Signature Analysis

Which proofs depend on the choice of metric signature, and which are pure algebra?

## Background

The Lean proofs use compact (positive-definite) signature throughout. Physical applications
require Lorentzian signature (e.g., SO(3,11) instead of SO(14)). This document classifies
every proof file by its signature dependence.

## Classification

### Signature-Independent (36/47 files, 77%)

These proofs use only algebraic structure (Lie brackets, dimensions, embeddings) that
holds in ANY real form. Changing the signature does not affect the results.

| File | Why Signature-Independent |
|------|--------------------------|
| `basic_operators` | Z4 roots of unity — pure algebra |
| `algebraic_necessity` | Algebraic identities — no metric |
| `polyphase_formula` | Polyphase decomposition — pure algebra |
| `telegraph_equation` | Expansion identity — pure algebra |
| `cl11` | Cl(1,1) algebra — signature is part of the definition |
| `su3_color` | sl(3) Lie algebra — complex semisimple, same in all real forms |
| `su3_cartan_weyl` | Cartan-Weyl decomposition — algebraic |
| `su5_grand` | sl(5) Lie algebra — complex semisimple |
| `su5_lie_structure` | Root system A4 — signature-independent |
| `georgi_glashow` | Charge quantization, anomalies — representation theory |
| `so10_grand` | so(10) Lie algebra — compact form, but Jacobi holds in all forms |
| `su5_so10_embedding` | Lie algebra embedding — algebraic |
| `unification` | Embedding morphisms — algebraic |
| `spinor_matter` | Dimension decomposition 16=1+5+10 — arithmetic |
| `grand_unified_field` | Numerical skeleton — arithmetic |
| `so14_unification` | 91=45+6+40 — dimension counting |
| `so14_anomalies` | Trace conditions — representation theory |
| `so14_breaking_chain` | Breaking chain dimensions — algebraic |
| `symmetry_breaking` | VEV analysis — algebraic (representation theory) |
| `yang_mills_energy` | H >= 0 — algebraic positivity |
| `covariant_derivative` | Axiomatized gauge field structure |
| `bianchi_identity` | Algebraic Bianchi from Jacobi |
| `yang_mills_equation` | Axiomatized Euler-Lagrange |
| `yukawa_couplings` | Axiomatized coupling structure |
| `rg_running` | Beta coefficient arithmetic |
| `circuit_action` | Lagrangian structure — algebraic |
| `grade2_lie_algebra` | Grade-2 Lie algebra — algebraic |
| `casimir_eigenvalues` | Casimir operator — algebraic |
| `casimir_spectral_gap` | Spectral gap from Casimir — algebraic |
| `block_tridiagonal` | Matrix structure — algebraic |
| `spinor_parity_obstruction` | 3 does not divide 2 — arithmetic |
| `e8_embedding` | E8 subgroup dimensions — arithmetic |
| `e8_su9_decomposition` | 248=80+84+84 — arithmetic |
| `e8_generation_mechanism` | Generation counting — arithmetic |
| `three_generation_theorem` | Dimensional skeleton — arithmetic |
| `j_anomaly_free_eigenspaces` | Anomaly traces — arithmetic |

### Compact-Only (1/47 files, 2%)

| File | What Depends on Compact Signature |
|------|----------------------------------|
| `cl30` | Cl(3,0) Pauli algebra — specific to signature (3,0). In signature (2,1) the algebra is different. However, the algebraic identities proved are ABOUT Cl(3,0) specifically. |

### Signature-Sensitive (10/47 files, 21%)

These files contain results where the physical INTERPRETATION depends on signature,
even though the algebraic identities may hold in multiple signatures.

| File | What's Signature-Sensitive |
|------|---------------------------|
| `cl31_maxwell` | Cl(1,3) spacetime algebra — Maxwell's equations require Lorentzian signature for physical interpretation |
| `gauge_gravity` | so(1,3) Lorentz algebra — the SPLIT between boosts and rotations depends on signature (3 boosts + 3 rotations in (1,3); different split in other signatures) |
| `dirac` | Spinor structure — chirality (gamma_5) requires specific signature |
| `lie_bridge` | Grade-2 to so(1,3) — specific to Cl(1,3) |
| `unification_gravity` | so(1,3) x so(10) in so(14) — the so(1,3) factor is signature-specific |
| `hilbert_space` | Wightman axioms assume Lorentzian signature |
| `mass_gap` | Spectral theory in Lorentzian QFT |
| `e8_chirality_boundary` | Chirality depends on signature (compact vs Lorentzian E8 forms) |
| `exterior_cube_chirality` | Non-self-conjugacy is signature-independent, but chirality interpretation is signature-sensitive |
| `massive_chirality_definition` | Def B (non-self-conjugacy) is signature-independent; Def D (Z6 sector index) involves root labeling that's compatible with but not identical across signatures |

## Key Insight

**77% of the project is pure algebra.** The Lie algebra structures, dimension
decompositions, embedding homomorphisms, and anomaly cancellations hold regardless
of whether we work in compact, split, or Lorentzian signature.

The signature-sensitive files (21%) contain results where the physical interpretation
(chirality, boost/rotation split, Wightman axioms) requires a specific signature choice.
The algebraic IDENTITIES in these files often still hold — it's the physical MEANING
that changes.

The compact-only file (cl30.lean, 2%) is simply about a specific Clifford algebra
Cl(3,0) and makes no claims about other signatures.

## Implications for Physics

For the SO(14) candidate theory:
- The breaking chain SO(14) -> SM is signature-independent (algebraic)
- The coupling unification is signature-independent (arithmetic)
- The chirality definition requires care: Def B is signature-independent,
  Def D requires root classification that differs between signatures
- The gravity sector (so(1,3)) is inherently signature-specific

For the E8 three-generation result:
- The dimension counting (248=80+84+84, three copies of 16) is signature-independent
- The chirality interpretation depends on which real form of E8 is used
- Wilson's argument (Lambda^3(C^9) non-self-conjugate) is signature-independent
