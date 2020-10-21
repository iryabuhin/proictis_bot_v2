from vkbottle import keyboard_gen
from vkbottle.bot import Blueprint, Message
from vkbottle.rule import PayloadRule, VBMLRule
from vkbottle.branch import ClsBranch, rule_disposal
from content.faq.handler_tools import detect_intent_texts
from google.api_core.exceptions import GoogleAPIError
from keyboards import MAIN_MENU_KEYBOARD, EXIT_BUTTON, EMPTY_KEYBOARD
from rules import ExitButtonPressed
from models import DBStoredBranch
from config import Config
from utils import return_to_main_menu

bp = Blueprint(name='faq')
bp.branch = DBStoredBranch()


@bp.on.message(PayloadRule({'selection': 'faq'}))
async def faq_wrapper(ans: Message):
    await ans('Задавайте свои вопросы как будто спрашиваете человека'
              'и я попытаюсь найти на них ответ!',
              keyboard=keyboard_gen([[EXIT_BUTTON]])
              )
    await bp.branch.add(ans.from_id, 'faq')


class FaqDialogflowBranch(ClsBranch):
    async def branch(self, ans: Message, *args):
        try:
            query_result = detect_intent_texts(
                Config.PROJECT_ID,
                ans.from_id,
                ans.text,
                'ru-RU'
            )
        # TODO add logging
        except GoogleAPIError as e:
            raise GoogleAPIError(e)
        except ValueError as e:
            raise ValueError(e)
        else:
            msg = query_result.get('fulfillmentText')
            await ans(msg, keyboard=keyboard_gen([[EXIT_BUTTON]], one_time=False))

    @rule_disposal(VBMLRule('выйти', lower=True))
    async def exit_branch(self, ans: Message):
        await return_to_main_menu(ans)

    @rule_disposal(ExitButtonPressed())
    async def exit_branch(self, ans: Message):
        await ans(
            message='За дополнительной информацией вы всегда можете обратиться к наставникам '
                    'или на сайт Проектного офиса',
            keyboard=keyboard_gen(EMPTY_KEYBOARD, one_time=False)
        )
        await return_to_main_menu(ans)


bp.branch.add_branch(FaqDialogflowBranch, 'faq')
