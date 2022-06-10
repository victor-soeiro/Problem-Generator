""" problem_generator.modifiers.classes.Multiplier """

from problem_generator.modifiers.Base import Modifier
from problem_generator.formatters.Numeric import FMT_ARGS_NUMERIC, format_numeric_value


REQUIRED_ARGS = [
    'anchor', 'multi'
]


class MultiplierValue(Modifier):
    ARGS = REQUIRED_ARGS
    FMT_ARGS = FMT_ARGS_NUMERIC
    PARSER = REQUIRED_ARGS

    def __init__(self, **kwargs) -> None:
        super(MultiplierValue, self).__init__(**kwargs)

    def generate(self, **kwargs):
        anchor = self.get_argument('anchor', **kwargs)
        multiplication = self.get_argument('multi', **kwargs)
        return anchor * multiplication

    def format(self, value):
        return format_numeric_value(value, **self.fmt_args)
