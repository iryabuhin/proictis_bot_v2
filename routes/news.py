from typing import List, Union, Dict, Tuple, AnyStr, Callable
from vkbottle.bot import Blueprint, Message
from vkbottle.rule import VBMLRule, AbstractMessageRule, LevenshteinDisRule
from vkbottle.branch import ClsBranch, rule_disposal
from proictis_api.news import NewsList
from vkbottle.keyboard import keyboard_gen
from vkbottle import PhotoUploader
from models.user_state import PostgresStoredBranch, UserState
import json

bp = Blueprint(name='news')
bp.branch = PostgresStoredBranch()


class PayloadContainsFieldRule(AbstractMessageRule):
        def __init__(self, fields=Union[str, List[str]], mode=1):
            self.mode = mode
            if isinstance(fields, str):
                self.fields = [fields]
            else:
                self.fields = fields
        @staticmethod
        def dispatch(payload: str) -> dict:
            try:
                return json.loads(payload)
            except json.decoder.JSONDecodeError:
                return dict()
            
        async def check(self, message: Message) -> bool:
            if message.payload is not None:
                payload = self.dispatch(message.payload)
                if self.mode == 1:
                    for field in self.fields:
                        if payload.get(field) is None:
                            return False
                    return True


@bp.on.message(VBMLRule('новости', lower=True))
async def news_handler(ans: Message):
    await ans(
        'Нажмите "Далее", чтобы увидеть последние новости с сайта Проектного офиса или'
        'нажмите "Поиск" для интерактивного поиска по новостям Проектного офиса и группы ИКТИБ ВКонтакте',
        keyboard=keyboard_gen([[{'text': 'Далее', 'color': 'positive'}], [{'text': 'Поиск'}]])
    )
    await bp.branch.add(ans.from_id, 'news')


class NewsBranch(ClsBranch):
    @rule_disposal(VBMLRule('выйти', lower=True))
    async def exit_branch(self, ans: Message):
        await ans('[DEBUG] Exiting branch {}'.format(self.__class__.__name__), keyboard=keyboard_gen([]))
        await bp.branch.exit(ans.from_id)

    @rule_disposal(LevenshteinDisRule('предыдущая страница', lev_d=85))
    async def inc_page(self, ans: Message):
        u = await UserState.get(uid=ans.from_id)

        if 'page_num' in u.context:
            u.context['page_num'] += 1
        else:
            u.context['page_num'] = 2

        await u.save()

        news = await NewsList()
        news.make_text_and_keyboard(page_num=u.context['page_num'])

        msg = news.get_text()
        kbrd = news.get_keyboard()

        await ans('Загружаем новости...', keyboard=keyboard_gen([]))
        await ans(message=msg, keyboard=keyboard_gen(kbrd))

    @rule_disposal(VBMLRule('далее', lower=True))
    async def send_news(self, ans: Message):
        news_list = await NewsList()
        news_list.make_text_and_keyboard()

        msg = news_list.get_text()
        kbrd = news_list.get_keyboard()

        u = await UserState.get(uid=ans.from_id)
        u.context['page_num'] = 1
        await u.save()

        await ans(
            message=msg,
            keyboard=keyboard_gen(kbrd, one_time=True)
        )

    @rule_disposal(PayloadContainsFieldRule('news_id'))
    async def get_detailed_news_view(self, ans: Message):
        payload = PayloadContainsFieldRule.dispatch(ans.payload)

        news_list = await NewsList()
        msg, image_url = news_list.get_news_desc_and_img_by_id(_id=payload['news_id'].strip('{}'))

        photo_uploader = PhotoUploader(api=bp.api, generate_attachment_strings=True)

        img_data = await photo_uploader.get_data_from_link(link=image_url)
        attachment = await photo_uploader.upload_message_photo(img_data)

        await ans(message=msg, attachment=attachment)

    async def branch(self, ans: Message):
        pass

bp.branch.add_branch(NewsBranch, 'news')