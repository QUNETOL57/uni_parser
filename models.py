from typing import NamedTuple


class Theme(NamedTuple):
    id          : int
    name        : str
    subject_id  : int
    semestr     : int
    messages    : str
    result      : str
    link        : str


class Subject(NamedTuple):
    id          : int
    name        : str
    semestr     : int
    type_id     : int
    teacher_id  : int
    link        : str