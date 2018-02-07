

simple_memory = {}


def classify(text):
    return simple_memory.get(text, None)


def learn(text, cls):
    simple_memory[text] = cls
