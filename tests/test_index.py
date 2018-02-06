import pytest
from flask import url_for

from src import make_app


@pytest.fixture
def app():
    return make_app()


def test_index(client):
    res = client.get(url_for('api.index'))
    assert res.status_code == 200
    assert res.json == {'Hello': 'World'}
