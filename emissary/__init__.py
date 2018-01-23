import logging
import sys

from flask import Flask
from flask_restplus import Api
import yaml


VERSION = '0.0.1'
CONFIG_FILENAME = 'emissary.yaml'

app = Flask(__name__)
api = Api(app, version=VERSION, title='Emissary API')

try:
    with open(CONFIG_FILENAME, 'r') as config_file:
        app.config['emissary'] = yaml.load(config_file.read()).get('emissary')
except IOError:
    logging.error('Could not read config file: %s' % CONFIG_FILENAME)


import emissary.handler
