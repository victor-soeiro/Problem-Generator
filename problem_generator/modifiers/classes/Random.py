""" problem_generator.modifiers.classes.Random """

from random import choice

from numpy import arange

from problem_generator.modifiers.Base import Modifier
from problem_generator.formatters.Numeric import FMT_ARGS_NUMERIC, format_numeric_value


class RandomValue(Modifier):
    """ A Random Value Generator """
    ARGS = [
        'min',
        'max',
        'step',
    ]

    FMT_ARGS = FMT_ARGS_NUMERIC

    MIN_DEFAULT = 0
    MAX_DEFAULT = 1000
    STEP_DEFAULT = 1

    COMMA_DEFAULT = True
    DECIMALS_DEFAULT = 1

    PARSER = 'default'

    def __init__(self, **kwargs):
        super(RandomValue, self).__init__(**kwargs)

    def generate(self, **kwargs):
        min_ = self.get_argument('min', self.MIN_DEFAULT, **kwargs)
        max_ = self.get_argument('max', self.MAX_DEFAULT, **kwargs)
        step = self.get_argument('step', self.STEP_DEFAULT, **kwargs)
        return float(choice(arange(min_, max_, step)))

    def format(self, value):
        return format_numeric_value(value, **self.fmt_args)
