# N-Phase Gross/Net Monitoring — Mathematical Specification

**Tag**: [OUR ANALYSIS] — specification for the N-Phase system based on quaternary findings
**Status**: Specified, ready for implementation in N-Phase repo
**Date**: 2026-03-17

## What This Specifies

A monitoring enhancement for any system that computes Fortescue/DFT sequence decomposition.
The enhancement adds three metrics at zero computational cost (the sequence components are
already computed). No changes to the core decomposition algorithm.

## Mathematical Foundation

### For N sequence components S_0, ..., S_{N-1}

After Fortescue decomposition of an N-phase signal:

```
Gross(S) = Σ_{k=0}^{N-1} |S_k|        sum of component magnitudes
Net(S)   = |Σ_{k=0}^{N-1} S_k|        magnitude of reconstructed signal
Conditioning(S) = Gross(S) / Net(S)    ≥ 1 always (triangle inequality)
```

### Conjugate pair structure

For N phases, S_k and S_{N-k} are conjugate pairs (for real input signals, S_{N-k} = S_k*).

```
PairGross(k) = |S_k| + |S_{N-k}|      total rotating field energy in pair
PairNet(k)   = ||S_k| - |S_{N-k}||    imbalance between forward/backward rotation
PairBalance(k) = PairNet(k) / PairGross(k)   0 = balanced, 1 = fully unbalanced
```

For 3-phase (N=3): S_1 (positive sequence) and S_2 (negative sequence) form the critical pair.

### Connection to quaternary identities

The pair product |S_k| · |S_{N-k}| is the N-phase analog of the quaternary identity 4uv:
- For N=4: |S_1| · |S_3| relates to the circular/hyperbolic cross-energy
- For general N: the product encodes the interaction between mode k and its conjugate

### Connection to standard EE quantities

For standing wave systems:
```
Conditioning ≈ SWR = (1 + |Γ|) / (1 - |Γ|)          for N=2 (forward/reflected)
Conditioning ≈ Q factor                                for lumped resonant circuits
Conditioning = cosh(ln(SWR)) = (SWR + 1/SWR)/2        exact identity
```

## Interface Specification

### Input
```python
sequences: Tensor  # shape (batch, N, features) — complex-valued Fortescue components
```

### Output
```python
class GrossNetResult:
    gross: Tensor         # shape (batch, features) — Σ|S_k|
    net: Tensor           # shape (batch, features) — |ΣS_k|
    conditioning: Tensor  # shape (batch, features) — gross/net
    pair_gross: Tensor    # shape (batch, N//2, features) — per conjugate pair
    pair_net: Tensor      # shape (batch, N//2, features) — per conjugate pair
    pair_balance: Tensor  # shape (batch, N//2, features) — imbalance ratio
```

### Implementation (3 lines of core computation)
```python
def compute_gross_net(sequences: Tensor) -> GrossNetResult:
    gross = torch.sum(torch.abs(sequences), dim=1)          # Σ|S_k|
    net = torch.abs(torch.sum(sequences, dim=1))             # |ΣS_k|
    conditioning = gross / (net + 1e-15)                      # health metric

    # Conjugate pairs (for real input, S_{N-k} = conj(S_k))
    N = sequences.shape[1]
    pair_gross = torch.abs(sequences[:, :N//2]) + torch.abs(sequences[:, -1:N//2-1:-1])
    pair_net = torch.abs(torch.abs(sequences[:, :N//2]) - torch.abs(sequences[:, -1:N//2-1:-1]))
    pair_balance = pair_net / (pair_gross + 1e-15)

    return GrossNetResult(gross, net, conditioning, pair_gross, pair_net, pair_balance)
```

## Use Cases

### 1. Resonance Detection
```python
if conditioning > threshold:
    # Near resonance — components are canceling
    # Flag for attention, use compensated arithmetic if projecting
```

### 2. Fault Classification (3-phase power)
```python
# S_1 = positive sequence, S_2 = negative sequence, S_0 = zero sequence
pair_balance_12 = pair_balance[..., 0]  # positive/negative imbalance
if pair_balance_12 > 0.1:
    # Significant negative sequence — line-to-line or single-phase fault
if abs(sequences[:, 0]) > threshold:
    # Significant zero sequence — ground fault
```

### 3. Feature for Neural Network
```python
# Add conditioning as input feature alongside sequence components
features = torch.cat([
    sequences.real, sequences.imag,  # standard Fortescue features
    conditioning.unsqueeze(1),        # health metric
    pair_balance,                     # per-pair imbalance
], dim=1)
```

### 4. Quality Metric for Signal Integrity
```python
# Balanced N-phase signal has conditioning ≈ 1 (all components in phase)
# Degraded signal has conditioning >> 1 (components canceling)
signal_quality = 1.0 / conditioning  # 1 = perfect, 0 = degenerate
```

## What This Does NOT Do

- Does NOT change the Fortescue decomposition algorithm
- Does NOT require the Z4 cyclic convolution (which is numerically inferior)
- Does NOT validate any of Dollard's physics claims
- Does NOT require carrying (u, x, v, y) through the pipeline
- Is NOT the "lifted representation" (which was killed)

This is a MONITORING ENHANCEMENT: extract information that's already computed but not surfaced.

## Lean Formalization

The mathematical foundation (triangle inequality, conditioning ≥ 1) is being formalized in:
`src/lean_proofs/foundations/quaternary_identities.lean`

Key theorem: `gross_geq_abs_net` — |u-v| ≤ u+v (basis for conditioning ≥ 1)
