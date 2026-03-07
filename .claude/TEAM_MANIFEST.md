# Team Manifest

Domain keywords: `formal-verification`, `mathematical-logic`, `algebraic-systems`,
`signal-processing`, `power-systems`, `geometric-algebra`, `lean4`

## Agents

| Agent | Tier | Role | QA Status |
|-------|------|------|-----------|
| dollard-theorist | opus | Verify math against source materials | INSTALLED. Paths reference N-Phase (`01_Source_Materials/`); reads project CLAUDE.md for local paths. Math content accurate. |
| experiment-designer | opus | Design experiments with falsification | INSTALLED. Methodology universal. REAL/PROPERTY/SMOKE classification applies directly. |
| power-systems-expert | opus | Validate Fortescue/polyphase claims | INSTALLED. EE domain knowledge universal. Fortescue validation directly relevant. |
| polymathic-researcher | opus | Deep cross-domain investigation | INSTALLED. Generic, project-aware. Creates notebooks in project `research/`. |
| droid-code-engineer | sonnet | General code implementation | INSTALLED. No Lean 4 knowledge -- pair with lean4-theorem-proving skill. |

### Agent Path Note

dollard-theorist, experiment-designer, and power-systems-expert were built for
the N-Phase project. Their internal path references (`01_Source_Materials/`,
`src/versor_algebra/`, etc.) point to N-Phase, not this project. This is expected:

- Agents read the project's CLAUDE.md on invocation for local context
- This project's CLAUDE.md documents local paths (`source_materials/`, `src/lean_proofs/`)
- The agents' domain knowledge (math, EE, experiment design) is universal

No agent modifications needed. The CLAUDE.md provides the bridge.

## Skills

| Skill | Role | QA Status |
|-------|------|-----------|
| lean4-theorem-proving | Lean 4 tactics, proof patterns, project setup | NEW. Created for this project. |
| dollard-versor-operators | Reference for h,j,k math | INSTALLED. Math content accurate. Contains inflated framing ("never been applied") -- ignore framing, use math. |
| fortescue-symmetrical-components | Standard EE reference | INSTALLED. Math content accurate. Same inflated framing caveat. |
| clifford-algebra-reference | Alternative algebraic frameworks | INSTALLED. Clean. Relevant to Experiment 1 (alternative h interpretations). |
| historical-electromagnetism | Heaviside/Steinmetz context | INSTALLED. Clean. Provides Track A historical grounding. |
| experimental-design-methodology | Experiment protocol design | INSTALLED. Clean. Universal methodology. |
| cognitive-protocols | Rigorous thinking methodology | INSTALLED. Clean. |
| polymathic-researcher | Deep research methodology | INSTALLED. Drives the polymathic pipeline. |

## Deployment Patterns

- **Track A (methodology)**: polymathic-researcher + cognitive-protocols
- **Track B (math analysis)**: dollard-theorist + lean4-theorem-proving + fortescue-symmetrical-components
- **Track C (physics claims)**: polymathic-researcher (literature search only)
- **Experiments**: experiment-designer (design) -> droid-code-engineer (implement)
- **Lean proofs**: droid-code-engineer + lean4-theorem-proving skill
- **Polyphase validation**: power-systems-expert + fortescue-symmetrical-components
