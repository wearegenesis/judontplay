from __future__ import annotations

from fastapi import FastAPI

from app.models.athlete import AthleteStrength
from app.models.betting import PortfolioBuildInput
from app.models.judo import AnalyzeResponse, BracketInput, TournamentAnalyzeInput, TournamentAnalyzeResponse
from app.services.bracket_parser import parse_bracket
from app.services.judobase_service import JudobaseService
from app.services.normalization import normalize_name, normalize_weight
from app.services.portfolio_builder import build_portfolio
from app.services.simulation_engine import simulate_bracket_monte_carlo
from app.services.strength_service import calculate_strength_score
from app.services.value_engine import detect_value

app = FastAPI(title="Judo Value Analysis API")
service = JudobaseService()


def analyze_single_bracket(payload: BracketInput) -> AnalyzeResponse:
    weight = normalize_weight(payload.weight)
    bracket = parse_bracket(payload.bracket)

    athletes = {a for matches in bracket.values() for pair in matches for a in pair if a}
    warnings: list[str] = []
    score_by_athlete: dict[str, float] = {}

    for athlete in athletes:
        n_athlete = normalize_name(athlete)
        data = payload.athlete_strengths.get(athlete) or payload.athlete_strengths.get(n_athlete)
        if data:
            model = AthleteStrength(name=athlete, normalized_name=n_athlete, weight=weight, gender=payload.gender, **data.model_dump())
            score = calculate_strength_score(model)
        elif n_athlete in payload.manual_strength:
            model = AthleteStrength(name=athlete, normalized_name=n_athlete, weight=weight, gender=payload.gender, manual_rating=payload.manual_strength[n_athlete])
            score = calculate_strength_score(model)
        else:
            warnings.append(f"No strength data for {athlete}, using default score.")
            model = AthleteStrength(name=athlete, normalized_name=n_athlete, weight=weight, gender=payload.gender)
            score = calculate_strength_score(model)
        score_by_athlete[n_athlete] = score

    winner_probs, top4_probs = simulate_bracket_monte_carlo(bracket, score_by_athlete, iterations=10000, seed=42)

    norm_winner_odds = {normalize_name(k): v for k, v in payload.odds_winner.items()}
    norm_top4_odds = {normalize_name(k): v for k, v in payload.odds_top4.items()}

    value_winner = detect_value(winner_probs, norm_winner_odds, "winner", weight)
    value_top4 = detect_value(top4_probs, norm_top4_odds, "top4", weight)
    for p in value_winner + value_top4:
        p.gender = payload.gender

    winner_ranking = [{"athlete": k, "prob": v} for k, v in sorted(winner_probs.items(), key=lambda x: x[1], reverse=True)]
    top4_ranking = [{"athlete": k, "prob": v} for k, v in sorted(top4_probs.items(), key=lambda x: x[1], reverse=True)]
    picks = sorted(value_winner + value_top4, key=lambda p: p.edge, reverse=True)

    return AnalyzeResponse(
        winner_ranking=winner_ranking,
        top4_ranking=top4_ranking,
        value_winner=value_winner,
        value_top4=value_top4,
        recommended_picks=picks,
        warnings=warnings,
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/competitions/{competition_id}")
async def get_competition(competition_id: int):
    return await service.get_competition(competition_id)


@app.get("/competitions/{competition_id}/contests")
async def get_competition_contests(competition_id: int):
    return await service.get_competition_contests(competition_id)


@app.get("/athletes/search")
async def search_athletes(name: str):
    return await service.search_athlete(name)


@app.post("/analyze/bracket", response_model=AnalyzeResponse)
async def analyze_bracket(payload: BracketInput):
    return analyze_single_bracket(payload)


@app.post("/analyze/tournament", response_model=TournamentAnalyzeResponse)
async def analyze_tournament(payload: TournamentAnalyzeInput):
    weight_results = {}
    global_picks = []
    warnings = []

    for weight_input in payload.weights:
        single = BracketInput(competition_name=payload.competition_name, **weight_input.model_dump())
        result = analyze_single_bracket(single)
        normalized_weight = normalize_weight(weight_input.weight)
        weight_results[normalized_weight] = result
        global_picks.extend(result.recommended_picks)
        warnings.extend([f"[{normalized_weight}] {w}" for w in result.warnings])

    global_picks = sorted(global_picks, key=lambda p: p.edge, reverse=True)
    return TournamentAnalyzeResponse(
        competition_name=payload.competition_name,
        weights=weight_results,
        global_recommended_picks=global_picks,
        warnings=warnings,
    )


@app.post("/portfolio/build")
async def portfolio(payload: PortfolioBuildInput):
    return build_portfolio(payload)
