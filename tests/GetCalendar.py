
import sys
sys.path.append('.')

import Ut3.Celcat
import Ut3.Utils

def method_1() -> None:

    # You are sure that information about your group

    celcat_calendar: Ut3.Celcat.Calendar = \
        Ut3.Celcat.Calendar(
            group = Ut3.Utils.Group(
                code = '31788',
                name = 'KINI9A',
            ),
            year_return = 2022
        )

    celcat_calendar.update()

    for crs_syllabus in celcat_calendar.syllabus:
        print(str(crs_syllabus))

def method_2() -> None:

    # You are not sure => check before get calendar
    # This method is more safe

    # Get group with name
    index: int = Ut3.Celcat.datas.is_group(s='KINI9A')

    # Get group with code
    # index: int = Ut3.Celcat.datas.is_group(s='31788')

    group: Ut3.Utils.Group = None if (index < 0) else Ut3.Celcat.datas.groups[index]

    if(group is None):
        print('Group not found')
    else:
        celcat_calendar: Ut3.Celcat.Calendar = \
            Ut3.Celcat.Calendar(
                group = group,
                year_return = 2022
            )

        celcat_calendar.update()

        for crs_syllabus in celcat_calendar.syllabus:
            print(str(crs_syllabus))


if __name__ == '__main__':

    print('Method 1 :')
    method_1()

    print('\nMethod 2 :')
    method_2()