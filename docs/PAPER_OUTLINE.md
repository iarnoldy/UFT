# Formal Verification of Alternative Mathematical Frameworks: A Case Study Using Lean 4

**Track A Methodology Paper — Outline**

**Target venue:** ITP (Interactive Theorem Proving) workshop or Journal of Automated Reasoning

---

## Abstract (~150 words, draft)

We present a systematic protocol for applying interactive theorem provers to claims originating from alternative or non-standard mathematical frameworks. Using Lean 4 and mathlib, we extract formalizable assertions from such sources, translate them into dependent type theory, and attempt proof or disproof — reporting results without prejudice. We demonstrate the protocol through a case study on Eric Dollard's "versor algebra," a non-standard extension of electrical engineering mathematics. Results are deliberately mixed: we verify a Z_4 cyclic group structure (trivially correct), disprove a claimed versor-form equivalence (sign error), establish by algebraic necessity that a proposed rehabilitation (h = -1) collapses the system to standard quaternion subalgebra, and classify remaining claims as notation-ambiguous or unfalsifiable by formal methods. We argue that mixed outcomes are the expected and methodologically interesting case, and propose a five-category taxonomy for classifying claims from alternative frameworks. To our knowledge, this represents the first application of interactive theorem provers to formalize claims from fringe mathematical sources.

---

## 1. Introduction

- Theorem provers have verified major results: Flyspeck (Kepler conjecture), Four Color Theorem, Tao et al. PFR formalization
- Common thread: all targets are mainstream mathematics (contested or complex, but within accepted frameworks)
- Gap: no prior art applying theorem provers to claims from alternative/fringe mathematical frameworks [NEEDS RESEARCH — 85% confidence]
- Why the gap likely exists: suitable targets are rare (must be specific enough to formalize, yet contain a mix of correct and incorrect claims)
- This paper's contribution:
  - A systematic protocol for extract-translate-verify on non-standard sources
  - A case study demonstrating mixed results (the interesting case)
  - A taxonomy for classifying outcomes
- Explicit framing: this is NOT a debunking exercise — it is a methodology paper; neutral stance throughout

## 2. Related Work

### 2.1 Formalization of Contested or Complex Mathematics
- Flyspeck project (Hales et al.) — Kepler conjecture, referee-disputed proof verified in HOL Light/Isabelle
- Tao et al. PFR formalization in Lean 4 — rapid formalization of a new result
- Four Color Theorem (Gonthier, Coq)
- These are contested-within-mainstream, not alternative/fringe — key distinction

### 2.2 Non-Standard Analysis as Methodological Parallel
- Robinson's non-standard analysis: once-fringe framework later formalized and accepted
- Demonstrates that "non-standard" does not mean "wrong" — some claims survive formalization, some do not
- Relevant attitude: take the framework seriously enough to formalize

### 2.3 Lean 4 and Mathlib
- de Moura et al. — Lean 4 architecture
- Mathlib community — algebraic structures used (groups, rings, etc.)

### 2.4 The Gap
- No prior art found for theorem-prover verification of fringe/alternative mathematical claims [NEEDS RESEARCH]
- Possible explanation: rarity of suitable targets (specific + mixed correct/incorrect)
- This paper fills that gap

## 3. The Protocol

- **Step 1: Source Identification** — Identify alternative mathematical framework with specific algebraic or structural claims
- **Step 2: Claim Extraction** — Enumerate all formalizable assertions; separate from rhetoric, physics claims, philosophical framing
- **Step 3: Translation** — Map claims to dependent type theory; document all translation choices and ambiguities
- **Step 4: Verification Attempt** — For each claim: prove, disprove, or classify as unformalizable/ambiguous
- **Step 5: Taxonomy Classification** — Assign each claim to one of five categories (see Section 5)
- **Step 6: Neutral Reporting** — Present all results without editorial judgment on the source framework

**Key principle:** Individual techniques are standard Lean 4 tactics (`ring`, `simp`, `decide`, etc.). The innovation is in the application domain and the systematic protocol.

## 4. Case Study: Dollard's Versor Algebra

### 4.1 Background
- Eric Dollard's work in electrical engineering and alternative electromagnetic theory
- Versor algebra: proposed extension/alternative to standard complex and quaternion methods
- Sources used (presentations, writings) — document which specific claims were extracted
- Historical context: Fortescue (1918) symmetrical components, Cherry (1951) [NEEDS RESEARCH — verify Cherry reference relevance]

### 4.2 VERIFIED: Z_4 Cyclic Group Structure
- Claim: operators {1, j, -1, -j} under multiplication form a cyclic group of order 4
- Result: trivially verified — this is standard mathematics (Z_4 = Z/4Z)
- Significance: confirms Dollard's framework includes correct standard results
- Lean proof: `decide` or exhaustive case analysis

### 4.3 DISPROVED: Versor Form Equivalence
- Claim: a specific equivalence between versor forms (detail the exact assertion)
- Result: disproved — sign error identified
- Lean proof: counterexample construction
- Significance: genuine mathematical finding; the sign error is not a typo but a structural mistake
- This is the paper's strongest individual result

### 4.4 ALGEBRAIC NECESSITY: h = -1 Forced
- Setup: Given jk = 1, j^2 = -1, and hj = k, what is h?
- Result: algebraic necessity forces h = -1
- Novel proof: closes the question of whether the versor algebra can be "rehabilitated" with a different value of h
- Collapses proposed system to a standard quaternion subalgebra
- Lean proof: algebraic manipulation (`ring` tactic or explicit derivation)

### 4.5 AMBIGUOUS: Notation Issues
- Certain Dollard claims are not formalizable due to notation ambiguity
- Formal methods can precisely IDENTIFY the ambiguity (contribution: showing where the framework is under-specified)
- Examples: [detail specific notation ambiguities encountered]

### 4.6 UNFALSIFIABLE: Physics Claims
- Some claims are physics assertions, not mathematical ones
- Theorem provers cannot address empirical claims
- Classification as unfalsifiable is itself a useful result — separates what CAN be checked from what CANNOT

## 5. A Taxonomy for Claims from Alternative Frameworks

Five categories (present as a table/figure):

| Category | Definition | Example from Case Study |
|---|---|---|
| **VERIFIED** | Claim is mathematically correct; formal proof produced | Z_4 structure |
| **DISPROVED** | Claim is mathematically false; formal counterexample or contradiction produced | Versor form equivalence (sign error) |
| **ALGEBRAIC NECESSITY** | Claim's premises force a specific conclusion the author did not intend | h = -1 forced |
| **AMBIGUOUS** | Claim cannot be formalized without resolving notation/definition gaps | Notation issues |
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

### 6.2 The Rarity of Suitable Targets
- Most alternative mathematical frameworks are too vague to formalize
- Some are entirely correct (just unconventional notation)
- The sweet spot — specific enough to formalize, with mixed correct/incorrect claims — is rare
- This rarity may explain the absence of prior art

### 6.3 Implications for the Lean/ITP Community
- Novel application domain for existing tools
- No new tactics or libraries required — standard mathlib suffices
- Potential pedagogical value (formalizing "wrong" math teaches proof techniques)

## 7. Limitations

- **Search not exhaustive:** Prior art search for theorem-prover applications to fringe math was not systematic (no formal literature review protocol). 85% confidence no prior art exists.
- **Single case study:** Protocol demonstrated on one framework only; generalizability to other alternative frameworks is conjectured, not proven.
- **Dollard notation ambiguity:** Some translation choices in the case study are judgment calls. Different interpretations could yield different results for the AMBIGUOUS category. All choices are documented.
- **Scope of "formalization":** We formalize algebraic/structural claims only. We make no claims about the physics, engineering utility, or broader validity of Dollard's work.
- **Lean 4 / mathlib dependency:** Results are verified within Lean 4's type theory. We do not address meta-theoretic concerns about Lean's foundations (standard limitation, shared with all Lean-based work).

## 8. Conclusion

- Summarize protocol, case study results, taxonomy
- Restate the methodological contribution: theorem provers can be productively applied to alternative mathematical frameworks
- The value is in discrimination (mixed results), not judgment
- Call for further case studies on other alternative frameworks to validate the protocol

---

## Figures and Tables

1. **Table 1:** Taxonomy of claim categories (Section 5) — the five-category classification with definitions and examples
2. **Figure 1:** Protocol flowchart — Steps 1-6 as a diagram
3. **Table 2:** Summary of all formalized claims from the Dollard case study, with category assignments and Lean proof references
4. **Figure 2:** The algebraic necessity proof (h = -1) — key derivation steps shown alongside Lean code
5. **Table 3:** Comparison with prior formalization efforts (Flyspeck, PFR, Four Color) — scope, techniques, target type

## References (to include)

- de Moura, L. et al. — Lean 4 (metaprogramming, dependent type theory)
- Mathlib community — mathlib4 library
- Hales, T. et al. — Flyspeck project (Kepler conjecture formalization)
- Tao, T. et al. — PFR formalization in Lean 4
- Gonthier, G. — Four Color Theorem in Coq
- Robinson, A. — Non-Standard Analysis (1966) [methodological parallel]
- Fortescue, C.L. — "Method of Symmetrical Co-ordinates Applied to the Solution of Polyphase Networks" (1918)
- Cherry, E.C. — (1951) [NEEDS RESEARCH — confirm exact reference and relevance]
- Dollard, E. — primary source material [NEEDS RESEARCH — identify citable sources]
- [NEEDS RESEARCH] — any prior art on formal verification of non-standard/fringe mathematical claims

## Open Questions / Sections Needing Further Research

- [ ] Confirm no prior art exists (systematic literature search needed)
- [ ] Verify Cherry 1951 reference — exact paper title, relevance to versor algebra
- [ ] Identify citable Dollard sources (presentations, self-published works)
- [ ] Determine ITP vs. JAR formatting requirements and page limits
- [ ] Consider whether "alternative mathematical framework" needs a formal definition in the paper
- [ ] Explore whether the ALGEBRAIC NECESSITY category is novel or has precedent in logic/philosophy of mathematics
