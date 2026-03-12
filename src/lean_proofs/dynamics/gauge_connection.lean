/-
UFT Formal Verification - Gauge Connection (Phase 1.2)
======================================================

GAUGE CONNECTIONS AS LIE-ALGEBRA-VALUED 1-FORMS

This file generalizes `covariant_derivative.lean` (which hardcodes SU(2)) to an
arbitrary gauge group with Lie algebra of dimension n.

A gauge connection is a Lie-algebra-valued 1-form on spacetime. For a gauge group
with Lie algebra g of dimension n, the connection consists of n real-valued 1-forms
A^a (one per generator), and the dynamics are governed by:

  F^a = dA^a + f^a_{bc} A^b ∧ A^c       (field strength)
  D   = d + [A, -]                        (covariant exterior derivative)

The abelian part F = dA is fully formalized using mathlib's `extDeriv`, giving us
the abelian Bianchi identity d(dA) = 0 as a THEOREM (not an axiom).

The non-abelian self-interaction term f^a_{bc} A^b ∧ A^c uses the wedge product
of 1-forms from `wedge_product.lean`. The wedge product itself is axiomatized
(see that file for the rationale), but the field strength construction here is
DERIVED: given any `WedgeProductOps` satisfying the axioms, we construct the
non-abelian term as a definition and prove its properties as theorems.

The legacy `NonAbelianTerm` structure is retained for backward compatibility with
`bianchi_from_principles.lean`. A bridge theorem shows that the wedge-product
construction provides a valid `NonAbelianTerm`.

Builds on:
  - differential_forms.lean: Spacetime, DiffForm, d, d_squared_zero
  - wedge_product.lean: WedgeProductOps (axiomatized wedge product)
  - covariant_derivative.lean: SU(2)-specific version (hardcoded)
  - gauge_gravity.lean: so(1,3) Jacobi identity (algebra side)
  - su3_color.lean, su5_grand.lean, so10_grand.lean: Lie algebra structure constants

References:
  - Yang & Mills, Physical Review 96 (1954)
  - Nakahara, "Geometry, Topology, and Physics" Ch. 10-11
  - Frankel, "The Geometry of Physics" Ch. 7
-/

import dynamics.wedge_product
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-! ## Part 1: The Gauge Theory Specification

We parametrize gauge theories by their Lie algebra dimension and structure constants.
The gauge potential is an n-tuple of real-valued 1-forms (one per generator).

This generalizes the SU(2)-specific `GaugePotential` in `covariant_derivative.lean`
(which hardcodes dim = 3 and ε_{abc} structure constants) to arbitrary gauge groups.

Examples:
- U(1): dim = 1, f^a_{bc} = 0 (electromagnetism)
- SU(2): dim = 3, f^a_{bc} = ε_{abc} (weak force)
- SU(3): dim = 8, f^a_{bc} from Gell-Mann matrices (strong force)
- SU(5): dim = 24 (Georgi-Glashow GUT)
- SO(10): dim = 45 (Fritzsch-Minkowski GUT)
- SO(14): dim = 91 (candidate unification) -/

/-- A gauge field theory specification.

    We axiomatize the Lie algebra structure via dimension and structure constants,
    and the gauge field as a collection of smooth 1-forms (one per generator).

    The structure constants f^a_{bc} satisfy:
    - Antisymmetry: f^a_{bc} = -f^a_{cb}
    - (Jacobi identity is a further constraint, not imposed here to keep the
      structure lightweight; verified separately for each specific algebra) -/
structure GaugeTheory where
  /-- Lie algebra dimension (number of generators) -/
  dim : ℕ
  /-- The gauge potential: one smooth 1-form per generator.
      A^a_μ(x) for a = 1..dim, at each spacetime point x. -/
  A : Fin dim → DiffForm 1
  /-- Structure constants f^a_{bc} of the Lie algebra.
      [T_b, T_c] = f^a_{bc} T_a (summed over a). -/
  structureConstants : Fin dim → Fin dim → Fin dim → ℝ
  /-- Antisymmetry of structure constants in the lower two indices. -/
  antisymm : ∀ a b c, structureConstants a b c = -structureConstants a c b
  /-- Smoothness: each gauge potential component is C^∞. -/
  smooth : ∀ a, ContDiff ℝ ⊤ (A a)

namespace GaugeTheory

/-! ## Part 2: Abelian Field Strength

For the abelian part of the field strength, F^a = dA^a. This applies directly
to U(1) (electromagnetism) where it gives the full field strength, and provides
the linear (kinetic) part of the field strength for any gauge theory.

The exterior derivative d maps 1-forms to 2-forms:
  (dA)_μν = ∂_μ A_ν - ∂_ν A_μ

For U(1) with a single component A = A_μ dx^μ:
  F_μν = ∂_μ A_ν - ∂_ν A_μ

This is the electromagnetic field tensor containing E and B fields. -/

/-- The abelian field strength: F^a = dA^a.

    This is the full field strength for abelian theories (like U(1) electromagnetism)
    and the linear part for non-abelian theories.

    dA maps a 1-form to a 2-form:
      (dA)_μν(x) = ∂_μ A_ν(x) - ∂_ν A_μ(x) -/
noncomputable def abelianFieldStrength (G : GaugeTheory) (a : Fin G.dim) :
    DiffForm 2 :=
  d (G.A a)

/-! ## Part 3: Abelian Bianchi Identity

The Bianchi identity d(dA) = 0 is the foundation of gauge theory consistency.

For electromagnetism, it encodes two of Maxwell's equations:
  ∇ · B = 0   (no magnetic monopoles)
  ∇ × E + ∂B/∂t = 0   (Faraday's law)

For non-abelian theories, the full Bianchi identity is D_[μ F_νρ] = 0 where
D is the covariant derivative. The abelian part d(dA) = 0 still holds for
each component separately.

This is a THEOREM, proved from the symmetry of second partial derivatives
via mathlib's `extDeriv_extDeriv`. Compare with `covariant_derivative.lean`
which proves it only for specific SU(2) triplets using the Jacobi identity. -/

/-- The abelian Bianchi identity: d(dA^a) = 0 for each gauge component.

    This is a genuine THEOREM (not an axiom), following from d^2 = 0
    which itself follows from the symmetry of second partial derivatives.

    For U(1): this gives ∂_{[μ} F_{νρ]} = 0 (homogeneous Maxwell equations).
    For SU(N): this gives the abelian part of D_{[μ} F^a_{νρ]} = 0. -/
theorem abelian_bianchi (G : GaugeTheory) (a : Fin G.dim) :
    d (abelianFieldStrength G a) = 0 :=
  d_squared_zero (G.A a) (G.smooth a)

/-- Pointwise abelian Bianchi: at each spacetime point. -/
theorem abelian_bianchi_at (G : GaugeTheory) (a : Fin G.dim) (x : Spacetime) :
    d (abelianFieldStrength G a) x = 0 :=
  d_squared_zero_at (G.A a) (G.smooth a) x

/-! ## Part 4: Non-Abelian Self-Interaction Term (Legacy Interface)

For non-abelian gauge theories, the field strength has an additional term:
  F^a = dA^a + f^a_{bc} A^b ∧ A^c

The second term (A∧A) involves:
1. The wedge product of two 1-forms (giving a 2-form)
2. Contraction with the structure constants f^a_{bc}

The wedge product of 1-forms α and β is:
  (α ∧ β)_μν = α_μ β_ν - α_ν β_μ

Composing with structure constants:
  (A∧A)^a_μν = f^a_{bc} (A^b_μ A^c_ν - A^b_ν A^c_μ)

This term is what makes non-abelian gauge theories NONLINEAR: the gauge field
interacts with itself. For U(1), f^a_{bc} = 0 and this term vanishes.

LEGACY: This `NonAbelianTerm` structure is the original axiomatization.
The PREFERRED approach is in Part 5b below, which uses `WedgeProductOps`
from `wedge_product.lean` to give a DERIVED definition. The bridge theorem
`NonAbelianTerm.fromWedge` shows that the new construction satisfies this
legacy interface, so downstream code continues to work unchanged. -/

/-- The non-abelian self-interaction term (legacy axiomatized interface).

    In components: (A∧A)^a_μν = f^a_{bc} A^b_μ A^c_ν - f^a_{bc} A^b_ν A^c_μ

    This is retained for backward compatibility with `bianchi_from_principles.lean`.
    The preferred construction is `selfInteractionW` in Part 5b, which uses the
    axiomatized wedge product to give an explicit formula. -/
structure NonAbelianTerm (G : GaugeTheory) where
  /-- The self-interaction 2-form for each generator -/
  selfInteraction : Fin G.dim → DiffForm 2
  /-- For abelian theories, the self-interaction vanishes.
      This is the defining property of the abelian/non-abelian distinction. -/
  abelian_vanishes : (∀ a b c, G.structureConstants a b c = 0) →
    ∀ a, selfInteraction a = 0

/-! ## Part 5: Full Non-Abelian Field Strength

The complete field strength F = dA + A∧A combines:
- The abelian (kinetic) part dA, which is a THEOREM-backed 2-form
- The non-abelian (self-interaction) part A∧A, which is AXIOMATIZED

For the abelian sector, we get genuine theorems (Bianchi identity).
For the full non-abelian sector, we get structural results conditional
on the axiomatized properties of the self-interaction term.

This is the same pattern used in covariant_derivative.lean for SU(2),
but now generalized to arbitrary dimension. -/

/-- The full non-abelian field strength: F^a = dA^a + (A∧A)^a.

    Combines the exterior derivative (kinetic/abelian part) with the
    self-interaction (non-abelian part).

    For U(1): (A∧A)^a = 0, so F = dA (Maxwell).
    For SU(2): (A∧A)^a = ε^a_{bc} A^b ∧ A^c (Yang-Mills).
    For SU(3): (A∧A)^a = f^a_{bc} A^b ∧ A^c (QCD). -/
noncomputable def fieldStrength (G : GaugeTheory) (T : NonAbelianTerm G)
    (a : Fin G.dim) : DiffForm 2 :=
  fun x => abelianFieldStrength G a x + T.selfInteraction a x

/-- For abelian theories, the full field strength equals the abelian field strength. -/
theorem fieldStrength_abelian (G : GaugeTheory) (T : NonAbelianTerm G)
    (habel : ∀ a b c, G.structureConstants a b c = 0) (a : Fin G.dim) :
    fieldStrength G T a = abelianFieldStrength G a := by
  have h := T.abelian_vanishes habel a
  funext x
  simp [fieldStrength]
  rw [h]
  simp

end GaugeTheory

/-! ## Part 5b: Non-Abelian Field Strength via Wedge Product

Given a `WedgeProductOps` (axiomatized wedge product from `wedge_product.lean`),
we can now DEFINE the non-abelian self-interaction term as:

  (A∧A)^a(x) = Σ_{b,c} f^a_{bc} (A^b ∧ A^c)(x)

This is a DERIVED definition: the non-abelian term is constructed from the
wedge product, not postulated as an opaque axiom. The key improvement over
the legacy `NonAbelianTerm` is that the formula is explicit and we can prove
properties from the wedge product axioms.

The bridge theorem `NonAbelianTerm.fromWedge` shows that this construction
satisfies the `NonAbelianTerm` interface, so existing downstream code
(e.g., `bianchi_from_principles.lean`) continues to work. -/

namespace GaugeTheory

variable (W : WedgeProductOps)

/-- The non-abelian self-interaction 2-form for generator a, constructed
    from the wedge product:

    (A∧A)^a(x) = Σ_{b,c} f^a_{bc} * (A^b ∧ A^c)(x)

    This is the term that makes non-abelian gauge theories nonlinear.
    For abelian theories (all f = 0), this vanishes identically (proved). -/
noncomputable def selfInteractionW (G : GaugeTheory) (a : Fin G.dim) : DiffForm 2 :=
  fun x => ∑ b : Fin G.dim, ∑ c : Fin G.dim,
    G.structureConstants a b c • W.wedge (G.A b) (G.A c) x

/-- For abelian theories, the wedge-product self-interaction vanishes.

    When all structure constants are zero, each summand
    f^a_{bc} * (A^b ∧ A^c) = 0 * (...) = 0, so the entire sum is zero.

    This is a THEOREM, proved from the wedge product axioms. -/
theorem selfInteractionW_abelian (G : GaugeTheory)
    (habel : ∀ a b c, G.structureConstants a b c = 0) (a : Fin G.dim) (x : Spacetime) :
    selfInteractionW W G a x = 0 := by
  simp [selfInteractionW, habel]

/-- The full non-abelian field strength via wedge product:
    F^a = dA^a + Σ_{b,c} f^a_{bc} A^b ∧ A^c

    This uses the explicit wedge product formula instead of an opaque axiom. -/
noncomputable def fieldStrengthW (G : GaugeTheory) (a : Fin G.dim) : DiffForm 2 :=
  fun x => abelianFieldStrength G a x + selfInteractionW W G a x

/-- For abelian theories, the wedge-product field strength equals dA. -/
theorem fieldStrengthW_abelian (G : GaugeTheory)
    (habel : ∀ a b c, G.structureConstants a b c = 0) (a : Fin G.dim) :
    fieldStrengthW W G a = abelianFieldStrength G a := by
  funext x
  simp [fieldStrengthW, selfInteractionW_abelian W G habel a x]

/-- The self-interaction term has compatible antisymmetry with structure constants.

    Because f^a_{bc} = -f^a_{cb} and (A^b ∧ A^c) = -(A^c ∧ A^b),
    the double antisymmetry means each pair (b,c) contributes consistently:
    f^a_{bc} (A^b ∧ A^c) = f^a_{cb} (A^c ∧ A^b). -/
theorem selfInteractionW_wedge_antisymm (G : GaugeTheory)
    (a : Fin G.dim) (x : Spacetime) (b c : Fin G.dim) :
    G.structureConstants a b c • W.wedge (G.A b) (G.A c) x =
    G.structureConstants a c b • W.wedge (G.A c) (G.A b) x := by
  rw [G.antisymm a b c]
  have hx : W.wedge (G.A b) (G.A c) x = -(W.wedge (G.A c) (G.A b) x) := by
    exact congrFun (W.wedge_antisymm (G.A b) (G.A c)) x
  rw [hx]
  simp [smul_neg, neg_smul]

/-- Bridge theorem: the wedge-product construction provides a valid `NonAbelianTerm`.

    This shows backward compatibility: any downstream code that uses the legacy
    `NonAbelianTerm` interface can be supplied with `NonAbelianTerm.fromWedge`. -/
noncomputable def NonAbelianTerm.fromWedge (G : GaugeTheory) : NonAbelianTerm G where
  selfInteraction := selfInteractionW W G
  abelian_vanishes := by
    intro habel a
    funext x
    exact selfInteractionW_abelian W G habel a x

/-- The legacy `fieldStrength` agrees with `fieldStrengthW` when using the
    wedge-product construction. -/
theorem fieldStrength_eq_fieldStrengthW (G : GaugeTheory) (a : Fin G.dim) :
    fieldStrength G (NonAbelianTerm.fromWedge W G) a = fieldStrengthW W G a := by
  funext x
  simp [fieldStrength, fieldStrengthW, NonAbelianTerm.fromWedge, selfInteractionW]

/-- The diagonal terms A^b ∧ A^b vanish in the self-interaction sum.

    Since f^a_{bb} = 0 (from antisymmetry) and A^b ∧ A^b = 0 (from wedge
    self-annihilation), the b=c terms contribute nothing. This means only
    the off-diagonal pairs b ≠ c contribute to the field strength. -/
theorem selfInteractionW_diag_vanishes (G : GaugeTheory) (a b : Fin G.dim) (x : Spacetime) :
    G.structureConstants a b b • W.wedge (G.A b) (G.A b) x = 0 := by
  have hf : G.structureConstants a b b = 0 := by linarith [G.antisymm a b b]
  rw [hf]
  simp

end GaugeTheory

/-! ## Part 6: Standard Gauge Group Dimensions

The dimension of a Lie algebra determines the number of gauge bosons:
- U(1): 1 generator → 1 boson (photon)
- SU(N): N²-1 generators → N²-1 bosons
- SO(N): N(N-1)/2 generators → N(N-1)/2 bosons

These dimension formulas connect to the existing Lie algebra files:
- gauge_gravity.lean: so(1,3) has 6 generators (Bivector structure)
- su3_color.lean: su(3) has 8 generators (SL3 structure)
- su5_grand.lean: su(5) has 24 generators (SL5 structure)
- so10_grand.lean: so(10) has 45 generators (SO10 structure)
- so14_unification.lean: so(14) has 91 generators (SO14 structure) -/

/-- U(1) has 1 generator (the photon). -/
theorem u1_dim : 1^2 - 1 = 0 := by norm_num

/-- More precisely, U(1) is 1-dimensional (the Lie algebra is ℝ). -/
theorem u1_generators : 1 = 1 := rfl

/-- SU(2) has 2²-1 = 3 generators (W⁺, W⁻, Z bosons before mixing). -/
theorem su2_dim : 2^2 - 1 = 3 := by norm_num

/-- SU(3) has 3²-1 = 8 generators (8 gluons).
    Matches: su3_color.lean uses SL3 with 8 fields. -/
theorem su3_dim : 3^2 - 1 = 8 := by norm_num

/-- SU(5) has 5²-1 = 24 generators (Georgi-Glashow GUT bosons).
    Matches: su5_grand.lean uses SL5 with 24 fields. -/
theorem su5_dim : 5^2 - 1 = 24 := by norm_num

/-- SO(10) has 10×9/2 = 45 generators (Fritzsch-Minkowski GUT bosons).
    Matches: so10_grand.lean uses SO10 with 45 fields. -/
theorem so10_dim : 10 * 9 / 2 = 45 := by norm_num

/-- SO(14) has 14×13/2 = 91 generators (candidate unification).
    Matches: so14_unification.lean uses SO14 with 91 fields. -/
theorem so14_dim : 14 * 13 / 2 = 91 := by norm_num

/-- The Standard Model gauge group SU(3)×SU(2)×U(1) has 8+3+1 = 12 generators. -/
theorem sm_dim : (3^2 - 1) + (2^2 - 1) + 1 = 12 := by norm_num

/-- SO(10) contains enough room for the Standard Model:
    45 > 12 (SM fits inside with 33 additional generators for new physics). -/
theorem so10_contains_sm : 45 > 12 := by norm_num

/-- SO(14) contains enough room for SO(10) plus gravity:
    91 > 45 + 6 (SO(10) + Lorentz group SO(1,3), with 40 additional generators). -/
theorem so14_contains_so10_plus_gravity : 91 > 45 + 6 := by norm_num

/-! ## Part 7: Gauge Potential Component Counting

For a gauge theory with dim generators on 4-dimensional spacetime,
the total number of gauge field components is:

  dim × C(4,1) = dim × 4  (one 1-form per generator, 4 components each)

The field strength has:

  dim × C(4,2) = dim × 6  (one 2-form per generator, 6 components each)

These numbers grow rapidly with the gauge group dimension:
- U(1): 4 potential + 6 field strength = 10 components
- SU(3): 32 potential + 48 field strength = 80 components
- SO(10): 180 potential + 270 field strength = 450 components -/

/-- U(1) gauge potential: 1 × 4 = 4 components (A_μ). -/
theorem u1_potential_components : 1 * 4 = 4 := by norm_num

/-- U(1) field strength: 1 × 6 = 6 components (F_μν). -/
theorem u1_field_components : 1 * 6 = 6 := by norm_num

/-- SU(3) gauge potential: 8 × 4 = 32 components (A^a_μ, a=1..8). -/
theorem su3_potential_components : 8 * 4 = 32 := by norm_num

/-- SU(3) field strength: 8 × 6 = 48 components (F^a_μν, a=1..8). -/
theorem su3_field_components : 8 * 6 = 48 := by norm_num

/-- SO(10) gauge potential: 45 × 4 = 180 components. -/
theorem so10_potential_components : 45 * 4 = 180 := by norm_num

/-- SO(10) field strength: 45 × 6 = 270 components. -/
theorem so10_field_components : 45 * 6 = 270 := by norm_num

/-- SO(14) gauge potential: 91 × 4 = 364 components. -/
theorem so14_potential_components : 91 * 4 = 364 := by norm_num

/-- SO(14) field strength: 91 × 6 = 546 components. -/
theorem so14_field_components : 91 * 6 = 546 := by norm_num

/-! ## Part 8: Structure Constant Antisymmetry Consequences

The antisymmetry of structure constants f^a_{bc} = -f^a_{cb} has
immediate consequences for the self-interaction term. -/

namespace GaugeTheory

/-- Structure constants vanish when two lower indices are equal:
    f^a_{bb} = 0 for all a, b. -/
theorem structureConstants_diag (G : GaugeTheory) (a b : Fin G.dim) :
    G.structureConstants a b b = 0 := by
  have h := G.antisymm a b b
  linarith

/-- For a 1-dimensional Lie algebra (U(1)), the only structure constant
    must be zero (there is only one index value, so b = c always). -/
theorem u1_trivial_structure (G : GaugeTheory) (h : G.dim = 1) :
    ∀ a b c : Fin G.dim, G.structureConstants a b c = 0 := by
  intro a b c
  have hbc : b = c := by ext; omega
  rw [hbc]
  exact structureConstants_diag G a c

end GaugeTheory

/-! ## Part 9: Connection to Existing Codebase

### Generalization of covariant_derivative.lean

`covariant_derivative.lean` defines:
- `GaugePotential`: 12 real fields (4 directions × 3 SU(2) generators)
- `FieldStrength`: 18 real fields (6 2-form components × 3 generators)
- `algebraicFieldStrength`: [A_μ, A_ν] via SU(2) cross product
- `algebraic_bianchi_*`: Jacobi identity for each direction triple

This file (`gauge_connection.lean`) generalizes:
- `GaugeTheory.A`: `Fin dim → DiffForm 1` (n smooth 1-forms, not 12 reals)
- `abelianFieldStrength`: `d(A^a)` via mathlib's exterior derivative
- `abelian_bianchi`: from d²=0 (a theorem, not Jacobi identity)
- `NonAbelianTerm`: axiomatized (vs. computed cross product for SU(2))

### What this file adds

1. **Generality**: works for ANY gauge group, not just SU(2)
2. **Genuine forms**: uses mathlib's DiffForm (functions on spacetime), not flat tuples
3. **Proved Bianchi**: from d^2=0 (calculus), not Jacobi (algebra)
4. **Dimension counting**: connects generator counts to existing Lean files
5. **Wedge-product field strength**: F = dA + f*A wedge A as a definition (not axiom)
6. **Bridge theorem**: wedge construction satisfies the legacy NonAbelianTerm interface

### What covariant_derivative.lean still does better

1. **Explicit non-abelian term**: computes [A_mu, A_nu] via cross product
2. **Matter field coupling**: defines T_a action on doublets
3. **Yang-Mills Lagrangian**: constructs L = -(1/4)Tr(F^2)

### Honest boundary

- [MV] Abelian Bianchi identity d(dA) = 0 (theorem from mathlib)
- [MV] Abelian field strength F = dA (definition using extDeriv)
- [MV] Structure constant antisymmetry consequences (theorems)
- [MV] Dimension counting for all gauge groups (arithmetic)
- [MV] selfInteractionW_abelian: vanishing for abelian theories (theorem)
- [MV] fieldStrengthW_abelian: F = dA for abelian theories (theorem)
- [MV] selfInteractionW_wedge_antisymm: double antisymmetry (theorem)
- [MV] selfInteractionW_diag_vanishes: self-wedge terms are zero (theorem)
- [MV] NonAbelianTerm.fromWedge: bridge to legacy interface (theorem)
- [MV] fieldStrength_eq_fieldStrengthW: new = old via bridge (theorem)
- [AX] wedge : DiffForm 1 -> DiffForm 1 -> DiffForm 2 (from wedge_product.lean)
- [AX-LEGACY] NonAbelianTerm structure (retained for backward compatibility)
- [STUB] Covariant exterior derivative D = d + [A,-] (not yet defined)
- [STUB] Non-abelian Bianchi identity DF = 0 (needs Leibniz rule for d on wedge)
- [STUB] Gauge transformation law (needs group action)

Machine-verified. 0 sorry. Soli Deo Gloria.
-/
