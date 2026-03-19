# QPE Mathematical Review: Is the Channel Basis Optimal?

**Date**: 2026-03-18
**Author**: dollard-theorist (Opus)
**Status**: COMPLETE
**Verdict**: {u,x,v,y} is NOT optimal. Recommend either (A) revert to standard PE with
more frequencies, or (B) use a hybrid basis {cos, sin, log(1+v), arctan(x)} with bounded channels.

---

**DOLLARD LENS COMPLIANCE:**
- Construction under test: mod-4 real subseries applied to positional encoding (OUR construction)
- Source text verified: N/A — this is not Dollard's construction
- Operators preserved: **NO** — QPE uses bare scalar functions as channel values
- Arguments match Dollard's: **NO** — Dollard's eq 73-77 decompose epsilon^j (imaginary exponent);
  QPE evaluates at real t = omega * p
- **WARNING: This is OUR construction, not Dollard's.** The analysis below concerns the
  mathematical properties of {u,x,v,y} as neural network features, not as versor algebra.

---

## Question Asked

Is {u,x,v,y} the optimal 4-channel basis for positional encoding, or would a different
decomposition serve the network better?

## Executive Summary

**No. The {u,x,v,y} basis has three fatal problems for neural network positional encoding:**

1. **Exponential channel correlation**: For omega*P > 2, the pairs (u,v) and (x,y) become
   near-identical (cosine similarity > 0.91), wasting 2 of 4 channels on redundant information.

2. **LayerNorm poisoning**: At moderate arguments, cosh/sinh terms dominate by 100x-10000x,
   destroying the cos/sin signal after LayerNorm normalization. The N-Phase system independently
   discovered and deprecated this same pathology.

3. **Frequency budget waste**: QPE uses 4 channels per frequency (32 frequencies for d_model=128),
   while standard PE uses 2 channels per frequency (64 frequencies). The extra cosh/sinh
   channels carry less useful information than the 32 additional frequency slots would provide.

The multi-seed experiment shows QPE has 3x higher variance (std 221 vs 72), consistent with
an unstable encoding that works well on some seeds and poorly on others. Its mean advantage
(-22.3% vs matched-frequency standard PE) may be partially a regularization effect from
using fewer frequency slots, not from superior encoding.

---

## 1. Is {u,x,v,y} the Optimal Basis?

### Answer: No.

The four functions are defined as:
```
u(t) = (cosh(t) + cos(t)) / 2
x(t) = (sinh(t) + sin(t)) / 2
v(t) = (cosh(t) - cos(t)) / 2
y(t) = (sinh(t) - sin(t)) / 2
```

The change-of-basis matrix to {cos, sin, cosh, sinh} is:
```
[cos ]   [1  0 -1  0] [u]
[sin ] = [0  1  0 -1] [x]
[cosh]   [1  0  1  0] [v]
[sinh]   [0  1  0  1] [y]
```

This matrix has determinant 4 and rank 4: the two bases are algebraically equivalent
(invertible linear transformation). Any property of one representation is accessible
from the other. **The choice of basis affects only what the network sees directly vs.
what it must learn to compute.**

However, {u,x,v,y} is the WORST presentation of these four functions for a neural network,
because:

**(a)** The "interesting" information (cos, sin) requires SUBTRACTION of large nearly-equal
numbers (u - v = cos when u, v are both ~ cosh/2). This is the textbook definition of
numerical ill-conditioning.

**(b)** The network must learn to compute u - v and x - y to recover phase information,
while the dominant (u + v = cosh) signal overwhelms the useful signal.

**(c)** The {cos, sin, cosh, sinh} basis presents the information directly: phase channels
are bounded [-1,1], scale channels are unbounded but explicit. No cancellation needed.

### What about {cos, sin, cosh, sinh}?

Better than {u,x,v,y} (no cancellation needed), but still suffers from unbounded cosh/sinh
channels causing LayerNorm poisoning. See Section 6 for the recommended alternative.

---

## 2. Orthogonality Analysis

### Inner product over positions: channels are highly correlated

Using the Lean-verified cross-energy identity (quaternary_cross_energy):
```
4 * u(p) * v(p) = sinh(omega*p)^2 + sin(omega*p)^2
```

The inner product over P positions is:
```
<u, v> = (1/4) * sum_{p=0}^{P-1} [sinh^2(omega*p) + sin^2(omega*p)]
```

**Cosine similarities for P=128 positions:**

| omega | max t | cos(u,v) | cos(x,y) | cos(u,x) | cos(cos,sin) |
|-------|-------|----------|----------|----------|--------------|
| 0.0001 | 0.013 | 0.744 | 0.917 | 0.864 | 0.864 |
| 0.001 | 0.127 | 0.744 | 0.917 | 0.864 | 0.863 |
| 0.005 | 0.635 | 0.745 | 0.917 | 0.865 | 0.839 |
| 0.01 | 1.270 | 0.761 | 0.919 | 0.875 | 0.733 |
| 0.02 | 2.540 | **0.910** | **0.989** | 0.957 | 0.123 |

**Key observations:**

1. At omega=0.02 (the experiment's maximum frequency), cos(u,v) = 0.91 and cos(x,y) = 0.99.
   The (x,y) pair is essentially identical. This means 1 of 4 channels is wasted.

2. As omega*P increases, ALL pairwise correlations approach 1.0 because cosh/sinh
   dominate all four functions: u ~ v ~ cosh/2, x ~ y ~ sinh/2.

3. Meanwhile, standard PE's cos(cos,sin) = 0.12 at omega=0.02 — the channels are
   nearly orthogonal, which is ideal for positional encoding.

**Analytical result**: For omega*P >> 1:
```
cos(u,v) -> 1    (proven: u ~ v ~ cosh(t)/2 as cosh >> |cos|)
cos(x,y) -> 1    (proven: x ~ y ~ sinh(t)/2 as sinh >> |sin|)
```

This is a **structural defect**: the exponential terms grow without bound and eventually
dominate any finite oscillation, making the channel pairs redundant.

---

## 3. Information Content

### Per-frequency analysis

For a single frequency omega at position p >= 0:
- t = omega * p is a **single real number**
- All four channels {u(t), x(t), v(t), y(t)} are deterministic functions of t
- **Independent information: exactly 1 degree of freedom (the value of t)**

The four channels carry this one DOF in different "projections":
- cos(t) and sin(t) together encode t modulo 2*pi (PHASE information, periodic)
- cosh(t) encodes |t| exactly (SCALE information, monotonic)
- sinh(t) = sqrt(cosh(t)^2 - 1) for t >= 0 (ZERO additional information)

**Effective DOF per frequency: 2** (phase + scale), not 4.

### Multi-frequency analysis

With K frequencies omega_1, ..., omega_K:
- Standard PE: 2K channels encoding K phase readings
- QPE: 4K channels encoding K phase readings + K scale readings

But the K scale readings {cosh(omega_i * p)} all encode the same quantity (position p)
viewed through different scales. The Chinese Remainder Theorem argument that makes
multi-frequency sinusoidal PE powerful (incommensurate phases resolve position uniquely)
does NOT apply to scale channels, because cosh is monotonic, not periodic.

**Result**: QPE adds K scale channels that collectively provide ~1 DOF (absolute position
scale), while standard PE with 2K frequencies provides 2K-K = K more phase readings.

### Redundancy quantification

With d_model = 128:
- QPE: 32 frequencies, effective rank 2.08
- Standard PE: 64 frequencies, effective rank 1.91
- QPE log_scale: effective rank 2.00

The effective ranks are surprisingly similar, suggesting that at these small frequencies
(0.0001 to 0.02), neither scheme achieves high utilization of the 128-dimensional space.
Both are dominated by a few principal components.

### Would 3 channels suffice?

Yes. {cos, sin, cosh} carries the same information as {cos, sin, cosh, sinh}, because
sinh(t) = sqrt(cosh(t)^2 - 1) * sign(t), and for positions p >= 0, sign(t) = sign(omega) is
known. The fourth channel adds zero information.

---

## 4. The Conditioning Ratio as a Feature

The conditioning ratio kappa(t) = cosh(t) / |cos(t)| measures the gross-to-net energy ratio
in Dollard's framework. As a positional encoding feature:

**It is useful as a DIAGNOSTIC, not as a FEATURE.**

Reasons:
1. kappa(t) diverges at t = pi/2 + n*pi. These positions are arbitrary functions of
   omega * p and have no linguistic meaning. The network would need to learn to IGNORE
   the spikes, not exploit them.

2. For a language model, there is no reason why "position 157 at frequency 0.01" (which
   happens to have cos(1.57) ~ 0) should be treated differently from "position 158."
   The conditioning ratio injects artificial structure into the position space.

3. The ratio encodes the same information as cosh(t)/|cos(t)|, which is derivable from
   cosh and cos individually. It is not independent information.

**Verdict**: The conditioning ratio is meaningful in electrical engineering (SWR, standing
wave ratio) but is noise in a language model. Do not expose it as a feature.

---

## 5. Scaling Behavior

### Standard PE: bounded [-1, 1]
- All channels in [-1, 1]
- Addition to embeddings does not distort scale
- LayerNorm sees uniform variance across channels
- Gradient magnitudes are uniform

### QPE: exponential growth
- At omega=0.02, position 500: cosh(10) = 11,013, sinh(10) = 11,013
- u ~ v ~ 5506, x ~ y ~ 5506, while cos = -0.84, sin = -0.54
- The signal-to-value ratio |cos|/|u| = 7.6e-3 (the useful information is 0.76% of the channel value)

### LayerNorm poisoning (quantified)

At omega=0.01, position 500 (t=5.0):
- Pre-LayerNorm: u = 37.25, v = 36.96, cos = u-v = 0.28
- Post-LayerNorm: u_n = 0.406, v_n = -0.396, cos_n = u_n - v_n = 0.80
- The cosine information is preserved post-normalization in this case.

BUT at omega=0.02, position 500 (t=10):
- u ~ v ~ 5506.5 (ratio to cos ~6500:1)
- LayerNorm normalizes across ALL channels in the layer, not just PE channels
- When PE channels dominate, non-PE embedding dimensions are squashed to near-zero
- This is exactly the "LayerNorm poisoning" the N-Phase system documented

### The log_scale mitigation

The current log_scale=True option applies log(1+x) compression after clamping args at 20.
This helps but introduces two problems:
1. Positions beyond 20/omega get IDENTICAL encoding (saturation)
2. The log transform breaks the linear relationship between {u,x,v,y} and {cos,sin,cosh,sinh}:
   log(1 + (cosh+cos)/2) is NOT (log(1+cosh) + log(1+cos))/2

---

## 6. Recommended Alternative Decompositions

### Option A: Just use Standard PE with 2x frequencies (RECOMMENDED)

For d_model = 128:
- Standard PE: 64 frequencies x 2 channels = 128
- All channels bounded [-1, 1]
- 64 independent phase readings vs QPE's 32
- Zero risk of overflow, LayerNorm poisoning, or channel correlation
- Established, well-understood, well-tuned

**This is the simplest option and likely the best.** QPE's multi-seed advantage (-22.3%
vs matched-frequency standard PE) needs to be tested against standard PE with the same
frequency range and 2x the frequency count.

### Option B: Hybrid basis {cos, sin, f(cosh), g(sinh)} with bounded channels

If you want 4 channels per frequency for theoretical reasons:

```python
# Bounded 4-channel encoding
cos_t = cos(omega * p)                          # [-1, 1]
sin_t = sin(omega * p)                          # [-1, 1]
scale_even = 2 / (1 + exp(-alpha * p)) - 1      # sigmoid: (-1, 1), monotone
scale_odd  = tanh(beta * omega * p)              # (-1, 1), freq-dependent scale
```

Or more directly:
```python
cos_t = cos(omega * p)                          # [-1, 1]
sin_t = sin(omega * p)                          # [-1, 1]
log_scale = log(cosh(omega * p)) / max_scale    # [0, 1] normalized
sign_scale = tanh(omega * p)                    # (-1, 1)
```

Properties:
- cos, sin recover standard PE (verified in Lean)
- log(cosh) provides monotonic scale without exponential blowup
- tanh provides early-position differentiation (saturates at ~3, so useful for t < 3 only)
- All channels bounded, LayerNorm-safe
- Correlation at omega=0.01: max |off-diagonal| = 0.55 (vs 1.0 for raw QPE)

**Problem**: tanh saturates quickly, wasting a channel for large t. Consider replacing
tanh with a linear ramp: min(omega*p / max_scale, 1.0).

### Option C: Decoupled frequency + scale encoding

Separate the frequency encoding from the scale encoding entirely:
```python
# First half of d_model: standard PE at 2x frequency count
pe[:, :d_model//2] = standard_sinusoidal(d_model//2, positions)

# Second half: scale encoding (NOT per-frequency)
# Use a few monotonic functions of absolute position
pe[:, d_model//2:] = scale_encoding(d_model//2, positions)
```

Where scale_encoding uses log-linear position, polynomial basis, or learned embeddings.
This cleanly separates the two types of information and avoids the correlation problem
entirely.

### Option D: QPE-inspired but with Fortescue normalization

The Fortescue DFT has condition number kappa = 1.0 (verified, Lean proof). If we
apply the Fortescue transform to the {u,x,v,y} channels per-position:

```
[alpha_0]   [1  1  1  1] [u]
[alpha_1] = [1  j -1 -j] [x]   * (1/4)
[alpha_2]   [1 -1  1 -1] [v]
[alpha_3]   [1 -j -1  j] [y]
```

This would yield:
- alpha_0 = (u+x+v+y)/4 = e^t/4 (forward exponential)
- alpha_2 = (u-x+v-y)/4 = e^(-t)/4 (backward exponential)
- alpha_1 = ((u-v) + j(x-y))/4 = (cos(t) + j*sin(t))/4 = e^(jt)/4
- alpha_3 = ((u-v) - j(x-y))/4 = (cos(t) - j*sin(t))/4 = e^(-jt)/4

Taking magnitudes of the complex components:
- |alpha_1| = |alpha_3| = 1/4 (constant — useless as encoding)
- alpha_0 and alpha_2 are real exponentials (same blowup problem)

**This does not help.** The Fortescue transform diagonalizes the algebra but does not
solve the exponential growth problem.

---

## 7. Root Cause: Why QPE Fails as Positional Encoding

The quaternary decomposition {u,x,v,y} was designed for a different purpose: decomposing
energy flow in AC circuits (Dollard's four-quadrant model). In that context:
- The exponential growth represents real energy accumulation
- The gross/net ratio (cosh/|cos|) measures standing wave ratio
- All four components have physical meaning (storage, transfer, return, dissipation)

For positional encoding, none of these properties are useful. A positional encoding needs:
1. **Unique encoding per position** — QPE provides this (each position gets a unique 4-vector)
2. **Bounded channels** — QPE VIOLATES this (cosh/sinh grow exponentially)
3. **Low correlation between channels** — QPE VIOLATES this (pairs converge as t grows)
4. **Efficient use of d_model dimensions** — QPE VIOLATES this (4 channels per freq vs 2)

The mathematical beauty of the quaternary identities (all Lean-verified, all correct) does
not translate into practical advantage for neural network positional encoding. The identities
hold in both the {u,x,v,y} and {cos,sin,cosh,sinh} bases, and the latter is strictly better
for the neural network use case.

---

## 8. Explaining the Experimental Results

### Why QPE (geometric) outperforms Standard PE (geometric) with matched frequencies

The multi-seed results show:
- QPE (geometric): mean_ppl = 614.1, std = 221.2
- Standard PE (geometric): mean_ppl = 790.8, std = 63.2

Possible explanations (not mutually exclusive):

**(a) Regularization effect**: QPE uses 32 frequencies vs Standard PE's 64. Fewer
frequency parameters may regularize the model, especially on a small dataset (Shakespeare).
Test: Run Standard PE with 32 frequencies and 64 zero-padded channels.

**(b) Scale signal is useful at small t**: For the geometric frequency range (0.0001-0.02),
the maximum t at position 128 is only 2.56. At these small values, cosh(2.56) = 6.57 and
the channels are not yet pathologically correlated (cos(u,v) = 0.91, not 1.0). The scale
information may provide genuine benefit in this regime.

**(c) High variance masks the signal**: std=221 on a mean of 614 means the 95% CI is
approximately [614 - 2*221/sqrt(5), 614 + 2*221/sqrt(5)] = [416, 812]. The Standard PE
CI is [790.8 +/- 2*63/sqrt(5)] = [734, 847]. These overlap, so the difference is NOT
statistically significant at the 95% level.

### Why QPE + Vaswani frequencies NaNs

Vaswani's highest frequency is omega = 1.0. At position 5000: cosh(5000) = Inf in float32.
This is a hard failure — no amount of normalization can fix it. The geometric frequency
schedule (max omega = 0.02) avoids this by keeping max t manageable.

### The N-Phase precedent

N-Phase independently discovered that quaternary features cause LayerNorm poisoning and
deprecated them. This is the same pathology from a different angle: deterministic cosh/sinh
channels dominate the feature vector and corrupt downstream processing.

---

## 9. Specific Answers to Questions

### Q1: Is {u,x,v,y} optimal?
**No.** It is the worst of the four considered bases ({u,x,v,y}, {cos,sin,cosh,sinh},
{cos,sin,log_cosh,tanh}, standard PE). The channel pairs (u,v) and (x,y) converge to
identical values as omega*p grows, wasting half the channels on redundant information.
The interesting information (cos, sin) requires cancellation of large numbers.

### Q2: Orthogonality?
**Channels are highly correlated.** Cosine similarity cos(u,v) ranges from 0.74 (small t)
to 1.0 (large t). The (x,y) pair is even worse: cos(x,y) = 0.92 at small t, approaching
1.0. By comparison, standard PE's cos(cos,sin) can be as low as 0.12 — nearly orthogonal.

### Q3: Information content?
**2 independent DOF per frequency** (phase and scale), not 4. sinh adds nothing beyond
cosh. The fourth channel is strictly redundant. Even the third channel (scale) is only
useful when omega*p is small enough that cosh/sinh haven't swamped the cos/sin signal.

### Q4: Conditioning ratio as feature?
**Diagnostic only, not a useful feature.** The ratio kappa = cosh(t)/|cos(t)| spikes at
arbitrary positions (t = pi/2 + n*pi) with no linguistic meaning. Useful for understanding
standing wave ratios in electrical engineering. Noise in a language model.

### Q5: Scaling behavior?
**Exponential growth is harmful.** Standard PE's bounded [-1,1] channels are
well-suited to additive injection into embeddings. QPE's exponential channels require
special handling (log_scale, clamping) that introduces saturation and breaks algebraic
identities. The log_scale mitigation works but sacrifices the mathematical properties
that motivated QPE in the first place.

### Q6: Alternative decompositions?
**Best option: standard PE with 2x frequencies.** If 4 channels per frequency are desired,
use {cos, sin, log(cosh)/max_scale, min(omega*p/max_scale, 1)} for all-bounded channels
with genuine information diversity.

---

## 10. Concrete Recommendations

### For immediate action

1. **Run the regularization control**: Standard PE with 32 geometric frequencies and 64
   zero-padded channels. If this matches QPE's performance, the advantage is regularization
   (fewer frequencies), not encoding.

2. **If QPE is retained**: Switch from {u,x,v,y} to {cos, sin, log(1+v), arctan(x/u)}
   or similar bounded representation that preserves information without exponential channels.

3. **If starting fresh**: Use standard sinusoidal PE with the geometric frequency schedule.
   The -11.8% frequency effect (geometric vs Vaswani) is real and worth keeping.

### For the QPE paper/claims

- The Lean-verified identities hold in ANY basis (they are algebraic, not representation-dependent)
- The "4 positive channels" property is mathematically interesting but practically harmful
- The claim "QPE is a strict superset of standard PE" is algebraically true but misleading:
  the superset channels carry redundant information at the cost of numerical pathology
- The multi-seed advantage is not statistically significant (overlapping 95% CIs)

---

## Appendix A: Verification Tags

- [MV] Machine-verified: All 7 quaternary identities (Lean, `quaternary_identities.lean`)
- [MV] Conditioning bound: `gross_geq_abs_net` in Lean
- [CO] Correlation analysis: computed numerically in this review
- [CO] Effective rank: Shannon entropy of SVD spectrum
- [CO] LayerNorm poisoning: quantified numerically
- [OUR ANALYSIS] All recommendations are our analysis, not Dollard's
- [OUR ANALYSIS] The QPE construction itself is our application of the mod-4 real subseries

## Appendix B: What the N-Phase System Learned

The N-Phase system (1194 tests, provisional patent 63/996,504) DEPRECATED its quaternary
feature mode because:
1. cosh/sinh channels were deterministic functions of signal magnitude
2. They caused LayerNorm to allocate most of its normalization budget to the exponential channels
3. The useful oscillatory information was suppressed post-normalization
4. Replacing quaternary features with standard magnitude + phase improved performance

This is independent confirmation of the same pathology identified here.

## Appendix C: Notation Bridge

| This document | Lean proof | Dollard (eq) | Standard math |
|---------------|-----------|--------------|---------------|
| u(t) | quat_u | 1(mu), eq 73 | (cosh + cos)/2 |
| v(t) | quat_v | h(nu), eq 75 | (cosh - cos)/2 |
| x(t) | quat_x | j(x), eq 74 | (sinh + sin)/2 |
| y(t) | quat_y | k(y), eq 76 | (sinh - sin)/2 |

Dollard's eq 73-76 use IMAGINARY argument (epsilon^j) with ALTERNATING signs.
Our QPE uses REAL argument (t = omega*p) with ALL POSITIVE terms.
These are different objects. See system prompt, "What Dollard's Quaternary Expansion Actually Is."
