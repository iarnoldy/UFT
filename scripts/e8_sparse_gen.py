#!/usr/bin/env python3
"""
E₈ Sparse Jacobi Generator
=============================

Generates Lean 4 files that verify E₈ is a Lie algebra using sparse
structure constant iteration. Instead of 30,628 matrix commutator checks
(900 CPU-hours), this verifies Jacobi directly on the structure constant
function with sparse inner loops (~3-4 CPU-hours).

Generates:
  - e8_sparse_defs.lean: bracket table + lookup + Jacobi check function
  - e8_sparse_jac_NN.lean (16 files): Jacobi theorems chunked by i-value
  - e8_sparse_antisymm.lean: antisymmetry verification

Input: research/e8-construction/e8_structure_constants.json
"""

import json
import os
import sys


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'research', 'e8-construction',
                              'e8_structure_constants.json')
    out_dir = os.path.join(base_dir, 'src', 'lean_proofs', 'clifford')

    print(f"Loading {json_path}...")
    with open(json_path) as f:
        data = json.load(f)

    sc = {}
    for key_str, terms in data['structure_constants'].items():
        i, j = map(int, key_str.split(','))
        sc[(i, j)] = [(k, c) for k, c in terms]

    n = 248
    print(f"  {len(sc)} nonzero bracket pairs")

    # Count total terms
    total_terms = sum(len(terms) for terms in sc.values())
    print(f"  {total_terms} total nonzero structure constant entries")

    # ═══════════════════════════════════════════════════════
    # Generate e8_sparse_defs.lean
    # ═══════════════════════════════════════════════════════
    print("\nGenerating e8_sparse_defs.lean...")

    lines = []
    lines.append("/-")
    lines.append("E₈ Lie Algebra — Sparse Structure Constants")
    lines.append("=============================================")
    lines.append("")
    lines.append("Defines the E₈ bracket as a sparse lookup table.")
    lines.append(f"7,752 nonzero bracket pairs, {total_terms} nonzero structure constants.")
    lines.append("Generated from SageMath oracle (Chevalley basis).")
    lines.append("")
    lines.append("Basis: H_1..H_8 (0-7), E_1..E_120 (8-127), F_1..F_120 (128-247)")
    lines.append("-/")
    lines.append("")
    lines.append("import Mathlib.Tactic")
    lines.append("")
    lines.append("set_option maxHeartbeats 16000000")
    lines.append("")
    lines.append("namespace E8Sparse")
    lines.append("")

    # Generate bracket data (upper triangle only)
    lines.append("/-- Nonzero brackets [B_i, B_j] for i < j. -/")
    lines.append("private def bracketData : List (Nat × Nat × List (Nat × Int)) :=")

    bracket_strs = []
    for (i, j), terms in sorted(sc.items()):
        term_str = ", ".join(f"({k}, {c})" for k, c in sorted(terms))
        bracket_strs.append(f"  ({i}, {j}, [{term_str}])")

    # Write in chunks to avoid overly long lines
    lines.append("  [" + ",\n   ".join(bracket_strs) + "]")
    lines.append("")

    # Build table function
    lines.append(f"/-- Sparse bracket table: Array of {n}×{n} = {n*n} entries. -/")
    lines.append("private def buildBracketTable : Array (List (Nat × Int)) :=")
    lines.append(f"  let base := (List.replicate {n*n} ([] : List (Nat × Int))).toArray")
    lines.append(f"  let t := bracketData.foldl (fun acc (i, j, terms) =>")
    lines.append(f"    acc.set! (i * {n} + j) terms) base")
    lines.append(f"  bracketData.foldl (fun acc (i, j, terms) =>")
    lines.append(f"    acc.set! (j * {n} + i) (terms.map fun (k, c) => (k, -c))) t")
    lines.append("")

    lines.append("private def bktTable : Array (List (Nat × Int)) := buildBracketTable")
    lines.append("")

    # Lookup function
    lines.append(f"/-- Look up [B_i, B_j] as a list of (k, coefficient) pairs. -/")
    lines.append(f"def bkt (i j : Nat) : List (Nat × Int) :=")
    lines.append(f"  bktTable.getD (i * {n} + j) []")
    lines.append("")

    # Sparse Jacobi term
    lines.append("/-- Sparse Jacobi term: Σ_{m : f(i,j,m)≠0} f(i,j,m) * f(m,k,l). -/")
    lines.append("def jacobiTerm (bkt_ij : List (Nat × Int)) (k l : Nat) : Int :=")
    lines.append("  bkt_ij.foldl (fun acc (m, c_m) =>")
    lines.append("    let f_mkl := (bkt m k).foldl")
    lines.append("      (fun a (idx, c) => if idx == l then a + c else a) 0")
    lines.append("    acc + c_m * f_mkl) 0")
    lines.append("")

    # Jacobi check function
    lines.append("/-- Full Jacobi check for a single (i,j,k,l) quadruple. -/")
    lines.append(f"def jacobiCheck (i j k l : Fin {n}) : Int :=")
    lines.append("  jacobiTerm (bkt i.val j.val) k.val l.val +")
    lines.append("  jacobiTerm (bkt j.val k.val) i.val l.val +")
    lines.append("  jacobiTerm (bkt k.val i.val) j.val l.val")
    lines.append("")

    lines.append("end E8Sparse")
    lines.append("")

    defs_path = os.path.join(out_dir, 'e8_sparse_defs.lean')
    with open(defs_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"  Written: {defs_path} ({len(lines)} lines)")

    # ═══════════════════════════════════════════════════════
    # Generate Jacobi chunk files (16 files)
    # ═══════════════════════════════════════════════════════
    n_chunks = 16
    chunk_size = (n + n_chunks - 1) // n_chunks  # ceil(248/16) = 16 i-values per chunk
    print(f"\nGenerating {n_chunks} Jacobi chunk files ({chunk_size} i-values each)...")

    for chunk_idx in range(n_chunks):
        i_start = chunk_idx * chunk_size
        i_end = min(i_start + chunk_size, n)
        if i_start >= n:
            break

        chunk_name = f"e8_sparse_jac_{chunk_idx:02d}"
        clines = []
        clines.append(f"/-")
        clines.append(f"E₈ Jacobi Verification — Chunk {chunk_idx:02d} (i = {i_start}..{i_end-1})")
        clines.append(f"-/")
        clines.append(f"")
        clines.append(f"import clifford.e8_sparse_defs")
        clines.append(f"")
        clines.append(f"set_option maxHeartbeats 16000000")
        clines.append(f"")
        clines.append(f"open E8Sparse")
        clines.append(f"")

        for i_val in range(i_start, i_end):
            clines.append(f"theorem e8_jacobi_{i_val:03d} : ∀ (j k l : Fin 248),")
            clines.append(f"    jacobiCheck ⟨{i_val}, by omega⟩ j k l = 0 := by")
            clines.append(f"  native_decide")
            clines.append(f"")

        chunk_path = os.path.join(out_dir, f'{chunk_name}.lean')
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(clines))
        print(f"  {chunk_name}.lean: i={i_start}..{i_end-1} ({i_end - i_start} theorems)")

    # ═══════════════════════════════════════════════════════
    # Generate antisymmetry file
    # ═══════════════════════════════════════════════════════
    print("\nGenerating antisymmetry verification...")
    alines = []
    alines.append("/-")
    alines.append("E₈ Antisymmetry — f(i,j,k) = -f(j,i,k)")
    alines.append("-/")
    alines.append("")
    alines.append("import clifford.e8_sparse_defs")
    alines.append("")
    alines.append("set_option maxHeartbeats 16000000")
    alines.append("")
    alines.append("open E8Sparse")
    alines.append("")

    # Antisymmetry: check that bkt(i,j) = -bkt(j,i) for all pairs
    # We encode this as: for all i j k, the lookup gives opposite signs
    alines.append("/-- Structure constant lookup for a specific (i,j,k) triple. -/")
    alines.append("def scLookup (i j k : Nat) : Int :=")
    alines.append("  (bkt i j).foldl (fun a (idx, c) => if idx == k then a + c else a) 0")
    alines.append("")
    alines.append("/-- E₈ bracket is antisymmetric. -/")
    alines.append("theorem e8_antisymm : ∀ (i j k : Fin 248),")
    alines.append("    scLookup i.val j.val k.val = -(scLookup j.val i.val k.val) := by")
    alines.append("  native_decide")
    alines.append("")

    antisymm_path = os.path.join(out_dir, 'e8_sparse_antisymm.lean')
    with open(antisymm_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(alines))
    print(f"  Written: {antisymm_path}")

    # ═══════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"  Definitions: e8_sparse_defs.lean ({len(lines)} lines)")
    print(f"  Jacobi: e8_sparse_jac_00..{n_chunks-1:02d} (248 theorems in {n_chunks} files)")
    print(f"  Antisymmetry: e8_sparse_antisymm.lean")
    print(f"")
    print(f"  Bracket data: {len(sc)} nonzero pairs, {total_terms} terms")
    print(f"  Total Jacobi evaluations: {n}^4 = {n**4:,}")
    print(f"")
    print(f"  Add to lakefile.lean roots:")
    roots = ["`clifford.e8_sparse_defs", "`clifford.e8_sparse_antisymm"]
    for i in range(n_chunks):
        roots.append(f"`clifford.e8_sparse_jac_{i:02d}")
    print(f"    {', '.join(roots)}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
