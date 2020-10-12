from typing import List, Dict, Tuple, AnyStr, Union
from exceptions import ScheduleResponseFormatException, ScheduleNoEntriesFoundException, ScheduleUnknownErrorException
from datetime import datetime
from keyboards import SCHEDULE_KEYBOARD, EXIT_BUTTON


class ScheduleResponseBuilder:
    def __init__(self, schedule_json: Dict, type: str = 'groups'):
        self.data = schedule_json
        self.text = ''
        self.keyboard = ''

        if self.data.get('table') is None:
            if self.data.get('results') == 'no_entries':
                raise ScheduleNoEntriesFoundException
            elif self.data.get('choices') is not None:
                self.choices = schedule_json['choices']
                self.parse_choices()
            else:
                raise ScheduleUnknownErrorException
        else:
            self.table: List = self.data['table']['table']
            self.name: str = self.data['table']['name']
            self.weekdays: List = [item[0] for item in self.table[2:]]
            self.days: List = [item[1:] for item in self.table[2:]]
            self.week = self.data['table']['week']

    def get_text(self) -> str:
        return self.text

    def get_keyboard(self) -> List[Union[List[Dict], Dict]]:
        return self.keyboard

    def reset_text(self) -> None:
        self.text = ''

    def build_text(self, weekday: int = 1) -> None:
        msg = list()
        msg.append('Расписание {}:'.format(self.name))
        msg.append('Сегодня: {}\n'.format(self.weekdays[weekday-1]))

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


    def parse_choices(self):
        pass

