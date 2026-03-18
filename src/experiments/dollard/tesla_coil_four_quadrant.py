"""
Tesla Coil Quarter-Wave Resonator: Dollard's Four-Quadrant Analysis

This is Dollard's home turf. A Tesla coil secondary is a quarter-wave
resonant transmission line with:
  - Distributed L and C (not lumped)
  - Very high Q (1000+)
  - Open circuit at the top (voltage magnification)
  - Ground connection at the bottom

Standard EE says: "standing wave, voltage magnification = Q, done."
Dollard's four-quadrant decomposition says: "HERE is where the energy
is storing, transferring, returning, and dissipating at every point
along the coil."

The question: does the four-quadrant view reveal structure that the
standard view compresses away? Specifically, in a system where
gross >> net (Q > 1000), what does the energy budget actually look like?
"""

import numpy as np
from math import factorial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# =============================================================================
# QUATERNARY DECOMPOSITION
# =============================================================================

def quaternary_subseries(t, N_terms=30):
    """Dollard's four subseries of e^t."""
    t = np.asarray(t, dtype=float)
    u = np.zeros_like(t)
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    y = np.zeros_like(t)

    for n in range(N_terms):
        k0, k1, k2, k3 = 4*n, 4*n+1, 4*n+2, 4*n+3
        u += t**k0 / factorial(k0)
        x += t**k1 / factorial(k1)
        v += t**k2 / factorial(k2)
        y += t**k3 / factorial(k3)

    return u, x, v, y


# =============================================================================
# TESLA COIL MODEL
# =============================================================================

class TeslaCoilSecondary:
    """
    Quarter-wave helical resonator (Tesla coil secondary).

    Physical model: distributed transmission line, shorted at base,
    open at top. Resonance at f where coil length = lambda/4.

    Typical values for a small demonstration coil:
      - Wire length: ~20m wound into ~0.5m height
      - Resonant frequency: ~200 kHz
      - Q factor: 200-1000 (depends on construction)
      - Characteristic impedance: ~20-50 kOhm (high, because L/C is large)
    """

    def __init__(self, wire_length=20.0, height=0.5,
                 L_per_m=50e-6, C_per_m=5e-12,
                 R_per_m=0.1, G_per_m=1e-9,
                 name="Demo Tesla Coil"):
        self.wire_length = wire_length  # total wire length (m)
        self.height = height            # physical height (m)
        self.L = L_per_m               # inductance per meter of wire
        self.C = C_per_m               # capacitance per meter of wire
        self.R = R_per_m               # resistance per meter of wire
        self.G = G_per_m               # conductance per meter of wire
        self.name = name

        # Derived quantities
        self.v_phase = 1.0 / np.sqrt(self.L * self.C)  # phase velocity
        self.Z0 = np.sqrt(self.L / self.C)              # characteristic impedance
        self.f_res = self.v_phase / (4 * self.wire_length)  # quarter-wave resonance
        self.omega_res = 2 * np.pi * self.f_res
        self.wavelength = 4 * self.wire_length

        # Q factor
        alpha_res = self.R / (2 * self.Z0) + self.G * self.Z0 / 2
        beta_res = self.omega_res / self.v_phase
        self.Q = beta_res / (2 * alpha_res) if alpha_res > 0 else float('inf')

        # Propagation constant at resonance
        Z = self.R + 1j * self.omega_res * self.L
        Y = self.G + 1j * self.omega_res * self.C
        self.gamma_res = np.sqrt(Z * Y)

    def voltage_distribution(self, x_norm, omega=None):
        """
        Voltage along the coil (normalized position 0=base, 1=top).

        For a quarter-wave line shorted at base, open at top:
        V(x) = V_max * sin(beta * x) * envelope(alpha * x)

        At resonance: V(top)/V(base_effective) = Q (approximately)
        """
        if omega is None:
            omega = self.omega_res

        x = x_norm * self.wire_length
        Z = self.R + 1j * omega * self.L
        Y = self.G + 1j * omega * self.C
        gamma = np.sqrt(Z * Y)

        alpha = gamma.real
        beta = gamma.imag

        # Quarter-wave standing wave pattern
        # V(x) proportional to sin(beta*x) with exponential envelope
        V = np.sin(beta * x) * np.exp(-alpha * x)

        # Normalize so V(top) = Q (voltage magnification)
        V_top = np.sin(beta * self.wire_length) * np.exp(-alpha * self.wire_length)
        if abs(V_top) > 1e-15:
            V = V / V_top * self.Q

        return V

    def current_distribution(self, x_norm, omega=None):
        """Current along the coil. Max at base, zero at top (open circuit)."""
        if omega is None:
            omega = self.omega_res

        x = x_norm * self.wire_length
        Z = self.R + 1j * omega * self.L
        Y = self.G + 1j * omega * self.C
        gamma = np.sqrt(Z * Y)

        alpha = gamma.real
        beta = gamma.imag

        # I(x) proportional to cos(beta*x) (90 degrees out of phase with V)
        I = np.cos(beta * x) * np.exp(-alpha * x)
        return I


def four_quadrant_energy_analysis(coil, n_points=500):
    """
    Dollard's four-quadrant energy analysis at every point along the coil.

    At each position x, decompose the energy into:
      Q1 (u): energy being stored (electric field building in C)
      Q2 (x): energy being transferred (Poynting vector, forward)
      Q3 (v): energy being returned (electric field collapsing)
      Q4 (y): energy being dissipated (ohmic loss in R)

    Standard analysis gives you:
      - V(x) = voltage envelope (standing wave)
      - I(x) = current envelope (90 degrees shifted)
      - P_avg = 0 at resonance (reactive power only)

    Dollard's analysis gives you the GROSS energy flows that sum to zero.
    """
    x_norm = np.linspace(0, 1, n_points)
    x_phys = x_norm * coil.wire_length

    gamma = coil.gamma_res
    alpha = gamma.real
    beta = gamma.imag

    # The propagation involves e^(-gamma*x) and e^(+gamma*x)
    # For a standing wave: V(x) ~ sin(beta*x) = (e^(j*beta*x) - e^(-j*beta*x))/(2j)
    # With losses: includes e^(-alpha*x) envelope

    # Quaternary decomposition of the ATTENUATION part at each position
    alpha_x = alpha * x_phys
    u_atten, x_atten, v_atten, y_atten = quaternary_subseries(alpha_x)
    u_atten_neg, x_atten_neg, v_atten_neg, y_atten_neg = quaternary_subseries(-alpha_x)

    # Quaternary decomposition of the PHASE part at each position
    beta_x = beta * x_phys
    u_phase, x_phase, v_phase, y_phase = quaternary_subseries(beta_x)

    # Standard analysis results
    V = coil.voltage_distribution(x_norm)
    I = coil.current_distribution(x_norm)

    # Energy densities (standard)
    E_electric = 0.5 * coil.C * V**2    # electric field energy per unit length
    E_magnetic = 0.5 * coil.L * I**2    # magnetic field energy per unit length
    E_total = E_electric + E_magnetic

    # Instantaneous power flow (standard): P = V * I (Poynting)
    P_flow = V * I

    # --- DOLLARD'S FOUR-QUADRANT DECOMPOSITION ---

    # The gross energy at each point from the quaternary expansion:
    # For the phase component (which dominates in a resonator):
    # cos(beta*x) = u_phase - v_phase  (net circular)
    # sin(beta*x) = x_phase - y_phase  (net circular)
    # cosh(beta*x) = u_phase + v_phase (gross circular)
    # sinh(beta*x) = x_phase + y_phase (gross circular)

    gross_circular = u_phase + v_phase    # = cosh(beta*x)
    net_circular = u_phase - v_phase      # = cos(beta*x)

    # The ratio: how much more energy is CIRCULATING vs PASSING
    # at each point along the coil
    gross_net_ratio = np.abs(gross_circular) / (np.abs(net_circular) + 1e-15)

    # Dollard's four energy quadrants at each position:
    # These track the gross energy flows, not the net
    Q1_storage = u_phase * u_atten_neg     # energy being stored (cosh-like * decay)
    Q2_transfer = x_phase * u_atten_neg    # energy being transferred forward
    Q3_return = v_phase * u_atten_neg      # energy being returned
    Q4_dissipation = y_phase * u_atten_neg # energy being dissipated

    # The KEY metric: at the top of the coil (open circuit),
    # how much gross energy is circulating vs how much net?
    top_idx = -1
    top_gross = gross_circular[top_idx]
    top_net = abs(net_circular[top_idx])

    return {
        'x_norm': x_norm,
        'x_phys': x_phys,

        # Standard analysis
        'V': V,
        'I': I,
        'E_electric': E_electric,
        'E_magnetic': E_magnetic,
        'E_total': E_total,
        'P_flow': P_flow,

        # Dollard's four quadrants
        'Q1_storage': Q1_storage,
        'Q2_transfer': Q2_transfer,
        'Q3_return': Q3_return,
        'Q4_dissipation': Q4_dissipation,

        # Phase decomposition
        'u_phase': u_phase,
        'x_phase': x_phase,
        'v_phase': v_phase,
        'y_phase': y_phase,

        # Key ratios
        'gross_circular': gross_circular,
        'net_circular': net_circular,
        'gross_net_ratio': gross_net_ratio,

        # Attenuation subseries
        'decay_envelope': np.exp(-alpha * x_phys),

        # Top-of-coil metrics
        'top_gross': top_gross,
        'top_net': top_net,
        'top_ratio': top_gross / (top_net + 1e-15),
    }


def energy_budget_comparison(coil, results):
    """
    Compare standard vs Dollard energy budgets.

    Standard: P_in = P_dissipated (conservation of energy, net)
    Dollard: Q1 + Q2 + Q3 + Q4 = P_in (conservation, but decomposed into gross)

    The difference: standard sees a small net power flow sustaining losses.
    Dollard sees an ENORMOUS gross power circulation with a tiny net leakage.
    """
    x = results['x_norm']
    dx = x[1] - x[0]

    # Standard energy budget
    E_total_integrated = np.trapz(results['E_total'], x)
    E_electric_integrated = np.trapz(results['E_electric'], x)
    E_magnetic_integrated = np.trapz(results['E_magnetic'], x)

    # Dollard energy budget
    Q1_total = np.trapz(np.abs(results['Q1_storage']), x)
    Q2_total = np.trapz(np.abs(results['Q2_transfer']), x)
    Q3_total = np.trapz(np.abs(results['Q3_return']), x)
    Q4_total = np.trapz(np.abs(results['Q4_dissipation']), x)
    gross_total = Q1_total + Q2_total + Q3_total + Q4_total

    # Gross-to-net ratio for the whole coil
    net_total = abs(Q1_total - Q3_total) + abs(Q2_total - Q4_total)
    overall_ratio = gross_total / (net_total + 1e-15)

    return {
        'E_total': E_total_integrated,
        'E_electric': E_electric_integrated,
        'E_magnetic': E_magnetic_integrated,
        'Q1': Q1_total,
        'Q2': Q2_total,
        'Q3': Q3_total,
        'Q4': Q4_total,
        'gross_total': gross_total,
        'net_total': net_total,
        'gross_to_net': overall_ratio,
    }


# =============================================================================
# MULTI-FREQUENCY SWEEP: WHERE DOES DOLLARD'S VIEW ADD THE MOST?
# =============================================================================

def frequency_sweep(coil, f_ratios=None):
    """
    Sweep frequency around resonance. At resonance, gross >> net.
    Away from resonance, gross ~ net.

    This shows WHERE Dollard's notation adds information: near resonance,
    where the standard analysis says "Q is high" but doesn't show you
    the internal energy circulation pattern.
    """
    if f_ratios is None:
        f_ratios = np.linspace(0.5, 1.5, 200)

    results = []
    for ratio in f_ratios:
        omega = ratio * coil.omega_res
        x_phys = np.linspace(0, coil.wire_length, 200)

        Z = coil.R + 1j * omega * coil.L
        Y = coil.G + 1j * omega * coil.C
        gamma = np.sqrt(Z * Y)

        beta_x = gamma.imag * x_phys

        # Quaternary decomposition at the TOP of the coil
        top_beta_x = gamma.imag * coil.wire_length
        u, x_q, v, y_q = quaternary_subseries(np.array([top_beta_x]))

        gross = float(u[0] + v[0])   # cosh(beta*L)
        net = float(abs(u[0] - v[0]))  # |cos(beta*L)|

        # At quarter-wave resonance: beta*L = pi/2, so cos(pi/2) = 0
        # and cosh(pi/2) = 2.509. The net vanishes but gross doesn't!

        results.append({
            'f_ratio': ratio,
            'omega': omega,
            'gross': gross,
            'net': net,
            'ratio': gross / (net + 1e-15),
            'beta_L': gamma.imag * coil.wire_length,
        })

    return results


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("TESLA COIL FOUR-QUADRANT ANALYSIS")
    print("Dollard's Notation Applied to His Own Domain")
    print("=" * 70)

    # Build the coil
    coil = TeslaCoilSecondary(
        wire_length=20.0,      # 20m of wire
        height=0.5,            # wound into 0.5m height
        L_per_m=50e-6,         # 50 uH/m (helical winding)
        C_per_m=5e-12,         # 5 pF/m (self-capacitance)
        R_per_m=0.1,           # 100 mOhm/m (copper wire)
        G_per_m=1e-9,          # 1 nS/m (air dielectric)
    )

    print(f"\n  Coil: {coil.name}")
    print(f"  Wire length: {coil.wire_length} m")
    print(f"  Height: {coil.height} m")
    print(f"  Phase velocity: {coil.v_phase:.0f} m/s")
    print(f"  Characteristic impedance Z0: {coil.Z0:.0f} Ohm")
    print(f"  Resonant frequency: {coil.f_res/1e3:.1f} kHz")
    print(f"  Wavelength: {coil.wavelength:.1f} m")
    print(f"  Q factor: {coil.Q:.0f}")
    print(f"  Propagation constant: gamma = {coil.gamma_res.real:.6f} + j{coil.gamma_res.imag:.4f}")

    # --- Run the four-quadrant analysis ---
    print(f"\n{'='*70}")
    print("FOUR-QUADRANT ENERGY DISTRIBUTION ALONG THE COIL")
    print(f"{'='*70}")

    results = four_quadrant_energy_analysis(coil)
    budget = energy_budget_comparison(coil, results)

    print(f"\n  STANDARD ENERGY BUDGET:")
    print(f"    Total stored energy (integrated): {budget['E_total']:.4f}")
    print(f"    Electric field energy: {budget['E_electric']:.4f}")
    print(f"    Magnetic field energy: {budget['E_magnetic']:.4f}")
    print(f"    Standard says: 'Energy sloshes between E and B fields.'")

    print(f"\n  DOLLARD'S FOUR-QUADRANT ENERGY BUDGET:")
    print(f"    Q1 (storage):     {budget['Q1']:.4f}")
    print(f"    Q2 (transfer):    {budget['Q2']:.4f}")
    print(f"    Q3 (return):      {budget['Q3']:.4f}")
    print(f"    Q4 (dissipation): {budget['Q4']:.4f}")
    print(f"    Gross total:      {budget['gross_total']:.4f}")
    print(f"    Net total:        {budget['net_total']:.4f}")
    print(f"    GROSS/NET RATIO:  {budget['gross_to_net']:.1f}x")

    print(f"\n  AT THE TOP OF THE COIL (open end, max voltage):")
    print(f"    Gross energy cycling: {results['top_gross']:.2f}")
    print(f"    Net energy flowing:   {results['top_net']:.4f}")
    print(f"    Ratio:                {results['top_ratio']:.0f}x")

    # --- Sample points along the coil ---
    print(f"\n  ENERGY QUADRANTS ALONG THE COIL:")
    print(f"  {'Position':>10} | {'Q1 store':>10} | {'Q2 xfer':>10} | {'Q3 return':>10} | {'Q4 loss':>10} | {'Gross/Net':>10}")
    print(f"  {'-'*72}")
    for pos in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
        idx = int(pos * (len(results['x_norm']) - 1))
        q1 = results['Q1_storage'][idx]
        q2 = results['Q2_transfer'][idx]
        q3 = results['Q3_return'][idx]
        q4 = results['Q4_dissipation'][idx]
        ratio = results['gross_net_ratio'][idx]
        label = f"{pos*100:.0f}%"
        if pos == 0:
            label += " (base)"
        elif pos == 1:
            label += " (top)"
        print(f"  {label:>10} | {q1:10.4f} | {q2:10.4f} | {q3:10.4f} | {q4:10.4f} | {ratio:10.1f}")

    # --- Frequency sweep ---
    print(f"\n{'='*70}")
    print("FREQUENCY SWEEP: Where Does Dollard's View Add the Most?")
    print(f"{'='*70}")

    sweep = frequency_sweep(coil)

    print(f"\n  {'f/f_res':>8} | {'beta*L':>10} | {'Gross':>10} | {'Net':>10} | {'Ratio':>10}")
    print(f"  {'-'*56}")
    for s in sweep:
        if abs(s['f_ratio'] - 0.5) < 0.003 or \
           abs(s['f_ratio'] - 0.75) < 0.003 or \
           abs(s['f_ratio'] - 0.9) < 0.003 or \
           abs(s['f_ratio'] - 0.95) < 0.003 or \
           abs(s['f_ratio'] - 0.99) < 0.003 or \
           abs(s['f_ratio'] - 1.0) < 0.003 or \
           abs(s['f_ratio'] - 1.01) < 0.003 or \
           abs(s['f_ratio'] - 1.05) < 0.003 or \
           abs(s['f_ratio'] - 1.1) < 0.003 or \
           abs(s['f_ratio'] - 1.25) < 0.003 or \
           abs(s['f_ratio'] - 1.5) < 0.003:
            marker = " <<<" if abs(s['f_ratio'] - 1.0) < 0.01 else ""
            print(f"  {s['f_ratio']:8.3f} | {s['beta_L']:10.4f} | {s['gross']:10.2f} | {s['net']:10.4f} | {s['ratio']:10.1f}{marker}")

    # --- The punchline ---
    print(f"\n{'='*70}")
    print("THE PUNCHLINE")
    print(f"{'='*70}")

    # Find the resonance point
    res_point = min(sweep, key=lambda s: abs(s['f_ratio'] - 1.0))
    off_res = min(sweep, key=lambda s: abs(s['f_ratio'] - 0.5))

    print(f"""
  AT RESONANCE (f/f_res = 1.0):
    beta*L = pi/2 = {res_point['beta_L']:.4f}
    cos(beta*L) = cos(pi/2) = {res_point['net']:.6f}  (NET -> nearly zero)
    cosh(beta*L) = cosh(pi/2) = {res_point['gross']:.4f}  (GROSS -> 2.51)
    Gross/Net ratio: {res_point['ratio']:.0f}x

  AWAY FROM RESONANCE (f/f_res = 0.5):
    beta*L = pi/4 = {off_res['beta_L']:.4f}
    cos(beta*L) = {off_res['net']:.4f}  (NET -> substantial)
    cosh(beta*L) = {off_res['gross']:.4f}  (GROSS -> similar)
    Gross/Net ratio: {off_res['ratio']:.1f}x

  WHAT THIS MEANS:

  Standard EE at resonance says:
    "The voltage magnification is Q = {coil.Q:.0f}. Standing wave."
    That's two numbers. You're done.

  Dollard's four-quadrant analysis at resonance says:
    "The NET energy flow at the top approaches ZERO (cos(pi/2) -> 0).
     But the GROSS energy cycling is {res_point['gross']:.2f}
     (cosh(pi/2) = 2.51).

     This means energy is being STORED and RETURNED in equal measure.
     The net is nearly zero not because nothing is happening, but because
     ENORMOUS equal-and-opposite flows are canceling.

     The Q factor tells you HOW CLOSE to perfect cancellation you are.
     The four quadrants tell you WHERE along the coil the storage
     and return are happening."

  Standard notation COMPRESSES the gross flows into a single number (Q).
  Dollard's notation DECOMPRESSES them into a spatial map.

  Is this new physics? No. Is it new information? YES.
  The spatial distribution of gross energy flows IS information
  that standard analysis doesn't surface. It's there in the math
  (you CAN derive it from standard formulas) but standard notation
  doesn't make it VISIBLE.

  Dollard's notation makes it visible by DEFAULT.
  That's not nothing. That's what good notation does.
    """)

    # --- Generate plots ---
    print("Generating plots...")

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(f"Tesla Coil Four-Quadrant Analysis (Q={coil.Q:.0f}, f_res={coil.f_res/1e3:.1f} kHz)",
                 fontsize=14, fontweight='bold')

    # Plot 1: Standard voltage and current distribution
    ax = axes[0, 0]
    ax.plot(results['x_norm']*100, results['V']/max(abs(results['V'])+1e-15),
            'b-', label='V(x) (voltage)', linewidth=2)
    ax.plot(results['x_norm']*100, results['I']/max(abs(results['I'])+1e-15),
            'r-', label='I(x) (current)', linewidth=2)
    ax.set_xlabel('Position along coil (%)')
    ax.set_ylabel('Normalized amplitude')
    ax.set_title('Standard: V and I Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)

    # Plot 2: Standard energy distribution
    ax = axes[0, 1]
    ax.plot(results['x_norm']*100, results['E_electric']/(max(results['E_total'])+1e-15),
            'b-', label='Electric (in C)', linewidth=2)
    ax.plot(results['x_norm']*100, results['E_magnetic']/(max(results['E_total'])+1e-15),
            'r-', label='Magnetic (in L)', linewidth=2)
    ax.plot(results['x_norm']*100, results['E_total']/(max(results['E_total'])+1e-15),
            'k--', label='Total', linewidth=1.5, alpha=0.5)
    ax.set_xlabel('Position along coil (%)')
    ax.set_ylabel('Normalized energy density')
    ax.set_title('Standard: Energy Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: Dollard's four quadrants along the coil
    ax = axes[0, 2]
    ax.plot(results['x_norm']*100, results['Q1_storage'], 'b-',
            label='Q1: Storage', linewidth=2)
    ax.plot(results['x_norm']*100, results['Q2_transfer'], 'r-',
            label='Q2: Transfer', linewidth=2)
    ax.plot(results['x_norm']*100, results['Q3_return'], 'g-',
            label='Q3: Return', linewidth=2)
    ax.plot(results['x_norm']*100, results['Q4_dissipation'], 'm-',
            label='Q4: Dissipation', linewidth=2)
    ax.set_xlabel('Position along coil (%)')
    ax.set_ylabel('Quadrant amplitude')
    ax.set_title("Dollard: Four Quadrant Energy Map")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 4: Gross vs Net along the coil
    ax = axes[1, 0]
    ax.semilogy(results['x_norm']*100, results['gross_circular'],
                'r-', label='Gross (cosh)', linewidth=2)
    ax.semilogy(results['x_norm']*100, np.abs(results['net_circular']) + 1e-15,
                'b-', label='|Net| (|cos|)', linewidth=2)
    ax.set_xlabel('Position along coil (%)')
    ax.set_ylabel('Energy (log scale)')
    ax.set_title('Gross vs Net Energy Along Coil')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 5: Gross/Net ratio along the coil
    ax = axes[1, 1]
    ratio_clipped = np.clip(results['gross_net_ratio'], 0, 1000)
    ax.plot(results['x_norm']*100, ratio_clipped, 'r-', linewidth=2)
    ax.set_xlabel('Position along coil (%)')
    ax.set_ylabel('Gross/Net Ratio')
    ax.set_title('Hidden Energy Circulation Along Coil')
    ax.grid(True, alpha=0.3)

    # Plot 6: Frequency sweep - gross/net ratio vs frequency
    ax = axes[1, 2]
    f_ratios = [s['f_ratio'] for s in sweep]
    ratios = [min(s['ratio'], 1e4) for s in sweep]
    ax.semilogy(f_ratios, ratios, 'b-', linewidth=2)
    ax.axvline(x=1.0, color='r', linestyle='--', label='Resonance', alpha=0.7)
    ax.set_xlabel('f / f_resonance')
    ax.set_ylabel('Gross/Net Ratio (log)')
    ax.set_title('Gross/Net vs Frequency')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.5, 1.5)

    plt.tight_layout()
    plt.savefig('src/experiments/results/tesla_coil_four_quadrant.png',
                dpi=150, bbox_inches='tight')
    print(f"  Saved: src/experiments/results/tesla_coil_four_quadrant.png")

    # --- Energy flow animation data ---
    print(f"\n{'='*70}")
    print("WHAT DOLLARD SEES THAT STANDARD DOESN'T:")
    print(f"{'='*70}")
    print(f"""
  1. SPATIAL ENERGY MAP: At each point along the coil, four numbers
     (not two) describe the energy state. Standard gives you V and I.
     Dollard gives you storage, transfer, return, and dissipation.

  2. GROSS/NET DIVERGENCE AT RESONANCE: At resonance, the net circular
     component (cos) approaches zero while the gross (cosh) stays at 2.51.
     Standard says "standing wave." Dollard says "massive energy
     circulation with near-perfect cancellation."

  3. WHERE THE Q FACTOR LIVES: Standard says Q = {coil.Q:.0f}. Period.
     Dollard's decomposition shows WHERE along the coil the Q manifests
     as excess storage over return. The spatial distribution of the
     four quadrants IS the Q factor, unpacked.

  4. THE RECIPROCATION OPERATOR: When h acts on V(x) = sin(beta*x),
     the reciprocal 1/sin(beta*x) has poles — infinite impedance points.
     The standard -sin(beta*x) has no poles. These poles are WHERE
     the voltage magnification happens. Dollard's h-as-reciprocation
     points directly at the physics that standard h-as-negation misses.
    """)

    print("=" * 70)
    print("DONE.")
    print("=" * 70)
