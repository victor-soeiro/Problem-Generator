""" problem_generator.modifiers.Base """

from typing import Type

from math_parser import evaluate

from problem_generator.main.Utils import get_raw_variables


class Modifier:
    """ A Base Class to Create Modifiers. """
    ARGS = []
    FMT_ARGS = []

    PARSER = None

    def __init__(self, **kwargs):
        """ Initialize the Modifier.

        Kwargs:
            The Modifier Arguments and it's Values.
        """
        self.args = {}
        self.fmt_args = {}

        self.set_arguments(**kwargs)

    def get_argument(self, key: str, default: any = None, type_: Type = float, parse: bool = True, **kwargs) -> any:
        """ Get the Given Argument.

        Args:
            key: The argument name.
            default: Default value if not defined.
            type_: The returned type.
            parse: True to parse a math expression.

        Kwargs:
            The correlated arguments.

        Returns:
            An argument value.
        """
        value = str(self.args.get(key, default))

        if parse:
            variables = get_raw_variables(value, remove_numbers=True)
            if not all([True if i in kwargs else False for i in variables]):
                raise Exception(f'Missing Variable(s) in {value}.')

            evaluated_value = evaluate(value, **{k: str(v) for k, v in kwargs.items() if k in variables})
            return type_(evaluated_value)

        else:
            return type_(value)

    def set_arguments(self, **kwargs) -> None:
        """ Set All Given Arguments.

        Kwargs:
            The Modifier Arguments and it's Values.
        """
        for key, value in kwargs.items():
            if key in self.ARGS:
                self.args[key] = value

            if key in self.FMT_ARGS:
                self.fmt_args[key] = value

    def generate(self, *args, **kwargs) -> str:
        """ Generates a Value.

        This is an abstract method. It needs to be implemented.

        Returns:
            A Generated Value.
        """
        raise NotImplementedError('Needs to be Implemented.')

    def format(self, value: str) -> str:
        """ Returns a Formatted Value.

        This is an abstract method. It needs to be implemented.

        Args:
            value: A Value.

        Returns:
            A Formatted Value.
        """
        raise NotImplementedError('Needs to be Implemented.')
