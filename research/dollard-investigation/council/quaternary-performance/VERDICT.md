# VERDICT: Quaternary Computational Engine Performance

**Investigation**: quaternary-performance
**Date**: 2026-03-17
**Rounds completed**: 5 of 5
**Kill conditions fired**: K2 (worse stability near resonance)

> **CAVEAT (added 2026-03-17)**: This council analyzed the mod-4 decomposition of the
> REAL exponential e^t (our construction), NOT Dollard's actual ε^j construction with
> operators {1,j,h,k}. The kill applies to the stripped real vector version. Dollard's
> operator-valued construction shows unexpected zero-error results at specific chain
> lengths when implemented exactly from his source text. See
> `research/dollard-theorist/2026-03-17-exact-construction-pivot.md`.

---

## One-Paragraph Verdict

The quaternary computational pathway (computing mod-4 subseries u, x, v, y) has exactly one genuine advantage over standard computation: the stride-4 Taylor recurrence reaches a given series order in half the iterations of the stride-2 standard recurrence, saving approximately 40% of floating-point operations when computing all four trig/hyperbolic functions simultaneously via Taylor series. This advantage is real, algorithmic (not an implementation artifact), and confirmed by both FLOP counting and wall-clock benchmarks (quaternary runs in 60% of standard time, consistently across array sizes from 1 to 100,000 elements). However, this advantage exists ONLY for custom Taylor implementations, not for compiled library functions (numpy is 25-75% faster than quaternary-from-numpy). Furthermore, the quaternary pathway introduces catastrophic cancellation in cos(t) = u - v and sin(t) = x - y, degrading accuracy by 16-68x at arguments |t| > 5 compared to the standard alternating Taylor series. For practical scientific computing, there is no advantage.

## Confidence Level: 95%

High confidence because results are based on direct computation with mpmath ground truth at 50-digit precision, 10+ statistical trials per timing benchmark, and confirmed by independent FLOP analysis. The 5% uncertainty accounts for: (a) possible advantage in specialized hardware (FPGA, custom CUDA) not tested; (b) possible advantage when combined with argument reduction that mitigates the cancellation issue.

## Hypothesis Results

| ID | Hypothesis | Verdict | Data |
|----|-----------|---------|------|
| H1 | Stability near resonance | **REFUTED**: Quaternary 5-68x worse | ULP error at t=pi/2+eps: Quat 844 vs Std 56 (eps=1e-3) |
| H2 | Monotone convergence | **REFUTED**: Quaternary worse for trig, neutral for hyp | At t=20: Quat 694M ULP vs Std 10M ULP for cos |
| H3 | Early warning | **CONFIRMED but trivial** | 2-2.5x earlier detection, but just division by cosh(t)>1 |
| H4a | Taylor efficiency | **CONFIRMED**: 40% fewer FLOPs | Quat 11.8us vs Std 18.8-19.6us (scalar); ratio 0.60 |
| H4b | Numpy efficiency | **REFUTED**: Numpy 25-75% faster | Quat-from-numpy is strictly more work |
| H5 | Gradient flow | **REFUTED**: No advantage | Identical computation, different labels |

## Recommendation: STOP

This investigation is complete. The question "does the quaternary pathway have different computational properties?" is answered definitively:

- **Speed**: Yes, faster for Taylor series (40% FLOP savings via stride-4 recurrence). No, not faster for compiled libraries.
- **Accuracy**: Worse for trig outputs (catastrophic cancellation in u-v). Neutral for hyperbolic outputs (u+v has no cancellation).
- **Diagnostics**: Trivially better early warning (normalization by cosh, not a deep property).
- **Gradients**: No difference.

No further investigation is warranted. The finding is a clean negative for practical computing with a minor positive for niche custom implementations.

## What Was Learned

1. The mod-4 grouping of the exponential series IS computationally different from the mod-2 grouping. The difference is a stride-4 vs stride-2 recurrence, yielding 40% FLOP savings for equivalent Taylor order. This is a genuine property of the Z4 algebraic structure.

2. Monotone convergence of subseries (no alternating signs) does NOT guarantee better numerical results. The final subtraction step can be worse than distributed alternating-sign cancellation. This is a useful numerical analysis lesson.

3. The condition number cosh(t)/|cos(t)| precisely characterizes the precision loss from the quaternary subtraction u - v = cos(t). This diverges exponentially with t and at zeros of cosine.

4. For standard scientific computing, compiled library functions (numpy cos/sin/cosh/sinh) dominate all Taylor-based approaches by orders of magnitude. The quaternary vs standard Taylor distinction is irrelevant in this context.

## Files Produced

| File | Contents |
|------|----------|
| `research/council/quaternary-performance/00-charter.md` | Investigation charter, kill conditions |
| `research/council/quaternary-performance/01-vision.md` | Theoretical predictions (H2 prediction was wrong) |
| `research/council/quaternary-performance/02-implementation.md` | Benchmark design documentation |
| `research/council/quaternary-performance/03-execution.md` | Raw benchmark results and kill condition evaluation |
| `research/council/quaternary-performance/04-analysis.md` | Hypothesis-by-hypothesis interpretation with deep dive |
| `research/council/quaternary-performance/05-synthesis.md` | Integrated assessment |
| `research/council/quaternary-performance/VERDICT.md` | This file |
| `src/experiments/council/quaternary_performance_benchmarks.py` | Main benchmark script |
| `src/experiments/council/quaternary_h4_deep_dive.py` | H4 source-of-advantage analysis |
| `src/experiments/council/quaternary_accuracy_verification.py` | Accuracy comparison verification |
| `src/experiments/results/quaternary_performance_results.json` | Full results data (JSON) |
