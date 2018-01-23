import logging
import sys

from flask import Flask
import yaml


VERSION = '0.0.1'
CONFIG_FILENAME = 'emissary.yaml'


def setup_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


app = Flask(__name__)

try:
    with open(CONFIG_FILENAME, 'r') as config_file:
        app.config['emissary'] = yaml.load(config_file.read()).get('emissary')
except IOError:
    logging.error('Could not read config file: %s' % CONFIG_FILENAME)

if not app.debug:
    setup_logging()

import emissary.handler
