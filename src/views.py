from flask import Blueprint
from flask import jsonify
from flask import request

from . import models


api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify({'Hello': 'World'})


@api.route('/classify', methods=['POST'])
def classify():
    request_msg = request.get_json()
    response = {
        'status': 'ok',
        'texts': [],
    }
    for text_obj in request_msg.get('texts'):
        text = text_obj.get('text')
        cls = models.classify(text)
        response['texts'].append(
            {
                'text': text,
                'class': cls,
            }
        )
    return jsonify(response)


@api.route('/learn', methods=['POST'])
def learn():
    request_msg = request.get_json()
    for text_obj in request_msg.get('texts'):
        text = text_obj.get('text')
        cls = text_obj.get('cls')
        models.learn(text, cls)
    return jsonify({'status': 'ok'})
