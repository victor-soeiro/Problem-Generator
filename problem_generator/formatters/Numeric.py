""" problem_generator.formatters.Numeric """


FMT_ARGS_NUMERIC = [
    'comma',
    'places'
]


def format_numeric_value(value, **kwargs):
    comma = kwargs.get('comma', False)
    places = kwargs.get('places', 2)
    if places == 0:
        value = str(int(value))

    else:
        value = str(round(value, places))

    return value.replace('.', ',') if comma else value
