from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AthleteStrengthInput(BaseModel):
    world_rank: int | None = None
    ranking_points: float | None = None
    recent_wins: int = 0
    recent_losses: int = 0
    h2h_wins: int = 0
    h2h_losses: int = 0
    manual_rating: float | None = None


class BracketPool(BaseModel):
    matches: list[list[str | None]] = Field(default_factory=list)


class BracketInput(BaseModel):
    competition_name: str
    weight: str
    gender: str
    bracket: dict[str, list[list[str | None]]]
    odds_winner: dict[str, float] = Field(default_factory=dict)
    odds_top4: dict[str, float] = Field(default_factory=dict)
    manual_strength: dict[str, float] = Field(default_factory=dict)
    athlete_strengths: dict[str, AthleteStrengthInput] = Field(default_factory=dict)


class TournamentWeightInput(BaseModel):
    weight: str
    gender: str
    bracket: dict[str, list[list[str | None]]]
    odds_winner: dict[str, float] = Field(default_factory=dict)
    odds_top4: dict[str, float] = Field(default_factory=dict)
    manual_strength: dict[str, float] = Field(default_factory=dict)
    athlete_strengths: dict[str, AthleteStrengthInput] = Field(default_factory=dict)


class TournamentAnalyzeInput(BaseModel):
    competition_name: str
    weights: list[TournamentWeightInput]


class PickRecommendation(BaseModel):
    market: str
    athlete: str
    weight: str
    fair_probability: float
    implied_probability: float
    edge: float
    odds: float
    gender: str | None = None


class AnalyzeResponse(BaseModel):
    winner_ranking: list[dict[str, Any]]
    top4_ranking: list[dict[str, Any]]
    value_winner: list[PickRecommendation]
    value_top4: list[PickRecommendation]
    recommended_picks: list[PickRecommendation]
    warnings: list[str] = Field(default_factory=list)


class TournamentAnalyzeResponse(BaseModel):
    competition_name: str
    weights: dict[str, AnalyzeResponse]
    global_recommended_picks: list[PickRecommendation]
    warnings: list[str] = Field(default_factory=list)
