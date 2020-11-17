import json

from keyboards import EXIT_BUTTON, PAGE_NAVIGATION_BUTTONS
from utils import fetch_json
from asyncinit import asyncinit
from config import Config
from typing import Tuple, List, Dict, Any, Union


@asyncinit
class NewsList:
    async def __init__(self):
        self.news_json = list(
            reversed(
                await fetch_json(
                    url=Config.BASE_API_URL + Config.URL_PATH['news']
                )
            )
        )
        self.keyboard = []
        self.text = ''
        self.current_page = 1

    def get_keyboard(self) -> List:
        return self.keyboard

    def get_text(self) -> str:
        return self.text

    def reset_keyboard(self) -> None:
        self.keyboard = list()

    def reset_text(self) -> None:
        self.text = ''

    def get_news_desc_and_img_by_id(self, _id: str) -> Tuple[str, str]:
        item = [i for i in self.news_json if i['_id'] == _id]

        text, image_link = item[0]['description'], item[0]['images'][0]['link']

        return text, image_link

    def make_text_and_keyboard(self, page_num=1):
        self.make_text(page_num=page_num)
        self.make_keyboard(page_num=page_num)

    def make_keyboard(self, page_num=0):
        self.reset_keyboard()

        if page_num*Config.NEWS_PER_MSG > len(self.news_json):
            self.keyboard = [[{'text': 'Назад', 'color': 'primary'}, EXIT_BUTTON]]
            return

        for i in range((page_num-1) * Config.NEWS_PER_MSG, Config.NEWS_PER_MSG * page_num):
            payload = json.dumps({'news_id': self.news_json[i]['_id']})
            title = self.news_json[i]['title']

            if len(title) >= 40:
                title = self.trim_news_title(title)

            self.keyboard.append([
                {
                    'text': title,
                    'color': 'primary',
                    'payload': payload
                }
            ])

        self.keyboard.append(
            PAGE_NAVIGATION_BUTTONS
        )
        self.keyboard.append(
            [EXIT_BUTTON]
        )


    def make_text(self, page_num=0):
        self.reset_text()
        message = []

        if page_num * Config.NEWS_PER_MSG > len(self.news_json):
            self.text = 'Новости закончились! Нажмите "Назад", чтобы вернуться ' \
                        'к предыдущим новостям или "Выйти", чтобы выйти'
            return

        for i in range((page_num - 1) * Config.NEWS_PER_MSG, Config.NEWS_PER_MSG * page_num):
                message.append(
                '{}\n\n{}\n\n'.format(
                    f'{str(i+1)}) ' + self.news_json[i]['title'],
                    self.news_json[i]['shortDescription'],
                )
            )
        self.text = ''.join(message)

    def trim_news_title(self, title: str) -> str:
        while len(title) >= Config.NEWS_TITLE_MAX_LENGTH - 5:
            title = ' '.join(title.split()[:-1])
        return title + '...'


