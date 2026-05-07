from __future__ import annotations

from collections import defaultdict


def _win_prob(sa: float, sb: float) -> float:
    return sa / (sa + sb) if sa + sb > 0 else 0.5


def simulate_probabilities(parsed_bracket: dict[str, list[tuple[str | None, str | None]]], strength: dict[str, float]):
    winner = defaultdict(float)
    top4 = defaultdict(float)

    for _, matches in parsed_bracket.items():
        for a, b in matches:
            if a and not b:
                winner[a] += 0.5
                top4[a] += 1.0
                continue
            if b and not a:
                winner[b] += 0.5
                top4[b] += 1.0
                continue
            if not a and not b:
                continue
            pa = _win_prob(strength.get(a, 1.0), strength.get(b, 1.0))
            pb = 1 - pa
            winner[a] += pa * 0.5
            winner[b] += pb * 0.5
            top4[a] += pa
            top4[b] += pb

    total_w = sum(winner.values()) or 1.0
    total_t = sum(top4.values()) or 1.0
    return ({k: v / total_w for k, v in winner.items()}, {k: v / total_t for k, v in top4.items()})
