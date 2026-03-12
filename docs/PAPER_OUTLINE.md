# Formal Verification of Alternative Mathematical Frameworks: A Case Study Using Lean 4

**Track A Methodology Paper — Outline**

**Target venue:** CICM 2026 (19th Conference on Intelligent Computer Mathematics)
- Ljubljana, Slovenia, September 21-25, 2026
- Abstract deadline: **March 25, 2026** | Paper deadline: **April 1, 2026**
- Regular paper: up to 15 pages + bibliography, LNCS format
- Published in Springer LNAI
- Fallback: JAR (Journal of Automated Reasoning, rolling submission)
- ITP 2026 deadline passed (Feb 19); CPP 2026 already held (Jan 2026)

---

## Abstract (~150 words, draft)

We present a systematic protocol for applying interactive theorem provers to claims originating from alternative or non-standard mathematical frameworks. Using Lean 4 and mathlib, we extract formalizable assertions from such sources, translate them into dependent type theory, and attempt proof or disproof — reporting results without prejudice. We demonstrate the protocol through a case study on Eric Dollard's "versor algebra," a non-standard extension of electrical engineering mathematics. Results are deliberately mixed: we verify a Z_4 cyclic group structure (trivially correct), disprove a claimed versor-form equivalence (sign error), establish by algebraic necessity that the proposed operators collapse to standard 4th roots of unity, trace the algebraic path from Z_4 through Clifford algebras Cl(1,1), Cl(3,0), Cl(1,3) to spacetime algebra, and classify remaining claims as notation-ambiguous or unfalsifiable by formal methods. We argue that mixed outcomes are the expected and methodologically interesting case, and propose a five-category taxonomy for classifying claims from alternative frameworks. To our knowledge, this represents the first application of interactive theorem provers to formalize claims from fringe mathematical sources.

---

## 1. Introduction

- Theorem provers have verified major results: Flyspeck (Kepler conjecture), Four Color Theorem, Tao et al. PFR, Liquid Tensor Experiment, NF consistency
- Common thread: all targets are mainstream mathematics (contested, complex, or uncertain, but within accepted frameworks)
- Gap: no prior art applying theorem provers to claims from alternative/fringe mathematical frameworks (95% confidence after exhaustive search — see `research/scratch/prior-art-deep-search.md`)
- Why the gap exists: cultural separation, no academic incentive, asymmetric difficulty, no client (see Section 6.2)
- This paper's contribution:
  - A systematic protocol for extract-translate-verify on non-standard sources
  - A case study demonstrating mixed results (the interesting case)
  - A taxonomy for classifying outcomes
  - A Clifford algebra hierarchy showing the "correct" path from the source claims
- Explicit framing: this is NOT a debunking exercise — it is a methodology paper; neutral stance throughout

## 2. Related Work

### 2.1 Formalization of Contested or Complex Mathematics
- **Flyspeck** (Hales et al.) — Kepler conjecture, referee-disputed proof verified in HOL Light/Isabelle
- **Liquid Tensor Experiment** (Commelin et al. 2022) — Scholze challenged Lean community to formalize a theorem where even the *author* had doubts. Verified correct. [Quanta, 2021]
- **NF Consistency** (Wilshaw 2024) — Quine's New Foundations consistency proof formalized in Lean after mainstream reviewers could not confidently evaluate Holmes' proof. [arXiv:1503.01406]
- **PFR formalization** (Tao et al.) — rapid formalization of a new result in Lean 4
- **Four Color Theorem** (Gonthier, Coq)
- **Key distinction**: All of these are contested-within-mainstream, not alternative/fringe

### 2.2 Formalization of Physical Theories
- **PhysLean/HepLean** (Tooby-Smith 2025) — digitalizing physics in Lean 4 across classical mechanics, relativity, QFT, Standard Model. Published in Computer Physics Communications. Formalizes *mainstream physics*, not alternative claims.
- **Chemical physics in Lean** (Bobbin et al. 2024) — Langmuir and BET theories of adsorption. Demonstrated Lean catches faulty logic and reveals hidden assumptions. Published in Digital Discovery (RSC). Closest methodological parallel: using Lean to expose hidden assumptions in theoretical derivations.

### 2.3 Historical Mathematics Formalization
- **Newton's Principia** (Fleuriot & Paulson, ~2001) — formalized Newton's geometric proofs in Isabelle/HOL using nonstandard analysis. Discovered a flaw in one of Newton's proofs. *Closest near-miss*: uses proof assistant on historical non-rigorous reasoning and finds errors. Differs because Newton is mainstream; the "non-standard" aspect is proof style, not framework.

### 2.4 Clifford Algebra Formalization
- **Geometric Algebra in Lean** (Wieser & Song, 2021) — formalized Clifford algebras in Lean 3/mathlib. The mathematical objects overlap with our case study (versors, Clifford algebras). Published in Advances in Applied Clifford Algebras. Formalizes standard theory, not alternative claims.

### 2.5 Philosophy of Formal Verification
- **Avigad** — understanding, FV, and philosophy of mathematics (Carnegie Mellon)
- **Imbert & Ardourel** (2023) — FV's epistemological role in computational science (Philosophy of Science, Cambridge)
- **Shulman** (2024) — "Strange New Universes": proof assistants for exploring non-standard foundations (HoTT). Discusses exploring alternative foundations, but these are rigorous alternative *foundations* proposed by credentialed mathematicians, not fringe claims.
- **Harris** — Formal proof and epistemic value

### 2.6 The Gap
- After exhaustive search (30+ queries, 10 source categories, 8 near-misses analyzed), **no prior art found** for theorem-prover verification of fringe/alternative mathematical claims
- The gap is structural: cultural separation + no academic incentive + no client (see Section 6.2)
- This paper fills that gap

## 3. The Protocol

- **Step 1: Source Identification** — Identify alternative mathematical framework with specific algebraic or structural claims
- **Step 2: Claim Extraction** — Enumerate all formalizable assertions; separate from rhetoric, physics claims, philosophical framing
- **Step 3: Translation** — Map claims to dependent type theory; document all translation choices and ambiguities
- **Step 4: Verification Attempt** — For each claim: prove, disprove, or classify as unformalizable/ambiguous
- **Step 5: Taxonomy Classification** — Assign each claim to one of five categories (see Section 5)
- **Step 6: Neutral Reporting** — Present all results without editorial judgment on the source framework

**Key principle:** Individual techniques are standard Lean 4 tactics (`ring`, `simp`, `norm_num`, `ext`, etc.). The innovation is in the application domain and the systematic protocol.

## 4. Case Study: Dollard's Versor Algebra

### 4.1 Background
- Eric Dollard's work in electrical engineering and alternative electromagnetic theory
- Versor algebra: proposed extension/alternative to standard complex and quaternion methods
- Sources: four foundational documents (Lone Pine Writings, Four Quadrant Theory, Versor Algebra, Advanced Versor Algebra II-23)
- Historical context: Fortescue (1918) symmetrical components, Cherry (1951) Lagrangian circuit theory, Heaviside (1880s) telegraph equation
- Sign convention note: Dollard uses Y = G - jB (negative susceptance), not standard Y = G + jB

### 4.2 VERIFIED: Z_4 Cyclic Group Structure
- Claim: operators {1, j, h, k} form a cyclic group with j^2=-1, h^2=1, k=hj=-j, jk=1
- Result: trivially verified — this is Z_4 = {1, i, -1, -i} under multiplication
- Lean: `basic_operators.lean` (0 sorry)
- Significance: confirms Dollard's framework includes correct standard results

### 4.3 DISPROVED: Versor Form Equivalence
- Claim: ZY = h(XB+RG) + j(XG-RB) is equivalent to standard form (RG+XB) + j(XG-RB)
- Result: disproved — real parts have opposite signs when h = -1
- Lean: `telegraph_equation.lean` (`versor_form_value`, 0 sorry)
- Robust: holds regardless of sign convention (Dollard or standard)
- This is the paper's strongest individual result

### 4.4 ALGEBRAIC NECESSITY: h = -1 Forced
- Given j^2=-1, hj=k, jk=1, the value h=-1 is algebraically forced over ANY field
- h^1=-1 and h^2=1 are REDUNDANT axioms
- Lean: `algebraic_necessity.lean` (`algebraic_necessity_general`, 0 sorry)
- Closes the rehabilitation question: cannot escape Z_4 without dropping at least two axioms

### 4.5 THE PATH FORWARD: Clifford Algebra Hierarchy
- Z_4 -> Cl(1,1) -> Cl(3,0) -> Cl(1,3): increasing dimension, increasing physical content
- Cl(1,1): what Dollard SHOULD have used. Idempotent projectors P+, P- decompose forward/backward waves. jk=1 FAILS. Non-commutative. Lean: `cl11.lean` (0 sorry)
- Cl(3,0): Pauli algebra. EM field as F = E + I*B. 3D rotations. Lean: `cl30.lean` (0 sorry)
- Cl(1,3): Spacetime algebra. Maxwell's four equations become one: nabla*F = J. Lean: `cl31_maxwell.lean` (0 sorry)
- The hierarchy shows Dollard's *instinct* (algebraic unification of EM) was correct; his *execution* (commutative Z_4) was too restrictive

### 4.6 AMBIGUOUS: Notation Issues
- h = sqrt(+1)^(1/2) is mathematically ambiguous
- Formal methods precisely IDENTIFY the ambiguity (contribution: showing where the framework is under-specified)
- Resolution: algebraic necessity makes the notation irrelevant (h is forced to -1 regardless)

### 4.7 UNFALSIFIABLE: Physics Claims
- "Electricity is fundamental," "aether as 5th state," "E=mc^2 replacement"
- Theorem provers cannot address empirical claims
- Classification as unfalsifiable is itself a useful result — separates checkable from uncheckable

## 5. A Taxonomy for Claims from Alternative Frameworks

Five categories (present as a table/figure):

| Category | Definition | Example from Case Study |
|---|---|---|
| **VERIFIED** | Claim is mathematically correct; formal proof produced | Z_4 structure |
| **DISPROVED** | Claim is mathematically false; formal counterexample or contradiction produced | Versor form equivalence (sign error) |
| **ALGEBRAIC NECESSITY** | Claim's premises force a specific conclusion the author did not intend | h = -1 forced; Z_4 is the only algebra |
| **AMBIGUOUS** | Claim cannot be formalized without resolving notation/definition gaps | h = sqrt(+1)^(1/2) notation |
| **UNFALSIFIABLE** | Claim is not addressable by formal mathematical methods | Physics/empirical claims |

- Argue: mixed results across categories are the expected and interesting case
- Uniform rejection would suggest the framework is too incoherent to formalize
- Uniform verification would suggest the framework is standard math with different notation
- Mixed results reveal genuine structure worth analyzing

## 6. Discussion

### 6.1 Why Mixed Results Matter
- Pure debunking is uninteresting (no methodological contribution)
- Pure verification is unlikely for alternative frameworks
- Mixed results demonstrate the protocol's value: it discriminates
- The sign error (Section 4.3) is a genuine finding that could not have been established with certainty without formalization
- The Clifford hierarchy (Section 4.5) shows formal methods can constructively suggest "what the author should have said"

### 6.2 Why the Gap Exists
Four structural factors explain the absence of prior art:
1. **Cultural separation**: formal verification and alternative mathematics communities have zero overlap
2. **No academic incentive**: no new theorems, no library contributions, risk of seeming to legitimize pseudoscience
3. **Asymmetric difficulty**: translation from informal fringe claims to formal language requires mathematical expertise and judgment
4. **No client**: fringe proponents don't seek verification (might disprove claims); mainstream doesn't need it (already rejects claims)

### 6.3 Implications for the Lean/ITP Community
- Novel application domain for existing tools
- No new tactics or libraries required — standard mathlib suffices
- Pedagogical value: formalizing "wrong" math teaches proof techniques and exposes hidden assumptions
- Complements Bobbin et al.'s (2024) approach of using Lean to catch hidden assumptions

### 6.4 The Constructive Dimension
- Beyond verification/refutation, formal methods can suggest corrections
- The Clifford algebra hierarchy is a constructive contribution: it traces the path from the alternative claim to the correct mathematical framework
- This goes beyond demarcation to mathematical rehabilitation

## 7. Limitations

- **Single case study**: Protocol demonstrated on one framework only; generalizability to other alternative frameworks is conjectured, not proven
- **Source ambiguity**: Dollard's works are self-published presentations, not peer-reviewed papers. Translation choices are judgment calls, all documented.
- **Compilation status**: Lean 4 proofs have not been machine-compiled against mathlib at time of writing (requires environment setup). All proofs use standard tactics and should compile.
- **Partial formalization**: Not all claims from the source materials were formalized. The polyphase formula has 3 sorry gaps on standard mathlib API calls.
- **Prior art search**: Not a systematic literature review. 95% confidence no prior art exists, with ~5% residual risk from unpublished work, non-English literature, and unindexed theses.
- **Scope**: We formalize algebraic/structural claims only. We make no claims about the physics, engineering utility, or broader validity of Dollard's work.

## 8. Conclusion

- Summarize protocol, case study results, taxonomy
- Restate the methodological contribution: theorem provers can be productively applied to alternative mathematical frameworks
- The value is in discrimination (mixed results) and construction (Clifford hierarchy), not judgment
- Call for further case studies on other alternative frameworks to validate the protocol

---

## Figures and Tables

1. **Table 1:** Taxonomy of claim categories (Section 5) — the five-category classification
2. **Figure 1:** Protocol flowchart — Steps 1-6
3. **Table 2:** Summary of all 17 formalized claims with category assignments and Lean proof references
4. **Figure 2:** The algebraic necessity proof — key derivation alongside Lean code
5. **Figure 3:** The Clifford algebra hierarchy: Z_4 -> Cl(1,1) -> Cl(3,0) -> Cl(1,3)
6. **Table 3:** Comparison with prior formalization efforts — scope, techniques, target type, distinguishing features

## References

### Must-cite (closest work):
1. Fleuriot, J. & Paulson, L. "Mechanizing Nonstandard Real Analysis." Cambridge, ~2001.
2. Bobbin, M.P. et al. "Formalizing chemical physics using the Lean theorem prover." Digital Discovery, RSC, 2024.
3. Tooby-Smith, J. "HepLean: Digitalising high energy physics." Computer Physics Communications, Vol. 308, 2025.
4. Imbert, C. & Ardourel, V. "Formal Verification, Scientific Code, and Epistemological Heterogeneity." Philosophy of Science, 2023.
5. Shulman, M. "Strange new universes: Proof assistants and synthetic foundations." Bull. AMS, 61(2), 2024.
6. Wilshaw, S. "New Foundations is consistent." Lean formalization, 2024. [leanprover-community/con-nf]

### Should-cite (context):
7. Gamboa, R. "Mechanizing Real Analysis in ACL2." PhD, UT Austin, 1999.
8. Wieser, E. & Song, U. "Formalizing Geometric Algebra in Lean." Adv. Appl. Clifford Algebras, 2021.
9. Commelin, J. et al. "Completion of the Liquid Tensor Experiment." Lean Community, 2022.
10. Tao, T. et al. "Polynomial Freiman-Ruzsa conjecture." Lean 4 formalization, 2023.

### Background:
11. de Moura, L. et al. — Lean 4 (dependent type theory, metaprogramming)
12. Mathlib community — mathlib4 library
13. Hales, T. et al. — Flyspeck project
14. Gonthier, G. — Four Color Theorem in Coq
15. Avigad, J. — Understanding, FV, and philosophy of mathematics
16. Fortescue, C.L. "Method of Symmetrical Co-ordinates Applied to Polyphase Networks." AIEE Trans., 1918.
17. Cherry, E.C. — Lagrangian circuit theory (1951). [TODO: confirm exact reference]
18. Dollard, E.P. — primary source material [self-published; cite specific documents used]
19. Hestenes, D. "Space-Time Algebra." Gordon and Breach, 1966.
20. Doran, C. & Lasenby, A. "Geometric Algebra for Physicists." Cambridge, 2003.

## Open Questions

- [x] Confirm no prior art exists (exhaustive search completed, 95% confidence)
- [x] Verify Cherry 1951 exact reference — "Some general theorems for non-linear systems possessing reactance," Phil. Mag. 42(333), 1161-1177, DOI: 10.1080/14786445108561362
- [x] Identify citable Dollard sources — "Lone Pine Writings", "Four Quadrant Theory", "Versor Algebra", "Advanced Versor Algebra II-23" (self-published)
- [x] Determine venue — CICM 2026 (Ljubljana, Sep 21-25). Abstract Mar 25, Paper Apr 1. 15pp + bib, LNCS. See `research/venue-research.md`
- [x] Compile all Lean proofs against mathlib — DONE (3269 jobs, 0 errors, 0 sorry)
- [x] Consider whether "alternative mathematical framework" needs a formal definition in the paper — YES, defined in Section 1 (line 95-100 of paper1.tex)
- [x] Explore whether the ALGEBRAIC NECESSITY category has precedent in logic/philosophy of mathematics — YES: Lakatos duality (axioms too strong vs too weak), Fagin-Halpern implicit commitment, Banach-Tarski as canonical example. All cited in Section 5.
- [x] Draft paper — `paper/paper1.tex` (LNCS format, complete first draft)
- [x] Confirm Dollard's Psi/Phi definitions from primary sources — Psi=Coulombs (charge), Phi=Webers (flux), matches Lagrangian circuit theory exactly
