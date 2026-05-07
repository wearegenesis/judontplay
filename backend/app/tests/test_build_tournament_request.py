import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from scripts.build_tournament_request import OUTPUT_PATH, build


def test_build_tournament_request_script_and_endpoint_acceptance():
    full_before = json.loads((Path(__file__).resolve().parents[2] / 'examples' / 'qazaqstan_2026_full_tournament_request.json').read_text())
    out = build()

    assert OUTPUT_PATH.exists()
    generated = json.loads(OUTPUT_PATH.read_text())
    assert len(generated['weights']) == 14

    before_brackets = {w['weight']: w['bracket'] for w in full_before['weights']}
    after_brackets = {w['weight']: w['bracket'] for w in generated['weights']}
    assert before_brackets == after_brackets

    w60 = next(w for w in generated['weights'] if w['weight'] == '-60 kg')
    assert 'Yang Yung Wei' in w60['odds_winner']
    assert 'Yang Yung Wei' in w60['athlete_strengths']

    client = TestClient(app)
    res = client.post('/analyze/tournament', json=out)
    assert res.status_code == 200
