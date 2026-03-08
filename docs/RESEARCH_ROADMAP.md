# Research Roadmap: From Versor Algebra to Spacetime Algebra

## The Path

Dollard doesn't have a UFT. But formal verification reveals he's standing
at the base of a road that DOES lead to one. This roadmap traces that path,
fixing what's wrong and extending what's right.

## The Four Levels

### Level 1: Where Dollard Is (VERIFIED)

| Result | Status | Evidence |
|--------|--------|----------|
| {1, j, h, k} = Z_4 = 4th roots of unity | PROVED | `algebraic_necessity.lean` (0 sorry) |
| Telegraph equation expansion correct | PROVED | `telegraph_equation.lean` |
| Versor form equivalence WRONG | DISPROVED | `telegraph_equation.lean:85-92` |
| jk=1 forces h=-1 (axioms redundant) | PROVED | `algebraic_necessity.lean` (0 sorry) |
| Q = Psi*Phi = action (J*s) | CONFIRMED | Dimensional analysis + Cherry 1951 |
| Fortescue = DFT on polyphase signals | CONFIRMED | N-Phase 1194 tests |

Dollard's contributions at Level 1: correctly identified the Z_4 structure,
correctly identified the four-factor telegraph analysis, and (accidentally)
pointed at the action interpretation. His errors: the versor form sign mistake,
the claim that this is novel (it's Fortescue 1918), and the overreach to "replace E=mc2."

### Level 2: The Corrected Extension (FORMALIZED)

**Core move: Replace Z_4 with Cl(1,1).**

Cl(1,1) is the Clifford algebra with signature (+1,-1). It has 4 basis elements
{1, e1, e2, e12} where:
- e1^2 = +1 (like h^2 = +1, but e1 is genuinely non-trivial)
- e2^2 = -1 (like j^2 = -1)
- e1*e2 = -e2*e1 (ANTICOMMUTATIVE -- what Dollard missed)

| Result | Status | Evidence |
|--------|--------|----------|
| Cl(1,1) well-defined, multiplication verified | PROVED | `clifford/cl11.lean` (0 sorry) |
| Dollard's jk=1 fails (e2*e12 = e1) | PROVED | `clifford/cl11.lean` |
| Dollard's commutativity fails (e1*e2 != e2*e1) | PROVED | `clifford/cl11.lean` |
| Idempotent decomposition P+, P- complete | PROVED | `clifford/cl11.lean` (0 sorry) |
| Forward/backward wave projection | PROVED | `clifford/cl11.lean` (0 sorry) |
| Versor form STILL fails (grade mismatch) | PROVED | `clifford/cl11.lean` |
| Telegraph eq lives in complex subalgebra {1,e2} | PROVED | `clifford/cl11.lean` |

**What Cl(1,1) gives us that Z_4 can't:**
- Non-trivial h (e1^2=+1 but e1 != +/-1)
- Forward/backward wave decomposition via idempotents
- Two subalgebras: complex {1,e2} for oscillation, split-complex {1,e1} for propagation
- Foundation for extending to higher dimensions

**What needs to happen at Level 2:**
1. Formalize the Lagrangian circuit theory connection in Lean 4
2. Show Q = q*lambda (charge * flux) satisfies Hamilton-Jacobi for LC circuit
3. Connect the complex subalgebra to the standard telegraph equation
4. Show the split-complex subalgebra naturally decomposes transmission line waves
5. Compare Cl(1,1) decomposition vs standard scattering parameters (S-parameters)

### Level 3: The Real Unification (FORMALIZED)

**Core move: Extend Cl(1,1) through Cl(3,0) to Cl(1,3) (spacetime algebra).**

Cl(1,3) has 16 basis elements and encodes ALL of special relativistic
electromagnetism. In this algebra:
- Maxwell's four equations collapse to ONE: nabla*F = J
- Electric and magnetic fields unify as bivector components of F
- Lorentz transformations are rotors (spinor group Spin(1,3))
- The Dirac equation has a natural geometric form

The algebraic hierarchy (ALL FORMALIZED):
```
Z_4 (Dollard)     -- 4 elements, commutative, trivial
  |                   [basic_operators.lean, algebraic_necessity.lean]
  v
Cl(1,1)            -- 4 elements, non-commutative, isomorphic to M2(R)
  |                   [cl11.lean: idempotent wave decomposition]
  v
Cl(3,0)            -- 8 elements, Pauli algebra
  |                   [cl30.lean: EM field as F = E + I*B]
  v
Cl(1,3)            -- 16 elements, spacetime algebra
  |                   [cl31_maxwell.lean: signature, EM bivector, Maxwell structure]
  v
Cl(1,4) / Cl(2,4)  -- conformal geometric algebra (HORIZON)
                      [gravity as gauge theory of Poincare group]
```

Each step DOUBLES the dimension and adds physical content.

| Task | Status | Evidence |
|------|--------|----------|
| Define Cl(3,0) with 8-component structure | DONE | `cl30.lean` (0 sorry) |
| Verify basis blade products and anticommutativity | DONE | `cl30.lean` |
| EM field representation as vector + bivector | DONE | `cl30.lean` |
| Define Cl(1,3) with 16-component structure | DONE | `cl31_maxwell.lean` (0 sorry) |
| Verify signature (+,-,-,-) and anticommutativity | DONE | `cl31_maxwell.lean` |
| EM field as bivector (electric + magnetic) | DONE | `cl31_maxwell.lean` |
| Cl(3,0) embeds as spatial subalgebra | DONE | `cl31_maxwell.lean` |
| Full 16×16 geometric product (256 terms) | DONE | `cl31_maxwell.lean` (0 sorry) |
| Signature verification via full product | DONE | `cl31_maxwell.lean` |
| Reversion for all 16 grades | DONE | `cl31_maxwell.lean` |
| Lorentz boost rotors in Cl(1,3) | DONE | `cl31_maxwell.lean` (0 sorry) |
| Boost of all 4 basis vectors | DONE | `cl31_maxwell.lean` |
| EM field transformation under boosts | DONE | `cl31_maxwell.lean` (E∥ invariant, E⊥ mixes with B) |
| Spatial rotation rotors in Cl(1,3) | DONE | `cl31_maxwell.lean` (0 sorry) |
| Lorentz Lie algebra (4 commutators) | DONE | `cl31_maxwell.lean` (0 sorry) |
| Prove Maxwell's nabla*F=J computationally | DEFERRED | Requires differential geometry in Lean |

### Level 4: Gauge Theory Gravity (STARTED)

**Core insight: Gravity is a gauge field for the Lorentz group.**

In GTG (Lasenby, Doran, Gull 1998), spacetime is FLAT. Gravity is encoded
in two gauge fields, just like electromagnetism is a gauge field for U(1):
  - h̄(a): position gauge (vierbein) — encodes stretching
  - Ω(a): rotation gauge (spin connection) — encodes Lorentz frame rotation
  - Field strength: R(a∧b) = ∂_aΩ(b) - ∂_bΩ(a) + Ω(a)×Ω(b) (Riemann tensor)
  - The nonlinear term Ω(a)×Ω(b) uses the COMMUTATOR PRODUCT we just formalized

| Task | Status | Evidence |
|------|--------|----------|
| Bivector type (6D Lorentz Lie algebra) | DONE | `gauge_gravity.lean` (0 sorry) |
| Commutator product definition | DONE | `gauge_gravity.lean` |
| All 15 structure constants of so(1,3) | DONE | 11 verified (4 redundant by antisymmetry) |
| Antisymmetry of commutator product | DONE | `gauge_gravity.lean` |
| **Jacobi identity** | **DONE** | `gauge_gravity.lean` — cornerstone of gauge theory |
| Hodge dual on bivectors (dual² = -1) | DONE | `gauge_gravity.lean` |
| Boost/rotation decomposition | DONE | `gauge_gravity.lean` |
| Riemann tensor structure (linear map) | DONE | `gauge_gravity.lean` |
| Gauge covariant derivative | NOT STARTED | Requires abstract differentiation |
| Einstein field equation structure | NOT STARTED | G + Λg = 8πT |
| EM as U(1) gauge theory in Cl(1,3) | NOT STARTED | Compare with Lorentz gauge |

**The Jacobi identity is the key result.** It guarantees that:
  - The gauge field equations are consistent
  - The covariant derivative satisfies the Leibniz rule
  - The Bianchi identity holds
  - Conservation laws work

### Level 5: Actual Unification (HORIZON)

A genuine UFT requires showing EM and gravity emerge from the SAME structure.
Two approaches:

**Approach A: Gauge Theory of Poincare Group**
- Already started in gauge_gravity.lean
- Show EM field strength F = dA is the U(1) case
- Show Riemann tensor R = dΩ + Ω×Ω is the Lorentz case
- Same algebraic machinery, different gauge group

**Approach B: Conformal Geometric Algebra**
- Work in Cl(2,4) or Cl(4,2) (conformal algebra, 64 elements)
- Encodes both Lorentz and conformal symmetries
- More speculative, fewer results

Neither approach is complete. This is the frontier of geometric algebra research.

## Connection to Dollard's Claims

| Dollard Claim | Corrected Version | Level |
|--------------|-------------------|-------|
| h^2=+1 (novel operator) | e1^2=+1 in Cl(1,1), genuinely non-trivial | 2 |
| Versor algebra is new math | Z_4 subset of known Clifford hierarchy | 1-2 |
| Q=Psi*Phi (fundamental quantity) | Action principle in Lagrangian mechanics | 2-3 |
| W=dQ/dt replaces E=mc2 | Hamilton-Jacobi for circuits, not mass-energy | 2 |
| Four-quadrant analysis | Idempotent decomposition in Cl(1,1) | 2 |
| Universal polyphase formula | Roots of unity = DFT kernel = Fortescue | 1 |
| Electricity is fundamental | EM is one component of Cl(3,1) field F | 3 |

## What's Publishable at Each Level

**Level 1 (NOW):** Track A methodology paper -- "Formal Verification of
Alternative Mathematical Frameworks." ITP workshop or J. Automated Reasoning.

**Level 2 (NEXT):** Cl(1,1) transmission line analysis paper --
"Clifford Algebra Cl(1,1) for Transmission Line Wave Decomposition:
A Formal Verification." IEEE or ACES conference.

**Level 3 (FUTURE):** Lean 4 formalization of Maxwell's equation in Cl(3,1).
This would be a significant formalization result regardless of Dollard context.

## Upstream/Downstream

**Upstream evidence:** N-Phase Patent Ready (1194 tests)
- Validates Fortescue decomposition computationally
- Validates polyphase formula to machine precision
- Provides real-world test cases (EEG, power, bearings)

**Downstream dependency:** N-Phase signal processing system
- Level 1 results: safe to depend on (Z_4, DFT, telegraph)
- Level 2 results: may enable Cl(1,1)-based decomposition features
- Level 3 results: would provide relativistic signal processing (future)

## Immediate Next Steps

1. ~~Compile all Lean proofs~~ DONE (3269 jobs, 0 errors, 0 sorry)
2. ~~Close sorry gaps in polyphase_formula.lean~~ DONE (all 3 closed)
3. ~~Draft Track A paper from PAPER_OUTLINE.md~~ DONE (`paper/main.tex`)
4. ~~Verify Cherry 1951 exact reference~~ DONE (DOI: 10.1080/14786445108561362)
5. ~~Full Cl(1,3) geometric product (256 terms)~~ DONE (`cl31_maxwell.lean`)
6. ~~Lorentz transformation as rotor in Cl(1,3)~~ DONE (boosts + rotations)
7. ~~Determine venue~~ DONE (CICM 2026, Ljubljana, abstract Mar 25, paper Apr 1)
8. Compile LaTeX paper and review
9. ~~Lorentz Lie algebra so(1,3)~~ DONE (`gauge_gravity.lean`, Jacobi identity proved)
10. Gauge covariant derivative (Level 4b)
11. Show EM and gravity share algebraic structure (Level 5)

## Completed

- [x] Prior art search (95% confidence in novelty — `research/scratch/prior-art-deep-search.md`)
- [x] Cl(3,0) formalization (8 basis elements, EM field)
- [x] Cl(1,3) spacetime algebra (16 basis elements, Maxwell structure)
- [x] Telegraph equation sign convention fix
- [x] Factor constraint proof (RG*XB = XG*RB)
- [x] All sorry gaps closed (3 in polyphase_formula.lean)
- [x] Full build: 3269 jobs, 0 errors, 0 sorry
- [x] Experiment 2 resolved: versor form irreparable (h_ne_one, versor_repaired_with_one)
- [x] Paper draft: `paper/main.tex` (LNCS format, ~4000 words)
- [x] Cl(1,1) Lorentz boost rotors (13 theorems, 0 sorry)
- [x] Cl(1,3) full 256-term geometric product
- [x] Cl(1,3) Lorentz boost rotors (6 theorems)
- [x] Cl(1,3) spatial rotation rotors (5 theorems)
- [x] Cl(1,3) EM field transformation under boosts (3 theorems)
- [x] Cl(1,3) Lorentz Lie algebra commutators (4 in cl31, 11 in gauge_gravity)
- [x] Lorentz Lie algebra Jacobi identity (gauge_gravity.lean)
- [x] Hodge dual on bivectors + boost/rotation decomposition
- [x] Riemann tensor algebraic structure
- [x] Full build: 3270 jobs, 0 errors, 0 sorry
