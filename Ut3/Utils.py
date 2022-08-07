import html
import re


class Course:

    def __init__(self, code: str, name: str) -> None:
        self.code: str = code
        self.name: str = name

    def __eq__(self, other: "Course") -> bool:
        return self.code == other.code

    def __str__(self) -> str:
        return self.code + '-' + self.name

    def __hash__(self) -> int:
        return str.__hash__(self.code)


class Group:

    def __init__(self, code: str, name: str) -> None:
        self.code: str = code
        self.name: str = name


class Location:

    def __init__(self, name) -> None:
        self.name: str = name


class String:

    def replace_html_number(s: str) -> str:
        return html.unescape(s)

    def remove_backslash_character(s: str) -> str:
        return re.compile(r'[\n\r\t]').sub('', s)


