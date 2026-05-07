from app.models.athlete import AthleteStrength
from app.services.strength_service import calculate_strength_score, predict_match_probability


def test_manual_rating_high_beats_default_score():
    high = AthleteStrength(name="A", normalized_name="A", manual_rating=90)
    default = AthleteStrength(name="B", normalized_name="B")
    assert calculate_strength_score(high) > calculate_strength_score(default)


def test_low_world_rank_better_than_high_world_rank():
    elite = AthleteStrength(name="A", normalized_name="A", world_rank=5)
    weak = AthleteStrength(name="B", normalized_name="B", world_rank=60)
    assert calculate_strength_score(elite) > calculate_strength_score(weak)


def test_predict_probability_bounded():
    p = predict_match_probability(300, 1)
    assert 0.05 <= p <= 0.95
