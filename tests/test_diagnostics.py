from __future__ import annotations

from app.analysis.diagnostics import diagnose
from app.simulation.scenario_factory import ScenarioConfig, ScenarioFactory


def test_diagnostics_output_shape() -> None:
    cfg = ScenarioConfig("cert_rotation_hidden_failure", intensity=0.6, points=16, seed=77)
    bundle = ScenarioFactory().generate(cfg)
    result = diagnose(cfg, bundle)
    assert "false_green_explanation" in result
    assert "recommended_signals" in result
    assert len(result["recommended_signals"]) >= 3
