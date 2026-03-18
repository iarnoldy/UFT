# VERDICT: The Quaternary Lifted Representation

> **CAVEAT (added 2026-03-17)**: This council analyzed the mod-4 decomposition of the
> REAL exponential e^t (bare real 4-vector), NOT Dollard's actual ε^j construction with
> operators {1,j,h,k}. The kill applies to the stripped version. Dollard's operator-valued
> construction shows unexpected zero-error results when implemented exactly from his source
> text. See `research/dollard-theorist/2026-03-17-exact-construction-pivot.md`.

**Investigation**: lifted-representation
**Date**: 2026-03-17
**Orchestrator**: Research Council (Sophia 3.1)
**Rounds completed**: 5 of 5
**Kill conditions fired**: K2 (advantage < 2x), K4 (mathematical impossibility), K5 (FLOP overhead never amortized), K8 (overflow)

---

## One-Paragraph Verdict

The quaternary lifted representation (DPQA) -- working in the (u, x, v, y) basis without projecting to cos/sin -- is algebraically elegant and numerically useless. The circulant matrix for argument addition has spectral radius e^theta > 1, causing exponential error growth O(n * u * e^{n*theta}). The standard rotation chain has spectral radius 1 (orthogonal), with linear error growth O(n * u). DPQA is exponentially worse for chained operations of any length, for any total angle, in every scenario tested. The central premise -- that resonance crossings cause cascading error in the standard chain -- is false: rotation preserves error norms. Eight empirical tests confirm: zero show advantage, five show degradation, three are irrelevant. The technique is novel (no prior publication found) but the novelty is academic: correct algebra, no numerical utility.

## Confidence Level: 98%

Based on mathematical proof (eigenvalue analysis, error propagation bounds) confirmed by eight independent computational tests with mpmath 50-digit ground truth. The 2% uncertainty accounts only for exotic hardware scenarios (quantum computing, analog computing) where the analysis framework may not apply.

## Hypothesis Results

| Test | Result | Data |
|------|--------|------|
| Resonance detection | NO ADVANTAGE | Both methods detect equally at all noise levels |
| Energy computation | NO ADVANTAGE | Gross (u+v) matches cosh() exactly; net (u-v) is worse than cos() |
| Neural network activations | NO ADVANTAGE | Gradient computation identical (prior council H5) |
| N-Phase pipeline | NO ADVANTAGE | Structural decomposition real, no conditioning improvement |
| Operation classification | CLOSED for 6 ops, BROKEN for 5 | Addition, scalar mult, arg addition, diff, integration, integer arg mult: closed. Pointwise mult, composition, non-integer arg mult, division, nonlinear: broken |
| Chained error growth | DPQA EXPONENTIALLY WORSE | Standard: 2.5e-13 at 5000 steps. DPQA: 2.1e-9 (8286x worse, growing) |
| Compensated head-to-head | DPQA DRAMATICALLY WORSE | At n=500: DPQA 32430x worse than compensated |
| Resonance non-amplification | STANDARD IS FINE | Absolute error does NOT spike at resonance crossings |

## Kill Conditions

| ID | Condition | Status | Round |
|----|-----------|--------|-------|
| K1 | No lifted computation exists | CLEAR | 1 |
| **K2** | **Advantage < 2x everywhere** | **FIRES** | 4 |
| K3 | Known published technique | CLEAR | 2 |
| **K4** | **Mathematical impossibility** | **FIRES** | 3 |
| **K5** | **FLOP overhead not amortized** | **FIRES** | 3 |
| K6 | No real algorithm chains enough ops | MOOT | -- |
| K7 | Compensated arithmetic cheaper | SUPERSEDED | 4 |
| **K8** | **Overflow for |t|>710** | **FIRES** | 3 |

## Recommendation: STOP

This investigation is complete. Three independent kill conditions fired. The mathematical proof is confirmed empirically. No pivot preserves the core idea (staying lifted) while avoiding the core problem (exponential error growth from spectral radius > 1).

## What Was Learned

1. **The standard rotation chain is near-optimal.** Its orthogonality (spectral radius = 1) is the mechanism that makes chained angle computation stable. This is more valuable than the DPQA proposal.

2. **Local condition numbers do not imply global instability.** The subtraction cos(a)cos(b) - sin(a)sin(b) has divergent condition number at resonance, but the absolute error remains O(ku) and does not propagate. This is a clean numerical analysis lesson.

3. **Bounded intermediate values are necessary for lifted representations to work.** Homogeneous coordinates (bounded), quaternion rotation (compact manifold), and haversine (values in [0,1]) all succeed because intermediates stay bounded. The quaternary representation fails because it carries cosh(t), which grows as e^t.

4. **The quaternary framework's value is interpretive, not computational.** Gross/net energy decomposition, conditioning diagnostics, and stride-4 Taylor savings survive. These were established by prior councils and are unchanged.

5. **The investigation methodology works.** Kill conditions were pre-registered, rigor preceded computation, and the negative result was accepted cleanly. The five-round council structure correctly identified and verified the fatal flaw.

## What Survives from All Three Councils

| Finding | Source | Status |
|---------|--------|--------|
| Algebra IS Z4 | dollard-pure-construction | PERMANENT |
| Stride-4 Taylor: 40% FLOP savings | quaternary-performance H4 | PERMANENT (niche) |
| Projection to cos: 15-68x worse | quaternary-performance H1-H2 | PERMANENT |
| Interpretive value: gross/net energy | dollard-pure-construction | PERMANENT |
| Staying lifted: exponentially worse | THIS COUNCIL | PERMANENT |
| Conditioning diagnostic: cosh/|cos| | This council + performance H3 | PERMANENT (trivial) |

## Files Produced

| File | Contents |
|------|----------|
| `research/council/lifted-representation/00-charter.md` | Investigation charter, kill conditions |
| `research/council/lifted-representation/01-vision.md` | Heptapod B Round 1: structural requirements (predictions mostly wrong) |
| `research/council/lifted-representation/02-literature.md` | Polymathic: 10 search directions, 14 prior art categories, K3 cleared |
| `research/council/lifted-representation/03-analysis.md` | Dollard Theorist: eigenvalue analysis, exponential error proof, K4/K5/K8 fire |
| `research/council/lifted-representation/04-computation.md` | 8 empirical tests confirming all theoretical predictions |
| `research/council/lifted-representation/05-synthesis.md` | Heptapod B Round 5: autopsy of Round 1 vision, final assessment |
| `research/council/lifted-representation/VERDICT.md` | This file |
| `src/experiments/council/lifted_representation_tests.py` | Computation script (8 tests) |
| `src/experiments/results/lifted_representation_results.json` | Raw results data |
