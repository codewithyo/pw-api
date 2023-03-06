from json import load


def get_course_id_title() -> dict[str, str]:
    return {i['title']: i['_id']
            for i in load(open('data/courses/all_course_data.json'))['courses']}


class Instructors:
    def __init__(self, data: dict) -> None:
        self.data = data

    @property
    def description(self) -> str:
        return self.data['description']

    @property
    def name(self) -> str:
        return self.data['name']

    @property
    def social(self) -> dict[str, str]:
        return self.data['social']


class Course:
    def __init__(self, name: str, _id: str) -> None:
        self.name = name
        self.id = _id

        # Data of the course from JSON file
        self.data: dict = [i for i in load(open('data/courses/all_course_data.json'))['courses']
                           if i['_id'] == self.id][0]

    @property
    def learn(self) -> list[str]:
        return self.data['courseMeta'][0]['overview']['learn']

    @property
    def features(self) -> list[str]:
        return self.data['courseMeta'][0]['overview']['features']

    @property
    def language(self) -> str:
        return self.data['courseMeta'][0]['overview']['language']

    @property
    def duration(self) -> str:
        try:
            return self.data['courseMeta'][0]['overview']['duration']
        except KeyError:
            return 'N/A'

    @property
    def price(self) -> str:
        pricing = self.data['pricing']
        price = pricing['IN']
        discount = pricing['discount']

        return price - (price * (discount/100))

    def instructors(self) -> list[Instructors]:
        return [Instructors(i) for i in self.data['instructorsDetails']]
