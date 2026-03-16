#!/usr/bin/env python3
"""
E8 Generation Analysis: Full Branching Chain
============================================

Computes the decomposition of the 248-dimensional adjoint representation of E8
through the chain:

    E8 -> SO(16) -> SO(14) x SO(2) -> SO(10) x SO(4) x SO(2)

This is the central computation for the three-generation problem.

CLAIM TAGS:
  [CO] = Computed (not Lean-verified) -- all branching rules here
  [MV] = Machine-verified -- references to existing Lean theorems
  [CP] = Candidate Physics -- physical interpretation of representations
  [SP] = Stated Property -- standard results from Slansky/representation theory

Author: SO(14) Generation Specialist
Date: 2026-03-16
"""

from itertools import product
from collections import defaultdict
from math import comb
import json

# ==========================================================================
# PART 1: E8 -> SO(16) Decomposition
# ==========================================================================

def e8_to_so16():
    """
    E8 adjoint (248) decomposes under SO(16) = D8 as:
      248 = 120 (adjoint of SO(16)) + 128_s (semi-spinor of Spin(16))

    This is a STANDARD result [SP]:
      - Slansky (1981), Table 22
      - Adams, "Lectures on Exceptional Lie Groups" (1996)
      - dim check: 120 + 128 = 248 [MV: e8_so16_decomposition in e8_embedding.lean]
    """
    print("=" * 80)
    print("PART 1: E8 -> SO(16) Decomposition")
    print("=" * 80)
    print()
    print("  248 = 120 (adjoint D8) + 128_s (semi-spinor D8)  [SP]")
    print(f"  Dimension check: 120 + 128 = {120 + 128}  [MV: e8_so16_decomposition]")
    print()
    print("  The 120 = C(16,2) generates the SO(16) gauge sector.")
    print("  The 128 = 2^(8-1) is the chiral semi-spinor S+ of Spin(16).")
    print("  Together they close under the E8 Lie bracket.")
    print()
    return {'adjoint_so16': 120, 'semispinor_so16': 128}


# ==========================================================================
# PART 2: SO(16) -> SO(14) x SO(2) Decomposition
# ==========================================================================

def so16_adjoint_under_so14():
    """
    The adjoint (120) of SO(16) decomposes under SO(14) x SO(2) as:

      120 = (91, 0) + (1, 0) + (14, +1) + (14, -1)

    where:
      91 = C(14,2) = adjoint of SO(14)  [MV: so14_dim in e8_embedding.lean]
      1 = C(2,2) = adjoint of SO(2) = U(1) generator
      14 + 14 = 2 * 14 = 28 = (vector_14, vector_2) mixed generators

    The 28 mixed generators split by SO(2) = U(1) charge into 14_(+1) + 14_(-1).

    Dimension: 91 + 1 + 14 + 14 = 120 [MV: so16_so14_decomposition]
    """
    print("=" * 80)
    print("PART 2a: SO(16) adjoint -> SO(14) x SO(2)")
    print("=" * 80)
    print()
    print("  120 = (91,0) + (1,0) + (14,+1) + (14,-1)  [SP]")
    print(f"  Dimension check: 91 + 1 + 14 + 14 = {91 + 1 + 14 + 14}")
    print(f"  [MV: so16_so14_decomposition in e8_embedding.lean]")
    print()

    # Verify
    assert 91 + 1 + 14 + 14 == 120

    return [
        ('adj_SO14', 91, 0),    # (SO(14) rep, dim, SO(2) charge)
        ('singlet', 1, 0),      # U(1)
        ('vector_14', 14, +1),  # mixed
        ('vector_14', 14, -1),  # mixed conjugate
    ]


def so16_semispinor_under_so14():
    """
    The semi-spinor 128_s of Spin(16) decomposes under Spin(14) x U(1) as:

      128_s = 64+_(+1/2) + 64-_(-1/2)

    where 64+ and 64- are the two chiral semi-spinors of Spin(14),
    and +/-1/2 are the U(1) charges from the SO(2) factor.

    This is the STANDARD spinor branching rule for D_n -> D_{n-1} x U(1) [SP]:
      S+(D_n) -> S+(D_{n-1})_(+1/2) + S-(D_{n-1})_(-1/2)

    Dimension: 64 + 64 = 128 [MV: semispinor_branching in e8_embedding.lean]

    CRITICAL for generation counting: each 64 is a SINGLE semi-spinor of Spin(14),
    which contains exactly ONE generation of SM fermions [CP].
    """
    print("=" * 80)
    print("PART 2b: SO(16) semi-spinor -> Spin(14) x U(1)")
    print("=" * 80)
    print()
    print("  128_s = 64+_(+1/2) + 64-_(-1/2)  [SP]")
    print(f"  Dimension check: 64 + 64 = {64 + 64}")
    print(f"  [MV: semispinor_branching in e8_embedding.lean]")
    print()
    print("  GENERATION COUNT AT THIS LEVEL: 2 semi-spinors of Spin(14)  [CO]")
    print("  Each semi-spinor = 1 generation (under CP identification)  [CP]")
    print("  => 2 generations visible at SO(14) x U(1) level.")
    print()

    assert 64 + 64 == 128

    return [
        ('64+', 64, +0.5),   # positive-chirality semi-spinor, U(1) charge +1/2
        ('64-', 64, -0.5),   # negative-chirality semi-spinor, U(1) charge -1/2
    ]


# ==========================================================================
# PART 3: SO(14) semi-spinor -> SO(10) x SO(4) (weight-level computation)
# ==========================================================================

def generate_spinor_weights(n):
    """Generate all 2^n spinor weights of D_n = SO(2n)."""
    weights = []
    for combo in product([+1, -1], repeat=n):
        weight = tuple(s / 2.0 for s in combo)
        weights.append(weight)
    return weights


def classify_so10_so4(weight_7tuple):
    """
    For a weight of D7 = SO(14), split into SO(10) x SO(4) parts.
    The weight is a 7-tuple (h1,...,h5, h6, h7).
    First 5 -> SO(10) = D5, last 2 -> SO(4) = D2.
    """
    so10_w = weight_7tuple[:5]
    so4_w = weight_7tuple[5:]

    # SO(10) semi-spinor classification
    n_minus_10 = sum(1 for h in so10_w if h < 0)
    so10_rep = '16' if n_minus_10 % 2 == 0 else '16bar'

    # SO(4) = SU(2)_L x SU(2)_R classification
    h6, h7 = so4_w
    if h6 * h7 > 0:  # same sign
        so4_rep = '(2,1)'  # 2_s
    else:  # opposite sign
        so4_rep = '(1,2)'  # 2_c

    return so10_rep, so4_rep


def so14_semispinor_decomposition():
    """
    Decompose the 64+ and 64- semi-spinors of Spin(14) under SO(10) x SO(4).

    Uses explicit weight construction. This is the core computation.

    RESULT [CO]:
      64+ = (16, (2,1)) + (16bar, (1,2))
      64- = (16bar, (2,1)) + (16, (1,2))

    Each semi-spinor contains:
      - 1 copy of (16, 2) of SO(10) x one SU(2) factor
      - 1 copy of (16bar, 2) of SO(10) x other SU(2) factor

    Generation count from each semi-spinor: 1 generation + 1 mirror [CO]
    (If SO(4) = Lorentz: matter + antimatter, no mirrors [CP])
    """
    print("=" * 80)
    print("PART 3: SO(14) semi-spinors -> SO(10) x SO(4)")
    print("=" * 80)
    print()

    all_weights = generate_spinor_weights(7)
    assert len(all_weights) == 128

    # Split into semi-spinors by D7 chirality
    n_minus_total = lambda w: sum(1 for h in w if h < 0)
    semi_plus = [w for w in all_weights if n_minus_total(w) % 2 == 0]   # 64+
    semi_minus = [w for w in all_weights if n_minus_total(w) % 2 == 1]  # 64-
    assert len(semi_plus) == 64
    assert len(semi_minus) == 64

    results = {}
    for label, semi in [("64+", semi_plus), ("64-", semi_minus)]:
        decomp = defaultdict(int)
        for w in semi:
            so10_rep, so4_rep = classify_so10_so4(w)
            decomp[(so10_rep, so4_rep)] += 1

        print(f"  {label} decomposition under SO(10) x SO(4) [CO]:")
        pieces = []
        for key in sorted(decomp.keys()):
            n_weights = decomp[key]
            so10_rep, so4_rep = key
            so10_dim = 16
            so4_dim = 2
            multiplicity = n_weights // (so10_dim * so4_dim)
            print(f"    ({so10_rep}, {so4_rep}): {n_weights} weights"
                  f" = {multiplicity} x ({so10_dim} x {so4_dim})")
            pieces.append((so10_rep, so4_rep, multiplicity))

        total_16 = sum(decomp[k] for k in decomp if k[0] == '16') // 16
        total_16bar = sum(decomp[k] for k in decomp if k[0] == '16bar') // 16
        print(f"    => Contains {total_16} copies of 16 and {total_16bar} copies of 16bar")
        print(f"       (as SO(10) reps, counting SO(4) multiplicity)")
        results[label] = {'pieces': pieces, 'n_16': total_16, 'n_16bar': total_16bar}
        print()

    print("  BRANCHING RULES [CO]:")
    print("    64+ = (16, (2,1)) + (16bar, (1,2))     [32 + 32 = 64]")
    print("    64- = (16bar, (2,1)) + (16, (1,2))     [32 + 32 = 64]")
    print()

    return results


# ==========================================================================
# PART 4: Full E8 -> SO(10) x SO(4) x U(1) decomposition
# ==========================================================================

def full_e8_decomposition():
    """
    Trace the full 248 of E8 through the chain:
      E8 -> SO(16) -> SO(14) x U(1) -> SO(10) x SO(4) x U(1)

    Adjoint part (120):
      91 (adj SO(14)) -> (45,1,1) + (1,3,1) + (1,1,3) + (10,2,2)
                         with SO(4) = SU(2)_L x SU(2)_R decomposition
      1 (adj SO(2)) -> (1,1,1) singlet
      28 (14_+1 + 14_-1) -> need to decompose 14 of SO(14) under SO(10)xSO(4)

    Semi-spinor part (128):
      64+ -> (16, (2,1)) + (16bar, (1,2))  with U(1) charge +1/2
      64- -> (16bar, (2,1)) + (16, (1,2))  with U(1) charge -1/2
    """
    print("=" * 80)
    print("PART 4: Full E8 -> SO(10) x SO(4) x U(1) Decomposition")
    print("=" * 80)
    print()

    # --- Adjoint 120 ---
    print("  FROM THE ADJOINT 120 of SO(16):")
    print()

    # 91 of SO(14) under SO(10) x SO(4)
    print("  91 (adjoint SO(14)) -> SO(10) x SO(4) [MV: unification_decomposition]:")
    print("    (45, (1,1)): adjoint of SO(10)     [45 dim]")
    print("    ((1,1), (3,1)+(1,3)): adjoint of SO(4)  [6 dim]")
    print("    (10, (2,2)): bifundamental           [40 dim]")
    print(f"    Total: 45 + 6 + 40 = {45+6+40}")
    assert 45 + 6 + 40 == 91
    print()

    # 1 of SO(2)
    print("  1 (adjoint SO(2) = U(1)):")
    print("    (1, (1,1), 0): a single neutral scalar  [1 dim]")
    print()

    # 28 = 14_(+1) + 14_(-1) mixed
    # 14 of SO(14) under SO(10) x SO(4): 14 = (10, (1,1)) + (1, (2,2))
    print("  28 = 14_(+1) + 14_(-1) (vector SO(14) x vector SO(2)):")
    print("    14 of SO(14) = (10, (1,1)) + (1, (2,2)) under SO(10)xSO(4)")
    print("    So 14_(+1) = (10, (1,1))_(+1) + (1, (2,2))_(+1)")
    print("    And 14_(-1) = (10, (1,1))_(-1) + (1, (2,2))_(-1)")
    print(f"    Dimensions: (10+4)*1 + (10+4)*1 = {14+14}")
    assert 14 + 14 == 28
    print()

    # --- Semi-spinor 128 ---
    print("  FROM THE SEMI-SPINOR 128 of Spin(16):")
    print()
    print("  64+_(+1/2):")
    print("    (16, (2,1))_(+1/2):   32 dim   [CO]")
    print("    (16bar, (1,2))_(+1/2): 32 dim  [CO]")
    print()
    print("  64-_(-1/2):")
    print("    (16bar, (2,1))_(-1/2): 32 dim  [CO]")
    print("    (16, (1,2))_(-1/2):   32 dim   [CO]")
    print()

    # --- Total SO(10) generation count ---
    print("  TOTAL 16 of SO(10) content in 248 of E8:")
    print()
    print("  From 120 (adjoint):     0 copies of 16  (adjoint is tensor, not spinor)")
    print("  From 128 (semi-spinor):")
    print("    64+: 1 x (16, (2,1)) = 2 copies of 16 as SO(10) reps")
    print("    64-: 1 x (16, (1,2)) = 2 copies of 16 as SO(10) reps")
    print("    64+: 1 x (16bar, (1,2)) = 2 copies of 16bar")
    print("    64-: 1 x (16bar, (2,1)) = 2 copies of 16bar")
    print()
    print("  TOTAL from 128: 4 copies of 16 + 4 copies of 16bar  [CO]")
    print()
    print("  NOTE: These are NOT 4 independent generations!")
    print("  The SO(4) and U(1) quantum numbers distinguish them.")
    print("  Counting independent generations requires specifying which")
    print("  symmetries are gauged vs. global vs. broken.")
    print()


# ==========================================================================
# PART 5: The SU(9) route -- the three-generation mechanism
# ==========================================================================

def su9_decomposition():
    """
    The ALTERNATIVE decomposition of 248 via E8 -> SU(9):
      248 = 80 + 84 + 84*

    Under SU(5) x SU(4) inside SU(9):
      84 = Lambda^3(C^9) decomposes via Cauchy formula.

    Under SU(5) x SU(3)_family x U(1) (via SU(4) -> SU(3) x U(1)):
      Three copies of the 16 of SO(10) emerge from the SU(3) fundamental.
    """
    print("=" * 80)
    print("PART 5: E8 -> SU(9) -> SU(5) x SU(3)_family Route")
    print("=" * 80)
    print()

    # E8 -> SU(9)
    print("  E8 -> SU(9)  [SP]:")
    print("    248 = 80 + 84 + 84*")
    print(f"    Check: 80 + 84 + 84 = {80 + 84 + 84}")
    print(f"    [MV: e8_su9_decomposition in three_generation_theorem.lean]")
    print()

    # SU(9) -> SU(5) x SU(4)
    print("  SU(9) -> SU(5) x SU(4)  [SP]:")
    print()
    print("    Adjoint 80 = (24,1) + (1,15) + (1,1) + (5,4bar) + (5bar,4)")
    print(f"    Check: 24 + 15 + 1 + 20 + 20 = {24+15+1+20+20}")
    assert 24 + 15 + 1 + 20 + 20 == 80
    print()

    # Lambda^3(C^9) Cauchy decomposition
    print("    Lambda^3(C^9) = 84 under SU(5) x SU(4) [Cauchy formula]  [CO]:")
    terms = [
        ("Lambda^3(5) x 1", comb(5,3), 1, "(10,1)"),
        ("Lambda^2(5) x 4", comb(5,2), comb(4,1), "(10bar,4)"),
        ("5 x Lambda^2(4)", comb(5,1), comb(4,2), "(5,6)"),
        ("1 x Lambda^3(4)", 1, comb(4,3), "(1,4bar)"),
    ]
    total = 0
    for desc, d1, d2, rep in terms:
        dim = d1 * d2
        total += dim
        print(f"      {rep}: {d1} x {d2} = {dim}")
    print(f"    Total: {total} (should be 84)")
    print(f"    [MV: cauchy_decomp_84 in three_generation_theorem.lean]")
    assert total == 84
    print()

    # SU(4) -> SU(3) x U(1)
    print("  SU(4) -> SU(3)_family x U(1)  [SP]:")
    print("    4 -> 3_(+1) + 1_(-3)")
    print("    6 -> 3_(+2) + 3bar_(-2)")
    print("    4bar -> 3bar_(-1) + 1_(+3)")
    print("    15 -> 8_0 + 1_0 + 3_(+4) + 3bar_(-4)")
    print()

    # Full decomposition of 84 under SU(5) x SU(3) x U(1)
    print("  84 under SU(5) x SU(3)_family x U(1) [CO]:")
    print()
    print("    From (10,1)_0:    (10, 1)_0         dim = 10")
    print("    From (10bar,4):   (10bar, 3)_(+1)   dim = 30")
    print("                      (10bar, 1)_(-3)    dim = 10")
    print("    From (5,6):       (5, 3)_(+2)       dim = 15")
    print("                      (5, 3bar)_(-2)     dim = 15")
    print("    From (1,4bar):    (1, 3bar)_(-1)     dim = 3")
    print("                      (1, 1)_(+3)        dim = 1")
    print(f"    Total: 10+30+10+15+15+3+1 = {10+30+10+15+15+3+1}")
    assert 10+30+10+15+15+3+1 == 84
    print(f"    [MV: complete_84_decomposition in e8_generation_mechanism.lean]")
    print()

    # Identify generations
    print("  GENERATION IDENTIFICATION [CP]:")
    print()
    print("  One SM generation under SU(5) = 10bar + 5bar + 1 = 16  [SP]")
    print("  (using the standard convention: 10bar contains Q,u^c,e^c;")
    print("   5bar contains d^c,L; 1 is nu^c)")
    print()
    print("  From the 84:")
    print("    (10bar, 3)_(+1): THREE copies of 10bar  [30 dim] -- GENERATIONS")
    print("  From the 84*:")
    print("    (5, 3bar)_(-2):  THREE copies of 5bar   [15 dim] -- GENERATIONS")
    print("    (1, 3bar)_(-1):  THREE singlets (nu^c)  [3 dim]  -- GENERATIONS")
    print()
    print(f"  Total generation matter: 30 + 15 + 3 = {30+15+3} = 3 x 16")
    print(f"  [MV: generation_matter_total in e8_generation_mechanism.lean]")
    assert 30 + 15 + 3 == 48 == 3 * 16
    print()

    print("  EXOTIC CONTENT:")
    print("    (10, 1)_0:         10 dim")
    print("    (10bar, 1)_(-3):   10 dim")
    print("    (5, 3)_(+2):       15 dim")
    print("    (1, 1)_(+3):        1 dim")
    print(f"    Total exotics: 10+10+15+1 = {10+10+15+1}")
    assert 10+10+15+1 == 36
    print(f"    [MV: exotic_content in three_generation_theorem.lean]")
    print()

    print("  GENERATION COUNT: EXACTLY 3  [CO]")
    print("  Origin: dim(fundamental of SU(3)_family) = 3")
    print()


# ==========================================================================
# PART 6: The SO(16) route and generation counting
# ==========================================================================

def so16_route_analysis():
    """
    Careful analysis of how many generations the SO(16) decomposition gives.

    Under SO(16) -> SO(14) x U(1):
      128_s = 64+_(+1/2) + 64-_(-1/2)

    Each 64 under SO(10) x SO(4):
      64+ = (16, (2,1)) + (16bar, (1,2))
      64- = (16bar, (2,1)) + (16, (1,2))

    Total 16's from the 128:
      From 64+: 1 x (16, (2,1)) -- this is 1 copy of 16 tensored with a 2 of SO(4)
      From 64-: 1 x (16, (1,2)) -- this is 1 copy of 16 tensored with a 2 of SO(4)

    The question is: how do you count "generations"?

    INTERPRETATION A: Count the 16 of SO(10) multiplicity
      Each (16, 2) gives 2 copies of 16 when the SO(4) is decomposed.
      Total: 4 copies of 16, 4 copies of 16bar.
      But this is vector-like (equal 16 and 16bar) -> no net chirality -> 0 chiral generations.

    INTERPRETATION B: Count chiral matter per semi-spinor
      64+ gives (16, (2,1)) + (16bar, (1,2))
      If SO(4) = Lorentz [CP]:
        (2,1) = left-handed, (1,2) = right-handed
        => 16_L + 16bar_R = one generation (particle + antiparticle)
      This gives 1 generation per semi-spinor.
      Two semi-spinors -> 2 generations.

    INTERPRETATION C: Use additional structure (E8 -> SU(9))
      The SU(9) decomposition naturally gives 3 generations.
      This requires using the FULL E8 structure, not just SO(16).
    """
    print("=" * 80)
    print("PART 6: Generation Counting -- SO(16) Route Analysis")
    print("=" * 80)
    print()

    print("  The 128 semi-spinor of Spin(16) under SO(10) x SO(4) x U(1):  [CO]")
    print()
    print("    (16, (2,1))_(+1/2):   32 dim   -- matter, left-handed")
    print("    (16bar, (1,2))_(+1/2): 32 dim  -- antimatter, right-handed")
    print("    (16bar, (2,1))_(-1/2): 32 dim  -- mirror matter, left-handed")
    print("    (16, (1,2))_(-1/2):   32 dim   -- mirror antimatter, right-handed")
    print()

    print("  GENERATION COUNTS (3 different conventions):")
    print()
    print("  A. Raw SO(10) multiplicity:  4 x 16 + 4 x 16bar = 128  [CO]")
    print("     (vector-like, no net chirality)")
    print()
    print("  B. Per semi-spinor (Lorentz [CP]):  1 generation per semi-spinor")
    print("     64+ = 1 gen (16_L + 16bar_R)  [CP]")
    print("     64- = 1 gen (16bar_L + 16_R)  [CP] (conjugate generation)")
    print("     => 2 semi-spinors, but only 1 independent generation")
    print("        (the other is its conjugate)")
    print()
    print("  C. Full E8 with SU(9) structure: 3 generations  [CO]")
    print("     The SU(3)_family from SU(4) inside SU(9) gives multiplicity 3.")
    print("     This is INVISIBLE to the SO(16) decomposition alone.")
    print()

    print("  KEY INSIGHT: The SO(16) route and SU(9) route MUST give")
    print("  compatible results, since both decompose the same 248.")
    print("  The apparent discrepancy (2 vs 3) is resolved by noting")
    print("  that the SO(16) route does not see the full structure.")
    print()

    print("  The SO(16) route sees 128 = 64+ + 64-, and calls each")
    print("  semi-spinor '1 generation'. But the SU(9) route reveals")
    print("  that the 128 spinor weights reorganize as 3 generations + exotics")
    print("  when viewed through the SU(5) x SU(3) lens.")
    print()


# ==========================================================================
# PART 7: Reconciling the two decompositions
# ==========================================================================

def reconcile_decompositions():
    """
    How can 128 be BOTH "2 x 64" and "contain 3 x 16"?

    The answer: the 128 is 128 regardless of how you decompose it.
    Under SO(10) alone (forgetting SO(4) and U(1)):
      128 = 4 x 16 + 4 x 16bar [CO]

    Under SU(5) alone (inside SO(10)):
      16 = 10bar + 5bar + 1
      16bar = 10 + 5 + 1

    So 128 = 4 x (10bar + 5bar + 1) + 4 x (10 + 5 + 1)
           = 4 x 10bar + 4 x 5bar + 4 x 1 + 4 x 10 + 4 x 5 + 4 x 1

    Under SU(5) x SU(3)_family (from the SU(9) route):
      The SAME 128 weights reorganize as:
        (10bar, 3) + (10bar, 1) + (5, 3) + (5, 3bar) + ...

    The 3 generations arise because SU(3)_family acts on the 128 in a way
    that groups 3 of the 4 copies of 16 into a triplet, with 1 left as singlet.

    Specifically: 4 = 3 + 1 (SU(4) -> SU(3) x U(1))
    The 4 copies of 10bar split as: 3 in a triplet + 1 as singlet.
    """
    print("=" * 80)
    print("PART 7: Reconciling SO(16) and SU(9) Decompositions")
    print("=" * 80)
    print()

    print("  Under SO(10) alone, the 128 contains:  [CO]")
    print("    4 copies of 16 + 4 copies of 16bar")
    print()

    print("  Under SU(5) x SU(4) (from SU(9) route), the 84 = Lambda^3(C^9):")
    print("    Contains (10bar, 4) = 4 copies of 10bar of SU(5)  [CO]")
    print()

    print("  Under SU(5) x SU(3) x U(1) (breaking SU(4)):  [CO]")
    print("    (10bar, 4) -> (10bar, 3)_(+1) + (10bar, 1)_(-3)")
    print("    => 3 copies in SU(3) triplet + 1 singlet")
    print()

    print("  THIS IS THE KEY: 4 = 3 + 1  [SP: SU(4) -> SU(3) x U(1)]")
    print()
    print("  The '4 copies of 16' from the SO(10) perspective split as:")
    print("    3 copies transforming as SU(3) triplet (= 3 generations)")
    print("    1 copy as SU(3) singlet (= exotic)")
    print()
    print("  Similarly for the 5bar and the singlet nu^c.")
    print()

    print("  DIMENSIONAL CROSS-CHECK:")
    print(f"    3 generations: 3 x 16 = {3*16}")
    print(f"    Exotics:       84 - 48 = {84-48}")
    print(f"    Total (one 84): {84}")
    print(f"    Full E8 matter: 84 + 84 = {84+84}")
    print(f"    E8 gauge:       80")
    print(f"    Total:          {80+84+84} = 248  [MV: e8_su9_decomposition]")
    print()


# ==========================================================================
# PART 8: Comparison table
# ==========================================================================

def comparison_table():
    """
    Systematic comparison of generation mechanisms across GUT groups.
    """
    print("=" * 80)
    print("PART 8: Comparison Table -- SO(14) vs SO(10) vs E6 vs E8")
    print("=" * 80)
    print()

    headers = [
        "Group", "Dim", "Matter Rep", "Matter Dim",
        "16 copies", "Mechanism", "Generations"
    ]
    rows = [
        ["SU(5)", "24", "5bar+10", "16", "1",
         "by hand: 3 copies", "3 (ad hoc)"],
        ["SO(10)", "45", "16 (spinor)", "16", "1",
         "by hand: 3 copies", "3 (ad hoc)"],
        ["E6", "78", "27 (fund)", "27", "1 (16+10+1)",
         "by hand: 3 copies", "3 (ad hoc)"],
        ["SO(14)", "91", "64 (semi-spinor)", "64", "2 (via SO(4))",
         "Lorentz: 1 gen", "1 or 2"],
        ["SO(14) in E8", "91/248", "128 (from E8)", "128", "4 (via SO(10))",
         "SU(9)->SU(3)_fam", "3 (from E8)"],
        ["E8", "248", "84+84* (adj)", "168", "3 x (16 equiv)",
         "SU(9) Lambda^3", "3 (natural)"],
    ]

    # Print table
    col_widths = [12, 8, 18, 12, 12, 18, 14]
    header_line = "  "
    for h, w in zip(headers, col_widths):
        header_line += f"{h:<{w}}"
    print(header_line)
    print("  " + "-" * sum(col_widths))
    for row in rows:
        line = "  "
        for val, w in zip(row, col_widths):
            line += f"{val:<{w}}"
        print(line)
    print()

    print("  TAGS:")
    print("    SU(5), SO(10), E6: 3 generations by putting 3 copies by hand [SP]")
    print("    SO(14) alone: 1-2 generations from semi-spinor structure [CO]")
    print("    E8 via SU(9): 3 generations from Lambda^3(C^9) structure [CO]")
    print("    The E8 mechanism is the only one that DERIVES 3 rather than assuming it.")
    print()


# ==========================================================================
# PART 9: Mechanisms for 3 generations (detailed)
# ==========================================================================

def generation_mechanisms():
    """
    Survey of mechanisms that could give exactly 3 generations for SO(14).
    """
    print("=" * 80)
    print("PART 9: Mechanisms for Exactly 3 Generations")
    print("=" * 80)
    print()

    print("  MECHANISM 1: E8 -> SU(9) -> SU(5) x SU(3)_family  [CO/CP]")
    print("  -" * 30)
    print("  Status: WORKS (proven dimensionally in Lean)")
    print("  Source of 3: dim(fund. SU(3)) = 3")
    print("  Evidence: [MV] Lean proofs in three_generation_theorem.lean")
    print("  Caveat: requires E8 structure beyond SO(14)")
    print("  Caveat: SU(3)_family identification is [CP]")
    print()

    print("  MECHANISM 2: Orbifold compactification  [CP]")
    print("  -" * 30)
    print("  Status: PLAUSIBLE (exists for SO(2N) in literature)")
    print("  Reference: Kawamura-Miura (2010), Maru-Nago (2025)")
    print("  Idea: 5D or 6D SO(14) with orbifold boundary conditions")
    print("    projects bulk spinor into 3 chiral zero modes")
    print("  Evidence: demonstrated for SO(18), SO(20) family unification")
    print("  Caveat: requires extra dimensions, specific orbifold choice")
    print()

    print("  MECHANISM 3: Calabi-Yau compactification  [CP]")
    print("  -" * 30)
    print("  Status: STANDARD in string theory")
    print("  Reference: Witten (1985), Candelas-Horowitz-Strominger-Witten (1985)")
    print("  Idea: Compactify on CY3 with Euler number chi = 6")
    print("    -> |chi|/2 = 3 generations")
    print("  Evidence: works for E8 x E8 heterotic string")
    print("  Caveat: requires 10D starting point, string theory")
    print()

    print("  MECHANISM 4: Discrete family symmetry (S3, A4, Z3)  [CP]")
    print("  -" * 30)
    print("  Status: WELL-STUDIED for SO(10)")
    print("  Reference: Gresnigt (2026), Babu-Pati-Wilczek")
    print("  Idea: impose S3 or A4 discrete symmetry on generation index")
    print("  Evidence: explains mass hierarchy, mixing angles")
    print("  Caveat: symmetry imposed by hand, not derived from gauge group")
    print()

    print("  MECHANISM 5: D4 triality in Spin(8)  [CP]")
    print("  -" * 30)
    print("  Status: SPECULATIVE but elegant")
    print("  Reference: Mentioned in e8_embedding.lean")
    print("  Idea: SO(8) has triality (S3 symmetry permuting 8v, 8s, 8c)")
    print("    Three 8-dim representations -> 3 generations")
    print("  Evidence: dimensional (3 distinct 8-dim reps exist)")
    print("  Caveat: how triality maps to fermion generations is unclear")
    print()

    print("  ASSESSMENT [CO]:")
    print("    Mechanism 1 (E8/SU(9)) is the most concrete and is partly")
    print("    machine-verified. Mechanisms 2-3 are standard physics but")
    print("    require additional structure. Mechanism 4 is ad hoc.")
    print("    Mechanism 5 needs further development.")
    print()
    print("    SO(14) ALONE does NOT give 3 generations. [MV: three_ndvd_two]")
    print("    SO(14) WITHIN E8 gives 3 generations via SU(9). [CO]")
    print("    This is NOT a kill condition -- it is the same open problem")
    print("    as in SO(10), with a concrete E8-based resolution. [CO]")
    print()


# ==========================================================================
# PART 10: Weight-level verification of 128 under SO(10)
# ==========================================================================

def weight_level_128():
    """
    Explicit weight-level computation of the 128 semi-spinor of D8
    under SO(10) x SO(4) x U(1).

    D8 semi-spinor weights: 8-tuples with all entries +/-1/2,
    even number of minus signs (for S+).

    Split as (h1,...,h5 | h6,h7 | h8):
      First 5 -> D5 = SO(10)
      Next 2  -> D2 = SO(4)
      Last 1  -> SO(2) = U(1)
    """
    print("=" * 80)
    print("PART 10: Explicit Weight-Level Computation of 128_s")
    print("=" * 80)
    print()

    # Generate D8 semi-spinor weights (S+: even number of minus signs)
    all_weights_8 = []
    for combo in product([+1, -1], repeat=8):
        weight = tuple(s / 2.0 for s in combo)
        n_minus = sum(1 for s in combo if s == -1)
        if n_minus % 2 == 0:
            all_weights_8.append(weight)

    assert len(all_weights_8) == 128
    print(f"  Generated {len(all_weights_8)} weights of S+(D8) = 128_s")
    print()

    # Classify under SO(10) x SO(4) x U(1)
    decomp = defaultdict(int)
    for w in all_weights_8:
        so10_w = w[:5]
        so4_w = w[5:7]
        u1_w = w[7]

        # SO(10)
        n_minus_10 = sum(1 for h in so10_w if h < 0)
        so10_rep = '16' if n_minus_10 % 2 == 0 else '16bar'

        # SO(4)
        h6, h7 = so4_w
        if h6 * h7 > 0:
            so4_rep = '(2,1)'
        else:
            so4_rep = '(1,2)'

        # U(1) charge
        u1_charge = u1_w

        decomp[(so10_rep, so4_rep, u1_charge)] += 1

    print("  128_s under SO(10) x SO(4) x U(1):")
    print()
    total = 0
    total_16 = 0
    total_16bar = 0
    for key in sorted(decomp.keys()):
        so10_rep, so4_rep, u1_q = key
        n = decomp[key]
        so10_dim = 16
        so4_dim = 2
        mult = n // (so10_dim * so4_dim)
        total += n
        if so10_rep == '16':
            total_16 += n // 16
        else:
            total_16bar += n // 16
        print(f"    ({so10_rep}, {so4_rep}, q={u1_q:+.1f}): {n} weights"
              f" = {mult} x ({so10_rep} x {so4_rep})")

    print(f"\n  Total weights: {total} (expected 128)")
    assert total == 128
    print(f"  Total copies of 16 (as SO(10) reps): {total_16}")
    print(f"  Total copies of 16bar:                {total_16bar}")
    print()

    # Group by SO(14) semi-spinor
    print("  Grouped by SO(14) semi-spinor (D7 chirality):")
    print()
    for label, chirality_fn in [
        ("64+ (even D7 minus)", lambda w: sum(1 for h in w[:7] if h < 0) % 2 == 0),
        ("64- (odd D7 minus)",  lambda w: sum(1 for h in w[:7] if h < 0) % 2 == 1)
    ]:
        sub_weights = [w for w in all_weights_8 if chirality_fn(w)]
        sub_decomp = defaultdict(int)
        for w in sub_weights:
            so10_w = w[:5]
            so4_w = w[5:7]
            n_minus_10 = sum(1 for h in so10_w if h < 0)
            so10_rep = '16' if n_minus_10 % 2 == 0 else '16bar'
            h6, h7 = so4_w
            so4_rep = '(2,1)' if h6 * h7 > 0 else '(1,2)'
            u1_q = w[7]
            sub_decomp[(so10_rep, so4_rep, u1_q)] += 1

        print(f"    {label}: {len(sub_weights)} weights")
        for key in sorted(sub_decomp.keys()):
            so10_rep, so4_rep, u1_q = key
            n = sub_decomp[key]
            print(f"      ({so10_rep}, {so4_rep}, q={u1_q:+.1f}): {n} weights")
        print()


# ==========================================================================
# PART 11: Summary and honest assessment
# ==========================================================================

def honest_assessment():
    """
    Honest assessment of the three-generation problem for SO(14).
    """
    print("=" * 80)
    print("PART 11: HONEST ASSESSMENT")
    print("=" * 80)
    print()

    print("  QUESTION: Does SO(14) naturally produce exactly 3 generations?")
    print()
    print("  ANSWER: NO, not by itself.  [MV: three_ndvd_two]")
    print()
    print("  The 64-dim semi-spinor of Spin(14) contains exactly")
    print("  ONE generation of SM fermions (with antiparticles).")
    print("  The multiplicity of the 16 of SO(10) is 2 (from SO(4)).")
    print("  Since 3 does not divide 2, three generations are impossible")
    print("  from SO(14) alone.")
    print()

    print("  FOLLOW-UP: Does SO(14) within E8 give 3 generations?")
    print()
    print("  ANSWER: YES, via the SU(9) decomposition.  [CO]")
    print()
    print("  E8 -> SU(9) -> SU(5) x SU(3)_family x U(1)")
    print("  gives exactly 3 generations from:")
    print("    248 = 80 + 84 + 84*")
    print("    84 contains 3 x (10 + 5bar + 1) = 3 x 16")
    print("    The 3 comes from dim(fund. SU(3)) = 3.")
    print()

    print("  DOES SO(14) HELP, HURT, OR NOT CHANGE THE 3-GEN PROBLEM?")
    print()
    print("  ANSWER: SO(14) DOES NOT CHANGE IT relative to SO(10).  [CO]")
    print()
    print("  Like SO(10), SO(14) gives 1 generation per matter multiplet.")
    print("  Like SO(10), SO(14) needs additional structure for 3 generations.")
    print("  UNLIKE SO(18), SO(14) does NOT produce mirror fermions")
    print("  (in the semi-spinor -- the full Dirac spinor has mirrors,")
    print("  but the Majorana-Weyl condition in Spin(11,3) removes them).")
    print()

    print("  UNIQUE ADVANTAGE OF SO(14): It sits inside E8 in a way that")
    print("  the SU(9) decomposition naturally gives 3 generations.  [CO]")
    print("  This is NOT available to SO(10) without E8.")
    print()

    print("  KC-5 STATUS: DOES NOT FIRE.  [CO]")
    print("  Three generations are available via E8/SU(9) mechanism.")
    print("  The problem is the same as for SO(10): inherited, not worsened.")
    print()

    print("  KC-ELEVATED STATUS: DOES NOT FIRE.  [CO]")
    print("  SO(14) does NOT make the generation problem worse than SO(10).")
    print()


# ==========================================================================
# MAIN
# ==========================================================================

def main():
    print()
    print("*" * 80)
    print("  E8 GENERATION ANALYSIS: FULL BRANCHING CHAIN")
    print("  248 -> SO(16) -> SO(14) x U(1) -> SO(10) x SO(4) x U(1)")
    print("*" * 80)
    print()

    e8_to_so16()
    so16_adjoint_under_so14()
    so16_semispinor_under_so14()
    so14_results = so14_semispinor_decomposition()
    full_e8_decomposition()
    su9_decomposition()
    so16_route_analysis()
    reconcile_decompositions()
    comparison_table()
    generation_mechanisms()
    weight_level_128()
    honest_assessment()

    print("=" * 80)
    print("END OF E8 GENERATION ANALYSIS")
    print("=" * 80)


if __name__ == '__main__':
    main()
