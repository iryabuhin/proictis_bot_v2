from typing import Dict, Union, List, AnyStr, Optional

from vkbottle import keyboard_gen
from vkbottle.framework.framework.rule import Message
from vkbottle.rule import AbstractMessageRule, PayloadRule
import os
import ujson
import aiohttp

from keyboards import MAIN_MENU_KEYBOARD
from models import UserState


def surname_fuzz_processor(surname: str) -> str:
    return surname.strip().lower().replace('ё', 'е')


def envget(key: str) -> str:
    return os.environ.get(key)


async def fetch_url(url: str, **kwargs) -> str:
    async with aiohttp.ClientSession() as client:
        response = await client.request(method='GET', url=url, **kwargs)
        response.raise_for_status()

        text = await response.text()

        return text


async def fetch_json(url: str, **kwargs) -> Dict:
    async with aiohttp.ClientSession() as client:
        resp = await client.get(url=url, **kwargs)
        resp.raise_for_status()

        _json = await resp.json(loads=ujson.loads, content_type=None)

        return _json


async def return_to_main_menu(message: Message, context: Dict[str, str] = None) -> None:
    u = await UserState.get_or_none(uid=message.from_id)
    u.branch = 'main'

    if context is not None:
        u.context.update(
            **context
        )

    await u.save()
    await message(
        message='Главное меню',
        keyboard=keyboard_gen(MAIN_MENU_KEYBOARD)
    )