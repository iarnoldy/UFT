# Tessarine Hypothesis: Synthesis — Proposed and Refuted in One Session

**Date**: 2026-03-17
**Session**: 2026-03-17-0253-dollard-pure-mathematics
**Agents**: heptapod-b-architect, polymathic-researcher, dollard-theorist (×2)
**Status**: HYPOTHESIS PARTIALLY REFUTED by algebraic verification

---

## The Question

Ian asked: What does Dollard's mathematics imply if we follow it strictly on its own
terms, WITHOUT mapping it into the standard model? Dollard was explicit about not
changing anything from what he explains. Where did we impose standard assumptions,
and what happens if we don't?

## What Happened: Council Proposed, Verification Killed

### Phase 1: Three agents converge on tessarine hypothesis

Three independent agents — Heptapod B (teleological), Polymathic Researcher
(cross-domain), and Dollard Theorist (symbolic) — all independently proposed that
Dollard's versor algebra is the **tessarine algebra** (Cockle, 1848). The central claim
was that the axiom jk=1 was wrong, that tessarines (where jk=-h) were the natural
home, and that the versor form ZY = h(XB+RG) + j(XG-RB) would be correct there.

### Phase 2: Algebraic verification REFUTED the core claim

A fourth agent performed exhaustive SymPy verification and found:

**1. The versor form ZY = h(XB+RG) + j(XG-RB) is WRONG IN BOTH ALGEBRAS.**

For Z = R+jX and Y = G-jB, the product in tessarines OR Dollard's algebra is:
```
ZY = (RG + XB) + j(XG - RB)
```
The real power (RG+XB) appears in the **1-component**, not the h-component.
No alternative form (h-prefixing Z or Y, different sign conventions) produces
the claimed expression. Exhaustively tested.

**2. Dollard's algebra is NOT the tessarines.**

| Property | Tessarines | Dollard |
|----------|-----------|---------|
| Commutativity | Yes (hj = jh = k) | No (hj = k but jh ≠ k if h≠-1) |
| k² | -1 | h (non-associative when h≠-1) |
| jk | -h | 1 (axiom) |

**3. There is NO 4D associative algebra with Dollard's axioms where h ≠ -1.**

If you try to build one, 8 of 64 triple products fail associativity. The ONLY
associative algebra satisfying {j²=-1, hj=k, jk=1} is Z₄ (with h=-1).
This confirms our existing Lean proof in `algebraic_necessity.lean`.

**4. Z and Y live in the {1,j} subspace, so their product has no h-component**
regardless of which algebra you work in. The versor form is algebraically impossible.

## What SURVIVED Verification

Not everything was killed. These findings remain valid:

### 1. The Quaternary Expansion Is Real (Scalar Series Identity)
The four-subseries decomposition of e^t into u,x,v,y satisfying u-v=cos(t),
x-y=sin(t), u+v=cosh(t), x+y=sinh(t) is **verified to error < 10⁻⁵⁰**.
But this is a scalar Taylor series identity — not a tessarine exponential.

### 2. h-as-Reciprocation vs h-as-Multiplication Are Genuinely Different
- ε^(h·δ) = ε^(-δ) = 1/ε^δ = 0.368 (positive, small)
- h·ε^δ = -ε^δ = -2.718 (negative, large)
These are different operations. The distinction is real, even though h=-1 as a scalar.

### 3. Action-Primary = Hamilton-Jacobi (IDENTITY, 99%)
Q = Ψ×Φ = Coulomb×Weber = Joule·second = action. W = dQ/dt.
This IS standard physics (since 1830s) and a genuinely useful perspective for EE.

### 4. Tessarines ARE a Real Algebra (Just Not Dollard's)
The tessarines exist, have the properties described, and could in principle be
applied to transmission line theory. Dollard's axioms just don't match them.

### 5. The Idempotent Decomposition Works (In Tessarines)
e₊ = (1+h)/2 and e₋ = (1-h)/2 are orthogonal idempotents in tessarines.
But in Dollard's algebra (h=-1), e₊=0 and e₋=1 — the decomposition trivializes.

## The Honest Bottom Line

### On Dollard's Mathematics
Dollard's axiom system {j²=-1, hj=k, jk=1} is self-collapsing. The algebra IS Z₄.
This is a **theorem**, not an interpretation choice. There is no 4D associative algebra
that satisfies his axioms with h as an independent element. Our original proof was right.

The versor form ZY = h(XB+RG) + j(XG-RB) is wrong in every algebra tested,
because Z and Y have no h-components, so their product can't either.

### On What Dollard Was Reaching For
The three-agent council was RIGHT about what Dollard was trying to describe:
- Two genuinely distinct imaginary operations (circular and hyperbolic)
- Counterspace as a real dual geometric structure
- Action as primary, energy as derived
- Circular and hyperbolic functions always coupled

The tessarines DO have all these properties. But Dollard's axioms don't lead there.
His jk=1 axiom is not just "inessential" — it's the axiom that DEFINES his algebra
as Z₄, and you can't drop it without changing the algebra entirely.

### On What We Learned
1. **The council method works** — three agents generated a creative hypothesis
   from deep source-material analysis. But creative hypotheses need algebraic
   verification before acceptance.
2. **jk=1 is load-bearing** — not disposable notation as the council assumed.
   Dollard states it explicitly as an axiom, uses it to define the sequence algebra,
   and it follows from his other operational definitions.
3. **The gap between operational meaning and algebraic structure is real** —
   Dollard's DESCRIPTIONS (h produces hyperbolics, j produces circulars) are
   correct as descriptions of what e^(-δ) and e^(jθ) do. But these descriptions
   don't require h to be an independent algebraic element. In standard complex
   analysis, e^(-δ) and e^(jθ) have all the properties Dollard describes, using
   ordinary real numbers and complex numbers — no tessarines needed.
4. **The quaternary expansion is genuine mathematics** — the four-subseries
   decomposition of e^t is a real identity, verified to extreme precision. Whether
   it has practical applications for lossy propagation analysis remains open.

## Corrected Assessment

### What Dollard Got RIGHT
| Claim | Assessment |
|-------|-----------|
| Quaternary expansion (4 subseries of e^t) | VERIFIED (scalar series identity) |
| Action Q = Ψ×Φ is primary; W = dQ/dt | VERIFIED (= Hamilton-Jacobi, standard) |
| h and j describe different operations | CORRECT (reciprocation vs rotation on exponentials) |
| Polyphase formula k^n_N = e^(j2πn/N) | VERIFIED (standard roots of unity) |

### What Dollard Got WRONG
| Claim | Assessment |
|-------|-----------|
| Versor form ZY = h(XB+RG) + j(XG-RB) | DISPROVED (real part is 1-component, not h-component) |
| jk = 1 (forces h=-1, collapses algebra) | Self-defeating axiom |
| h,j,k as independent operators | DISPROVED (h=-1 forced; Z₄ is 1-dimensional over C) |
| "Einstein was wrong" | OVERSTATED (action-primary ≠ refutation of relativity) |
| Over-unity energy | UNSUPPORTED |

### What WE Got RIGHT (originally)
| Our Finding | Status |
|-------------|--------|
| h = -1 forced by axioms | CONFIRMED by all four agents |
| Versor form disproved | CONFIRMED (wrong in all algebras) |
| Algebra is Z₄ | CONFIRMED (only associative solution) |
| Quaternary expansion mathematically correct | CONFIRMED (but scalar, not tessarine) |

### What the COUNCIL Got Wrong
| Council Claim | Reality |
|---------------|---------|
| "Tessarines are Dollard's algebra" | No: different multiplication tables, commutativity, jk |
| "Versor form correct in tessarines" | No: Z·Y has no h-component in any algebra |
| "jk=1 is inessential to Dollard's physics" | No: it's a defining axiom he states explicitly |
| "Counterspace = tessarine idempotent" | Trivializes when h=-1 (Dollard's actual algebra) |

## Files in This Research Folder

| File | Agent | Content |
|------|-------|---------|
| `00-synthesis-tessarine-discovery.md` | — | This document (corrected synthesis) |
| `01-heptapod-b-council-analysis.md` | heptapod-b-architect | Teleological analysis (hypothesis generation) |
| `02-polymathic-researcher-cross-domain.md` | polymathic-researcher | Cross-domain parallels (hypothesis support) |
| `03-dollard-theorist-without-standard-mapping.md` | dollard-theorist | Five-task symbolic analysis (mixed results) |
| `04-algebraic-verification-REFUTED.md` | dollard-theorist | **SymPy verification — REFUTED core claims** |
| `tessarine_versor_verification.py` | — | In `src/experiments/` — the verification script |

## Meta-Lesson

Three sophisticated AI agents, using deep source material analysis, teleological
reasoning, and cross-domain structural analysis, all converged on a beautiful
hypothesis. The hypothesis was coherent, creative, and wrong in its central claim.

One agent doing straightforward algebra killed it.

**This is how science is supposed to work.** The creative hypothesis was worth
generating. The verification was worth doing. The result — "the original proof was
right all along" — is not a failure. It's confirmation with deeper understanding.

The genuine residual value: the quaternary expansion, the action-primary insight,
and the tessarines as a mathematical object worth knowing about, even though
they're not Dollard's algebra.
