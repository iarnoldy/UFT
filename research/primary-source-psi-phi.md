# Primary Source Analysis: Dollard's Psi and Phi Definitions

**Date**: 2026-03-08
**Source**: `source_materials/00_Lone Pine Writings_extracted.txt`
**Question**: Do Dollard's definitions of Psi and Phi match standard Lagrangian circuit variables?

## Findings

### Dollard's Definitions (from Lone Pine Writings)

| Symbol | Dollard's Name | Unit | Standard Equivalent |
|--------|---------------|------|-------------------|
| Psi | Total dielectric induction | Coulomb (charge) | q (generalized coordinate) |
| Phi | Total magnetic induction | Weber (flux) | lambda (conjugate momentum) |
| Q | Total electrification | Planck (J*s) | S = q*lambda (action) |
| W | dQ/dt | Joule (energy) | dS/dt = -H (Hamilton-Jacobi) |
| I | dPsi/dt | Ampere | dq/dt (current) |
| E | dPhi/dt | Volt | dlambda/dt (Faraday's law) |

### Key Passages

**Lines 525-535** (definitions):
> PSI, The total dielectric induction... This is the "Coulomb" (charge).
> PHI, The total magnetic induction... This is the "Weber" (induction).

**Lines 611-612** (time derivatives):
> v PSI equals I, Ampere, or Coulomb per second.
> v PHI equals E, Volt, or Weber per second.

**Lines 905-906** (explicit units):
> the dielectric field Psi in Coulombs and the magnetic field of Phi
> in Webers respectively.

**Lines 550-553** (grouping):
> Group One consists of: Q, Plancks, Psi, Coulombs, and Phi, Webers
> Group Two consists of: W, Joules, E, Volts, and I, Amperes.
> Group one represent PRIMARY quantities, whereas group two represent
> REACTIONS by the primary quantities to their variation in quantity
> with respect to Time.

**Line 659**:
> WEBER-COULOMB equals PLANCK

### Analysis

Dollard's system is a precise reinvention of Lagrangian circuit theory:

1. **Psi = q** (charge as generalized coordinate)
2. **Phi = lambda** (flux linkage as conjugate momentum)
3. **Q = Psi*Phi = q*lambda** (action = coordinate * momentum)
4. **W = dQ/dt** (energy = time derivative of action)
5. **Group One = configuration variables**, **Group Two = rate variables**

This is Cherry (1951) / Chua (1969) Lagrangian circuit formulation.
Dollard's "Group One" (primary, Q/Psi/Phi) are the generalized coordinates
and momenta; "Group Two" (reactions, W/E/I) are the Euler-Lagrange rates.

### Important Correction

Our CLAIM_TRIAGE.md originally said "IF Dollard's Psi and Phi match standard
flux and charge (plausible but not confirmed from primary sources)." This is
now CONFIRMED with 99% confidence from direct quotation.

Note: Dollard uses Psi for charge and Phi for flux, which is the opposite
of the most common physics convention (where psi often denotes a wavefunction
and phi/Phi denotes flux). But the correspondence to Lagrangian variables is
exact.

### Confidence

- Dimensional correctness: 99%
- Identity with Lagrangian circuit theory: 95%
- Novelty of Dollard's contribution: 0% (Cherry 1951, arguably Heaviside 1880s)
