#!/usr/bin/env python3
"""
E8 Structure Constant Generator — Casselman-Kottwitz Algorithm
================================================================

Computes all structure constants of the E8 Lie algebra in the Chevalley basis
using the inductive algorithm from Casselman (2021), specialized for the
simply-laced case.

Key insight: signs of N_{alpha,beta} cannot be computed locally from a cocycle.
They must emerge from a GLOBAL construction where basis vectors and signs are
built simultaneously via Weyl group reflections.

Algorithm (simplified for simply-laced E8):
  1. Build root system with reflection tables
  2. For each positive root, find a descending chain of simple reflections to
     a simple root (every positive root is reachable this way)
  3. Compute structure constants inductively:
     - Base case: [E_{alpha_i}, E_beta] for simple alpha_i
     - Inductive step: use Weyl reflection to reduce to known cases
  4. Fill in [E-, E-] via Chevalley involution and [E+, E-] via Jacobi

The structure constants are integers (Chevalley basis), and for simply-laced E8,
|N_{alpha,beta}| = 1 whenever alpha+beta is a root.

Output: JSON file with all nonzero bracket pairs for Lean 4 code generation.

References:
  - Casselman, "A simple way to compute structure constants" (2021)
  - Humphreys, "Introduction to Lie Algebras", Ch 25
  - Carter, "Lie Algebras of Finite and Affine Type", Ch 4
"""

import json
import os
import sys
import time
from fractions import Fraction

from e8_roots import (
    construct_e8_roots,
    get_simple_roots,
    ip,
    build_cartan_matrix,
    roots_to_simple_coords,
    classify_positive_negative,
)


# ──────────────────────────────────────────────────────────────
# Phase 1: Root system infrastructure
# ──────────────────────────────────────────────────────────────

def build_reflection_tables(simple_roots, all_root_vecs, cartan_matrix):
    """
    Build reflection tables: s_{alpha_i}(lambda) for each simple root alpha_i
    and each root lambda.

    For simply-laced: s_i(lambda) = lambda - <lambda, alpha_i^v> alpha_i
    where <lambda, alpha_i^v> = 2(lambda, alpha_i)/(alpha_i, alpha_i) is integer.
    """
    n_rank = len(simple_roots)
    reflect = {}  # (i, root_vec) -> reflected_root_vec

    for i in range(n_rank):
        si = simple_roots[i + 1]
        si_norm_sq = ip(si, si)  # = 2 for E8

        for vec in all_root_vecs:
            # <lambda, alpha_i^v> = 2(lambda, alpha_i)/(alpha_i, alpha_i)
            pairing = ip(vec, si) * 2 / si_norm_sq
            pairing_int = int(pairing)
            assert pairing == pairing_int, f"Non-integer pairing: {pairing}"

            # s_i(lambda) = lambda - <lambda, alpha_i^v> * alpha_i
            reflected = tuple(v - pairing_int * s for v, s in zip(vec, si))
            assert reflected in all_root_vecs, \
                f"Reflection of {vec} by simple root {i+1} gave non-root {reflected}"
            reflect[(i, vec)] = reflected

    return reflect


def root_height(coords):
    """Height of a root = sum of simple root coordinates."""
    return sum(coords)


def find_descending_chains(pos_root_coords, pos_root_vecs, simple_roots,
                           cartan_matrix, reflect, all_root_vecs):
    """
    For each positive root lambda, find a chain of simple reflections that
    descends to a simple root:
      lambda -> s_{i_1}(lambda) -> s_{i_2}(...) -> ... -> alpha_j (simple)

    Each step DECREASES height. Returns dict: root_vec -> list of
    (simple_root_index, intermediate_root_vec) steps.
    """
    n_rank = len(simple_roots)
    simple_vecs = set()
    for i in range(1, n_rank + 1):
        simple_vecs.add(simple_roots[i])

    # Map vec -> coords for height computation
    vec_to_coords = {}
    for coords, vec in zip(pos_root_coords, pos_root_vecs):
        vec_to_coords[vec] = coords

    chains = {}

    for idx, vec in enumerate(pos_root_vecs):
        coords = pos_root_coords[idx]

        if vec in simple_vecs:
            # Already a simple root — no chain needed
            chains[vec] = []
            continue

        # Find chain by greedily reflecting to decrease height
        chain = []
        current_vec = vec
        current_coords = coords

        max_steps = 60  # E8 max height is 29, so 60 is generous
        for _ in range(max_steps):
            if current_vec in simple_vecs:
                break

            # Find a simple root alpha_i such that <current, alpha_i^v> > 0
            # Reflecting by such alpha_i decreases height
            found = False
            h = root_height(current_coords)
            for i in range(n_rank):
                si = simple_roots[i + 1]
                si_norm_sq = ip(si, si)
                pairing = int(ip(current_vec, si) * 2 / si_norm_sq)

                if pairing > 0:
                    reflected = reflect[(i, current_vec)]
                    if reflected in vec_to_coords:
                        new_coords = vec_to_coords[reflected]
                        new_h = root_height(new_coords)
                        if new_h < h:
                            chain.append((i, current_vec))
                            current_vec = reflected
                            current_coords = new_coords
                            found = True
                            break
                    else:
                        # Reflected to a negative root — skip
                        pass

            if not found:
                # Should never happen for positive roots
                raise RuntimeError(
                    f"Cannot descend from {vec} (coords={coords}), "
                    f"stuck at {current_vec} (coords={current_coords})")

        if current_vec not in simple_vecs:
            raise RuntimeError(
                f"Chain from {vec} didn't reach a simple root after {max_steps} steps")

        chains[vec] = chain

    return chains


# ──────────────────────────────────────────────────────────────
# Phase 2: Structure constant computation (inductive)
# ──────────────────────────────────────────────────────────────

def compute_N_simple(simple_idx, beta_vec, simple_roots, cartan_matrix,
                     all_root_vecs, reflect):
    """
    Compute N_{alpha_i, beta} where alpha_i is a simple root and beta is any root
    such that alpha_i + beta is also a root.

    For simply-laced: |N| = r + 1 where r = max{k >= 0 : beta - k*alpha_i is a root}.
    Sign from Tits convention on simple roots: N_{alpha_i, beta} = +(r+1)
    for the canonical basis choice where e_{alpha_i} are the Chevalley generators.

    Actually, for the CHEVALLEY basis with the standard normalization:
      N_{alpha_i, alpha_j} = ±1 when alpha_i + alpha_j is a root.
    The sign depends on the ordering convention.

    We use: N_{alpha_i, beta} = -(r+1) * sign
    where sign comes from the extraspecial pair convention.

    For simply-laced E8: r is always 0 (when alpha+beta is root and both positive)
    or 1 (possible in some configurations), so |N| = 1 or 2.
    """
    alpha_vec = simple_roots[simple_idx + 1]

    # Compute r = length of backward root string
    r = 0
    test = beta_vec
    while True:
        test = tuple(t - a for t, a in zip(test, alpha_vec))
        if test in all_root_vecs:
            r += 1
        else:
            break

    return r + 1  # magnitude; sign handled by the inductive framework


def compute_structure_constants_CK(simple_roots, cartan_matrix, positive_roots,
                                    negative_roots):
    """
    Compute all E8 structure constants using the Casselman-Kottwitz inductive method.

    Returns: (sc, pos_root_coords, neg_root_coords, pos_root_vecs, neg_root_vecs)
    """
    n_rank = len(simple_roots)

    # Order positive roots by height then lexicographically
    pos_root_coords = sorted(positive_roots.keys(), key=lambda c: (root_height(c), c))
    neg_root_coords = [tuple(-c for c in coords) for coords in pos_root_coords]

    pos_root_vecs = [positive_roots[c] for c in pos_root_coords]
    neg_root_vecs = [negative_roots[c] for c in neg_root_coords]

    # All root vectors (for reflection and membership checks)
    all_root_vecs = set(pos_root_vecs) | set(neg_root_vecs)

    # Lookups
    vec_to_basis_idx = {}
    for i, vec in enumerate(pos_root_vecs):
        vec_to_basis_idx[vec] = 8 + i
    for i, vec in enumerate(neg_root_vecs):
        vec_to_basis_idx[vec] = 128 + i

    pos_vec_to_idx = {vec: i for i, vec in enumerate(pos_root_vecs)}
    neg_vec_to_pos_idx = {}  # neg_vec -> index into pos list (of corresponding positive root)
    for i, vec in enumerate(neg_root_vecs):
        neg_vec_to_pos_idx[vec] = i

    vec_to_coords = {}
    for i in range(len(pos_root_coords)):
        vec_to_coords[pos_root_vecs[i]] = pos_root_coords[i]
        vec_to_coords[neg_root_vecs[i]] = neg_root_coords[i]

    # Simple root identification
    simple_vec_to_idx = {}
    for i in range(1, n_rank + 1):
        simple_vec_to_idx[simple_roots[i]] = i - 1  # 0-indexed

    # Build reflection tables
    print("  Building reflection tables...")
    reflect = build_reflection_tables(simple_roots, all_root_vecs, cartan_matrix)

    # Find descending chains for all positive roots
    print("  Finding descending chains...")
    chains = find_descending_chains(pos_root_coords, pos_root_vecs, simple_roots,
                                     cartan_matrix, reflect, all_root_vecs)

    # ── Compute [E+, E+] structure constants ──
    # N_table[(alpha_vec, beta_vec)] = N  where [E_alpha, E_beta] = N * E_{alpha+beta}
    # Only stored for alpha_vec, beta_vec both positive roots with alpha+beta a root.
    print("  Computing [E+, E+] structure constants (inductive)...")

    N_table = {}

    def add_vectors(a, b):
        return tuple(x + y for x, y in zip(a, b))

    def neg_vector(a):
        return tuple(-x for x in a)

    # Step 1: Compute N for all pairs where at least one root is simple.
    # For simple root alpha_i and positive root beta with alpha_i + beta a root:
    # We set N_{alpha_i, beta} = r + 1 (positive convention).
    # This is our FRAME — all other signs derive from this.
    for i in range(n_rank):
        alpha_vec = simple_roots[i + 1]
        for beta_vec in pos_root_vecs:
            if beta_vec == alpha_vec:
                continue
            sum_vec = add_vectors(alpha_vec, beta_vec)
            if sum_vec in all_root_vecs and sum_vec not in neg_vec_to_pos_idx:
                # alpha_i + beta is a positive root
                # Compute r = backward string length
                r = 0
                test = beta_vec
                while True:
                    prev = tuple(t - a for t, a in zip(test, alpha_vec))
                    if prev in all_root_vecs:
                        r += 1
                        test = prev
                    else:
                        break
                N_table[(alpha_vec, beta_vec)] = r + 1
                N_table[(beta_vec, alpha_vec)] = -(r + 1)  # antisymmetry

    print(f"    Simple root pairs: {sum(1 for k, v in N_table.items() if v > 0)} "
          f"(with antisymmetric partners)")

    # Step 2: Inductive extension using Weyl reflections.
    # If we know N_{lambda, mu} and s_i is a simple reflection:
    #   N_{s_i(lambda), s_i(mu)} = eta_i(lambda) * eta_i(mu) * eta_i(-nu) * N_{lambda, mu}
    # where nu = -(lambda + mu), and eta_i(gamma) = (-1)^{max(0, <gamma, alpha_i^v>)}
    #
    # For simply-laced: eta_i(gamma) = (-1)^{max(0, p)} where p = <gamma, alpha_i^v>.
    # This is the "Kottwitz sign factor."

    def kottwitz_sign(simple_i, root_vec):
        """(-1)^{max(0, <root, alpha_i^v>)} for simply-laced."""
        si = simple_roots[simple_i + 1]
        si_norm_sq = ip(si, si)
        p = int(ip(root_vec, si) * 2 / si_norm_sq)
        return (-1) ** max(0, p)

    # Process positive roots by increasing height.
    # For each pair (lambda, mu) with lambda+mu a positive root:
    #   If we don't know N_{lambda, mu}, find a simple reflection s_i that
    #   sends lambda to a "lower" root, compute N from the reflected pair.
    print("  Extending via Weyl reflections...")

    # Build pairs to compute: all (a, b) with a < b and a+b a positive root
    pairs_needed = []
    for idx_a in range(120):
        for idx_b in range(idx_a + 1, 120):
            sum_vec = add_vectors(pos_root_vecs[idx_a], pos_root_vecs[idx_b])
            if sum_vec in pos_vec_to_idx:
                pairs_needed.append((idx_a, idx_b))

    print(f"    Total [E+, E+] pairs needed: {len(pairs_needed)}")

    # Iteratively fill in N_table using reflections
    max_iters = 50
    for iteration in range(max_iters):
        missing = [(a, b) for a, b in pairs_needed
                    if (pos_root_vecs[a], pos_root_vecs[b]) not in N_table]

        if not missing:
            print(f"    All pairs filled after {iteration} iterations")
            break

        filled_this_iter = 0
        for idx_a, idx_b in missing:
            lambda_vec = pos_root_vecs[idx_a]
            mu_vec = pos_root_vecs[idx_b]
            sum_vec_lm = add_vectors(lambda_vec, mu_vec)  # lambda + mu

            # Try each simple reflection
            for i in range(n_rank):
                s_lambda = reflect[(i, lambda_vec)]
                s_mu = reflect[(i, mu_vec)]

                # Both reflected roots must be positive for the lookup to work
                if s_lambda not in pos_vec_to_idx or s_mu not in pos_vec_to_idx:
                    continue

                # Check if we know N for the reflected pair
                key = (s_lambda, s_mu)
                rev_key = (s_mu, s_lambda)
                if key in N_table:
                    N_reflected = N_table[key]
                elif rev_key in N_table:
                    N_reflected = -N_table[rev_key]
                else:
                    continue

                # Weyl group sign transfer (derived from first principles):
                #   N_{s(l), s(m)} = c(s,l) * c(s,m) * c(s,l+m) * N_{l,m}
                # where c(s_alpha, gamma) = (-1)^{max(0, <gamma, alpha^v>)}
                # Inverting (c values are ±1):
                #   N_{l,m} = c(s,l) * c(s,m) * c(s,l+m) * N_{s(l), s(m)}
                eta_lambda = kottwitz_sign(i, lambda_vec)
                eta_mu = kottwitz_sign(i, mu_vec)
                eta_sum = kottwitz_sign(i, sum_vec_lm)  # c(s, lambda+mu), NOT -(lambda+mu)

                sign_factor = eta_lambda * eta_mu * eta_sum
                N_val = sign_factor * N_reflected

                N_table[(lambda_vec, mu_vec)] = N_val
                N_table[(mu_vec, lambda_vec)] = -N_val
                filled_this_iter += 1
                break

        if filled_this_iter == 0 and missing:
            print(f"    WARNING: Stuck with {len(missing)} pairs unfilled at iteration {iteration}")
            # Try reflecting where one result is negative root
            # (need to handle the sign differently)
            break

        if iteration % 5 == 0 or filled_this_iter == 0:
            print(f"    Iteration {iteration}: filled {filled_this_iter}, "
                  f"remaining {len(missing) - filled_this_iter}")

    # Check completion
    final_missing = [(a, b) for a, b in pairs_needed
                     if (pos_root_vecs[a], pos_root_vecs[b]) not in N_table]
    if final_missing:
        print(f"  WARNING: {len(final_missing)} [E+, E+] pairs still missing!")
        print(f"  Attempting negative-root reflection strategy...")

        # Extended strategy: allow reflections where one root goes negative
        # If s_i(lambda) is negative = -gamma (gamma positive), then
        # [E_{-gamma}, E_{s_i(mu)}] is a [E-, E+] bracket.
        # We can use: [E_{-gamma}, E_{s_i(mu)}] = -N_{s_i(mu), -gamma} E_{...}
        # But this requires knowing [E+, E-] brackets, which we derive LATER.
        #
        # Alternative: use a different simple root for the reflection.
        # Every pair MUST be reachable by SOME sequence of reflections that
        # keeps both roots positive. This is guaranteed by the theory.
        #
        # Let's try harder: use MULTIPLE reflections (chains).
        for idx_a, idx_b in final_missing[:5]:
            lambda_vec = pos_root_vecs[idx_a]
            mu_vec = pos_root_vecs[idx_b]
            lc = vec_to_coords.get(lambda_vec, "?")
            mc = vec_to_coords.get(mu_vec, "?")
            print(f"    Missing: ({lc}) + ({mc})")

    # ── Build the full sc dictionary ──
    print("  Building full bracket table...")
    sc = {}

    # [H_i, H_j] = 0 (nothing to store)

    # [H_i, E_alpha] = <alpha, alpha_i^v> E_alpha
    for i in range(n_rank):
        si_vec = simple_roots[i + 1]
        si_norm_sq = ip(si_vec, si_vec)
        for j in range(120):
            alpha_vec = pos_root_vecs[j]
            coeff = int(ip(alpha_vec, si_vec) * 2 / si_norm_sq)
            if coeff != 0:
                sc[(i, 8 + j)] = [(8 + j, coeff)]
                sc[(i, 128 + j)] = [(128 + j, -coeff)]

    # [E_alpha, E_{-alpha}] = H_alpha = sum_i <alpha, alpha_i^v> H_i
    for j in range(120):
        alpha_vec = pos_root_vecs[j]
        terms = []
        for i in range(n_rank):
            si_vec = simple_roots[i + 1]
            si_norm_sq = ip(si_vec, si_vec)
            coeff = int(ip(alpha_vec, si_vec) * 2 / si_norm_sq)
            if coeff != 0:
                terms.append((i, coeff))
        if terms:
            sc[(8 + j, 128 + j)] = terms

    # [E_alpha, E_beta] for alpha, beta both positive, alpha+beta a root
    count_pp = 0
    for idx_a, idx_b in pairs_needed:
        key = (pos_root_vecs[idx_a], pos_root_vecs[idx_b])
        if key in N_table:
            N = N_table[key]
            sum_vec = add_vectors(pos_root_vecs[idx_a], pos_root_vecs[idx_b])
            target_idx = vec_to_basis_idx[sum_vec]
            sc[(8 + idx_a, 8 + idx_b)] = [(target_idx, N)]
            count_pp += 1

    print(f"    [E+, E+] nonzero: {count_pp} pairs")

    # [E_{-alpha}, E_{-beta}] = -N_{alpha,beta} E_{-(alpha+beta)}
    # (Chevalley involution: N_{-a,-b} = -N_{a,b})
    count_nn = 0
    for idx_a, idx_b in pairs_needed:
        key = (pos_root_vecs[idx_a], pos_root_vecs[idx_b])
        if key in N_table:
            N = N_table[key]
            sum_neg = add_vectors(neg_root_vecs[idx_a], neg_root_vecs[idx_b])
            target_idx = vec_to_basis_idx[sum_neg]
            sc[(128 + idx_a, 128 + idx_b)] = [(target_idx, -N)]
            count_nn += 1

    print(f"    [E-, E-] nonzero: {count_nn} pairs")

    # [E_alpha, E_{-beta}] for alpha != beta, alpha - beta a root
    # Derived from [E+, E+] via Jacobi identity on (E_alpha, E_{-beta}, E_beta):
    #   Case A (alpha-beta positive = gamma):
    #     N_{alpha,-beta} = -N_{beta,gamma}  (= N_{gamma,beta} by antisymmetry)
    #   Case B (beta-alpha positive = gamma):
    #     Jacobi on (E_{-alpha}, E_alpha, E_{-beta}) gives:
    #     N_{alpha,-beta} = N_{alpha,gamma}  where gamma = beta-alpha
    count_pm = 0
    for idx_a in range(120):
        for idx_b in range(120):
            if idx_a == idx_b:
                continue
            alpha_vec = pos_root_vecs[idx_a]
            neg_beta_vec = neg_root_vecs[idx_b]
            diff_vec = add_vectors(alpha_vec, neg_beta_vec)

            if diff_vec not in vec_to_basis_idx:
                continue

            target_idx = vec_to_basis_idx[diff_vec]

            # Derive N from [E+, E+] constants
            if diff_vec in pos_vec_to_idx:
                # Case A: gamma = alpha - beta is positive
                # N_{alpha,-beta} = N_{gamma, beta}  (Jacobi-derived)
                gamma_vec = diff_vec
                beta_vec = pos_root_vecs[idx_b]
                N_key = (gamma_vec, beta_vec)
                N_rev = (beta_vec, gamma_vec)
                if N_key in N_table:
                    N = N_table[N_key]
                elif N_rev in N_table:
                    N = -N_table[N_rev]
                else:
                    print(f"    WARNING: Missing N for Case A")
                    continue
            else:
                # Case B: gamma = beta - alpha is positive (diff_vec is negative)
                # N_{alpha,-beta} = N_{alpha, gamma}  (Jacobi-derived)
                gamma_vec = neg_vector(diff_vec)  # beta - alpha
                alpha_vec_lookup = pos_root_vecs[idx_a]
                N_key = (alpha_vec_lookup, gamma_vec)  # (alpha, gamma)
                N_rev = (gamma_vec, alpha_vec_lookup)   # (gamma, alpha)
                if N_key in N_table:
                    N = N_table[N_key]
                elif N_rev in N_table:
                    N = -N_table[N_rev]
                else:
                    print(f"    WARNING: Missing N for Case B")
                    continue

            sc[(8 + idx_a, 128 + idx_b)] = [(target_idx, N)]
            count_pm += 1

    print(f"    [E+, E-] nonzero: {count_pm} pairs")

    return sc, pos_root_coords, neg_root_coords, pos_root_vecs, neg_root_vecs


# ──────────────────────────────────────────────────────────────
# Phase 3: Verification
# ──────────────────────────────────────────────────────────────

def verify_jacobi(sc, n_basis=248, n_samples=None):
    """
    Verify Jacobi identity. If n_samples is None, check ALL triples.
    [B_i, [B_j, B_k]] + [B_j, [B_k, B_i]] + [B_k, [B_i, B_j]] = 0
    """
    def bracket(i, j):
        if i == j:
            return []
        if i < j:
            return sc.get((i, j), [])
        else:
            return [(k, -c) for k, c in sc.get((j, i), [])]

    def bracket_with_vector(i, vec):
        result = {}
        for k, c_k in vec:
            for m, c_m in bracket(i, k):
                result[m] = result.get(m, 0) + c_k * c_m
        return [(m, c) for m, c in result.items() if c != 0]

    failures = 0

    if n_samples is not None:
        import random
        random.seed(42)
        triples = [tuple(random.sample(range(n_basis), 3)) for _ in range(n_samples)]
        total = n_samples
    else:
        # All triples (i < j < k)
        triples = []
        for i in range(n_basis):
            for j in range(i + 1, n_basis):
                for k in range(j + 1, n_basis):
                    triples.append((i, j, k))
        total = len(triples)
        print(f"  Checking ALL {total:,} ordered triples...")

    check_interval = max(1, total // 20)
    for count, (i, j, k) in enumerate(triples):
        if n_samples is None and count % check_interval == 0 and count > 0:
            print(f"    Progress: {count:,}/{total:,} ({100*count//total}%)")

        bjk = bracket(j, k)
        term1 = bracket_with_vector(i, bjk)
        bki = bracket(k, i)
        term2 = bracket_with_vector(j, bki)
        bij = bracket(i, j)
        term3 = bracket_with_vector(k, bij)

        tot = {}
        for terms in [term1, term2, term3]:
            for m, c in terms:
                tot[m] = tot.get(m, 0) + c
        nonzero = {m: c for m, c in tot.items() if c != 0}

        if nonzero:
            failures += 1
            if failures <= 5:
                print(f"  JACOBI FAILURE #{failures}: ({i},{j},{k}) -> {nonzero}")

    return failures


# ──────────────────────────────────────────────────────────────
# Phase 4: Output
# ──────────────────────────────────────────────────────────────

def save_structure_constants(sc, pos_root_coords, neg_root_coords, output_dir):
    """Save structure constants to JSON."""
    data = {
        'rank': 8,
        'dimension': 248,
        'n_positive_roots': 120,
        'basis_ordering': [
            'H_1..H_8 (indices 0-7)',
            'E_{alpha_1}..E_{alpha_120} (indices 8-127)',
            'E_{-alpha_1}..E_{-alpha_120} (indices 128-247)',
        ],
        'positive_root_coords': [list(c) for c in pos_root_coords],
        'negative_root_coords': [list(c) for c in neg_root_coords],
        'structure_constants': {},
    }

    for (i, j), terms in sorted(sc.items()):
        key = f"{i},{j}"
        data['structure_constants'][key] = [[k, c] for k, c in terms]

    path = os.path.join(output_dir, 'e8_structure_constants.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1)

    print(f"  Saved to {path} ({os.path.getsize(path):,} bytes)")
    return path


def main():
    t0 = time.time()
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'research', 'e8-construction')
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("E8 Structure Constants — Casselman-Kottwitz Algorithm")
    print("=" * 60)

    print("\n[1/5] Constructing E8 root system...")
    roots = construct_e8_roots()
    simple = get_simple_roots()
    print(f"  {len(roots)} roots, {len(simple)} simple roots")

    print("\n[2/5] Classifying roots...")
    cartan = build_cartan_matrix(simple)
    root_coords = roots_to_simple_coords(roots, simple, cartan)
    positive, negative = classify_positive_negative(root_coords)
    print(f"  {len(positive)} positive, {len(negative)} negative")
    assert len(positive) == 120
    assert len(negative) == 120

    # Verify Cartan matrix
    expected_cartan = [
        [ 2, 0,-1, 0, 0, 0, 0, 0],
        [ 0, 2, 0,-1, 0, 0, 0, 0],
        [-1, 0, 2,-1, 0, 0, 0, 0],
        [ 0,-1,-1, 2,-1, 0, 0, 0],
        [ 0, 0, 0,-1, 2,-1, 0, 0],
        [ 0, 0, 0, 0,-1, 2,-1, 0],
        [ 0, 0, 0, 0, 0,-1, 2,-1],
        [ 0, 0, 0, 0, 0, 0,-1, 2],
    ]
    assert cartan == expected_cartan, "Cartan matrix mismatch!"
    print("  Cartan matrix: MATCHES expected E8")

    print("\n[3/5] Computing structure constants (Casselman-Kottwitz)...")
    sc, pos_coords, neg_coords, pos_vecs, neg_vecs = compute_structure_constants_CK(
        simple, cartan, positive, negative)
    print(f"  Total nonzero bracket pairs: {len(sc)}")

    t1 = time.time()
    print(f"  Computation time: {t1-t0:.1f}s")

    print("\n[4/5] Verifying Jacobi identity (1000 random triples first)...")
    failures = verify_jacobi(sc, n_samples=1000)
    if failures == 0:
        print("  Random Jacobi: PASSED (0/1000)")
        print("  Running FULL Jacobi verification (all 2.5M triples)...")
        failures = verify_jacobi(sc, n_samples=None)
        if failures == 0:
            print("  FULL Jacobi: PASSED (0 failures)")
        else:
            print(f"  FULL Jacobi: FAILED ({failures} failures)")
    else:
        print(f"  Random Jacobi: FAILED ({failures}/1000)")
        print("  Skipping full verification.")

    print("\n[5/5] Saving structure constants...")
    json_path = save_structure_constants(sc, pos_coords, neg_coords, output_dir)

    t2 = time.time()
    print(f"\nTotal time: {t2-t0:.1f}s")
    print(f"Output: {json_path}")

    if failures > 0:
        print("\nWARNING: Jacobi failures detected. Do NOT proceed to Lean generation.")
        return 1

    print("\nSUCCESS. Next step: python scripts/e8_lean_gen.py")
    return 0


if __name__ == '__main__':
    sys.exit(main())
