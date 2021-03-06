import json
import random

import pytest
from flask import url_for

from pestca import models


def learn(client, texts):
    client.post(
        url_for('api.learn'),
        data=json.dumps({
            'texts': texts
        }),
        content_type='application/json',
    )


def classification_accuracy(texts):
    correct = 0
    for text in texts:
        if models.classify(text['text']) == text['class']:
            correct += 1
    return correct / len(texts)


def shuffled(iterable):
    return random.sample(iterable, len(iterable))


def test_golf_dataset(client, clear_after):
    texts = [
        {
            'text': 'Sunny Hot High False',
            'class': 'No',
        },
        {
            'text': 'Rainy Cool Normal True',
            'class': 'No',
        },
        {
            'text': 'Sunny Mild Normal True',
            'class': 'Yes',
        },
        {
            'text': 'Sunny Mild High True',
            'class': 'No',
        },
        {
            'text': 'Overcast Cool Normal True',
            'class': 'Yes',
        },
        {
            'text': 'Sunny Cool Normal False',
            'class': 'Yes',
        },
        {
            'text': 'Rainy Mild Normal False',
            'class': 'Yes',
        },
        {
            'text': 'Rainy Mild High True',
            'class': 'No',
        },
        {
            'text': 'Overcast Hot High False',
            'class': 'Yes',
        },
        {
            'text': 'Rainy Mild High False',
            'class': 'Yes',
        },
        {
            'text': 'Rainy Cool Normal True',
            'class': 'Yes',
        },
        {
            'text': 'Rainy Hot High False',
            'class': 'No',
        },
        {
            'text': 'Overcast Mild High True',
            'class': 'Yes',
        },
        {
            'text': 'Overcast Hot Normal False',
            'class': 'No',
        },
    ]
    split_points = int(0.8 * len(texts))
    learn(client, texts[:split_points])
    assert 0.66 < classification_accuracy(texts[split_points:]) < 0.67


def test_two_simple_classes(client, clear_after):
    learn(client, [
        {
            'text': 'Lorem ipsum',
            'class': 'Alpha',
        },
        {
            'text': 'Lorem dolor',
            'class': 'Beta',
        },
    ])
    result = models.compute_classes_probabilities('Lorem dolor')
    assert result == {
        'Beta': 0.5,
        'Alpha': 0,
    }