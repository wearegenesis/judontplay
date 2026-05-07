from __future__ import annotations

from app.models.judo import PickRecommendation


def detect_value(probabilities: dict[str, float], odds: dict[str, float], market: str, weight: str) -> list[PickRecommendation]:
    recs: list[PickRecommendation] = []
    for athlete, odd in odds.items():
        fair = probabilities.get(athlete, 0.0)
        implied = 1 / odd if odd > 0 else 0
        edge = fair - implied
        if edge > 0:
            recs.append(
                PickRecommendation(
                    market=market,
                    athlete=athlete,
                    weight=weight,
                    fair_probability=fair,
                    implied_probability=implied,
                    edge=edge,
                    odds=odd,
                )
            )
    return sorted(recs, key=lambda r: r.edge, reverse=True)
