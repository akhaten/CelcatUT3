


import enum

BASE_RESOURCE = 'https://edt.univ-tlse3.fr/calendar2/Home/ReadResourceListItems?myResources=false'
CALENDAR = 'https://edt.univ-tlse3.fr/calendar2/Home/GetCalendarData'

class Formation(enum.Enum):
    ALL = '___'
    L1 = 'L1_'
    L2 = 'L2_'
    L3 = 'L3_'
    M1 = 'M1_'
    M2 = 'M2_'


class ResType(enum.Enum):
    COURSE = 100
    LOCATION = 102
    GROUP = 103 


def url(search_term: str, max_size: int, res_type: int) -> str:
    return BASE_RESOURCE \
        + '&searchTerm='+search_term \
        + '&pageSize='+str(max_size) \
        + '&resType='+str(res_type)


def all_groups_in_formation(formation_id: Formation, max_size: int = 5000) -> str : 
    return url(search_term=formation_id.value, max_size=max_size, res_type=ResType.GROUP.value)

def locations(max_size: int = 5000) -> str:
    return url(search_term='___', max_size=max_size, res_type=ResType.LOCATION.value)

def courses(max_size: int = 5000) -> str:
    return url(search_term='___', max_size=max_size, res_type=ResType.COURSE.value)

