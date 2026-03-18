# The Sign Flip as Physics: Prediction Space, Mechanisms, and Falsification

**Agent**: Heptapod B Architect (teleological reasoning)
**Date**: 2026-03-17
**Investigation**: dollard-pure-construction, extension
**Prior rounds**: All five (`01-vision.md` through `05-synthesis.md`, `VERDICT.md`)
**Methodology**: Teleological reasoning + constructive vision + structural fusion

---

## Preamble: What This Document Is and Is Not

This document does NOT validate Dollard's sign flip claim. The mathematics is
settled: standard complex multiplication gives ZY = (RG+XB) + j(XG-RB), and
Dollard's form ZY = h(XB+RG) + j(XG-RB) with h = -1 yields -(XB+RG) for the
real part, which is wrong. This is proved in Lean, verified in SymPy, confirmed
by five council rounds. The algebraic claim is dead.

This document asks a different question: **If we treat the sign flip not as an
algebraic error but as a physical prediction, what would the observable universe
look like?** This is the constructive-vision technique of asking "what would
[impossible thing] look like if it existed?" -- not to validate it, but to map
the prediction space so thoroughly that either (a) we find a testable regime
where standard and alternative predictions diverge, or (b) we demonstrate that
the claim is unfalsifiable in practice, which is itself a finding.

---

## Step 1: Assume the Answer Exists

The answer exists. It says:

*There is a specific, testable physical scenario where the sign of the real
power term in the product ZY is predicted differently by standard circuit
theory and by an alternative framework in which real power can appear
negative. The scenario involves [specific components], [specific frequencies],
[specific measurement]. The standard prediction is [X watts]. The alternative
prediction is [-X watts] or [some other measurable deviation]. The experiment
costs [amount] and takes [time].*

I am reading this answer. What does it contain?

---

## Step 2: Characterize the Necessary Structure

For the sign flip to be "real physics" rather than an algebraic error, the
following conditions MUST hold:

### C1. There must exist a physical regime where Re(ZY) < 0

In standard theory, for a passive network:
- Z = R + jX with R >= 0 (resistance is non-negative)
- Y = G + jB with G >= 0 (conductance is non-negative)
- Re(ZY) = RG + XB (can be negative if XB < -RG, i.e., if reactive terms
  dominate with opposite signs)

Wait. This is important. **Re(ZY) CAN be negative in standard theory** when
X and B have opposite signs and |XB| > RG. This happens when the impedance
is inductive (X > 0) and the admittance has negative susceptance (B < 0), or
vice versa. The real part of the complex power product is not the same as the
real power dissipated -- it is a mathematical quantity that depends on how Z
and Y are defined.

### C2. The physical meaning of Re(ZY) must be clarified

The product ZY is dimensionless (ohms times siemens = 1). It is the
**propagation function** of a transmission line section, not the power
dissipated. Specifically:

- For a transmission line: gamma = sqrt(ZY) where Z = R + jwL (series
  impedance per unit length) and Y = G + jwC (shunt admittance per unit
  length)
- The real part of gamma is the attenuation constant alpha
- The imaginary part is the phase constant beta

For power: P = V*I* = |V|^2 * Y* = |I|^2 * Z, where the real part of Z
(resistance) and the real part of Y (conductance) determine dissipation.

### C3. Dollard's context must be identified precisely

Dollard's versor form appears in the context of the **telegraph equation**,
specifically in the Heaviside form for the propagation of signals along a
transmission line. The relevant product is:

    ZY = (R + jwL)(G + jwC)

Expanding:
- Standard: (RG - w^2LC) + jw(RC + LG)
- Dollard's claimed form (with h = -1 absorbed): -(RG - w^2LC) + jw(LG - RC)

Note: Dollard writes Z = R + jX and Y = G - jB, which differs from the
standard Y = G + jB. With his sign convention Y = G - jB where B = wC:

    ZY = (R + jX)(G - jB) = (RG + XB) + j(XG - RB)

This is correct. The issue is that Dollard then writes this as
h(XB + RG) + j(XG - RB), putting the real part in the h-component. Since
h = -1, this gives -(XB + RG), flipping the sign of the attenuation term.

### C4. What "sign flip in real power" would mean physically

If the attenuation constant alpha were negative, a signal would GROW as it
propagated along the line. This is:
- **Physically real** in active media (laser amplifiers, traveling wave tubes)
- **Physically impossible** in passive media (no energy source)
- **Observable** as signal amplitude increasing with distance from source

### C5. Necessary structure of the answer

The answer must contain:
1. A specific physical configuration where alpha < 0 could occur
2. A mechanism that supplies the energy (conservation is not optional)
3. A measurement protocol that distinguishes alpha > 0 from alpha < 0
4. A clear statement of what Dollard's framework predicts vs. standard theory
5. Kill conditions for the experiment itself

---

## Step 3: Inventory -- What Physical Mechanisms Could Produce an Effective Sign Flip?

### 3.1 Negative Resistance Devices (REAL PHYSICS, well-understood)

**Tunnel diodes** (Esaki, 1957) exhibit negative differential resistance (NDR)
in a specific voltage range. The I-V curve has a region where dI/dV < 0.

**Gunn diodes** exhibit NDR via the transferred electron effect (Ridley-Watkins-
Hilsum mechanism). Electrons transfer from a high-mobility valley to a
low-mobility valley in the conduction band, reducing current as voltage
increases.

**Relevance to sign flip**: In a circuit containing a negative resistance device,
the effective R in Z = R + jX can be negative. If |R_negative| > R_positive
(the passive losses), the net resistance is negative, and Re(ZY) flips sign.

**Structural fusion verdict**: ANALOGY (75%). The mechanism is real but it is
NOT what Dollard describes. Dollard's sign flip is in the ZY product formula
itself, not in the sign of R. A tunnel diode changes the VALUE of R, not the
FORMULA for ZY. Standard circuit theory with R < 0 already predicts
amplification -- no new algebra needed.

### 3.2 Parametric Amplification (REAL PHYSICS, well-understood)

A nonlinear reactance (varactor diode, nonlinear capacitor) pumped at frequency
f_p can amplify a signal at frequency f_s, with energy conservation enforced by
the Manley-Rowe relations:

    P_s/f_s + P_i/f_i = 0  (signal power + idler power = 0)
    P_s/f_s + P_p/f_p = 0  (signal power + pump power = 0)

The signal sees an effective negative resistance because energy is being
transferred from the pump to the signal via the nonlinear reactance.

**Relevance to sign flip**: The parametric amplifier creates conditions where
power flows from a "hidden" source (the pump) to the signal, making the signal
port appear to have negative resistance. A naive measurement of Z at the signal
port would show Re(Z) < 0.

**Structural fusion verdict**: ANALOGY (70%). Again, the mechanism changes the
effective value of R, not the formula. The Manley-Rowe relations are derived
from standard circuit theory. No sign flip in the algebra is needed.

### 3.3 Distributed Systems Where Lumped Models Break Down (REAL PHYSICS, subtle)

**This is the most promising lead for Dollard's specific domain.**

When the physical length of a circuit element is comparable to the wavelength
of the signal, the lumped-element approximation Z = R + jX breaks down. The
impedance becomes a function of position along the element, and standing waves
can create local regions where power flows backward (from load to source).

Specific scenarios:

**3.3.1 Quarter-wave transformer**: A transmission line of length lambda/4
transforms impedance by Z_in = Z_0^2 / Z_L. If Z_L is reactive (purely
imaginary), Z_in can have surprising properties -- including apparent negative
real part when measured with a lumped-element model at a specific point.

**3.3.2 Standing waves on a mismatched line**: When SWR > 1, there exist points
along the line where the reflected wave partially cancels the incident wave.
Between the voltage minimum and the current minimum (a quarter-wave apart),
the local V and I can be nearly 180 degrees out of phase, making the
instantaneous power flow negative (from load toward source). The TIME-AVERAGED
power is still positive (flowing from source to load), but a single-point
instantaneous measurement could show negative power.

**3.3.3 Tesla coils / helical resonators**: Dollard's primary experimental domain.
A Tesla coil secondary is a distributed resonator, not a lumped inductor. At
resonance, the voltage distribution along the coil follows a standing wave
pattern. The "extra coil" in Tesla's magnifying transmitter is a quarter-wave
resonator where voltage is amplified by the Q factor. A naive lumped-element
analysis of this system would give wrong signs for the power terms because the
Z and Y are functions of position, not constants.

**Structural fusion verdict**: IDENTITY (85%) with the domain where Dollard's
sign flip WOULD MATTER. In distributed systems, the lumped-element formula
ZY = (RG+XB) + j(XG-RB) is an approximation. The exact distributed formula
involves hyperbolic functions:

    gamma = sqrt(ZY),  Z_in = Z_0 * tanh(gamma * l)

The lumped formula (first-order Taylor approximation) and the distributed
formula (exact) can have opposite signs for the real part of the propagation
function in specific frequency ranges near resonance. This is not because the
algebra is wrong -- it is because the lumped model is being applied outside
its domain of validity.

**This is the most honest reading of Dollard's sign flip**: he may be describing
the failure mode of lumped-element analysis applied to distributed systems,
using incorrect algebra to point at a real physical phenomenon.

### 3.4 Transient Energy Return from Reactive Components (REAL PHYSICS, elementary)

In any circuit with inductors or capacitors, the instantaneous power can be
negative. An inductor stores energy in its magnetic field; when current
decreases, the inductor returns energy to the circuit. During this phase,
power flows FROM the inductor TO the source, giving negative instantaneous
power at that component.

For a purely reactive circuit (ideal inductor or capacitor, no resistance):
- Average real power = 0 (all energy stored and returned)
- Instantaneous power oscillates between positive and negative
- Peak negative power equals peak positive power

**Relevance to sign flip**: During the return phase of the energy storage cycle,
a wattmeter measuring instantaneous power would show a negative reading. If
the measurement window is synchronized to this phase, it would appear that
"real power is negative."

**Structural fusion verdict**: COINCIDENCE (35%). This is standard reactive power,
not a sign flip in the ZY formula. Every EE student learns this in the first
circuits course. The average power over a full cycle is zero for ideal reactive
components and positive for any component with resistance. This cannot explain
a systematic sign flip.

### 3.5 Nonlinear Reactance at Saturation (REAL PHYSICS, complex)

Ferrite cores at magnetic saturation, varactors at large signal levels, and
other nonlinear reactive elements have impedance that depends on signal
amplitude. At saturation:

- The effective inductance drops (permeability decreases)
- The impedance Z = R + jwL(I) becomes amplitude-dependent
- Harmonic generation transfers energy between frequencies
- The fundamental-frequency impedance can appear to have negative real part
  because energy is being transferred to harmonics (not dissipated, but removed
  from the measurement bandwidth)

**Relevance to sign flip**: A network analyzer measuring Z at the fundamental
frequency would see energy "disappearing" into harmonics, which could appear
as anomalous dissipation (positive R) or, if the harmonics feed back into the
fundamental through nonlinear mixing, as anomalous gain (negative R).

**Structural fusion verdict**: ANALOGY (60%). The mechanism is real but well-
understood via Volterra series analysis. No new algebra needed.

### 3.6 Casimir Effect and Quantum Vacuum Fluctuations (REAL PHYSICS, exotic)

At nanometer-scale gaps, the Casimir force between conductors can do work.
The effective impedance of a nano-gap capacitor includes contributions from
quantum vacuum fluctuations that are not captured by the classical capacitance
formula C = epsilon*A/d.

**Relevance to sign flip**: The Casimir effect contributes a tiny but real force
that could, in principle, affect the impedance of a nanoscale device. However,
the energy available is negligible compared to any practical electrical
measurement, and the effect is entirely within standard quantum electrodynamics.

**Structural fusion verdict**: COINCIDENCE (15%). No practical relevance to
Dollard's claims, which concern macroscopic circuits.

### 3.7 Active Antennas and Radiation Resistance (REAL PHYSICS, subtle)

An antenna has radiation resistance -- the component of impedance that accounts
for power radiated as electromagnetic waves. From the antenna's perspective,
this power leaves and never returns. But from the perspective of a distant
receiver antenna, the radiated power arrives as an incident field that
induces current, and the receiving antenna appears to have negative radiation
resistance (it outputs power rather than dissipating it).

**Relevance to sign flip**: In a coupled system of transmitting and receiving
antennas, the receiving side's impedance as seen by its load has Re(Z) that
is effectively "negative" in the sense that power flows out of the antenna
into the load without a local energy source. The energy comes from the
radiated field of the distant transmitter.

**Structural fusion verdict**: ANALOGY (55%). This is standard antenna theory.
The "negative resistance" of a receiving antenna is not mysterious -- it is
just the antenna converting field energy to circuit energy. No sign flip in
the ZY formula.

---

## Step 4: Identify the Precise Gap

The gap between "Dollard's sign flip" and "real physics" has three layers:

### Gap 1: Algebraic vs. Physical

Dollard's sign flip is in the FORMULA (algebraic). Real physics sign flips
are in the VALUES of R, G, X, B (parametric). The formula ZY = (RG+XB) +
j(XG-RB) is correct in all regimes where Z and Y are well-defined scalars.
The formula fails when Z and Y are not scalars -- i.e., in distributed
systems where impedance is a function of position.

### Gap 2: Lumped vs. Distributed

The ONE regime where the lumped formula gives wrong answers is the distributed
regime -- precisely Dollard's domain (Tesla coils, transmission lines at
resonance). In this regime:
- The correct model uses the telegrapher's equations (PDEs)
- The lumped model (algebraic formula) is an approximation
- Near resonance, the approximation can have the wrong sign for the
  attenuation term
- But the distributed model (using hyperbolic functions) gives the right answer

Dollard's "sign flip" could be a garbled recognition that the lumped formula
fails near resonance, expressed as a modification of the formula rather than
a recognition that the formula's domain of validity has been exceeded.

### Gap 3: Instantaneous vs. Average

In any reactive circuit, instantaneous power oscillates between positive and
negative. Only the time-averaged power is constrained to be non-negative
(for passive networks). A measurement synchronized to the reactive return
phase will show negative power.

Dollard's experimental domain (Tesla coils at resonance) involves very high
Q circuits where the reactive power is enormously larger than the real power.
A small timing error in power measurement would swamp the real power signal
with reactive oscillations, including negative excursions.

### Summary of the Gap

**The gap is not in the physics. The gap is between what Dollard's algebra says
(formula is wrong) and what his experiments might show (lumped model
breaks down in distributed systems near resonance, creating apparent
sign anomalies in naively-applied formulas).** Standard physics predicts
all of these phenomena. No new algebra is needed.

---

## Step 5: Design the Bridge -- A Concrete Experimental Test

### 5.1 The Experiment

**Title**: Measurement of Real Power Sign in a Transmission Line Near
Quarter-Wave Resonance

**Purpose**: Determine whether the sign of the real part of the propagation
function ZY, as measured by lumped-element methods, agrees with the sign
predicted by distributed-parameter analysis, and whether any discrepancy
can be mistaken for Dollard's sign flip.

### 5.2 Equipment (all bench-level, total cost < $500)

| Item | Specification | Purpose |
|------|--------------|---------|
| Signal generator | 1 Hz - 30 MHz, 50 ohm output | Drive the line |
| Oscilloscope | 2-channel, 100 MHz, with math functions | Measure V and I simultaneously |
| Current probe | AC current clamp or sense resistor (1 ohm) | Measure line current |
| Coaxial cable | RG-58, 50 ohm, exactly 5 meters | The transmission line under test |
| Resistive loads | 10, 25, 50, 100, 200 ohm (1%) | Termination conditions |
| Reactive loads | Inductors (1 uH, 10 uH, 100 uH), capacitors (100 pF, 1 nF, 10 nF) | Create mismatch |
| BNC tees and adapters | Standard | Measurement access points |

### 5.3 The Critical Frequency

For RG-58 cable (velocity factor ~0.66), the quarter-wave resonance frequency
for a 5-meter cable is:

    f_quarter = c * 0.66 / (4 * 5 m) = 9.9 MHz

At this frequency, the cable is exactly one quarter wavelength long. The
lumped model is maximally wrong here.

### 5.4 Measurement Protocol

**Step A: Baseline (lumped regime)**

At f = 100 kHz (cable is 0.025 wavelengths -- solidly lumped):
1. Terminate with 50 ohm load (matched)
2. Measure V_in, I_in, phase angle between them
3. Compute P_real = V_rms * I_rms * cos(phi)
4. Compute Z_in from V/I and phase
5. Record Re(Z_in), Im(Z_in)

**Prediction (standard AND Dollard)**: P_real > 0, Re(Z_in) approx 50 ohm.
Both models agree. The cable is short compared to wavelength.

**Step B: Quarter-wave resonance, matched load**

At f = 9.9 MHz, with 50 ohm termination:
1. Same measurements as Step A
2. Z_in should still be approximately 50 ohm (matched line)
3. P_real should be positive

**Prediction**: Both models agree. Matched line has no standing waves.

**Step C: Quarter-wave resonance, mismatched reactive load**

At f = 9.9 MHz, terminate with a pure capacitor (100 pF):
1. Z_load = 1/(jwC) = -j * 160.8 ohm (purely reactive)
2. Z_in = Z_0^2 / Z_load = (50)^2 / (-j*160.8) = j * 15.55 ohm
3. The input impedance SHOULD be purely reactive (positive imaginary)
4. Measure V_in, I_in, phase angle
5. P_real SHOULD be approximately zero (no dissipation in ideal case)
6. In practice, cable loss makes P_real slightly positive

**Now apply the lumped-element ZY formula naively**:
- Z = series impedance = R + jwL per unit length
- Y = shunt admittance = G + jwC per unit length
- For RG-58: R ~ 0.05 ohm/m, L ~ 250 nH/m, G ~ 0, C ~ 100 pF/m
- At 9.9 MHz: X = wL = 2*pi*9.9e6*250e-9 = 15.55 ohm/m
- B = wC = 2*pi*9.9e6*100e-12 = 6.22e-3 S/m
- ZY per meter = (0.05 + j15.55)(0 + j0.00622) = -0.0967 + j0.000311
- Re(ZY) = -0.0967 < 0

**The lumped formula gives negative real part.**

The distributed formula gives:
- gamma = sqrt(ZY) = sqrt(-0.0967 + j0.000311) = j*0.3110 + 0.0005
- alpha = Re(gamma) = 0.0005 Np/m (positive -- attenuation)
- beta = Im(gamma) = 0.3110 rad/m (phase constant)

**The distributed formula gives positive attenuation.**

THIS IS THE DISCREPANCY. The lumped ZY product has negative real part, but
the propagation constant (its square root) has positive real part. The sign
flip is an artifact of taking the product without the square root. In the
distributed model, the square root "fixes" the sign because sqrt of a negative
real number has positive real part when the imaginary part is positive.

**Step D: The Measurement That Distinguishes**

At f = 9.9 MHz, with reactive load (100 pF):
1. Measure ATTENUATION along the cable by probing at multiple points
2. If the signal amplitude DECREASES from input to load: alpha > 0 (standard)
3. If the signal amplitude INCREASES from input to load: alpha < 0 (anomalous)

**Standard prediction**: Signal decreases (cable has loss, alpha > 0)
**Dollard prediction (if taken literally)**: Signal increases (sign flip makes
alpha effectively negative in the lumped formula)

### 5.5 Concrete Numerical Predictions

For the specific configuration above (5m RG-58, 100 pF load, 9.9 MHz):

| Quantity | Standard prediction | "Sign flip" prediction | How to measure |
|----------|--------------------|-----------------------|----------------|
| V at input | V_0 (set by generator) | V_0 | Oscilloscope Ch 1 |
| V at load | V_0 * 0.997 (slight loss) | V_0 * 1.003 (slight gain) | Oscilloscope Ch 2 |
| Phase at load | +90 deg relative to input I | +90 deg | Phase measurement |
| P_real (time-averaged) | +2.5 mW (into cable loss) | -2.5 mW (out of cable) | V*I*cos(phi), averaged |
| Insertion loss | +0.025 dB | -0.025 dB | Network analyzer |

**The difference is 0.05 dB (0.6% in voltage).** This is at the edge of what
a bench oscilloscope can resolve. A network analyzer would do better.

### 5.6 Why This Experiment Is Not Trivial (Honest Assessment)

The predicted difference between standard and "sign flip" models is TINY --
about 0.6% in voltage for a 5-meter cable. This is because:

1. Cable loss at 10 MHz is small (RG-58 has about 0.025 dB/m at 10 MHz)
2. The sign flip affects only the attenuation term, not the phase term
3. At these signal levels, thermal noise, connector loss, and probe loading
   all introduce errors of the same order

**To make the effect larger, use a higher-loss cable or a longer line.** A
100-meter run of lossy cable (RG-174, about 0.1 dB/m at 10 MHz) would give:

- Standard: 10 dB loss
- Sign flip: 10 dB gain

This would be unmistakable. A signal that should be attenuated by a factor of
10 instead appears amplified by a factor of 10. This violates conservation of
energy unless there is an external power source.

**The experiment is definitive at sufficient cable length.** The challenge is
only at short lengths where the effect is small.

---

## Step 6: Kill Conditions

### KC-1: Conservation of Energy (FATAL)

If the sign flip predicts that a passive cable amplifies a signal (alpha < 0)
without an external energy source, this violates conservation of energy. This
is not a subtle theoretical objection -- it means the cable would have to
create energy from nothing. No passive network can do this.

**Status**: This kill condition fires IMMEDIATELY for any passive network.
The sign flip, taken literally, predicts perpetual motion. It is physically
impossible in a passive system.

**How to test**: Run 100 meters of cable. Measure output. If output > input,
where did the energy come from?

### KC-2: Kramers-Kronig Relations (FATAL for passive systems)

The Kramers-Kronig relations, derived from causality (the response cannot
precede the stimulus), require that the real and imaginary parts of any
causal response function are related by Hilbert transforms. For a passive
system, these relations guarantee that Re(Z) >= 0 at all frequencies.

A system with Re(ZY) < 0 everywhere (as Dollard's formula predicts) would
violate causality. The system would respond before being stimulated.

**Status**: This kill condition fires for any causal, passive system.

**How to test**: Measure Z(f) across a broad frequency range. Apply the
Kramers-Kronig consistency test. If the real part violates the relations,
either the measurement is wrong or the system is active (has a hidden source).

### KC-3: Thermodynamic Consistency (FATAL)

A network with negative real power (net power flowing from load to source)
is a refrigerator that runs without power input. The second law of
thermodynamics forbids this for any closed system.

**Status**: Fires immediately.

### KC-4: Every Negative-Resistance Effect Has an Identified Energy Source (LIMITS SCOPE)

Every known physical system with effective negative resistance has an
identified external energy source:
- Tunnel diode: DC bias supply
- Parametric amplifier: pump oscillator
- Laser: optical or electrical pump
- Receiving antenna: distant transmitter's radiated field

If Dollard claims negative real power without identifying the energy source,
the claim is incomplete. If no source exists, it is impossible.

**Status**: Dollard does not identify an energy source. His framework implies
that the "counterspace" or "dielectric field" provides the energy. This is
Track C material (extraordinary claim, no evidence).

### KC-5: Measurement Resolution (PRACTICAL)

For short cables, the predicted difference is < 1%. Measurement uncertainty
at 10 MHz with bench equipment is typically 1-3%. The experiment is
inconclusive at short lengths.

**Status**: Does not kill the physics, but kills the cheap experiment.
Resolution: use longer cables (100+ meters) or a precision network analyzer.

---

## Step 7: Build Forward -- The Complete Analysis

### 7.1 What Dollard's Framework Predicts Differently (Summary)

| Scenario | Standard prediction | Dollard prediction | Difference | Testable? |
|----------|--------------------|--------------------|------------|-----------|
| Short cable, low freq | P > 0, small loss | P > 0, small loss | ~0 | No |
| Short cable, f = lambda/4 | P > 0, moderate loss | P < 0, moderate gain | ~0.05 dB | Barely |
| Long cable, f = lambda/4 | P > 0, large loss | P < 0, large gain | 10+ dB | YES |
| Tesla coil secondary | High Q amplification by resonance | Same, but attributed to sign flip | ~0 (same measurement) | No |
| Parametric circuit | Gain from pump energy | Gain from "counterspace" | ~0 (same measurement, different interpretation) | Maybe |

### 7.2 Where the Predictions Are IDENTICAL

In every scenario where the system is truly passive and the lumped model
is valid, the predictions are IDENTICAL. The sign flip only produces different
predictions in:
1. Distributed systems near resonance (where the lumped model fails anyway)
2. Active systems with hidden energy sources (where the energy accounting
   differs)

### 7.3 Where the Predictions DIVERGE

The predictions diverge only in the INTERPRETATION of where energy comes from:

- **Standard**: Loss in transmission line comes from R and G (conductor
  resistance and dielectric loss). Gain requires an external source.
- **Dollard**: The "counterspace" (dielectric/magnetic field energy) provides
  a source term that can exceed the loss term under specific conditions.

The physical measurement (voltages, currents, power) would be IDENTICAL
in both frameworks for any system that obeys conservation of energy. The
frameworks diverge only when Dollard predicts energy creation -- and that
prediction is falsified by conservation of energy.

### 7.4 The Honest Answer to Ian's Question

**Q: Is there a SPECIFIC circuit configuration where the standard model predicts
positive real power and an alternative model predicts negative real power?**

A: Yes, but only in two ways:

1. **Active circuits** (containing negative resistance devices, parametric
   amplifiers, or any external energy source). In these systems, the effective
   impedance can have Re(Z) < 0, and Re(ZY) < 0 is real. But standard theory
   already handles this correctly with R < 0. No new algebra is needed.

2. **Distributed systems analyzed with lumped formulas** near resonance. The
   product ZY (per unit length) naturally has Re(ZY) < 0 when w^2 LC > RG
   (the reactive terms dominate). But this is not a sign error in the
   distributed model -- it is a feature of the square root: gamma = sqrt(ZY)
   still has Re(gamma) > 0 (positive attenuation). Dollard may have confused
   the sign of Re(ZY) with the sign of Re(gamma).

**Q: What physical mechanisms COULD produce an effective sign flip?**

A: Negative resistance devices, parametric amplification, and nonlinear
reactance at saturation. All are well-understood, all require an external
energy source, and all are correctly described by standard circuit theory
with R < 0 substituted into the unchanged formula.

**Q: What is the cheapest experiment that would falsify or support the claim?**

A: **100 meters of RG-174 coaxial cable, signal generator at 9.9 MHz,
resistive loads, two-channel oscilloscope.** Total cost: about $200.

- **If output < input** (standard): cable attenuates, sign flip is wrong
- **If output > input** (Dollard): cable amplifies, conservation of energy
  is violated, check for hidden energy sources
- **If output = input** (within measurement error): inconclusive, use
  longer cable or network analyzer

Expected result: output < input. The cable is a passive attenuator. This
is the result observed in every transmission line measurement ever made
on a passive cable without an amplifier.

**Q: Is there any known physics where real power in a passive network appears
to be negative?**

A: Yes, in two senses:

1. **Instantaneous power** is negative during the reactive return phase of
   every cycle in any circuit with inductors or capacitors. This is standard
   reactive power, not a sign error.

2. **Local power flow** can be negative (toward the source) at specific
   points on a transmission line with standing waves. The total
   time-averaged power flow is still positive (source to load), but at
   points between voltage minimum and current minimum, the local
   instantaneous Poynting vector points backward. This is a standing wave
   phenomenon, not a sign error.

Neither of these is what Dollard claims. He claims the FORMULA is different,
not that instantaneous or local power flow can be negative (which is
standard physics).

### 7.5 Where It Matters Most in Dollard's Domain

Dollard's applications are:

1. **Tesla coils**: Distributed resonators with very high Q (100-1000).
   The voltage magnification Q * V_input can be enormous. A naive
   power calculation (P = V^2/R with V = Q * V_input) gives apparent
   power gain of Q^2 -- but this is reactive power being circulated, not
   real power being created. The real power input (from the primary drive
   circuit) equals the real power dissipated (in the coil resistance and
   radiation).

2. **Transmission lines at resonance**: At quarter-wave resonance, a
   transmission line transforms impedance. A short circuit at the far end
   appears as an open circuit at the input. A low impedance load appears as
   a high impedance. This impedance transformation can create the illusion
   of power gain when measuring voltage alone (voltage step-up) but power
   is conserved.

3. **Polyphase power systems**: In a three-phase system, the reactive power
   circulates between phases. The total real power is the sum of three phase
   contributions, each of which can be negative at some instant. A
   single-phase measurement on a three-phase system can show negative
   instantaneous power on one phase while the total is positive.

In EVERY case, the "anomalous" power reading has a standard explanation:
reactive circulation, impedance transformation, or measurement of a subset
of a multi-port system. No sign flip in the ZY formula is needed.

---

## The Vision (Seen from the End)

The sign flip in Dollard's versor form is an algebraic error that, when
interpreted as a physical prediction, would violate conservation of energy
in passive systems. However, the DOMAIN where Dollard works -- distributed
systems near resonance, Tesla coils, high-Q transmission lines -- is precisely
the domain where lumped-element formulas break down and naive application of
ZY = (RG+XB) + j(XG-RB) gives misleading results.

The charitable interpretation is that Dollard observed real physical phenomena
(reactive power circulation, impedance transformation, voltage magnification
at resonance) that are incorrectly described by lumped-element analysis, and
expressed this as a modification to the formula rather than recognizing that
the formula's domain of validity had been exceeded.

The uncharitable interpretation is that the sign flip is a simple algebraic
error that happens to point in the direction of over-unity claims.

The TESTABLE prediction is: **a long passive cable at quarter-wave resonance
will attenuate (standard) or amplify (Dollard) a signal.** Every observation
ever made confirms attenuation. The claim is falsified by routine engineering
measurement.

## The Gap

The gap is not in the mathematics or the physics. The gap is in Dollard's
INTERPRETATION of what his formulas mean. He attributes to a new algebra
what is actually a failure of the lumped-element approximation. The physical
phenomena he describes are real (resonant voltage magnification, reactive
power circulation, distributed impedance transformation). His explanation
of them (sign flip in ZY) is wrong.

## The Bridge

No bridge is needed. Standard distributed-parameter circuit theory
(telegrapher's equations, transmission line theory, standing wave analysis)
correctly describes every phenomenon Dollard observes. The "bridge" is
education: understanding when lumped models fail and distributed models
are required.

## Kill Conditions (Numbered, Testable)

1. **KC-1 (Conservation of energy)**: A passive cable cannot amplify a signal.
   If claimed, identify the hidden energy source. FIRES for any passive-only
   over-unity claim.

2. **KC-2 (Kramers-Kronig)**: The real part of impedance of a passive, causal
   system is non-negative at all frequencies. A broadband measurement of Z(f)
   will confirm or deny.

3. **KC-3 (Thermodynamics)**: A system that outputs more power than it receives
   from all identified sources violates the second law. Calorimetric
   measurement (total heat dissipated vs. total electrical input) is definitive.

4. **KC-4 (Energy source identification)**: Every known negative-resistance
   effect has a specific identified energy source. If Dollard's sign flip
   requires energy from "counterspace," the energy must be measurable and
   depletable.

5. **KC-5 (Distributed model agreement)**: The telegrapher's equations with
   standard ZY always give alpha > 0 for passive media. If a distributed
   measurement shows alpha < 0, the medium is active or the measurement is
   wrong.

## Recommendations

1. **Do NOT build the experiment.** The prediction is falsified by KC-1 through
   KC-5 and by every transmission line measurement ever made. The experiment
   would confirm what is already known.

2. **IF Ian wants to build it anyway** (for pedagogical or demonstration
   purposes), use 100+ meters of lossy cable (RG-174), a signal generator at
   the quarter-wave frequency, and compare input and output power with a
   two-channel oscilloscope. The result will be: output < input. Document this
   as a negative result confirming standard theory.

3. **The real value of this analysis** is the identification of WHERE Dollard's
   intuition points at real physics (distributed systems, reactive circulation,
   lumped model breakdown) even when his algebra is wrong. This belongs in the
   project's assessment of Dollard's contribution: he was working in the right
   DOMAIN (distributed electrical systems near resonance) with the wrong TOOLS
   (modified lumped-element algebra instead of distributed-parameter theory).

4. **For Paper 2 (AACA)**: This analysis supports the friction catalog entry
   A1 (versor form sign error) by showing that even the most charitable
   physical interpretation of the sign flip leads to falsified predictions.

5. **For the N-Phase system**: The quaternary expansion (verified correct) may
   have practical value for analyzing lossy distributed systems where
   simultaneous circular and hyperbolic behavior occurs. This is independent
   of the sign flip and is worth testing computationally.

## Confidence Calibration

| Component | Confidence | Basis |
|-----------|-----------|-------|
| Sign flip violates conservation of energy in passive systems | 99.9% | Thermodynamics, causality, every measurement ever |
| No passive network can have average negative real power | 99.9% | Foster's theorem, Kramers-Kronig, second law |
| Distributed systems can show apparent sign anomalies in lumped analysis | 95% | Standard transmission line theory |
| Dollard's domain (Tesla coils, transmission lines) is where lumped models fail | 90% | Physical analysis of his specific applications |
| The charitable interpretation (lumped model failure, not new physics) is correct | 85% | Consistent with all evidence; 15% reserved for unknown unknowns |
| 100m cable experiment would show attenuation, not amplification | 99.99% | Every cable measurement ever made |
| Experiment is not worth building | 80% | Pedagogically it might be valuable; scientifically it is not |

---

## Appendix A: The ZY Product in Distributed vs. Lumped Models

For a transmission line with series impedance Z = R + jwL (per unit length)
and shunt admittance Y = G + jwC (per unit length):

**Lumped product (per unit length)**:
```
ZY = (R + jwL)(G + jwC)
   = (RG - w^2LC) + jw(RC + LG)
```

At high frequency (w^2LC >> RG):
```
Re(ZY) = RG - w^2LC < 0
```

This is not an error. It is the correct value of Re(ZY). The point is that
the propagation constant is gamma = sqrt(ZY), and:

```
gamma = sqrt(negative_real + j*positive_imaginary)
```

The square root of a complex number with negative real part and positive
imaginary part has POSITIVE real part. So alpha = Re(gamma) > 0 even though
Re(ZY) < 0. The attenuation is always positive for a passive line.

**Dollard's error** (if it is a lumped-model confusion): conflating Re(ZY) < 0
with alpha < 0. These are different statements. The first is true at high
frequency. The second is never true for passive media.

## Appendix B: Specific Numerical Example

**Cable**: RG-58, 50 ohm, 100 meters
**Frequency**: 9.9 MHz (quarter-wave resonance for 5m; 100m = 5 full wavelengths)
**Load**: 100 pF capacitor (Z_load = -j*160.8 ohm)

Per-unit-length parameters at 9.9 MHz:
- R = 0.052 ohm/m (copper loss, including skin effect)
- L = 253 nH/m
- G = 1e-6 S/m (dielectric loss in polyethylene)
- C = 101 pF/m

Computed:
- wL = 2*pi*9.9e6*253e-9 = 15.74 ohm/m
- wC = 2*pi*9.9e6*101e-12 = 6.28e-3 S/m
- ZY = (0.052 + j15.74)(1e-6 + j6.28e-3) = (-0.0988 + j3.27e-4 + j1.57e-5 + j^2*0)
       = -0.0988 + j*0.000343

Actually, computing properly:
```
ZY = (R*G - w^2*L*C) + j*(w*R*C + w*L*G)
   = (0.052*1e-6 - (2*pi*9.9e6)^2 * 253e-9 * 101e-12)
     + j*(2*pi*9.9e6)*(0.052*101e-12 + 253e-9*1e-6)
   = (5.2e-8 - 0.09886) + j*(6.22e7)*(5.252e-12 + 2.53e-13)
   = -0.09886 + j*3.42e-4
```

So Re(ZY) = -0.09886 (negative, as expected at high frequency).

gamma = sqrt(-0.09886 + j*3.42e-4)

The magnitude |ZY| = 0.09886 (to good approximation).
The angle of ZY is approximately pi - 0.00346 radians (just past 180 degrees).

gamma = sqrt(0.09886) * exp(j*(pi - 0.00346)/2)
      = 0.3144 * exp(j*(pi/2 - 0.00173))
      = 0.3144 * (sin(0.00173) + j*cos(0.00173))
      = 0.3144 * (0.00173 + j*0.99999)
      = 0.000544 + j*0.3144

So: alpha = 0.000544 Np/m (positive -- attenuation)
    beta = 0.3144 rad/m (phase constant)

Over 100 meters:
- Total attenuation = 100 * 0.000544 = 0.0544 Np = 0.473 dB
- Signal at output = signal at input * exp(-0.0544) = 0.947 * input

**Standard prediction**: Output is 94.7% of input (5.3% loss).
**"Sign flip" prediction**: Output is 105.6% of input (5.6% gain).

A 10.9% difference in output voltage. THIS IS MEASURABLE with a good
oscilloscope. But the standard prediction is confirmed by every cable
manufacturer's specification sheet. RG-58 at 10 MHz has approximately
0.5 dB/100m loss. This matches our calculation.

## Appendix C: Why Tesla Coils Are Not Evidence

A Tesla coil with Q = 500 produces voltage magnification of 500x at resonance.
This looks like "energy amplification" to a naive observer because:

- Input: 10 V at the primary
- Output: 5000 V at the secondary tip

But the POWER is not amplified:
- Input power: V_in * I_in * cos(phi) = 10V * 2A * 0.01 = 0.2 W (low power factor)
- Output power: V_out * I_out * cos(phi) = 5000V * 0.00004A * 1.0 = 0.2 W (approximately)

The voltage is high because the current is low. Q amplifies voltage at the
expense of current. Total power is conserved (minus resistive losses).

Dollard's sign flip is not needed to explain this. It is standard resonant
circuit behavior, understood since the 19th century by Heaviside, Steinmetz,
and Tesla himself.

---

*Filed by: Heptapod B Architect, 2026-03-17*
*Investigation: dollard-pure-construction, Round 6 (extension)*
*Status: ANALYSIS COMPLETE. Sign flip prediction falsified by conservation laws and standard measurement. Charitable interpretation identified: lumped-model failure in distributed domain.*
