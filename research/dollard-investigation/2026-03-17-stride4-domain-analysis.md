# Stride-4 Domain Analysis — Heptapod-B Teleological Assessment

**Date**: 2026-03-17
**Agent**: heptapod-b-architect
**Question**: What system would be NATIVELY built on the stride-4 quaternary primitive?
**Tag**: [OUR ANALYSIS]

## Key Structural Insight

The same-argument constraint (all four functions of the SAME t) is naturally satisfied by ANY system whose characteristic polynomial has roots forming a Z4 orbit: {+t, -t, +it, -it}. This is the general solution to the fourth-order ODE:

d⁴f/ds⁴ = t⁴·f

This is the **Euler-Bernoulli beam equation** and its relatives.

## Best Candidate Domains

### 1. Phononic Crystal / Metamaterial Band Diagrams (PUREST)
- Periodic structure, one cell, many frequencies
- Transfer matrix entries ARE {u, v, x, y}
- N=1 cell, M=10⁴ frequencies → function eval IS the dominant cost

### 2. Rotor Dynamics Frequency Response
- Many bearings/disks, frequency sweep
- Industrial use (GE, Rolls-Royce, Siemens)
- TMM is still the standard approach

### 3. Guided Wave Forward Modeling (SHM)
- Real-time constraint favors faster function evaluation
- Pipeline/rail inspection

## Critical Kill Condition (KC1)

**Benchmark stride-4 against optimized libm (glibc/MKL) for computing all four functions.**
If stride-4 doesn't beat 4× independent libm calls by >15%, the proposition fails.
This is UNTESTED and CRITICAL.

## Confidence

| Component | Confidence |
|-----------|-----------|
| Math correct | 99.9% (Lean verified) |
| FLOP savings (theory) | 95% |
| FLOP savings (practice vs libm) | 40% — UNTESTED |
| Beam/wave = natural home | 85% |
| Industrial demand | 30% |
| Becomes a product | 15% |

## Bottom Line

The stride-4 primitive is the RIGHT computation for beam vibration / wave propagation.
Whether it's the right IMPLEMENTATION depends on KC1 (the benchmark against libm).
Mathematical curiosity AND real application — balance depends on KC1.

Full analysis in session context (2026-03-17-1920-dollard-synthesis-integration).
