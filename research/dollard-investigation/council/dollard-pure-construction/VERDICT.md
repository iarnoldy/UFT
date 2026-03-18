# VERDICT: Dollard's Pure Construction from Epsilon

**Investigation**: dollard-pure-construction
**Date**: 2026-03-17
**Orchestrator**: Research Council (Sophia 3.1)
**Rounds completed**: 5 of 5 (no kills fired)

---

## One-Paragraph Verdict

Dollard's mathematical construction, followed step by step on his own terms from epsilon through h, j, k to the quaternary expansion and polyphase theory, IS the algebra Z_4 (the cyclic group of fourth roots of unity, equivalent to the complex numbers restricted to {1, i, -1, -i}). The algebraic collapse h = -1 is instantaneous -- Dollard himself writes h = -1 in the same equation where he introduces h. There is no intermediate state where operational content could survive algebraic classification. The quaternary expansion (four subseries of e^t) is mathematically correct but is the standard mod-4 subseries decomposition, containing zero information beyond what cos, sin, cosh, sinh already contain. Dollard's specific versor form ZY = h(XB+RG)+j(XG-RB) is wrong in his own algebra. The value of Dollard's work is PRESENTATIONAL (a pedagogically effective construction path that makes physical meaning explicit at every step) and INTERPRETIVE (a bookkeeping discipline that tracks sign origins), not ALGEBRAIC (no new mathematical structure).

## Confidence Level

**92%** that this is the complete and final answer.

The 8% uncertainty is allocated to:
- 5%: the possibility that Dollard's operators could be reinterpreted as elements of a larger algebraic structure a la Mikusiński (no concrete proposal exists, but the path is not provably closed)
- 3%: the possibility that the quaternary expansion has practical computational advantages in specific lossy propagation problems (untested empirically)

## Recommendation

**STOP.**

This line of investigation has reached a definitive conclusion through five independent rounds of analysis. The algebra IS Z_4. Every numerical computation confirms. The prior Lean proofs are validated. Continuing to search for hidden algebraic content in Dollard's operators would be searching for something that three independent analyses (Lean, SymPy, council) have proved does not exist.

## What Was Learned

This investigation was NOT wasted. It produced five substantive results:

1. **The operational/algebraic distinction is real but trivializes for finite algebras.** This is a generalizable insight: when evaluating any alternative mathematical system, "what algebra is it?" is the right question for finite-dimensional cases.

2. **Dollard's construction is a case study in presentation masking simplicity.** Four operators that are really two. A "new math" that is really Steinmetz phasor analysis. Understanding HOW notation creates the appearance of novelty is itself a finding.

3. **MacFarlane's independent h was the road not taken.** Dollard's jk = 1 axiom and MacFarlane's independent h are mutually exclusive. Dollard chose the physical interpretation (counter-rotations cancel) over the algebraic richness (tessarines with independent h). This is a documented design decision, not a mathematical error.

4. **The quaternary expansion is worth knowing about.** It is standard mod-4 subseries decomposition, but it is a non-obvious identity that unifies circular and hyperbolic functions in a single framework. Real value for pedagogy, uncertain value for computation.

5. **Three-round convergence with zero disagreement** between the mathematical analysis (Round 3), the cross-domain literature (Round 2), and the computation (Round 4). The structural vision (Round 1) correctly predicted the outcome. The council methodology works.

## Files

| File | Content |
|------|---------|
| `00-charter.md` | Investigation setup, kill conditions |
| `01-vision.md` | Heptapod B: structural requirements for the distinction |
| `02-literature.md` | Polymathic: prior work across 8 domains |
| `03-analysis.md` | Dollard Theorist: step-by-step reconstruction |
| `04-computation.md` | Python/SymPy: four computational tests |
| `05-synthesis.md` | Heptapod B: revised vision with all evidence |
| `VERDICT.md` | This document |
| `src/experiments/council/dollard_pure_construction_tests.py` | Computation script |
