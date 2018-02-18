from flask import url_for


def test_index(client):
    res = client.get(url_for('api.index'))
    assert res.status_code == 200
    assert res.json == {'Hello': 'World'}
