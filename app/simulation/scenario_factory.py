from __future__ import annotations

import random
from dataclasses import dataclass

from app.simulation.time_series import SeriesBundle, clamp

SCENARIOS = {
    "cert_rotation_hidden_failure",
    "retry_storm_masked_by_averages",
    "downstream_queue_saturation",
}


@dataclass
class ScenarioConfig:
    scenario: str
    intensity: float
    points: int
    seed: int


class ScenarioFactory:
    def generate(self, config: ScenarioConfig) -> SeriesBundle:
        if config.scenario not in SCENARIOS:
            raise ValueError(f"Unsupported scenario: {config.scenario}")
        rng = random.Random(config.seed)
        t = list(range(config.points))

        if config.scenario == "cert_rotation_hidden_failure":
            return self._cert_hidden_failure(config, rng, t)
        if config.scenario == "retry_storm_masked_by_averages":
            return self._retry_storm(config, rng, t)
        return self._downstream_saturation(config, rng, t)

    def _cert_hidden_failure(self, cfg: ScenarioConfig, rng: random.Random, t: list[int]) -> SeriesBundle:
        intensity = clamp(cfg.intensity, 0.2, 1.0)
        success = [clamp(99.7 - 0.1 * rng.random(), 98.8, 100.0) for _ in t]
        throughput = [clamp(500 + rng.randint(-15, 15), 420, 560) for _ in t]

        p95 = [120 + 10 * i * intensity + rng.randint(0, 30) for i in t]
        p99 = [200 + 18 * i * intensity + rng.randint(0, 50) for i in t]
        token_failures = [int(2 + i * 1.8 * intensity + rng.random() * 4) for i in t]
        cert_error_rate = [round(clamp(0.01 + 0.004 * i * intensity, 0.0, 0.6), 3) for i in t]

        return SeriesBundle(
            time_index=t,
            executive_metrics={"success_rate": success, "throughput_rps": throughput},
            truth_metrics={
                "p95_latency_ms": p95,
                "p99_latency_ms": p99,
                "token_failures": token_failures,
                "cert_error_rate": cert_error_rate,
            },
        )

    def _retry_storm(self, cfg: ScenarioConfig, rng: random.Random, t: list[int]) -> SeriesBundle:
        intensity = clamp(cfg.intensity, 0.2, 1.0)
        success = [clamp(99.5 - 0.15 * rng.random(), 98.0, 100.0) for _ in t]
        throughput = [clamp(620 + rng.randint(-20, 20), 500, 700) for _ in t]

        retries = [int(20 + i * 10 * intensity + rng.random() * 15) for i in t]
        queue_depth = [int(100 + i * 35 * intensity + rng.random() * 30) for i in t]
        p99 = [250 + i * 28 * intensity + rng.randint(0, 60) for i in t]
        saturation = [round(clamp(0.3 + 0.03 * i * intensity, 0.0, 1.0), 3) for i in t]

        return SeriesBundle(
            time_index=t,
            executive_metrics={"success_rate": success, "throughput_rps": throughput},
            truth_metrics={
                "retry_rate": retries,
                "queue_depth": queue_depth,
                "p99_latency_ms": p99,
                "saturation": saturation,
            },
        )

    def _downstream_saturation(self, cfg: ScenarioConfig, rng: random.Random, t: list[int]) -> SeriesBundle:
        intensity = clamp(cfg.intensity, 0.2, 1.0)
        success = [clamp(99.3 - 0.2 * rng.random(), 97.8, 100.0) for _ in t]
        throughput = [clamp(570 + rng.randint(-18, 18), 460, 640) for _ in t]

        downstream_5xx = [round(clamp(0.01 + 0.005 * i * intensity, 0.0, 0.7), 3) for i in t]
        queue_depth = [int(80 + i * 40 * intensity + rng.random() * 35) for i in t]
        p95 = [170 + i * 20 * intensity + rng.randint(0, 40) for i in t]
        p99 = [280 + i * 30 * intensity + rng.randint(0, 70) for i in t]

        return SeriesBundle(
            time_index=t,
            executive_metrics={"success_rate": success, "throughput_rps": throughput},
            truth_metrics={
                "downstream_5xx": downstream_5xx,
                "queue_depth": queue_depth,
                "p95_latency_ms": p95,
                "p99_latency_ms": p99,
            },
        )
