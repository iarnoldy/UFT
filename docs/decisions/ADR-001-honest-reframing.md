# ADR-001: Honest Reframing of Dollard Verification Project

## Status

Accepted

## Context

The original UFT_Formal_Verification project described itself as achieving
"EXTRAORDINARY SUCCESS" for verifying basic complex arithmetic. An honest audit
revealed:

1. **The verified math is standard.** h,j,k as 4th roots of unity is trivial.
   Telegraph expansion is standard complex multiplication. These are not novel findings.

2. **One genuine finding exists.** The versor form equivalence claim is provably wrong:
   when h = -1, h(XB+RG) != (XB+RG). This is a real result.

3. **The methodology is novel.** Using Lean 4 to formally verify alternative/fringe
   mathematical frameworks has legitimate academic value.

4. **UFT claims are unsupported.** Aether, over-unity, anti-gravity, E=mc2 replacement
   have zero formal backing. The project documentation treated them as credible research
   directions without evidence.

5. **Documentation was severely inflated.** "EXTRAORDINARY SUCCESS" for basic arithmetic.
   "First formal verification" framing obscured that the math being verified was standard.

## Decision

Reframe the project around three research tracks:

- **Track A (Primary)**: Methodology -- Lean 4 for alternative math verification.
  This is the genuinely novel contribution.
- **Track B**: Mathematical analysis -- catalog where Dollard's math equals standard
  math and where it provably errs.
- **Track C**: Physics claims -- documented with UNFALSIFIABLE/EXTRAORDINARY tags,
  not centered in the project.

Adopt the polymathic-research system with pre-registration and falsification criteria.
Discard advocacy documents (Core_Theoretical_Framework, Academic_Paper, Experimental_Predictions).
Preserve the real work (Lean proofs, source materials, claim extraction).

## Consequences

### Positive
- Academically viable -- honest methodology paper is publishable
- Intellectually honest -- no inflated claims
- Preserves novel contribution (Lean 4 for alternative math)
- Clear downstream protocol for N-Phase system

### Negative
- Discards significant documentation effort (papers, frameworks)
- Requires rebuilding project narrative from scratch

### Neutral
- Physics claims remain documented but not centered
- Source materials preserved for future investigation
