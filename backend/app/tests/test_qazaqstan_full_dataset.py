import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_qazaqstan_full_dataset_structure_and_endpoint_acceptance():
    data_path = Path(__file__).resolve().parents[2] / 'examples' / 'qazaqstan_2026_full_tournament_request.json'
    payload = json.loads(data_path.read_text())

    assert len(payload['weights']) == 14
    for item in payload['weights']:
        bracket = item['bracket']
        assert set(bracket.keys()) == {'A', 'B', 'C', 'D'}
        assert any(len(matches) > 0 for matches in bracket.values())

    client = TestClient(app)
    res = client.post('/analyze/tournament', json=payload)
    assert res.status_code == 200
