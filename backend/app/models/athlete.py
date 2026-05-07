from __future__ import annotations

from pydantic import BaseModel, Field


class AthleteStrength(BaseModel):
    name: str
    normalized_name: str
    country: str | None = None
    weight: str | None = None
    gender: str | None = None
    world_rank: int | None = None
    ranking_points: float | None = None
    recent_wins: int = 0
    recent_losses: int = 0
    h2h_wins: int = 0
    h2h_losses: int = 0
    manual_rating: float | None = None
    notes: list[str] = Field(default_factory=list)
