""" problem_generator.modifiers.classes.Delta """

from problem_generator.modifiers.Base import Modifier
from problem_generator.formatters.Numeric import FMT_ARGS_NUMERIC, format_numeric_value


REQUIRED_ARGS = [
    'anchor', 'delta'
]


class DeltaValue(Modifier):
    ARGS = REQUIRED_ARGS
    FMT_ARGS = FMT_ARGS_NUMERIC
    PARSER = REQUIRED_ARGS

    def __init__(self, **kwargs) -> None:
        super(DeltaValue, self).__init__(**kwargs)

    def generate(self, **kwargs) -> str:
        anchor = self.get_argument('anchor', **kwargs)
        delta = self.get_argument('delta', **kwargs)
        return anchor + delta

    def format(self, value):
        return format_numeric_value(value, **self.fmt_args)
