from typing import Union, Optional, Dict
from vkbottle import keyboard_gen
from vkbottle.bot import Blueprint, Message
from vkbottle.branch import ClsBranch, rule_disposal
from vkbottle.rule import PayloadRule, CommandRule, VBMLRule
from aiocache import caches
from keyboards import MAIN_MENU_KEYBOARD, SCHEDULE_KEYBOARD, EMPTY_KEYBOARD
from typing import List, Tuple, Dict, AnyStr, Union
from content.schedule import ScheduleResponseBuilder
from exceptions import ScheduleNoEntriesFoundException, ScheduleUnknownErrorException,\
    ScheduleResponseFormatException,\
    ScheduleMultipleChoicesException
from rules import PayloadHasKey, ExitButtonPressed
from utils import fetch_json, return_to_main_menu
from models import DBStoredBranch, UserState
from config import Config
from cache_config import CACHE_CONFIG
from datetime import datetime
import ujson
import aiohttp

bp = Blueprint(name='schedule')
bp.branch = DBStoredBranch()


def parse_choices(data: Dict) -> Tuple[str, List[List[Dict]]]:
    msg = list()
    keyboard = list()

    options = [item['name'] for item in data['choices']]

    msg.append('Возможно, вы имели в виду:\n')

    for i, option in enumerate(options):
        msg.append('{}) {}'.format(
            str(i + 1),
            option
        ))

        keyboard.append(
            [
                {
                    'text': option,
                    'color': 'primary'
                }
            ]
        )

    msg = '\n'.join(msg)

    return msg, keyboard


async def fetch_schedule_json(q: str, week: int = None) -> Dict:
    params = {'query': q}

    try:
        data = await fetch_json(
            url=Config.SCHEDULE_URL,
            params=params
        )
    except aiohttp.ClientResponseError as e:
        print('[ERROR] Schedule API bad response with status {}: {}'.format(
            str(e.status),
            e.message
        ))
        raise
    except aiohttp.ClientError as e:
        print('[ERROR] General HTTP error occured: {}'.format(
            str(e)
        ))
        raise
    except ValueError as e:
        print('[ERROR] Schedule API general error: {}'.format(e))
        raise
    else:
        if week is not None:
            if data.get('table') is None:
                return data

            group = data['table']['group']
            params = {
                'group': group,
                'week': str(week)
            }

            data = await fetch_json(
                Config.SCHEDULE_URL,
                params=params
            )

        return data


@bp.on.message(CommandRule('keyboard'))
async def wrapper(ans: Message):
    await ans('Heres your keyboard', keyboard=keyboard_gen(MAIN_MENU_KEYBOARD))


@bp.on.message(PayloadRule({'selection': 'schedule'}))
async def schedule_enter(ans: Message):
    await ans('Введите ваш запрос - это может быть номер группы, аудитории или фамилия преподователя')
    await bp.branch.add(ans.from_id, 'schedule')


class ScheduleBranch(ClsBranch):
    async def branch(self, ans: Message):
        q = ans.text

        weekday = datetime.today().weekday()

        try:
            data = await fetch_schedule_json(q)
            schedule = ScheduleResponseBuilder(data)
        except aiohttp.ClientResponseError:
            await ans('Произошла ошибка, возможно API расписания временно не работает. '
                      'Если это продолжается длительное время, обратитесь к администрации сайта.')
        except ScheduleNoEntriesFoundException:
            await ans('Извините, по вашему запросу ничего не найдено.', keyboard=keyboard_gen(EMPTY_KEYBOARD))
        except ScheduleUnknownErrorException:
            await ans(
                message='Произошла неизвестная ошибка при обработке расписания. '
                        'Обратитесь к администрации сайта за дополнительной информацией.',
                keyboard=keyboard_gen(EMPTY_KEYBOARD)
                )
        except ScheduleMultipleChoicesException:
            msg, keyboard = parse_choices(data)

            await ans(
                message=msg,
                keyboard=keyboard_gen(keyboard)
            )
        else:
            schedule.build_text(weekday)
            msg = schedule.get_text()

            u = await UserState.get(uid=ans.from_id)

            if isinstance(u.context, str):
                u.context = ujson.loads(u.context)

            u.context['weekday'] = weekday
            u.context['week'] = schedule.week
            u.context['query'] = q

            caches.set_config(CACHE_CONFIG)
            cache = caches.get('redis')
            await cache.set(
                'schedule_{}'.format(str(ans.from_id)),
                schedule,
                ttl=900
            )

            await u.save()

            await ans(
                message=msg,
                keyboard=keyboard_gen(SCHEDULE_KEYBOARD, one_time=True)
            )
        
    @rule_disposal(PayloadHasKey('day'))
    async def day_schedule(self, ans: Message):

        payload = ujson.loads(ans.payload)

        u = await UserState.get(uid=ans.from_id)

        if isinstance(u.context, str):
            u.context = ujson.loads(u.context)

        u_weekday = u.context['weekday']

        if payload['day'] == 'next':
            u_weekday = (u_weekday + 1) % 7
        else:
            u_weekday = (u_weekday - 1) % 7

        caches.set_config(CACHE_CONFIG)
        cache = caches.get('redis')

        schedule = await cache.get('schedule_{}'.format(str(ans.from_id)))
        if schedule is None:
            data = await fetch_schedule_json(q=u.context['query'])
            schedule = ScheduleResponseBuilder(data)
            await cache.set(
                'schedule_{}'.format(str(ans.from_id)),
                schedule,
                ttl=900
            )

        schedule.build_text(weekday=u_weekday)

        msg = schedule.get_text()

        await ans(
            message=msg,
            keyboard=keyboard_gen(SCHEDULE_KEYBOARD, one_time=False)
        )

        u.context['weekday'] = u_weekday
        await u.save()

    @rule_disposal(PayloadHasKey('week'))
    async def change_week(self, ans: Message):
        payload = ujson.loads(ans.payload)

        u = await UserState.get(uid=ans.from_id)

        if isinstance(u.context, str):
            u.context = ujson.loads(u.context)

        _u_week = u.context['week']
        _query = u.context['query']

        if payload['week'] == 'next':
            _u_week += 1
        else:
            _u_week -= 1

        try:
            data = await fetch_schedule_json(_query, week=_u_week)
            schedule = ScheduleResponseBuilder(data)
            schedule.build_text(weekday=1)
        except aiohttp.ClientResponseError:
            await ans('При обработке запроса произошла ошибка, возможно API расписания временно не работает. '
                      'Если это продолжается длительное время, обратитесь к администрации сайта.')
        except ScheduleUnknownErrorException:
            await ans(
                message='Произошла неизвестная ошибка при обработке расписания. Обратитесь к администрации сайта за дополнительной информацией.',
                keyboard=keyboard_gen(EMPTY_KEYBOARD)
            )
        else:
            caches.set_config(CACHE_CONFIG)
            cache = caches.get('redis')

            msg = schedule.get_text()
            await ans(message=msg, keyboard=keyboard_gen(SCHEDULE_KEYBOARD, one_time=False))

            await cache.set(
                'schedule_{}'.format(str(ans.from_id)),
                schedule,
                ttl=900
            )

            u.context['week'] = _u_week
            await u.save()


    @rule_disposal(PayloadHasKey('weekdays'))
    async def show_weekdays(self, ans: Message):

        caches.set_config(CACHE_CONFIG)
        cache = caches.get('redis')

        schedule = await cache.get('schedule_{}'.format(ans.from_id))

        if schedule is None:
            data = await fetch_schedule_json()
            schedule = ScheduleResponseBuilder(data)
            await cache.set(
                'schedule_{}'.format(ans.from_id),
                schedule,
                ttl=900
            )

        schedule.build_weekday_keyboard()
        keyboard = schedule.get_keyboard()

        await ans(
            message='Выберите день недели:',
            keyboard=keyboard_gen(keyboard)
        )

    @rule_disposal(PayloadHasKey('day_num'))
    async def get_day_schedule(self, ans: Message):

        payload = ujson.loads(ans.payload)
        weekday = int(payload['day_num'])

        u = await UserState.get(uid=ans.from_id)

        if isinstance(u.context, str):
            u.context = ujson.loads(u.context)

        caches.set_config(CACHE_CONFIG)
        cache = caches.get('redis')

        schedule = await cache.get('schedule_{}'.format(str(ans.from_id)))
        if schedule is None:
            data = await fetch_schedule_json(q=u.context['query'])
            schedule = ScheduleResponseBuilder(data)
            await cache.set(
                'schedule_{}'.format(str(ans.from_id)),
                schedule,
                ttl=900
            )

        schedule.build_text(weekday=weekday)
        msg = schedule.get_text()

        await ans(
            message=msg,
            keyboard=keyboard_gen(SCHEDULE_KEYBOARD, one_time=False)
        )

        u.context['weekday'] = weekday
        await u.save()

    @rule_disposal(ExitButtonPressed())
    async def exit(self, ans: Message):
        await return_to_main_menu(ans)

    @rule_disposal(VBMLRule('выйти', lower=True))
    async def _exit(self, ans: Message):
        await return_to_main_menu(ans)


bp.branch.add_branch(ScheduleBranch, 'schedule')
