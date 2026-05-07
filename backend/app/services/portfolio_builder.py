from __future__ import annotations

from itertools import combinations

from app.models.betting import PortfolioBuildInput, PortfolioResponse, Ticket


def _valid_combo(picks):
    weights = [p.weight for p in picks]
    athletes = [p.athlete for p in picks]
    return len(weights) == len(set(weights)) and len(athletes) == len(set(athletes))


def build_portfolio(data: PortfolioBuildInput) -> PortfolioResponse:
    profile_ratio = {"conservadora": [0.7, 0.25, 0.05], "media": [0.5, 0.35, 0.15], "agresiva": [0.3, 0.45, 0.25]}
    r = profile_ratio.get(data.profile, profile_ratio["media"])
    tickets = []
    warnings = []

    ordered = sorted(data.picks, key=lambda p: p.edge, reverse=True)
    singles = ordered[: min(6, len(ordered))]
    if singles:
        per = (data.stake_total * r[0]) / len(singles)
        for p in singles:
            tickets.append(Ticket(type="single", picks=[p], total_odds=p.odds, stake=per, potential_return=per * p.odds))

    combo2 = [c for c in combinations(ordered[:8], 2) if _valid_combo(c)]
    if combo2:
        per = (data.stake_total * r[1]) / min(4, len(combo2))
        for c in combo2[:4]:
            odds = c[0].odds * c[1].odds
            tickets.append(Ticket(type="combo_2", picks=list(c), total_odds=odds, stake=per, potential_return=per * odds))

    combo34 = [c for n in (3, 4) for c in combinations(ordered[:10], n) if _valid_combo(c)]
    if combo34:
        c = combo34[0]
        stake = data.stake_total * r[2]
        odds = 1.0
        for p in c:
            odds *= p.odds
        tickets.append(Ticket(type=f"combo_{len(c)}", picks=list(c), total_odds=odds, stake=stake, potential_return=stake * odds))

    exp_a, exp_w = {}, {}
    for t in tickets:
        for p in t.picks:
            exp_a[p.athlete] = exp_a.get(p.athlete, 0) + t.stake / data.stake_total
            exp_w[p.weight] = exp_w.get(p.weight, 0) + t.stake / data.stake_total

    for athlete, ex in exp_a.items():
        if ex > data.max_exposure_per_judoka:
            warnings.append(f"Exposicion alta por judoka: {athlete} ({ex:.2f})")
    for weight, ex in exp_w.items():
        if ex > data.max_exposure_per_weight:
            warnings.append(f"Exposicion alta por peso: {weight} ({ex:.2f})")

    return PortfolioResponse(tickets=tickets, exposure_by_judoka=exp_a, exposure_by_weight=exp_w, warnings=warnings)
