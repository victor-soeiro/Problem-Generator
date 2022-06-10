""" problem_generator.modifiers.classes.Group """

from random import choice

from problem_generator import CONFIG
from problem_generator.modifiers.Base import Modifier


GROUPS = CONFIG['GROUPS']


class GroupValue(Modifier):
    ARGS = [
        'group'
    ]

    GROUP_DEFAULT = 'default'

    PARSER = 'group'

    def __init__(self, **kwargs):
        super(GroupValue, self).__init__(**kwargs)

    def generate(self, **kwargs) -> str:
        self.set_arguments(**kwargs)

        key = self.args.get('group', self.GROUP_DEFAULT)
        if key not in GROUPS.keys():
            key = self.GROUP_DEFAULT

        value = choice(GROUPS[key])
        return value
