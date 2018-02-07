import json

from flask import url_for


def post_json(client, url, data):
    return client.post(
        url,
        data=json.dumps(data),
        content_type='application/json'
    )


def test_unexisting_text(client):
    res = post_json(
        client,
        url_for('api.classify'),
        data={
            'texts': [
                {
                    'text': 'Lorem ipsum is simply dummy text.',
                },
            ],
        }
    )
    response_msg = res.get_json()
    for text_obj in response_msg.get('texts'):
        assert text_obj.get('cls') is None
