""" problem_generator.modifiers.Parser """

from problem_generator.modifiers.Base import Modifier

DEFAULT_MODIFIERS = [[cls.PARSER, cls] for cls in Modifier.__subclasses__()]


def parse_variable_modifiers(**kwargs) -> Modifier:
    """ Parse the Variables to Get a Modifier.

    Kwargs:
        The variable arguments.

    Returns:
        A modifier
    """
    keys = kwargs.keys()
    for modifier in DEFAULT_MODIFIERS:
        parser = modifier[0]
        if not isinstance(parser, list):
            parser = [parser]

        if set(parser).issubset(keys):
            return modifier[1](**kwargs)

    default = next(filter(lambda i: i[0] == 'default', DEFAULT_MODIFIERS))[1]
    return default(**kwargs)
