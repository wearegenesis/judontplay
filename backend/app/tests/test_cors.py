from fastapi.testclient import TestClient

from app.main import app


def test_cors_preflight_analyze_tournament_not_404():
    client = TestClient(app)
    res = client.options(
        '/analyze/tournament',
        headers={
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'POST',
        },
    )
    assert res.status_code in (200, 400)
    assert 'access-control-allow-origin' in res.headers
