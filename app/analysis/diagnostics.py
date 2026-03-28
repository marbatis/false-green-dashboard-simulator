from __future__ import annotations

from typing import Dict, List, Union

from app.simulation.scenario_factory import ScenarioConfig
from app.simulation.time_series import SeriesBundle


def diagnose(config: ScenarioConfig, bundle: SeriesBundle) -> Dict[str, Union[str, List[str]]]:
    scenario = config.scenario

    if scenario == "cert_rotation_hidden_failure":
        danger = (
            "Dashboard success rate stays green while token failures and certificate errors trend up, "
            "creating delayed authentication outage risk."
        )
        signals = [
            "Track token verification failures per minute",
            "Alert on cert_error_rate trend, not only absolute threshold",
            "Monitor p99 auth latency and handshake failures",
        ]
    elif scenario == "retry_storm_masked_by_averages":
        danger = (
            "Top-line availability appears healthy, but retries and queue depth compound load until the "
            "system crosses a sudden failure cliff."
        )
        signals = [
            "Track retry_rate and retry amplification ratio",
            "Alert on queue_depth slope, not static values only",
            "Monitor saturation and p99 latency together",
        ]
    else:
        danger = (
            "Throughput and success can stay green while downstream 5xx and queue depth rise, masking "
            "dependency saturation and looming collapse."
        )
        signals = [
            "Track downstream_5xx and dependency timeout ratio",
            "Track queue_depth growth per minute",
            "Create saturation alerts using p95/p99 divergence",
        ]

    return {
        "false_green_explanation": danger,
        "recommended_signals": signals,
    }
