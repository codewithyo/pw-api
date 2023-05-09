from datetime import date
from datetime import datetime as dt
from json import load
from pathlib import Path
from typing import Self, TypeAlias

from utils.pw.api import UrlType

from .api import UrlType

QuestionTitle: TypeAlias = str
QuizQuestions: TypeAlias = list[tuple[QuestionTitle,
                                      tuple[str, str, str, str]]]


class GeneralParser:
    def __init__(self, data: dict, type: UrlType) -> None:
        self.data = data
        self.type = type

    @property
    def id_(self) -> str:
        return self.data['_id']

    @property
    def title(self) -> str:
        return self.data['title']

    @property
    def date_created(self) -> date:
        """ Return the date created at. """
        date = self.data['createdAt']
        return dt.fromisoformat(date).date()

    @staticmethod
    def get_all_title_with_id(fp: Path) -> dict[str, str]:
        data: list[dict] = load(open(fp))
        return {d['_id']: d['title'] for d in data}

    @staticmethod
    def generate_fp(cid: str, type: UrlType) -> Path:
        return Path('data') / type / f'{type}_{cid}.json'

    @classmethod
    def from_id(cls, fp: Path, id_: str, type: UrlType) -> Self:
        data: list[dict] = load(open(fp))
        d = [i for i in data if i['_id'] == id_][0]
        return cls(d, type)


class Quiz(GeneralParser):
    def __init__(self, data: dict) -> None:
        """ Use this to parse through the data related to Quiz. """
        super().__init__(data=data, type='quiz')

    def questions(self) -> QuizQuestions:
        """
        Returns: `QuizQuestions = list[tuple[QuestionTitle, tuple[str, str, str, str]]]`
        """
        questions: QuizQuestions = []
        for i in self.data['quizQuestions']:
            title = i['title']
            options = []

            for opt in i['options']:
                options.append(opt['name'])

            questions.append(tuple([title, tuple(options)]))
        return questions

    @property
    def marks(self) -> int:
        return len(self.data['quizQuestions'])

    @staticmethod
    def generate_fp(cid: str) -> Path:
        return GeneralParser.generate_fp(cid, 'quiz')

    @classmethod
    def from_id(cls, fp: Path, id_: str) -> Self:
        parser = GeneralParser.from_id(fp, id_, 'quiz')
        return cls(parser.data)


class Assignment(GeneralParser):
    def __init__(self, data: dict) -> None:
        """ Use this to parse through the data related to Assignment. """
        super().__init__(data=data, type='assignment')

    @property
    def marks(self) -> int:
        """ Return max point or marks of assignment. """
        return self.data['data']['maxPoints']

    @property
    def question_url(self) -> str:
        """ Return url of the PDF file in Google Drive. """
        return self.data['data']['url']

    @property
    def solution_url(self) -> str | None:
        """ Return submitted url if assignment submitted on the website. """
        return self.data['solution']

    @property
    def download_url(self) -> str:
        prefix = 'https://drive.google.com/uc?export=download&id='
        _id = self.question_url.rsplit('/', 2)[-2]
        return prefix + _id

    @staticmethod
    def generate_fp(cid: str) -> Path:
        return GeneralParser.generate_fp(cid, 'assignment')

    @classmethod
    def from_id(cls, fp: Path, id_: str) -> Self:
        parser = GeneralParser.from_id(fp, id_, 'assignment')
        return Assignment(parser.data)
