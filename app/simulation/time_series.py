from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SeriesBundle:
    time_index: List[int]
    executive_metrics: Dict[str, List[float]]
    truth_metrics: Dict[str, List[float]]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))
