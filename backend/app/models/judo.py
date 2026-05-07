from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


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


class PickRecommendation(BaseModel):
    market: str
    athlete: str
    weight: str
    fair_probability: float
    implied_probability: float
    edge: float
    odds: float


class AnalyzeResponse(BaseModel):
    winner_ranking: list[dict[str, Any]]
    top4_ranking: list[dict[str, Any]]
    value_winner: list[PickRecommendation]
    value_top4: list[PickRecommendation]
    recommended_picks: list[PickRecommendation]
