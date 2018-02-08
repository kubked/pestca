import json

import pytest
from flask import url_for

from pestca import models


@pytest.fixture(scope="function")
def clear_after():
    yield clear_after
    models.redis.flushdb()


def post_json(client, url, data):
    return client.post(
        url,
        data=json.dumps(data),
        content_type='application/json',
    ).json


def test_classify_corect_req(client, clear_after):
    res = post_json(
        client,
        url_for('api.classify'),
        data={
            'texts': [
                {
                    'text': 'Lorem ipsum is simply dummy text.',
                },
            ],
        },
    )
    for text_obj in res.get('texts'):
        assert text_obj.get('cls') is None


def test_classify_text_payload(client, clear_after):
    res = client.post(
        url_for('api.classify'),
        data="lorem ipsum dolor sit amet",
        content_type='application/text',
    ).json
    assert res.get('status') == 'error'


def test_learn_wrong_json(client, clear_after):
    res = post_json(
        client,
        url_for('api.classify'),
        data={
            'texts': [
                {
                    'class': 'developers developers developers',
                },
            ],
        },
    )
    assert res.get('status') == 'error'


def test_learn_correct_req(client, clear_after):
    res = post_json(
        client,
        url_for('api.learn'),
        data={
            'texts': [
                {
                    'text': 'Lorem ipsum is simply dummy text.',
                    'class': 'Lorem Ipsum',
                }
            ]
        },
    )
    assert res.get('status') == 'ok'


def test_learn_text_payload(client, clear_after):
    res = client.post(
        url_for('api.learn'),
        data="first roadster on mars}{",
        content_type='application/text',
    ).json
    assert res.get('status') == 'error'


def test_learn_wrong_json(client, clear_after):
    res = post_json(
        client,
        url_for('api.learn'),
        data={
            'alfa': 'beta',
        },
    )
    assert res.get('status') == 'error'