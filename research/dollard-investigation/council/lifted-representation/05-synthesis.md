# Round 5: SYNTHESIS -- The Heptapod B Reckoning

**Investigation**: lifted-representation
**Round**: 5 of 5 (FINAL)
**Agent**: heptapod-b-architect (teleological reasoning)
**Date**: 2026-03-17

---

## Executive Summary

**The quaternary lifted representation (DPQA) is a novel, algebraically elegant,
numerically useless technique.** The question asked was: does staying in the
(u, x, v, y) basis provide measurable computational advantages? The answer is
NO -- and not by a narrow margin. DPQA is exponentially worse than the standard
approach it claimed to improve upon. Three kill conditions fire. Zero of the
five charter tests show advantage. The investigation is COMPLETE.

**VERDICT: STOP.** Clean negative result. No pivot. No continuation.

---

## Part I: The Autopsy of Round 1

I built the vision in Round 1. The evidence destroyed it. Intellectual honesty
requires accounting for exactly what went right, what went wrong, and why.

### What Round 1 Got Right

1. **Operation closure (N1).** The cyclic convolution IS algebraically closed
   under argument addition, differentiation, and integration. This was verified
   in all subsequent rounds. The algebra is real. [Confirmed: Rounds 3, 4]

2. **Novelty assessment.** The technique IS novel. Ten search directions across
   seven disciplines found no exact match. All parallels are analogies, not
   identities. The haversine (1835) is the closest precedent but addresses a
   single function, not a systematic framework. [Confirmed: Round 2]

3. **Structural fusion classifications.** Every analogy score (homogeneous
   coordinates 75%, expm1/log1p 70%, etc.) held up under literature scrutiny.
   No identity was found. No false connection was claimed. [Confirmed: Round 2]

4. **K1 correctly cleared.** Lifted computations exist. The algebraic
   framework works on its own terms.

5. **K7 correctly identified as most threatening.** Round 1 said: "K7 is the
   most dangerous kill condition." This was correct in spirit -- the compensated
   arithmetic comparison ultimately showed DPQA is inferior -- though the
   mechanism of defeat was different than expected.

6. **The 45% overall confidence.** Round 1 said: "Honest. More likely than not
   to be a niche-but-real technique, but K7 could reduce it to 'just use Kahan.'"
   The confidence level was appropriate. The investigation was warranted. A 45%
   probability means the outcome was within expected range.

### What Round 1 Got Wrong

**The central premise was false.**

Round 1 stated: "Each step has a subtraction. If any intermediate s_k is near
pi/2, the subtraction is catastrophic, AND the error propagates forward through
all subsequent steps."

This is wrong in two places:

1. **"The subtraction is catastrophic"** -- technically true in terms of RELATIVE
   error (|delta|/|cos(s_k)| is large when cos(s_k) ~ 0), but misleading. The
   ABSOLUTE error |delta| = |cos(s_k)| * u is TINY when cos(s_k) ~ 0. Calling
   it "catastrophic" conflates relative and absolute error.

2. **"The error propagates forward"** -- FALSE. The rotation matrix R(theta) is
   orthogonal: ||R||_2 = 1. Error norms are preserved. A large relative error at
   step k produces a SMALL absolute error that propagates with constant norm
   through all subsequent steps. There is no cascading.

This is a textbook error in numerical analysis: **confusing local condition
numbers with global stability.** The local condition number of the subtraction
cos(a)cos(b) - sin(a)sin(b) diverges at resonance. But the stability of the
iteration depends on the spectral radius of the propagation matrix, which is 1
for rotation (stable) and e^theta for DPQA (unstable).

I made the error because I reasoned about the OPERATION (subtraction has
cancellation) instead of the ITERATION (rotation preserves norms). The operation
was the wrong unit of analysis. The iteration was the right one.

**The homogeneous coordinates analogy broke where it mattered.**

Round 1 scored this analogy at 75% and noted: "Both carry extra dimension to
avoid singularity at projection." The break point was identified as "not a
quotient space." But the CRITICAL break was missed:

- Homogeneous coordinates: ALL components remain bounded. The extra w coordinate
  doesn't grow without bound. Projection (x/w, y/w) is a ratio of bounded
  quantities.
- Quaternary representation: The extra components grow EXPONENTIALLY. u and v
  contain cosh(t)/2, which grows as e^t. Projection (u-v) subtracts two
  exponentially large quantities to recover a bounded result.

The analogy should have scored lower (perhaps 50%) once the boundedness
mismatch was identified. The "quotient space" break point was real but wasn't
the lethal one.

**The predicted advantage was exactly backwards.**

Round 1 predicted: "The advantage should scale with k" (number of resonance
crossings). Reality: the DISADVANTAGE scales exponentially with total angle.
More operations make DPQA worse, not better. The prediction was not merely
quantitatively off -- it pointed in the wrong direction.

**The FLOP analysis was irrelevant.**

Round 1 spent considerable effort on FLOP comparisons (28 vs 12 vs 42). This
was methodologically sound but practically irrelevant, because DPQA has worse
conditioning than ALL alternatives. A cheaper method that gives worse answers
is not an advantage. The FLOP analysis should have been contingent on the
conditioning analysis, not presented as an independent factor.

### Root Cause Analysis

The failure was a **LEVEL 2 error** (in the Causality Loop framework):
analyzing the symptom (subtraction causes cancellation) instead of the
mechanism (how does the error propagate through the chain?).

The seven-step methodology was followed correctly IN FORM:
- Step 1 (Assume solved): done
- Step 2 (Necessary structure): N1-N5 were genuine necessary conditions
- Step 3 (Inventory): thorough
- Step 4 (Gap): correctly identified
- Step 5 (Bridge design): elegant but wrong
- Step 6 (Kill conditions): K1-K8 were well-chosen
- Step 7 (Build forward): deferred to later rounds (correct)

But **Step 2 contained an unverified assumption**: that resonance crossings
cause cascading error. This assumption was stated as if it were self-evident
("catastrophic cancellation" is a well-known phenomenon). It was not verified
against the SPECIFIC context of iterated rotations.

The lesson: **necessary conditions must be VERIFIED, not assumed, even when
they sound like standard numerical analysis wisdom.** "Subtraction of nearly
equal quantities causes cancellation" is TRUE in isolation. "Cancellation in
one step of an iterative process causes error growth" is a SEPARATE claim that
requires its own verification.

---

## Part II: The State of Knowledge

### What Is Now Established

**Theorem (Round 3, empirically confirmed Round 4).** For a chain of n
rotation steps with angle theta each:

| Method | Absolute error | Spectral radius | FLOPs/step |
|--------|---------------|-----------------|------------|
| Standard rotation | O(n * u) | 1 | 12 |
| DPQA cyclic conv | O(n * u * e^{n*theta}) | e^theta | 28 |
| Compensated rotation | O(n * u^2) | 1 | 12-42 |

The standard rotation chain is near-optimal among bounded representations.
Compensated rotation improves precision by a factor of u ~ 10^{-16}.
DPQA degrades precision by a factor of e^{n*theta} -- exponential in the
total angle.

**Corollary.** No representation that includes the exponential e^t as a
component can provide better conditioning than the standard (cos, sin)
representation for computing cos(s_n) through chained angle addition.

**Corollary.** The only path to improved conditioning for chained angle
addition is PRECISION EXTENSION (compensated arithmetic, double-double,
arbitrary precision), not REPRESENTATION CHANGE. The (cos, sin) representation
is already optimal among bounded representations.

### What the Quaternary Framework IS Good For

Three genuine (if modest) contributions survive:

1. **Interpretive framework.** The gross/net decomposition
   (cosh = u+v, cos = u-v) reveals the energy structure of oscillatory
   systems. The ratio cosh(t)/|cos(t)| is a natural conditioning indicator.
   This is INSIGHT, not COMPUTATION. It tells you WHY a computation is
   ill-conditioned; it doesn't fix the computation.

2. **Stride-4 Taylor recurrence.** Computing all four functions
   (cos, sin, cosh, sinh) simultaneously via mod-4 subseries saves ~40% of
   Taylor FLOPs. This is a real but niche optimization, applicable only to
   custom Taylor implementations (not to compiled library calls). Confirmed
   in the prior quaternary-performance council.

3. **Algebraic novelty.** The use of Z4 cyclic convolution as a
   cancellation-free argument addition formula appears to be unpublished.
   It is correct algebra. It is not useful numerics, but it is a clean
   mathematical fact that could appear in a survey paper or textbook section
   on the group algebra structure of exponential subseries.

### What Is Dead

- DPQA as a computational technique for improving numerical conditioning
- The "chained operation advantage" hypothesis
- The "resonance crossings cause cascading error" premise
- Any claim of >2x conditioning improvement in any scenario
- The neural network activation domain (debunked in prior council)
- The N-Phase pipeline domain (no computational advantage)

---

## Part III: Kill Condition Final Assessment

| ID | Kill Condition | Status | Round Fired | Evidence |
|----|---------------|--------|-------------|----------|
| K1 | No lifted computation exists | CLEAR | -- | Operations are algebraically closed |
| **K2** | **Advantage <2x in ALL scenarios** | **FIRES** | 4 | DPQA is WORSE, not better, everywhere |
| K3 | Known published technique | CLEAR | -- | Novel technique confirmed |
| **K4** | **Mathematical impossibility (conditioning)** | **FIRES** | 3 | Spectral radius e^theta > 1; exponential error growth |
| **K5** | **FLOP overhead not amortized** | **FIRES** | 3 | No conditioning advantage to amortize |
| K6 | No real algorithm chains enough ops | MOOT | -- | No advantage at any chain length |
| K7 | Compensated arithmetic cheaper | SUPERSEDED | 4 | Compensated is better in every metric |
| **K8** | **Overflow** | **FIRES** | 3 | cosh overflows float64 for |t| > 710 |

Three kill conditions fire independently (K4, K5, K8). K2 fires as
confirmation. K7 is superseded (compensated is better, but so is doing
nothing -- standard rotation is already excellent). K6 is moot.

The continue condition was: "ANY test shows >2x conditioning improvement
for a realistic computation." Zero of eight tests showed any improvement.
Five showed degradation. Three were irrelevant.

---

## Part IV: Structural Fusion -- Final Verdicts

The Round 1 analogies can now be sharpened with hindsight:

| Parallel System | R1 Score | Revised Score | What Changed |
|----------------|----------|---------------|-------------|
| Homogeneous coordinates | 75% | 50% | CRITICAL: homogeneous coords stay bounded; quaternary grows exponentially. The boundedness mismatch is the lethal break, not the quotient-space issue. |
| expm1/log1p | 70% | 65% | Confirmed as closest in spirit. Both defer a lossy operation. Break: expm1 defers subtraction of O(1) quantities; DPQA defers subtraction of O(e^t) quantities. The scale of what's deferred matters. |
| Lie group integrators | 70% | 60% | Both "stay lifted, project late." Break: quaternions stay on a compact manifold (S^3); quaternary representation leaves the compact domain (includes e^t). Compactness is the key property that makes Lie group integrators work. |
| Compensated Clenshaw | 70% | 70% | Unchanged. Same problem domain, different solution. Compensated Clenshaw's approach (track the error) turns out to be superior to DPQA's approach (change the representation). |
| Haversine | 75% | 70% | Confirmed as strongest analogy. Both avoid specific subtractions. Break: haversine replaces ONE subtraction with an algebraically equivalent form; DPQA defers ALL subtractions but introduces exponential growth. Haversine works because it doesn't carry unbounded quantities. |

**The unifying lesson**: Every successful "stay lifted" technique maintains
BOUNDED intermediate values. Homogeneous coordinates: bounded ratios.
Lie group integrators: compact manifold (unit quaternions). Haversine:
sin^2(theta/2) in [0,1]. The quaternary representation violates this principle
by carrying cosh(t), which grows without bound. The boundedness requirement is
the necessary condition that Round 1 missed.

---

## Part V: What This Investigation Produced

### For the Project

1. **A clean negative result.** The question "does staying lifted help?" is
   now answered: NO, with full mathematical proof and empirical confirmation.
   This closes the investigation permanently. No future council needs to
   revisit it.

2. **A deeper understanding of WHY the standard rotation works.** The
   orthogonality of the rotation matrix is not just an algebraic convenience --
   it is the mechanism that makes chained angle computation stable.
   This insight (spectral radius = 1 for rotations) is more valuable than
   the DPQA proposal.

3. **A calibrated understanding of the quaternary framework's scope.**
   The framework provides: Z4 algebra (known), interpretive insight into
   gross/net energy (real but modest), stride-4 Taylor optimization (niche).
   It does not provide: numerical conditioning improvement, computational
   advantage for chained operations, any benefit for staying lifted.

### For the Methodology

4. **A case study in teleological reasoning failure modes.** The seven-step
   method worked correctly in form but failed at Step 2 because a necessary
   condition was ASSUMED rather than VERIFIED. The lesson: when Step 2 says
   "the solution must have property P," verify P independently before
   proceeding to Step 5 (bridge design).

5. **A case study in the Wilson Principle.** The prior two councils said STOP.
   This council asked a different question and got the same answer. The
   persistence was warranted (the question was genuinely different), but the
   answer converges: the quaternary framework's value is interpretive, not
   computational.

6. **A kill condition design success.** K4 (mathematical impossibility for
   conditioning) was pre-registered and fired cleanly. K7 (compensated
   arithmetic) was identified as the most threatening and correctly drove
   the empirical testing. The kill condition framework worked as designed.

---

## Part VI: Verdict and Recommendation

### (a) Does the evidence support, refute, or modify the Round 1 vision?

**REFUTES.** The core prediction (conditioning advantage for chained
operations near resonance) is not merely unconfirmed -- it is proved false.
The mechanism is the opposite of what was predicted: DPQA makes chained
operations exponentially WORSE, not better. The secondary predictions
(resonance detection advantage, energy computation advantage, neural network
gradient advantage) are all refuted.

The vision's structural analysis (operation closure, novelty, structural
parallels) holds. The vision's numerical predictions are all wrong.

### (b) What is the precise current state of knowledge?

The quaternary decomposition of e^t into mod-4 subseries is:
- **Algebraically**: A real Z4 group algebra with cyclic convolution for
  argument addition. Correct, complete, novel as a numerical proposal.
- **Numerically**: Inferior to standard rotation for chained computation
  by a factor of e^{total_angle}. Provably so. No rescue by rescaling,
  compensation, or other modification is possible while preserving the
  algebraic structure.
- **Interpretively**: Provides genuine insight into the gross/net energy
  structure of oscillatory systems. The conditioning diagnostic
  cosh(t)/|cos(t)| has real value for understanding numerical pathology,
  even though it cannot fix it.

### (c) What concrete next steps exist?

None for DPQA. The investigation is complete.

For the broader project:
- The stride-4 Taylor recurrence (40% FLOP savings) could be benchmarked
  against modern hardware (SIMD, FMA) to see if the niche advantage
  persists. This is a MINOR investigation, not worth a council.
- The interpretive framework (gross/net energy) is already used in the
  N-Phase patent work. No additional investigation needed.
- The algebraic novelty (Z4 convolution for argument addition) could be
  noted in a paper about Dollard's framework, as an example of correct
  but numerically unhelpful algebra. One paragraph, not a paper.

### (d) Should this line of investigation continue, pivot, or stop?

**STOP.**

Three independent kill conditions have fired. The mathematical proof is
complete and confirmed empirically. There is no pivot that preserves the
core idea (staying lifted) while avoiding the core problem (exponential
error growth). The exponential growth is inherent to any representation
that includes e^t, and the quaternary representation necessarily includes
e^t because e^t = u + x + v + y.

The ONLY way to avoid the exponential growth is to work in the bounded
subspace -- which is exactly the standard (cos, sin) representation.
DPQA's bridge back to the bounded world IS the standard rotation.
This is not a pivot opportunity. This is the end of the road.

---

## Part VII: Confidence Calibration (Final)

| Component | R1 Confidence | Final Confidence | What Changed |
|-----------|--------------|-----------------|-------------|
| Operation closure | 95% | **99%** | Confirmed algebraically, formally, and empirically |
| Novelty | 85% | **95%** | Comprehensive 10-direction literature search found no match |
| Structural parallels correct | 85% | **90%** | Confirmed, with homogeneous coords revised downward |
| At least one domain benefits | 60% | **<1%** | No domain benefits. Mathematical impossibility proven. |
| DPQA beats compensated | 40% | **<1%** | DPQA is exponentially worse than standard, let alone compensated |
| Chain-length advantage practical | 50% | **0%** | Chain length makes DPQA worse, not better |
| **Overall engineering value** | **45%** | **<5%** | Value is purely interpretive, not computational |

The 45% → <5% collapse is the signature of a clean negative result. The
investigation was warranted at 45%. The answer is clear at <5%. The
remaining ~5% accounts for the interpretive value, not any computational
claim.

---

## Closing: The Honest Scale

DPQA is: **a correct algebraic observation with no numerical utility.**

It is comparable in status to the observation that you can compute pi by
throwing needles at a floor (Buffon's needle): mathematically valid,
pedagogically interesting, computationally absurd. The Z4 cyclic convolution
for angle addition is pretty algebra. The standard rotation matrix is
better numerics. Beauty does not imply utility.

The investigation consumed five rounds and produced a definitive answer.
That answer is NO. The process worked: kill conditions were pre-registered,
the cheapest tests were run first (rigor before computation), and the
result was accepted when it arrived.

This is what a successful negative result looks like. The question was worth
asking. The answer was worth finding. The answer is no.

---

**INVESTIGATION STATUS: CLOSED**
**VERDICT: STOP**
**RESULT: CLEAN NEGATIVE -- DPQA provides no computational advantage**
