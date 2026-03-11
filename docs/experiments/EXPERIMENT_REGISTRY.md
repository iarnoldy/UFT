# Experiment Registry

All experiments must be pre-registered here before execution.
Each entry requires a hypothesis, falsification criteria, and track assignment.

---

## Experiment 0: Polyphase Formula Verification [BLOCKING]

**Status**: FULLY VERIFIED (0 sorry gaps, all proofs compile)
**Track**: B
**Priority**: COMPLETE -- was BLOCKING, now resolved

**Hypothesis**: The universal polyphase formula k^n_N = exp(j*2*pi*n/N) is provable
in Lean 4 as a consequence of the nth roots of unity.

**Method**: Write Lean 4 proof in `src/lean_proofs/polyphase/` that:
1. Defines nth_root_unity(n, N) = exp(2*pi*i*n/N)
2. Proves (nth_root_unity(1, N))^n = nth_root_unity(n, N)
3. Proves nth_root_unity(N, N) = 1
4. Proves the 3-phase specialization: a^3 = 1 where a = exp(2*pi*i/3)

**Falsification**: If Lean rejects the proof, the polyphase claim needs
reinterpretation. Specifically, if the formula requires non-standard definitions
or axioms beyond mathlib, document what's needed.

**Expected outcome**: VERIFIED (this is standard roots-of-unity math, expected to
be trivial like the basic operator proofs).

**Proof file**: `src/lean_proofs/polyphase/polyphase_formula.lean`
**Status details (2026-03-08)**:
- 16 theorems fully proved (0 sorry): omega powers, root multiplication,
  periodicity, exponent simplification, 3-phase geometric sum, 4-phase versors,
  unit circle, omega_pow_N, omega4_eq_I, omega_on_unit_circle
- All 3 former sorry gaps CLOSED using mathlib lemmas:
  1. `omega_pow_N`: closed via Complex.exp_two_pi_mul_I
  2. `omega4_eq_I`: closed via Complex.ext + simp (cos(π/2)=0, sin(π/2)=1)
  3. `omega_on_unit_circle`: closed via Complex.norm_exp_ofReal_mul_I
- Build passes: `lake build` (3269 jobs, 0 errors)

**Dependencies**: None
**Downstream impact**: N-Phase system's Fortescue decomposition depends on this

---

## Experiment 1: h Operator Alternative Interpretations

**Status**: SUBSTANTIALLY COMPLETE (Lean proofs written)
**Track**: A + B

**Hypothesis**: There exists a non-trivial algebraic structure (beyond complex
numbers) where h satisfies h^2 = 1 and h^1 = -1 simultaneously, AND h != -1.

**Polymathic Finding (2026-03-07)**: The axioms j^2=-1, hj=k, jk=1 ALONE force
h=-1 by pure algebra. Proof: jk=1 => k=j^{-1}=-j; hj=k=-j => h=-1. This means
even dropping h^1=-1 and h^2=1, the remaining axioms force h=-1 in ANY unital
associative algebra. To get non-trivial h (e.g. Cl(1,1) where h^2=1, h != +/-1),
you must drop jk=1 (and commutativity) -- yielding a DIFFERENT algebra, not
Dollard's. Confidence: 97%.

**Proof file**: `src/lean_proofs/foundations/algebraic_necessity.lean`
**Status details (2026-03-07)**:
- General theorem proved over ANY field (not just C): 0 sorry
- Concrete instantiation for C verified: 0 sorry
- Redundancy of h^1=-1 and h^2=1 proved as corollaries
- Cl(1,1) incompatibility documented (anticommutativity blocks embedding)

**Cl(1,1) proof file**: `src/lean_proofs/clifford/cl11.lean`
**Cl(1,1) status (2026-03-07)**: 0 sorry. Full multiplication table verified.
  Dollard axiom failures proved. Idempotent decomposition proved complete.
  Telegraph equation in complex subalgebra proved. Versor form grade mismatch proved.

**Remaining work**:
1. ~~Formalize the jk=1-forces-h=-1 proof in Lean 4~~ DONE (0 sorry)
2. ~~Formalize Cl(1,1) in Lean 4 showing it requires different axioms~~ DONE (0 sorry)
3. ~~Document the algebraic hierarchy: Z_4 < Cl(1,0) < Cl(1,1) < Cl(3,0)~~ DONE (RESEARCH_ROADMAP.md)
4. ~~Extend to Cl(3,0) formalization~~ DONE (cl30.lean, 0 sorry)
5. ~~Extend to Cl(1,3) spacetime algebra~~ DONE (cl31_maxwell.lean, 0 sorry)
6. Compile all proofs (requires elan/Lean 4 installation)

**Falsification**: CONFIRMED -- h=-1 is forced. No non-trivial structure satisfies
ALL of Dollard's axioms simultaneously. The full Clifford hierarchy is now formalized:
Z_4 -> Cl(1,1) -> Cl(3,0) -> Cl(1,3).

**Outcome**: RESOLVED. The path from Dollard to UFT goes through Clifford algebras.
Dollard's axioms collapse to Z_4; the correct algebra is Cl(1,3) (spacetime algebra).

**Dependencies**: None
**Downstream impact**: Versor algebra has NO novel algebraic content. It is Z_4.

---

## Experiment 2: Versor Form Repair

**Status**: RESOLVED — FALSIFIED (no repair preserves Dollard's algebra)
**Track**: B
**Resolved**: 2026-03-08

**Hypothesis**: There exists a consistent modification of Dollard's versor form
ZY = h(XB+RG) + j(XG-RB) that preserves equivalence with the standard telegraph
equation ZY = (RG+XB) + j(XG-RB).

**Method**:
1. Enumerate possible repairs: replace h with 1, redefine h, change sign convention
2. For each candidate repair, attempt Lean 4 proof of equivalence
3. Check whether any repair preserves Dollard's other claimed properties

**Falsification**: If no repair preserves both equivalence and the h operator
properties (h^2=1, h^1=-1), the versor form is simply wrong and cannot be saved.

**Result**: FALSIFIED. Three candidate repairs enumerated; none preserves Dollard's system.

| Repair | Works mathematically? | Preserves Dollard's algebra? | Lean proof |
|--------|----------------------|------------------------------|-----------|
| Replace h with 1 | YES (`versor_repaired_with_one`, 0 sorry) | NO — h=1 contradicts h=-1 (`h_ne_one`, 0 sorry) | `telegraph_equation.lean` |
| Negate argument: h(-XB-RG) | YES ((-1)(-a) = a) | NO — changes Dollard's claimed formula | Trivial |
| Drop jk=1 to escape h=-1 | Possible in Cl(1,1) | NO — yields a DIFFERENT algebra entirely | `cl11.lean` |

**Conclusion**: The versor form has a sign error. The coefficient on the real part
must be +1 for equivalence, but Dollard's axioms force it to -1. The only "repairs"
either abandon the versor algebra (repair 1), change the claimed formula (repair 2),
or switch to an entirely different algebraic framework (repair 3). The versor form
is irreparable within its own system.

**Proof files**: `telegraph_equation.lean` (`h_ne_one`, `versor_repaired_with_one`)
**Dependencies**: None
**Downstream impact**: N-Phase system correctly avoids versor form (uses standard DFT)

---

## Experiment 3: Dimensional Analysis Verification

**Status**: RESOLVED — VERIFIED (dimensionally correct, not novel)
**Track**: B + C
**Resolved**: 2026-03-08

**Hypothesis**: Q = Psi * Phi with W = dQ/dt is dimensionally consistent,
where Psi has units of Coulomb and Phi has units of Weber.

**Polymathic Finding (2026-03-07)**: Weber * Coulomb = J*s (units of action).
This is the coordinate-momentum product in Lagrangian circuit theory (Cherry 1951).
W = dQ/dt has energy units, consistent with Hamilton-Jacobi dS/dt = -H.
Dimensionally correct but not novel -- this is 1830s analytical mechanics.
The "E=mc^2 replacement" claim is a category error: circuit energy vs. rest mass.

**Primary Source Confirmation (2026-03-08)**: Lone Pine Writings explicitly define:
- Psi = "total dielectric induction" in Coulombs (lines 525-529)
- Phi = "total magnetic induction" in Webers (lines 531-535)
- dPsi/dt = I (Amperes, line 611), dPhi/dt = E (Volts, line 612)
This exactly matches standard Lagrangian circuit theory: Psi = q (generalized
coordinate = charge), Phi = λ (conjugate momentum = flux linkage).
Confidence: 99% (dimensional), 95% (physical identity with Lagrangian theory).

**Remaining work**:
1. ~~Define dimensional type system in Lean 4~~ DONE (`circuit_action.lean`)
2. ~~Verify: Weber * Coulomb = Joule * second (formally)~~ DONE (0 sorry)
3. For an LC circuit, derive the Hamilton-Jacobi equation and check whether
   Q = q*lambda(q,t) satisfies it (closes the Gap 2 from polymathic research)
4. ~~Read Dollard primary sources to confirm Psi = charge, Phi = flux~~ DONE (Lone Pine lines 525-535, 905-906)

**Falsification**: Dimensional inconsistency would invalidate the energy framework.
**Result**: NOT FALSIFIED. Dimensionally verified both formally and from primary sources.
The only remaining gap is the Hamilton-Jacobi connection (item 3), which is a deeper
physics question beyond dimensional analysis.

**Expected outcome**: VERIFIED dimensionally; physical identity probable but conditional.

**Dependencies**: None
**Downstream impact**: Affects Track C physics claims about energy

---

## Experiment 4: SO(14) Candidate Theory Construction

**Status**: IN PROGRESS (Phase 0)
**Track**: D (Candidate Theory Construction)
**Priority**: ACTIVE
**Started**: 2026-03-08

**Hypothesis**: SO(14) is a viable candidate for a unified gauge group that:
1. Contains SO(10) (Grand Unified) × SO(4) (gravity sector) as subgroups
2. Achieves coupling constant unification at a single energy scale
3. Predicts proton lifetime above the Super-Kamiokande bound (τ_p > 1.6 × 10^34 years)
4. Admits a symmetry breaking chain to the Standard Model

**Method**: Gate-controlled, kill-condition-first construction:
- Phase 0: Literature survey + matter content decomposition
- Phase 1: RG coupling unification test (cheapest falsification)
- Phase 2: Lagrangian + proton decay + selection principle
- Phase 3: Synthesis and documentation

**Falsification criteria (Kill Conditions)**:

| ID | Condition | Phase | Cost | Severity |
|----|-----------|-------|------|----------|
| KC-0 | SO(14) already ruled out in literature | 0 | LOW | FATAL |
| KC-1 | Couplings don't unify under SO(14) matter content (>5% miss) | 1 | MEDIUM | FATAL |
| KC-2 | Proton lifetime < Super-K bound (1.6 × 10^34 years) | 2 | MEDIUM | FATAL |
| KC-3 | Signature question (SO(14,0) vs SO(11,3)) has no resolution | 0-2 | LOW-MED | SERIOUS |
| KC-4 | Three-generation problem has no plausible resolution | 2 | LOW | SERIOUS |
| KC-5 | No Higgs achieves required breaking pattern | 2 | MEDIUM | FATAL |
| KC-6 | Gravity sector requires separate action (not Yang-Mills) | 2 | LOW | SERIOUS |

**Rule**: If a FATAL kill condition fires, the experiment is OVER. Document as negative result and stop.
**Rule**: SERIOUS conditions require explicit acknowledgment and proposed resolution path.

**Inputs (from scaffold)**:
- SO(14) dimension: 91 = C(14,2) [MV: so14_dimension in so14_unification.lean]
- Decomposition: 91 = 45 + 6 + 40 [MV: unification_decomposition in so14_unification.lean]
- SM beta-coefficients: b_1=41/10, b_2=-19/6, b_3=-7 [MV: rg_running.lean]
- Low-energy couplings: α_1^-1(M_Z)=59.0, α_2^-1(M_Z)=29.6, α_3^-1(M_Z)=8.5 [SP]

**Claim tagging**:
- [MV] Machine-verified (Lean 4 proof compiles)
- [CO] Computed (Python/SymPy, reproducible)
- [CP] Candidate physics (proposed, not verified)
- [SP] Standard physics (textbook result)
- [OP] Open problem (acknowledged gap)

**Gate decisions**: Made by Ian at each phase boundary.

**Phase 0 deliverables**:
- `research/so14-gut-literature.md` — literature survey (polymathic-researcher)
- `src/experiments/so14_matter_decomposition.py` — spinor branching rules (clifford-engineer)

**Phase 1 deliverables** (if Phase 0 passes):
- `src/experiments/so14_rg_unification.py` — RG evolution computation
- `src/lean_proofs/dynamics/rg_running_so14.lean` — beta-coefficient verification (if unification found)

**Phase 2 deliverables** (if Phase 1 passes):
- `docs/so14_lagrangian.md` — explicit Lagrangian
- `src/experiments/so14_proton_decay.py` — proton lifetime computation
- `docs/so14_selection_principle.md` — why SO(14)?

**Phase 3 deliverables** (if Phase 2 passes):
- `paper/so14_candidate_theory.tex` — candidate theory paper

**Dependencies**: Experiments 0-3 (all complete), Lean scaffold (35 files, 878 theorems)
**Downstream impact**: Defines Track D research program

---

## Experiment 5: KC-E3 Chirality in E₈(-24)

**Status**: COMPLETE — BOUNDARY
**Track**: D (Candidate Theory Construction)
**Priority**: RESOLVED
**Started**: 2026-03-10
**Resolved**: 2026-03-10

**Hypothesis**: Fermion chirality survives in E₈(-24) when three generations are
embedded via SU(9)/Z₃, i.e., the Distler-Garibaldi no-go theorem does not apply
to Wilson's massive-chirality construction.

**Method**:
1. Compute Clifford periodicity for all relevant signatures: Cl(14,0), Cl(11,3), Cl(12,4)
2. Verify dimension equalities for real forms: dim SU(9) = dim SU(7,2) = 80
3. Verify Spin(3,11) → Spin(4,12) embedding: 91 + 1 + 28 = 120
4. Machine-verify all algebraic prerequisites in Lean 4
5. Document the precise D-G vs Wilson boundary

**Falsification criteria**:
- If a dimensional inconsistency is found in the signature analysis, KC-E3 FAILS
- If the generation count changes under signature change, KC-E3 FAILS
- If D-G can be shown to apply specifically to E₈(-24), KC-E3 FAILS

**Result**: BOUNDARY. All algebraic prerequisites verified. The ONLY remaining question
is the definition of chirality (massless vs massive), which is an open problem in
mathematical physics that cannot be resolved by formal verification.

**Claim tagging**:
- [MV] Clifford periodicity, dimension equalities, embedding arithmetic (Lean 4)
- [CO] Spinor reality types from Clifford periodicity (Python)
- [SP] Distler-Garibaldi theorem statement (published result)
- [OP] Chirality definition question (open problem)

**Deliverables**:
- `src/experiments/e8_signature_chirality.py` — Python computation [CO]
- `src/lean_proofs/clifford/e8_chirality_boundary.lean` — Lean proofs [MV]
- `research/kc-e3-chirality-resolution.md` — research note

**Dependencies**: Experiments 0-4, e8_embedding.lean, e8_su9_decomposition.lean,
  e8_generation_mechanism.lean, three_generation_theorem.lean
**Downstream impact**: Closes the last open kill condition (KC-E3)

---

## Experiment 6: Chirality Kill Conditions KC-C4 and KC-C5

**Status**: IN PROGRESS
**Track**: D (Candidate Theory Construction)
**Priority**: ACTIVE
**Started**: 2026-03-10

**Context**: Experiment 5 resolved KC-E3 as BOUNDARY. The Heptapod B teleological
analysis proposed a concrete chirality operator J = (2/sqrt(3))(sigma + 1/2 Id) on
the 168-dim matter space, where sigma is the Z3 automorphism of E8. This experiment
tests whether J has the required physical properties.

**Hypotheses**:
- **KC-C4**: SU(2)_W x U(1)_Y distinguishes the 84 from the 84-bar. The complex
  structure J provides a physically meaningful label (gauge bosons see the distinction).
- **KC-C5**: J reduces to i*gamma_5 under the E8 -> SM breaking chain. The +i eigenspace
  (84) corresponds to left-handed SM fermions, and the -i eigenspace (84-bar) to right-handed.

**Method**:
1. Decompose Lambda^3(C^9) under SU(5) x SU(4) (dimensional verification)
2. Branch SU(4) -> SU(3)_family x U(1) to extract generation content
3. Decompose SU(5) reps under SU(3)_C x SU(2)_W x U(1)_Y
4. Catalog all SM quantum numbers in the 84 and 84-bar
5. Test KC-C4: are the SM catalogs different? (yes = PASS)
6. Test KC-C5: does J eigenvalue correlate with SM chirality? (yes = PASS)

**Falsification criteria**:
- KC-C4 FAILS if 84 and 84-bar have identical SM quantum numbers (this would mean
  J provides no physical distinction)
- KC-C5 FAILS if a single SM generation requires components from BOTH J eigenspaces
  (this would mean J != i*gamma_5)

**Claim tagging**:
- [MV] Branching rules verified in e8_generation_mechanism.lean (dimensions)
- [CO] SM quantum number catalogs (Python computation)
- [CP] Physical interpretation of J operator

**Deliverables**:
- `src/experiments/chirality_kc_c4_c5.py` — Python computation [CO]

**Dependencies**: Experiment 5, e8_generation_mechanism.lean
**Downstream impact**: Determines whether J is chirality (gamma_5) or something new
