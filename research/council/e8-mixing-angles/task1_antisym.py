import numpy as np
import math

print("TASK 1: [84,84] -> 84* Antisymmetric Coupling Analysis")
print("="*60)

# Under SU(5) x SU(4):
# 84 = Lambda^3(C^9):
#   p=3: Lambda^3(C^5) x 1 = (10-bar, 1), dim 10
#   p=2: Lambda^2(C^5) x C^4 = (10, 4), dim 40
#   p=1: C^5 x Lambda^2(C^4) = (5, 6), dim 30
#   p=0: 1 x Lambda^3(C^4) = (1, 4-bar), dim 4
# Total: 10+40+30+4=84

# 84* = Lambda^6(C^9):
#   p=2: Lambda^2(C^5) x Lambda^4(C^4) = (10, 1), dim 10
#   p=3: Lambda^3(C^5) x Lambda^3(C^4) = (10-bar, 4-bar), dim 40
#   p=4: Lambda^4(C^5) x Lambda^2(C^4) = (5-bar, 6), dim 30
#   p=5: Lambda^5(C^5) x Lambda^1(C^4) = (1, 4), dim 4
# Total: 10+40+30+4=84

print("Wedge product channels Lambda^3 ^ Lambda^3 -> Lambda^6:")
print()

# Factor 1 has p1 SU(5) + (3-p1) SU(4) indices
# Factor 2 has p2 SU(5) + (3-p2) SU(4) indices
# Result: (p1+p2) SU(5) + (6-p1-p2) SU(4) indices
# Need: 0 <= p1+p2 <= 5 and 0 <= 6-p1-p2 <= 4

channels = []
for p1 in range(4):  # 0,1,2,3
    for p2 in range(p1, 4):  # avoid double counting
        p_out = p1 + p2
        q_out = 6 - p_out
        if p_out > 5 or q_out > 4 or q_out < 0:
            continue

        su5_reps_in = {0: "(1", 1: "(5", 2: "(10", 3: "(10-bar"}
        su4_reps_in = {0: ",1)", 1: ",4)", 2: ",6)", 3: ",4-bar)"}
        su5_reps_out = {2: "10", 3: "10-bar", 4: "5-bar", 5: "1"}
        su4_reps_out = {0: "1*", 1: "4", 2: "6", 3: "4-bar", 4: "1"}

        in1 = su5_reps_in[p1] + su4_reps_in[3-p1]
        in2 = su5_reps_in[p2] + su4_reps_in[3-p2]
        out_s = "(%s, %s)" % (su5_reps_out.get(p_out,"?"), su4_reps_out.get(q_out,"?"))

        sym = "antisym" if p1 == p2 else "both orders"
        channels.append((in1, in2, out_s, p1, p2, q_out, sym))
        print("  %s x %s -> %s  [SU5: %d+%d=%d, SU4: %d] (%s)" %
              (in1, in2, out_s, p1, p2, p_out, q_out, sym))

print()
print("Generation space (SU(3) inside SU(4)) analysis:")
print("  SU(4) -> SU(3)_fam x U(1):")
print("  4 -> 3_i + 1  (i=1,2,3 generations)")
print("  6 -> 3-bar + 3")
print("  4-bar -> 3-bar + 1")
print()

# KEY channel: (10,4) x (10,4) -> (5-bar,6)
# SU(4): 4 ^ 4 -> Lambda^2(4) = 6
# Under SU(3): (3+1) ^ (3+1) = Lambda^2(3) + 3^1 = 3-bar + 3
# The 3_i ^ 3_j part -> 3-bar_k via epsilon_{ijk}
# The 3_i ^ 1 part -> 3_i (a different component of the 6)

print("Channel (10,4) x (10,4) -> (5-bar, 6):")
print("  SU(4) contraction: 4_i ^ 4_j -> 6_{ij}")
print("  Generation indices i,j in {1,2,3}:")
print("  3_i ^ 3_j = epsilon_{ijk} * (3-bar)_k")
print("  This is COMPLETELY DETERMINED: the Levi-Civita tensor.")
print()

# Build the 3x3 effective mass matrix from epsilon tensor
print("Effective mass matrix from epsilon coupling:")
print("  If 84* VEV in (5-bar, 6) direction, with SU(3) component phi_k:")
print("  M_{ij} = g * epsilon_{ijk} * phi_k")
print()

for desc, phi in [("phi=(0,0,1)", [0,0,1]),
                  ("phi=(1,0,0)", [1,0,0]),
                  ("phi=(1,1,1)/sqrt3", [1/math.sqrt(3)]*3)]:
    M = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)]:
                    M[i,j] += phi[k]
                elif (i,j,k) in [(0,2,1),(2,1,0),(1,0,2)]:
                    M[i,j] -= phi[k]
    evals = np.sort(np.real(np.linalg.eigvals(M)))
    print("  %s:" % desc)
    print("    M = ")
    for row in M:
        print("      [%s]" % ", ".join("%.4f" % x for x in row))
    print("    eigenvalues = [%s]" % ", ".join("%.4f" % x for x in evals))
    print("    NOTE: det(M) = 0 always (3x3 antisymmetric -> one zero eigenvalue)")
    print()

# Combined: Y = y*I + g*A
print("="*60)
print("COMBINED texture: Y = y*I + g*A(phi)")
print("  I = identity (from [84,84*]->80, symmetric coupling)")
print("  A_{ij} = epsilon_{ijk}*phi_k (from [84,84]->84*, antisymmetric)")
print()

phi = np.array([0, 0, 1.0])
A = np.zeros((3,3))
for i in range(3):
    for j in range(3):
        for k in range(3):
            if (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)]:
                A[i,j] += phi[k]
            elif (i,j,k) in [(0,2,1),(2,1,0),(1,0,2)]:
                A[i,j] -= phi[k]

for y_val, g_val in [(5.0, 1.0), (5.0, 0.5), (1.0, 0.3)]:
    Y = y_val * np.eye(3) + g_val * A
    evals = np.sort(np.abs(np.linalg.eigvals(Y)))
    print("  y=%.1f, g=%.1f, phi=(0,0,1):" % (y_val, g_val))
    print("    Y = ")
    for row in Y:
        print("      [%s]" % ", ".join("%.3f" % x for x in row))
    print("    |eigenvalues| = [%s]" % ", ".join("%.4f" % x for x in evals))
    print("    mass ratios: [%s]" % ", ".join("%.4f" % x for x in evals/evals.max()))

    # The eigenvalues of y*I + g*A where A is antisymmetric with eigenvalues (ia, -ia, 0):
    # are y+ig*a, y-ig*a, y. So |eigenvalues| = sqrt(y^2+g^2*a^2), sqrt(y^2+g^2*a^2), y.
    # TWO masses are DEGENERATE! Only the third is different.
    # This means: NO CKM mixing from this texture alone (two degenerate states).
    print("    NOTE: Two eigenvalues are degenerate (|y+ig|=|y-ig|=sqrt(y^2+g^2))")
    print("    The antisymmetric part does NOT split the degeneracy!")
    print("    To get 3 different masses, need ADDITIONAL breaking.")
    print()

print("="*60)
print("CRITICAL FINDING:")
print("  Y = y*I + g*A has eigenvalues sqrt(y^2+g^2), sqrt(y^2+g^2), y")
print("  Two masses are ALWAYS degenerate.")
print("  This gives:")
print("    - 2 degenerate heavy generations + 1 light generation (if g > 0)")
print("    - Or 1 heavy + 2 degenerate light (depending on sign convention)")
print("  To get 3 distinct masses: need BOTH up and down sectors with")
print("  different y and g values, OR need SU(3)_fam breaking VEV.")
print()
print("  For CKM mixing: need Y_u != Y_d. Even with antisymmetric part,")
print("  each sector individually has a 2-fold degeneracy. The CKM matrix")
print("  from two degenerate-pair textures has limited structure.")
print()

# Check if up and down sectors with different parameters give CKM mixing
print("CKM from two sectors:")
y_u, g_u = 5.0, 1.0
y_d, g_d = 3.0, 0.5
Y_u = y_u * np.eye(3) + g_u * A
Y_d = y_d * np.eye(3) + g_d * A

# Diagonalize
eval_u, evec_u = np.linalg.eigh(Y_u @ Y_u.T)
eval_d, evec_d = np.linalg.eigh(Y_d @ Y_d.T)

# CKM = V_u^dag V_d
V_ckm = evec_u.T @ evec_d
print("  Y_u: y=%.1f, g=%.1f; Y_d: y=%.1f, g=%.1f" % (y_u, g_u, y_d, g_d))
print("  V_CKM = ")
for row in np.abs(V_ckm):
    print("    [%s]" % ", ".join("%.4f" % x for x in row))
print("  Note: since both use SAME phi direction, V_CKM = I")
print("  (same diagonalization basis). Need DIFFERENT phi for u vs d sectors.")
print()

# With different phi directions:
phi_u = np.array([0, 0, 1.0])
phi_d = np.array([0.5, 0.5, 1.0/math.sqrt(2)])  # different direction
A_u = np.zeros((3,3))
A_d = np.zeros((3,3))
for i in range(3):
    for j in range(3):
        for k in range(3):
            eps = 0
            if (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)]: eps = 1
            elif (i,j,k) in [(0,2,1),(2,1,0),(1,0,2)]: eps = -1
            A_u[i,j] += eps * phi_u[k]
            A_d[i,j] += eps * phi_d[k]

Y_u2 = y_u * np.eye(3) + g_u * A_u
Y_d2 = y_d * np.eye(3) + g_d * A_d

eval_u2, evec_u2 = np.linalg.eigh(Y_u2 @ Y_u2.T)
eval_d2, evec_d2 = np.linalg.eigh(Y_d2 @ Y_d2.T)
V_ckm2 = evec_u2.T @ evec_d2

print("  With DIFFERENT phi directions:")
print("  V_CKM = ")
for row in np.abs(V_ckm2):
    print("    [%s]" % ", ".join("%.4f" % x for x in row))
print("  NOW we get non-trivial mixing!")
print("  BUT: the phi directions are dynamical (VEV alignment), not geometric.")
print()

print("="*60)
print("FINAL VERDICT on Task 1:")
print("="*60)
print()
print("1. The [84,84]->84* coupling IS non-trivial in generation space.")
print("   Structure: M_{ij} = epsilon_{ijk} * phi_k (Levi-Civita tensor)")
print()
print("2. Combined with [84,84*]->80 (identity): Y = y*I + g*A")
print("   This has eigenvalues sqrt(y^2+g^2), sqrt(y^2+g^2), y")
print("   TWO masses are always degenerate.")
print()
print("3. CKM mixing requires DIFFERENT phi directions for up and down.")
print("   The relative orientation of phi_u and phi_d determines mixing.")
print("   This is a DYNAMICAL choice (VEV alignment), not geometric.")
print()
print("4. The texture Y = y*I + g*A is more RESTRICTIVE than generic SU(3)")
print("   models. It has only 2 parameters per sector instead of 6.")
print("   But the 2-fold degeneracy is a problem for realistic phenomenology.")
print()
print("5. To break the degeneracy: need additional Higgs fields or")
print("   non-perturbative SU(3)_fam effects. The E8 structure alone")
print("   is insufficient for realistic fermion masses.")
print()
print("CLASSIFICATION: NEUTRAL")
print("  The epsilon tensor coupling exists and is non-trivial,")
print("  but the 2-fold mass degeneracy and VEV dependence mean")
print("  it does not provide geometric mixing angles.")
print("  It constrains the texture more than previously recognized,")
print("  but falls short of determining mixing.")
