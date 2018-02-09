import string

from redis import Redis


redis = Redis(host='redis', port=6379, decode_responses=True)


letters_whitespace = set(string.ascii_letters + string.whitespace)


def is_letter_whitespace(char):
    """Check if character is letter or whitespace.

    :param char:
        Tested character.
    """
    return char in letters_whitespace


def tokenize(text):
    """Generate tokens from given text.

    :param text:
        Source of tokens. In this version of pestca text will be
        lowercased and delimited to alpha characters only.
    :return:
        Iterable containing tokens.
    """
    alpha_text = ''.join(filter(is_letter_whitespace, text))
    return alpha_text.lower().split()


def classify(text):
    """Classify given text to the most probable class.

    :param text:
        A string, representing an observation which needs to be classified.
    :return:
        The most likely class or ``None`` if no class available.
    """
    # get numbers of classifications tokens to classes
    tokens = {}
    for token in tokenize(text):
        tokens[token] = redis.hgetall('token:{}'.format(token))

    # get classes and compute their probabilities of occurrences
    classes = redis.hgetall('classes')
    if not classes:
        return None
    print(classes)
    classes_all = sum(map(int, classes.values()))
    probabilities = dict(
        (cls, float(count) / classes_all)
        for (cls, count) in classes.items()
    )
    # compute conditional probabilities of the token set
    for token in tokens:
        for cls in tokens[token]:
            supports_cls = float(tokens[token].get(cls, 0))
            prob_token_cls = supports_cls / float(classes[cls])
            probabilities[cls] *= prob_token_cls
    # return class with maximum probability
    return max(probabilities, key=probabilities.get)


def learn(text, cls):
    """Learn classifier by assignment given text to class.

    Learn by increasing occurrences counters.
    It's important to increase cls counter first
    to avoid reading while tokens will be increased
    and cls counter not. Probability >1.0 is not acceptable.
    :param text:
        A string, representing an observation which is classified to cls.
    :param cls:
        A string, representing category.
    :return:
    """
    redis.hincrby('classes', cls, 1)
    for token in tokenize(text):
        redis.hincrby('token:{}'.format(token), cls, 1)
