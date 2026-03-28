# Task Environment

## 1. Rational objective
Simulate deceptive health signals where executive dashboards remain green while operational indicators trend toward failure.

## 2. PEAS
- Performance: reproducible scenarios, clear false-green narrative, actionable monitoring recommendations.
- Environment: synthetic time-series scenarios.
- Actuators: interactive charts and narrative diagnostics.
- Sensors: scenario selection, intensity, seed, time window.

## 3. Environmental dimensions
Partially observable, dynamic, stochastic-but-seeded, safety-critical interpretation.

## 4. Problem formalization
Generate deterministic time-series for executive and truth signal sets; detect divergence and explain risk.

## 5. Architecture choice
Scenario generator + diagnostics module + Streamlit UI for fast simulator iteration.

## 6. Guardrails / workflow maturity
No production automation, no external integrations, deterministic seeds for inspectability.
