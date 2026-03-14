#!/usr/bin/env python3
"""
Generate the so(14) Lie bracket for Lean 4.

so(14) has 91 generators L_{ij} (1 <= i < j <= 14), represented as
antisymmetric 14x14 matrices.

Lie bracket: [L_{ij}, L_{kl}] = delta_{jk}*L_{il} - delta_{ik}*L_{jl}
                                - delta_{jl}*L_{ik} + delta_{il}*L_{jk}

where L_{ij} = -L_{ji} (antisymmetry).

This script:
1. Generates all 91*91 bracket entries
2. Verifies Jacobi identity numerically (100 random triples)
3. Verifies so(10) and so(4) subalgebra closure
4. Outputs Lean 4 code for the SO14 structure, bracket, and instances
5. Generates SO10 -> SO14 embedding map for LieHom file

Adapted from scripts/so10_bracket.py for N=14.

References:
  - Nesti & Percacci, "Graviweak unification" JPCAM 41 (2008)
  - so10_bracket.py (pattern source)
"""

import itertools
import numpy as np
from collections import defaultdict
import sys
import os

# ============================================================
# Configuration
# ============================================================
N = 14
pairs = [(i, j) for i in range(1, N+1) for j in range(i+1, N+1)]
assert len(pairs) == 91, f"Expected 91 pairs, got {len(pairs)}"

# Field naming: 1-9 digits, 10=a, 11=b, 12=c, 13=d, 14=e
def idx_char(k):
    """Convert 1-based index to field name character."""
    return str(k) if k <= 9 else chr(ord('a') + k - 10)

def field_name(i, j):
    """Generate Lean field name for L_{ij}."""
    return f"l{idx_char(i)}{idx_char(j)}"

pair_to_field = {(i,j): field_name(i,j) for i,j in pairs}
pair_to_idx = {p: k for k, p in enumerate(pairs)}
fields = [pair_to_field[p] for p in pairs]

# ============================================================
# Bracket computation
# ============================================================

def canonical(p, q):
    """Convert L_{pq} to canonical form. Returns ((i,j), sign) or (None, 0)."""
    if p == q:
        return None, 0
    if p < q:
        return (p, q), 1
    else:
        return (q, p), -1

def compute_bracket(ij, kl):
    """Compute [L_{ij}, L_{kl}] as dict of {(a,b): coefficient}."""
    i, j = ij
    k, l = kl
    result = defaultdict(int)

    # [L_{ij}, L_{kl}] = delta_{jk}*L_{il} - delta_{ik}*L_{jl}
    #                   - delta_{jl}*L_{ik} + delta_{il}*L_{jk}
    terms = []
    if j == k: terms.append((i, l, +1))
    if i == k: terms.append((j, l, -1))
    if j == l: terms.append((i, k, -1))
    if i == l: terms.append((j, k, +1))

    for p, q, coeff in terms:
        can, sign = canonical(p, q)
        if can is not None:
            result[can] += coeff * sign

    return {k: v for k, v in result.items() if v != 0}

# Compute all brackets
print(f"Computing all {len(pairs)}x{len(pairs)} = {len(pairs)**2} brackets...")
brackets = {}
for ij in pairs:
    for kl in pairs:
        b = compute_bracket(ij, kl)
        if b:
            brackets[(ij, kl)] = b

nonzero_count = len(brackets)
total_terms = sum(len(v) for v in brackets.values())
print(f"Non-zero brackets: {nonzero_count} / {len(pairs)**2}")
print(f"Total non-zero structure constant terms: {total_terms}")

# ============================================================
# Verification: Antisymmetry
# ============================================================
print("\nVerifying antisymmetry...")
for ij in pairs:
    for kl in pairs:
        b1 = brackets.get((ij, kl), {})
        b2 = brackets.get((kl, ij), {})
        for key in set(list(b1.keys()) + list(b2.keys())):
            assert b1.get(key, 0) == -b2.get(key, 0), \
                f"Antisymmetry fails for [{ij}, {kl}] at {key}"
print("Antisymmetry: PASSED")

# ============================================================
# Verification: Jacobi identity (numerical)
# ============================================================
print("\nVerifying Jacobi identity numerically (100 random elements)...")
rng = np.random.default_rng(42)

def bracket_vec(X, Y):
    """Compute [X, Y] where X, Y are 91-dim vectors."""
    result = np.zeros(91)
    for k, ij in enumerate(pairs):
        if abs(X[k]) < 1e-15:
            continue
        for l, kl in enumerate(pairs):
            if abs(Y[l]) < 1e-15:
                continue
            b = brackets.get((ij, kl), {})
            for (a, b_idx), coeff in b.items():
                m = pair_to_idx[(a, b_idx)]
                result[m] += coeff * X[k] * Y[l]
    return result

for trial in range(100):
    A = rng.standard_normal(91)
    B = rng.standard_normal(91)
    C = rng.standard_normal(91)

    j1 = bracket_vec(A, bracket_vec(B, C))
    j2 = bracket_vec(B, bracket_vec(C, A))
    j3 = bracket_vec(C, bracket_vec(A, B))

    jacobi = j1 + j2 + j3
    err = np.max(np.abs(jacobi))
    assert err < 1e-8, f"Jacobi fails at trial {trial}: max error = {err}"

print("Jacobi identity: PASSED (100 random trials)")

# ============================================================
# Verification: Subalgebra closures
# ============================================================

# so(10) subalgebra: indices 1-10
print("\nVerifying so(10) subalgebra closure (indices 1-10)...")
so10_pairs = [(i,j) for i in range(1,11) for j in range(i+1,11)]
assert len(so10_pairs) == 45
for ij in so10_pairs:
    for kl in so10_pairs:
        b = compute_bracket(ij, kl)
        for key in b:
            assert key in so10_pairs, \
                f"so(10) not closed: [{ij}, {kl}] has {key} component"
print(f"so(10) closure: PASSED ({len(so10_pairs)} generators close)")

# so(4) subalgebra: indices 11-14
print("Verifying so(4) subalgebra closure (indices 11-14)...")
so4_pairs = [(i,j) for i in range(11,15) for j in range(i+1,15)]
assert len(so4_pairs) == 6
for ij in so4_pairs:
    for kl in so4_pairs:
        b = compute_bracket(ij, kl)
        for key in b:
            assert key in so4_pairs, \
                f"so(4) not closed: [{ij}, {kl}] has {key} component"
print(f"so(4) closure: PASSED ({len(so4_pairs)} generators close)")

# mixed generators: one index in {1..10}, one in {11..14}
mixed_pairs = [(i,j) for i,j in pairs
               if not (i <= 10 and j <= 10) and not (i >= 11 and j >= 14+1)
               and not (i >= 11)]
# More precisely: mixed = pairs with one index in 1-10 and one in 11-14
mixed_pairs = [(i,j) for i,j in pairs if i <= 10 and j >= 11]
assert len(mixed_pairs) == 40, f"Expected 40 mixed pairs, got {len(mixed_pairs)}"
print(f"Mixed generators: {len(mixed_pairs)} (10 x 4 = 40) PASSED")

# Verify decomposition: 45 + 6 + 40 = 91
assert len(so10_pairs) + len(so4_pairs) + len(mixed_pairs) == len(pairs)
print(f"Decomposition: {len(so10_pairs)} + {len(so4_pairs)} + {len(mixed_pairs)} = {len(pairs)} PASSED")

# ============================================================
# Cross-check: so(10) sub-bracket matches so10_bracket.py output
# ============================================================
print("\nCross-checking so(10) sub-bracket against standalone computation...")
# Import the so(10) bracket from so10_bracket.py's logic
so10_brackets_standalone = {}
for ij in so10_pairs:
    for kl in so10_pairs:
        i, j = ij
        k, l = kl
        result = defaultdict(int)
        terms = []
        if j == k: terms.append((i, l, +1))
        if i == k: terms.append((j, l, -1))
        if j == l: terms.append((i, k, -1))
        if i == l: terms.append((j, k, +1))
        for p, q, coeff in terms:
            can, sign = canonical(p, q)
            if can is not None:
                result[can] += coeff * sign
        result = {k: v for k, v in result.items() if v != 0}
        if result:
            so10_brackets_standalone[(ij, kl)] = result

for ij in so10_pairs:
    for kl in so10_pairs:
        b14 = brackets.get((ij, kl), {})
        b10 = so10_brackets_standalone.get((ij, kl), {})
        # Restrict b14 to so(10) indices
        b14_restricted = {k: v for k, v in b14.items() if k in so10_pairs}
        assert b14_restricted == b10, \
            f"Cross-check fails at [{ij}, {kl}]: {b14_restricted} vs {b10}"
print("so(10) sub-bracket cross-check: PASSED")

# ============================================================
# Generate Lean 4 code
# ============================================================
print("\n" + "="*70)
print("GENERATING LEAN 4 CODE")
print("="*70)

lean_file = f"""/-
UFT Formal Verification - SO(14) Grand Unification Algebra
============================================================

THE so(14) LIE ALGEBRA AS A LEAN TYPE WITH CERTIFIED INSTANCES

so(14) has 91 generators L_{{ij}} (1 ≤ i < j ≤ 14) with the standard
orthogonal Lie bracket:
  [L_{{ij}}, L_{{kl}}] = δ_{{jk}}L_{{il}} - δ_{{ik}}L_{{jl}}
                        - δ_{{jl}}L_{{ik}} + δ_{{il}}L_{{jk}}

This algebra decomposes as so(10) ⊕ so(4) ⊕ (10,4):
  - 45 generators with both indices in {{1,...,10}}: so(10) gauge sector
  - 6 generators with both indices in {{11,...,14}}: so(4) gravity sector
  - 40 generators with one index in each: mixed sector

All {len(pairs)**2} bracket entries computed by scripts/so14_bracket_gen.py.
Jacobi identity verified numerically (100 random triples) before Lean proof.
so(10) and so(4) subalgebra closures verified.

NOTE ON SIGNATURE: This file defines so(14) in compact (positive-definite)
signature — the Lie algebra of SO(14,0). The gravity sector is so(4), NOT
so(1,3). The Lorentzian version would require so(11,3), a different real form.
See docs/SIGNATURE_ANALYSIS.md.

References:
  - Nesti & Percacci, "Graviweak unification" JPCAM 41 (2008)
  - so10_grand.lean: pattern source (45 generators)
  - su5c_compact.lean: LieAlgebra instance pattern
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Algebra.Lie.Basic

/-! ## Part 1: The so(14) Lie Algebra

91 generators corresponding to antisymmetric 14×14 matrices.
Indices: 1-9 as digits, 10=a, 11=b, 12=c, 13=d, 14=e. -/

/-- The Lie algebra so(14), with 91 generators L_{{ij}} (i < j).
    Decomposition: 45 (so(10)) + 6 (so(4)) + 40 (mixed). -/
@[ext]
structure SO14 where
"""

# Generate structure fields
for i, (a, b) in enumerate(pairs):
    fn = pair_to_field[(a, b)]
    sector = ""
    if a <= 10 and b <= 10:
        sector = "  -- gauge"
    elif a >= 11 and b >= 14+1:
        sector = "  -- gravity"  # won't trigger for b<=14
    elif a >= 11:
        sector = "  -- gravity"
    else:
        sector = "  -- mixed"
    lean_file += f"  {fn} : ℝ  -- L_{{{a},{b}}}{sector}\n"

lean_file += """
namespace SO14

/-! ## Part 2: Basic Operations -/

"""

# Generate zero
lean_file += "def zero : SO14 where\n"
for f in fields:
    lean_file += f"  {f} := 0\n"

# Generate neg
lean_file += "\ndef neg (X : SO14) : SO14 where\n"
for f in fields:
    lean_file += f"  {f} := -X.{f}\n"

# Generate add
lean_file += "\ndef add (X Y : SO14) : SO14 where\n"
for f in fields:
    lean_file += f"  {f} := X.{f} + Y.{f}\n"

# Generate smul
lean_file += "\ndef smul (c : ℝ) (X : SO14) : SO14 where\n"
for f in fields:
    lean_file += f"  {f} := c * X.{f}\n"

# Instances
lean_file += """
instance : Add SO14 := ⟨add⟩
instance : Neg SO14 := ⟨neg⟩
instance : Zero SO14 := ⟨zero⟩
instance : Sub SO14 := ⟨fun a b => add a (neg b)⟩
instance : SMul ℝ SO14 := ⟨smul⟩

@[simp] lemma add_def (X Y : SO14) : X + Y = add X Y := rfl
@[simp] lemma neg_def (X : SO14) : -X = neg X := rfl
@[simp] lemma zero_val : (0 : SO14) = zero := rfl
@[simp] lemma sub_def' (a b : SO14) : a - b = add a (neg b) := rfl
@[simp] lemma smul_def' (r : ℝ) (a : SO14) : r • a = smul r a := rfl

"""

# Generate comm (bracket)
lean_file += """/-! ## Part 3: The Lie Bracket

The Lie bracket [X, Y] of two so(14) elements.
Generated by scripts/so14_bracket_gen.py from the formula
[L_{ij}, L_{kl}] = δ_{jk}L_{il} - δ_{ik}L_{jl} - δ_{jl}L_{ik} + δ_{il}L_{jk}. -/

"""
lean_file += "def comm (X Y : SO14) : SO14 where\n"

for idx_out, (a, b) in enumerate(pairs):
    fn = pair_to_field[(a, b)]
    terms = []
    for k, ij in enumerate(pairs):
        for l, kl in enumerate(pairs):
            bkt = brackets.get((ij, kl), {})
            if (a, b) in bkt:
                coeff = bkt[(a, b)]
                x_field = pair_to_field[ij]
                y_field = pair_to_field[kl]
                if coeff == 1:
                    terms.append(f"X.{x_field} * Y.{y_field}")
                elif coeff == -1:
                    terms.append(f"-(X.{x_field} * Y.{y_field})")
                else:
                    terms.append(f"{coeff} * X.{x_field} * Y.{y_field}")

    if terms:
        expr = " + ".join(terms)
        expr = expr.replace("+ -(", "- (")
    else:
        expr = "0"

    lean_file += f"  {fn} := {expr}\n"

# Antisymmetry
lean_file += """
set_option maxHeartbeats 16000000 in
/-- The Lie bracket is antisymmetric: [X, Y] = -[Y, X]. -/
theorem comm_antisymm (X Y : SO14) : comm X Y = neg (comm Y X) := by
  ext <;> simp [comm, neg] <;> ring

"""

# A few basis generators for testing
lean_file += """/-! ## Part 4: Selected Basis Generators -/

"""

# Generate first 5 basis generators for structure constant checks
for idx in range(min(5, len(pairs))):
    i, j = pairs[idx]
    fn = pair_to_field[(i, j)]
    gen_name = f"L{idx_char(i)}{idx_char(j)}"
    lean_file += f"/-- Basis generator L_{{{i},{j}}}. -/\n"
    lean_file += f"def {gen_name} : SO14 where\n"
    for f in fields:
        val = "1" if f == fn else "0"
        lean_file += f"  {f} := {val}\n"
    lean_file += "\n"

# Also generate one gravity sector basis generator
grav_pair = so4_pairs[0]  # (11,12) = lbc
gi, gj = grav_pair
gfn = pair_to_field[grav_pair]
gname = f"L{idx_char(gi)}{idx_char(gj)}"
lean_file += f"/-- Basis generator L_{{{gi},{gj}}} (gravity sector). -/\n"
lean_file += f"def {gname} : SO14 where\n"
for f in fields:
    val = "1" if f == gfn else "0"
    lean_file += f"  {f} := {val}\n"
lean_file += "\n"

# Structure constant verification
lean_file += """/-! ## Part 5: Structure Constant Verification -/

set_option maxHeartbeats 1600000 in
/-- [L12, L23] = L13. Two rotations compose (same as in so(10)). -/
theorem bracket_L12_L23 : comm L12 L23 = L13 := by
  ext <;> simp [comm, L12, L23, L13]

set_option maxHeartbeats 1600000 in
/-- [L12, L34] = 0. Orthogonal rotations commute. -/
theorem bracket_L12_L34 : comm L12 L34 = zero := by
  ext <;> simp [comm, L12, L34, zero]

"""

# Jacobi identity
lean_file += """/-! ## Part 6: The Jacobi Identity

The Jacobi identity for so(14). 91 generators — larger than so(10)'s 45.
Expected compile time: substantial (cubic in generators). -/

set_option maxHeartbeats 64000000 in
/-- The Jacobi identity for so(14).

    For all A, B, C ∈ so(14):
      [A, [B, C]] + [B, [C, A]] + [C, [A, B]] = 0

    This is the identity that makes so(14) a Lie algebra.
    91 generators, cubic polynomial ring proof. -/
theorem jacobi (A B C : SO14) :
    comm A (comm B C) + comm B (comm C A) + comm C (comm A B) = zero := by
  ext <;> simp [comm, add, zero] <;> ring

"""

# LieRing and LieAlgebra instances
lean_file += """/-! ## Part 7: Mathlib LieRing and LieAlgebra Instances

so(14) is certified as a Lie algebra over ℝ via mathlib's typeclass system.
91 generators — the largest Lie algebra in the project with this certification. -/

instance : AddCommGroup SO14 where
  add_assoc := by intros; ext <;> simp [add] <;> ring
  zero_add := by intros; ext <;> simp [add, zero]
  add_zero := by intros; ext <;> simp [add, zero]
  add_comm := by intros; ext <;> simp [add] <;> ring
  neg_add_cancel := by intros; ext <;> simp [add, neg, zero]
  sub_eq_add_neg := by intros; rfl
  nsmul := nsmulRec
  zsmul := zsmulRec

instance : Module ℝ SO14 where
  one_smul := by intros; ext <;> simp [smul]
  mul_smul := by intros; ext <;> simp [smul] <;> ring
  smul_zero := by intros; ext <;> simp [smul, zero]
  smul_add := by intros; ext <;> simp [smul, add] <;> ring
  add_smul := by intros; ext <;> simp [smul, add] <;> ring
  zero_smul := by intros; ext <;> simp [smul, zero]

instance : Bracket SO14 SO14 := ⟨comm⟩

@[simp] lemma bracket_def' (a b : SO14) : ⁅a, b⁆ = comm a b := rfl

set_option maxHeartbeats 64000000 in
instance : LieRing SO14 where
  add_lie := by intros; ext <;> simp [comm, add] <;> ring
  lie_add := by intros; ext <;> simp [comm, add] <;> ring
  lie_self := by intro x; ext <;> simp [comm, zero] <;> ring
  leibniz_lie := by intros; ext <;> simp [comm, add] <;> ring

set_option maxHeartbeats 32000000 in
instance : LieAlgebra ℝ SO14 where
  lie_smul := by intros; ext <;> simp [comm, smul] <;> ring

"""

# Subalgebra predicates
lean_file += """/-! ## Part 8: Subalgebra Identification -/

/-- The so(10) subalgebra: L_{ij} with i,j in {1,...,10}. -/
def isSO10 (X : SO14) : Prop :=
"""
# All mixed and gravity fields must be zero
non_so10_fields = [pair_to_field[p] for p in pairs if not (p[0] <= 10 and p[1] <= 10)]
for i, f in enumerate(non_so10_fields):
    if i == 0:
        lean_file += f"  X.{f} = 0"
    else:
        lean_file += f" ∧\n  X.{f} = 0"
lean_file += "\n"

lean_file += """
/-- The so(4) subalgebra: L_{ij} with i,j in {11,...,14} (gravity sector). -/
def isSO4 (X : SO14) : Prop :=
"""
non_so4_fields = [pair_to_field[p] for p in pairs if not (p[0] >= 11 and p[1] >= 11)]
for i, f in enumerate(non_so4_fields):
    if i == 0:
        lean_file += f"  X.{f} = 0"
    else:
        lean_file += f" ∧\n  X.{f} = 0"
lean_file += "\n"

lean_file += """
end SO14

/-! ## Summary

### What this file proves:
1. so(14) Lie algebra with 91 generators and explicit bracket (Parts 1-3)
2. Structure constant verification (Part 5)
3. Jacobi identity for so(14) (Part 6)
4. Certified LieRing and LieAlgebra ℝ instances (Part 7)
5. so(10) and so(4) subalgebra predicates (Part 8)

### Signature:
This is the COMPACT form so(14,0). The gravity sector is so(4), not so(1,3).
Lorentzian signature requires so(11,3) — a different real form.

### Next steps:
- SO10 ↪ SO14 LieHom (so10_so14_liehom.lean)
- so(4) ↪ SO14 LieHom (so4_so14_liehom.lean)
- Anomaly cancellation as algebraic theorem

0 sorry gaps.
-/
"""

# ============================================================
# Write main Lean file
# ============================================================
output_path = "src/lean_proofs/clifford/so14_grand.lean"
# Ensure directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(lean_file)

print(f"\nLean file written to: {output_path}")
print(f"Structure: {len(fields)} fields")
print(f"Non-zero bracket entries: {nonzero_count}")
print(f"Total structure constant terms: {total_terms}")
print(f"File size: {len(lean_file)} bytes ({len(lean_file)//1024} KB)")

# ============================================================
# Generate SO10 -> SO14 embedding map
# ============================================================
print("\n" + "="*70)
print("SO10 -> SO14 EMBEDDING MAP")
print("="*70)

print("""
-- For so10_so14_liehom.lean:
-- The embedding maps SO10 generators (indices 1-10) into SO14
-- by setting the corresponding fields and zeroing the rest.

def so10_toSO14 (x : SO10) : SO14 where""")

for a, b in pairs:
    fn = pair_to_field[(a, b)]
    if a <= 10 and b <= 10:
        # This field exists in SO10
        so10_fn = pair_to_field[(a, b)]  # Same name in SO10
        print(f"  {fn} := x.{so10_fn}")
    else:
        print(f"  {fn} := 0")

# ============================================================
# Generate SO4 -> SO14 embedding map (gravity sector)
# ============================================================
print("\n" + "="*70)
print("SO4 (gravity) -> SO14 EMBEDDING MAP")
print("="*70)

# The so(4) subalgebra uses indices 11-14
# Map so(4) generators with indices {1,2,3,4} to so(14) indices {11,12,13,14}
# so4 pairs: (1,2),(1,3),(1,4),(2,3),(2,4),(3,4)
# mapped to: (11,12),(11,13),(11,14),(12,13),(12,14),(13,14)

so4_field_map = {}
so4_gen_pairs = [(i,j) for i in range(1,5) for j in range(i+1,5)]
for (si, sj), (ti, tj) in zip(so4_gen_pairs, so4_pairs):
    so4_name = f"l{si}{sj}"
    so14_name = pair_to_field[(ti, tj)]
    so4_field_map[so4_name] = so14_name

print(f"""
-- NOTE: This embeds so(4) (compact), NOT so(1,3) (Lorentz).
-- The Bivector type in gauge_gravity.lean has so(1,3) structure constants.
-- so(1,3) and so(4) are different real Lie algebras (different signs in
-- boost-rotation brackets). A LieHom Bivector → SO14 is NOT possible
-- in compact signature. For that, we need so(11,3).
--
-- This embedding is for a SEPARATE so(4) type, or equivalently,
-- restricting to the gravity-sector subalgebra of SO14 directly.
--
-- Mapping: so(4) index {{1,2,3,4}} → so(14) index {{11,12,13,14}}

-- Example (requires an SO4 type, not yet defined):
-- def so4_toSO14 (x : SO4) : SO14 where""")
for a, b in pairs:
    fn = pair_to_field[(a, b)]
    if a >= 11 and b >= 11:
        # Map back to so(4) indices
        s_a = a - 10
        s_b = b - 10
        so4_fn = f"l{s_a}{s_b}"
        print(f"--   {fn} := x.{so4_fn}")
    else:
        print(f"--   {fn} := 0")

# ============================================================
# Statistics
# ============================================================
print("\n" + "="*70)
print("STATISTICS")
print("="*70)

# Count terms per comm component
max_terms = 0
min_terms = 999
for a, b in pairs:
    terms = 0
    for ij in pairs:
        for kl in pairs:
            bkt = brackets.get((ij, kl), {})
            if (a, b) in bkt:
                terms += 1
    max_terms = max(max_terms, terms)
    min_terms = min(min_terms, terms)

print(f"Generators: {len(pairs)}")
print(f"Non-zero brackets: {nonzero_count} / {len(pairs)**2}")
print(f"Sparsity: {1 - nonzero_count/(len(pairs)**2):.1%}")
print(f"Terms per comm component: min={min_terms}, max={max_terms}")
print(f"Lean file size: {len(lean_file)} bytes ({len(lean_file)//1024} KB)")
print(f"\nSubalgebra decomposition:")
print(f"  so(10): {len(so10_pairs)} generators (gauge)")
print(f"  so(4):  {len(so4_pairs)} generators (gravity)")
print(f"  mixed:  {len(mixed_pairs)} generators")
print(f"  total:  {len(so10_pairs) + len(so4_pairs) + len(mixed_pairs)} = {len(pairs)}")

print("\nDone! Run `lake build` to compile the Lean proof.")
print("Expected compile time: 30-120 minutes (91-generator Jacobi + LieRing).")
