# The Dollard Gestalt — Three Texts, One Insight

**Date**: 2026-03-17
**Tag**: [OUR ANALYSIS] — synthesis across all three Dollard source texts
**Status**: COMPLETE synthesis, informs all downstream work
**Sources**: Lone Pine Writings (2011), Four Quadrant Representation (2013), Versor Algebra (2015)

## The Core Insight

Dollard's notation is not about computing differently. It is about PRESERVING INFORMATION
that standard notation destroys. The four operators {1, j, h, k} are a bookkeeping system
for four distinct directions of energy flow. Collapsing them to two (real/imaginary) loses
the ability to see how much energy is circulating internally versus flowing through.

## Text 1: Lone Pine Writings — The Four Dimensions

Dollard establishes FOUR primary dimensions of electricity:
1. **Time** (metrical)
2. **Space** (metrical)
3. **Dielectricity** (physical — contractive, in counterspace)
4. **Magnetism** (physical — expansive, in space)

Everything else derives from these four. Volts = variation of Phi with time. Amps = variation
of Psi with time. Ohms = ratio of Phi to Psi. Energy itself is a "phantom" — a derivative
that appears only during VARIATION with respect to time. The Planck Q = Phi x Psi is the
fundamental quantity.

Key claim: "Push the Erase Button on your head for two notions: Energy is the product of
mass times the velocity of light squared, erased? Next, Electricity is the flow of electrons
in the wire, erased?"

## Text 2: Four Quadrant Representation — The Physical Geometry

The four quadrants are not mathematical convenience — they are four distinct energy
transfer conditions between fields of induction and an external device:

1. **Magnetic Energy Discharge** — Forward EMF (energy leaving magnetic field)
2. **Dielectric Energy Discharge** — Forward Displacement (energy leaving dielectric field)
3. **Magnetic Energy Charge** — Back EMF (energy entering magnetic field)
4. **Dielectric Energy Charge** — Back Displacement (energy entering dielectric field)

"Four Distinct Conditions exist, a pair for each Field of Induction, one pair the Energy
Transfer between the Drycell and Inductor, (1) charge, (2) discharge, the second pair the
Energy Transfer between the Drycell and Condenser, (3) charge, (4) discharge."

The versor operators {1, j, h, k} correspond to these four directions. The operator carries
the DIRECTION of energy flow. The scalar carries the MAGNITUDE.

## Text 3: Versor Algebra — The Mathematical Formalization

The infinite series of epsilon^j grouped by operator:

```
epsilon^j = 1(u) + j(x) + h(nu) + k(y)     [eq 77]
```

Where u, x, nu, y are the four mod-4 subseries — all positive, all monotonically increasing.
The operators {1, j, h=-1, k=-j} carry the sign/direction structure.

Critical passage (eq 80-83): The "duo-binary form" collapses this to:
```
epsilon^j = (u - nu) + j(x - y) = cos + j*sin    [eq 80-82]
```

Dollard explicitly states: "This duo-binary form neglects the factors" (eq 83).

What is neglected: the individual magnitudes u and nu. When cos(theta) = u - nu = 0.001,
you cannot tell whether u = 0.5005, nu = 0.4995 (healthy, low circulation) or
u = 5,000,000.0005, nu = 4,999,999.9995 (catastrophic cancellation, enormous hidden
circulation). Standard notation gives 0.001 in both cases. Dollard's notation gives you
the components.

## The Gestalt: What the Three Texts Say Together

The progression is:
1. **Lone Pine**: Four fundamental dimensions exist (Time, Space, Dielectricity, Magnetism)
2. **Four Quadrant**: Energy circulates in four directions (charge/discharge x magnetic/dielectric)
3. **Versor Algebra**: The mathematical notation must preserve all four directions separately

The unified claim: **Standard mathematical notation (complex numbers, sin/cos) collapses
four distinct physical processes into two numbers. This is computationally equivalent but
informationally lossy. The lost information is the GROSS circulation — how much energy is
flowing internally without producing external effect.**

Verified algebraically: Dollard's algebra IS Z4 = {1, i, -1, -i}. The computation is identical.
But the REPRESENTATION preserves structure that the collapsed form hides.

## Application to AI/ML: The Quaternary Positional Encoding

The gestalt maps directly onto neural network positional encoding:

| Dollard's domain | AI/ML domain |
|---|---|
| Four quadrants of energy flow | Four channels of positional information |
| Operators carry direction | Channel position carries mode |
| Scalars carry magnitude | Values carry positional weight |
| Net oscillation (cos, sin) | Standard PE (sin/cos) |
| Gross circulation (cosh, sinh) | Scale/growth information |
| Conditioning (cosh/|cos|) | Numerical sensitivity of representation |
| "Duo-binary neglects factors" | sin/cos PE loses growth structure |

Standard sin/cos PE encodes position with two channels that oscillate around zero.
QPE encodes position with four ALWAYS-POSITIVE channels representing four distinct
modes of positional information. The downstream network can selectively attend to:
- OSCILLATORY view (u-v, x-y) = phase/relative position
- GROWTH view (u+v, x+y) = scale/absolute position
- ENERGY view (4uv, 4xy) = cross-mode interaction
- CONDITIONING view (u+v)/|u-v| = numerical sensitivity

This is Dollard's core argument — four quadrants preserve information that two collapse —
applied to information representation instead of electrical energy.

## Machine-Verified Foundation

Every structural property traces to a Lean 4 theorem (9 theorems, 0 sorry):

| Property | Lean theorem |
|---|---|
| u - v = cos(t) | `quaternary_diff_eq_cos` |
| u + v = cosh(t) | `quaternary_sum_eq_cosh` |
| x - y = sin(t) | `quaternary_x_diff_eq_sin` |
| x + y = sinh(t) | `quaternary_x_sum_eq_sinh` |
| u + x + v + y = exp(t) | `quaternary_total_eq_exp` |
| 4uv = sinh^2 + sin^2 | `quaternary_cross_energy` |
| 4xy = sinh^2 - sin^2 | `quaternary_cross_differential` |
| |cos t| <= cosh t | `gross_geq_abs_net` |
| cosh(ln s) = (s+1/s)/2 | `cosh_log_eq_swr` |

File: `src/lean_proofs/foundations/quaternary_identities.lean`

## What Was Killed (and Why)

| Approach | Verdict | Error |
|---|---|---|
| Z4 multiplication as layer | DEAD (spectral radius e^theta) | Tested computation, should test representation |
| Stride-4 Taylor evaluation | DEAD (libm wins 3-26x) | Tested implementation, should test architecture |
| Zero-error finding | DEAD (IEEE 754 coincidence) | Tested numerical artifact, was FP noise |
| DPQA lifted representation | DEAD (exponential error growth) | Tested wrong construction entirely |

## What Survives

1. The REPRESENTATION insight: four positive channels whose differences oscillate
2. The conditioning diagnostic: gross/net ratio as health metric
3. The cross-energy identities: products encode mode interactions
4. The machine-verified foundation: Lean proofs backing all structural claims
5. The source text methodology: follow the author's construction exactly

## References

- Dollard, E. P. "The Lone Pine Writings" (2011/2013), Transmissions 1-10
- Dollard, E. P. "Four Quadrant Representation of Electricity" (2013), esp. Appendix [2]
- Dollard, E. P. "Versor Algebra As Applied to Polyphase Power Systems" (2015), eq 67-83
- QPE proposal: `research/dollard-investigation/2026-03-17-quaternary-positional-encoding.md`
- Domain analysis: `research/dollard-investigation/2026-03-17-stride4-domain-analysis.md`
- Investigation status: `research/dollard-investigation/INVESTIGATION_STATUS.md`
