from fastapi.testclient import TestClient

from app.main import app


def test_analyze_bracket_not_flat_with_strengths():
    client = TestClient(app)
    payload = {
        "competition_name": "X",
        "weight": "-60 kg",
        "gender": "M",
        "bracket": {
            "A": [["Strong", "Weak"]],
            "B": [["B1", "B2"]],
            "C": [["C1", "C2"]],
            "D": [["D1", "D2"]],
        },
        "odds_winner": {"Strong": 2.0},
        "odds_top4": {"Strong": 1.5},
        "athlete_strengths": {
            "Strong": {"manual_rating": 95, "world_rank": 3, "ranking_points": 4000},
            "Weak": {"manual_rating": 50, "world_rank": 80, "ranking_points": 200},
        },
    }
    res = client.post("/analyze/bracket", json=payload)
    assert res.status_code == 200
    body = res.json()
    probs = {item["athlete"]: item["prob"] for item in body["winner_ranking"]}
    assert probs["Strong"] > probs["Weak"]
    assert probs["Strong"] != probs["Weak"]
