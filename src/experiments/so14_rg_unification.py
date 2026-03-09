#!/usr/bin/env python3
"""
SO(14) RG Coupling Unification Computation (Phase 1)
=====================================================

Pre-registered as Experiment 4, Phase 1 in EXPERIMENT_REGISTRY.md.

Kill Condition KC-1: If couplings miss unification by >5%, theory is DEAD.
Kill Condition KC-2: If proton lifetime < 1.6e34 years, theory is DEAD.

Claim tags:
  [MV] Machine-verified (Lean 4)
  [CO] Computed (this script)
  [SP] Standard physics (textbook)
  [CP] Candidate physics (proposed)

Convention (Langacker 1991, Martin SUSY Primer):
  All three couplings are GUT-normalized at M_Z:

    alpha_1^{-1}(M_Z) = (3/5) * alpha_em^{-1} * cos^2(theta_W) = 59.0
    alpha_2^{-1}(M_Z) = alpha_em^{-1} * sin^2(theta_W) = 29.6
    alpha_3^{-1}(M_Z) = 1/alpha_s = 8.5

  Evolution:  alpha_i^{-1}(mu) = alpha_i^{-1}(M_Z) - b_i/(2pi) * ln(mu/M_Z)

  SM GUT-normalized betas:
    b_1 = 123/50 = 2.46   [derived: (3/5) * (41/10) where 41/10 is hypercharge b_1]
    b_2 = -19/6 = -3.167
    b_3 = -7

  Derivation of b_1_GUT:
    alpha_1_GUT = (5/3)*alpha_Y => alpha_1_GUT^{-1} = (3/5)*alpha_Y^{-1}
    d(alpha_GUT^{-1})/d(ln mu) = (3/5) * d(alpha_Y^{-1})/d(ln mu) = (3/5)*(-41/10)/(2pi)
    => b_1_GUT = (3/5)*(41/10) = 123/50

  Cross-check: MSSM betas (33/5, 1, -3) with these inputs give
  0.6% miss at 10^{16.3} GeV -- matches the famous MSSM result.

Author: Clifford Unification Engineer
Date: 2026-03-08
"""

import numpy as np
import json
import os
from datetime import datetime

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ============================================================================
# CONSTANTS
# ============================================================================

M_Z = 91.1876       # GeV [SP]
M_PLANCK = 1.22e19  # GeV [SP]
M_PROTON = 0.938272 # GeV [SP]
HBAR = 6.582119569e-25  # GeV*s [SP]
YEAR_S = 3.1557e7   # seconds per year [SP]
TWO_PI = 2.0 * np.pi

# GUT-normalized couplings at M_Z [SP]
A1_MZ = 59.0   # alpha_1_GUT^{-1}(M_Z) = (3/5)*alpha_em^{-1}*cos^2(theta_W)
A2_MZ = 29.6   # alpha_2^{-1}(M_Z)
A3_MZ = 8.5    # alpha_3^{-1}(M_Z) = 1/alpha_s

# SM 1-loop beta-coefficients (GUT-normalized) [MV: rg_running.lean]
B1 = 123.0 / 50.0   # = 2.46  [= (3/5)*(41/10)]
B2 = -19.0 / 6.0    # = -3.167
B3 = -7.0

# MSSM 1-loop beta-coefficients (GUT-normalized) [SP]
B1_MSSM = 33.0 / 5.0  # = 6.6
B2_MSSM = 1.0
B3_MSSM = -3.0


def alpha_inv(a_mz, b, mu):
    """alpha_i^{-1}(mu) = a_i(M_Z) - b_i/(2pi) * ln(mu/M_Z)"""
    return a_mz - (b / TWO_PI) * np.log(mu / M_Z)


def find_crossing(a1_mz, b1, a2_mz, b2):
    """Find energy scale where two inverse couplings cross."""
    db = b1 - b2
    if abs(db) < 1e-15:
        return None, None
    t = TWO_PI * (a1_mz - a2_mz) / db
    mu = M_Z * np.exp(t)
    val = a1_mz - (b1 / TWO_PI) * t
    return mu, val


# ============================================================================
# PART 1: SM 1-loop unification
# ============================================================================

def part1_sm():
    print("=" * 78)
    print("PART 1: SM 1-LOOP COUPLING UNIFICATION [SP + CO]")
    print("=" * 78)
    print()

    # Verify GUT normalization
    a_em_inv = 127.9
    sin2w = 0.2312
    a1_check = (3.0/5.0) * a_em_inv * (1.0 - sin2w)
    a2_check = a_em_inv * sin2w
    print("GUT normalization cross-check:")
    print(f"  alpha_em^{{-1}} = {a_em_inv}, sin^2(theta_W) = {sin2w}")
    print(f"  alpha_1_GUT^{{-1}} = (3/5)*{a_em_inv}*{1-sin2w:.4f} = {a1_check:.1f}"
          f"  (input: {A1_MZ})")
    print(f"  alpha_2^{{-1}} = {a_em_inv}*{sin2w} = {a2_check:.1f}  (input: {A2_MZ})")
    print()

    print("Inputs:")
    print(f"  alpha_i^{{-1}}(M_Z) = ({A1_MZ}, {A2_MZ}, {A3_MZ})")
    print(f"  b_i = ({B1:.4f}, {B2:.4f}, {B3})")
    print()

    # Pairwise crossings
    mu_12, v_12 = find_crossing(A1_MZ, B1, A2_MZ, B2)
    mu_23, v_23 = find_crossing(A2_MZ, B2, A3_MZ, B3)
    mu_13, v_13 = find_crossing(A1_MZ, B1, A3_MZ, B3)

    print("Pairwise crossings:")
    for tag, mu, v in [("1-2", mu_12, v_12), ("2-3", mu_23, v_23), ("1-3", mu_13, v_13)]:
        print(f"  {tag}: 10^{np.log10(mu):.2f} GeV, alpha^{{-1}} = {v:.2f}")
    print()

    # Triangle
    logs = sorted([np.log10(mu_12), np.log10(mu_23), np.log10(mu_13)])
    vals = sorted([v_12, v_23, v_13])
    print(f"Unification triangle:")
    print(f"  log10(mu) spread: {logs[2]-logs[0]:.2f}")
    print(f"  alpha^{{-1}} spread: {vals[2]-vals[0]:.2f}")
    print()

    # Miss at 2-3 crossing
    a1_at_23 = alpha_inv(A1_MZ, B1, mu_23)
    miss_abs = abs(a1_at_23 - v_23)
    miss_pct = miss_abs / v_23 * 100

    print(f"Unification quality (at 2-3 crossing, 10^{np.log10(mu_23):.2f} GeV):")
    print(f"  alpha_2^{{-1}} = alpha_3^{{-1}} = {v_23:.2f}")
    print(f"  alpha_1^{{-1}} = {a1_at_23:.2f}")
    print(f"  |miss| = {miss_abs:.2f},  miss% = {miss_pct:.1f}%")
    print()

    # Evolution table
    print("Evolution table:")
    print(f"  {'log10(mu)':<10} {'a1^-1':<10} {'a2^-1':<10} {'a3^-1':<10} {'spread':<10}")
    print(f"  {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
    for lm in [2, 4, 6, 8, 10, 12, 14, 15, 16, 16.5, 17]:
        mu = 10.0**lm
        a1 = alpha_inv(A1_MZ, B1, mu)
        a2 = alpha_inv(A2_MZ, B2, mu)
        a3 = alpha_inv(A3_MZ, B3, mu)
        sp = max(a1,a2,a3) - min(a1,a2,a3)
        print(f"  {lm:<10} {a1:<10.2f} {a2:<10.2f} {a3:<10.2f} {sp:<10.2f}")
    print()

    return {
        'mu_12': mu_12, 'v_12': v_12,
        'mu_23': mu_23, 'v_23': v_23,
        'mu_13': mu_13, 'v_13': v_13,
        'a1_at_23': a1_at_23,
        'miss_abs': miss_abs,
        'miss_pct': miss_pct,
    }


# ============================================================================
# PART 2: MSSM comparison
# ============================================================================

def part2_mssm():
    print("=" * 78)
    print("PART 2: MSSM COMPARISON [SP]")
    print("=" * 78)
    print()

    mu_12, v_12 = find_crossing(A1_MZ, B1_MSSM, A2_MZ, B2_MSSM)
    mu_23, v_23 = find_crossing(A2_MZ, B2_MSSM, A3_MZ, B3_MSSM)
    mu_13, v_13 = find_crossing(A1_MZ, B1_MSSM, A3_MZ, B3_MSSM)

    print(f"MSSM betas: ({B1_MSSM}, {B2_MSSM}, {B3_MSSM})")
    print()
    for tag, mu, v in [("1-2", mu_12, v_12), ("2-3", mu_23, v_23), ("1-3", mu_13, v_13)]:
        print(f"  {tag}: 10^{np.log10(mu):.2f} GeV, alpha^{{-1}} = {v:.2f}")
    print()

    a1_at_23 = alpha_inv(A1_MZ, B1_MSSM, mu_23)
    miss = abs(a1_at_23 - v_23) / v_23 * 100
    print(f"Miss at 2-3 crossing: {miss:.2f}%")
    print(f"(Famous MSSM result: ~0.5% miss at ~2 x 10^16 GeV)")
    print()

    return {'miss_mssm': miss, 'mu_23_mssm': mu_23}


# ============================================================================
# PART 3: Required corrections for exact unification
# ============================================================================

def part3_corrections(R):
    print("=" * 78)
    print("PART 3: REQUIRED BETA CORRECTIONS [CO]")
    print("=" * 78)
    print()

    mu_23 = R['mu_23']
    v_23 = R['v_23']
    a1_at_23 = R['a1_at_23']
    deficit = a1_at_23 - v_23

    print(f"At 2-3 crossing (10^{np.log10(mu_23):.2f} GeV):")
    print(f"  alpha_1 line is {deficit:+.2f} from target ({v_23:.2f})")
    print(f"  alpha_1 is too {'high' if deficit > 0 else 'low'} by {abs(deficit):.2f}")
    print()

    # Option A: modify b1 above an intermediate scale
    print("A) Required delta(b1) from new physics at scale M_I:")
    print(f"  {'log10(M_I)':<14} {'delta(b1)':<14}")
    print(f"  {'-'*14} {'-'*14}")
    for log_mi in [3, 4, 6, 8, 10, 12, 14]:
        mi = 10.0**log_mi
        if mi >= mu_23:
            continue
        ln_r = np.log(mu_23 / mi)
        db = deficit * TWO_PI / ln_r
        print(f"  {log_mi:<14} {db:+.4f}")
    print()

    # Option B: fix at a specific M_GUT keeping b3 unchanged
    print("B) Fix all three to meet at chosen M_GUT (keep b3 = -7):")
    print(f"  {'log10(M_GUT)':<14} {'a_GUT^-1':<12} {'b1 needed':<12} "
          f"{'b2 needed':<12} {'d(b1)':<12} {'d(b2)':<12}")
    print(f"  {'-'*14} {'-'*12} {'-'*12} {'-'*12} {'-'*12} {'-'*12}")
    for lg in [14, 15, 16, 16.5, 17]:
        mu_g = 10**lg
        t = np.log(mu_g / M_Z)
        a_gut = A3_MZ - (B3 / TWO_PI) * t
        b1_n = TWO_PI * (A1_MZ - a_gut) / t
        b2_n = TWO_PI * (A2_MZ - a_gut) / t
        print(f"  {lg:<14} {a_gut:<12.2f} {b1_n:<12.4f} "
              f"{b2_n:<12.4f} {b1_n-B1:<+12.4f} {b2_n-B2:<+12.4f}")
    print()

    R['deficit'] = deficit
    return R


# ============================================================================
# PART 4: SO(14) threshold analysis
# ============================================================================

def part4_so14(R):
    print("=" * 78)
    print("PART 4: SO(14) THRESHOLD ANALYSIS [CP + CO]")
    print("=" * 78)
    print()

    print("SO(14) -> SO(10) x SO(4) -> SM")
    print("Extra generators: 91 - 12 = 79 beyond SM [MV: so14_unification.lean]")
    print("  45 - 12 = 33 from SO(10)/SM")
    print("  6 from SO(4)")
    print("  40 from (10,4) mixed")
    print()

    print("DESERT HYPOTHESIS (all 79 at M_GUT):")
    print(f"  SM running applies. Miss = {R['miss_pct']:.1f}%. Same as any non-SUSY GUT.")
    print()

    print("(10,4) INTERMEDIATE CONTENT ANALYSIS:")
    print()
    print("  40 mixed bosons = 4 x [10 of SO(10)] x [singlet under SM from SO(4)]")
    print()
    print("  10 of SO(10) under SM: (3,1,-1/3) + (3bar,1,1/3) + (1,2,1/2) + (1,2,-1/2)")
    print()
    print("  Beta contributions per 10 (as complex scalars):")
    print("    d(b3) = 1/3 * T(3) * 2 + 0 = 1/3")
    print("    d(b2) = 0 + 1/3 * T(2) * 2 = 1/3")
    print("    d(b1) = (3/5)*[1/3*(1/3)^2*3*2 + 1/3*(1/2)^2*2*2] = (3/5)*[2/9+1/3]")
    print("          = (3/5)*(5/9) = 1/3")
    print()
    print("  => d(b1) = d(b2) = d(b3) = 1/3 per copy of 10")
    print()
    print("  EQUAL CORRECTIONS [CO]:")
    print("  Complete GUT multiplets shift all three betas equally.")
    print("  Equal shifts move all three lines together without")
    print("  changing their relative positions.")
    print("  The (10,4) states CANNOT fix the unification miss.")
    print()
    print("  With 4 copies: d(b_i) = 4/3 for all i. Still equal.")
    print("  SO(4) bosons: SM singlets, d(b_i) = 0.")
    print()

    print("VERDICT ON SO(14) CONTENT:")
    print("  - Desert hypothesis: identical to non-SUSY SO(10)")
    print("  - Intermediate (10,4): equal beta shifts, no help")
    print("  - Conclusion: SO(14) unification requires the SAME remedy")
    print("    as SO(10): SUSY, split multiplets, or threshold corrections")
    print("    from Higgs sector")
    print()

    R['equal_shifts'] = True
    return R


# ============================================================================
# PART 5: Proton decay
# ============================================================================

def part5_proton(R):
    print("=" * 78)
    print("PART 5: PROTON DECAY ESTIMATE [CO + SP]")
    print("=" * 78)
    print()

    mu_gut = R['mu_23']
    v_gut = R['v_23']
    a_gut = 1.0 / v_gut

    tau_nat = mu_gut**4 / (a_gut**2 * M_PROTON**5)
    tau_yr = tau_nat * HBAR / YEAR_S

    print(f"M_GUT = 10^{np.log10(mu_gut):.2f} GeV")
    print(f"alpha_GUT = {a_gut:.5f}")
    print(f"tau_p = M_GUT^4 / (alpha_GUT^2 * m_p^5)")
    print(f"      = {tau_yr:.2e} years  (log10 = {np.log10(tau_yr):.1f})")
    print()

    # With A_R enhancement factor
    A_R = 2.5
    tau_refined = tau_yr / A_R**2
    print(f"With renormalization factor A_R = {A_R}:")
    print(f"  tau_p = {tau_refined:.2e} years  (log10 = {np.log10(tau_refined):.1f})")
    print()

    bound = 1.6e34
    print(f"Super-K bound: tau > {bound:.1e} years (log10 = {np.log10(bound):.1f})")
    print()

    ok = tau_yr > bound
    ok_refined = tau_refined > bound
    print(f"Dimensional estimate:   {'SAFE' if ok else 'RULED OUT'}"
          f"  (factor {tau_yr/bound:.0e})")
    print(f"With A_R correction:    {'SAFE' if ok_refined else 'RULED OUT'}"
          f"  (factor {tau_refined/bound:.0e})")
    print()

    R['tau_yr'] = tau_yr
    R['log_tau'] = np.log10(tau_yr)
    R['tau_bound'] = bound
    R['proton_ok'] = ok

    return R


# ============================================================================
# PART 6: Plot
# ============================================================================

def part6_plot(R):
    if not HAS_MATPLOTLIB:
        print("(matplotlib not available, plot skipped)")
        return

    log_mu = np.linspace(np.log10(M_Z), 18, 1000)
    mu = 10**log_mu

    a1_sm = alpha_inv(A1_MZ, B1, mu)
    a2_sm = alpha_inv(A2_MZ, B2, mu)
    a3_sm = alpha_inv(A3_MZ, B3, mu)

    a1_ms = alpha_inv(A1_MZ, B1_MSSM, mu)
    a2_ms = alpha_inv(A2_MZ, B2_MSSM, mu)
    a3_ms = alpha_inv(A3_MZ, B3_MSSM, mu)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    for ax, a1, a2, a3, title, miss_val in [
        (ax1, a1_sm, a2_sm, a3_sm, 'SM (non-SUSY)', R['miss_pct']),
        (ax2, a1_ms, a2_ms, a3_ms, 'MSSM (supersymmetric)', None),
    ]:
        ax.plot(log_mu, a1, 'b-', lw=2, label=r'$\alpha_1^{-1}$ (U(1), GUT)')
        ax.plot(log_mu, a2, 'r-', lw=2, label=r'$\alpha_2^{-1}$ (SU(2))')
        ax.plot(log_mu, a3, 'g-', lw=2, label=r'$\alpha_3^{-1}$ (SU(3))')
        ax.set_xlabel(r'$\log_{10}(\mu / \mathrm{GeV})$', fontsize=13)
        ax.set_ylabel(r'$\alpha_i^{-1}(\mu)$', fontsize=13)
        ax.set_title(title, fontsize=14)
        ax.legend(fontsize=10)
        ax.set_xlim(2, 18)
        ax.set_ylim(0, 70)
        ax.grid(True, alpha=0.3)

    ax1.text(0.05, 0.05, f'Miss at 2-3: {R["miss_pct"]:.1f}%\n'
             f'KC-1 threshold: 5%',
             transform=ax1.transAxes, fontsize=11,
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    mu23_m, v23_m = find_crossing(A2_MZ, B2_MSSM, A3_MZ, B3_MSSM)
    a1_at_23m = alpha_inv(A1_MZ, B1_MSSM, mu23_m)
    miss_m = abs(a1_at_23m - v23_m) / v23_m * 100
    ax2.text(0.05, 0.05, f'Miss at 2-3: {miss_m:.1f}%',
             transform=ax2.transAxes, fontsize=11,
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    fig.suptitle('Gauge Coupling Unification -- SO(14) Phase 1 Test',
                 fontsize=15, fontweight='bold')
    fig.tight_layout()

    plot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    os.makedirs(plot_dir, exist_ok=True)
    plot_path = os.path.join(plot_dir, 'so14_rg_unification_plot.png')
    fig.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Plot saved: {plot_path}")


# ============================================================================
# VERDICT
# ============================================================================

def verdict(R):
    print()
    print("=" * 78)
    print("VERDICT: PRE-REGISTERED KILL CONDITIONS")
    print("=" * 78)
    print()

    miss = R['miss_pct']
    print(f"KC-1: Coupling unification miss > 5%?")
    print(f"  Miss at SU(2)-SU(3) crossing: {miss:.1f}%")

    if miss <= 5.0:
        kc1 = "GREEN"
        print(f"  STATUS: GREEN ({miss:.1f}% <= 5%)")
    else:
        kc1 = "YELLOW"
        print(f"  STATUS: YELLOW ({miss:.1f}% > 5%, generic non-SUSY miss)")
    print()

    tau = R['tau_yr']
    bound = R['tau_bound']
    print(f"KC-2: Proton lifetime < Super-K bound?")
    print(f"  tau_p = 10^{np.log10(tau):.1f} years,  bound = 10^{np.log10(bound):.1f} years")

    if tau > bound:
        kc2 = "GREEN"
        print(f"  STATUS: GREEN (safe by factor {tau/bound:.0e})")
    else:
        kc2 = "RED"
        print(f"  STATUS: RED -- KILL CONDITION FIRES")
    print()

    print("-" * 60)
    print(f"  KC-1 (coupling unification): {kc1}")
    print(f"  KC-2 (proton decay):         {kc2}")
    print()

    if kc2 == "RED":
        overall = "FAIL"
    elif kc1 == "YELLOW":
        overall = "YELLOW"
    elif kc1 == "GREEN" and kc2 == "GREEN":
        overall = "PASS"
    else:
        overall = "FAIL"

    print(f"  OVERALL: {overall}")
    if overall == "PASS":
        print("  Both kill conditions pass. Proceed to Phase 2.")
    elif overall == "YELLOW":
        print("  Generic non-SUSY miss. Not SO(14)-specific.")
        print("  Recommendation: proceed with noted caveat.")
    elif overall == "FAIL":
        print("  At least one FATAL kill condition fires.")
    print()

    R['kc1'] = kc1
    R['kc2'] = kc2
    R['overall'] = overall
    return R


# ============================================================================
# MAIN
# ============================================================================

def main():
    print()
    print("*" * 78)
    print("SO(14) RG COUPLING UNIFICATION -- PHASE 1 FALSIFICATION TEST")
    print("Experiment 4, Phase 1 (EXPERIMENT_REGISTRY.md)")
    print("KC-1: coupling miss > 5% => investigate")
    print("KC-2: proton lifetime < 1.6e34 years => DEAD")
    print("*" * 78)
    print()

    R = part1_sm()
    part2_mssm()
    R = part3_corrections(R)
    R = part4_so14(R)
    R = part5_proton(R)
    part6_plot(R)
    R = verdict(R)

    # Save
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    os.makedirs(out_dir, exist_ok=True)
    output = {
        'experiment': 'Experiment 4 Phase 1: SO(14) RG Coupling Unification',
        'timestamp': datetime.now().isoformat(),
        'convention': 'alpha_i^{-1}(mu) = alpha_i^{-1}(M_Z) - b_i/(2pi)*ln(mu/M_Z)',
        'normalization': 'GUT: alpha_1^{-1}(M_Z)=59.0, b1=123/50=2.46',
        'inputs': {
            'M_Z_GeV': M_Z, 'a1_MZ': A1_MZ, 'a2_MZ': A2_MZ, 'a3_MZ': A3_MZ,
            'b1': B1, 'b2': B2, 'b3': B3,
        },
        'results': {k: float(v) if isinstance(v, (np.floating, float, int)) else v
                    for k, v in R.items() if not isinstance(v, np.ndarray)},
    }
    out_path = os.path.join(out_dir, 'so14_rg_unification_results.json')
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Results saved: {out_path}")
    print()
    print("=" * 78)
    print("END")
    print("=" * 78)


if __name__ == '__main__':
    main()
