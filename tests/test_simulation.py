from __future__ import annotations

from app.simulation.scenario_factory import ScenarioConfig, ScenarioFactory


def test_generation_is_deterministic_for_seed() -> None:
    cfg = ScenarioConfig("retry_storm_masked_by_averages", intensity=0.7, points=20, seed=123)
    bundle_a = ScenarioFactory().generate(cfg)
    bundle_b = ScenarioFactory().generate(cfg)
    assert bundle_a.executive_metrics == bundle_b.executive_metrics
    assert bundle_a.truth_metrics == bundle_b.truth_metrics


def test_retry_storm_relationships_hold() -> None:
    cfg = ScenarioConfig("retry_storm_masked_by_averages", intensity=0.9, points=18, seed=5)
    bundle = ScenarioFactory().generate(cfg)
    retries = bundle.truth_metrics["retry_rate"]
    queue = bundle.truth_metrics["queue_depth"]
    assert retries[-1] > retries[0]
    assert queue[-1] > queue[0]


def test_exec_dashboard_appears_green() -> None:
    cfg = ScenarioConfig("downstream_queue_saturation", intensity=0.8, points=20, seed=9)
    bundle = ScenarioFactory().generate(cfg)
    success = bundle.executive_metrics["success_rate"]
    assert min(success) > 97.5
