""" problem_generator.modifiers.Utils """


from string import Formatter
from typing import Tuple, Union, Dict

from problem_generator import MODIFIER_INITIALIZER, MODIFIER_VALUE_DEFINITION, MODIFIER_SEPARATOR, FUNCTION_INITIALIZER
from problem_generator.modifiers.Base import Modifier


def get_sections(text: str) -> Tuple[str, str]:
    """ Get all Section within a Text.

    Args:
        text: The text containing the variables.

    Returns:
        The metadata and question section.
    """

    lines = text.split('\n')

    metadata_index = [i for i, line in enumerate(lines) if line.strip() == '[metadata]']
    question_index = [i for i, line in enumerate(lines) if line.strip() == '[question]']

    if metadata_index and question_index:
        metadata = '\n'.join(lines[metadata_index[0]+1:question_index[0]])
        question = '\n'.join(lines[question_index[0]+1:])

    elif metadata_index and not question_index:
        raise ValueError('Question Section not Found.')

    elif not metadata_index and question_index:
        metadata = ''
        question = '\n'.join(lines[question_index[0] + 1:])

    else:
        metadata = ''
        question = '\n'.join(lines)

    return metadata, question


def get_metadata(text: str) -> Tuple[dict, dict, str]:
    """ Get all Values in the Metadata Section.

    This method will collect all the information contained in metadata section, including variables
    definitions, global modifiers and a answer function.

    Args:
        text: The text containing the variables.

    Returns:
        [dict, dict, str] The clean text and all variables.

    """
    variables = {}
    modifiers = {}
    function = ''

    lines = text.split('\n')
    for line in lines:
        if MODIFIER_INITIALIZER in line:
            values = line.split(MODIFIER_INITIALIZER)
            if len(values) == 1 or not values[0]:
                continue

            name = values[0].strip()
            variables[name] = {'modifiers': {}}

            mods = [i.split('=') for i in values[1].split(MODIFIER_SEPARATOR)]
            mods_to_dict = {mod[0].strip(): mod[1].strip() for mod in mods}
            variables[name]['modifiers'] = mods_to_dict

        elif line.startswith(FUNCTION_INITIALIZER):
            function = line[2:].strip()

        elif MODIFIER_VALUE_DEFINITION in line:
            values = line.split(MODIFIER_VALUE_DEFINITION)
            if len(values) == 1 or not values[0]:
                continue

            modifier = values[0].strip()
            value = values[1].strip()
            modifiers[modifier] = value

        else:
            continue

    return variables, modifiers, function


def get_clean_text_and_variables(text: str) -> Tuple[str, Dict[str, Union[dict, Modifier]]]:
    """ Get all Variables and Clean the Text.

    This method will gather all variables defined within brackets, and clean the text of the
    variables modifiers.

    Args:
        text: The text containing the variables.

    Returns:
        [str, dict] The clean text and all variables.
    """
    clean_text = text
    variables = {}

    variables_in_text = [fn for _, fn, _, _ in Formatter().parse(text) if fn is not None]

    for var in variables_in_text:
        values = var.split(MODIFIER_INITIALIZER)
        name = values[0].strip()

        if len(values) == 1 or not name:
            clean_text = clean_text.replace('{'+values[0]+'}', '')
            continue

        if name not in variables.keys():
            variables[name] = {'modifiers': {}}

        if len(values) > 1:
            clean_text = clean_text.replace(var, name)

            modifiers = [i.split('=') for i in values[1].split(MODIFIER_SEPARATOR)]
            modifiers_to_dict = {mod[0].strip(): mod[1].strip() for mod in modifiers}

            if variables[name].get('modifiers', {}):
                variables[name]['modifiers'].update(modifiers_to_dict)
            else:
                variables[name]['modifiers'] = modifiers_to_dict

    return clean_text, variables
