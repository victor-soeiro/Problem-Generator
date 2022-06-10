""" problem_generator.main.Utils """

import numpy as np

from os import listdir
from os.path import isfile, join
from typing import Union, List

from math_parser.Node import OPERATIONS_ALLOWED


def get_all_templates(path: Union[str, list]):
    if isinstance(path, (list, tuple)):
        templates = []
        for p in path:
            templates.extend([
                join(p, x) for x in listdir(p) if isfile(join(p, x))
            ])

    elif isinstance(path, str):
        templates = [
            join(path, x) for x in listdir(path) if isfile(join(path, x))
        ]

    else:
        templates = []

    return templates


def get_raw_variables(value: str, remove_numbers: bool = False) -> List[str]:
    """ Get all the Raw Values of an Argument.

    Args:
        value: An argument.
        remove_numbers: If True removes all the numbers of the argument.

    Returns:
        A list of values.
    """

    raw = value.replace(' ', '')
    for operation in OPERATIONS_ALLOWED:
        raw = raw.replace(operation, ' ')

    variables_in_raw = raw.split(' ')
    if remove_numbers:
        variables_in_raw = [i for i in variables_in_raw if not i.replace('.', '').replace(',', '').isdigit()]

    return [i for i in variables_in_raw if i]


def get_connections(values: list, variables: list, index: bool = True) -> list:
    """ Get the Correlations between Variables of a Row.

    Args:
        values: The arguments of the variable modifiers.
        variables: All variables.
        index: If True returns the variables index.

    Returns:
        [list] A list containing the connected variables.
    """
    connects_to = []
    for j in values:
        raw_variables = get_raw_variables(j)
        for i in variables:
            if i in raw_variables and i not in connects_to:
                connects_to.append(variables.index(i))

    if index:
        return connects_to
    else:
        return [variables[i] for i in connects_to]


def verify_connections_to_not_loop(mods: dict) -> bool:
    """ Verify if the Modifiers Values does not Create a Loop.

    This function creates a correlation matrix with the variables from the modifier dictionary, and
    calculates it's determinant. If the determinant is zero, it will create a loop.

    Args:
        mods: The modifiers dictionary.

    Returns:
        [bool] True if it's verified, else False.
    """
    variables = list(mods.keys())
    n = len(variables)
    connections = np.diag(np.full(n, 1))

    for i, var in enumerate(variables):
        values = mods[var].values()
        connections[i][i] = 1
        connects_to = get_connections(values=values, variables=variables)
        for c in connects_to:
            connections[i][c] = 1

    det = np.linalg.det(connections)
    if det == 0:
        return False

    return True


def get_order_queue(mods: dict) -> list:
    """ Order the Variables Executions to Generate the Values.

    Args:
       mods: The modifiers dictionary.

    Returns:
        A list containing the modifiers order.
    """
    if not verify_connections_to_not_loop(mods=mods):
        raise ValueError('Variables are creating a Loop.')

    variables = list(mods.keys())
    queue = []
    for var in mods.keys():
        values = mods[var].values()
        # bounds = set([i for i in variables for j in list(values) if i == j])
        bounds = get_connections(values, variables, index=False)
        if bounds:
            if var in bounds:
                raise ValueError(f'{var} depends on it self.')

            indexes = [queue.index(i) for i in bounds if i in queue]
            if indexes:
                queue.insert(max(indexes)+1, var)
            else:
                queue.insert(-1, var)
        else:
            queue.insert(0, var)

    return queue
