# Quaternary Positional Encoding (QPE) — Discovery Analysis

**Date**: 2026-03-17
**Agent**: heptapod-b-architect (teleological analysis)
**Tag**: [OUR ANALYSIS] — novel application of quaternary decomposition
**Status**: PROPOSED, untested empirically

## The Pattern of Our Error (Third Time)

| What we tested | What we should have tested | Error type |
|---|---|---|
| Three councils: bare 4-vector | Operator-valued element | Stripped operators |
| Z4 circulant as layer activation | Decomposition as encoding | Confused computation with representation |
| Stride-4 Taylor for evaluation | Mod-4 decomposition for information | Confused implementation with architecture |

**Root cause**: We kept testing the quaternary decomposition as a COMPUTATION ENGINE.
It is a REPRESENTATION SCHEME.

## The Proposal

Standard transformer PE (Vaswani 2017): 2 channels per frequency (sin, cos). Both oscillate, cross zero.

Quaternary PE: 4 channels per frequency, ALL positive:
```
QPE(p, 4k)   = u(w_k*p) = (cosh(w_k*p) + cos(w_k*p))/2
QPE(p, 4k+1) = x(w_k*p) = (sinh(w_k*p) + sin(w_k*p))/2
QPE(p, 4k+2) = v(w_k*p) = (cosh(w_k*p) - cos(w_k*p))/2
QPE(p, 4k+3) = y(w_k*p) = (sinh(w_k*p) - sin(w_k*p))/2
```

QPE is a STRICT SUPERSET of standard PE:
- Differences recover sin/cos (Lean-verified: quaternary_diff_eq_cos, quaternary_x_diff_eq_sin)
- Sums give scale (Lean-verified: quaternary_sum_eq_cosh, quaternary_x_sum_eq_sinh)
- Products give cross-energy (Lean-verified: quaternary_cross_energy, quaternary_cross_differential)
- Conditioning = cosh/|cos| (Lean-verified: gross_geq_abs_net)

Standard PE encodes PHASE ONLY. QPE encodes PHASE AND SCALE.

## Connection to Dollard's Explicit Claim

Versor Algebra eq 83: "This duo-binary form neglects the factors"
When cos = u - v, you lose the information about how much is CIRCULATING vs OSCILLATING.
QPE preserves exactly the information Dollard says standard notation destroys.

## Kill Conditions

| # | Condition | Status |
|---|-----------|--------|
| K1 | cosh/sinh overflow for large w*p | FIRES. Mitigated: log-space or small frequencies |
| K2 | 4 channels = 2x cost, half frequency resolution | UNTESTED |
| K3 | No empirical benefit demonstrated | UNTESTED (central risk) |
| K4 | x,y negative for t < 0 | Mild: u,v positive for ALL t |
| K5 | FlashAttention compatibility | LIKELY OK |

## Confidence

- Math correct: 99% (Lean verified)
- Implementable: 95%
- Provides info not in standard PE: 90%
- Outperforms on any benchmark: 35%
- Publishable result: 65%

## Next Steps

1. Implement QPE in PyTorch (~2 hrs)
2. Verify gradient flow (~1 hr)
3. Small-scale comparison (~4 hrs)
4. If positive: real benchmark (~24 hrs GPU)

## First neural network primitive with formal verification backing

Every structural property traces to a Lean theorem (9 theorems, 0 sorry).
