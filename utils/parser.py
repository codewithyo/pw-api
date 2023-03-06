""" Used to get some data from assignments data. """


from datetime import date, datetime
from enum import Enum, auto
from typing import Literal


class SubmitError(Exception):
    """ Raises when data is not submitted on the website. """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GeneralParser:
    def __init__(self, data: dict, type: Literal['quiz', 'assignment']) -> None:
        self.data = data
        self.type = type

    @property
    def id(self) -> str:
        return self.data['lesson']['_id']

    @property
    def title(self) -> str:
        return self.data['lesson']['title']

    @property
    def course_id(self) -> str:
        return self.data['lesson']['courseId']

    @property
    def is_submitted(self) -> bool:
        """ True if submitted on the website """
        return 'userSubmission' in self.data.keys()

    def get_submitted_points(self) -> tuple[int, int]:
        """ Return (received, outOf) """
        key = 'quizSubmission' if self.type == 'quiz' else 'assignmentSubmission'

        if GeneralParser.is_submitted:
            return tuple(self.data['userSubmission'][key]['points'].values())

        raise SubmitError(f"{self.type.title()} is not submitted on website.")

    @property
    def date_created(self) -> date:
        """ Return the date created at. """
        date = self.data['lesson']['createdAt']
        return datetime.fromisoformat(date).date()


class Quiz(GeneralParser):
    def __init__(self, data: dict) -> None:
        """ Used to get all the related to Quiz. """
        super().__init__(data=data, type='quiz')

    def questions(self):
        """ Returns a list of tuple which includes title of the question
        at `0th` index and `4` options. """
        questions = []
        for i in self.data['lesson']['quizQuestions']:
            title = i['title']
            options = []

            for opt in i['options']:
                options.append(opt['name'])

            questions.append(tuple([title] + options))
        return questions

    @property
    def marks(self) -> int:
        return len(self.data['lesson']['quizQuestions'])


class Assignment(GeneralParser):
    def __init__(self, data: dict) -> None:
        """ Used to fetch all the data related to Assignments. """
        super().__init__(data=data, type='assignment')

    @property
    def marks(self) -> int:
        """ Return max point or marks of assignment. """
        return self.data['lesson']['data']['maxPoints']

    @property
    def url(self) -> str:
        """ Return url of the PDF file in Google Drive. """
        return self.data['lesson']['data']['url']

    @property
    def submitted_url(self) -> str:
        """ Return submitted url if assignment submitted on the website. """
        if self.is_submitted:
            return self.data['userSubmission']['assignmentSubmission']['data']['url']

        raise SubmitError("Assignment is not submitted on website.")

    @property
    def submitted_comment(self) -> str:
        """ Returns the comment given by the checker of the assignment. """
        if self.is_submitted:
            return self.data['userSubmission']['assignmentSubmission']['data']['comment']

        raise SubmitError("Assignment is not submitted on website.")

    @property
    def download_url(self) -> str:
        # Get the id from url
        _id = self.url.rsplit('/', 2)[-2]

        # Download url prefix
        prefix = 'https://drive.google.com/uc?export=download&id='

        return prefix + _id
