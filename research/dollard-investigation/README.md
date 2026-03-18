# Dollard Investigation — Reference Copy

**Canonical location**: `../dollard-exact-construction/` (private sibling repo)
**This copy**: Reference for context within the formal verification project
**Date**: 2026-03-17
**Status**: RESOLVED — zero-error finding was IEEE 754 coincidence

## What Happened

A full-day investigation (2026-03-17) explored whether Dollard's quaternary decomposition
has computational properties beyond its algebraic content (Z4). Three research councils,
two experiments, and one critical source-text QA produced these results.

## What Survived (Valid, Valuable)

1. **Gross/net energy framework** — cosh/|cos| connects Q, SWR, directional couplers
2. **N-phase generalization** — gross/net divergence for all N, mod-N = Fortescue
3. **Stride-4 Taylor** — 40% FLOP savings for all-four-at-once computation
4. **Conditioning diagnostic** — free from Fortescue, monitors resonance proximity
5. **Z4 verdict** — Dollard's algebra IS Z4 (council/dollard-pure-construction/)
6. **Source text methodology** — dollard-lens skill, follow-the-process mandate

## What Did Not Survive

- Zero-error finding → IEEE 754 coincidence (Experiments 001+002)
- Lifted representation / DPQA → killed (spectral radius e^theta > 1)
- Computational superiority claim → standard rotation wins 979/1000

## Directory Contents

```
council/
  dollard-pure-construction/    8 files — Z4 verdict (CORRECT, foundational)
  quaternary-performance/       7 files — performance analysis (WRONG construction, caveated)
  lifted-representation/        7 files — lifted rep analysis (WRONG construction, caveated)
tessarine-discovery/            5 files — tessarine hypothesis (generated & killed)
dollard-theorist/               4 files — exact construction pivot, tessarine, DPQA
INVESTIGATION_STATUS.md         Master status (RESOLVED)
WHAT_WE_GOT_WRONG.md           Honest error account
lifted-representation-question-alignment.md    Ian's research question
lifted-representation-signal-processing.md     Signal processing exploration
dollard-bookkeeping-discovery-presentation.html  12-slide presentation (pre-correction)
```

## How This Connects to Formal Verification

| Surviving finding | Relevance to this repo |
|-------------------|----------------------|
| Z4 verdict | Confirms the Lean proofs (h=-1, algebra=Z4) |
| Gross/net framework | Track B paper material; N-Phase patent enhancement |
| Stride-4 advantage | Niche but relevant for custom numerical implementations |
| Conditioning diagnostic | Useful for any Fortescue-based computation |
| Source text mandate | Methodology applicable to ALL external math system analysis |
