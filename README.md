# CelcatUT3

Python package to get public datas from Celcat UT3 (University Toulouse 3).

Public datas are :
- Calendars
- Groups
- Rooms and Building
- Courses

Mainly, this package make request and parse data send by Celcat.

## Exemple:

```py
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
```