# Research Council Charter: Dollard's Pure Construction from Epsilon

**Investigation Slug:** `dollard-pure-construction`
**Date:** 2026-03-17
**Initiated by:** Ian Arnoldy
**Orchestrator:** Research Council (Sophia 3.1)

---

## The Question

**What does Dollard's mathematics imply when we follow his construction step-by-step from epsilon, in HIS order of presentation, without mapping to any known algebra until the final round?**

Specifically:
1. Start from epsilon (epsilon = e^delta) -- Dollard's base object, NOT from abstract algebra axioms
2. Follow HIS construction steps in the order he presents them across all 4 source texts
3. At each step, note what operations he defines and what they DO (operationally), not what algebra they "are"
4. Do NOT compare to Z_4, tessarines, quaternions, or any named algebra until Round 5
5. Track where Dollard's steps force specific algebraic consequences vs. where they leave freedom
6. Map the divergence points: where does his construction predict something DIFFERENT from what we'd get by starting from a standard algebra?

## Why Standard Approaches Failed

Two prior investigations projected standard algebraic frameworks onto Dollard and killed his structure in the process:

1. **Z_4 analysis**: Dollard's axiom system {j^2 = -1, hj = k, jk = 1} was shown to force h = -1, collapsing the algebra to Z_4. The versor form ZY = h(XB+RG) + j(XG-RB) was proved wrong in ALL algebras because Z, Y live in the {1,j} subspace.

2. **Tessarine hypothesis**: Three agents converged on "Dollard's algebra = tessarines." A fourth agent REFUTED this with exhaustive SymPy verification.

Both times the methodology was: "What known algebra does this look like?" followed by forcing a fit. This kills any structure that lives in Dollard's OPERATIONS (what epsilon does, how versor products compose, what the quaternary expansion computes) rather than in his ALGEBRA (what multiplication table the symbols satisfy).

The question is whether there IS such operational content, or whether algebraic classification fully captures everything Dollard defines.

## What a Successful Answer Looks Like

A step-by-step reconstruction of Dollard's mathematical construction that:
- Follows HIS presentation order, not ours
- Distinguishes operational content (what the math DOES) from algebraic classification (what it IS)
- Identifies exactly where algebraic collapse happens and whether Dollard's operational content survives the collapse
- Determines whether Dollard has mathematical content beyond what Z_4 captures -- content that lives in his OPERATIONS rather than his ALGEBRA
- Gives a precise answer: is there genuine mathematical structure here that our algebraic analysis missed by killing it too early?

## Source Materials

### Primary Sources (Dollard's 4 texts)
- `source_materials/PDFs/00_Lone Pine Writings.pdf`
- `source_materials/PDFs/01_fourquadbook.pdf`
- `source_materials/PDFs/02_versoralgebra.pdf`
- `source_materials/PDFs/03_Versor Algebra II-23.pdf`

### Prior Investigation (Phase 1 Tessarine Discovery)
- `research/tessarine-discovery/00-synthesis-tessarine-discovery.md` (corrected synthesis)
- `research/tessarine-discovery/04-algebraic-verification-REFUTED.md` (refutation)

## Pre-registered Kill Conditions

### Round 1 Kill (VISION)
If Heptapod B concludes there is NO structural distinction between "operational content" and "algebraic structure" -- that they are necessarily the same thing in finite-dimensional associative algebras -- then the investigation is over. The premise of the question would be incoherent.

### Round 2 Kill (ARCHAEOLOGY)
No automatic kill. If NO prior work exists distinguishing operational from algebraic content in ANY field, this is a serious warning but not fatal. Note the warning and proceed with caution.

### Round 3 Kill (RIGOR)
If the rigorous step-by-step analysis shows that every operational consequence of Dollard's construction is fully captured by Z_4 or standard complex analysis, with no residual content whatsoever, the investigation is over. Negative result, but informative.

### Round 4 Kill (COMPUTATION)
If computation directly contradicts the mathematical analysis from Round 3 -- e.g., Round 3 says there is residual content but computation shows there is not, or vice versa -- kill. Internal contradiction means the analysis framework is broken.

### Round 5
No kill condition. Synthesis produces the verdict regardless.

## Agent Assignments

| Round | Name | Agent | Purpose |
|-------|------|-------|---------|
| 1 | VISION | `heptapod-b-architect` | Structural requirements for a "Dollard-on-his-own-terms" reconstruction. What is the distinction between operational content and algebraic classification? |
| 2 | ARCHAEOLOGY | `polymathic-researcher` | Prior work on operational vs. algebraic content. Category theory? Constructive math? Operational semantics? |
| 3 | RIGOR | `dollard-theorist` | Step-by-step reconstruction from epsilon = e^delta through all 4 source texts. Operational content vs. algebraic consequence at each step. |
| 4 | COMPUTATION | Direct Python/SymPy | Test operational predictions. Does epsilon-as-operator produce different results from e^delta-as-number? |
| 5 | SYNTHESIS | `heptapod-b-architect` | Compare to known algebras with all evidence in hand. Final verdict. |

## File Plan

```
research/council/dollard-pure-construction/
  00-charter.md           <- This file
  01-vision.md            <- Heptapod B: structural requirements
  02-literature.md        <- Polymathic: prior work
  03-analysis.md          <- Dollard Theorist: step-by-step reconstruction
  04-computation.md       <- Python/SymPy results
  05-synthesis.md         <- Heptapod B: final verdict with all evidence
  VERDICT.md              <- Orchestrator's recommendation
```
