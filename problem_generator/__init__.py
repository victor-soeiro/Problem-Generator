""" problem_generator """

from os.path import join, dirname
from json import load


__CONFIG__ = 'config.json'

FUNCTION_INITIALIZER = 'f='

MODIFIER_INITIALIZER = '|'
MODIFIER_VALUE_DEFINITION = '='
MODIFIER_SEPARATOR = ';'

with open(join(dirname(__file__), __CONFIG__), 'r', encoding='utf-8') as file:
    CONFIG = load(file)
