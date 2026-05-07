from copy import deepcopy

from fastapi.testclient import TestClient

from app.main import app


def test_get_qazaqstan_state_returns_14_weights():
    c = TestClient(app)
    r = c.get('/qazaqstan/state')
    assert r.status_code == 200
    assert len(r.json()['weights']) == 14


def test_custom_tournament_analysis_accepts_full_state_and_modified_bracket_and_odds():
    c = TestClient(app)
    state = c.get('/qazaqstan/state').json()
    payload = deepcopy(state)

    w60 = next(w for w in payload['weights'] if w['weight'] == '-60 kg')
    w60['odds_winner']['Yang Yung Wei'] = 3.0
    w60['odds_top4']['Yang Yung Wei'] = 1.6
    w60['bracket']['A'][0] = ['Yang Yung Wei', None]

    r = c.post('/analyze/tournament/custom', json=payload)
    assert r.status_code == 200
    body = r.json()
    assert len(body['weights']) == 14
    assert isinstance(body['global_recommended_picks'], list)

    found = [p for p in body['weights']['-60 kg']['recommended_picks'] if p['athlete'] == 'Yang Yung Wei']
    assert found
