import ujson
from exceptions import ScheduleResponseFormatException,\
    ScheduleNoEntriesFoundException, \
    ScheduleUnknownErrorException, \
    ScheduleMultipleChoicesException
from typing import List, Dict, Tuple, AnyStr, Union


class ScheduleResponseBuilder:
    def __init__(self, data: Dict):
        self.data: Dict[str, Union[List[str], Dict[str, str]]] = data
        self.text: str = ''
        self.keyboard: List = []

        if self.data.get('table') is None:
            if self.data.get('results') == 'no_entries':
                raise ScheduleNoEntriesFoundException
            elif self.data.get('choices') is not None:
                raise ScheduleMultipleChoicesException
            else:
                raise ScheduleUnknownErrorException
        else:
            self.table: List = self.data['table']['table']
            self.name: str = self.data['table']['name']
            self.weekdays: List = [item[0] for item in self.table[2:]]
            self.days: List = [item[1:] for item in self.table[2:]]
            self.week: str = self.data['table']['week']

    def get_text(self) -> str:
        return self.text

    def get_keyboard(self) -> List[Union[List[Dict], Dict]]:
        return self.keyboard

    def reset_text(self) -> None:
        self.text = ''

    def reset_keyboard(self) -> None:
        self.keyboard = []

    def build_text(self, weekday: int = 1) -> None:
        msg = list()
        msg.append('Расписание {}:'.format(self.name))
        msg.append('{}\n'.format(self.weekdays[weekday-1]))

        for num, time, entry in zip(
            self.table[0][1:],
            self.table[1][1:],
            self.days[weekday-1]
        ):
            msg.append('{}) {}: {}\n'.format(
                num,
                time,
                entry if entry else '-'
            ))

        self.text = '\n'.join(msg)

    def build_weekday_keyboard(self):
        keyboard = list()

        for i, day in enumerate(self.weekdays):
            keyboard.append(
                [
                    {
                        'text': day,
                        'color': 'primary',
                        'payload': ujson.dumps({'day_num': str(i+1)})
                    }
                ]
            )

        self.keyboard = keyboard



