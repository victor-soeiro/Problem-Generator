""" problem_generator """

import os.path
import json


__CONFIG__ = 'config.json'

FUNCTION_INITIALIZER = 'f='

MODIFIER_INITIALIZER = '|'
MODIFIER_VALUE_DEFINITION = '='
MODIFIER_SEPARATOR = ';'

with open(os.path.join(os.path.dirname(__file__), __CONFIG__), 'r', encoding='utf-8') as file:
    CONFIG = json.load(file)
