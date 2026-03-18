# Investigation Charter: The Quaternary Lifted Representation

**Investigation slug**: lifted-representation
**Date**: 2026-03-17
**Orchestrator**: Research Council (Sophia 3.1)

---

## The Question

Does working in the (u, x, v, y) quaternary basis -- staying lifted, deferring projection to standard trig functions -- provide measurable computational advantages for algorithms that don't need cos(t) directly?

## Why Standard Approaches Failed

Two prior councils answered DIFFERENT questions:

1. **dollard-pure-construction**: Proved the algebra IS Z4. The math is settled. No new algebraic content. VERDICT: STOP.

2. **quaternary-performance**: Tested whether quaternary computes cos(t) better. Answer: NO, it is 15-68x WORSE near resonance due to catastrophic cancellation in u - v. The stride-4 Taylor recurrence is 40% faster, but that's a niche advantage. VERDICT: STOP.

**The gap**: Neither council tested whether an algorithm can AVOID computing cos(t) entirely by working with (u, v) directly. The prior councils tested projection quality. This council tests staying-lifted quality.

## The Key Mathematical Insight

Each mod-4 subseries has ALL POSITIVE TERMS:
- u = t^0/0! + t^4/4! + t^8/8! + ...  (all positive)
- x = t^1/1! + t^5/5! + t^9/9! + ...  (all positive)
- v = t^2/2! + t^6/6! + t^10/10! + ... (all positive)
- y = t^3/3! + t^7/7! + t^11/11! + ... (all positive)

Projections:
- cos(t) = u - v  --> catastrophic cancellation when u ~ v (near resonance)
- cosh(t) = u + v  --> always well-conditioned (addition of positives)
- sin(t) = x - y   --> catastrophic cancellation when x ~ y (near pi)
- sinh(t) = x + y  --> always well-conditioned

Analogy: homogeneous coordinates avoid division-by-zero singularity by not dividing by w. The quaternary basis avoids subtraction singularity by not computing u - v.

## What a Successful Answer Looks Like

A positive result means: at least one realistic computation achieves >2x conditioning improvement by working in the (u, x, v, y) basis without projecting to trig functions.

A definitive negative result means: no computation can avoid the projection step, OR the conditioning advantage is <2x in every scenario tested.

## Five Tests

1. **Resonance detection**: Compare |cos(t)| < epsilon (ill-conditioned) vs |1 - v/u| < epsilon (well-conditioned ratio). Which is more reliable with noisy inputs?

2. **Energy computation**: gross = u+v always well-conditioned. Compare precision of computing gross/net ratio via lifted (u,v directly) vs standard (cosh/cos separately).

3. **Neural network activations**: Design layer with (u(t), v(t)) activations. Gradients du/dt = y, dv/dt = x (well-conditioned). Compare loss landscape near resonance vs cos(t) activation.

4. **N-Phase pipeline**: Does Fortescue decomposition work in lifted basis? Can we detect near-resonance from data already computed?

5. **Operation classification**: Which operations preserve the lift? Addition, scalar multiplication, derivatives work. What about multiplication? Composition? Classify.

## Pre-Registered Kill Conditions

| ID | Kill Condition | Fires If | Round |
|----|---------------|----------|-------|
| K1 | No lifted computation exists | No test can be done entirely in (u,x,v,y) without projecting | 1 (Vision) |
| K2 | Trivial advantage | Conditioning advantage <2x in ALL tested scenarios | 4 (Computation) |
| K3 | Known technique | Prior art shows this is well-published under another name | 2 (Literature) |
| K4 | Mathematical impossibility | Formal analysis shows the lift breaks under needed operations | 3 (Rigor) |

**Continue condition**: ANY test shows >2x conditioning improvement for a realistic computation.

## Agent Assignments

| Round | Agent | Purpose |
|-------|-------|---------|
| 1 VISION | heptapod-b-architect | Structural requirements for a useful lifted representation |
| 2 LITERATURE | polymathic-researcher | Prior art: deferred-projection in numerical analysis |
| 3 RIGOR | dollard-theorist | Formal conditioning analysis, operation classification |
| 4 COMPUTATION | Direct Python execution | Benchmark the five tests with actual numbers |
| 5 SYNTHESIS | heptapod-b-architect | Revised vision with all evidence |

## Key Files

- Question alignment: `research/lifted-representation question alignment.md`
- Prior council (algebra): `research/council/dollard-pure-construction/VERDICT.md`
- Prior council (performance): `research/council/quaternary-performance/VERDICT.md`
- Prior analysis detail: `research/council/quaternary-performance/04-analysis.md`
