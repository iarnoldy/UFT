# Claim Triage

Honest assessment of every mathematical and physics claim from Dollard's source materials.
Each claim is tagged with its verification status and linked to evidence.

## Evidence Sources

- **Formal**: Lean 4 proofs in `src/lean_proofs/` (mathematical certainty)
- **Computational**: N-Phase Patent Ready test suite, 1194 tests (confirmed live 2026-03-07)
  (see `source_materials/N_PHASE_EVIDENCE.md` for full catalog)
- **Empirical**: N-Phase experiments on real datasets (EEG, power systems, bearing faults)

## Verdict Key

- **VERIFIED**: Lean 4 proof accepted. The math is correct.
- **DISPROVED**: Lean 4 proof shows the claim is false.
- **NOT YET VERIFIED**: Could be verified but proof not yet written.
- **AMBIGUOUS**: Source notation is unclear; multiple interpretations exist.
- **UNFALSIFIABLE**: Cannot be tested with formal methods (physics claims).
- **EXTRAORDINARY**: Would require extraordinary evidence; none exists.

---

## Track B: Mathematical Claims

### Claim 1: h, j, k as 4th Roots of Unity

| Field | Value |
|-------|-------|
| Source | Versor Algebra, Advanced Versor Algebra II-23 |
| Statement | j = sqrt(-1), j^4 = 1; h^2 = 1, h^1 = -1; k = hj = -j, jk = 1 |
| Verdict | **VERIFIED** (trivial -- standard complex arithmetic) |
| Formal evidence | `src/lean_proofs/foundations/basic_operators.lean` |
| Computational evidence | N-Phase `test_operators.py`: 133 tests, complete Cayley table, associativity, commutativity all pass. Confirms Z_4 isomorphism. |
| Note | When h = -1, the system is {1, i, -1, -i} = 4th roots of unity. This is not a novel algebraic structure; it is Z_4 under multiplication. |

### Claim 2: Telegraph Equation Expansion

| Field | Value |
|-------|-------|
| Source | Four Quadrant Theory, Lone Pine Writings |
| Statement | ZY = (R+jX)(G-jB) = (RG+XB) + j(XG-RB) |
| Verdict | **VERIFIED** (standard complex multiplication under Dollard's convention) |
| Evidence | `src/lean_proofs/telegraph/telegraph_equation.lean` (`telegraph_expansion`) |
| Sign convention | Dollard uses Y = G - jB (negative susceptance). The original proof file used Y = G + jB but claimed Dollard's result — this was CORRECTED. With Y = G - jB, the expansion is correct. With standard Y = G + jB, the result would be (RG - XB) + j(RB + XG). |
| Note | This is textbook complex algebra. Not a Dollard contribution — it's Heaviside's work from the 1880s. The sign convention choice is the only content. |

### Claim 3: Four-Factor Independence

| Field | Value |
|-------|-------|
| Source | Four Quadrant Theory |
| Statement | RG, XB, XG, RB are four independent electrical products |
| Verdict | **PARTIALLY VERIFIED** (four terms exist; "independence" is overstated) |
| Evidence | `src/lean_proofs/telegraph/telegraph_equation.lean` (`four_factors_nonzero`, `factor_constraint`) |
| Detail | The four products can all be nonzero simultaneously (existence proof). However, they satisfy the quadratic constraint (RG)(XB) = (XG)(RB) = RXGB, so they are NOT algebraically independent. Three free parameters determine four constrained products. |
| Note | The false `factors_independent_variation` theorem (which had sorry gaps) has been removed. Dollard's "independence" is better understood as: four distinct terms appear in the expansion. |

### Claim 4: Versor Form Equivalence

| Field | Value |
|-------|-------|
| Source | Advanced Versor Algebra II-23 |
| Statement | ZY = h(XB+RG) + j(XG-RB) is equivalent to the standard form |
| Verdict | **DISPROVED** |
| Formal evidence | `src/lean_proofs/telegraph/telegraph_equation.lean:85-92` |
| Computational evidence | N-Phase uses standard DFT (not versor form) in `decomposer.py`. The system works precisely because it avoids the versor form. Implicitly confirms the disproof. |
| Detail | With h = -1: h(XB+RG) = -(XB+RG), which differs from +(XB+RG) in the standard form. The real parts have opposite signs. |
| Note | This is the project's one genuine non-trivial finding. |

### Claim 5: Universal Polyphase Formula

| Field | Value |
|-------|-------|
| Source | Versor Algebra, Advanced Versor Algebra II-23 |
| Statement | k^n_N = 1^(n/N) = exp(j*2*pi*n/N) |
| Verdict | **VERIFIED** (formally, 0 sorry; computationally, 491 tests) |
| Experiment | Experiment 0 (COMPLETE) |
| Formal evidence | `src/lean_proofs/polyphase/polyphase_formula.lean` — 16 theorems, 0 sorry. Covers: omega^N=1, root generation, 3-phase (a^3=1, sum=0), 4-phase (versors={1,I,-1,-I}), periodicity, unit circle. |
| Computational evidence | N-Phase `test_decomposer.py`: 491 tests across N=2..12. Lossless reconstruction (NMSE<1e-10), orthogonality (kappa=1.0), Parseval's theorem, cross-validated against numpy.fft. |
| Empirical evidence | N-Phase E007 (EEG, p=0.033 vs CSP+LDA), E008c (3-phase power, d=3.1). The formula works on real data. |
| Note | This is the standard nth roots of unity formula. Both formally proved and computationally validated. The credit belongs to Fortescue (1918) and standard DFT theory. |

### Claim 6: h = sqrt(+1)^(1/2) Notation

| Field | Value |
|-------|-------|
| Source | Versor Algebra |
| Statement | h is defined as sqrt(+1)^(1/2) |
| Verdict | **AMBIGUOUS** (notation) / **RESOLVED** (algebraically) |
| Experiment | Experiment 1 (partially resolved by polymathic research) |
| Computational evidence | N-Phase `operators.py` defines H as VectorOperator corresponding to -1. No alternative interpretation implemented or tested. |
| Polymathic finding | The axioms j^2=-1, hj=k, jk=1 ALONE force h=-1 by pure algebra, without needing h^1=-1 or h^2=1 as additional axioms. Proof: jk=1 => k=j^{-1}=-j; hj=k=-j => h=-1. This means the notation is irrelevant -- whatever sqrt(+1)^(1/2) means, h must be -1 in any algebra satisfying Dollard's three core axioms. (97% confidence) |
| Note | Rehabilitation via Cl(1,1) or split-complex numbers requires dropping jk=1 (and commutativity), which changes the algebra entirely. The notation remains ambiguous, but the value is forced. |

### Claim 7: Sequence Periodicity

| Field | Value |
|-------|-------|
| Source | Advanced Versor Algebra II-23 |
| Statement | Forward sequence 1,j,h,k has period 4; reverse sequence 1,k,h,j has period 4 |
| Verdict | **VERIFIED** (trivial -- defined to be periodic) |
| Evidence | `src/lean_proofs/foundations/basic_operators.lean:82-84` |
| Note | The sequences are defined with period 4 by construction (pattern match on n mod 4). This verifies the definition, not an independent property. |

### Claim 8: Dimensional Consistency (Q = Psi * Phi)

| Field | Value |
|-------|-------|
| Source | Lone Pine Writings |
| Statement | Q = Psi * Phi (Weber-Coulomb), W = dQ/dt (Joule) |
| Verdict | **DIMENSIONALLY CORRECT** but **NOT NOVEL** |
| Experiment | Experiment 3 |
| Polymathic finding | Weber * Coulomb = J*s (units of action). This is the coordinate-momentum product in Lagrangian circuit theory (Cherry 1951): charge q is the generalized coordinate, flux lambda is the conjugate momentum, q*lambda = action. W = dQ/dt = energy is dimensionally consistent with the Hamilton-Jacobi equation dS/dt = -H. However, this is 1830s analytical mechanics, not a new discovery. **PRIMARY SOURCE CONFIRMED** (2026-03-08): Lone Pine Writings lines 525-535 and 905-906 explicitly define Psi = "total dielectric induction" in Coulombs (charge) and Phi = "total magnetic induction" in Webers (flux). Lines 611-612: dPsi/dt = I (Amperes), dPhi/dt = E (Volts). This exactly matches standard Lagrangian circuit theory: Psi = q (generalized coordinate), Phi = λ (conjugate momentum). (95% confidence on physical identity, 99% on dimensional correctness) |
| Note | Dollard's definitions (Psi=Coulombs, Phi=Webers, dPsi/dt=I, dPhi/dt=E) exactly reproduce the Lagrangian circuit variables (q, λ, I=dq/dt, V=dλ/dt). His framework accidentally points toward quantum circuit theory (Josephson junctions, superconducting qubits), which begins with exactly this classical Lagrangian formulation. The "E=mc^2 replacement" claim (Claim 11) is a category error: W=dQ/dt is about circuits, E=mc^2 is about rest mass-energy equivalence. |

---

## Track C: Physics Claims

### Claim 9: Electricity as Fundamental Phenomenon

| Field | Value |
|-------|-------|
| Source | Lone Pine Writings |
| Statement | "Electricity is the fundamental phenomenon, not electromagnetic fields" |
| Verdict | **UNFALSIFIABLE** (by formal methods) |
| Note | This is a philosophical/physical claim about the nature of reality. Cannot be addressed by Lean 4. Would require experimental physics program. |

### Claim 10: Aether as 5th State of Matter

| Field | Value |
|-------|-------|
| Source | Core Theoretical Framework |
| Statement | "Aether exists as a fifth state of matter beyond plasma" |
| Verdict | **UNFALSIFIABLE** (by formal methods) |
| Note | No mathematical content to verify. Physics claim requiring experimental evidence. No evidence provided. |

### Claim 11: E=mc2 Replacement

| Field | Value |
|-------|-------|
| Source | Core Theoretical Framework |
| Statement | "W = dQ/dt replaces E = mc^2 as the fundamental energy equation" |
| Verdict | **EXTRAORDINARY** / **CATEGORY ERROR** |
| Polymathic finding | W = dQ/dt is a notational variant of the Hamilton-Jacobi equation dS/dt = -H, which is standard analytical mechanics (1830s). E = mc^2 describes rest mass-energy equivalence in special relativity. These operate in completely different domains. One cannot "replace" the other any more than Ohm's law can "replace" the ideal gas law. The steelmanned version of Dollard's claim is that EE should reconnect with Lagrangian/Hamiltonian mechanics -- which is correct (this is the basis of quantum circuit theory), but the gap is already filled by existing textbooks (Chua 1969, Vool & Devoret 2017). (80% confidence on steelman interpretation) |
| Note | The claim as stated requires extraordinary evidence. None provided. |

### Claim 12: Over-Unity Energy Production

| Field | Value |
|-------|-------|
| Source | Experimental Predictions |
| Statement | "Parameter variation in transmission lines can produce excess energy" |
| Verdict | **EXTRAORDINARY** |
| Note | Violates conservation of energy (first law of thermodynamics). Would require extraordinary experimental evidence. None provided. No mathematical formalization possible without a physical model. |

### Claim 13: Dielectric Fields in Counterspace

| Field | Value |
|-------|-------|
| Source | Core Theoretical Framework |
| Statement | "Dielectric fields exist in counterspace (inverse/reciprocal space)" |
| Verdict | **UNFALSIFIABLE** (by formal methods) |
| Note | "Counterspace" is not a standard mathematical concept. If interpreted as reciprocal space (Fourier dual), this could have mathematical content, but Dollard's usage does not map to standard Fourier theory. |

---

## Track B (Supplementary): Claims Validated by N-Phase but Not in Dollard's Core

### Claim 14: Quaternary Expansion (e^(j*theta) into 4 subseries)

| Field | Value |
|-------|-------|
| Source | Versor Algebra, Advanced Versor Algebra II-23 |
| Statement | e^(j*theta) = u + j*x + h*v + k*y, where u-v=cos, x-y=sin, u+v=cosh, x+y=sinh |
| Verdict | **VERIFIED** (mathematically correct) then **DEPRECATED** (practically useless) |
| Computational evidence | N-Phase `test_quaternary.py`: 175 tests, verified to 12 decimal places |
| Empirical evidence | N-Phase E006a: cosh/sinh features are redundant with magnitude; catastrophic condition number collapse on EEG data |
| Note | A perfect case study in honest verification: the math is correct, but the application provides no benefit. Mathematical truth does not imply practical utility. |

### Claim 15: Fortescue Decomposition Is Domain-Specific

| Field | Value |
|-------|-------|
| Source | N-Phase experimental results |
| Statement | Fortescue decomposition provides advantage where physical phase coupling exists |
| Verdict | **CONFIRMED** empirically |
| Evidence | E007 (EEG: p=0.033), E008c (3-phase power: d=3.1), E011 (finance: NOT MET) |
| Note | This constrains Track C claims. Fortescue works because it is standard DFT applied to polyphase signals -- not because of aether or counterspace. Where physical phase structure is absent (finance), it provides no advantage. |

### Claim 16: N=4 Fortescue Matrix Matches Dollard's Versor Matrix

| Field | Value |
|-------|-------|
| Source | N-Phase implementation cross-referenced with Dollard's Versor Algebra |
| Statement | The Fortescue A_4 matrix rows cycle through {1, j, h, k} |
| Verdict | **VERIFIED** computationally |
| Computational evidence | N-Phase `test_decomposer.py` -- A_4 construction matches Dollard's claimed matrix |
| Note | This confirms Dollard correctly identified that versor operators are the N=4 case of Fortescue's general DFT. The insight is valid; the credit belongs to Fortescue (1918). |

### Claim 17: jk=1 + j^2=-1 + hj=k Forces h=-1 (Algebraic Necessity)

| Field | Value |
|-------|-------|
| Source | Polymathic research Phase 5 (adversarial analysis) |
| Statement | The three axioms j^2=-1, hj=k, jk=1 alone force h=-1 without needing h^1=-1 or h^2=1 |
| Verdict | **VERIFIED** (formally, 0 sorry) |
| Formal evidence | `src/lean_proofs/foundations/algebraic_necessity.lean` — proves `h = -1` over ANY field from j^2=-1, hj=k, jk=1. |
| Clifford evidence | `src/lean_proofs/clifford/cl11.lean` — shows jk=1 FAILS in Cl(1,1), confirming that a non-trivial h requires dropping this axiom. |
| Note | This is STRONGER than previously known: h^1=-1 and h^2=1 are REDUNDANT axioms. Any algebra with j^2=-1, hj=k, jk=1 is forced to Z_4. To get a non-trivial h (e.g., Cl(1,1)), you must drop jk=1 AND commutativity. |
