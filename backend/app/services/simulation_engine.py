from __future__ import annotations

import random
from collections import defaultdict

from app.services.normalization import normalize_name
from app.services.strength_service import predict_match_probability


def simulate_probabilities(parsed_bracket: dict[str, list[tuple[str | None, str | None]]], score_by_athlete: dict[str, float]):
    """Legacy simplistic simulator (kept for backward compatibility)."""
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

            score_a = score_by_athlete.get(normalize_name(a), 50.0)
            score_b = score_by_athlete.get(normalize_name(b), 50.0)
            pa = predict_match_probability(score_a, score_b)
            pb = 1 - pa
            winner[a] += pa * 0.5
            winner[b] += pb * 0.5
            top4[a] += pa
            top4[b] += pb

    total_w = sum(winner.values()) or 1.0
    return ({k: v / total_w for k, v in winner.items()}, dict(top4))


def _simulate_match(a: str | None, b: str | None, scores: dict[str, float], rng: random.Random) -> str | None:
    if a and not b:
        return a
    if b and not a:
        return b
    if not a and not b:
        return None
    pa = predict_match_probability(scores.get(normalize_name(a), 50.0), scores.get(normalize_name(b), 50.0))
    return a if rng.random() < pa else b


def _simulate_pool(matches: list[tuple[str | None, str | None]], scores: dict[str, float], rng: random.Random) -> str | None:
    branches = [_simulate_match(a, b, scores, rng) for a, b in matches]
    branches = [x for x in branches if x is not None]
    if not branches:
        return None
    while len(branches) > 1:
        nxt = []
        i = 0
        while i < len(branches):
            if i + 1 >= len(branches):
                nxt.append(branches[i])
            else:
                nxt.append(_simulate_match(branches[i], branches[i + 1], scores, rng))
            i += 2
        branches = [x for x in nxt if x is not None]
    return branches[0]


def simulate_bracket_monte_carlo(parsed_bracket: dict[str, list[tuple[str | None, str | None]]], score_by_athlete: dict[str, float], iterations: int = 10000, seed: int = 42):
    rng = random.Random(seed)
    winner_counts = defaultdict(int)
    top4_counts = defaultdict(int)

    for _ in range(iterations):
        pool_winners = {}
        for pool in ("A", "B", "C", "D"):
            pool_winners[pool] = _simulate_pool(parsed_bracket.get(pool, []), score_by_athlete, rng)

        semifinalists = [w for w in [pool_winners["A"], pool_winners["B"], pool_winners["C"], pool_winners["D"]] if w]
        for s in semifinalists:
            top4_counts[s] += 1

        sf1 = _simulate_match(pool_winners["A"], pool_winners["B"], score_by_athlete, rng)
        sf2 = _simulate_match(pool_winners["C"], pool_winners["D"], score_by_athlete, rng)
        champion = _simulate_match(sf1, sf2, score_by_athlete, rng)
        if champion:
            winner_counts[champion] += 1

    winner_probs = {k: v / iterations for k, v in winner_counts.items()}
    top4_probs = {k: v / iterations for k, v in top4_counts.items()}
    return winner_probs, top4_probs
