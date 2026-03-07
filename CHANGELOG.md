# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-03-07

### Added
- Project scaffold with honest reframing (ADR-001)
- Preserved Lean proofs: basic_operators.lean, telegraph_equation.lean
- Preserved source materials (Dollard PDFs + extracted text)
- Preserved claim inventory (MATHEMATICAL_CLAIMS_EXTRACTION.md)
- New claim triage with honest verdicts (CLAIM_TRIAGE.md)
- Rewritten verification results with accurate tone
- Audit findings document
- Experiment registry with pre-registered experiments
- Hook guardrails (protect-results, run-tests-on-src-change)
- Team manifest and experiment-workflow skill

### Changed
- Reframed project from "UFT validation" to "formal verification methodology"
- Moved source materials from Source_Materials/ to source_materials/
- Moved lean proofs under src/lean_proofs/

### Removed
- Core_Theoretical_Framework/ (advocacy, not analysis)
- Academic_Paper/ (not viable as written)
- Experimental_Predictions/ (physics claims without evidence)
- ANALYSIS_STATUS_README.md (infrastructure cheerleading)
- All inflated language documentation
