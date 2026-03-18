# The Complete Quaternary Identity Set

**Date**: 2026-03-17
**Tag**: [OUR ANALYSIS] — derived from mod-4 subseries decomposition of e^t
**Status**: Verified computationally, ready for Lean formalization

## The Four Quantities

From the mod-4 subseries decomposition of e^t:
```
u(t) = (cosh(t) + cos(t))/2     — "storage" component
x(t) = (sinh(t) + sin(t))/2     — "transfer" component
v(t) = (cosh(t) - cos(t))/2     — "return" component (Dollard: ν)
y(t) = (sinh(t) - sin(t))/2     — "dissipation" component
```

All four are positive for t > 0. All are monotonically increasing for t > 0.

## The Seven Identities

### Linear identities (well-known, in Dollard's text as eq 80-82 equivalent)
```
(1) u - v = cos(t)           net circular
(2) u + v = cosh(t)          gross circular
(3) x - y = sin(t)           net hyperbolic
(4) x + y = sinh(t)          gross hyperbolic
(5) u + x + v + y = e^t      total exponential
```

### Cross-product identities (NOT seen stated as a pair in standard references)
```
(6) 4uv = sinh²(t) + sin²(t)     cross-energy: storage × return
(7) 4xy = sinh²(t) - sin²(t)     cross-energy differential: transfer × dissipation
```

## Proofs

### Identity (6): 4uv = sinh²(t) + sin²(t)

```
4uv = (cosh(t) + cos(t))(cosh(t) - cos(t))        [substitute definitions]
    = cosh²(t) - cos²(t)                           [difference of squares]
    = [(cosh(2t) + 1)/2] - [(cos(2t) + 1)/2]       [double-angle identities]
    = (cosh(2t) - cos(2t))/2                        [simplify]

sinh²(t) + sin²(t)
    = [(cosh(2t) - 1)/2] + [(1 - cos(2t))/2]       [double-angle identities]
    = (cosh(2t) - cos(2t))/2                        [simplify]

Therefore 4uv = sinh²(t) + sin²(t).  QED.
```

### Identity (7): 4xy = sinh²(t) - sin²(t)

```
4xy = (sinh(t) + sin(t))(sinh(t) - sin(t))         [substitute definitions]
    = sinh²(t) - sin²(t)                           [difference of squares]
QED.
```

## What This Reveals

### The crossing structure

The zeros of cos(t) are the points where u(t) = v(t) — two monotonically increasing
positive curves crossing. Standard notation shows "cos hits zero." Quaternary shows
"two rising curves intersect." This transforms zero-finding into intersection-finding.

### One-operation energy computation

Standard: computing sinh²(t) + sin²(t) requires 4 function evaluations + 2 squares + 1 addition = 7 operations.
Quaternary: computing 4uv requires 1 multiplication + 1 shift = 2 operations (if u, v already available).

### The complete energy picture

From just u and v:
- cos(t) = u - v (net circular oscillation)
- cosh(t) = u + v (gross circular magnitude)
- sinh²(t) + sin²(t) = 4uv (total mode energy)

From just x and y:
- sin(t) = x - y (net hyperbolic oscillation)
- sinh(t) = x + y (gross hyperbolic magnitude)
- sinh²(t) - sin²(t) = 4xy (mode energy differential)

### For N-Phase Fortescue decomposition

The analog for N sequence components S_0, ..., S_{N-1}:
- Gross = Σ|S_k|
- Net = |ΣS_k|
- Conjugate pair energy = |S_k| · |S_{N-k}| (analog of uv)
- The product encodes cross-mode energy between forward and backward rotating components

## Lean Formalization Plan

All seven identities are algebraic. No limits, no series convergence, no topology.
Each follows from the closed-form definitions and basic real arithmetic.

Target file: `src/lean_proofs/foundations/quaternary_identities.lean`

Theorems to prove:
1. `quaternary_diff_eq_cos`: u - v = cos(t)
2. `quaternary_sum_eq_cosh`: u + v = cosh(t)
3. `quaternary_x_diff_eq_sin`: x - y = sin(t)
4. `quaternary_x_sum_eq_sinh`: x + y = sinh(t)
5. `quaternary_total_eq_exp`: u + x + v + y = e^t
6. `quaternary_cross_energy`: 4 * u * v = sinh(t)^2 + sin(t)^2
7. `quaternary_cross_differential`: 4 * x * y = sinh(t)^2 - sin(t)^2
