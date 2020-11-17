from typing import List, Union, Dict, Tuple, AnyStr, Callable
import ujson
from vkbottle.bot import Blueprint, Message
from vkbottle.rule import VBMLRule, AbstractMessageRule, LevenshteinDisRule, PayloadRule
from vkbottle.branch import ClsBranch, rule_disposal
from content.news import NewsList
from vkbottle.keyboard import keyboard_gen
from vkbottle import PhotoUploader
from models.user_state import DBStoredBranch, UserState
from keyboards import MAIN_MENU_KEYBOARD, EMPTY_KEYBOARD
from rules import PayloadHasKey, ExitButtonPressed

from utils import return_to_main_menu

bp = Blueprint(name='news')
bp.branch = DBStoredBranch()


@bp.on.message(VBMLRule('новости', lower=True))
async def news_handler(ans: Message):
    await ans(
        'Нажмите "Далее", чтобы увидеть последние новости Проектного офиса',
        keyboard=keyboard_gen([[{'text': 'Далее', 'color': 'positive'}]])
    )
    await bp.branch.add(ans.from_id, 'news')


class NewsBranch(ClsBranch):
    @rule_disposal(ExitButtonPressed())
    async def exit_branch(self, ans: Message):
        await return_to_main_menu(ans)

    @rule_disposal(VBMLRule('выйти', lower=True))
    async def exit_branch_(self, ans: Message):
        await return_to_main_menu(ans)

    @rule_disposal(PayloadHasKey('page'))
    async def change_news_page(self, ans: Message):
        u = await UserState.get(uid=ans.from_id)

        if isinstance(u.context, str):
            u.context = ujson.loads(u.context)

        if 'page_num' not in u.context:
            u.context['page_num'] = 1

        payload = ujson.loads(ans.payload)
        page_num = u.context['page_num']

        if payload.get('page') == 'next':
            page_num += 1
        elif page_num <= 1:
            page_num = 1
        else:
            page_num -= 1

        news = await NewsList()
        news.make_text_and_keyboard(page_num=page_num)

        msg = news.get_text()
        kbrd = news.get_keyboard()

        await ans('Загружаем новости....', keyboard=keyboard_gen(EMPTY_KEYBOARD))
        await ans(message=msg, keyboard=keyboard_gen(kbrd))

        u.context['page_num'] = page_num
        await u.save()

    # TODO убрать заглушку и написать полноценный поиск
    @rule_disposal(PayloadRule({'selection': 'search'}))
    async def search_ictis_news(self, ans: Message):
        await ans(
            message='Извините, эта функция временно не доступна.\n'
                    'Вы можете увидеть последние новости в группе ИКТИБ ИТА ЮФУ ВКонтакте (https://vk.com/ictis_sfedu)'
        )
        await return_to_main_menu(ans)

    @rule_disposal(PayloadRule({'selection': 'next'}))
    async def send_news(self, ans: Message):
        news_list = await NewsList()
        news_list.make_text_and_keyboard()

        msg = news_list.get_text()
        kbrd = news_list.get_keyboard()

        u = await UserState.get(uid=ans.from_id)

        if isinstance(u.context, str):
            u.context = ujson.loads(u.context)

        u.context['page_num'] = 1
        await u.save()

        await ans(
            message=msg,
            keyboard=keyboard_gen(kbrd, one_time=True)
        )

    @rule_disposal(PayloadHasKey('news_id'))
    async def get_detailed_news_view(self, ans: Message):
        payload = PayloadHasKey.dispatch(ans.payload)

        news_list = await NewsList()
        msg, image_url = news_list.get_news_desc_and_img_by_id(_id=payload['news_id'].strip('{}'))

        photo_uploader = PhotoUploader(api=bp.api, generate_attachment_strings=True)

        img_data = await photo_uploader.get_data_from_link(link=image_url)
        attachment = await photo_uploader.upload_message_photo(img_data)

        await ans(message=msg, attachment=attachment)

    async def branch(self, ans: Message):
        pass


bp.branch.add_branch(NewsBranch, 'news')
