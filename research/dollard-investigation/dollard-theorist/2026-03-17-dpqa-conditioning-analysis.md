# DPQA Conditioning Analysis -- FATAL FLAW IDENTIFIED

**Date**: 2026-03-17
**Task**: Research Council Round 3 (RIGOR) for lifted-representation investigation
**Question**: Does working in (u,x,v,y) quaternary basis provide conditioning advantages?

## Key Finding

**DPQA has a fatal conditioning flaw: exponential error growth.**

The DPQA circulant matrix C(theta) has spectral radius e^theta > 1.
Rounding errors are amplified by e^theta at each step. After n steps:

| Method | Absolute error | FLOPs/step |
|--------|---------------|------------|
| Standard rotation | O(nu) | 12 |
| DPQA convolution | O(nu * e^{n*theta}) | 28 |
| Compensated rotation | O(nu^2) | 12-42 |

DPQA is exponentially worse than standard for any positive total angle.

## Why the "No Subtraction" Argument Fails

The standard rotation chain R(theta) is ORTHOGONAL (condition number 1).
Error propagation preserves norms. "Catastrophic cancellation" at resonance
(cos ~ 0) is LOCAL: absolute error remains O(ku) at step k, regardless of
resonance crossings. The large relative error at resonance does NOT propagate.

DPQA avoids subtraction but introduces exponential component growth.
The e^t eigenvalue of the circulant causes rounding errors proportional to
e^{k*theta} at step k. This dominates the avoided cancellation by an
exponential factor.

## Kill Conditions

- K4 (mathematical impossibility): FIRES -- exponential error growth
- K5 (FLOP overhead not amortized): FIRES -- no advantage to amortize
- K8 (overflow): FIRES for |t| > 710

## Salvageable

1. Conditioning diagnostic: cosh/|cos| ratio as health indicator
2. Stride-4 Taylor: 40% fewer FLOPs (confirmed prior council)
3. Interpretive: gross/net energy structure

## Full Analysis

Saved to: `research/council/lifted-representation/03-analysis.md`
Contains: complete proofs (Theorems A1-A4, F1), operation classification,
eigenvalue analysis, computation specifications for Round 4.
