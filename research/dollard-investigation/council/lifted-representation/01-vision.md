# Round 1: VISION -- Structural Requirements for a Useful Lifted Representation

**Investigation**: lifted-representation
**Round**: 1 of 5
**Agent**: heptapod-b-architect (teleological reasoning)
**Date**: 2026-03-17

---

## Preamble: What Prior Councils Settled

Two prior councils answered two different questions:

1. **dollard-pure-construction**: The algebra IS Z4. No new content. CLOSED.
2. **quaternary-performance**: Computing cos(t) via u - v is 15-68x WORSE than standard Taylor. The stride-4 recurrence saves 40% of FLOPs, but that's niche. CLOSED.

Neither council asked: *what if you never compute cos(t)?* That is the open question.

---

## Step 1: Assume the Solution Exists

The lifted representation IS useful. There exist algorithms that work entirely in the (u, x, v, y) basis, never project to cos/sin, and achieve measurable advantages in numerical conditioning. I am reading the solution. What does it say?

**What "solved" looks like**: A class of computations -- identifiable, non-trivial, occurring in real engineering -- where:
- All intermediate values are combinations of {u, x, v, y} (all-positive-term series)
- No subtraction u - v or x - y occurs until the final output (if ever)
- The resulting computation achieves >2x better conditioning near resonance compared to the equivalent standard-function computation
- The FLOP overhead of working in the lifted basis is bounded and amortized over the computation chain

---

## Step 2: Necessary Structure of a Useful Lifted Representation

For the lifted (u, x, v, y) representation to be genuinely useful, it MUST satisfy these conditions. These are logical necessities, not guesses. If ANY fails, the approach is dead.

### N1. Operation Closure
The lifted space must be CLOSED under the operations that algorithms need. If every interesting computation requires projecting to cos/sin as an intermediate step, there is no benefit to staying lifted.

**Status: SATISFIED.** The quaternary representation is closed under:

| Operation | In lifted space | Cancellation? |
|-----------|----------------|---------------|
| Argument addition (t₁+t₂) | Cyclic convolution in Z₄ algebra | **None** -- all terms are products of positives, summed |
| Differentiation d/dt | Cyclic shift: (u,x,v,y) → (y,u,x,v) | **None** -- permutation of positive values |
| Integration ∫dt | Cyclic shift: (u,x,v,y) → (x,v,y,u) with constants | **None** |
| Linear combination | Componentwise: α(u₁,x₁,v₁,y₁) + β(u₂,...) | **None** if α,β > 0; possible if mixed sign |
| Scalar multiplication of argument | Multiply then use argument addition | **None** in multiplication step |
| Gross energy extraction | u + v = cosh(t), x + y = sinh(t) | **None** -- addition of positives |

**Critical computation -- argument addition (multiplication in Z₄ algebra)**:

Given quaternary vectors for arguments t₁ and t₂, the quaternary vector for t₁+t₂ is:

```
u(t₁+t₂) = u₁u₂ + x₁y₂ + v₁v₂ + y₁x₂
x(t₁+t₂) = u₁x₂ + x₁u₂ + v₁y₂ + y₁v₂
v(t₁+t₂) = u₁v₂ + x₁x₂ + v₁u₂ + y₁y₂
y(t₁+t₂) = u₁y₂ + x₁v₂ + v₁x₂ + y₁u₂
```

Every term is a product of two positive numbers. Every component is a sum of four such products. **No subtraction anywhere.** This is cyclic convolution over Z₄, and it is unconditionally well-conditioned.

Compare to the standard addition formula: cos(t₁+t₂) = cos(t₁)cos(t₂) - sin(t₁)sin(t₂). This has a subtraction that becomes catastrophic when cos(t₁)cos(t₂) ≈ sin(t₁)sin(t₂) -- i.e., when t₁+t₂ ≈ π/2 (resonance).

### N2. Deferred Projection
The projection step (u-v, x-y) must be deferrable to the FINAL output. If some intermediate operation forces early projection, the benefit collapses.

**Status: SATISFIED for the closed operations above.** Multiplication, differentiation, integration, and linear combination all stay within the lifted space. Projection is needed only when the algorithm's consumer requires cos(t) or sin(t) directly.

### N3. The Extra Information Must Have Independent Value
Carrying 4 values instead of 2 (or 1) costs memory and FLOPs. The extra information must be worth carrying -- either because it serves a distinct purpose (monitoring, diagnostics) or because discarding it early is lossy.

**Status: SATISFIED.**
- u + v = cosh(t): the "gross magnitude" of the oscillatory system. Has independent physical meaning in energy analysis. Always well-conditioned.
- (u+v)/(u-v) = cosh(t)/cos(t): the conditioning indicator. Tells you, from data you already carry, whether projection will be lossy.
- u/v ratio: resonance proximity. u ≈ v means you're near a zero of cosine. Detectable without computing the zero.

### N4. There Must Exist Real-World Domains
A theoretical advantage that applies to no real computation is not an advantage.

**Status: PLAUSIBLE but UNVERIFIED.** Candidate domains identified in Step 3 below.

### N5. The FLOP Overhead Must Be Bounded
The quaternary cyclic convolution (argument addition) costs 16 multiplications + 12 additions = 28 FLOPs. The standard four-function addition formulas cost 8 multiplications + 4 additions = 12 FLOPs (for cos, sin, cosh, sinh of t₁+t₂ given all four of t₁ and t₂). The lifted approach is 2.3x more expensive per step.

**Status: CONDITIONALLY SATISFIED.** The 2.3x FLOP overhead is acceptable IF:
- The computation chains enough operations that the conditioning advantage matters (accumulation of error over a chain), OR
- The final projection is never needed (gross energy analysis), OR
- A single ill-conditioned projection at the end is cheaper than ill-conditioned intermediates at every step

---

## Step 3: Inventory of Existing Deferred-Projection Systems

The idea of "stay in a richer representation, project late" is not new. But each instance has different characteristics. Using the structural-fusion method, I classify the parallels:

### 3.1 Homogeneous Coordinates → Cartesian
- **Mechanism**: Carry (x, y, w) ∈ ℝ³, project to (x/w, y/w) ∈ ℝ².
- **Singularity avoided**: Division by w = 0 (point at infinity).
- **Operation closure**: Projective transformations are linear in homogeneous coords; perspective division is nonlinear in Cartesian.
- **Verdict**: **ANALOGY (75%)**. Both carry extra dimension to avoid singularity at projection. Both have operations that are simpler in lifted space. Break: homogeneous coords are a quotient space (rays through origin); quaternary components are NOT a quotient -- (u,v) and (αu, αv) represent different arguments.

### 3.2 Log-Space Computation
- **Mechanism**: Carry log(x) instead of x. Multiplication → addition. Products of small numbers → sums of large negatives (no underflow).
- **Singularity avoided**: Underflow in products of probabilities.
- **Operation closure**: Multiplication and powers are closed. Addition requires logsumexp trick.
- **Verdict**: **ANALOGY (55%)**. Both re-represent to avoid numerical pathology. Break: log-space is bijective on ℝ⁺; quaternary is 4-to-2 redundant. Log-space makes multiplication easier but addition harder; quaternary makes argument addition easier but pointwise multiplication harder.

### 3.3 expm1(x) / log1p(x) Special Functions
- **Mechanism**: Compute exp(x)-1 or log(1+x) directly, avoiding catastrophic cancellation near x=0.
- **Singularity avoided**: exp(x)-1 ≈ 0 for small x.
- **Verdict**: **ANALOGY (70%)**. Closest parallel in spirit. Both defer a lossy subtraction. Both are special functions designed for a specific cancellation regime. Break: expm1/log1p are single-function patches; the quaternary lift is a SYSTEMATIC framework covering all four trig/hyp functions simultaneously.

### 3.4 Compensated (Kahan) Summation
- **Mechanism**: Carry (sum, compensation) pair. Each addition step computes the exact error and stores it.
- **Singularity avoided**: Accumulated rounding error in long sums.
- **Operation closure**: Addition is closed. Other operations require extension.
- **Verdict**: **ANALOGY (60%)**. Both carry extra data through a pipeline. Break: Kahan's extra value is an ERROR CORRECTION term; quaternary's extra values carry INDEPENDENT PHYSICAL QUANTITIES (gross energy). Kahan is about precision of one number; quaternary is about avoiding cancellation between two.

### 3.5 Double-Double Arithmetic
- **Mechanism**: Represent one number as (hi, lo) where value = hi + lo, with hi carrying the high bits and lo carrying the low bits.
- **Singularity avoided**: Precision loss in double-precision arithmetic.
- **Operation closure**: All arithmetic operations are closed (with care).
- **Verdict**: **ANALOGY (65%)**. Both carry a pair of values that combine to give the desired result. Both have operations that keep the pair separated. Break: double-double approximates ONE number with extra precision; quaternary represents TWO independent quantities (cos and cosh) that happen to share a factored representation.

### 3.6 Redundant Number Representations (Carry-Save, Signed-Digit)
- **Mechanism**: Use redundant digit representation to avoid carry propagation.
- **Singularity avoided**: O(n) carry chains in addition.
- **Verdict**: **ANALOGY (50%)**. Both use redundancy for operational benefit. Break: redundant number systems improve LATENCY; quaternary improves CONDITIONING. Different bottlenecks.

### 3.7 Stochastic Gradient Estimation (REINFORCE vs. Reparameterization)
- **Mechanism**: Reparameterization trick: instead of computing ∇_θ E_{p(z|θ)}[f(z)] (high variance), reparameterize z = g(ε, θ) with ε ~ p(ε) and compute ∇_θ f(g(ε,θ)) (low variance).
- **Singularity avoided**: Variance explosion in score-function estimators.
- **Verdict**: **ANALOGY (45%)**. Distant parallel. Both reroute computation through a better-conditioned path. Break: reparameterization changes the estimator; quaternary changes the representation of the same computation.

### Summary: No Exact Identity Found

The quaternary lifted representation is NOT a known technique under a different name. It is closest in spirit to expm1/log1p (deferring a specific cancellation) but operates on a systematic algebraic framework (Z₄ group algebra) rather than being a single-function patch. The structural parallels are all ANALOGIES, not IDENTITIES.

**Kill condition K3 (known technique) preliminary status: DOES NOT FIRE.** But Round 2 (literature search) must search more thoroughly.

---

## Step 4: The Precise Gap

**What we NEED (from Step 2)**:
- N1: Operation closure ✓ (verified algebraically)
- N2: Deferred projection ✓ (verified)
- N3: Independent value of extra information ✓ (cosh, conditioning indicator)
- N4: Real-world domains that benefit — **GAP**
- N5: Bounded FLOP overhead — **PARTIALLY GAP** (overhead is 2.3x per multiplication; need to know if it amortizes)

**What we HAVE (from Step 3)**:
- Structural parallels to 7 deferred-projection systems (all analogies, no identities)
- Algebraic closure proof for key operations
- No known prior art for this specific technique

**The precise gap is twofold**:

**Gap A (Empirical)**: We need concrete measurements showing that chained quaternary operations near resonance achieve >2x better conditioning than the equivalent standard computation. The algebra proves no cancellation occurs in the lifted space. The question is whether this matters IN PRACTICE -- does error actually accumulate differently?

**Gap B (Domain)**: We need at least one realistic computation where:
1. The algorithm chains multiple operations (argument additions, differentiations) in the oscillatory domain
2. Some of those operations occur near resonance (cos ≈ 0)
3. The final output is either a gross quantity (cosh, energy) or can tolerate a single final projection
4. The 2.3x FLOP overhead per operation is acceptable

---

## Step 5: Bridge Design -- What a Useful Lifted Computation Looks Like

### 5.1 The Design Pattern

**Name**: Deferred-projection quaternary arithmetic (DPQA)

**Operational description** (before formalism):
- Represent oscillatory state as a 4-vector (u, x, v, y) ∈ ℝ⁴₊ (all positive)
- Advance time / add arguments via cyclic convolution (28 FLOPs, no cancellation)
- Extract gross quantities (u+v, x+y) freely at any point (always well-conditioned)
- Extract net quantities (u-v, x-y) ONLY at the final output, or use compensated subtraction
- Monitor conditioning via the ratio (u+v)/|u-v| = cosh/|cos| at any point (free, from data already carried)

**When to use**: Computations that chain ≥3 argument additions near resonance and need either (a) gross quantities or (b) the final answer with controlled precision loss.

**When NOT to use**: Single evaluations; algorithms that need cos(t) at every step; anything where compiled library functions suffice.

### 5.2 The Critical Test: Chained Argument Addition

The strongest case for DPQA is a CHAIN of operations:

**Standard chain**: Compute cos(t₁ + t₂ + ... + tₙ) by iterating:
```
cos(s₀) = cos(t₁)
cos(sₖ) = cos(sₖ₋₁)cos(tₖ₊₁) - sin(sₖ₋₁)sin(tₖ₊₁)
```
Each step has a subtraction. If any intermediate sₖ is near π/2, the subtraction is catastrophic, AND the error propagates forward through all subsequent steps.

**DPQA chain**: Compute (u, x, v, y) for t₁ + t₂ + ... + tₙ by iterating cyclic convolutions:
```
(u₀, x₀, v₀, y₀) = quaternary(t₁)
(uₖ, xₖ, vₖ, yₖ) = cyclic_conv((uₖ₋₁, ..., yₖ₋₁), quaternary(tₖ₊₁))
```
No subtraction at any step. Error does not accumulate from cancellation. Project ONCE at the end: cos(Σtᵢ) = uₙ - vₙ.

**Predicted advantage**: For a chain of n operations passing through k resonance points, the standard chain accumulates ~k × (cosh/|cos|) conditioning penalty at each resonance. The DPQA chain accumulates NO conditioning penalty until the single final projection. The advantage should scale with k.

### 5.3 Candidate Domains

**Domain 1: High-Q resonator simulation**
- Chain of many phase advances near resonance frequency
- Gross energy (cosh) is often the quantity of interest
- Near-resonance conditioning is a known numerical issue
- **Likelihood of benefit**: HIGH

**Domain 2: Power systems Fortescue analysis at resonance**
- Three-phase systems near harmonic resonance
- Fortescue decomposition into positive/negative/zero sequences
- Near-resonance: sequence components nearly cancel
- **Likelihood of benefit**: MEDIUM (3-phase uses Z₃, not Z₄, but the principle generalizes to mod-N)

**Domain 3: Phase-locked loop (PLL) simulation**
- PLL tracking involves iterative phase updates
- Near lock: the phase error oscillates near a resonance-like condition
- The "lock detector" is a gross/net ratio (analogous to cosh/cos)
- **Likelihood of benefit**: MEDIUM

**Domain 4: Orbital mechanics at commensurability**
- Mean-motion resonances (e.g., Jupiter:Saturn 5:2) involve iterated angle combinations
- Near commensurability: cos(nλ₁ - mλ₂) ≈ 0 oscillates through zero repeatedly
- Long integrations chain thousands of steps through resonance
- **Likelihood of benefit**: MEDIUM-HIGH (but this community uses specialized integrators)

**Domain 5: Neural network with quaternary activations**
- Novel: design activation function as (u(t), v(t)) pair
- Gradients du/dt = y, dv/dt = x are well-conditioned (positive-term series)
- Near-resonance: no gradient pathology (no -sin(t) in the gradient path)
- **Likelihood of benefit**: SPECULATIVE (no existing architecture to compare against)

**Domain 6: Digital signal processing near Nyquist**
- DFT involves sums of cos(2πkn/N) terms
- Near Nyquist: frequencies are near π, cos(π) = -1, and beat frequencies produce near-zero cosines
- Could the DFT be restructured to work with quaternary components?
- **Likelihood of benefit**: LOW (FFT is already highly optimized; restructuring would lose FFTW-level optimization)

---

## Step 6: Kill Conditions

| ID | Kill Condition | Test | Status | Round |
|----|---------------|------|--------|-------|
| K1 | No lifted computation exists | Show that no non-trivial algorithm works entirely in (u,x,v,y) | **CLEAR**: cyclic convolution, differentiation, integration are all closed | 1 |
| K2 | Trivial advantage | Chained DPQA achieves <2x conditioning improvement in ALL tested scenarios | Untested | 4 |
| K3 | Known technique | Literature search finds this published under another name | Preliminary: no exact match found (all analogies, no identities) | 2 |
| K4 | Mathematical impossibility | The lift breaks under operations needed by candidate algorithms | **CLEAR** for convolution, differentiation, integration. UNTESTED for composition, nonlinear operations | 3 |
| K5 | FLOP overhead dominates | The 2.3x per-operation overhead exceeds the conditioning benefit for chains of realistic length (n < 10) | Untested; critical threshold: how long must the chain be? | 4 |
| K6 | No real-world algorithm chains enough operations near resonance | Survey of candidate domains shows no realistic computation with ≥3 chained resonance crossings | Untested | 2 |
| K7 | Compensated arithmetic is cheaper | Kahan-compensated standard addition formulas achieve the same conditioning at lower FLOP cost (12 FLOPs + 6 compensation ≈ 18 FLOPs vs 28 for DPQA) | Untested; this is the most threatening kill condition | 4 |
| K8 | Growth of u, v causes overflow before conditioning matters | For large |t|, u and v grow as cosh(t)/2 ∼ e^|t|/4. If they overflow float64 before the conditioning advantage becomes significant, the lift is useless | Untested; cosh(710) overflows float64 | 3 |

### Kill Condition Analysis

**K7 is the most dangerous.** If compensated subtraction (Kahan or TwoSum-based error-free transformation) applied to cos(a)cos(b) - sin(a)sin(b) achieves similar conditioning improvement at 18 FLOPs vs DPQA's 28, then DPQA is a more expensive version of a known technique. Round 4 MUST test this head-to-head.

**K5 is the practical gate.** If 2.3x overhead per operation means you need chains of n > 100 before the conditioning benefit compensates, and no real algorithm chains that many near-resonance operations, then the technique is theoretically sound but practically irrelevant.

**K8 is a scope limiter.** For |t| > 710 (float64 overflow of cosh), the lifted representation requires extended precision or rescaling. This doesn't kill the approach but limits its regime.

---

## Step 7: Recommended Search Directions for Round 2 (Literature)

The polymathic-researcher should investigate:

### Priority 1 (Must Search)

1. **"Deferred subtraction" or "cancellation-free" numerical methods for trigonometric computation.** Keywords: catastrophic cancellation, trigonometric recurrence, error-free transformation, compensated trigonometric computation. Target: whether anyone has systematically studied deferring the sin/cos subtraction.

2. **Cyclic convolution as an alternative to trigonometric addition formulas.** Keywords: circular convolution, number-theoretic transform, DFT-based arithmetic. Target: whether cyclic convolution over Z₄ has been used for phase arithmetic.

3. **Split-radix FFT and mod-4 decomposition.** The split-radix FFT already decomposes DFT computation into mod-4 groups. Does any literature discuss the NUMERICAL CONDITIONING properties of working in the split basis? Keywords: split-radix FFT, numerical stability, round-off error analysis.

4. **Compensated trigonometric addition.** Does anyone publish error-free or compensated versions of cos(a+b) = cos(a)cos(b) - sin(a)sin(b)? This is the competitor to DPQA. Keywords: compensated dot product, accurate difference, TwoProduct, error-free transformation trigonometric.

### Priority 2 (Should Search)

5. **Homogeneous representations for oscillatory systems.** Do physicists or engineers use un-projected representations in wave mechanics? Keywords: projective phase space, homogeneous wave representation, lifted oscillatory coordinates.

6. **Gross/net energy analysis in electrical engineering.** Does Fortescue analysis or circuit theory use the "carry both cosh and cos" pattern? Keywords: reactive power, apparent power, gross circulation, Dollard energy.

7. **Numerical conditioning of Chebyshev recurrences.** Chebyshev polynomials satisfy T_{n+1}(x) = 2xT_n(x) - T_{n-1}(x). For x near a zero, this recurrence is ill-conditioned. Has anyone proposed a "lifted" Chebyshev recurrence that avoids this? This would be a direct analog.

### Priority 3 (Speculative)

8. **Quaternary number systems in computer arithmetic.** Base-4 and related representations. Any conditioning analysis?

9. **Geometric algebra / Clifford algebra numerical methods.** Multivector arithmetic keeps multiple grades. Is there a "deferred projection to scalar" pattern in the GA numerical computing literature?

10. **Lie group integration near singularities.** Integrators for rotation groups that avoid gimbal-lock-like singularities by staying in the Lie algebra. Structural parallel to DPQA.

---

## Summary of the Vision

### What the Solution Looks Like (Seen From the End)

A design pattern -- not a theory, not a framework, but a TECHNIQUE -- for numerical computation in oscillatory systems near resonance:

> **Deferred-Projection Quaternary Arithmetic (DPQA)**: Represent the oscillatory state as a 4-vector (u, x, v, y) of all-positive components. Chain operations (argument addition via cyclic convolution, differentiation via cyclic shift, linear combination) in the lifted space with no cancellation. Extract gross quantities (cosh = u+v, sinh = x+y) freely. Defer net quantities (cos = u-v, sin = x-y) to the final output, applying compensated subtraction if needed.

### What Precisely Is Missing

1. **Empirical confirmation** that chained DPQA operations near resonance achieve >2x conditioning improvement over standard computation (Gap A)
2. **At least one real-world domain** where the technique applies to a non-trivial computation (Gap B)
3. **Head-to-head comparison** with compensated standard arithmetic (Kill condition K7)

### What New Construction Fills the Gap

The bridge is the CHAINED OPERATION ANALYSIS: measure conditioning not for a single evaluation (already done -- DPQA loses for single cos(t)), but for CHAINS of n operations passing through resonance. The prediction is that DPQA's advantage scales with chain length × resonance crossings.

### Kill Conditions (Numbered, Testable)

1. ~~K1: No lifted computation exists~~ → CLEAR (cyclic convolution is closed, well-conditioned)
2. K2: Conditioning advantage <2x in ALL scenarios → Test in Round 4
3. K3: Known published technique → Investigate in Round 2
4. ~~K4: Mathematical impossibility~~ → CLEAR for core operations; test nonlinear ops in Round 3
5. K5: 2.3x FLOP overhead not amortized for realistic chains → Test in Round 4
6. K6: No real algorithm chains enough resonance crossings → Investigate in Round 2
7. **K7: Compensated arithmetic achieves same benefit cheaper** → MOST THREATENING; test in Round 4
8. K8: float64 overflow of u, v before conditioning matters → Characterize in Round 3

### Structural Fusion Verdicts

| Parallel System | Verdict | Score | Key Break Point |
|----------------|---------|-------|-----------------|
| Homogeneous coordinates | ANALOGY | 75% | Not a quotient space; different geometric meaning |
| expm1/log1p | ANALOGY | 70% | Single-function patch vs. systematic Z₄ framework |
| Double-double arithmetic | ANALOGY | 65% | Error correction vs. independent physical quantities |
| Kahan compensated summation | ANALOGY | 60% | Tracks rounding error vs. tracks gross magnitude |
| Log-space computation | ANALOGY | 55% | Bijective vs. 4-to-2 redundant |
| Redundant number representations | ANALOGY | 50% | Latency optimization vs. conditioning optimization |
| Reparameterization trick | ANALOGY | 45% | Distant: different domain, different mechanism |

No IDENTITY found. The quaternary lifted representation is a distinct technique, though it shares structural DNA with all of the above.

### Confidence Calibration

| Component | Confidence | Justification |
|-----------|------------|---------------|
| Operation closure (N1) | **95%** | Algebraic verification; cyclic convolution is textbook |
| Independent value (N3) | **90%** | cosh and conditioning ratio have clear utility |
| Structural parallels are analogies not identities | **85%** | Systematic comparison; could be wrong if literature search finds exact match |
| At least one domain benefits | **60%** | Plausible candidates identified, none empirically confirmed |
| DPQA beats compensated standard arithmetic | **40%** | This is the key uncertainty; K7 may kill it |
| Chain-length advantage is practical (n < 20) | **50%** | Depends on FLOP overhead amortization rate |
| Overall: the technique has real engineering value | **45%** | Honest. More likely than not to be a niche-but-real technique, but K7 could reduce it to "just use Kahan" |

### The Honest Scale

This is at the level of: **a numerical conditioning design pattern for oscillatory computation near resonance.** Comparable in scope and novelty to expm1/log1p, not to a new algorithm or theory. If it survives K7 (compensated arithmetic comparison), it earns a place in the numerical analyst's toolkit for a specific class of problems. If K7 fires, it reduces to "an algebraically interesting rederivation of why you should use compensated subtraction."

Either outcome is a clean result. Proceed to Round 2.
