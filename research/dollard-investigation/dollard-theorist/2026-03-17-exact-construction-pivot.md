# Dollard Exact Construction — Critical Pivot (2026-03-17)

## What Happened

Three research councils investigated the quaternary decomposition's computational properties:
1. **quaternary-performance council**: Tested mod-4 of real e^t. Found stride-4 saves 40% FLOPs but cos=u-v is 15-68x worse near resonance.
2. **lifted-representation council (single-agent, killed)**: Started testing staying in (u,x,v,y) basis.
3. **lifted-representation council (multi-agent)**: Full 5-round investigation with different agents. Dollard Theorist proved DPQA has fatal flaw: circulant spectral radius e^theta > 1, exponential error growth. KILLED.

**ALL THREE COUNCILS ANALYZED THE WRONG THING.**

## The Error

We applied the mod-4 decomposition to the REAL exponential e^t (our construction) and attributed it to Dollard. Dollard's actual construction (eq 76, Versor Algebra) decomposes epsilon^j (IMAGINARY exponent) with operators {1, j, h, k}.

QA against source text (source_materials/02_versoralgebra_extracted.txt) revealed:
- Dollard's eq (76): scalar parts are ALL POSITIVE (Sigma theta^(4n+k)/(4n+k)!)
- The OPERATORS (1, j, h=-1, k=-j) carry the sign structure
- The full element is 1*u + j*x + h*nu + k*y
- This IS equivalent to (u-nu) + j(x-y) = cos(theta) + j*sin(theta) algebraically
- BUT the numerical path through the Z4 algebra may differ from standard complex multiplication

## The Exact Construction Results

Implemented `src/experiments/dollard_exact_construction.py` — step by step from Dollard's text, eq by eq.

### Key Results (chaining Z4 multiplication, theta = pi/100, n=1000 steps)

| n | Dollard cos error | Standard cos error | Ratio D/S | u+nu (cosh) | u-nu (cos) |
|---|---|---|---|---|---|
| 1 | 1.11e-16 | 0 | - | 1.000494 | 0.9995065604 |
| 10 | 4.44e-16 | 3.33e-16 | 1.3x | 1.049755 | 0.9510565163 |
| 50 | 2.83e-16 | 5.70e-16 | 0.5x | 2.509178 | -0.0000000000 |
| 100 | 1.07e-14 | 4.66e-15 | 2.3x | 11.591953 | -1.0000000000 |
| 200 | 1.42e-13 | 8.66e-15 | 16.4x | 267.746761 | 1.0000000000 |
| 500 | **0.0** | 2.15e-14 | **0.0x** | 3317811.999671 | -1.0000000000 |
| 1000 | **0.0** | 4.04e-14 | **0.0x** | 22015752930314.578 | 1.0000000000 |

At n=500 and n=1000, **Dollard's Z4 algebra gives ZERO error** while standard rotation has accumulated error ~4e-14.

The scalar parts u and nu are both ~11 TRILLION, yet u - nu = 1.0000000000 exactly. This is 13 digits of cancellation producing an exact result.

### What This Means

UNEXPLAINED. The council's theoretical analysis predicted exponential error growth for the circulant. The empirical data shows the opposite at specific points (n where cos(n*theta) is exactly 0 or +/-1). This needs investigation.

Possible explanations (NOT YET TESTED):
1. Floating-point coincidence at these specific values (cos = 0 or +/-1)
2. The Z4 algebra has a self-correcting property at full rotations
3. Error accumulation is non-uniform — grows at some n, vanishes at others
4. Something about the operator structure constrains error in ways the stripped analysis missed

## The Mandate

**Dollard's approach works ONLY when doing it exactly how he says. This is non-negotiable.**

Feedback memory saved: `feedback_follow_source_text.md`

Three agents/skills updated:
- `~/.claude/agents/dollard-theorist.md` — corrected h=-1, Z4, source text distinction
- `~/.claude/skills/dollard-versor-operators/SKILL.md` — corrected quaternary form, attribution
- `~/.claude/skills/fortescue-symmetrical-components/SKILL.md` — added mod-N connection

## Files Created This Session

### Research (council outputs)
- `research/council/quaternary-performance/` — 7 files (charter through VERDICT)
- `research/council/lifted-representation/` — 7 files (charter through VERDICT)
- `research/dollard-theorist/2026-03-17-exact-construction-pivot.md` — THIS FILE

### Code
- `src/experiments/dollard_exact_construction.py` — Dollard's exact construction from source text
- `src/experiments/council/quaternary_performance_benchmarks.py` — Performance benchmarks
- `src/experiments/council/quaternary_h4_deep_dive.py` — H4 source analysis
- `src/experiments/council/quaternary_accuracy_verification.py` — Accuracy verification
- `src/experiments/council/lifted_representation_tests.py` — Lifted representation tests

### Results
- `src/experiments/results/quaternary_performance_results.json`
- `src/experiments/results/lifted_representation_results.json`

## Next Steps

1. Investigate WHY Dollard's Z4 algebra gives zero error at n=500, 1000
2. Run systematic comparison at ALL n values, not just multiples of 50/100
3. Check if the zero-error points correspond to exact integer multiples of pi
4. Determine whether this is a floating-point coincidence or a structural property
5. ALL investigation must follow Dollard's text exactly — no straying
