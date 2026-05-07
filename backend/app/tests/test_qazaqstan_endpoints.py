from fastapi.testclient import TestClient

from app.main import app


def test_get_qazaqstan_full_example_has_14_weights():
    client = TestClient(app)
    res = client.get('/examples/qazaqstan/full')
    assert res.status_code == 200
    body = res.json()
    assert len(body['weights']) == 14


def test_post_analyze_qazaqstan_returns_14_weights_and_global_picks_field():
    client = TestClient(app)
    res = client.post('/analyze/qazaqstan')
    assert res.status_code == 200
    body = res.json()
    assert len(body['weights']) == 14
    assert 'global_recommended_picks' in body
    assert isinstance(body['global_recommended_picks'], list)
