# Physics-Math Friction Catalog

Where formalization constrained, corrected, or redirected physics assumptions.

Every instance below records a specific point where physics pointed one direction
and mathematics pushed back. These are the load-bearing findings of the project —
and the natural connective tissue for the papers.

## Category A: Dollard-Specific Corrections

### A1. Versor Form Sign Error (DISPROVEN)
- **Physics said:** Dollard's versor form `ZY = h(XB+RG) + j(XG-RB)` is equivalent to the standard telegraph equation
- **Math said:** With h=-1 (forced by axioms), real part is `-(XB+RG)`, not `+(RG+XB)`. Sign flip. Not equivalent.
- **Adjusted:** Three repair strategies tested, all fail. Irreparable within Dollard's framework.
- **Lean:** `telegraph_equation.lean` (0 sorry)
- **Implication:** Dollard's core claim is mathematically false. The standard form is correct.

### A2. h=-1 Algebraic Necessity (REDUCED TO TRIVIAL)
- **Physics said:** Dollard's h operator is novel algebraic structure
- **Math said:** From j²=-1, hj=k, jk=1: derive k=j⁻¹=-j, then h=k/j=(-j)/j=-1. Over ANY field.
- **Adjusted:** Entire versor algebra reduces to Z₄ (fourth roots of unity). h=-1, j=i, k=-i. No novelty.
- **Lean:** `algebraic_necessity.lean` (0 sorry)
- **Implication:** Path to novel physics goes through Clifford algebras (Cl(1,1)→Cl(1,3)), not versor modification.

## Category B: Three-Generation Obstructions (7 mechanisms killed)

### B1. Z₂×Z₂ Klein Four Blocks 3+1 (IMPOSSIBILITY THEOREM)
- **Physics said:** SO(4) torus Z₂×Z₂ splits 64⁺ spinor into sectors giving 3+1 mass hierarchy
- **Math said:** SO(4) eigenvalues are {a+b, a-b, -a+b, -a-b}. To get 3 equal: a+b=a-b → b=0 and a+b=-a+b → a=0. All collapse to zero.
- **Adjusted:** Proved impossibility via exhaustive search over 2,025 generator combinations.
- **Script:** `yukawa_definitive.py`
- **Implication:** Z₂×Z₂ algebraic structure FORCES 2+2 pairing, never 3+1. Not fixable by parameter tuning.

### B2. Gresnigt S₃ Sedenion Extension (CHIRALITY MIXING)
- **Physics said:** Import Gresnigt's sedenion S₃ mechanism (proven in Cl(8)) to SO(14) via Cl(14)=Cl(8)⊗Cl(6)
- **Math said:** Sedenion automorphisms don't commute with Γ₈. Off-diagonal blocks U±=2.449. Extension to Cl(14) has leakage |P₋UP₊|=6.928.
- **Adjusted:** KC-5 fires. Mechanism dead. Fallback: orbifold (Kawamura-Miura).
- **Script:** `cl6_su3_generations.py`
- **Implication:** S₃ triality in SO(8) cannot port to SO(14) through tensor products. Structural obstruction.

### B3. E₈ SO(14)×SU(3)×E₆ Dimension Mismatch (INTERSECTION FAILS)
- **Physics said:** E₈ contains both SO(14)×U(1) and SU(3)×E₆. Under E₆: 248→(3,27)+(3̄,27̄). Match to SO(14) matter?
- **Math said:** SO(14) spinor 64⁺ branches as (16,(2,1))+(16̄,(1,2)) under SO(10)×SO(4). Fragments as 16+16+32 across E₆ Z₃ grades. 27 of E₆ cannot contain 64 of SO(14).
- **Adjusted:** Intersection algebra is SU(7), not a three-generation structure.
- **Script:** `e8_so14_intersection.py`
- **Implication:** E₈ does NOT naturally encode 3+1 generations when restricted to SO(14).

### B4. Cl(6) SU(3) Family Symmetry (GAUGE INCOMPATIBLE)
- **Physics said:** Cl(6) inside Cl(14)=Cl(8)⊗Cl(6) has natural SU(3). Under it: 64⁺=16×1+16×3. Three families!
- **Math said:** SU(3) EXISTS and preserves chirality. But does NOT commute with SO(10). Overlap in directions 9-10.
- **Adjusted:** Documented as gauge-incompatible. Can't have both gauge invariance and family structure.
- **Implication:** Hidden Clifford symmetries don't automatically become viable GUT mechanisms.

### B5. A₄ Discrete Flavor in SO(4) (WRONG REPRESENTATION TYPE)
- **Physics said:** SO(4)=SU(2)×SU(2) hosts A₄ with 3-dim irreps → three families
- **Math said:** Family space from SO(14) branching is (2,1)+(1,2) — spinorial doublets. Under diagonal SU(2): 2+2, not 3+1. Tensor 2⊗2=3⊕1 applies to vectors, not spinors.
- **Adjusted:** Mechanism fails. Wrong representation type.
- **Script:** `three_gen_remaining_avenues.py`
- **Implication:** Discrete flavor symmetries require vectorial reps; fermion family space is spinorial.

### B6. 331 Anomaly Mechanism (VANISHES IN GUT)
- **Physics said:** Pisano-Pleitez 331 model forces N_gen=N_color=3 via horizontal anomaly cancellation
- **Math said:** N_gen=N_color constraint is specific to standalone 331 gauge theory. In GUT embedding, anomaly cancellation is automatic. The constraint that forces 3 disappears.
- **Adjusted:** Documented as intrinsically non-GUT. Cannot port to SO(14).
- **Implication:** Physics principles valid in isolated models don't universally transfer to unified frameworks.

### B7. Spinor Parity Obstruction (2^k ≠ 3)
- **Physics said:** SO(14)→SO(10)×SO(4) decomposition should yield three copies of the 16
- **Math said:** 64⁺ branches as (16,2)+(16*,2). Multiplicity of 16 is exactly 2. 3∤2. All embeddings conjugate (Grassmannian transitivity), no escape.
- **Adjusted:** Three generations cannot arise from SO(14) algebra alone. Need extrinsic mechanisms.
- **Lean:** `spinor_parity_obstruction.lean` (0 sorry)
- **Implication:** SO(14) has the same three-generation problem as SO(10). Formalization proved this rigorously.

## Category C: Signature and Representation Issues

### C1. so(1,3) ≇ so(4) (SIGNATURE MATTERS)
- **Physics said:** Embed the Lorentz group so(1,3) into SO(14)
- **Math said:** so(1,3) ≅ sl(2,ℂ)_ℝ (non-compact). so(4) ≅ su(2)⊕su(2) (compact). Boost-rotation cross-terms differ by sign.
- **Adjusted:** Embedded SO(4) instead. Documented in SIGNATURE_ANALYSIS.md.
- **Lean:** `so4_gravity.lean`, `so4_so14_liehom.lean` (0 sorry)
- **Implication:** Physics hand-waves "Wick rotation." Formalization forces the distinction. Known since Cartan 1914.

### C2. 16-dim Spinor Irreducibly Complex
- **Physics said:** so(10) acts on real 16-dim spinor space (fermions live in real spacetime)
- **Math said:** 16-dim spinor rep has no real structure. No real 16×16 matrices represent it faithfully.
- **Adjusted:** Split into real (R) and imaginary (J) parts from Cl(5,5). Verified 990+990=1,980 brackets via native_decide.
- **Lean:** `spinor_rep_homomorphism.lean` (0 sorry)
- **Implication:** "Real fermions" is physics intuition. The mathematics is irreducibly complex.

### C3. Cl(5,5) ↔ Cl(10,0) Basis Mismatch (180 BRACKET FAILURES)
- **Physics said:** Use Cl(5,5) directly (real Clifford algebra matching η-metric)
- **Math said:** Bracket formula [γ_i,γ_j]=2η_{ij} gives 180 mismatches out of 990 bracket pairs
- **Adjusted:** Found basis transformation γ'_i = γ_i (odd i), i·γ_i (even i). Converts Cl(5,5)→Cl(10,0). All 990 brackets verified.
- **Implication:** Different Clifford signatures require different bracket formulas. Physics choice of signature affects computation.

### C4. Chirality Γ²=-I (EIGENDECOMPOSITION FAILS)
- **Physics said:** Use pseudoscalar Γ=γ₁γ₂...γₙ to define chirality via eigendecomposition
- **Math said:** For Cl(10,0): Γ²=-I, not +I. Volume element not real-diagonalizable.
- **Adjusted:** Use iΓ instead (Hermitian, eigenvalues ±1). Algebraically valid but physically unnatural.
- **Lean:** `massive_chirality_definition.lean`
- **Implication:** Massive chirality remains open. Standard geometric approach doesn't work cleanly.

## Category D: Formalization Reveals Hidden Assumptions

### D1. Arithmetic ≠ Algebraic Proof
- **Physics said:** 91=45+6+40 proves SO(14) decomposes into gauge+gravity+mixed
- **Math said:** `(45:ℕ)+6+40=91 := by norm_num` is arithmetic. The actual decomposition [so(10),so(4)]=0 requires closing brackets, not summing dimensions.
- **Adjusted:** Three-tier classification: [MV-structural], [MV-arithmetic], [MV-definitional]
- **Implication:** Dimensional arithmetic is necessary but never sufficient for algebraic claims.

### D2. Anomaly Trace Cyclicity Error
- **Physics said:** Tr(ABC)=Tr(CAB) by trace cyclicity, therefore Tr(A{B,C})=0
- **Math said:** CBA is anti-cyclic, not cyclic. Tr(ABC)≠Tr(CBA) in general. Correct: Tr(ABC)=-Tr(CBA) by transpose+antisymmetry, then Tr(CBA)=Tr(ACB) by genuine cyclicity.
- **Adjusted:** Corrected proof in `anomaly_trace.lean`
- **Lean:** `anomaly_trace.lean` (0 sorry)
- **Implication:** Sign error in standard proof sketch. Lean caught it.

### D3. δS=0 Is Honest Axiom
- **Physics said:** Lagrangian L=Tr(F²) should be derivable from symmetry
- **Math said:** Variational principle δS=0 is external physics, not derivable from Lie algebra structure.
- **Adjusted:** Accepted as honest axiom in `yang_mills_variation.lean`. Bianchi is derived (from Jacobi), Lagrangian is not.
- **Implication:** Lean formalization cannot prove SO(14) is correct — only that IF L=Tr(F²) on SO(14) bundle, THEN consistency conditions hold.

### D4. Wedge Product for Lie-Valued Forms (AXIOMATIZED)
- **Physics said:** F=dA+[A,A] requires wedge product on Lie-valued forms
- **Math said:** Mathlib has d²=0 but NOT Lie-valued wedge. Had to axiomatize: 6 axioms.
- **Adjusted:** Left axiomatized. Upgrade path exists via mathlib but deferred.
- **Lean:** `wedge_product.lean`
- **Implication:** Gauge theory formulation F=dA+[A,A] not fully formalizable yet. Physics "foundation" has a gap.

### D5. SO(14) = SO(10) for Coupling Unification (NO ADVANTAGE)
- **Physics said:** SO(14) might improve coupling unification over SO(10)
- **Math said:** Mixed (10,4) bosons contribute equally to all three SM beta functions. SO(14) unification miss: 3.3% (desert), 0.88% (multi-scale). Identical to SO(10).
- **Adjusted:** KC-FATAL-5 and KC-FATAL-6 both PASS but show no improvement.
- **Script:** `so14_rg_unification_v2.py`
- **Implication:** SO(14) does not improve low-energy predictions. Any advantage must come from other mechanisms.

### D6. Spinor Representation Only 5/45 Complete
- **Physics said:** so(10) acts on 16-dim spinors via 45 generators
- **Math said:** Only 5 diagonal (Cartan) generators have explicit matrix representations. 40 off-diagonal generators remain.
- **Lean:** `spinor_rep.lean` (partial)
- **Implication:** "Full spinor representation" claim was premature. Only Cartan subalgebra verified.

## Category E: Open Boundaries Identified

### E1. Massive Chirality in E₈(-24) (OPEN PROBLEM)
- **Physics said:** Standard chirality (γ₅/Γ₁₄) separates left/right in E₈(-24) spinor content
- **Math said:** NONE of the standard operators work. Γ₁₄ mixes with SU(9). J operator (Z₃ automorphism) has J²=-1 and commutes with SU(9), but is NOT γ₅. Distler-Garibaldi theorem prevents net chirality.
- **Adjusted:** KC-E3 status: BOUNDARY. The J operator is genuinely novel. Chirality requires new quantum number.
- **Lean:** `massive_chirality_definition.lean`, `exterior_cube_chirality.lean`
- **Implication:** SM chirality is not explained by any single Clifford operator in E₈(-24). Open problem with precisely defined boundary.

## Summary Statistics

| Category | Count | Pattern |
|----------|-------|---------|
| A: Dollard corrections | 2 | Core claims disproven by algebra |
| B: Three-gen obstructions | 7 | Every proposed mechanism killed by formalization |
| C: Signature/rep issues | 4 | Physics imprecision caught |
| D: Hidden assumptions | 6 | Formalization reveals what physics assumed silently |
| E: Open boundaries | 1 | Precisely identifies where math runs out |
| **TOTAL** | **20** | |

## What This Catalog IS

Each entry is a place where the physics-math bijection produced a finding:
- Physics pointed a direction
- Math checked whether the direction was consistent
- When it wasn't, the adjustment constrained, corrected, or redirected the physics

These findings are the NATURAL CONNECTIVE TISSUE for the papers. They are not
post-hoc interpretation — they are the actual reasoning path of the project.

## What This Catalog IS NOT

- A claim that we "fixed" mainstream GUT physics (we didn't — mainstream results mostly hold)
- A claim that formalization replaces physics (it constrains, it doesn't replace)
- A claim that all physics assumptions were wrong (most were right; the imprecise ones got caught)

## Files Referenced

| Instance | Key File(s) |
|----------|------------|
| A1 | `telegraph_equation.lean` |
| A2 | `algebraic_necessity.lean` |
| B1 | `yukawa_definitive.py` |
| B2 | `cl6_su3_generations.py` |
| B3 | `e8_so14_intersection.py` |
| B4 | `cl6_su3_generations.py` |
| B5 | `three_gen_remaining_avenues.py` |
| B7 | `spinor_parity_obstruction.lean` |
| C1 | `so4_gravity.lean`, `so4_so14_liehom.lean` |
| C2 | `spinor_rep_homomorphism.lean` |
| C3 | `spinor_rep_homomorphism.lean` |
| C4 | `massive_chirality_definition.lean` |
| D1 | Various `_unification.lean` files |
| D2 | `anomaly_trace.lean` |
| D3 | `yang_mills_variation.lean` |
| D4 | `wedge_product.lean` |
| D5 | `so14_rg_unification_v2.py` |
| D6 | `spinor_rep.lean` |
| E1 | `massive_chirality_definition.lean`, `exterior_cube_chirality.lean` |
