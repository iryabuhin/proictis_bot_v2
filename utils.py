import os
import aiohttp
import ujson
from typing import Dict

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


async def get_json(url: str, **kwargs) -> Dict:
    async with aiohttp.ClientSession() as client:
        resp = await client.request(method='GET', url=url, **kwargs)
        resp.raise_for_status()

        _json = await resp.json()

        return _json
