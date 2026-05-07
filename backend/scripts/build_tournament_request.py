from __future__ import annotations

import json
from pathlib import Path

from app.services.normalization import normalize_weight

BASE = Path(__file__).resolve().parents[1] / "examples"
FULL_PATH = BASE / "qazaqstan_2026_full_tournament_request.json"
ODDS_PATH = BASE / "qazaqstan_2026_odds.json"
STRENGTHS_PATH = BASE / "qazaqstan_2026_strengths.json"
OUTPUT_PATH = BASE / "qazaqstan_2026_ready_to_analyze.json"


def build() -> dict:
    full = json.loads(FULL_PATH.read_text())
    odds = json.loads(ODDS_PATH.read_text())
    strengths = json.loads(STRENGTHS_PATH.read_text())

    for w in full.get("weights", []):
        key = normalize_weight(w["weight"])
        odds_entry = odds.get(key, {})
        w["odds_winner"] = odds_entry.get("odds_winner", {})
        w["odds_top4"] = odds_entry.get("odds_top4", {})
        w["athlete_strengths"] = strengths.get(key, {})

    OUTPUT_PATH.write_text(json.dumps(full, indent=2, ensure_ascii=False))
    return full


if __name__ == "__main__":
    result = build()
    print(f"Generated: {OUTPUT_PATH}")
    print(f"Weights: {len(result.get('weights', []))}")
