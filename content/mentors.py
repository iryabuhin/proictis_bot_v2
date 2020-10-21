import aiohttp
import aiofiles
import pathlib
from typing import Dict, Tuple, Optional, List
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


class MentorMessageCard:

    _MENTORS_API_URL: str = 'https://proictis.sfedu.ru/api/mentors'

    def __init__(self, mentor_data: List[Dict[str, str]], surname: str):
        self.mentor_data: List[List, Dict[str, str]] = mentor_data
        self.surname: str = surname
        self.mentor_info = None

        self.find_mentor()

    def find_mentor(self) -> None:

        for mentor in self.mentor_data:
            current_mentor_surname = mentor['surname']
            ratio: float = 0.0

            ratio = fuzz.partial_ratio(
                self.surname.lower(),
                current_mentor_surname.lower()
            )

            if ratio >= FUZZ_RATIO_CUTOFF:
                # TODO log every ratio and input values for debug purposes
                self.mentor_info = mentor

                return

        raise MentorNotFoundException('Mentor with surname "{}" not found!'.format(
            self.surname
        ))

    def generate_card_text(self) -> str:

        if self.mentor_info is None:
            raise MentorNotFoundException

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

        if self.mentor_info is None:
            raise MentorNotFoundException

        return (
            self.mentor_info['avatar']['link'],
            self.mentor_info['files'][0]['link']
        )

    def as_tuple(self) -> Tuple[str, str, str]:

        if self.mentor_info is None:
            raise MentorNotFoundException

        return (
            self.generate_card_text(),
            *self.get_photo_and_doc_links()
        )

