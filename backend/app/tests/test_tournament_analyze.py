from fastapi.testclient import TestClient

from app.main import app


def test_tournament_analyze_two_weights_and_global_picks():
    client = TestClient(app)
    payload = {
        "competition_name": "Qazaqstan Barysy Grand Slam 2026",
        "weights": [
            {
                "weight": "-60 kg",
                "gender": "M",
                "bracket": {"A": [["M1", "M2"]], "B": [["M3", "M4"]], "C": [["M5", "M6"]], "D": [["M7", "M8"]]},
                "odds_winner": {"M1": 3.0},
                "odds_top4": {"M1": 1.5},
                "athlete_strengths": {"M1": {"manual_rating": 90}, "M2": {"manual_rating": 50}},
            },
            {
                "weight": "-52 kg",
                "gender": "F",
                "bracket": {"A": [["F1", "F2"]], "B": [["F3", "F4"]], "C": [["F5", "F6"]], "D": [["F7", "F8"]]},
                "odds_winner": {"F1": 2.5},
                "odds_top4": {"F1": 1.6},
                "athlete_strengths": {"F1": {"manual_rating": 91}, "F2": {"manual_rating": 48}},
            },
        ],
    }
    res = client.post('/analyze/tournament', json=payload)
    assert res.status_code == 200
    body = res.json()
    assert '-60 kg' in body['weights']
    assert '-52 kg' in body['weights']
    weights_in_picks = {p['weight'] for p in body['global_recommended_picks']}
    assert '-60 kg' in weights_in_picks
    assert '-52 kg' in weights_in_picks


def test_tournament_no_odds_in_one_weight_does_not_break():
    client = TestClient(app)
    payload = {
        'competition_name': 'X',
        'weights': [
            {
                'weight': '-60 kg',
                'gender': 'M',
                'bracket': {'A': [['A1', 'A2']], 'B': [['B1', 'B2']], 'C': [['C1', 'C2']], 'D': [['D1', 'D2']]},
                'odds_winner': {},
                'odds_top4': {},
                'athlete_strengths': {'A1': {'manual_rating': 80}},
            }
        ],
    }
    res = client.post('/analyze/tournament', json=payload)
    assert res.status_code == 200
    body = res.json()
    assert '-60 kg' in body['weights']
