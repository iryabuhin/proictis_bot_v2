import pathlib
from typing import List, Dict, Optional, AnyStr, Union, Tuple

import aiofiles
from dotenv import load_dotenv
from utils import envget

class SingletonMeta:
    _instances = dict()

    def __call__(self, cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BotConfig:
    def __init__(self, tokens: List = [], use_dotenv: bool = True):
        self._dict = dict()
        self._dict['TOKENS'] = tokens

        if use_dotenv:
            self.load_dotenv()

        self.load_tokens_from_env()


    def __getitem__(self, item):
        return self._dict.__getitem__(item)

    def __setitem__(self, key, value):
        return self._dict.__setitem__(key, value)

    async def load_tokens_from_env(self):
        """ Loads a list of colon-separated tokens from environment variables $TOKEN[S] """
        tokens = envget('TOKEN') or envget('TOKENS')

        if tokens is None or not tokens:
            raise ValueError(
                'No VK tokens provided! Make sure that your tokens are stored in '
                'environment variable TOKENS separated by colon sign!'
            )

        for token in tokens.split(':'):
            self._dict['TOKENS'].append(token)

    def load_dotenv(self) -> None:
        here = pathlib.Path(__file__).parent
        dotenv_path = here.joinpath('.env')

        if dotenv_path.exists():
            load_dotenv(
                dotenv_path=dotenv_path.absolute().as_posix()
            )
        else:
            raise ValueError('No .env configuration file found in root directory!')


if __name__ == '__main__':
    cfg = BotConfig()
    print(id(cfg))
    cfg2 = BotConfig()
    print(id(cfg2))