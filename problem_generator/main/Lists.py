""" problem_generator.main.Lists

This package defines the ListOfQuestions object.

TODO:
- Multiple versions of a list.
- Multiple different lists.
"""

from typing import Union

from problem_generator.main.Questions import Question
from problem_generator.main.Utils import get_all_templates


class ListOfQuestions:
    def __init__(self, path: Union[str, list], number_of_questions: int = 5, init: bool = True, **kwargs) -> None:
        """ Initialize a List of Questions.

        Args:
            path: A Template Path or a List of Templates Path containing the Questions.
            number_of_questions: Number of Questions of the List
        """
        self._path = path
        if not kwargs.get('copy', False):
            self._templates = get_all_templates(self._path)

        self.questions = []
        self.number_of_questions = number_of_questions

        if init:
            self.generate()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        self._templates = get_all_templates(self.path)

    @property
    def amount_of_questions(self):
        return len(self._templates)

    def generate(self) -> list:
        """ Generates a given Number of Questions.

        Returns:
            A List containing the Generated Questions.
        """
        self.questions.clear()

        for _ in range(self.number_of_questions):
            new_question = Question()
            new_question.choose(templates=self._templates)
            self.questions.append(new_question)

        return self.questions

    def randomize(self) -> list:
        """ Randomizes the Questions of the List.

        Returns:
            A List containing the Questions Randomized.
        """
        for question in self.questions:
            question.randomize()

        return self.questions

    def __copy__(self):
        new = type(self)(path=self.path, number_of_questions=self.number_of_questions, copy=True)
        new.__dict__.update(self.__dict__)
        return new


def get_multiple_versions():
    pass


def get_different_versions():
    pass
