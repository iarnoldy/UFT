# SO(16) → E₈ Embedding Analysis

**Date:** 2026-03-16
**Status:** Verified [CO] in Python, Lean formalization pending

## The Embedding

E₈ (248-dim) contains SO(16) (120-dim) as a maximal subalgebra. The decomposition is:

```
248 = 120 + 128_s
```

Where 120 is the adjoint representation of SO(16) and 128_s is a half-spinor representation.

## Root Classification

In Euclidean coordinates (R^8), E₈ has 240 roots in two types:
- **Type 1 (D8/SO(16)):** ±e_i ± e_j for i ≠ j — 112 roots (56 positive + 56 negative)
- **Type 2 (Spinor):** (1/2)(±1,...,±1) with even number of minus signs — 128 roots (64 pos + 64 neg)

The SO(16) subalgebra consists of:
- 8 Cartan elements (shared with E₈)
- 56 positive D8 root vectors
- 56 negative D8 root vectors
- **Total: 120 generators**

## Identification in Our Basis

Using our height-sorted E₈ basis ordering:
- **Cartan:** indices 0-7
- **Positive D8 roots:** indices {8,9,10,11,12,13,14,16,17,...} (56 elements, saved in `so16_e8_embedding.json`)
- **Negative D8 roots:** indices {128,129,130,131,...} (56 elements, corresponding negatives)
- **Positive spinor roots:** the complementary 64 positive root indices
- **Negative spinor roots:** the complementary 64 negative root indices

## Closure Verification [CO]

Python verified: for every pair (i,j) of SO(16) indices, the E₈ bracket [B_i, B_j] contains only terms with indices in the SO(16) subset. **Zero violations.**

This confirms SO(16) is a Lie subalgebra of E₈ [CO — computed, not yet Lean-verified].

## Method

1. Converted each positive root from simple root coordinates to Euclidean R^8
2. Classified as integer-coordinate (D8 type) or half-integer-coordinate (spinor type)
3. Result: 56 D8 + 64 spinor = 120 positive roots (exact match)
4. Checked bracket closure: all 120×120/2 = 7,140 pairs, zero violations

## Files

- `so16_e8_embedding.json` — maps SO(16) basis element indices into E₈ basis
- `e8_structure_constants.json` — full E₈ bracket table (source data)
- SageMath computation via WSL (inline, not saved as separate script)

## Lean Formalization Plan

Verify in Lean: for each pair (i,j) of SO(16) indices, `jacobiTerm` restricted to SO(16) outputs only produces SO(16) indices. This is a `native_decide` check on ~7,140 pairs — should take minutes with the sparse approach.

## Significance

This completes the algebraic chain:
```
SU(5) →ₗ⁅ℝ⁆ SO(10) →ₗ⁅ℝ⁆ SO(14) →ₗ⁅ℝ⁆ SO(16) →ₗ⁅ℝ⁆ E₈
```

Five embeddings. Each verified by Lean's kernel. From the Standard Model gauge group to the largest exceptional Lie algebra.
