from flask import jsonify


class ErrorHandler(Exception):
    def __init__(self, error, status_code=500):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code

    def to_json(self):
        response = {
            'error': self.error,
            'status_code': self.status_code,
            'status': 'error',
        }
        return jsonify(response)

    @classmethod
    def not_json_format(cls):
        return cls('Message is not json', 400)

    @classmethod
    def wrong_msg_format(cls):
        return cls('Message format does not apply to schema', 400)
