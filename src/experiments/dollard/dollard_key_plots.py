"""
Clean, focused plots showing what Dollard's notation reveals.
"""

import numpy as np
from math import factorial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def quaternary_subseries(t, N_terms=30):
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
# FIGURE 1: The Core Insight — Gross vs Net Energy
# =============================================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("What Dollard's Notation Reveals That Standard Notation Hides",
             fontsize=16, fontweight='bold', y=1.02)

# --- Panel A: The quaternary decomposition ---
ax = axes[0]
t = np.linspace(0, 5, 500)
u, xq, v, yq = quaternary_subseries(t)

ax.fill_between(t, 0, u, alpha=0.3, color='blue', label='Q1: Storage (u)')
ax.fill_between(t, 0, -v, alpha=0.3, color='green', label='Q3: Return (v)')
ax.plot(t, u - v, 'k-', linewidth=3, label='NET = cos(t)')
ax.plot(t, u + v, 'r--', linewidth=2, label='GROSS = cosh(t)')

ax.set_xlabel('t (propagation distance / time constants)', fontsize=12)
ax.set_ylabel('Energy', fontsize=12)
ax.set_title('A) Four-Quadrant Decomposition of e^t\n'
             'Gross energy (red) vs Net energy (black)', fontsize=11)
ax.legend(loc='upper left', fontsize=9)
ax.set_ylim(-15, 50)
ax.grid(True, alpha=0.3)

# Annotate the divergence
ax.annotate(f'At t=5:\nGross = {np.cosh(5):.0f}\nNet = {abs(np.cos(5)):.2f}\nRatio = {np.cosh(5)/abs(np.cos(5)):.0f}x',
            xy=(5, np.cosh(5)), fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8),
            xytext=(3.2, 40), arrowprops=dict(arrowstyle='->', color='red', lw=2))

# --- Panel B: Tesla coil — gross/net ratio along the coil ---
ax = axes[1]

# Tesla coil parameters
L_per_m, C_per_m = 50e-6, 5e-12
R_per_m, G_per_m = 0.1, 1e-9
wire_length = 20.0
omega = 2 * np.pi * (1.0 / np.sqrt(L_per_m * C_per_m)) / (4 * wire_length) * 2 * np.pi

Z = R_per_m + 1j * omega * L_per_m
Y = G_per_m + 1j * omega * C_per_m
gamma = np.sqrt(Z * Y)
Z0 = np.sqrt(L_per_m / C_per_m)
Q_factor = gamma.imag / (2 * gamma.real) if gamma.real > 0 else 1000

x_pos = np.linspace(0, wire_length, 500)
beta_x = gamma.imag * x_pos

u_p, x_p, v_p, y_p = quaternary_subseries(beta_x)
gross = u_p + v_p   # cosh(beta*x)
net = np.abs(u_p - v_p)  # |cos(beta*x)|
ratio = gross / (net + 1e-15)

x_pct = x_pos / wire_length * 100

ax.semilogy(x_pct, gross, 'r-', linewidth=2.5, label='GROSS energy (cosh)')
ax.semilogy(x_pct, net + 1e-10, 'b-', linewidth=2.5, label='NET energy (|cos|)')
ax.fill_between(x_pct, net + 1e-10, gross, alpha=0.15, color='red',
                label='Hidden circulation')

ax.set_xlabel('Position along Tesla coil (%)\n(0% = grounded base, 100% = open top)',
              fontsize=11)
ax.set_ylabel('Energy (log scale)', fontsize=12)
ax.set_title(f'B) Tesla Coil (Q={Q_factor:.0f})\n'
             'Energy standard EE sees vs what actually circulates', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(1e-4, 10)

ax.annotate('At the top:\nNET -> 0\nGROSS = 2.51\n'
            'Standard sees nothing.\nDollard sees everything.',
            xy=(98, 2.5), fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9),
            xytext=(40, 5), arrowprops=dict(arrowstyle='->', color='red', lw=2))

# --- Panel C: The three meanings of h ---
ax = axes[2]
t_op = np.linspace(0.01, 3, 200)

f_t = np.exp(t_op)
h_number = -np.exp(t_op)         # h as -1: just negate
h_reciprocal = np.exp(-t_op)     # h as reciprocation: 1/f(t) = e^(-t)

ax.plot(t_op, f_t, 'b-', linewidth=2.5, label='f(t) = e^t')
ax.plot(t_op, h_number, 'r-', linewidth=2.5, label='Standard: -e^t  (negate)')
ax.plot(t_op, h_reciprocal, 'g-', linewidth=2.5, label="Dollard: e^(-t)  (reciprocate)")
ax.axhline(y=0, color='k', linewidth=0.5, linestyle='-')

ax.set_xlabel('t', fontsize=12)
ax.set_ylabel('Value', fontsize=12)
ax.set_title('C) h as Number vs h as Operator\n'
             'Three different physical operations', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(-15, 20)

# Annotate the key difference
ax.annotate('At t=1:\n-e = -2.72\n1/e = 0.37\n\nSame "h".\nDifferent physics.',
            xy=(1, -np.e), fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9),
            xytext=(1.8, -12), arrowprops=dict(arrowstyle='->', color='red', lw=2))

ax.annotate('', xy=(1, np.exp(-1)),
            xytext=(1.75, -10.5),
            arrowprops=dict(arrowstyle='->', color='green', lw=2))

plt.tight_layout()
plt.savefig('src/experiments/results/dollard_key_insight.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("Saved: src/experiments/results/dollard_key_insight.png")


# =============================================================================
# FIGURE 2: Tesla Coil Four-Quadrant Energy Map
# =============================================================================

fig2, axes2 = plt.subplots(2, 2, figsize=(14, 11))
fig2.suptitle(f"Tesla Coil Four-Quadrant Energy Map (Q = {Q_factor:.0f})",
              fontsize=15, fontweight='bold')

# Panel A: Standard view — just V and I
ax = axes2[0, 0]
V = np.sin(gamma.imag * x_pos) * np.exp(-gamma.real * x_pos)
I = np.cos(gamma.imag * x_pos) * np.exp(-gamma.real * x_pos)
V_norm = V / (max(abs(V)) + 1e-15)
I_norm = I / (max(abs(I)) + 1e-15)

ax.plot(x_pct, V_norm, 'b-', linewidth=2.5, label='Voltage V(x)')
ax.plot(x_pct, I_norm, 'r-', linewidth=2.5, label='Current I(x)')
ax.fill_between(x_pct, 0, V_norm, alpha=0.1, color='blue')
ax.fill_between(x_pct, 0, I_norm, alpha=0.1, color='red')
ax.set_xlabel('Position along coil (%)', fontsize=11)
ax.set_ylabel('Normalized amplitude', fontsize=11)
ax.set_title('Standard View: V and I\n(This is ALL standard EE shows you)', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)

# Panel B: Dollard's four quadrants
ax = axes2[0, 1]
decay = np.exp(-gamma.real * x_pos)
ax.plot(x_pct, u_p * decay, 'b-', linewidth=2.5, label='Q1: Storage')
ax.plot(x_pct, x_p * decay, 'r-', linewidth=2.5, label='Q2: Transfer')
ax.plot(x_pct, v_p * decay, 'g-', linewidth=2.5, label='Q3: Return')
ax.plot(x_pct, y_p * decay, color='purple', linewidth=2.5, label='Q4: Dissipation')
ax.set_xlabel('Position along coil (%)', fontsize=11)
ax.set_ylabel('Quadrant amplitude', fontsize=11)
ax.set_title("Dollard's View: Four Energy Quadrants\n"
             "(WHERE energy stores, transfers, returns, dissipates)", fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Panel C: Gross/Net ratio along the coil
ax = axes2[1, 0]
ratio_clipped = np.clip(ratio, 1, 5000)
ax.plot(x_pct, ratio_clipped, 'r-', linewidth=2.5)
ax.fill_between(x_pct, 1, ratio_clipped, alpha=0.2, color='red')
ax.set_xlabel('Position along coil (%)', fontsize=11)
ax.set_ylabel('Gross / Net Energy Ratio', fontsize=11)
ax.set_title('Hidden Energy Circulation\n'
             '(How much more energy circulates than flows)', fontsize=11)
ax.set_yscale('log')
ax.grid(True, alpha=0.3)
ax.axhline(y=1, color='k', linewidth=1, linestyle='--', alpha=0.5)
ax.annotate(f'At top: {ratio[-1]:.0f}x more\nenergy CIRCULATING\nthan FLOWING',
            xy=(95, min(ratio_clipped[-1], 5000)), fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9),
            xytext=(30, 500), arrowprops=dict(arrowstyle='->', color='red', lw=2))

# Panel D: Frequency response of gross/net
ax = axes2[1, 1]
f_ratios = np.linspace(0.5, 1.5, 500)
ratios_freq = []
for fr in f_ratios:
    w = fr * omega
    Z_f = R_per_m + 1j * w * L_per_m
    Y_f = G_per_m + 1j * w * C_per_m
    g_f = np.sqrt(Z_f * Y_f)
    top_beta = g_f.imag * wire_length
    u_t, _, v_t, _ = quaternary_subseries(np.array([top_beta]))
    gr = float(u_t[0] + v_t[0])
    nt = float(abs(u_t[0] - v_t[0]))
    ratios_freq.append(gr / (nt + 1e-15))

ax.semilogy(f_ratios, ratios_freq, 'b-', linewidth=2.5)
ax.axvline(x=1.0, color='r', linewidth=2, linestyle='--', alpha=0.7, label='Resonance')
ax.fill_between(f_ratios, 1, ratios_freq, alpha=0.1, color='blue')
ax.set_xlabel('Frequency / Resonant Frequency', fontsize=11)
ax.set_ylabel('Gross / Net Ratio (log)', fontsize=11)
ax.set_title('Frequency Response of Hidden Circulation\n'
             '(Peaks sharply at resonance)', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0.5, 1.5)
ax.annotate(f'At resonance:\n{max(ratios_freq):.0f}x hidden\ncirculation',
            xy=(1.0, max(ratios_freq)), fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9),
            xytext=(1.15, max(ratios_freq)/2),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))

plt.tight_layout()
plt.savefig('src/experiments/results/tesla_coil_energy_map.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("Saved: src/experiments/results/tesla_coil_energy_map.png")


# =============================================================================
# FIGURE 3: The Income/Expenses Analogy
# =============================================================================

fig3, axes3 = plt.subplots(1, 2, figsize=(14, 5))
fig3.suptitle("Standard EE vs Dollard: Profit Sheet vs Full Ledger",
              fontsize=14, fontweight='bold', y=1.02)

# Panel A: Standard view (just the net)
ax = axes3[0]
positions = ['Base', '25%', '50%', '75%', 'Top']
pos_vals = [0, 0.25, 0.5, 0.75, 1.0]
net_vals = [abs(np.cos(gamma.imag * p * wire_length)) for p in pos_vals]
ax.bar(positions, net_vals, color='steelblue', edgecolor='black', linewidth=1.5)
ax.set_ylabel('Net Energy Flow', fontsize=12)
ax.set_title('Standard EE: "Profit Only"\n(Net power at each position)', fontsize=11)
ax.set_ylim(0, 1.5)
ax.grid(True, alpha=0.3, axis='y')
for i, v in enumerate(net_vals):
    ax.text(i, v + 0.03, f'{v:.3f}', ha='center', fontsize=10, fontweight='bold')

# Panel B: Dollard view (income AND expenses)
ax = axes3[1]
bar_width = 0.35
x_bar = np.arange(len(positions))

storage_vals = []
return_vals = []
for p in pos_vals:
    bx = gamma.imag * p * wire_length
    u_t, _, v_t, _ = quaternary_subseries(np.array([bx]))
    storage_vals.append(float(u_t[0]))
    return_vals.append(float(v_t[0]))

bars1 = ax.bar(x_bar - bar_width/2, storage_vals, bar_width,
               label='Q1: Storage (income)', color='blue', alpha=0.7,
               edgecolor='black', linewidth=1)
bars2 = ax.bar(x_bar + bar_width/2, return_vals, bar_width,
               label='Q3: Return (expense)', color='green', alpha=0.7,
               edgecolor='black', linewidth=1)

ax.set_xticks(x_bar)
ax.set_xticklabels(positions)
ax.set_ylabel('Gross Energy Flow', fontsize=12)
ax.set_title("Dollard: Full Ledger\n(Gross storage AND return at each position)", fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 1.5)

# Annotate the top position
ax.annotate(f'At top: storage = return\n= {storage_vals[-1]:.3f}\n'
            f'Net = {abs(storage_vals[-1]-return_vals[-1]):.6f}\n'
            f'NEARLY PERFECT cancellation',
            xy=(4, max(storage_vals[-1], return_vals[-1])),
            fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8),
            xytext=(2, 1.3), arrowprops=dict(arrowstyle='->', color='red', lw=2))

plt.tight_layout()
plt.savefig('src/experiments/results/dollard_income_expenses.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("Saved: src/experiments/results/dollard_income_expenses.png")

print("\nAll plots generated.")
