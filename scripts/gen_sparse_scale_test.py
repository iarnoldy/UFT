#!/usr/bin/env python3
"""
Generate a sparse Jacobi scale test for Fin 100 with ~200 bracket entries.
Simulates E₈-like density: 200 nonzero pairs out of C(100,2) = 4950 total pairs.
Uses so(3) subalgebras + cross-terms to create a valid Lie algebra.

Strategy: Build so(10) embedded in a 100-dim space. so(10) has 45 generators
and C(45,2) = 990 nonzero bracket pairs — closer to E₈'s density.
"""

import itertools

def main():
    # so(10): generators L_{ij} for 1 <= i < j <= 10
    # 45 generators, indexed 0..44
    N_SO = 10
    DIM = 100  # embed in 100-dim space (55 generators are zero)
    pairs = [(i, j) for i in range(1, N_SO+1) for j in range(i+1, N_SO+1)]
    assert len(pairs) == 45
    pair_to_idx = {p: k for k, p in enumerate(pairs)}

    def canonical(p, q):
        if p == q: return None, 0
        if p < q: return (p, q), 1
        return (q, p), -1

    # Compute all nonzero brackets
    brackets = {}  # (idx_a, idx_b) -> [(idx_c, coeff)]
    for idx_a, (i, j) in enumerate(pairs):
        for idx_b, (k, l) in enumerate(pairs):
            if idx_a >= idx_b:
                continue
            # [L_{ij}, L_{kl}] = d_{jk}L_{il} - d_{ik}L_{jl} - d_{jl}L_{ik} + d_{il}L_{jk}
            terms = []
            if j == k:
                c, s = canonical(i, l)
                if c: terms.append((pair_to_idx[c], s))
            if i == k:
                c, s = canonical(j, l)
                if c: terms.append((pair_to_idx[c], -s))
            if j == l:
                c, s = canonical(i, k)
                if c: terms.append((pair_to_idx[c], -s))
            if i == l:
                c, s = canonical(j, k)
                if c: terms.append((pair_to_idx[c], s))

            # Combine terms with same index
            combined = {}
            for idx, coeff in terms:
                combined[idx] = combined.get(idx, 0) + coeff
            terms = [(idx, c) for idx, c in combined.items() if c != 0]

            if terms:
                brackets[(idx_a, idx_b)] = terms

    print(f"so({N_SO}) in {DIM}-dim space: {len(brackets)} nonzero bracket pairs")

    # Generate Lean code
    lines = []
    lines.append("/-")
    lines.append(f"Sparse Jacobi scale test: so({N_SO}) in Fin {DIM}.")
    lines.append(f"{len(brackets)} nonzero bracket pairs (E₈ has 7,752).")
    lines.append(f"Fin({DIM})^4 = {DIM**4:,} evaluations.")
    lines.append("-/")
    lines.append("")
    lines.append("import Mathlib.Tactic")
    lines.append("")
    lines.append("set_option maxHeartbeats 8000000")
    lines.append("")

    # Generate bracket data
    lines.append(f"private def scale_brackets : List (Nat × Nat × List (Nat × Int)) :=")
    bracket_strs = []
    for (a, b), terms in sorted(brackets.items()):
        term_str = ", ".join(f"({idx}, {coeff})" for idx, coeff in terms)
        bracket_strs.append(f"  ({a}, {b}, [{term_str}])")
    lines.append("  [" + ",\n   ".join(bracket_strs) + "]")
    lines.append("")

    # Build table
    n = DIM
    lines.append(f"private def scale_table : Array (List (Nat × Int)) :=")
    lines.append(f"  let base := (List.replicate {n*n} ([] : List (Nat × Int))).toArray")
    lines.append(f"  let t := scale_brackets.foldl (fun acc (i, j, terms) =>")
    lines.append(f"    acc.set! (i * {n} + j) terms) base")
    lines.append(f"  scale_brackets.foldl (fun acc (i, j, terms) =>")
    lines.append(f"    acc.set! (j * {n} + i) (terms.map fun (k, c) => (k, -c))) t")
    lines.append("")

    lines.append(f"private def s_bkt (i j : Nat) : List (Nat × Int) :=")
    lines.append(f"  scale_table.getD (i * {n} + j) []")
    lines.append("")

    lines.append(f"private def s_jterm (bkt : List (Nat × Int)) (k l : Nat) : Int :=")
    lines.append(f"  bkt.foldl (fun acc (m, c_m) =>")
    lines.append(f"    let f_mkl := (s_bkt m k).foldl")
    lines.append(f"      (fun a (idx, c) => if idx == l then a + c else a) 0")
    lines.append(f"    acc + c_m * f_mkl) 0")
    lines.append("")

    lines.append(f"def s_jacobi (i j k l : Fin {n}) : Int :=")
    lines.append(f"  s_jterm (s_bkt i.val j.val) k.val l.val +")
    lines.append(f"  s_jterm (s_bkt j.val k.val) i.val l.val +")
    lines.append(f"  s_jterm (s_bkt k.val i.val) j.val l.val")
    lines.append("")

    lines.append(f"/-- Sparse Jacobi for so({N_SO}) in Fin {n}. {DIM**4:,} evaluations. -/")
    lines.append(f"theorem scale_sparse_jacobi : ∀ (i j k l : Fin {n}),")
    lines.append(f"    s_jacobi i j k l = 0 := by")
    lines.append(f"  native_decide")
    lines.append("")

    out_path = "src/lean_proofs/clifford/e8_sparse_scale100.lean"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Written: {out_path} ({len(lines)} lines, {len(brackets)} brackets)")
    print(f"Evaluations: {DIM**4:,}")
    print(f"Run: time lake env lean {out_path}")

if __name__ == '__main__':
    main()
