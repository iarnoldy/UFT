#!/usr/bin/env python3
"""
Generate a small Lean 4 test file with 5 E₈ bracket equations.
If this compiles with native_decide, the full generator will work.

Tests:
1. One [H, E] bracket (Cartan action on root vector)
2. One [E+, E+] bracket (positive root sum)
3. One [E+, E-] bracket (root-negative root → Cartan)
4. One [E-, E-] bracket (negative root sum)
5. One zero bracket (commuting elements)
"""

import json
import os
import sys


def main():
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'research', 'e8-construction', 'e8_structure_constants.json')
    with open(json_path) as f:
        data = json.load(f)

    sc = {}
    for key_str, terms in data['structure_constants'].items():
        i, j = map(int, key_str.split(','))
        sc[(i, j)] = [(k, c) for k, c in terms]

    n = 248

    def get_bracket(i, j):
        if i == j:
            return []
        if i < j:
            return sc.get((i, j), [])
        else:
            return [(_k, -_c) for _k, _c in sc.get((j, i), [])]

    # Build adjoint matrices (standard convention: M[k,j] = f^k_{ij})
    def build_ad(basis_idx):
        """Build 248x248 adjoint matrix for basis element basis_idx."""
        entries = {}  # (row, col) -> value
        for j in range(n):
            terms = get_bracket(basis_idx, j)
            for k, c in terms:
                entries[(k, j)] = c
        return entries

    # Select 5 test brackets
    test_cases = []

    # 1. [H, E] bracket: pick first nonzero [H_i, E_j]
    for (i, j), terms in sorted(sc.items()):
        if i < 8 and 8 <= j < 128:
            test_cases.append((i, j, terms, "[H,E+]"))
            break

    # 2. [E+, E+] bracket
    for (i, j), terms in sorted(sc.items()):
        if 8 <= i < 128 and 8 <= j < 128:
            test_cases.append((i, j, terms, "[E+,E+]"))
            break

    # 3. [E+, E-] bracket (gives Cartan)
    for (i, j), terms in sorted(sc.items()):
        if 8 <= i < 128 and j >= 128 and any(k < 8 for k, c in terms):
            test_cases.append((i, j, terms, "[E+,E-]->H"))
            break

    # 4. [E-, E-] bracket
    for (i, j), terms in sorted(sc.items()):
        if i >= 128 and j >= 128:
            test_cases.append((i, j, terms, "[E-,E-]"))
            break

    # 5. Zero bracket: find a pair with no entry
    for i in range(8):
        for j in range(8, 128):
            if (i, j) not in sc:
                test_cases.append((i, j, [], "zero"))
                break
        if len(test_cases) == 5:
            break

    print(f"Selected {len(test_cases)} test brackets:")
    for i, j, terms, label in test_cases:
        print(f"  [{i},{j}] = {terms}  ({label})")

    # Build adjoint matrices for all indices appearing in test cases
    needed_indices = set()
    for i, j, terms, _ in test_cases:
        needed_indices.add(i)
        needed_indices.add(j)
        for k, c in terms:
            needed_indices.add(k)

    print(f"\nNeed adjoint matrices for {len(needed_indices)} basis elements")

    ads = {}
    for idx in needed_indices:
        ads[idx] = build_ad(idx)

    # Generate Lean code
    lean_lines = []
    lean_lines.append("/-")
    lean_lines.append("E₈ Bracket Test — 5 equations via native_decide")
    lean_lines.append("================================================")
    lean_lines.append("")
    lean_lines.append("Quick compilation test before generating full 31-file E₈.")
    lean_lines.append("Each matrix is 248×248 over ℤ, entries from Chevalley basis.")
    lean_lines.append("Convention: ad(B_i)_{k,j} = f^k_{ij} where [B_i, B_j] = Σ_k f^k_{ij} B_k")
    lean_lines.append("-/")
    lean_lines.append("")
    lean_lines.append("import Mathlib.Data.Real.Basic")
    lean_lines.append("import Mathlib.Tactic")
    lean_lines.append("")
    lean_lines.append("set_option maxHeartbeats 800000")
    lean_lines.append("")
    lean_lines.append("abbrev E8Mat := Matrix (Fin 248) (Fin 248) ℤ")
    lean_lines.append("")

    # Generate matrix definitions
    for idx in sorted(needed_indices):
        entries = ads[idx]
        lean_lines.append(f"/-- Adjoint matrix for basis element B_{idx}. -/")
        lean_lines.append(f"def ad{idx} : E8Mat := Matrix.of fun i j => match i.val, j.val with")
        for (row, col), val in sorted(entries.items()):
            lean_lines.append(f"    | {row}, {col} => {val}")
        lean_lines.append(f"    | _, _ => 0")
        lean_lines.append("")

    # Generate bracket test theorems
    for test_num, (i, j, terms, label) in enumerate(test_cases):
        lean_lines.append(f"/-- Bracket test {test_num + 1}: [{i},{j}] ({label}). -/")

        if not terms:
            # Zero bracket
            lean_lines.append(f"theorem e8_test_{test_num + 1} :")
            lean_lines.append(f"    ad{i} * ad{j} - ad{j} * ad{i} = (0 : E8Mat) := by")
        elif len(terms) == 1:
            k, c = terms[0]
            if c == 1:
                rhs = f"ad{k}"
            elif c == -1:
                rhs = f"-(ad{k})"
            else:
                rhs = f"({c} : ℤ) • ad{k}"
            lean_lines.append(f"theorem e8_test_{test_num + 1} :")
            lean_lines.append(f"    ad{i} * ad{j} - ad{j} * ad{i} = {rhs} := by")
        else:
            # Multiple terms: build as sum
            parts = []
            for k, c in terms:
                if c == 1:
                    parts.append(f"ad{k}")
                elif c == -1:
                    parts.append(f"-(ad{k})")
                else:
                    parts.append(f"({c} : ℤ) • ad{k}")
            rhs = " + ".join(parts)
            lean_lines.append(f"theorem e8_test_{test_num + 1} :")
            lean_lines.append(f"    ad{i} * ad{j} - ad{j} * ad{i} = {rhs} := by")

        lean_lines.append(f"  native_decide")
        lean_lines.append("")

    # Write file
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            'src', 'lean_proofs', 'clifford', 'e8_bracket_test.lean')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lean_lines))

    print(f"\nGenerated: {out_path}")
    print(f"  {len(lean_lines)} lines")
    print(f"  {len(needed_indices)} matrix definitions")
    print(f"  {len(test_cases)} bracket theorems")
    print(f"\nNext: lake env lean {out_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
