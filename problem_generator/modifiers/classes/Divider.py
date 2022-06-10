""" problem_generator.modifiers.classes.Divider """

from problem_generator.modifiers.Base import Modifier
from problem_generator.formatters.Numeric import FMT_ARGS_NUMERIC, format_numeric_value


REQUIRED_ARGS = [
    'anchor', 'div'
]


class DividerValue(Modifier):
    ARGS = REQUIRED_ARGS
    FMT_ARGS = FMT_ARGS_NUMERIC
    PARSER = REQUIRED_ARGS

    def __init__(self, **kwargs) -> None:
        super(DividerValue, self).__init__(**kwargs)

    def generate(self, **kwargs) -> str:
        anchor = self.get_argument('anchor', **kwargs)
        division = self.get_argument('div', **kwargs)
        if division == 0:
            division = 1

        return anchor / division

    def format(self, value):
        return format_numeric_value(value, **self.fmt_args)
