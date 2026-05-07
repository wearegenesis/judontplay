import asyncio

from app.services.judobase_service import JudobaseService


def test_get_competition_mock():
    svc = JudobaseService()
    out = asyncio.run(svc.get_competition(123))
    assert out is not None
