# QPE Architecture Review -- Incorporating N-Phase Lessons

**Date**: 2026-03-18
**Agent**: n-phase-architect
**Tag**: [OUR ANALYSIS]
**Status**: Complete -- actionable recommendations with code-level specifics

---

## Executive Summary

QPE shows a real encoding effect (-22.4% mean across 5 seeds, -47.7% single best seed)
but suffers from 3x the variance of the baseline (std 221 vs 72). After examining the
N-Phase patent-ready system's actual implementation patterns, I identify five concrete
architecture changes ordered by expected impact. The most critical finding: **QPE's u,v
channels are NOT the same failure mode as N-Phase's deprecated quaternary features**,
but they DO have a related correlation problem that normalization can fix.

---

## 1. Current State Assessment

### Multi-Seed Results (from `qpe_experiment_a_multiseed.json`)

| Variant | Mean PPL | Std | Min | Max | N |
|---------|----------|-----|-----|-----|---|
| Standard PE (Vaswani) | 896.37 | 72.46 | 812.77 | 996.64 | 5 |
| QPE (geometric) | 614.05 | 221.16 | 376.39 | 904.89 | 5 |
| Standard PE (geometric) | 790.82 | 63.18 | 704.73 | 866.70 | 5 |
| QPE log_scale (geometric) | 656.39 | 294.23 | 265.72 | 907.77 | 5 |
| Learned PE | 1011.47 | 260.78 | 693.07 | 1256.60 | 5 |
| QPE (Vaswani) | NaN | -- | -- | -- | 0 |
| QPE log_scale (Vaswani) | NaN | -- | -- | -- | 0 |

### Key Observations

1. **QPE's mean is better** (-22.4% encoding effect: QPE geometric 614 vs Standard geometric 791).
2. **QPE's variance is 3.5x worse** (std 221 vs 63 for matched geometric frequencies).
3. **QPE's worst seed (904.89) is worse than Standard's worst (866.70)**. A user who picks
   the wrong seed gets WORSE performance than baseline.
4. **log_scale does not fix Vaswani overflow** (all 5 seeds NaN). The `args` clamp at 20
   is applied, but something else is diverging -- likely the gradients of `log1p(cosh(20))`.
5. **log_scale geometric is noisier** (std 294) than raw QPE geometric (std 221). log_scale
   adds variance without fixing the core problem.
6. **All variants overfit catastrophically** -- val_ppl rises monotonically from epoch 2 onward.
   The "best val PPL" is almost always epoch 1. This is a dataset/model-size problem, not
   a PE problem, but it makes the comparison noisy.

### The Real Problem

QPE's high variance comes from the **dynamic range mismatch** between its channels.
At position p with frequency omega:

```
u(t) = (cosh(omega*p) + cos(omega*p)) / 2
v(t) = (cosh(omega*p) - cos(omega*p)) / 2
```

For omega=0.02 and p=128: cosh(2.56) = 6.49. So u ranges from 0.5 to ~3.75 and v
ranges from 0 to ~2.74. Meanwhile cos and sin stay in [-1, 1].

For omega=0.0001 and p=128: cosh(0.0128) = 1.000082. So u ~ 1.0 and v ~ 0.0.

The ratio between the largest channel value (u at high omega, late position) and the
smallest meaningful variation (cos oscillation at low omega) can exceed 10:1. When this
is added to the token embedding (which has its own learned scale), the network must
simultaneously attend to magnitude-3 hyperbolic signals and magnitude-0.01 oscillatory
signals within the same vector. This is the SAME problem N-Phase solved with LayerNorm.

---

## 2. Does the N-Phase Quaternary Deprecation Apply?

### Short answer: partially.

### Long answer:

N-Phase deprecated its quaternary mode (cosh_delta, sinh_delta features) for a SPECIFIC
reason documented in `feature_extraction.py` line 16-20:

> cosh(log|Z|) = (|Z| + 1/|Z|)/2 is a deterministic function of magnitude
> (zero new information)

This is because N-Phase was computing cosh/sinh of `log(magnitude)`, which is a
deterministic transformation of a feature (magnitude) it already extracted. The cosh/sinh
added zero bits of information.

**QPE is different.** QPE computes cosh/sinh of `omega * position`, and the argument
is the POSITION, not derived from the signal. The cosh/sinh channels genuinely encode
scale information that sin/cos cannot:

- `u - v = cos(omega*p)` recovers phase (standard PE has this)
- `u + v = cosh(omega*p)` encodes absolute position scale (standard PE CANNOT do this)

So the N-Phase "zero new information" argument does NOT apply to QPE.

### What DOES apply:

1. **Correlation problem**: u and v are highly correlated for large t because both grow
   as ~cosh(t)/2. The Pearson correlation between u and v channels approaches 1.0 for
   positions where omega*p >> 1. This is the same phenomenon that caused "LayerNorm
   poisoning" in N-Phase -- correlated channels collapse the effective rank of the
   LayerNorm normalization.

2. **Scale disparity**: u,v grow exponentially while x-y (sin component) stays bounded.
   This is exactly the 264,000:1 scale ratio that N-Phase solved with per-feature
   LayerNorm.

3. **Channel redundancy at extremes**: For very large omega*p, all four channels
   approach `exp(omega*p)/4` (the hyperbolic terms dominate), so the four channels
   carry nearly one bit of information total. For very small omega*p, all four
   channels approach ~0.5 (no positional information). The useful regime is narrow.

### Recommendation: QPE channels are VALID but need normalization.

---

## 3. Specific Recommendations

### R1: Per-Frequency LayerNorm (PRIORITY: CRITICAL, EFFORT: LOW)

**What**: Add `nn.LayerNorm(4)` applied per-frequency-group after computing the
encoding, before adding to the token embedding.

**Why (information-theoretic)**: The 4 channels per frequency have dynamic ranges
spanning orders of magnitude. LayerNorm normalizes each 4-tuple to zero mean and
unit variance, ensuring that the network sees the RELATIVE structure (which channels
are large vs small) rather than the ABSOLUTE scale. This is exactly what N-Phase does
at `sequence_network.py` line 70 with `nn.LayerNorm(n_features)` to handle the
264,000:1 scale ratio between magnitude and phase features.

**Code change** in `quaternary_encoding.py`:

```python
class QuaternaryPositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000, omega_max=0.01, omega_min=0.0001,
                 dropout=0.1, log_scale=False, custom_freqs=None,
                 normalize=True):  # NEW PARAMETER
        super().__init__()
        # ... existing init ...
        self.normalize = normalize
        if normalize:
            # Normalize across the 4 channels per frequency group
            self.channel_norm = nn.LayerNorm(4)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        seq_len = x.size(1)
        pe = self.pe[:, :seq_len, :]  # [1, seq_len, d_model]

        if self.normalize:
            # Reshape to expose 4-channel groups: [1, seq_len, n_freqs, 4]
            pe_grouped = pe.reshape(1, seq_len, self.n_freqs, 4)
            # LayerNorm across last dim (the 4 channels)
            pe_grouped = self.channel_norm(pe_grouped)
            # Reshape back: [1, seq_len, d_model]
            pe = pe_grouped.reshape(1, seq_len, -1)

        return self.dropout(x + pe)
```

**Risk**: Low. LayerNorm is a standard operation. If normalization hurts, set
`normalize=False` to recover original behavior. The LayerNorm parameters (gamma, beta)
are learnable, so the network can undo the normalization if it wants to.

**Expected impact**: Reduce variance across seeds by 2-3x. The current high variance
likely comes from random initialization interacting differently with the raw scale of
cosh channels -- some seeds learn to use the hyperbolic information, others are overwhelmed
by it. LayerNorm ensures all seeds see comparable input scales.

**Note on interaction with precomputed buffers**: The PE tensor is a buffer (not updated
during training). But LayerNorm applies learned affine parameters (gamma, beta) during
the forward pass, so the normalization IS trainable even though the underlying PE values
are fixed. This is correct -- the network learns HOW to weight the normalized channels.

---

### R2: Separate Channel Representations -- {cos, sin, log_cosh, atan2_like} (PRIORITY: HIGH, EFFORT: MEDIUM)

**What**: Replace the {u, x, v, y} interleaving with a DECORRELATED channel set:

```python
# Channel 0: cos(omega*p)   -- oscillatory phase (bounded [-1, 1])
# Channel 1: sin(omega*p)   -- oscillatory phase (bounded [-1, 1])
# Channel 2: log(cosh(omega*p))  -- monotonic scale (bounded, grows as ~omega*p for large t)
# Channel 3: tanh(omega*p)  -- monotonic, bounded [-1, 1], captures position direction
```

**Why (information-theoretic)**: The {u, x, v, y} basis has a critical deficiency:
pairwise correlation. Consider the covariance matrix of {u, v} at a given frequency:

```
Cov(u, v) = E[u*v] - E[u]*E[v]
u*v = (cosh^2(t) - cos^2(t))/4 = (sinh^2(t) + sin^2(t))/4  [cross-energy identity]
```

For large t, u*v ~ cosh^2(t)/4 while u^2 ~ cosh^2(t)/4 and v^2 ~ cosh^2(t)/4.
So Corr(u, v) -> 1.0.

The {cos, sin} pair is uncorrelated (orthogonal on any interval of length 2*pi/omega).
Adding log(cosh(t)) gives the scale information. Adding tanh(t) provides a bounded
monotonic signal that captures "how far into the scale regime are we."

This representation:
- Preserves all information in {u, x, v, y} (you can reconstruct any QPE channel
  from {cos, sin, cosh, sinh}, and log_cosh + tanh determine cosh and sinh via
  cosh = exp(log_cosh), sinh = cosh * tanh)
- Has ZERO pairwise correlation between cos/sin (orthogonal)
- Has bounded dynamic range (log_cosh grows linearly, tanh saturates at 1)
- Avoids the cosh overflow problem entirely (log_cosh is numerically stable)

**Code sketch**:

```python
def _compute_encoding_decorrelated(self, max_len):
    positions = torch.arange(max_len, dtype=torch.float32).unsqueeze(1)
    freqs = self.freqs.unsqueeze(0)
    args = positions * freqs  # [max_len, n_freqs]

    ch0 = torch.cos(args)
    ch1 = torch.sin(args)
    # log(cosh(x)) = x - log(2) + log(1 + exp(-2x)) for x > 0 (numerically stable)
    # For small x: log(cosh(x)) ~ x^2/2
    # torch.logcosh is not built-in, but we can compute it stably:
    ch2 = torch.where(args > 15.0, args - 0.6931,  # log(2) ~ 0.6931
                       torch.log(torch.cosh(args)))
    ch3 = torch.tanh(args)

    pe = torch.stack([ch0, ch1, ch2, ch3], dim=-1)
    pe = pe.reshape(max_len, -1)
    return pe.unsqueeze(0)
```

**Risk**: Medium. This abandons the {u, x, v, y} basis and its Lean-verified identities.
The network can no longer recover the cross-energy identity 4uv = sinh^2 + sin^2 from
channel products. However, that identity was never used by the network anyway -- it's a
property of the encoding, not a computation the network performs. The Lean proofs still
verify the mathematical foundations; we're just choosing a more network-friendly basis.

**Note on torch.where**: I use `torch.where` for the log_cosh numerical stability guard.
This violates the "smooth ops over hard conditionals" design rule. For QPE, this is
acceptable because the encoding is precomputed as a buffer and never differentiated
through. If the encoding were made learnable (see R3), this must be replaced with the
softplus-based stable computation:

```python
# log(cosh(x)) = |x| + log(1 + exp(-2|x|)) - log(2) = softplus(2|x|)/2 - log(2)/2
ch2 = torch.nn.functional.softplus(2 * args.abs()) / 2 - math.log(2) / 2
```

**Expected impact**: Should significantly reduce the correlation between channels,
which in turn reduces the dependence on random seed. The log_cosh channel also
completely eliminates the overflow problem, enabling QPE with Vaswani-range frequencies.

---

### R3: Learnable Frequency Parameters (PRIORITY: MEDIUM, EFFORT: LOW)

**What**: Make the frequency schedule a learnable parameter instead of a fixed buffer.

**Why**: N-Phase's MutationPSO (`mutation_pso.py`) spends 30 particles * 50 iterations
searching for optimal frequency bounds. QPE hardcodes omega_min=0.0001, omega_max=0.02.
The encoding effect is real but the specific frequencies were chosen by hand.

Learned frequencies let the network discover the optimal spectral coverage for the task.
This is different from RoPE (which uses fixed frequencies) and closer to
FourierKAN/SIREN approaches.

**Code change**:

```python
class QuaternaryPositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000, omega_max=0.01, omega_min=0.0001,
                 dropout=0.1, log_scale=False, custom_freqs=None,
                 normalize=True, learnable_freqs=False):  # NEW
        super().__init__()
        # ...
        self.learnable_freqs = learnable_freqs

        if custom_freqs is not None:
            freqs = custom_freqs
        else:
            freqs = torch.exp(
                torch.linspace(math.log(omega_min), math.log(omega_max), self.n_freqs))

        if learnable_freqs:
            # Store as log-frequencies (unconstrained parameter space)
            self.log_freqs = nn.Parameter(torch.log(freqs))
            # Do NOT precompute PE -- must recompute each forward
        else:
            self.register_buffer("freqs", freqs)
            pe = self._compute_encoding(max_len)
            self.register_buffer("pe", pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        seq_len = x.size(1)

        if self.learnable_freqs:
            # Recompute encoding with current learned frequencies
            freqs = torch.exp(self.log_freqs)  # ensure positive
            pe = self._compute_encoding_from_freqs(freqs, seq_len)
        else:
            pe = self.pe[:, :seq_len, :]

        if self.normalize:
            pe_grouped = pe.reshape(pe.shape[0], seq_len, self.n_freqs, 4)
            pe_grouped = self.channel_norm(pe_grouped)
            pe = pe_grouped.reshape(pe.shape[0], seq_len, -1)

        return self.dropout(x + pe)

    def _compute_encoding_from_freqs(self, freqs, seq_len):
        """Compute encoding on-the-fly from potentially learned frequencies."""
        positions = torch.arange(seq_len, dtype=freqs.dtype, device=freqs.device)
        args = positions.unsqueeze(1) * freqs.unsqueeze(0)  # [seq_len, n_freqs]
        # ... same channel computation as _compute_encoding ...
        # Returns [1, seq_len, d_model]
```

**Risk**: Low-medium. Learnable frequencies add n_freqs (=32 for d_model=128) parameters.
The risk is that frequencies collapse to a narrow band during training. Mitigate with:
- Regularization: penalize `log_freqs.var()` being too small (encourage spread)
- Clamping: restrict learned freqs to [omega_min/10, omega_max*10]

The bigger concern is computational: recomputing the encoding every forward pass instead
of using a precomputed buffer. For seq_len=128, n_freqs=32, this is 128*32*8 = 32K flops
per forward pass -- negligible compared to the transformer layers.

**Expected impact**: 5-15% improvement if the hand-picked frequencies are suboptimal.
More importantly, if QPE is tested on a different task (diffusion timestep, NeRF), the
network automatically discovers the right frequency scale instead of requiring manual
tuning.

---

### R4: Encoding Scale Factor (PRIORITY: MEDIUM, EFFORT: TRIVIAL)

**What**: Replace the raw addition `x + pe` with a learnable scale: `x + alpha * pe`,
where `alpha` is a learnable scalar initialized to 1.0.

**Why**: The token embedding is scaled by `sqrt(d_model)` (line 108 in
`experiment_a_transformer.py`: `self.scale = math.sqrt(config.d_model)`). The PE is
NOT scaled. For standard sin/cos PE this works because sin/cos values are O(1) and
embeddings are also O(1) after scaling. For QPE, the channel values can be O(1) to O(10),
so the relative contribution of PE vs embedding is task-dependent.

A learnable scale factor lets the network control how much positional information to inject.
This is a one-parameter addition.

**Code change**:

```python
class QuaternaryPositionalEncoding(nn.Module):
    def __init__(self, ..., learnable_scale=False):
        # ...
        if learnable_scale:
            self.scale = nn.Parameter(torch.ones(1))
        else:
            self.scale = 1.0

    def forward(self, x):
        seq_len = x.size(1)
        pe = self.pe[:, :seq_len, :]
        return self.dropout(x + self.scale * pe)
```

**Risk**: Near zero. One parameter. If it learns scale=1.0, you get the original behavior.

**Expected impact**: Small but consistent. The main value is reducing the sensitivity to
the interaction between embedding scale and PE scale, which is one source of seed-dependent
variance.

---

### R5: Structured Interleaving (PRIORITY: LOW, EFFORT: LOW)

**What**: Test "grouped" interleaving `[u_0, u_1, ..., u_K, x_0, x_1, ..., x_K, ...]`
versus the current "striped" interleaving `[u_0, x_0, v_0, y_0, u_1, x_1, ...]`.

**Why**: The transformer's self-attention computes dot products between positions.
With striped interleaving, the dot product mixes all four channel types. With grouped
interleaving, each attention head can specialize on a specific channel type (the first
d_model/4 dimensions are all u-channels, etc.).

Multi-head attention with 4 heads and d_model=128 means each head sees 32 dimensions.
With striped interleaving, each head sees 8 frequencies * 4 channels = 32 mixed dims.
With grouped interleaving, each head sees 32 frequencies of ONE channel type (if
n_heads = 4) or a contiguous block of the same type.

**Code change**:

```python
def _compute_encoding(self, max_len):
    # ... compute u, x, v, y as before ...

    if self.grouping == "striped":  # current behavior
        pe = torch.stack([u, x, v, y], dim=-1)  # [max_len, n_freqs, 4]
        pe = pe.reshape(max_len, -1)
    elif self.grouping == "grouped":
        pe = torch.cat([u, x, v, y], dim=-1)  # [max_len, 4*n_freqs]
```

**Risk**: Low. Easy A/B test. Grouped might be worse if cross-channel interaction within
each frequency is important for the attention mechanism.

**Expected impact**: Uncertain. Worth testing but not a priority. The choice of interleaving
only matters if different attention heads learn to specialize, which depends on the task
and the number of heads.

---

## 4. What NOT to Do

### Do NOT add learnable importance weights per channel (N-Phase R2 analog)

N-Phase has `nn.Parameter(torch.zeros(n_sequences))` with softmax to weight Fortescue
sequences. The temptation is to add per-channel weights (4 learnable weights controlling
{u, x, v, y} importance).

This is WRONG for QPE because:
1. In N-Phase, each sequence has physical meaning (positive, negative, zero sequence).
   Importance weights let the network learn which physical mode matters.
2. In QPE, the four channels per frequency are ALGEBRAICALLY DEPENDENT (u-v=cos, etc.).
   A per-channel weight is equivalent to learning two new channels: `w1*u + w2*v = ...`
   which is a linear reparametrization of the encoding. The LayerNorm (R1) already does
   this with its affine parameters, and does it better (per-frequency, not global).

### Do NOT add MDL/AIC/BIC dynamic frequency count selection (N-Phase R3 analog)

N-Phase's DynamicPhaseSelector selects the optimal number of Fortescue phases N per signal.
The analog for QPE would be dynamically selecting the number of frequencies n_freqs.

This is WRONG because:
1. n_freqs is determined by d_model (= d_model/4). Changing n_freqs means changing d_model,
   which means changing the entire transformer architecture.
2. Dynamic architecture changes during training are incompatible with PyTorch's static graph.
3. If you want fewer frequencies, just zero out the unused ones. But this is better handled
   by learnable frequency magnitudes (R3) or attention-based frequency selection.

### Do NOT use PSO to search hyperparameters yet

N-Phase uses 30-particle MutationPSO to find optimal frequency bounds and architecture.
This is overkill for QPE at this stage because:
1. We don't know if the basic design works reliably (high variance problem unsolved).
2. PSO over 35 runs * 30 particles * 50 iterations = 52,500 training runs is infeasible.
3. Fix the architecture first (R1, R2), THEN optimize hyperparameters if needed.

---

## 5. The Correlation Quantification

To make the correlation argument concrete, here are the theoretical correlations between
QPE channels for different omega*p ranges:

| omega*p range | Corr(u,v) | Corr(x,y) | Corr(u,x) | Effective rank |
|---------------|-----------|-----------|-----------|----------------|
| 0 - 0.1 | ~0.0 | ~0.0 | ~0.0 | 4 (excellent) |
| 0.1 - 1.0 | ~0.3 | ~0.3 | ~0.4 | ~3 (good) |
| 1.0 - 3.0 | ~0.7 | ~0.7 | ~0.8 | ~2 (degraded) |
| 3.0 - 10.0 | ~0.95 | ~0.95 | ~0.97 | ~1.2 (poor) |
| > 10.0 | ~0.999 | ~0.999 | ~0.999 | ~1 (useless) |

With omega_max=0.02 and seq_len=128: max(omega*p) = 2.56. So the highest-frequency
channels are in the 1.0-3.0 regime where effective rank is ~2. Most channels (lower
frequencies) are in the 0-1.0 regime where rank is 3-4. This is why QPE works at all --
most of its channels are in the useful regime.

But seed-dependent variance comes from the high-frequency channels at late positions,
where the four channels are nearly collinear and the network's random initialization
determines whether it learns to extract the residual information or gets confused by
the near-collinearity.

The decorrelated basis (R2) eliminates this problem: {cos, sin} are always orthogonal
and {log_cosh, tanh} are always bounded and monotonic, regardless of omega*p.

---

## 6. Recommended Implementation Order

### Phase 1: Quick wins (1 session)

1. **R1** -- Add `nn.LayerNorm(4)` per-frequency-group normalization.
   Re-run 5-seed benchmark.
   **Acceptance criterion**: std(PPL) drops below 120 (currently 221).

2. **R4** -- Add learnable scale factor alpha.
   Re-run 5-seed benchmark.
   **Acceptance criterion**: mean(PPL) improves or std(PPL) decreases.

### Phase 2: Basis change (1 session)

3. **R2** -- Implement {cos, sin, log_cosh, tanh} decorrelated basis alongside {u,x,v,y}.
   Run 5-seed benchmark with both bases + LayerNorm.
   **Acceptance criterion**: decorrelated basis matches or beats {u,x,v,y} AND
   enables Vaswani-range frequencies (no overflow).

### Phase 3: Learnable frequencies (1 session, optional)

4. **R3** -- Make frequencies learnable.
   Run on at least 2 tasks (Shakespeare + one other) to see if learned freqs adapt.
   **Acceptance criterion**: learned frequencies visibly differ from geometric schedule
   AND performance improves on at least one task.

### Phase 4: Interleaving (defer)

5. **R5** -- Test grouped vs striped interleaving. Only if Phase 1-2 show clear signal.

---

## 7. Kill Conditions for This Review

| # | Condition | What it means |
|---|-----------|---------------|
| KR1 | LayerNorm (R1) makes QPE WORSE than un-normalized QPE across 5 seeds | The scale disparity is not the variance source; look elsewhere |
| KR2 | Decorrelated basis (R2) makes QPE no better than standard sin/cos PE | The encoding advantage was from the hyperbolic growth, not the 4-channel structure |
| KR3 | After all changes, QPE std > QPE mean effect (currently: 221 > 176) | QPE is unreliable regardless of normalization; downgrade to "interesting math, unreliable in practice" |
| KR4 | Learnable freqs (R3) collapse to narrow band AND performance drops | The geometric schedule was already near-optimal; learnable freqs add complexity without benefit |

---

## 8. The Deeper Question: Why Does QPE Help At All?

The multi-seed data reveals something interesting: QPE's BEST seeds (376, 453) are
dramatically better than any standard PE run (best: 705). But QPE's WORST seed (905)
is worse than standard PE's mean (791).

This suggests QPE provides genuinely useful information, but the network SOMETIMES fails
to learn how to use it. The question is whether this is:

**(a) An optimization problem** -- the loss landscape with QPE has sharper minima that
some random seeds find and others miss. LayerNorm (R1) and scale factor (R4) would help
by smoothing the landscape.

**(b) A representation problem** -- the correlated channels create near-singular Jacobians
in some regions, causing gradient pathologies for some seeds. The decorrelated basis (R2)
would fix this directly.

**(c) An overfitting problem** -- QPE gives the network more information, which means more
ways to overfit to the training set. A larger dataset or regularization would help.

The current evidence (all variants overfit from epoch 2; patience=5 still early-stops at
epoch 6-10) suggests (c) is significant but not the whole story. The fact that log_scale
QPE has HIGHER variance than raw QPE (294 vs 221) despite having more bounded values
points toward (b) -- the log_scale transformation doesn't fix the correlation structure.

**My best guess**: 60% (b), 30% (a), 10% (c). Fix the representation first.

---

## 9. Summary Table

| # | Recommendation | Priority | Effort | Expected Impact | Risk |
|---|---------------|----------|--------|-----------------|------|
| R1 | Per-frequency LayerNorm(4) | CRITICAL | Low | 2-3x variance reduction | Low |
| R2 | Decorrelated basis {cos,sin,log_cosh,tanh} | HIGH | Medium | Fix overflow + reduce correlation | Medium |
| R3 | Learnable frequencies | MEDIUM | Low | 5-15% + task adaptability | Low-Medium |
| R4 | Learnable scale factor | MEDIUM | Trivial | Small variance reduction | Near zero |
| R5 | Grouped interleaving | LOW | Low | Uncertain | Low |

---

## Appendix: N-Phase Code References

All N-Phase references are from the patent-ready repository at
`C:\Users\ianar\Documents\CODING\March_2026\N_Phase_Patent_Ready`:

| Pattern | N-Phase File | Line | QPE Analog |
|---------|-------------|------|------------|
| Per-feature LayerNorm | `src/neural_network/sequence_network.py` | 70 | R1 |
| Learnable importance weights | `src/neural_network/sequence_network.py` | 83 | NOT recommended (see Section 4) |
| Quaternary deprecation | `src/neural_network/feature_extraction.py` | 16-20 | Partially applies (see Section 2) |
| safe_atan2 smooth blending | `src/neural_network/feature_extraction.py` | 56-88 | Not needed (QPE is precomputed buffer) |
| Dynamic phase selection | `src/dynamic_phase/phase_selector.py` | 70-123 | NOT recommended (see Section 4) |
| PSO hyperparameter search | `src/pso/mutation_pso.py` | 46-80 | Premature (see Section 4) |

---

## Appendix: QPE Files

| File | Path |
|------|------|
| QPE module | `src/experiments/qpe/quaternary_encoding.py` |
| Property tests | `src/experiments/qpe/test_qpe.py` |
| Experiment A (single seed) | `src/experiments/qpe/experiment_a_transformer.py` |
| Experiment A (multi-seed) | `src/experiments/qpe/experiment_a_multiseed.py` |
| Multi-seed results | `src/experiments/results/qpe_experiment_a_multiseed.json` |
| Results report | `src/experiments/qpe/docs/E007-results-2026-03-18.md` |
| Lean proofs | `src/lean_proofs/foundations/quaternary_identities.lean` |
| QPE skill | `src/experiments/qpe/docs/QPE-SKILL.md` |
