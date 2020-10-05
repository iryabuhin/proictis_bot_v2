import aiohttp
import aiofiles
import pathlib
from typing import Dict, Tuple, Optional
from aiohttp.web import HTTPClientError
from asyncinit import asyncinit
from rapidfuzz import fuzz
from utils import surname_fuzz_processor, fetch_url

import importlib.util
spec = importlib.util.find_spec('ujson')
if spec is None:
    import json
else:
    import ujson as json


FUZZ_RATIO_CUTOFF = 80


class MentorNotFoundException(Exception):
    pass


@asyncinit
class MentorMessageCard:

    _MENTORS_API_URL: str = 'https://proictis.sfedu.ru/api/mentors'

    async def __init__(self, mentor_surname: str, use_cached: bool = True):
        # async constructor wont work without "asyncinit" pip package
        self.mentor_surname = mentor_surname
        self.use_cached = use_cached

        self.mentor_info: Dict = dict()
        await self.find_mentor()

    async def find_mentor(self) -> None:
        all_mentors = await self.fetch_all_mentors_data()

        for mentor in all_mentors:
            current_mentor_surname = mentor['surname']
            ratio: float

            ratio = fuzz.partial_ratio(
                self.mentor_surname,
                current_mentor_surname,
                processor=surname_fuzz_processor
            )

            if ratio >= FUZZ_RATIO_CUTOFF:
                # TODO log every ratio and input values for debug purposes
                self.mentor_info = mentor

                return

        raise MentorNotFoundException('Mentor with surname "{}" not found!'.format(
            self.mentor_surname
        ))

    def generate_card_text(self) -> str:
        msg = list()
        msg.append('{} {} {}, {}'.format(
            self.mentor_info['surname'],
            self.mentor_info['name'],
            self.mentor_info['patronymic'],
            self.mentor_info['post']
        ))
        msg.append(self.mentor_info['directions'])
        msg.append('\n')
        msg.append('Почта: {}'.format(self.mentor_info['email']))
        msg.append('Телефон: {}'.format(self.mentor_info['phone']))
        msg.append('\n')

        return '\n'.join(msg)

    def get_photo_and_doc_links(self) -> Tuple[str, str]:
        return (
            self.mentor_info['avatar']['link'],
            self.mentor_info['files'][0]['link']
        )

    def as_tuple(self) -> Tuple[str, str, str]:
        return (
            self.generate_card_text(),
            *self.get_photo_and_doc_links()
        )


    async def fetch_all_mentors_data(self, **kwargs) -> Dict:
        try:
            text = await fetch_url(
                url=MentorMessageCard._MENTORS_API_URL,
                **kwargs
            )
        except (aiohttp.ClientError, HTTPClientError):
            # TODO implement a proper database caching here
            if self.use_cached:
                return await self.parse_cached_mentor_info()
            else:
                raise

        try:
            all_mentors_data = json.loads(text)
        except json.JSONDecodeError as e:
            raise

        return all_mentors_data

    async def parse_cached_mentor_info(
            self,
            filename: str = 'mentor_info.json'
    ) -> Dict:
        here = pathlib.Path(__file__).parent
        async with aiofiles.open(here.joinpath(filename), 'r') as f:
            content = await f.read()

            all_mentor_data = json.loads(content)

            return all_mentor_data

