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

### Level 2: The Corrected Extension (FORMALIZING NOW)

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

### Level 3: The Real Unification (RESEARCH PROGRAM)

**Core move: Extend Cl(1,1) to Cl(3,1) (spacetime algebra).**

Cl(3,1) has 16 basis elements and encodes ALL of special relativistic
electromagnetism. In this algebra:
- Maxwell's four equations collapse to ONE: nabla*F = J
- Electric and magnetic fields unify as bivector components of F
- Lorentz transformations are rotors (spinor group Spin(3,1))
- The Dirac equation has a natural geometric form

The algebraic hierarchy:
```
Z_4 (Dollard)     -- 4 elements, commutative, trivial
  |
  v
Cl(1,1)            -- 4 elements, non-commutative, isomorphic to M2(R)
  |                   [forward/backward wave decomposition]
  v
Cl(3,0)            -- 8 elements, Pauli algebra
  |                   [3D rotations, spin]
  v
Cl(3,1)            -- 16 elements, spacetime algebra
  |                   [Maxwell + Dirac + Lorentz in one equation]
  v
Cl(1,4) / Cl(2,4)  -- conformal geometric algebra
                      [gravity as gauge theory of Poincare group]
```

Each step DOUBLES the dimension and adds physical content.
The Lean 4 formalization pattern is the same at each level:
define the basis, verify the multiplication table, prove the theorems.

| Task | Status | Difficulty |
|------|--------|------------|
| Define Cl(3,0) with 8-component structure | NOT STARTED | Medium |
| Verify Pauli matrix isomorphism | NOT STARTED | Medium |
| Define Cl(3,1) with 16-component structure | NOT STARTED | Hard |
| Prove Maxwell's equation nabla*F = J | NOT STARTED | Hard |
| Show Lorentz transformation as rotor | NOT STARTED | Hard |

### Level 4: What Constitutes a UFT (HORIZON)

A genuine UFT requires unifying electromagnetism with gravity.
The geometric algebra path offers two approaches:

**Approach A: Gauge Theory of Poincare Group**
- Gravity as a gauge field for local Lorentz transformations
- Uses Cl(1,3) (or Cl(3,1) depending on convention)
- Connects to Einstein-Cartan theory (GR + torsion)
- Active research area (Lasenby, Doran, Gull 1998)

**Approach B: Conformal Geometric Algebra**
- Work in Cl(2,4) or Cl(4,2) (conformal algebra)
- Encodes both Lorentz and conformal symmetries
- Gravity appears as curvature in the conformal structure
- More speculative, fewer results

Neither approach is complete. This is the frontier of geometric algebra research.
The contribution of THIS project would be: bringing Lean 4 formal verification
to bear on the geometric algebra program, ensuring each step is mathematically
rigorous.

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

1. Compile all Lean proofs (install elan, lake update, lake build)
2. Close sorry gaps in polyphase_formula.lean (3 exp/trig facts)
3. Formalize Lagrangian circuit theory (Experiment 3 completion)
4. Begin Cl(3,0) formalization (8-component structure)
5. Draft Track A paper from outline
6. Close prior-art search gap (Mizar, ACL2, HOL Light, ITP/CPP)
