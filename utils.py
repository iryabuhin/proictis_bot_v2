import os
import asyncio
import aiohttp
import sys


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
