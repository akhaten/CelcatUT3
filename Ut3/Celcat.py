import datetime
import requests
import dateutil.rrule
import parse
import enum
import typing

import Ut3.Utils
import Ut3.Celcat
import Ut3.Url


class Datas:
    class Category(enum.Enum):
        GROUP = 1
        LOCATION = 2
        COURSE = 3
        UNKNOW = 100

    def __init__(self) -> None:

        self.groups: list[Ut3.Utils.Group] = []

        response: requests.Response = requests.post(url=Ut3.Url.all_groups_in_formation(
            formation_id=Ut3.Url.Formation.ALL,
            max_size=10000
        )
        )

        for res in response.json()["results"]:
            id: str = res['id']
            r = parse.parse('{name} (' + id + ')', res['text'])
            self.groups.append(
                Ut3.Utils.Group(
                    code=res['id'],
                    name=r['name']
                )
            )

        self.locations: list[Ut3.Utils.Location] = []
        response: requests.Response = requests.post(url=Ut3.Url.locations(max_size=10000))
        for res in response.json()["results"]:
            self.locations.append(Ut3.Utils.Location(name=res['id']))

        self.courses: list[Ut3.Utils.Course] = []
        response: requests.Response = requests.post(url=Ut3.Url.courses(max_size=100000))

        for res in response.json()["results"]:

            r = parse.parse('{code} - {name}', res['text'])

            if r == None:
                r = parse.parse('{code} {name}', res['text'])

            self.courses.append(
                Ut3.Utils.Course(
                    code=r['code'],
                    name=r['name']
                )
            )

    def is_location(self, s: str) -> int:
        for index in range(0, len(self.locations)):
            loc: Ut3.Utils.Location = self.locations[index]
            if s in loc.name:
                return index
        return -1

    def is_group(self, s: str) -> int:
        for index in range(0, len(self.groups)):
            grp: Ut3.Utils.Group = self.groups[index]
            if (s == grp.name) or (s == grp.code):
                return index
        return -1

    def is_course(self, s: str) -> bool:
        for index in range(0, len(self.courses)):
            crs: Ut3.Utils.Course = self.courses[index]
            if crs.code in s:
                return index
        return -1
    


datas: Datas = Datas()


class Course:

    def __init__(
            self,
            id: Ut3.Utils.Course,
            begin: datetime.datetime,
            end: datetime.datetime,
            location: Ut3.Utils.Location,
            groups: "list[Ut3.Utils.Group]",
            category: str
    ) -> None:
        self.id: Ut3.Utils.Course = id
        self.begin: datetime.datetime = begin
        self.end: datetime.datetime = end
        self.location: Ut3.Utils.Location = location
        self.groups: list[Ut3.Utils.Group] = groups
        self.category: str = category


class Calendar:

    def __init__(self, group: Ut3.Utils.Group, year_return: int) -> None:
        self.__group: Ut3.Utils.Group = group
        self.__year_return: int = year_return
        self.__courses: list[Course] = []
        self.__syllabus: list[Ut3.Utils.Course] = []

    @property
    def courses(self) -> 'list[Course]':
        return self.__courses

    @courses.setter
    def courses(self, value) -> None:
        raise AttributeError('courses is not writeable')

    @property
    def syllabus(self) -> 'list[Ut3.Utils.Course]':
        return self.__syllabus

    @syllabus.setter
    def syllabus(self, value) -> None:
        raise AttributeError('syllabus is not writeable')

    def update(self) -> None:
        self.__syllabus, self.__courses = Request.get(group=self.__group, year_return=self.__year_return)

    # def save_as_yaml(self, path_filename: str) -> None:
    #     pass

    # def save_as_json(self, path_filename: str) -> None:
    #     pass

    # def save_as_ics(self, path_filename: str) -> None:
    #     pass


class Request:

    def __responses_to_courses(response: "list[dict]") -> typing.Tuple[set, "list[Course]"]:

        to_courses: list[Ut3.Celcat.Course] = []
        syllabus: set[Ut3.Utils.Course] = set()

        for res in response:

            category: str = res['eventCategory']

            if not (category in ('CONGES', 'FERIE', 'PONT')):

                description: list[str] = list(map(
                    lambda s: Ut3.Utils.String.remove_backslash_character(Ut3.Utils.String.replace_html_number(s)),
                    [r[0] for r in parse.findall(">{}<", '>' + res['description'] + '<')])
                )

                courses: list[Ut3.Utils.Course] = []
                groups: list[str] = []
                locations: list[str] = []
                start: datetime.datetime = datetime.datetime.strptime(res['start'], '%Y-%m-%dT%H:%M:%S')
                end: datetime.datetime = datetime.datetime.strptime(res['end'], '%Y-%m-%dT%H:%M:%S')

                def process(s: str) -> bool:

                    index: int = datas.is_course(s)
                    if 0 <= index:
                        courses.append(datas.courses[index])
                        return True

                    index: int = datas.is_group(s)
                    if 0 <= index:
                        groups.append(datas.groups[index])
                        return True

                    index: int = datas.is_location(s)
                    if 0 <= index:
                        locations.append(datas.locations[index])
                        return True

                    return False

                for s in description:
                    added: bool = process(s)

                for course in courses:
                    syllabus.add(course)

                    to_courses.append(
                        Course(
                            id=course,
                            begin=start,
                            end=end,
                            location=locations,
                            groups=groups,
                            category=category
                        )
                    )

        return syllabus, to_courses

    def get(group: Ut3.Utils.Group, year_return: int) -> typing.Tuple[set, "list[Course]"]:

        # Make dates for request data
        # https://dateutil.readthedocs.io/en/stable/rrule.html

        rule = dateutil.rrule.rrule(
            freq=dateutil.rrule.MONTHLY,
            dtstart=datetime.date(year=year_return, month=9, day=1),
            until=datetime.date(year=year_return + 1, month=9, day=1),
        )

        dates: list[datetime.date] = list(rule)

        # Convert response to CalcatUT3.Celcat.Courses

        response: list[dict] = Request.__make_request(group=group, dates=dates)
        syllabus, courses = Request.__responses_to_courses(response)

        return syllabus, courses

    def __data(federationIds: str, start: datetime.datetime, end: datetime.datetime, resType: Ut3.Url.ResType) -> dict:
        return {
            'federationIds[]': federationIds,
            'start': str(start),
            'end': str(end),
            'resType': resType.value,
            'calView': 'month'
        }

    def __make_request(group: Ut3.Utils.Group, dates: "list[datetime.date]") -> "list[dict]":

        response_json = []

        #requests.get()

        for index in range(0, len(dates) - 1):
            response = requests.post(
                url=Ut3.Url.CALENDAR,
                data=Request.__data(
                    federationIds=group.code,
                    start=dates[index],
                    end=dates[index + 1],
                    resType=Ut3.Url.ResType.GROUP
                )
            )

            response_json += response.json()

        return response_json
