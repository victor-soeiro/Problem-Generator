""" problem_generator.modifiers.classes.Value """

from problem_generator.modifiers.Base import Modifier
from problem_generator.formatters.Numeric import FMT_ARGS_NUMERIC, format_numeric_value


REQUIRED_ARGS = [
    'value'
]


class Value(Modifier):
    ARGS = REQUIRED_ARGS
    FMTS_ARGS = FMT_ARGS_NUMERIC
    PARSER = REQUIRED_ARGS

    def __init__(self, **kwargs) -> None:
        super(Value, self).__init__(**kwargs)

    def generate(self, **kwargs) -> float:
        value = self.get_argument('value', parse=True, **kwargs)
        return value

    def format(self, value):
        return format_numeric_value(value, **self.fmt_args)
