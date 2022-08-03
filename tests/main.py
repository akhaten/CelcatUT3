
import sys
sys.path.append('.')

import Ut3.Celcat
import Ut3.Utils

if __name__ == '__main__':

    celcat_calendar: Ut3.Celcat.Calendar = \
        Ut3.Celcat.Calendar(
            group = Ut3.Utils.Group(
                code = 'MINF8TPA13',
                name = None,
            ),
            year_return = 2021
        )

    celcat_calendar.update()

    for crs_syllabus in celcat_calendar.syllabus:
        print(str(crs_syllabus))