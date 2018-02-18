learn_post_schema = {
    'type': 'object',
    'properties': {
        'texts': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                    },
                    'class': {
                        'type': 'string',
                    }
                },
                'required': ['text', 'class'],
            },
            'minItems': 1,
        },
    },
    'required': ['texts'],
}


classify_post_schema = {
    'type': 'object',
    'properties': {
        'texts': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                    }
                },
                'required': ['text'],
            },
            'minItems': 1,
        }
    },
    'required': ['texts'],
}
