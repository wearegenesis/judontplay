from __future__ import annotations

from app.services.normalization import normalize_name


def parse_bracket(bracket: dict[str, list[list[str | None]]]) -> dict[str, list[tuple[str | None, str | None]]]:
    parsed: dict[str, list[tuple[str | None, str | None]]] = {}
    for pool, matches in bracket.items():
        parsed[pool] = []
        for left, right in matches:
            parsed[pool].append((normalize_name(left) if left else None, normalize_name(right) if right else None))
    return parsed
