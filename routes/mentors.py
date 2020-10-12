from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from vkbottle.branch import ClsBranch, rule_disposal
from vkbottle.rule import VBMLRule, LevenshteinDisRule, PayloadRule
from vkbottle.keyboard import Keyboard, Text, OpenLink, keyboard_gen
from bot import photo_uploader
from proictis_api.mentors import MentorMessageCard, MentorNotFoundException
from models.user_state import DBStoredBranch
from keyboards import MAIN_MENU_KEYBOARD

try:
    import ujson as json
except ImportError:
    import json


KEYBOARD = [
    [
        {
            'text': 'Выйти',
            'color': 'primary',
            'payload': "{\"command\": \"exit\"}"
        }
    ]
]


bp = Blueprint(name='mentors')
bp.branch = DBStoredBranch()

@bp.on.message(
    VBMLRule('наставники', lower=True)
)
async def wrapper(ans: Message):
    await bp.branch.add(ans.from_id, 'mentors')
    await ans('Вы можете узнать о наставнике отправив мне его/её фамилию.\n'
          'Если я смогу найти наставника с такой фамилией, я покажу вам информацию о нем'
          'и его контактные данные.',
        keyboard=keyboard_gen(KEYBOARD, one_time=True))


class MentorInfoBranch(ClsBranch):
    @rule_disposal(VBMLRule('выйти', lower=True))
    async def exit_branch(self, ans: Message):
        await ans(
            'Дополнительную информацию о наставниках вы всегда можете найти на сайте Проектного офиса.',
            keyboard=keyboard_gen(MAIN_MENU_KEYBOARD, inline=True)
        )
        await bp.branch.exit(ans.peer_id)

    async def branch(self, ans: Message):
        surname = ans.text.split()[0]
        try:
            # awaitable constructors WON'T WORK without
            # decorator provided by asyncinit pip pkg
            card = (await MentorMessageCard(surname)).as_tuple()

        except MentorNotFoundException:
            await ans(
                'Извините, я не могу найти наставника с такой фамилией.\n'
                'Вы можете спросить меня еще раз, отправив фамилию наставника.\n\n'
                'Чтобы закончить, нажмите кнопку "Выйти".',
                keyboard=keyboard_gen(KEYBOARD, one_time=True)
                )
            return

        card_text, avatar_link, doc_link = card

        photo_data = await photo_uploader.get_data_from_link(link=avatar_link)
        pic = await photo_uploader.upload_message_photo(photo_data)

        temp_kbrd = KEYBOARD
        temp_kbrd.append([
                {
                    'type': 'open_link',
                    'label': 'Больше информации о наставнике',
                    'link': doc_link
                }
            ]
        )

        await ans(card_text, attachment=pic, keyboard=keyboard_gen(temp_kbrd, one_time=True))


bp.branch.add_branch(MentorInfoBranch, 'mentors')
