import aiohttp
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from vkbottle.branch import ClsBranch, rule_disposal
from vkbottle.rule import VBMLRule, PayloadRule
from vkbottle.keyboard import keyboard_gen
from bot import photo_uploader
from config import Config
from content.mentors import MentorMessageCard, MentorNotFoundException
from models import DBStoredBranch, UserState
from keyboards import MAIN_MENU_KEYBOARD, EMPTY_KEYBOARD, EXIT_BUTTON
from utils import fetch_json, return_to_main_menu

try:
    import ujson as json
except ImportError:
    import json


bp = Blueprint(name='mentors')
bp.branch = DBStoredBranch()


@bp.on.message(PayloadRule({'selection': 'mentors'}))
async def wrapper(ans: Message):
    await bp.branch.add(ans.from_id, 'mentors')
    await ans(
        'Вы можете узнать о наставнике отправив мне его/её фамилию.\n'
        'Если я смогу найти наставника с такой фамилией, я покажу вам информацию о нем'
        'и его контактные данные.',
        keyboard=keyboard_gen([[EXIT_BUTTON]], one_time=True)
    )


class MentorInfoBranch(ClsBranch):
    @rule_disposal(VBMLRule('выйти', lower=True))
    async def exit_branch(self, ans: Message):
        await ans(
            'Дополнительную информацию о наставниках вы всегда можете найти на сайте Проектного офиса.\n'
            '(https://proictis.sfedu.ru)',
            keyboard=keyboard_gen(EMPTY_KEYBOARD)
        )
        await return_to_main_menu(ans)

    async def branch(self, ans: Message):
        surname = ans.text.split()[0]
        try:

            data = await fetch_json(Config.BASE_API_URL + Config.URL_PATH['mentors'])
            card = MentorMessageCard(data, surname)

        except aiohttp.ClientResponseError as e:
            print('[ERROR] HTTP Client Response Error occured: {}, {}'.format(
                e.status,
                e.message
            ))
            await ans(
                'Произошла ошибка при обработке запроса к API Проектного офиса, возможно, он временно недоступен.\n'
                'Если эта ошибка возникает продолжительно в течение более чем нескольких часов, обратитесь к администрации сайта.',
                keyboard=keyboard_gen(EMPTY_KEYBOARD)
            )

        except MentorNotFoundException:
            await ans(
                'Извините, я не могу найти наставника с такой фамилией.\n'
                'Вы можете спросить меня еще раз, отправив фамилию наставника.\n\n'
                'Чтобы закончить, нажмите кнопку "Выйти".',
                keyboard=keyboard_gen([[EXIT_BUTTON]], one_time=False)
                )
            return

        card_text, avatar_link, doc_link = card.as_tuple()

        photo_data = await photo_uploader.get_data_from_link(link=avatar_link)
        pic = await photo_uploader.upload_message_photo(photo_data)

        temp_kbrd = [[EXIT_BUTTON]]
        temp_kbrd.append([
                {
                    'type': 'open_link',
                    'label': 'Больше информации о наставнике',
                    'link': doc_link
                }
            ]
        )

        await ans(message=card_text, attachment=pic)
        await ans('Введите фамилию наставника, о котором хотели бы узнать или нажмите "Выйти", чтобы вернуться в главное меню',
                  keyboard=keyboard_gen(temp_kbrd, one_time=True))


bp.branch.add_branch(MentorInfoBranch, 'mentors')
