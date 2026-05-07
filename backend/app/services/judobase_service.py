from __future__ import annotations

import os
from typing import Any

from judobase import JudoBase


class JudobaseService:
    def __init__(self) -> None:
        self.use_mock = os.getenv("USE_JUDOBASE_MOCK", "true").lower() == "true"

    async def get_competition(self, competition_id: int) -> Any:
        try:
            async with JudoBase() as api:
                return await api.competition_by_id(competition_id)
        except Exception:
            if self.use_mock:
                return {"id": competition_id, "name": "Mock Competition", "city": "Mock City"}
            raise

    async def get_competition_contests(self, competition_id: int) -> Any:
        try:
            async with JudoBase() as api:
                if hasattr(api, "contests_by_competition_id"):
                    return await api.contests_by_competition_id(competition_id)
                # TODO: fallback kept only for backwards compatibility with older judobase versions.
                all_contests = await api.all_contests()
                return [c for c in all_contests if getattr(c, "competition_id", None) == competition_id]
        except Exception:
            if self.use_mock:
                return [{"id": 1, "competition_id": competition_id, "athlete_a": "Mock A", "athlete_b": "Mock B"}]
            raise

    async def get_all_contests(self) -> Any:
        try:
            async with JudoBase() as api:
                return await api.all_contests()
        except Exception:
            return []

    async def search_athlete(self, name: str) -> Any:
        try:
            async with JudoBase() as api:
                # TODO: judobase currently has no direct judoka search by free-text name.
                # Temporary adapter: search contest index when find_contests is available.
                if hasattr(api, "find_contests"):
                    return await api.find_contests(name)
                contests = await api.all_contests()
                return [c for c in contests if name.lower() in str(c).lower()][:10]
        except Exception:
            if self.use_mock:
                return [{"id": 999, "name": name}]
            raise

    async def get_athlete_profile(self, athlete_id: int) -> Any:
        try:
            async with JudoBase() as api:
                if hasattr(api, "judoka_by_id"):
                    return await api.judoka_by_id(athlete_id)
                # TODO: compatibility with older versions only.
                if hasattr(api, "athlete_by_id"):
                    return await api.athlete_by_id(athlete_id)
                return {"id": athlete_id, "detail": "judoka_by_id no disponible"}
        except Exception:
            if self.use_mock:
                return {"id": athlete_id, "name": "Mock Athlete"}
            raise
