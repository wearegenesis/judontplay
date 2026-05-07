from app.models.betting import PortfolioBuildInput
from app.models.judo import PickRecommendation
from app.services.portfolio_builder import build_portfolio


def test_ticket_rules_no_same_weight_inside_combo():
    picks = [
        PickRecommendation(market="winner", athlete="A", weight="-60 kg", fair_probability=0.5, implied_probability=0.4, edge=0.1, odds=2.5),
        PickRecommendation(market="winner", athlete="B", weight="-60 kg", fair_probability=0.45, implied_probability=0.3, edge=0.15, odds=3.0),
        PickRecommendation(market="winner", athlete="C", weight="-66 kg", fair_probability=0.3, implied_probability=0.2, edge=0.1, odds=4.0),
    ]
    result = build_portfolio(PortfolioBuildInput(picks=picks, stake_total=100))
    for t in result.tickets:
        if t.type.startswith("combo"):
            weights = [p.weight for p in t.picks]
            assert len(weights) == len(set(weights))
