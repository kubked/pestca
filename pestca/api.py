from flask import Blueprint
from flask import jsonify
from flask import request
from jsonschema import validate as validate_json
from jsonschema import ValidationError

from pestca import models
from pestca.error_handlers import ErrorHandler
from pestca.schemas import classify_post_schema
from pestca.schemas import learn_post_schema


api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify({'Hello': 'World'})


def get_request_json(schema):
    msg = request.get_json()
    if msg is None:
        raise ErrorHandler.not_json_format()
    try:
        validate_json(msg, schema)
    except ValidationError:
        raise ErrorHandler.wrong_msg_format()
    return msg


@api.route('/classify', methods=['POST'])
def classify():
    request_msg = get_request_json(classify_post_schema)
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
    request_msg = get_request_json(learn_post_schema)
    for text_obj in request_msg.get('texts'):
        text = text_obj.get('text')
        cls = text_obj.get('cls')
        models.learn(text, cls)
    return jsonify({'status': 'ok'})
