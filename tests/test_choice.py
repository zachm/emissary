from collections import defaultdict
import random
import string

from emissary import app
from emissary.choice import Choice
import emissary.mailgun

app.config['emissary']['providers'] = {
                                       'mailgun': {
                                                   'enabled': 1.0,
                                                   'class': 'emissary.mailgun.Mailgun'
                                                  },
                                       'mandrill': {
                                                    'enabled': 0.0,
                                                    'class': 'emissary.mandrill.Mandrill'
                                                   }
                                      }


def test_config_integration():
    c = Choice()
    assert sorted(c.weights) == [0.0, 1.0]
    assert sorted(c.classes) == ['emissary.mailgun.Mailgun', 'emissary.mandrill.Mandrill']


def test_static_config_for_class():
    c = Choice()
    assert c.choose() == emissary.mailgun.Mailgun


def test_choice():
    c = Choice()
    c.weights = [0.1] * 10
    c.classes = string.ascii_lowercase[:10]

    random.seed(0)  # break the PRNG

    distribution = defaultdict(lambda: 0)
    for x in range(1000):
        distribution[c._choose()] += 1

    # even enough distribution for my taste.
    assert len(distribution.keys()) == 10
    assert distribution['a'] == 114
    assert distribution['b'] == 87
    assert distribution['c'] == 95
    assert distribution['d'] == 102
    assert distribution['e'] == 110
    assert distribution['f'] == 89
    assert distribution['g'] == 109
    assert distribution['h'] == 104
    assert distribution['i'] == 86
    assert distribution['j'] == 104
