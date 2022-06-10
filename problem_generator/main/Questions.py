""" problem_generator.main.Questions

This packages contains the Question object.

TODO:
- Databases implementation.
"""

from random import choice

from math_parser import evaluate

from problem_generator.modifiers.Parser import parse_variable_modifiers
from problem_generator.modifiers.Utils import get_sections, get_clean_text_and_variables, get_metadata
from problem_generator.main.Utils import get_order_queue, get_all_templates


class Question:
    def __init__(self) -> None:
        """ Initialize the Question Object. """
        self.text = None
        self.path = None
        self.function = None
        self.variables = {}
        self.values = {}
        self.values_formatted = {}
        self.order = []

        self._raw = None
        self._raw_metadata = None

    @property
    def raw(self) -> str:
        return self._raw

    @raw.setter
    def raw(self, value) -> None:
        self._raw_metadata, self._raw = get_sections(value)

        self._set_variables()
        self._set_metadata()
        self._set_order()

        self._set_generators()

        self.randomize()

    def choose(self, templates: list, **kwargs) -> None:
        """ Choose a Random Template of a List of Templates.

        Args:
            templates: A list of templates.

        Kwargs:
            collect: Set True to collect all templates of a path or list of paths.
       """
        if kwargs.get('collect', False):
            templates = get_all_templates(templates)

        self.path = choice(templates)
        with open(self.path, 'r', encoding='utf-8') as file:
            self.raw = file.read().strip()

    def randomize(self) -> str:
        """ Randomize the Variables.

        Returns:
            [str] The text with the variables value.
        """
        if not self.variables:
            raise Warning('Modifiers are not defined.')

        values = [self.variables[v] for v in self.order]
        for key, val in zip(self.order, values):
            self.values[key] = val['generator'].generate(**self.values)
            self.values_formatted[key] = val['generator'].format(self.values[key])

        return self.text.format(**self.values_formatted)

    def answer(self) -> str:
        """ Given the Function and the Variables Values Returns the Answer.

        Returns:
            [str] The Formatted Answer.
        """
        if self.function:
            return str(evaluate(self.function, **self.values))

        return ''

    def _set_variables(self) -> None:
        """ Get and Set the Variables and the Clean Text. """
        text, variables = get_clean_text_and_variables(self.raw)
        self.text = text
        self.variables = variables

    def _set_metadata(self) -> None:
        """ Get and Set the Metadata Information. """
        if not self._raw_metadata:
            return

        variables, modifiers, function = get_metadata(self._raw_metadata)
        self.function = function
        self.variables.update(variables)

        for var in self.variables.keys():
            for key, value in modifiers.items():
                if key not in self.variables[var]['modifiers'].keys():
                    self.variables[var]['modifiers'][key] = value

    def _set_order(self) -> None:
        """ Get and Set the Variables Definition Order. """
        order_dict = {key: values['modifiers'] for key, values in self.variables.items()}
        self.order = get_order_queue(order_dict)

    def _set_generators(self) -> None:
        for key in self.variables.keys():
            self.variables[key]['generator'] = parse_variable_modifiers(**self.variables[key]['modifiers'])

    def __copy__(self):
        new = type(self)()
        new.__dict__.update(self.__dict__)
        return new

    def __repr__(self):
        if self.raw and self.values:
            return self.text.format(**self.values_formatted)

        return None
