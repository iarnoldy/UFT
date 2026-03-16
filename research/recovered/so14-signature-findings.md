# SO(14) Signature Analysis Research -- Recovered from Session Transcripts

## Source
Recovered from JSONL session transcripts on 2026-03-14.
Primary session: `22571151-c83d-482c-8ee8-1d07656f6997` (Bridge implementation, where
`so14-signature-analyst` subagent was dispatched).
Also: `docs/SIGNATURE_ANALYSIS.md` (updated by this session), `research/so14-gut-literature.md`
(Section 4), `docs/PHYSICS_MATH_FRICTION_CATALOG.md` (Category C).

## Summary

The `so14-signature-analyst` agent was dispatched as a background subagent in session `22571151`
(the Bridge implementation session, line 98) to analyze the Bivector vs SO14 signature mismatch.
The agent was given an "URGENT FINDING" prompt documenting the impossibility of a Bivector -> SO14
LieHom due to the so(1,3) vs so(4) non-isomorphism. The findings were incorporated into
`docs/SIGNATURE_ANALYSIS.md` during the same session.

## Findings

### 1. The so(1,3) vs so(4) Non-Isomorphism (Critical Finding)

Discovered during the Bridge implementation (session `22571151`, March 2026):

**The problem**: The original plan called for a Bivector -> SO14 LieHom (Step 1.3 of Milestone 1).
This is MATHEMATICALLY IMPOSSIBLE because:

- **Bivector type** (`gauge_gravity.lean`): implements so(1,3) (Lorentz algebra from Cl(1,3))
- **SO14 type** (`so14_grand.lean`): implements so(14,0) (compact form)
- The gravity sector (indices 11-14) in SO14 has so(4) structure constants (Kronecker deltas)
- so(1,3) uses Minkowski metric eta, so(4) uses Euclidean metric delta

**Explicit verification**:
```
Bivector: [K1, J3] = -K2     (so(1,3) bracket, eta_{11} = -1)
SO14:     [L_{11,12}, L_{12,13}] = +L_{11,13}   (so(4) bracket, delta_{22} = +1)
```
Sign difference in boost-rotation cross-terms makes them non-isomorphic as real Lie algebras.

**Algebraic fact**:
- so(4) is isomorphic to su(2) + su(2) -- compact real form
- so(1,3) is isomorphic to sl(2,R) + sl(2,R) -- split real form
- The comment in `gauge_gravity.lean` (lines 44-52) claiming "so(1,3) is isomorphic to so(4)
  as abstract Lie algebras" was MATHEMATICALLY INCORRECT and was corrected.

### 2. Resolution: SO(4) Compact Gravity Type

Instead of the impossible Bivector -> SO14 LieHom, the following was implemented:
- `so4_gravity.lean`: New SO4 type with compact so(4) brackets, certified LieRing + LieAlgebra R
- `so4_so14_liehom.lean`: Certified embedding SO4 ->_{L[R]} SO14

This gives the compact-signature gravity embedding. Physical gravity (so(1,3)) requires
so(11,3), which is documented as future work.

### 3. Proof File Classification: Signature-Independent vs Signature-Dependent

The signature-analyst's task included classifying all proof files. Results (from
`docs/SIGNATURE_ANALYSIS.md`):

**Signature-Independent (36/47 original files + 15 new files = ~77%)**:
These proofs use only algebraic structure (Lie brackets, dimensions, embeddings) that
holds in ANY real form. Changing the signature does not affect the results.

Key signature-independent results:
- All dimensional arithmetic (91 = 45 + 6 + 40, 248 = 80 + 84 + 84, etc.)
- All Lie algebra embeddings (SU5C -> SO10 -> SO14)
- Anomaly trace conditions
- Breaking chain dimensions
- Root system A4 structure
- Casimir eigenvalues

**Compact-Only (3 files, ~4%)**:
- `cl30.lean`: Cl(3,0) Pauli algebra -- specific to signature (3,0)
- `so4_gravity.lean`: so(4) compact form -- structure constants are compact-specific
- `so4_so14_liehom.lean`: Embeds so(4) into so(14,0) -- compact signature required

**Signature-Sensitive (10 files, ~21%)**:
Physical INTERPRETATION depends on signature, even though algebraic identities may hold:
- `cl31_maxwell.lean`: Maxwell's equations require Lorentzian signature
- `gauge_gravity.lean`: Bivector = so(1,3), boost/rotation split is signature-specific
- `dirac.lean`: Chirality (gamma_5) requires specific signature
- `lie_bridge.lean`: Grade-2 to so(1,3) -- specific to Cl(1,3)
- `unification_gravity.lean`: so(1,3) x so(10) in so(14) -- the so(1,3) factor is signature-specific
- `hilbert_space.lean`: Wightman axioms assume Lorentzian signature
- `mass_gap.lean`: Spectral theory in Lorentzian QFT
- `e8_chirality_boundary.lean`: Chirality depends on E8 real form
- `exterior_cube_chirality.lean`: Chirality interpretation is signature-sensitive
- `massive_chirality_definition.lean`: Chirality definitions vary across signatures

### 4. SO(14,0) vs SO(11,3) vs SO(3,11): What the Signatures Mean

From `so14-gut-literature.md`, Section 4:

| Property | SO(14,0) compact | SO(11,3) non-compact |
|----------|-----------------|---------------------|
| Lie algebra | D_7 (same) | D_7 (same) |
| Dimension | 91 | 91 |
| Spinor reality | Real (Majorana) | Real (Majorana-Weyl possible) |
| Semi-spinor dim | 64 | 64 |
| Gauge theory | Standard YM | Problematic (non-compact) |
| Gravity content | None | SO(3,1) Lorentz subgroup |
| Fermion chirality | No natural chirality | Chirality from Majorana-Weyl |

**Why (11,3) is chosen by physics**:
1. Contains SO(3,1) as subgroup -- provides Lorentz group for gravity
2. Majorana-Weyl spinors exist -- gives 64 real components matching one SM generation
3. Majorana-Weyl condition projects out mirror fermions

**Why (14,0) is used in Lean proofs**:
1. Compact groups have well-defined finite-dimensional unitary representations
2. Lie algebra structure (dimension, Casimir, root system) is the same
3. Formal verification is cleaner with compact groups
4. Physical signature choice is a downstream decision

### 5. The Distler Ghost Objection

From `so14-gut-literature.md`, Section 2 and 5:
- Non-compact gauge fields lead to negative-norm states (ghosts) unless handled carefully
- This is a genuine technical challenge for the Spin(11,3) program
- Same challenge as any gauge theory of gravity (including standard GR as Poincare gauge theory)
- Distler's specific objection: the topological phase argument is questionable because at
  accessible energies the theory must reduce to conventional QFT where Coleman-Mandula applies

**Kill condition KC-4 assessment**: CONTESTED (not killed, not confirmed)

### 6. Wick Rotation Considerations

From friction catalog C1:
- Physics hand-waves "Wick rotation" between compact and Lorentzian forms
- Formalization FORCES the distinction -- so(4) and so(1,3) have different structure constants
- A proper Wick rotation is a complexification followed by restriction to a different real form
- The algebraic identities (dimensions, embeddings) survive Wick rotation
- The physical interpretation (chirality, gravity content) does not

### 7. The Certified Chain and Its Signature

From `SIGNATURE_ANALYSIS.md`, updated during session `22571151`:
```
SU5C ->_{L[R]} SO10 ->_{L[R]} SO14 <-_{L[R]} SO4
```
ALL four morphisms in this chain use COMPACT signature (so(14,0)).
Physical gravity needs so(11,3) -- a different project.

### 8. Impact on Papers 3 & 4

From the signature-analyst's assessment (incorporated into session findings):
- **Paper 3 (PRD)**: Must explicitly state compact signature. Must NOT claim physical gravity
  content. The embedding is so(4) into so(14,0), not so(1,3) into so(14,0).
- **Paper 4 (LMP)**: E8 three-generation arguments are largely signature-independent
  (dimensional arithmetic). Chirality interpretation is signature-sensitive.
- Both papers must reference the Nesti-Percacci program for the physical Lorentzian version
  and clearly distinguish our compact algebraic verification from their physical construction.

## Cross-References

- `docs/SIGNATURE_ANALYSIS.md` -- Full classification (updated by this research)
- `docs/PHYSICS_MATH_FRICTION_CATALOG.md` -- C1: so(1,3) vs so(4) non-isomorphism
- `research/so14-gut-literature.md` -- Section 4: SO(14,0) vs SO(11,3)
- `src/lean_proofs/clifford/gauge_gravity.lean` -- Bivector type (so(1,3))
- `src/lean_proofs/clifford/so14_grand.lean` -- SO14 type (compact so(14,0))
- `src/lean_proofs/clifford/so4_gravity.lean` -- SO4 compact type (so(4))
- `src/lean_proofs/clifford/so4_so14_liehom.lean` -- Certified SO4 -> SO14 embedding
