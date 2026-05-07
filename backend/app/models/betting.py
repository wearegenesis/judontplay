from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.judo import PickRecommendation


class PortfolioBuildInput(BaseModel):
    picks: list[PickRecommendation]
    stake_total: float
    max_exposure_per_judoka: float = 0.2
    max_exposure_per_weight: float = 0.35
    profile: str = "media"


class Ticket(BaseModel):
    type: str
    picks: list[PickRecommendation]
    total_odds: float
    stake: float
    potential_return: float


class PortfolioResponse(BaseModel):
    tickets: list[Ticket]
    exposure_by_judoka: dict[str, float]
    exposure_by_weight: dict[str, float]
    warnings: list[str] = Field(default_factory=list)
