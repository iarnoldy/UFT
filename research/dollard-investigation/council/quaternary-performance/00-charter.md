# Charter: Quaternary Computational Engine -- Performance Characteristics

**Investigation**: quaternary-performance
**Date**: 2026-03-17
**Orchestrator**: Research Council (Sophia 3.1)
**Provenance**: Prior council `dollard-pure-construction` VERDICT.md allocated 3% uncertainty to "the possibility that the quaternary expansion has practical computational advantages in specific lossy propagation problems (untested empirically)." This investigation tests that 3%.

---

## The Question

Does the quaternary computational PATHWAY -- computing u, x, v, y as four independent mod-4 subseries -- have different PERFORMANCE characteristics than the standard pathway of computing cos, sin, cosh, sinh directly?

This is an engineering question, not an algebra question. The prior council settled the algebra: it IS Z4. Same algebra, potentially different computational properties.

## Why Standard Approaches Are Insufficient

Standard numerical analysis focuses on CORRECTNESS of computation (do you get the right answer?). The prior council proved algebraic equivalence. But algebraic equivalence does not imply computational equivalence. Two algorithms computing the same function can differ in:

1. **Numerical stability** -- catastrophic cancellation, conditioning near singularities
2. **Parallelism** -- alternating-sign series vs monotone series, SIMD vectorization
3. **Early warning** -- detecting proximity to singularities before they hit
4. **Joint efficiency** -- computing related functions simultaneously
5. **Gradient flow** -- autodiff properties for machine learning applications

None of these were tested in the prior council. They require BENCHMARKS, not proofs.

## What a Successful Answer Looks Like

- Actual benchmark numbers (wall-clock time, relative error, ULP differences)
- Head-to-head comparison on identical hardware
- At least 5 independent trials per benchmark for statistical significance
- Clear statement: "quaternary is faster/slower/equivalent by X% for Y problem"
- Figures showing the performance characteristics
- HONEST assessment -- if quaternary loses on every benchmark, that IS the answer

## Hypotheses (Pre-Registered)

**H1: Numerical Stability Near Resonance**
Near t = pi/2, cos(t) approaches 0. Standard computation divides by near-zero. The quaternary form u - v = cos(t) computes this as the difference of two large positive numbers (catastrophic cancellation risk). OR: having u and v separately avoids the division. Test: compare precision of cos(t) vs (u-v) near t = pi/2 +/- epsilon for various epsilon.

**H2: Monotone Convergence (No Alternating Signs)**
Standard: cos(t) = sum(-1)^n t^(2n)/(2n)!, alternating signs, cancellation within the series.
Quaternary: u = sum t^(4n)/(4n)!, ALL POSITIVE TERMS. No alternating signs within each subseries.
Hypothesis: quaternary subseries converge monotonically, potentially better conditioned.
Test: compare convergence rate and numerical stability for large t.

**H3: Resonance Early Warning**
The ratio |u-v|/|u+v| = |cos(t)|/cosh(t) approaches 0 at resonance. This is a NATURAL resonance detector that decays smoothly. Compare detection horizon: how early does |u-v|/|u+v| < threshold detect approaching resonance vs |cos(t)| < threshold?

**H4: All-Four-at-Once Efficiency**
If you need cos, sin, cosh, sinh simultaneously (lossy propagation), standard requires 4 function evaluations. Quaternary: compute u, x, v, y (4 subseries with shared structure), then 4 additions/subtractions. Test: wall-clock time for all-four via quaternary vs 4 direct calls, for arrays of 10K-1M values.

**H5: Gradient Flow Properties**
d(u-v)/dt requires d(u)/dt and d(v)/dt. Does the decomposed form give better autodiff properties? Test: symbolic differentiation comparison, and if pytorch is available, actual backward pass timing.

## Kill Conditions (Pre-Registered)

| ID | Condition | Fires | Action |
|----|-----------|-------|--------|
| K1 | Quaternary is uniformly SLOWER than standard for ALL array sizes in H4 | After Round 3 | STOP -- no computational advantage exists |
| K2 | Quaternary has WORSE numerical stability near resonance (H1) -- more ULP error, not less | After Round 3 | STOP on stability claim |
| K3 | EVERY hypothesis shows no measurable advantage (all within noise) | After Round 3 | STOP -- performance is identical, report null result |
| CONTINUE | ANY hypothesis shows measurable advantage (>5% improvement, p<0.05) | After Round 3 | CONTINUE to synthesis |

## Agent Assignments

| Round | Agent | Purpose |
|-------|-------|---------|
| 1: VISION | Heptapod B Architect | What would a computational advantage look like? Theoretical analysis of why it could or could not exist. |
| 2: IMPLEMENTATION | Direct execution | Write the benchmark code. Head-to-head quaternary engine vs standard engine. |
| 3: EXECUTION | Direct execution | Run all benchmarks. Collect actual numbers. Produce figures. |
| 4: ANALYSIS | Dollard Theorist | Interpret results. Which hypotheses survived? Mathematical explanation. |
| 5: SYNTHESIS | Heptapod B Architect | Final verdict with actual performance data. |

## Output Locations

- Research files: `research/council/quaternary-performance/`
- Benchmark scripts: `src/experiments/council/`
- Result figures: `src/experiments/results/`
- VERDICT.md: `research/council/quaternary-performance/VERDICT.md`

---

**Status: AWAITING APPROVAL**

This charter must be approved before Round 1 begins.
