from __future__ import annotations

import math

from app.models.athlete import AthleteStrength


def calculate_strength_score(strength: AthleteStrength) -> float:
    rank_score = max(0.0, 100.0 - strength.world_rank) if strength.world_rank is not None else 0.0
    points_score = math.log(1 + strength.ranking_points) if strength.ranking_points is not None else 0.0
    recent_form = strength.recent_wins * 3 - strength.recent_losses * 2
    h2h_bonus = strength.h2h_wins * 4 - strength.h2h_losses * 4

    base = strength.manual_rating if strength.manual_rating is not None else 50.0
    final_score = base + rank_score + points_score + recent_form + h2h_bonus
    return max(1.0, final_score)


def predict_match_probability(score_a: float, score_b: float) -> float:
    prob_a = 1 / (1 + 10 ** ((score_b - score_a) / 40))
    return min(0.95, max(0.05, prob_a))
