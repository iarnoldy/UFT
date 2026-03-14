#!/usr/bin/env python3
"""
Generate the so(16) Lie bracket for Lean 4.

so(16) has 120 generators L_{ij} (1 <= i < j <= 16), represented as
antisymmetric 16x16 matrices.

Lie bracket: [L_{ij}, L_{kl}] = delta_{jk}*L_{il} - delta_{ik}*L_{jl}
                                - delta_{jl}*L_{ik} + delta_{il}*L_{jk}

where L_{ij} = -L_{ji} (antisymmetry).

This script:
1. Generates all 120*120 bracket entries
2. Verifies Jacobi identity numerically (100 random triples)
3. Verifies so(14) and so(10) subalgebra closure
4. Outputs Lean 4 code for the SO16 structure, bracket, and instances
5. Generates SO14 -> SO16 embedding map and LieHom file

Adapted from scripts/so14_bracket_gen.py for N=16.

References:
  - so14_bracket_gen.py (pattern source)
  - so10_so14_liehom.lean (LieHom pattern)
"""

import itertools
import numpy as np
from collections import defaultdict
import sys
import os

# ============================================================
# Configuration
# ============================================================
N = 16
pairs = [(i, j) for i in range(1, N+1) for j in range(i+1, N+1)]
assert len(pairs) == 120, f"Expected 120 pairs, got {len(pairs)}"

# Field naming: 1-9 digits, 10=a, 11=b, 12=c, 13=d, 14=e, 15=f, 16=g
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
    """Compute [X, Y] where X, Y are 120-dim vectors."""
    result = np.zeros(120)
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
    A = rng.standard_normal(120)
    B = rng.standard_normal(120)
    C = rng.standard_normal(120)

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

# so(14) subalgebra: indices 1-14
print("\nVerifying so(14) subalgebra closure (indices 1-14)...")
so14_pairs = [(i,j) for i in range(1,15) for j in range(i+1,15)]
assert len(so14_pairs) == 91
for ij in so14_pairs:
    for kl in so14_pairs:
        b = compute_bracket(ij, kl)
        for key in b:
            assert key in so14_pairs, \
                f"so(14) not closed: [{ij}, {kl}] has {key} component"
print(f"so(14) closure: PASSED ({len(so14_pairs)} generators close)")

# so(10) subalgebra: indices 1-10
print("Verifying so(10) subalgebra closure (indices 1-10)...")
so10_pairs = [(i,j) for i in range(1,11) for j in range(i+1,11)]
assert len(so10_pairs) == 45
for ij in so10_pairs:
    for kl in so10_pairs:
        b = compute_bracket(ij, kl)
        for key in b:
            assert key in so10_pairs, \
                f"so(10) not closed: [{ij}, {kl}] has {key} component"
print(f"so(10) closure: PASSED ({len(so10_pairs)} generators close)")

# Complement: indices 15-16 form so(2) — just 1 generator
so2_pairs = [(15,16)]
print(f"so(2) complement (indices 15-16): {len(so2_pairs)} generator")
for ij in so2_pairs:
    for kl in so2_pairs:
        b = compute_bracket(ij, kl)
        for key in b:
            assert key in so2_pairs, \
                f"so(2) not closed: [{ij}, {kl}] has {key} component"
print(f"so(2) closure: PASSED ({len(so2_pairs)} generator closes trivially)")

# mixed generators: one index in {1..14}, one in {15..16}
mixed_pairs = [(i,j) for i,j in pairs if i <= 14 and j >= 15]
print(f"Mixed generators (so(14) x so(2)): {len(mixed_pairs)}")

# Verify decomposition: 91 + 1 + 28 = 120
# Actually: so(14) has 91, so(2) has 1, mixed has 14*2 = 28
extra_pairs = [(i,j) for i,j in pairs if not (i <= 14 and j <= 14)]
so16_complement = [p for p in extra_pairs if p[0] >= 15 and p[1] >= 15]
so16_mixed = [p for p in extra_pairs if not (p[0] >= 15 and p[1] >= 15)]
assert len(so14_pairs) + len(so16_complement) + len(so16_mixed) == len(pairs), \
    f"{len(so14_pairs)} + {len(so16_complement)} + {len(so16_mixed)} != {len(pairs)}"
print(f"Decomposition: {len(so14_pairs)} (so14) + {len(so16_complement)} (so2) + {len(so16_mixed)} (mixed) = {len(pairs)} PASSED")

# ============================================================
# Cross-check: so(14) sub-bracket matches standalone computation
# ============================================================
print("\nCross-checking so(14) sub-bracket against standalone computation...")
so14_brackets_standalone = {}
for ij in so14_pairs:
    for kl in so14_pairs:
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
            so14_brackets_standalone[(ij, kl)] = result

for ij in so14_pairs:
    for kl in so14_pairs:
        b16 = brackets.get((ij, kl), {})
        b14 = so14_brackets_standalone.get((ij, kl), {})
        # Restrict b16 to so(14) indices
        b16_restricted = {k: v for k, v in b16.items() if k in so14_pairs}
        assert b16_restricted == b14, \
            f"Cross-check fails at [{ij}, {kl}]: {b16_restricted} vs {b14}"
print("so(14) sub-bracket cross-check: PASSED")

# ============================================================
# Generate Lean 4 code
# ============================================================
print("\n" + "="*70)
print("GENERATING LEAN 4 CODE")
print("="*70)

lean_file = f"""/-
UFT Formal Verification - SO(16) Lie Algebra
============================================================

THE so(16) LIE ALGEBRA AS A LEAN TYPE WITH CERTIFIED INSTANCES

so(16) has 120 generators L_{{ij}} (1 ≤ i < j ≤ 16) with the standard
orthogonal Lie bracket:
  [L_{{ij}}, L_{{kl}}] = δ_{{jk}}L_{{il}} - δ_{{ik}}L_{{jl}}
                        - δ_{{jl}}L_{{ik}} + δ_{{il}}L_{{jk}}

This algebra contains so(14) as a subalgebra (indices 1-14):
  - 91 generators with both indices in {{1,...,14}}: so(14) subalgebra
  - 1 generator with both indices in {{15,16}}: so(2) complement
  - 28 generators with one index in {{1,...,14}} and one in {{15,16}}: mixed

All {len(pairs)**2} bracket entries computed by scripts/so16_bracket_gen.py.
Jacobi identity verified numerically (100 random triples) before Lean proof.
so(14) and so(10) subalgebra closures verified.

NOTE ON SIGNATURE: This file defines so(16) in compact (positive-definite)
signature — the Lie algebra of SO(16,0). See docs/SIGNATURE_ANALYSIS.md.

References:
  - so14_grand.lean: pattern source (91 generators)
  - scripts/so16_bracket_gen.py: generator script
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Algebra.Lie.Basic

/-! ## Part 1: The so(16) Lie Algebra

120 generators corresponding to antisymmetric 16×16 matrices.
Indices: 1-9 as digits, 10=a, 11=b, 12=c, 13=d, 14=e, 15=f, 16=g. -/

/-- The Lie algebra so(16), with 120 generators L_{{ij}} (i < j).
    Contains so(14) as subalgebra (91 generators, indices 1-14). -/
@[ext]
structure SO16 where
"""

# Generate structure fields
for i_idx, (a, b) in enumerate(pairs):
    fn = pair_to_field[(a, b)]
    if a <= 14 and b <= 14:
        sector = "  -- so(14)"
    elif a >= 15:
        sector = "  -- so(2)"
    else:
        sector = "  -- mixed"
    lean_file += f"  {fn} : ℝ  -- L_{{{a},{b}}}{sector}\n"

lean_file += """
namespace SO16

/-! ## Part 2: Basic Operations -/

"""

# Generate zero
lean_file += "def zero : SO16 where\n"
for f in fields:
    lean_file += f"  {f} := 0\n"

# Generate neg
lean_file += "\ndef neg (X : SO16) : SO16 where\n"
for f in fields:
    lean_file += f"  {f} := -X.{f}\n"

# Generate add
lean_file += "\ndef add (X Y : SO16) : SO16 where\n"
for f in fields:
    lean_file += f"  {f} := X.{f} + Y.{f}\n"

# Generate smul
lean_file += "\ndef smul (c : ℝ) (X : SO16) : SO16 where\n"
for f in fields:
    lean_file += f"  {f} := c * X.{f}\n"

# Instances
lean_file += """
instance : Add SO16 := ⟨add⟩
instance : Neg SO16 := ⟨neg⟩
instance : Zero SO16 := ⟨zero⟩
instance : Sub SO16 := ⟨fun a b => add a (neg b)⟩
instance : SMul ℝ SO16 := ⟨smul⟩

@[simp] lemma add_def (X Y : SO16) : X + Y = add X Y := rfl
@[simp] lemma neg_def (X : SO16) : -X = neg X := rfl
@[simp] lemma zero_val : (0 : SO16) = zero := rfl
@[simp] lemma sub_def' (a b : SO16) : a - b = add a (neg b) := rfl
@[simp] lemma smul_def' (r : ℝ) (a : SO16) : r • a = smul r a := rfl

"""

# Generate comm (bracket)
lean_file += """/-! ## Part 3: The Lie Bracket

The Lie bracket [X, Y] of two so(16) elements.
Generated by scripts/so16_bracket_gen.py from the formula
[L_{ij}, L_{kl}] = δ_{jk}L_{il} - δ_{ik}L_{jl} - δ_{jl}L_{ik} + δ_{il}L_{jk}. -/

"""
lean_file += "def comm (X Y : SO16) : SO16 where\n"

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
set_option maxHeartbeats 32000000 in
/-- The Lie bracket is antisymmetric: [X, Y] = -[Y, X]. -/
theorem comm_antisymm (X Y : SO16) : comm X Y = neg (comm Y X) := by
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
    lean_file += f"def {gen_name} : SO16 where\n"
    for f in fields:
        val = "1" if f == fn else "0"
        lean_file += f"  {f} := {val}\n"
    lean_file += "\n"

# Structure constant verification
lean_file += """/-! ## Part 5: Structure Constant Verification -/

set_option maxHeartbeats 3200000 in
/-- [L12, L23] = L13. Two rotations compose (same as in so(10), so(14)). -/
theorem bracket_L12_L23 : comm L12 L23 = L13 := by
  ext <;> simp [comm, L12, L23, L13]

set_option maxHeartbeats 3200000 in
/-- [L12, L34] = 0. Orthogonal rotations commute. -/
theorem bracket_L12_L34 : comm L12 L34 = zero := by
  ext <;> simp [comm, L12, L34, zero]

"""

# Jacobi identity
lean_file += """/-! ## Part 6: The Jacobi Identity

The Jacobi identity for so(16). 120 generators — larger than so(14)'s 91.
Expected compile time: substantial (cubic in generators). -/

set_option maxHeartbeats 128000000 in
/-- The Jacobi identity for so(16).

    For all A, B, C ∈ so(16):
      [A, [B, C]] + [B, [C, A]] + [C, [A, B]] = 0

    This is the identity that makes so(16) a Lie algebra.
    120 generators, cubic polynomial ring proof. -/
theorem jacobi (A B C : SO16) :
    comm A (comm B C) + comm B (comm C A) + comm C (comm A B) = zero := by
  ext <;> simp [comm, add, zero] <;> ring

"""

# LieRing and LieAlgebra instances
lean_file += """/-! ## Part 7: Mathlib LieRing and LieAlgebra Instances

so(16) is certified as a Lie algebra over ℝ via mathlib's typeclass system.
120 generators — the largest Lie algebra in the project with this certification. -/

instance : AddCommGroup SO16 where
  add_assoc := by intros; ext <;> simp [add] <;> ring
  zero_add := by intros; ext <;> simp [add, zero]
  add_zero := by intros; ext <;> simp [add, zero]
  add_comm := by intros; ext <;> simp [add] <;> ring
  neg_add_cancel := by intros; ext <;> simp [add, neg, zero]
  sub_eq_add_neg := by intros; rfl
  nsmul := nsmulRec
  zsmul := zsmulRec

instance : Module ℝ SO16 where
  one_smul := by intros; ext <;> simp [smul]
  mul_smul := by intros; ext <;> simp [smul] <;> ring
  smul_zero := by intros; ext <;> simp [smul, zero]
  smul_add := by intros; ext <;> simp [smul, add] <;> ring
  add_smul := by intros; ext <;> simp [smul, add] <;> ring
  zero_smul := by intros; ext <;> simp [smul, zero]

instance : Bracket SO16 SO16 := ⟨comm⟩

@[simp] lemma bracket_def' (a b : SO16) : ⁅a, b⁆ = comm a b := rfl

set_option maxHeartbeats 400000000 in
instance : LieRing SO16 where
  add_lie := by intros; ext <;> simp [comm, add] <;> ring
  lie_add := by intros; ext <;> simp [comm, add] <;> ring
  lie_self := by intro x; ext <;> simp [comm, zero] <;> ring
  leibniz_lie := by intros; ext <;> simp [comm, add] <;> ring

set_option maxHeartbeats 256000000 in
instance : LieAlgebra ℝ SO16 where
  lie_smul := by intros; ext <;> simp [comm, smul] <;> ring

"""

# Subalgebra predicates
lean_file += """/-! ## Part 8: Subalgebra Identification -/

/-- The so(14) subalgebra: L_{ij} with i,j in {1,...,14}. -/
def isSO14 (X : SO16) : Prop :=
"""
# All non-so(14) fields must be zero
non_so14_fields = [pair_to_field[p] for p in pairs if not (p[0] <= 14 and p[1] <= 14)]
for i, f in enumerate(non_so14_fields):
    if i == 0:
        lean_file += f"  X.{f} = 0"
    else:
        lean_file += f" ∧\n  X.{f} = 0"
lean_file += "\n"

lean_file += """
/-- The so(10) subalgebra: L_{ij} with i,j in {1,...,10}. -/
def isSO10 (X : SO16) : Prop :=
"""
non_so10_fields = [pair_to_field[p] for p in pairs if not (p[0] <= 10 and p[1] <= 10)]
for i, f in enumerate(non_so10_fields):
    if i == 0:
        lean_file += f"  X.{f} = 0"
    else:
        lean_file += f" ∧\n  X.{f} = 0"
lean_file += "\n"

lean_file += """
end SO16

/-! ## Summary

### What this file proves:
1. so(16) Lie algebra with 120 generators and explicit bracket (Parts 1-3)
2. Structure constant verification (Part 5)
3. Jacobi identity for so(16) (Part 6)
4. Certified LieRing and LieAlgebra ℝ instances (Part 7)
5. so(14) and so(10) subalgebra predicates (Part 8)

### Signature:
This is the COMPACT form so(16,0).

### Next steps:
- SO14 ↪ SO16 LieHom (so14_so16_liehom.lean)
- Connection to E₈ via half-spinor representation

0 sorry gaps.
-/
"""

# ============================================================
# Write main Lean file
# ============================================================
output_path = "src/lean_proofs/clifford/so16_grand.lean"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(lean_file)

print(f"\nLean file written to: {output_path}")
print(f"Structure: {len(fields)} fields")
print(f"Non-zero bracket entries: {nonzero_count}")
print(f"Total structure constant terms: {total_terms}")
print(f"File size: {len(lean_file)} bytes ({len(lean_file)//1024} KB)")

# ============================================================
# Generate SO14 -> SO16 LieHom file
# ============================================================
print("\n" + "="*70)
print("GENERATING SO14 -> SO16 LieHom FILE")
print("="*70)

# SO14 has 91 generators with pairs (i,j) where 1 <= i < j <= 14
# These map to the first 91 fields of SO16 (same field names)
so14_pairs_list = [(i,j) for i in range(1,15) for j in range(i+1,15)]
so14_field_set = set(pair_to_field[p] for p in so14_pairs_list)

liehom_file = """/-
UFT Formal Verification - SO(14) →ₗ⁅ℝ⁆ SO(16) Lie Homomorphism
=================================================================

CERTIFIED LIE ALGEBRA EMBEDDING: so(14) INTO so(16)

This file constructs a LieHom from so(14) (defined in so14_grand.lean)
to so(16) (defined in so16_grand.lean).

The embedding is the block-diagonal inclusion: the first 14 indices of
so(16) form an so(14) subalgebra. Generators L_{ij} with i,j ∈ {1,...,14}
map directly to the corresponding SO16 fields; all other fields are zero.

91 of the 120 SO16 slots receive SO14 data.
29 slots are zero (1 so(2) + 28 mixed).

The key theorem: so14_embed preserves the Lie bracket:
  embed([X,Y]_{so14}) = [embed(X), embed(Y)]_{so16}

This extends the certified morphism chain:
  SU5C →ₗ⁅ℝ⁆ SO10 →ₗ⁅ℝ⁆ SO14 →ₗ⁅ℝ⁆ SO16

References:
  - so14_grand.lean: SO14 type with LieAlgebra ℝ instance
  - so16_grand.lean: SO16 type with LieAlgebra ℝ instance
  - so10_so14_liehom.lean: pattern source
  - scripts/so16_bracket_gen.py: embedding function specification
-/

import clifford.so14_grand
import clifford.so16_grand

/-! ## Part 1: The Embedding Function -/

/-- The embedding of so(14) into so(16).
    Each SO14 component maps to the corresponding SO16 component.
    Generated by scripts/so16_bracket_gen.py.

    91 of the 120 SO16 slots receive SO14 data.
    29 slots are zero (the so(2) complement + mixed directions). -/
def so14_toSO16 (x : SO14) : SO16 where
"""

# Generate embedding function
for a, b in pairs:
    fn = pair_to_field[(a, b)]
    if a <= 14 and b <= 14:
        # This field exists in SO14 — use same field name
        liehom_file += f"  {fn} := x.{fn}\n"
    else:
        liehom_file += f"  {fn} := 0\n"

liehom_file += """
/-! ## Part 2: Linearity Proofs -/

theorem so14_toSO16_add (a b : SO14) :
    so14_toSO16 (a + b) = so14_toSO16 a + so14_toSO16 b := by
  ext <;> simp [so14_toSO16, SO14.add, SO16.add, SO14.add_def, SO16.add_def] <;> ring

theorem so14_toSO16_smul (r : ℝ) (a : SO14) :
    so14_toSO16 (r • a) = r • so14_toSO16 a := by
  ext <;> simp [so14_toSO16, SO14.smul, SO16.smul, SO14.smul_def', SO16.smul_def'] <;> ring

/-! ## Part 3: Bracket Preservation (The Main Theorem) -/

set_option maxHeartbeats 256000000 in
/-- THE HOMOMORPHISM THEOREM: the embedding preserves the Lie bracket.
    so14_toSO16([X,Y]_{so14}) = [so14_toSO16(X), so14_toSO16(Y)]_{so16}

    This certifies that so(14) is a genuine Lie subalgebra of so(16),
    with the bracket preserved exactly.

    182 input variables (91 per argument) × 120 output goals × polynomial ring.
    Budget: 256M heartbeats. Many output components are trivially zero
    (mixed/complement fields are zero on both sides). -/
theorem so14_toSO16_lie (x y : SO14) :
    so14_toSO16 ⁅x, y⁆ = ⁅so14_toSO16 x, so14_toSO16 y⁆ := by
  ext <;> simp [so14_toSO16, SO14.comm, SO16.comm, SO14.bracket_def', SO16.bracket_def'] <;> ring

/-! ## Part 4: The Certified LieHom -/

/-- The certified Lie algebra homomorphism SO14 →ₗ⁅ℝ⁆ SO16.
    This extends the certified morphism chain:
    SU5C →ₗ⁅ℝ⁆ SO10 →ₗ⁅ℝ⁆ SO14 →ₗ⁅ℝ⁆ SO16

    Combined with so10_embed : SO10 →ₗ⁅ℝ⁆ SO14, this gives
    a three-arrow certified chain from su(5) to so(16). -/
def so14_embed : SO14 →ₗ⁅ℝ⁆ SO16 :=
  { toLinearMap := {
      toFun := so14_toSO16
      map_add' := so14_toSO16_add
      map_smul' := so14_toSO16_smul
    }
    map_lie' := fun {x} {y} => so14_toSO16_lie x y }

/-! ## Summary

### What this file proves:
1. Linear embedding so14_toSO16 : SO14 → SO16 (Part 1)
2. Linearity: preserves addition and scalar multiplication (Part 2)
3. Bracket preservation: embed([X,Y]) = [embed(X), embed(Y)] (Part 3)
4. Certified LieHom: SO14 →ₗ⁅ℝ⁆ SO16 (Part 4)

### What this enables:
- **Composable chain**: SU5C →ₗ⁅ℝ⁆ SO10 →ₗ⁅ℝ⁆ SO14 →ₗ⁅ℝ⁆ SO16
- **so(14) subalgebra identification**: so(14) sits inside so(16)
  as the subalgebra on indices 1-14
- **Connection to E₈**: so(16) is a maximal subalgebra of E₈

### Relationship to so10_so14_liehom.lean:
That file provides SO10 →ₗ⁅ℝ⁆ SO14 (45→91 generators).
This file provides SO14 →ₗ⁅ℝ⁆ SO16 (91→120 generators).
Composition gives the chain SO10 →ₗ⁅ℝ⁆ SO16.

0 sorry gaps.
-/
"""

liehom_output_path = "src/lean_proofs/clifford/so14_so16_liehom.lean"
with open(liehom_output_path, 'w', encoding='utf-8') as f:
    f.write(liehom_file)

print(f"LieHom file written to: {liehom_output_path}")
print(f"File size: {len(liehom_file)} bytes ({len(liehom_file)//1024} KB)")

# ============================================================
# Print embedding map for reference
# ============================================================
print("\n" + "="*70)
print("SO14 -> SO16 EMBEDDING MAP")
print("="*70)

print(f"\n-- SO14 fields mapped: {len(so14_pairs_list)} / {len(pairs)}")
print(f"-- SO16 zero fields: {len(pairs) - len(so14_pairs_list)}")
for a, b in pairs:
    fn = pair_to_field[(a, b)]
    if a <= 14 and b <= 14:
        print(f"  {fn} := x.{fn}  -- L_{{{a},{b}}}")
    else:
        print(f"  {fn} := 0        -- L_{{{a},{b}}}")

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
    t = 0
    for ij in pairs:
        for kl in pairs:
            bkt = brackets.get((ij, kl), {})
            if (a, b) in bkt:
                t += 1
    max_terms = max(max_terms, t)
    min_terms = min(min_terms, t)

print(f"Generators: {len(pairs)}")
print(f"Non-zero brackets: {nonzero_count} / {len(pairs)**2}")
print(f"Sparsity: {1 - nonzero_count/(len(pairs)**2):.1%}")
print(f"Terms per comm component: min={min_terms}, max={max_terms}")
print(f"Lean file size: {len(lean_file)} bytes ({len(lean_file)//1024} KB)")
print(f"LieHom file size: {len(liehom_file)} bytes ({len(liehom_file)//1024} KB)")
print(f"\nSubalgebra decomposition (so14 + so2 + mixed):")
print(f"  so(14): {len(so14_pairs_list)} generators")
print(f"  so(2):  {len(so2_pairs)} generator")
print(f"  mixed:  {len(so16_mixed)} generators")
print(f"  total:  {len(so14_pairs_list) + len(so2_pairs) + len(so16_mixed)} = {len(pairs)}")

print("\nDone! Run `lake build` to compile the Lean proofs.")
print("Expected compile time: VERY LONG (120-generator Jacobi + LieRing).")
print("The LieRing budget is set to 400M heartbeats; LieAlgebra to 256M.")
