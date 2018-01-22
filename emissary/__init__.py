import logging
import sys

from flask import Flask
import yaml


VERSION = '0.0.1'
CONFIG_FILENAME = 'emissary.yaml'

app = Flask(__name__)

try:
    with open(CONFIG_FILENAME, 'r') as config_file:
        app.config['emissary'] = yaml.load(config_file.read()).get('emissary')
except IOError:
    logging.error('Could not read config file: %s' % CONFIG_FILENAME)


import emissary.handler

