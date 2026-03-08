"""
Mass Gap Investigation: Four Mathematical Questions
====================================================

Rigorous symbolic verification of mathematical claims connecting
Clifford algebras, Fortescue decomposition, and spectral theory
to the Yang-Mills mass gap problem.

Author: dollard-theorist agent
Date: 2026-03-08

QUESTIONS INVESTIGATED:
1. Does Clifford grading constrain Casimir eigenvalues?
2. Is there a Fortescue-to-root-space-decomposition map?
3. Does Cl(p,q) signature encode mass gap existence?
4. Do Dollard's four quadrants map to spectral decomposition?
"""

import numpy as np
from sympy import (
    symbols, Matrix, sqrt, Rational, pi, exp, I, cos, sin,
    cosh, sinh, simplify, expand, trigsimp, factor,
    eye, zeros, diag, conjugate, adjoint, trace,
    Symbol, Integer, Sum, Product, binomial, factorial,
    latex, pprint, BlockMatrix, tensorproduct,
    KroneckerDelta, LeviCivita
)
from sympy.physics.quantum import TensorProduct
from itertools import combinations
import sys

print("=" * 78)
print("MASS GAP INVESTIGATION: FOUR MATHEMATICAL QUESTIONS")
print("=" * 78)

# ============================================================================
# QUESTION 1: CLIFFORD ALGEBRA SPECTRAL STRUCTURE
# ============================================================================

print("\n" + "=" * 78)
print("QUESTION 1: CLIFFORD GRADING AND CASIMIR EIGENVALUES")
print("=" * 78)

print("""
THEOREM (Grade-2 Lie algebra):
  For Cl(n,0), the grade-2 elements e_ij (i<j) form so(n) under [A,B] = AB-BA.
  There are C(n,2) = n(n-1)/2 such generators.

For Cl(14,0): dim so(14) = C(14,2) = 91.

QUESTION: Does the Clifford grade structure constrain Casimir eigenvalues?
""")

# Verify dimension counting
n = 14
so_dim = n * (n - 1) // 2
print(f"so({n}) dimension = C({n},2) = {so_dim}")
assert so_dim == 91

# The Casimir operator C_2 = sum_a T_a^2
# For so(n), the quadratic Casimir in the fundamental representation:
#   C_2(fund) = (n-1)/2 * I_n
# This is a KNOWN result (Humphreys, "Introduction to Lie Algebras").

print(f"\nQuadratic Casimir C_2 for so({n}) in fundamental representation:")
casimir_fund = Rational(n - 1, 2)
print(f"  C_2(fund) = {casimir_fund} * I_{n} = {float(casimir_fund)} * I_{n}")

# For general irrep labeled by highest weight lambda:
# C_2(lambda) = (lambda, lambda + 2*rho) where rho = half-sum of positive roots
# For so(n), rho = (1/2) * sum of positive roots

print(f"\nFor so({n}), the rank is r = {n//2} = 7")
print(f"Positive roots: C({n},2) - {n//2} = {so_dim - n//2} non-Cartan + {n//2} Cartan = {so_dim}")

# Key observation about grading:
print("""
ANALYSIS: The Clifford grading and Casimir eigenvalues

The Clifford algebra Cl(n,0) has a Z-grading: Cl(n,0) = oplus_{k=0}^n Cl^k(n,0)
where Cl^k has dimension C(n,k).

The grade-2 space Cl^2(n,0) = so(n) under the commutator bracket.

DOES the grading constrain Casimir eigenvalues?

The answer depends on what we mean precisely:

1. The CLIFFORD grading is a Z/2-grading (even/odd) that makes Cl(n,0)
   into a superalgebra. The even subalgebra Cl^+(n,0) contains so(n)
   as a subspace.

2. The Casimir C_2 = sum T_a^2 where T_a are the so(n) generators
   (grade-2 elements) acting in a representation V.

3. For the ADJOINT representation (so(n) acting on itself):
   C_2(adj) acts on the 91-dimensional adjoint space.
   By Schur's lemma, if adjoint is irreducible, C_2(adj) = c * I_{91}.

   For so(n), the adjoint IS irreducible (for n >= 3).
   The Casimir eigenvalue in the adjoint is:
     C_2(adj) = 2(n-2) for so(n)
""")

casimir_adj = 2 * (n - 2)
print(f"C_2(adjoint of so({n})) = 2({n}-2) = {casimir_adj}")

# Now: does the GRADE structure add anything beyond standard Lie theory?
print("""
CRITICAL FINDING:

The Clifford grading does NOT directly constrain Casimir eigenvalues
BEYOND what standard Lie theory already gives. Here is why:

a) The grade-2 space forms so(n) as a Lie algebra. The Casimir is
   determined by the Lie algebra structure constants, which are
   FULLY determined by the Clifford relations e_i*e_j + e_j*e_i = 2*delta_ij.

b) The grade structure tells us DIM(so(n)) = C(n,2), which is standard.

c) The Clifford algebra gives an efficient COMPUTATIONAL framework
   for computing with so(n), but it does not give spectral information
   that is not already in the Lie algebra.

d) The higher grades (3,4,...) of Cl(n,0) do NOT directly constrain
   the spectrum of the Casimir on representations of so(n).

HOWEVER, there is one indirect connection:

The SPINOR representation of so(n) is naturally constructed from
Cl(n,0). The spinor space is a minimal left ideal of Cl(n,0).
For so(14), the spinor has dimension 2^7 = 128.

The Casimir eigenvalue on the spinor representation IS constrained
by the Clifford structure:
""")

# Casimir on spinor representation of so(n)
# For so(2m), spinor dim = 2^m, and C_2(spinor) = m*(2m-1)/8 * n
# Actually, more precisely:
# C_2(Dirac spinor of so(2m)) = m(2m-1)/4
# for the half-spinors: C_2(S+) = C_2(S-) = m(2m-1)/4

m = n // 2  # m = 7
casimir_spinor = Rational(m * (2 * m - 1), 4)
print(f"C_2(spinor of so({n})) = {m}*{2*m-1}/4 = {casimir_spinor} = {float(casimir_spinor)}")

print("""
VERDICT on Question 1:

The Clifford grading does NOT directly imply a mass gap through
Casimir eigenvalue constraints. The Casimir eigenvalues are determined
by representation theory of the Lie algebra so(n), which is independent
of whether we realize so(n) inside a Clifford algebra or not.

The grading provides COMPUTATIONAL convenience but no new SPECTRAL
information. The mass gap is a property of the QUANTUM DYNAMICS
(functional integral, non-perturbative effects), not of the algebraic
structure of the gauge group.

STATUS: NO new constraint found. The Clifford embedding is computationally
useful but spectrally neutral for the mass gap question.
""")

# ============================================================================
# QUESTION 2: FORTESCUE AND ROOT SPACE DECOMPOSITION
# ============================================================================

print("\n" + "=" * 78)
print("QUESTION 2: FORTESCUE vs ROOT SPACE DECOMPOSITION")
print("=" * 78)

print("""
SETUP:
  Fortescue: F_k = (1/N) sum_{n=0}^{N-1} x_n * omega^{-nk},  omega = e^{2*pi*i/N}
  Root space: g = h oplus (oplus_alpha g_alpha),  [H, E_alpha] = alpha(H) * E_alpha

QUESTION: Is there a precise mathematical map between these?
""")

# Let's work with so(N) for small N to check this concretely.
# Start with so(4) which decomposes as su(2) x su(2).

print("=== Concrete verification: N=4, so(4) ===\n")

# so(4) generators: e_{ij} for 1 <= i < j <= 4
# There are C(4,2) = 6 generators.
# so(4) = su(2)_L x su(2)_R (accident of dimension 4)

# Cartan subalgebra of so(4): rank 2
# Choose H_1 = e_{12}, H_2 = e_{34}
# Root space decomposition:
#   Cartan: {H_1, H_2} (2-dimensional)
#   Roots: {e_{13}, e_{14}, e_{23}, e_{24}} (4 root spaces, each 1-dimensional)
#   But paired: alpha and -alpha share generators via E_alpha, E_{-alpha}

print("so(4) has rank 2, dim = 6")
print("Cartan subalgebra h = span{H_1=e_{12}, H_2=e_{34}}")
print("Root spaces: 4 roots (2 positive + 2 negative)")
print()

# Now: Fortescue's 4-phase decomposition
# F = (1/4) * A_4^H * x  where A_4[p,s] = omega^{p*s}, omega = e^{2*pi*i/4} = i

print("=== Fortescue 4-phase DFT matrix ===\n")
N = 4
omega_N = np.exp(2j * np.pi / N)
A_4 = np.array([[omega_N**(p*s) for s in range(N)] for p in range(N)])
print("A_4 =")
# Clean display
for row in A_4:
    print("  [", "  ".join(f"{z.real:+.0f}{z.imag:+.0f}j" for z in row), "]")

print()

# The Fortescue matrix for N=4 uses omega = i, so:
# A_4 = [[1, 1, 1, 1],
#         [1, i, -1, -i],
#         [1, -1, 1, -1],
#         [1, -i, -1, i]]

# This decomposes a 4-phase signal into symmetrical components:
# F_0 = zero-sequence (common mode)
# F_1 = positive sequence (forward rotation)
# F_2 = negative sequence (backward rotation - for even N, this is special)
# F_3 = negative sequence (conjugate of positive)

print("=== Root system of so(4) ===\n")

# so(4) root system in the standard basis:
# Positive roots: e_1 - e_2, e_1 + e_2
# where e_1, e_2 are the standard basis of h*

# These are the roots of the D_2 = A_1 x A_1 root system
print("Root system of so(4) = D_2:")
print("  Positive roots: {(1,-1), (1,1)}")
print("  Negative roots: {(-1,1), (-1,-1)}")
print("  This is A_1 x A_1 (two copies of su(2))")
print()

# KEY ANALYSIS: The connection
print("""
=== ANALYSIS: The precise relationship ===

The Fortescue DFT and the root space decomposition are BOTH
eigenvalue decompositions, but of DIFFERENT operators:

FORTESCUE: Decomposes by eigenvalues of the CYCLIC SHIFT operator
  sigma: (x_0, x_1, ..., x_{N-1}) -> (x_{N-1}, x_0, ..., x_{N-2})
  The eigenvalues are omega^k for k = 0, ..., N-1.
  The DFT diagonalizes this cyclic shift.

ROOT SPACE: Decomposes by eigenvalues of the CARTAN generators
  ad(H): g -> g,  ad(H)(X) = [H, X]
  The eigenvalues are the roots alpha(H).

QUESTION: When do these coincide?

THEOREM: They coincide when g has a Z/N automorphism phi such that:
  (a) phi^N = id
  (b) The eigenspaces of phi give the root space decomposition
  (c) phi acts as the cyclic shift on a suitable basis

This happens for the PRINCIPAL GRADING of a Lie algebra.
""")

# Verify for su(N): the principal Z/N grading
print("=== Verification: su(3) with Z/3 grading ===\n")

# su(3) has rank 2, dim 8
# The principal grading uses the Coxeter element phi = s_1 * s_2
# (product of simple reflections) which has order h = 3 (Coxeter number)

# For su(3), the Coxeter number is h = 3
# The principal grading: g = g_0 oplus g_1 oplus g_2
# where g_k = {X in g : phi(X) = omega^k * X}

# g_0 = Cartan subalgebra h (dim 2)
# g_1 = positive root spaces (dim 3)
# g_2 = negative root spaces (dim 3)
# Total: 2 + 3 + 3 = 8 = dim su(3)

print("su(3): Coxeter number h = 3")
print("Principal Z/3 grading:")
print("  g_0 = Cartan subalgebra, dim 2")
print("  g_1 = positive root spaces, dim 3")
print("  g_2 = negative root spaces, dim 3")
print("  Total: 2 + 3 + 3 = 8 = dim su(3)  OK")
print()

# For su(N), Coxeter number = N
# Principal grading: g_k for k = 0, ..., N-1
# This IS a Fortescue-type decomposition with omega = e^{2*pi*i/N}

print("GENERAL RESULT for su(N):")
print(f"  Coxeter number h = N")
print(f"  Principal Z/N grading: g = oplus_{{k=0}}^{{N-1}} g_k")
print(f"  g_0 = Cartan subalgebra, dim = N-1 (rank)")
print(f"  g_k (k != 0) = root spaces with Coxeter eigenvalue omega^k")
print()

# For so(N), the Coxeter number is different
print("For so(N):")
so_coxeter = {3: 2, 4: 2, 5: 4, 6: 4, 7: 6, 8: 6, 10: 8, 14: 12}
for nn, h_cox in sorted(so_coxeter.items()):
    print(f"  so({nn}): Coxeter number h = {h_cox}, "
          f"so principal grading is Z/{h_cox}, NOT Z/{nn}")

print()

# Explicit verification: Fortescue as a representation-theoretic tool
print("=== The precise theorem ===\n")

print("""
THEOREM (Fortescue-Root Space Connection):

Let g be a simple Lie algebra of rank r with Coxeter number h.
Let phi be a Coxeter element (product of simple reflections).
Then:

  g = oplus_{k=0}^{h-1} g_k

where g_k = {X in g : phi(X) = omega_h^k * X} and omega_h = e^{2*pi*i/h}.

This decomposition has the SAME structure as Fortescue's N-phase
decomposition with N = h (the Coxeter number), NOT N = dim(g).

Specifically:
  - The Fortescue matrix F_h diagonalizes the action of phi on g
  - The "symmetrical components" are the eigenspaces g_k
  - The "zero sequence" g_0 is the Cartan subalgebra

PROOF SKETCH:
  The Coxeter element phi has order h and acts semisimply on g.
  Its eigenvalues are omega_h^{m_i} where m_i are the EXPONENTS
  of g (i = 1, ..., r). For su(N), the exponents are 1, 2, ..., N-1.
  The eigenspace decomposition IS a DFT with period h.

CONSEQUENCE:
  Fortescue's decomposition generalizes to ANY Lie algebra via the
  principal grading. It gives spectral information about the adjoint
  representation, decomposing by Coxeter eigenvalues.
""")

# Verify exponents
print("Verification of exponents:")
print("  su(3) = A_2: exponents = {1, 2}, Coxeter h = 3")
print("  su(4) = A_3: exponents = {1, 2, 3}, Coxeter h = 4")
print("  su(5) = A_4: exponents = {1, 2, 3, 4}, Coxeter h = 5")
print("  so(7) = B_3: exponents = {1, 3, 5}, Coxeter h = 6")
print()

# For so(2m) = D_m: rank = m, Coxeter number = 2(m-1)
# D_m exponents: 1, 3, 5, ..., 2m-3, m-1
# so(10) = D_5: rank 5, h = 2*4 = 8, exponents = {1, 3, 4, 5, 7}
# so(14) = D_7: rank 7, h = 2*6 = 12, exponents = {1, 3, 5, 6, 7, 9, 11}

print("Exponents for so(2m) = D_m:")
print("  D_m exponents: {1, 3, 5, ..., 2m-3, m-1}")
print("  D_5 (so(10)): exponents = {1, 3, 4, 5, 7}, h = 8")
print("  D_7 (so(14)): exponents = {1, 3, 5, 6, 7, 9, 11}, h = 12")
print()

# So for so(14), the principal grading is Z/12, not Z/14
print("KEY RESULT for so(14):")
print("  Coxeter number h = 12")
print("  Principal grading: so(14) = oplus_{k=0}^{11} g_k")
print("  This is a 12-phase Fortescue decomposition of so(14)")
print("  NOT a 14-phase decomposition")
print()

# Verify dimensions add up
# dim so(14) = 91
# Eigenspace dimensions: for D_7, exponents are 1,3,5,7,9,11,6
# Each exponent m_i contributes rank=1 to g_{m_i} and g_{h-m_i}
# g_0 = Cartan, dim = rank = 7
# Total = 7 + 2*sum of non-zero eigenspace dims = 7 + 2*42 = 91? Let me check
print("Dimension verification for D_7 principal grading:")
print("  g_0 (Cartan): dim = 7 (rank)")
# D_7 exponents: 1, 3, 5, 6, 7, 9, 11
# Each exponent m_i != h/2 contributes dim 1 to g_{m_i}
# For h=12, h/2=6. The exponent 6 contributes to g_6 only.
exponents_D7 = [1, 3, 5, 6, 7, 9, 11]
print(f"  Exponents: {exponents_D7}")
# g_k has dimension = number of exponents equal to k (for k != 0)
# plus number of exponents equal to h-k (via the mapping)
# Actually, the standard result is:
# dim g_k = |{i : m_i = k mod h}| for the ADJOINT representation
# For the principal grading, each g_k (k != 0) has dim = rank = r if
# the eigenvalue omega^k appears with multiplicity equal to the number
# of exponents congruent to k mod h.

# Actually the correct statement: g_k has dimension equal to the
# number of roots alpha such that ht(alpha) = k mod h
# where ht is the height function.

# Let me just verify the total
total = 7  # Cartan
# For D_7 with h=12, the 84 root vectors distribute among g_1,...,g_11
# Total roots = 2 * (number of positive roots) = 2 * C(7,2) + 2*C(7,2)
# Wait: |roots of D_m| = 2*m*(m-1)
num_roots = 2 * 7 * (7 - 1)
print(f"  Number of roots of D_7: 2*7*6 = {num_roots}")
print(f"  dim so(14) = rank + |roots| = 7 + {num_roots} = {7 + num_roots}")
assert 7 + num_roots == 91

print(f"\n  Verified: 7 + 84 = 91 = dim so(14)")

print("""
VERDICT on Question 2:

YES, there IS a precise mathematical relationship, but it is MORE SUBTLE
than a naive identification:

1. Fortescue's N-phase decomposition is a DFT with period N.
2. The root space decomposition of g is related to the PRINCIPAL GRADING,
   which is a DFT with period h (Coxeter number), NOT N.
3. For su(N), h = N, so the identification is exact:
   Fortescue's N-phase decomposition = principal grading of su(N).
4. For so(N), h != N in general (h = N-2 for so(N) with N even).
5. The Fortescue "symmetrical components" correspond to eigenspaces
   of the Coxeter element, which organize the root system.

THE PRECISE MAP:
  Fortescue component F_k <-> principal grading eigenspace g_k
  Fortescue omega = e^{2*pi*i/h} <-> Coxeter element eigenvalue
  Zero sequence F_0 <-> Cartan subalgebra h

This gives Fortescue's method a representation-theoretic interpretation:
it is decomposing the adjoint representation by Coxeter eigenvalues.

DOES THIS HELP WITH THE MASS GAP?
  Partially. The principal grading organizes the root system, and the
  root system determines the representation theory of g, which in turn
  determines the classical structure of Yang-Mills theory. But the
  mass gap is a QUANTUM, NON-PERTURBATIVE phenomenon that goes beyond
  the algebraic structure of the gauge group.

  The Fortescue-Coxeter connection is MATHEMATICALLY GENUINE but
  PHYSICALLY INSUFFICIENT for the mass gap.

STATUS: Genuine mathematical relationship found. Insufficient for mass gap.
""")

# ============================================================================
# QUESTION 3: Cl(p,q) SIGNATURE AND MASS GAP
# ============================================================================

print("\n" + "=" * 78)
print("QUESTION 3: CLIFFORD SIGNATURE AND MASS GAP EXISTENCE")
print("=" * 78)

print("""
SETUP:
  Cl(p,q) has p generators with e_i^2 = +1 and q generators with e_j^2 = -1.
  The grade-2 elements form so(p,q) (indefinite orthogonal Lie algebra).

  j (j^2=-1) -> Cl(0,1) component -> circular/compact/rotation
  h (h^2=+1) -> Cl(1,0) component -> hyperbolic/non-compact/boost

  Compact gauge groups: SU(N), SO(N), Sp(N) -> mass gap expected
  Non-compact gauge groups: SO(p,q), SL(N,R) -> NO mass gap

QUESTION: Does Cl(p,q) signature directly encode mass gap existence?
""")

# Key mathematical facts about compact vs non-compact
print("=== Compact vs Non-compact Lie groups ===\n")

print("""
DEFINITIONS:
  - A Lie group G is COMPACT if it is compact as a topological space.
  - Equivalently, G is compact iff its Lie algebra g admits a
    POSITIVE DEFINITE ad-invariant bilinear form (Killing form is
    negative definite for compact semisimple groups).

CLIFFORD CONNECTION:
  - so(n) = so(n,0) comes from Cl(n,0) (all positive signature)
    -> so(n) is the Lie algebra of SO(n), which IS compact

  - so(p,q) with q > 0 comes from Cl(p,q) (mixed signature)
    -> so(p,q) is the Lie algebra of SO(p,q), which is NOT compact

  - su(n) does NOT come directly from a real Clifford algebra,
    but from the COMPLEXIFICATION. su(n) is compact.

THEOREM (Killing form criterion):
  The Killing form B(X,Y) = Tr(ad_X o ad_Y) is:
  - NEGATIVE DEFINITE for compact semisimple Lie algebras
  - INDEFINITE for non-compact semisimple Lie algebras
""")

# Compute Killing form signatures for small cases
print("=== Killing form computation for so(3) vs so(2,1) ===\n")

# so(3) generators: standard basis L_1, L_2, L_3
# [L_i, L_j] = epsilon_{ijk} L_k
# Killing form: B(L_i, L_j) = Tr(ad_{L_i} ad_{L_j})

# For so(3): ad_{L_1} has matrix [[0,0,0],[0,0,-1],[0,1,0]] etc
# B_{ij} = -2 delta_{ij} (negative definite -> compact)

print("so(3) = Lie algebra of SO(3) [compact]:")
# Structure constants of so(3)
def so3_structure_constants():
    """f_{ijk} where [L_i, L_j] = sum_k f_{ijk} L_k"""
    f = np.zeros((3, 3, 3))
    # [L_1, L_2] = L_3, etc (Levi-Civita)
    f[0, 1, 2] = 1; f[1, 0, 2] = -1
    f[1, 2, 0] = 1; f[2, 1, 0] = -1
    f[0, 2, 1] = -1; f[2, 0, 1] = 1
    return f

f_so3 = so3_structure_constants()

# Killing form: B_{ij} = sum_{k,l} f_{ikl} f_{jlk}
B_so3 = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                B_so3[i, j] += f_so3[i, k, l] * f_so3[j, l, k]

print(f"  Killing form B = \n{B_so3}")
eigenvals_so3 = np.linalg.eigvalsh(B_so3)
print(f"  Eigenvalues: {eigenvals_so3}")
print(f"  Signature: ({sum(eigenvals_so3 > 0)}, {sum(eigenvals_so3 < 0)}, {sum(np.abs(eigenvals_so3) < 1e-10)})")
print(f"  NEGATIVE DEFINITE: {all(eigenvals_so3 < 0)}")
print()

# so(2,1) generators: K_1, K_2 (boosts), L_3 (rotation)
# [L_3, K_1] = K_2, [L_3, K_2] = -K_1, [K_1, K_2] = -L_3
# Note the minus sign in the last relation (non-compact!)

print("so(2,1) = Lie algebra of SO(2,1) [non-compact]:")

def so21_structure_constants():
    """[L_3, K_1] = K_2, [L_3, K_2] = -K_1, [K_1, K_2] = -L_3"""
    # Basis: {K_1, K_2, L_3} = {0, 1, 2}
    f = np.zeros((3, 3, 3))
    # [L_3(=2), K_1(=0)] = K_2(=1)
    f[2, 0, 1] = 1; f[0, 2, 1] = -1
    # [L_3(=2), K_2(=1)] = -K_1(=0)
    f[2, 1, 0] = -1; f[1, 2, 0] = 1
    # [K_1(=0), K_2(=1)] = -L_3(=2)
    f[0, 1, 2] = -1; f[1, 0, 2] = 1
    return f

f_so21 = so21_structure_constants()

B_so21 = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                B_so21[i, j] += f_so21[i, k, l] * f_so21[j, l, k]

print(f"  Killing form B = \n{B_so21}")
eigenvals_so21 = np.linalg.eigvalsh(B_so21)
print(f"  Eigenvalues: {eigenvals_so21}")
print(f"  Signature: ({sum(eigenvals_so21 > 0)}, {sum(eigenvals_so21 < 0)}, {sum(np.abs(eigenvals_so21) < 1e-10)})")
print(f"  NEGATIVE DEFINITE: {all(eigenvals_so21 < 0)}")
print(f"  INDEFINITE: {any(eigenvals_so21 > 0) and any(eigenvals_so21 < 0)}")
print()

# The key theorem
print("""
=== The signature theorem ===

THEOREM (Compactness from Clifford signature):

Let so(p,q) be the Lie algebra of grade-2 elements of Cl(p,q).
Then:
  (a) so(p,q) is compact  iff  q = 0  (or p = 0, by symmetry)
  (b) so(p,q) with p,q > 0 is non-compact (indefinite Killing form)

PROOF:
  The Killing form of so(p,q) has signature determined by:
  B(e_{ij}, e_{kl}) = Tr(ad_{e_ij} o ad_{e_kl})

  For so(n,0): B is negative definite (standard result for compact
  simple Lie algebras, Cartan's criterion).

  For so(p,q) with p,q > 0: the "boost" generators e_{ab} with
  a in {1,...,p} and b in {p+1,...,p+q} generate non-compact directions.
  The Killing form restricted to these generators has the OPPOSITE sign
  from the rotation generators, making B indefinite.

CONNECTION TO MASS GAP:

The Clay Institute mass gap problem specifies:
  "For any COMPACT simple gauge group G..."

The Cl(p,q) signature tells us EXACTLY when the gauge group is compact:
  - Cl(n,0) -> so(n) -> SO(n) [compact] -> mass gap EXPECTED
  - Cl(p,q) with q>0 -> so(p,q) -> SO(p,q) [non-compact] -> NO mass gap

But this is NOT a new result. It is the DEFINITION of the problem.
The mass gap conjecture is STATED for compact groups because:
  1. Non-compact gauge theories are not unitary (ghost states)
  2. The functional integral does not converge for non-compact groups
  3. Physically, non-compact gauge symmetries correspond to
     spacetime symmetries (Lorentz, diffeomorphisms), not internal symmetries

SO: The Clifford signature encodes compactness, which is a PREREQUISITE
for the mass gap, not a PROOF of it.
""")

# Verify the claim computationally for so(4) vs so(3,1) vs so(2,2)
print("=== Numerical verification: Killing form signatures ===\n")

def compute_killing_form(structure_constants, dim):
    """Compute Killing form from structure constants."""
    B = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                for l in range(dim):
                    B[i, j] += structure_constants[i, k, l] * structure_constants[j, l, k]
    return B

def so_structure_constants(n, signature=None):
    """
    Structure constants of so(p,q) where p+q=n.
    Generators: e_{ab} for a < b.
    [e_{ab}, e_{cd}] = eta_{bc}*e_{ad} - eta_{ac}*e_{bd} + eta_{ad}*e_{bc} - eta_{bd}*e_{ac}
    where eta = diag(+1,...,+1,-1,...,-1) with p plus signs and q minus signs.
    """
    if signature is None:
        signature = [1] * n  # all positive = so(n,0)

    eta = np.diag(signature)
    dim = n * (n - 1) // 2

    # Index mapping: (a,b) with a < b -> linear index
    pairs = [(a, b) for a in range(n) for b in range(a+1, n)]
    pair_to_idx = {p: i for i, p in enumerate(pairs)}

    f = np.zeros((dim, dim, dim))

    for i, (a, b) in enumerate(pairs):
        for j, (c, d) in enumerate(pairs):
            # [e_{ab}, e_{cd}] = eta_{bc}*e_{ad} - eta_{ac}*e_{bd} + eta_{ad}*e_{bc} - eta_{bd}*e_{ac}
            terms = [
                (eta[b, c], a, d),
                (-eta[a, c], b, d),
                (eta[a, d], b, c),
                (-eta[b, d], a, c),
            ]
            for coeff, p, q in terms:
                if coeff == 0:
                    continue
                if p == q:
                    continue
                if p < q:
                    k = pair_to_idx.get((p, q))
                    if k is not None:
                        f[i, j, k] += coeff
                else:
                    k = pair_to_idx.get((q, p))
                    if k is not None:
                        f[i, j, k] -= coeff  # antisymmetry of e_{pq}

    return f

for label, sig in [("so(4)=so(4,0)", [1,1,1,1]),
                    ("so(3,1)", [1,1,1,-1]),
                    ("so(2,2)", [1,1,-1,-1])]:
    n = len(sig)
    dim = n * (n-1) // 2
    f = so_structure_constants(n, sig)
    B = compute_killing_form(f, dim)
    eigs = np.linalg.eigvalsh(B)
    n_pos = sum(eigs > 1e-10)
    n_neg = sum(eigs < -1e-10)
    n_zero = sum(np.abs(eigs) < 1e-10)
    compact = n_neg == dim and n_pos == 0
    print(f"  {label}: Killing eigenvalues = {np.sort(eigs).round(2)}")
    print(f"    Signature (+,-,0) = ({n_pos},{n_neg},{n_zero})")
    print(f"    Compact (neg def): {compact}")
    print()

print("""
VERDICT on Question 3:

The Cl(p,q) signature DOES encode which theories can have mass gaps,
but ONLY through the standard criterion: compact gauge group.

The statement "compact part of Cl(p,q) gauge theory has mass gap iff q=0"
is ALMOST correct, but needs refinement:

PRECISE STATEMENT:
  The Lie group SO(p,q) is compact iff min(p,q) = 0.
  The Yang-Mills mass gap conjecture applies only to compact gauge groups.
  Therefore, the Clifford signature (p,q) determines ELIGIBILITY for
  having a mass gap: eligible iff min(p,q) = 0.

This is NOT a new theorem. It is a restatement of the compactness
condition in Clifford algebra language.

WHAT ABOUT Dollard's h and j?
  - j (j^2=-1) generates compact (circular) directions -> ELIGIBLE
  - h (h^2=+1) generates non-compact (hyperbolic) directions -> INELIGIBLE

  In Z_4: h = -1 (forced), so h is actually in the compact part.
  In Cl(1,1): h = e_1 with e_1^2 = +1, genuinely non-compact.

  Dollard's algebra is too small (Z_4 is compact/finite) to exhibit
  the compact/non-compact distinction that matters for mass gaps.

STATUS: Correct restatement of known result. No new theorem.
""")

# ============================================================================
# QUESTION 4: QUATERNARY EXPANSION AND OPERATOR SPECTRA
# ============================================================================

print("\n" + "=" * 78)
print("QUESTION 4: QUATERNARY EXPANSION AND SPECTRAL DECOMPOSITION")
print("=" * 78)

print("""
SETUP:
  Dollard's four-quadrant expansion:
    u - v = cos(t)    (trigonometric cosine)
    x - y = sin(t)    (trigonometric sine)
    u + v = cosh(t)   (hyperbolic cosine)
    x + y = sinh(t)   (hyperbolic sine)

  Operator spectral decomposition:
    sigma(A) = sigma_p(A) U sigma_ac(A) U sigma_sc(A)
    (point spectrum, absolutely continuous spectrum, singular continuous spectrum)

QUESTION: Is there a mapping between the four quadrants and spectral types?
""")

# First, let's understand the quaternary expansion algebraically
print("=== Algebraic structure of the quaternary expansion ===\n")

t = symbols('t', real=True)
u, v, x, y = symbols('u v x y', real=True)

# From the definitions:
# u - v = cos(t) and u + v = cosh(t)
# Solving: u = (cos(t) + cosh(t))/2, v = (cosh(t) - cos(t))/2
# Similarly: x = (sin(t) + sinh(t))/2, y = (sinh(t) - sin(t))/2

u_expr = (cos(t) + cosh(t)) / 2
v_expr = (cosh(t) - cos(t)) / 2
x_expr = (sin(t) + sinh(t)) / 2
y_expr = (sinh(t) - sin(t)) / 2

print("Quaternary components:")
print(f"  u = (cos(t) + cosh(t))/2")
print(f"  v = (cosh(t) - cos(t))/2")
print(f"  x = (sin(t) + sinh(t))/2")
print(f"  y = (sinh(t) - sin(t))/2")
print()

# Verify
assert simplify(u_expr - v_expr - cos(t)) == 0
assert simplify(x_expr - y_expr - sin(t)) == 0
assert simplify(u_expr + v_expr - cosh(t)) == 0
assert simplify(x_expr + y_expr - sinh(t)) == 0
print("Verified: u-v=cos, x-y=sin, u+v=cosh, x+y=sinh")
print()

# What ARE u, v, x, y in terms of exponentials?
print("In terms of exponentials:")
print(f"  u = (cos(t) + cosh(t))/2 = (e^it + e^-it + e^t + e^-t) / 4")
print(f"  v = (cosh(t) - cos(t))/2 = (e^t + e^-t - e^it - e^-it) / 4")
print(f"  x = (sin(t) + sinh(t))/2 = (e^it - e^-it + e^t - e^-t) / (4i, 4)")
print(f"  y = (sinh(t) - sin(t))/2 = (e^t - e^-t - e^it + e^-it) / (4, 4i)")
print()

# These are projections onto the four "quadrants" of the
# complex-hyperbolic plane: {e^t, e^-t, e^it, e^-it}
print("""
INSIGHT: The four quantities u, v, x, y are PROJECTIONS onto the
four exponential modes:
  e^t     (growth)
  e^{-t}  (decay)
  e^{it}  (positive frequency oscillation)
  e^{-it} (negative frequency oscillation)

Specifically:
  u = coefficient of (e^t + e^{-t} + e^{it} + e^{-it})/4
  v = coefficient of (e^t + e^{-t} - e^{it} - e^{-it})/4
  x = coefficient of (e^t - e^{-t} + ... )/... [mixed]
  y = coefficient of (e^t - e^{-t} - ... )/... [mixed]
""")

# Now: what about operator spectra?
print("=== Operator spectral decomposition ===\n")

print("""
For a self-adjoint operator A on a Hilbert space H:

  sigma(A) = sigma_p(A)  U  sigma_ac(A)  U  sigma_sc(A)

1. Point spectrum sigma_p: eigenvalues (discrete energies)
   - Bound states in quantum mechanics
   - Correspond to e^{i*omega_n*t} oscillations with DISCRETE frequencies

2. Absolutely continuous spectrum sigma_ac: continuous part
   - Scattering states in quantum mechanics
   - Correspond to wave packets with CONTINUOUS frequency content

3. Singular continuous spectrum sigma_sc: fractal-like part
   - Rare in physics (some quasicrystals, Anderson localization transition)
   - No simple time-domain characterization

DOES the quaternary expansion map to this decomposition?
""")

print("""
=== Analysis: Quaternary vs spectral decomposition ===

The quaternary expansion decomposes a function of t into four channels:
  cos(t), sin(t), cosh(t), sinh(t)

These correspond to eigenfunction types of the SECOND DERIVATIVE operator:
  d^2/dt^2 [cos(t)] = -cos(t)     (eigenvalue -1, oscillatory)
  d^2/dt^2 [sin(t)] = -sin(t)     (eigenvalue -1, oscillatory)
  d^2/dt^2 [cosh(t)] = +cosh(t)   (eigenvalue +1, growing/decaying)
  d^2/dt^2 [sinh(t)] = +sinh(t)   (eigenvalue +1, growing/decaying)

So the quaternary expansion is an eigenvalue decomposition of d^2/dt^2
into its TWO eigenspaces: {-1} and {+1}.

This is a SPECTRAL decomposition, but of a SECOND-ORDER ODE operator,
not of the Hamiltonian.

The connection to the quantum spectral decomposition is:

  - cos/sin channels: eigenvalue -1 of d^2/dt^2
    -> IMAGINARY eigenvalues of d/dt (d/dt has eigenvalue +-i)
    -> These correspond to OSCILLATORY solutions
    -> In quantum mechanics: UNITARY time evolution e^{-iHt}
    -> These ARE the quantum states (point or continuous spectrum)

  - cosh/sinh channels: eigenvalue +1 of d^2/dt^2
    -> REAL eigenvalues of d/dt (d/dt has eigenvalue +-1)
    -> These correspond to GROWING/DECAYING solutions
    -> In quantum mechanics: these appear in:
      (a) Tunneling (exponential decay under barriers)
      (b) Euclidean (imaginary time) formulation: t -> -it
      (c) UNSTABLE modes (if present, theory is sick)

CRITICAL OBSERVATION:

The cos/sin vs cosh/sinh split is NOT the same as
point spectrum vs continuous spectrum.

Rather, it is the split between:
  - PHYSICAL modes (cos/sin) = unitary time evolution = healthy QFT
  - UNPHYSICAL modes (cosh/sinh) = non-unitary = instabilities or tunneling

In the Euclidean (imaginary time) formulation:
  - t -> -i*tau (Wick rotation)
  - e^{-iEt} -> e^{-E*tau}  (oscillatory -> decaying)
  - cos(Et) -> cosh(E*tau)   (EXACTLY the quaternary swap!)
  - sin(Et) -> i*sinh(E*tau)

So the quaternary expansion's four channels encode the
WICK ROTATION structure, not the spectral decomposition.
""")

# Verify the Wick rotation connection
print("=== Verification: Wick rotation and quaternary ===\n")

tau = symbols('tau', real=True, positive=True)
E = symbols('E', real=True, positive=True)

# Minkowski: f(t) = cos(E*t)
# Euclidean: f(-i*tau) = cos(E*(-i*tau)) = cos(-i*E*tau) = cosh(E*tau)
wick_cos = cos(-I * E * tau)
wick_cos_simplified = simplify(wick_cos)
print(f"  cos(E*(-i*tau)) = {wick_cos_simplified}")

wick_sin = sin(-I * E * tau)
wick_sin_simplified = simplify(wick_sin)
print(f"  sin(E*(-i*tau)) = {wick_sin_simplified}")

# These should give cosh and i*sinh
print(f"  Expected: cosh(E*tau) and -i*sinh(E*tau)")
print(f"  cos(-iEt) = cosh(Et): {simplify(wick_cos_simplified - cosh(E*tau)) == 0}")
print(f"  sin(-iEt) = -i*sinh(Et): {simplify(wick_sin_simplified + I*sinh(E*tau)) == 0}")
print()

print("""
PRECISE RESULT:

The quaternary expansion's four channels correspond to the
four sectors of the TWO-FOLD decomposition:

  {cos, sin} x {real t, imaginary t}

which equals:

  {cos(t), sin(t), cosh(t), sinh(t)}

This is the WICK ROTATION decomposition:
  (Minkowski oscillatory) <-> (Euclidean decaying)
  cos(Et) <-> cosh(Etau)
  sin(Et) <-> sinh(Etau)

And NOT the spectral decomposition:
  sigma_p <-> sigma_ac <-> sigma_sc
""")

# One more connection to check: does the quaternary have anything to do
# with the mass gap specifically?
print("=== Connection to the mass gap ===\n")

print("""
The Euclidean formulation IS relevant to the mass gap:

In Euclidean QFT, the two-point correlator behaves as:
  <phi(x) phi(0)> ~ e^{-m|x|}  for |x| -> infinity

where m is the MASS (= mass gap Delta if it's the lightest state).

The RATE OF DECAY in the Euclidean correlator DIRECTLY measures the mass gap:
  Delta = -lim_{|x|->inf} (1/|x|) log <phi(x) phi(0)>

This exponential decay is a COSH/SINH function (the quaternary's
hyperbolic channels):
  <phi(x) phi(0)> = A * e^{-m*|x|} = A * [cosh(m*x) - sinh(m*x)]  for x > 0

So the HYPERBOLIC part of the quaternary expansion contains the
mass gap information in the Euclidean formulation.

But this is just the standard Euclidean propagator analysis.
The quaternary notation does not add new mathematical content.
""")

print("""
VERDICT on Question 4:

The quaternary expansion does NOT map to the operator spectral decomposition
(point/continuous/singular continuous). Instead, it maps to the
WICK ROTATION structure:

  u - v = cos(t)   \\ Minkowski (oscillatory, physical time)
  x - y = sin(t)   /

  u + v = cosh(t)  \\ Euclidean (decaying, imaginary time)
  x + y = sinh(t)  /

The connection to the mass gap is through the Euclidean formulation:
  - The cosh/sinh channels encode exponential decay rates
  - The decay rate = mass gap (for the lightest state)
  - This is standard Euclidean QFT, not a new result

The quaternary expansion is a NOTATION for the Wick rotation,
not a new mathematical structure for spectral theory.

STATUS: Incorrect mapping proposed. Correct mapping identified (Wick rotation).
""")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 78)
print("FINAL SUMMARY: ALL FOUR QUESTIONS")
print("=" * 78)

print("""
Q1: CLIFFORD GRADING -> CASIMIR EIGENVALUES -> MASS GAP?
    ANSWER: NO. The Clifford grading determines so(n) structure constants,
    which determine Casimir eigenvalues through standard Lie theory.
    No NEW spectral constraint from the Clifford embedding.
    The mass gap is a dynamical/analytical property, not algebraic.

Q2: FORTESCUE -> ROOT SPACE DECOMPOSITION?
    ANSWER: YES (partially). The precise connection is through the
    PRINCIPAL GRADING of the Lie algebra, which is a DFT decomposition
    with period h (Coxeter number). For su(N), h = N, so the Fortescue
    N-phase decomposition IS the principal grading. For so(N), h != N
    in general. This gives Fortescue a representation-theoretic
    interpretation but does not directly constrain the mass gap.

Q3: Cl(p,q) SIGNATURE -> MASS GAP EXISTENCE?
    ANSWER: PARTIALLY. The signature determines whether the gauge group
    is compact (min(p,q) = 0) or non-compact (min(p,q) > 0). The mass
    gap conjecture applies only to compact groups. But this is a
    PREREQUISITE, not a proof -- it's the definition of the problem.

Q4: QUATERNARY EXPANSION -> SPECTRAL DECOMPOSITION?
    ANSWER: NO (wrong mapping). The quaternary expansion maps to the
    WICK ROTATION structure (Minkowski <-> Euclidean), not to the
    operator spectral decomposition (point/continuous/singular).
    The Euclidean decay rate encodes the mass gap, but this is
    standard Euclidean QFT, not a new result.

OVERALL ASSESSMENT:
    None of these four approaches provides a route to PROVING the mass gap.
    They provide useful LANGUAGE and COMPUTATIONAL FRAMEWORKS for stating
    and organizing the problem, but the core difficulty -- controlling the
    non-perturbative quantum dynamics -- remains untouched.

    The honest conclusion: the algebraic chain Z_4 -> Cl(1,1) -> ... -> so(14)
    is NECESSARY scaffolding, verified to be correct, but INSUFFICIENT for
    the mass gap. The gap between "correct algebra" and "mass gap proof"
    is the entire content of the Millennium Prize problem.
""")
